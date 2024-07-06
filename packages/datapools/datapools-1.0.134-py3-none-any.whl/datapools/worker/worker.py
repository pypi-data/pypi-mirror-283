import asyncio
from enum import Enum
import time
import importlib
import tempfile
import inspect
import os
import re
import sys

import traceback
import uuid
from typing import Optional, Set, List, Tuple, Any, Dict, NamedTuple

from ..common.backend_api import BackendAPI
from ..common.logger import logger
from ..common.queues import (
    GenericQueue,
    QueueMessage,
    QueueMessageType,
    QueueRole,
    QueueTopicMessage,
    MESSAGE_HIGH_PRIORITY,
    MESSAGE_NORMAL_PRIORITY,
)

from ..common.session_manager import SessionManager, Session, SessionStatus, URLState, ContentStatus, ContentState
from ..common.stoppable import Stoppable
from ..common.storage import FileStorage
from ..common.types import (
    CrawlerBackTask,
    CrawlerContent,
    CrawlerDemoUser,
    CrawlerHintURLStatus,
    CrawlerNop,
    DatapoolContentType,
    InvalidUsageException,
    WorkerSettings,
    WorkerTask,
    DelayedWorkerTask,
    WorkerEvaluationReport,
    ProducerTask,
    EvaluationStatus,
)
from .types import WorkerContext, YieldResult
from .plugins.base_plugin import BasePlugin, UnexpectedContentTypeException, BaseReader, BaseReaderException
from .utils import get_storage_invalidation_topic


class WorkerFileStorage(FileStorage):
    def __init__(self, dstpath, worker_id):
        super().__init__(os.path.join(dstpath, worker_id))


class PluginData(NamedTuple):
    cls: Tuple[str, Any]
    lock: asyncio.Lock
    objs: List[BasePlugin]
    params: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None


class LoopResult(Enum):
    WorkerStopped = 1
    SessionClosed = 2
    PluginException = 3


MAX_INSTANCES_ERROR = -1


class CrawlerWorker(Stoppable):
    id: str
    cfg: WorkerSettings
    demo_users: dict[str, dict[str, str]]
    api: BackendAPI
    session_manager: SessionManager
    storage: WorkerFileStorage
    hp_todo_tasks: Set[asyncio.Task]
    lp_todo_tasks: Set[asyncio.Task]
    plugins: List[PluginData]
    hp_todo_queue_r: GenericQueue
    lp_todo_queue_r: GenericQueue
    lp_todo_queue_w: GenericQueue
    reports_queue: GenericQueue
    producer_queue: GenericQueue
    topics_queue: GenericQueue
    stop_task_received: Optional[asyncio.Event] = None

    def __init__(self, cfg: Optional[WorkerSettings] = None):
        super().__init__()
        self.id = uuid.uuid4().hex
        logger.info(f"worker id={self.id}")

        self.cfg = cfg if cfg is not None else WorkerSettings()

        self.demo_users = {}
        self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)

        self.session_manager = self._get_session_manager()

        # Worker storage must be separated from other workers
        # so default schema when path is $STORAGE_PATH/$storage_id does not work here.
        # Using $STORAGE_PATH/$worker_id/$storage_id path
        self.storage = WorkerFileStorage(self.cfg.STORAGE_PATH, self.id)

        self.hp_todo_tasks = set()
        self.lp_todo_tasks = set()

        self.init_plugins()
        self.hp_todo_queue_r = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.WORKER_HP_TASKS_QUEUE_NAME,
            size=self.cfg.MAX_TOTAL_PROCESSING_TASKS - self.cfg.MAX_LOW_PRIORITY_PROCESSING_TASKS,
            max_priority=MESSAGE_HIGH_PRIORITY,
        )
        logger.info(f"created receiver {self.cfg.WORKER_HP_TASKS_QUEUE_NAME}")
        self.lp_todo_queue_r = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.WORKER_LP_TASKS_QUEUE_NAME,
            size=self.cfg.MAX_LOW_PRIORITY_PROCESSING_TASKS,
        )
        logger.info(f"created receiver {self.cfg.WORKER_LP_TASKS_QUEUE_NAME}")

        self.lp_todo_queue_w = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.WORKER_LP_TASKS_QUEUE_NAME,
        )
        logger.info(f"created publisher {self.cfg.WORKER_LP_TASKS_QUEUE_NAME}")

        self.reports_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.REPORTS_QUEUE_NAME,
        )
        logger.info("created publisher reports")
        self.producer_queue = GenericQueue(
            role=QueueRole.Publisher,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.EVAL_TASKS_QUEUE_NAME,
        )
        logger.info("created publisher eval_tasks")
        self.topics_queue = GenericQueue(
            role=QueueRole.Receiver,
            url=self.cfg.QUEUE_CONNECTION_URL,
            name=self.cfg.TOPICS_QUEUE_NAME,
            topic=get_storage_invalidation_topic(self.id),
        )
        logger.info("created receiver topics")

        if self.cfg.CLI_MODE is True:
            self.stop_task_received = asyncio.Event()

    def run(self):
        # self.tasks.append( asyncio.create_task( self.tasks_fetcher_loop() ) )
        self.hp_todo_queue_r.run()
        self.lp_todo_queue_r.run()
        self.lp_todo_queue_w.run()
        self.reports_queue.run()
        self.producer_queue.run()
        self.topics_queue.run()
        self.tasks.append(asyncio.create_task(self.worker_loop()))
        # self.tasks.append(asyncio.create_task(self.delayed_tasks_loop()))
        self.tasks.append(asyncio.create_task(self.topics_loop()))
        super().run()

    async def wait(self):
        """for CLI mode usage only"""
        if self.cfg.CLI_MODE is False:
            logger.error("worker invalid usage")
            raise InvalidUsageException("not a cli mode")
        logger.info("CrawlerWorker wait()")
        await self.stop_task_received.wait()
        logger.info("CrawlerWorker stop_task_received")
        waiters = (
            self.hp_todo_queue_r.until_empty(),
            self.lp_todo_queue_r.until_empty(),
            self.lp_todo_queue_w.until_empty(),
            self.reports_queue.until_empty(),
            self.producer_queue.until_empty(),
            self.topics_queue.until_empty(),
        )
        await asyncio.gather(*waiters)
        logger.info("CrawlerWorker wait done")

    async def stop(self):
        logger.info("worker::stop")
        await super().stop()
        logger.info("super stopped")

        logger.info("waiting todo tasks..")
        while len(self.hp_todo_tasks) > 0 or len(self.lp_todo_tasks) > 0:
            await asyncio.sleep(0.2)
        logger.info("todo tasks done")

        await self.hp_todo_queue_r.stop()
        logger.info("hp_todo queue_r stopped")
        await self.lp_todo_queue_r.stop()
        logger.info("lp_todo queue_r stopped")
        await self.lp_todo_queue_w.stop()
        logger.info("lp_todo queue_w stopped")
        await self.reports_queue.stop()
        logger.info("reports queue stopped")
        await self.producer_queue.stop()
        logger.info("producer queue stopped")
        await self.topics_queue.stop()
        logger.info("topics queue stopped")

        # for plugin_data in self.plugins:
        #     if plugin_data[0] is not None:
        #         logger.info( f'clearing plugin {plugin_data[1]}')
        #         plugin_data[0] = None
        #         plugin_data[1] = None

        logger.info("worker stopped")

    def _get_session_manager(self):
        return SessionManager(self.cfg.REDIS_HOST, self.cfg.REDIS_PORT)

    def init_plugins(self):
        self.plugins = []
        plugin_names = []

        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
        logger.info(f"{plugins_dir=}")

        internal_plugins = []
        for dir_name in os.listdir(plugins_dir):
            if dir_name != "__pycache__" and os.path.isdir(os.path.join(plugins_dir, dir_name)):
                internal_plugins.append(dir_name)
                if self.cfg.USE_ONLY_PLUGINS is None or dir_name in self.cfg.USE_ONLY_PLUGINS:
                    name = f"datapools.worker.plugins.{dir_name}"
                    plugin_names.append(name)

        if self.cfg.ADDITIONAL_PLUGINS is not None:
            for name in self.cfg.ADDITIONAL_PLUGINS:
                if importlib.util.find_spec(name):
                    plugin_names.append(name)

        for name in plugin_names:
            if name not in sys.modules:
                logger.info(f"loading module {name}")
                module = importlib.import_module(name)
            else:
                logger.info(f"RE-loading module {name}")
                module = importlib.reload(sys.modules[name])

            clsmembers = inspect.getmembers(module, inspect.isclass)

            for cls in clsmembers:
                for base in cls[1].__bases__:
                    if base.__name__ == "BasePlugin":
                        (params, config) = self._get_plugin_config_entry(cls[0])
                        self.plugins.append(
                            PluginData(cls=cls, lock=asyncio.Lock(), params=params, config=config, objs=[])
                        )
                        break

    async def topics_loop(self):
        # from Producer.Evaluator - receives storage_id which content can be removed
        try:
            while not await self.is_stopped():
                message = await self.topics_queue.pop(timeout=1)
                if message:
                    qm = QueueTopicMessage.decode(message.routing_key, message.body)
                    expected_routing_key = get_storage_invalidation_topic(self.id)
                    logger.info(f"topics_loop {message.routing_key=} {expected_routing_key=}")
                    if message.routing_key == expected_routing_key:
                        report = WorkerEvaluationReport(**qm.data)
                        logger.info(f"got producer {report=}")
                        if not report.is_shared_storage and report.status == EvaluationStatus.Success:
                            await self.storage.remove(report.storage_id)

                        await self.topics_queue.mark_done(message)
                    elif message.redelivered is False:  # TODO: anyway, why is it delivered to me?
                        logger.error(f"!!!!!!!!!!!!!!! BUG: unexpected topic {message=} {qm=} {expected_routing_key=}")
                        await self.topics_queue.reject(message, requeue=False)
        except Exception as e:
            logger.error(f"!!!!!!!!Exception in topics_loop() {e}")
            logger.error(traceback.format_exc())
        finally:
            logger.info("topics_loop done")

    # async def delayed_tasks_loop(self):
    #     timeout = 5
    #     while not await self.is_stopped(timeout=timeout):
    #         timeout = 5
    #         message = await self.delayed_todo_queue_r.pop(timeout=1)
    #         if message:
    #             logger.info(f"got delayed {message=}")
    #             qm = QueueMessage.decode(message.body)
    #             logger.info(f"{qm.data=}")

    #             session = await self.session_manager.get(qm.session_id)
    #             if not session or not await session.is_alive():
    #                 logger.error(f"Session not found or done {qm.session_id}")
    #                 await self.delayed_todo_queue_r.reject(message, requeue=False)
    #                 timeout = 0
    #             elif qm.type == QueueMessageType.DelayedTask:
    #                 diff = int(time.time()) - qm.data["timestamp"]
    #                 logger.info(f"delayed task time {diff=}")
    #                 if diff > self.cfg.DELAYED_TASK_REQUEUE_PERIOD:
    #                     logger.info("enqueue task back to the main worker queue")
    #                     await self.todo_queue_w.push(QueueMessage(qm.session_id, QueueMessageType.Task, qm.data))

    #                     await self.delayed_todo_queue_r.mark_done(message)
    #                     timeout = 0
    #                 else:
    #                     await self.delayed_todo_queue_r.reject(message)
    #             else:
    #                 logger.error(f"BUG: unexpected delayed message {qm=}")
    #                 await self.delayed_todo_queue_r.reject(message, requeue=False)

    async def worker_loop(self):
        # fetches urls one by one from the queue and scans them using available plugins
        try:

            def on_hp_done(task):
                logger.info(f"_process_todo_message done {task=}")
                self.hp_todo_tasks.discard(task)
                logger.info(f"HP {len(self.hp_todo_tasks)} still working")

            def on_lp_done(task):
                logger.info(f"_process_todo_message done {task=}")
                self.lp_todo_tasks.discard(task)
                logger.info(f"LP {len(self.lp_todo_tasks)} still working")

            while not await self.is_stopped():
                if len(self.hp_todo_tasks) + len(self.lp_todo_tasks) >= self.cfg.MAX_TOTAL_PROCESSING_TASKS:
                    logger.info("max tasks, no pop..")
                    await asyncio.sleep(3)
                    continue
                message = await self.hp_todo_queue_r.pop(timeout=1)
                if message:
                    task = asyncio.create_task(self._process_todo_message(message))
                    task.add_done_callback(on_hp_done)
                    self.hp_todo_tasks.add(task)
                else:
                    if len(self.lp_todo_tasks) < self.cfg.MAX_LOW_PRIORITY_PROCESSING_TASKS:
                        message = await self.lp_todo_queue_r.pop(timeout=0.2)
                        if message:
                            task = asyncio.create_task(self._process_todo_message(message))
                            task.add_done_callback(on_lp_done)
                            self.lp_todo_tasks.add(task)

        except Exception as e:
            logger.error(f"!!!!!!!!Exception in worker_loop() {e}")
            logger.error(traceback.format_exc())
        finally:
            logger.info("worker loop done")

    async def loop_done(self, session: Session) -> LoopResult | None:
        if await self.is_stopped():
            return LoopResult.WorkerStopped
        if not await session.is_alive():
            return LoopResult.SessionClosed
        return None

    async def _process_todo_message(self, message):

        heartbeat_stop: asyncio.Event = None
        heartbeat_task: asyncio.Task = None

        async def heartbeat(session_id):
            try:
                sm = self._get_session_manager()  # separate redis connection
                session = await sm.get(session_id)
                while not heartbeat_stop.is_set():
                    await session.add_heartbeat(self.id)
                    await asyncio.sleep(1)
            except Exception:
                logger.error(f"Exception in heartbeat {self.id}")
                logger.error(traceback.format_exc())

        try:
            qm = QueueMessage.decode(message.body)

            session = await self.session_manager.get(qm.session_id)
            if not session or not await session.is_alive():
                logger.error(f"Session not found or done {qm.session_id}")
                await self._reject_message(message, requeue=False)
                return

            if qm.type == QueueMessageType.Task or qm.type == QueueMessageType.DelayedTask:
                if qm.type == QueueMessageType.DelayedTask:
                    delayed_task = DelayedWorkerTask(**qm.data)
                    diff = int(time.time()) - delayed_task.timestamp
                    logger.info(f"delayed task time {diff=}")
                    if diff < self.cfg.DELAYED_TASK_REDO_PERIOD:
                        # it's not time to process this task, postpone it again
                        await self._add_delayed_task(qm.session_id, delayed_task, message)
                        return

                task = WorkerTask(**qm.data)
                logger.info(f"got {message=}")
                logger.info(f"got {task=} {qm.session_id=}")

                status = await session.get_status()

                logger.info(f"processing {task.url=}")

                # check if this message is not resent by rabbitmq as ack-timeouted
                if message.redelivered is True:
                    url_state = await session.get_url_state(task.url)
                    if url_state is None:  # should not be possible..
                        logger.error(f"url state not found for {task.url=}")
                        await self._reject_message(message, requeue=False)
                        return

                    if url_state.status not in (CrawlerHintURLStatus.Unprocessed, CrawlerHintURLStatus.Processing):
                        logger.error(f"url already processed: {task.url=} {url_state.status=} {url_state.worker_id=}")
                        await self._reject_message(message, requeue=False)
                        return

                    if url_state.worker_id:
                        logger.info(f"{url_state.worker_id=}")
                        if url_state.worker_id == self.id:  # we are procesing this message already, ignoring
                            logger.info(f"already processing task {task.url=}, ignore")
                            await self._add_delayed_task(qm.session_id, task, message)
                            return
                        if await self._is_worker_alive(url_state.worker_id, session):
                            logger.info(f"worker still alive on {task.url=}")
                            await self._add_delayed_task(qm.session_id, task, message)
                            return
                        logger.info(f"it's dead, accepting task {task.url=}")

                await session.set_url_state(
                    task.url, URLState(worker_id=self.id, status=CrawlerHintURLStatus.Processing)
                )
                heartbeat_stop = asyncio.Event()
                heartbeat_task = asyncio.Task(heartbeat(session.id))

                plugin = await self._get_url_plugin(task, session)

                if plugin is None:
                    logger.info("suitable plugin not found")
                    await self._reject_message(message, requeue=False)
                    return

                if plugin == MAX_INSTANCES_ERROR:
                    logger.info(f"MAX_INSTANCES {session.id=}")
                    await self._add_delayed_task(qm.session_id, task, message)
                    return

                logger.info(f"suitable {plugin=}")

                loop_result: LoopResult | None = None
                try:
                    async for process_res in plugin.process(task):
                        # logger.info( f'{type( process_res )=}')
                        t = type(process_res)
                        # logger.info( f'{(t is CrawlerNop)=}')

                        loop_result = await self.loop_done(session)
                        if loop_result is not None:
                            if loop_result == LoopResult.SessionClosed:
                                logger.info(f"Session is stopped/deleted, breaking. {qm.session_id=}")
                            elif loop_result == LoopResult.WorkerStopped:
                                logger.debug("worker stopped, breaking")
                            break

                        if t is CrawlerContent:
                            await self._process_crawled_content(process_res, session, plugin, task)
                        elif t is CrawlerBackTask:
                            await self._add_back_task(qm.session_id, process_res)
                        elif t is CrawlerDemoUser:
                            ct: CrawlerDemoUser = process_res
                            if ct.platform not in self.demo_users:
                                self.demo_users[ct.platform] = {}
                            if ct.user_name not in self.demo_users[ct.platform]:
                                logger.info(f"============= adding demo user {dict(ct)} ===========")
                                await self.api.add_demo_user(dict(ct))
                                self.demo_users[ct.platform][ct.user_name] = ct.short_tag_id

                        elif t is CrawlerNop:
                            pass
                        else:
                            raise Exception(f"unknown {process_res=}")

                        await self._notify_process_iteration(qm.session_id)
                except Exception:
                    logger.error("Exception in plugin loop")
                    logger.error(traceback.format_exc())
                    loop_result = LoopResult.PluginException

                logger.info(f"plugin.process done {loop_result=}")

                plugin.is_busy = False

                if loop_result is None:  # task fully processed by plugin
                    logger.info(f"sending ack for {message.message_id=}")
                    await self._mark_done_message(message)
                    await session.set_url_status(task.url, CrawlerHintURLStatus.Success)
                    await self._report_task_status(session, task, CrawlerHintURLStatus.Success)
                else:
                    logger.info(f"sending reject for {message.message_id=} {loop_result=} ")
                    await self._reject_message(message, requeue=loop_result == LoopResult.WorkerStopped)
                    status = (
                        CrawlerHintURLStatus.Failure
                        if loop_result != LoopResult.SessionClosed
                        else CrawlerHintURLStatus.Canceled
                    )
                    await session.set_url_status(task.url, status)
                    await self._report_task_status(session, task, status)

            elif qm.type == QueueMessageType.Stop:
                await self._mark_done_message(message)
                logger.info("worker: got stop task")

                await self.producer_queue.push(QueueMessage(qm.session_id, QueueMessageType.Stop))
                # notifying scheduler that we are done
                await self.reports_queue.push(QueueMessage(qm.session_id, QueueMessageType.Stop))
                self.stop_task_received.set()

            else:
                logger.error(f"!!!!!!!!!!!!!!! BUG: unexpected {message=} {qm=}")
                await self._reject_message(message)
        except Exception:
            logger.error("unhandled exception in _process_todo_message")
            logger.error(traceback.format_exc())
            raise
        finally:
            if heartbeat_task is not None:
                # logger.info("waiting for heartbeat ends")
                heartbeat_stop.set()
                await heartbeat_task
                # logger.info("heartbeat done")

    async def _mark_done_message(self, message):
        if message.routing_key == self.cfg.WORKER_HP_TASKS_QUEUE_NAME:
            await self.hp_todo_queue_r.mark_done(message)
        elif message.routing_key == self.cfg.WORKER_LP_TASKS_QUEUE_NAME:
            await self.lp_todo_queue_r.mark_done(message)
        else:
            raise Exception(f"BUG: mark_done_message eunknown routing key {message=}")

    async def _reject_message(self, message, requeue=True):
        if message.routing_key == self.cfg.WORKER_HP_TASKS_QUEUE_NAME:
            await self.hp_todo_queue_r.reject(message, requeue)
        elif message.routing_key == self.cfg.WORKER_LP_TASKS_QUEUE_NAME:
            await self.lp_todo_queue_r.reject(message, requeue)
        else:
            raise Exception(f"BUG: reject_message unknown routing key {message=}")

    async def _is_worker_alive(self, worker_id, session: Session):
        last_heartbeat = await session.get_heartbeat(worker_id)
        return time.time() - last_heartbeat < 60

    async def _report_task_status(self, session: Session, task: WorkerTask, status: CrawlerHintURLStatus):
        task.status = status
        await self.reports_queue.push(QueueMessage(session.id, QueueMessageType.ReportTaskStatus, task))

    async def _notify_process_iteration(self, session_id):
        await self.reports_queue.push(QueueMessage(session_id, QueueMessageType.ProcessIteration))

    async def _process_content_helper(
        self, cc: CrawlerContent, session: Session, url: str, storage_id: Optional[str] = None
    ) -> bool:
        res = False
        logger.info(f"process_content {type(cc.content)=}")
        if cc.content:
            if not cc.type:
                try:
                    cc.type = BasePlugin.get_content_type_by_content(cc.content)
                except UnexpectedContentTypeException:
                    logger.error("Unsupported content, skipped")

            logger.info(f"{cc.type=}")

            if cc.type:
                if not cc.tag_id:
                    # trying to parse author tag
                    if cc.type == DatapoolContentType.Image:
                        image_tag = BasePlugin.parse_image_tag(cc.content)
                        cc.tag_id = str(image_tag) if image_tag is not None else None
                        cc.tag_keepout = image_tag.is_keepout() if image_tag is not None else False
                    # TODO: add video/audio parsing here

                if cc.tag_id is not None or cc.copyright_tag_id is not None or cc.platform_tag_id is not None:

                    if storage_id is None:
                        storage_id = self.storage.gen_id(cc.url)
                        logger.info(f"putting to {storage_id=}")
                        await self.storage.put(storage_id, cc.content)

                        await session.set_content_state(
                            cc.url,
                            ContentState(
                                worker_id=self.id, status=ContentStatus.DOWNLOAD_SUCCESS, storage_id=storage_id
                            ),
                        )
                        await session.inc_crawled_content()

                    if cc.tag_id is not None:
                        await session.inc_tag_usage(cc.tag_id, cc.tag_keepout)
                    if cc.copyright_tag_id is not None:
                        await session.inc_tag_usage(cc.copyright_tag_id, cc.copyright_tag_keepout)
                    if cc.platform_tag_id is not None:
                        await session.inc_tag_usage(cc.platform_tag_id, cc.platform_tag_keepout)

                    # notifying producer about new crawled data
                    await self.producer_queue.push(
                        QueueMessage(
                            session.id,
                            QueueMessageType.Task,
                            ProducerTask(
                                **{
                                    "parent_url": url,
                                    "url": cc.url,
                                    "storage_id": storage_id,
                                    "tag_id": cc.tag_id,
                                    "tag_keepout": cc.tag_keepout,
                                    "copyright_tag_id": cc.copyright_tag_id,
                                    "copyright_tag_keepout": cc.copyright_tag_keepout,
                                    "platform_tag_id": cc.platform_tag_id,
                                    "platform_tag_keepout": cc.platform_tag_keepout,
                                    "type": DatapoolContentType(cc.type).value,
                                    "priority_timestamp": cc.priority_timestamp,
                                    "worker_id": self.id,
                                }
                            ),
                        )
                    )
                    res = True
                else:
                    logger.info("no tag available")
            else:
                logger.info("unknown content type")
        else:
            logger.info("no content")

        return res

    async def _process_crawled_content(
        self, cc: CrawlerContent, session: Session, plugin: BasePlugin, task: WorkerTask
    ):
        no_tagged_content = True
        content_ok = False
        is_content_ignored = False
        content_state = await session.get_content_state(cc.url)
        logger.info(f"_process_crawled_content {content_state=}")
        if content_state is None or (
            content_state.status == ContentStatus.DOWNLOAD_SUCCESS
            and (not content_state.storage_id or not await self.storage.has(content_state.storage_id))
        ):

            last_check = 0
            is_stopped = False

            async def stopper():
                nonlocal is_stopped
                if time.time() - last_check > 1:
                    is_stopped = await self.is_stopped() or not await session.is_alive()
                    return is_stopped
                return False

            if not cc.content:
                logger.info("no content, downloading from url")
                with tempfile.TemporaryFile("wb+") as tmp:
                    try:
                        async for chunk in plugin.async_read_url(cc.url, expected_type=cc.type):
                            tmp.write(chunk)
                            if await stopper():
                                is_stopped = True
                                break
                        cc.content = tmp
                        content_ok = True
                    except UnexpectedContentTypeException as e:
                        logger.error(f"Unexpected content type: {str(e)}")

                    if content_ok and not is_stopped:
                        if await self._process_content_helper(cc, session, task.url):
                            no_tagged_content = False

            elif isinstance(cc.content, BaseReader):
                logger.info("content is BaseReader instance")

                with tempfile.TemporaryFile("wb+") as tmp:
                    logger.info("read_to tmp")
                    try:
                        await cc.content.read_to(tmp, stopper)
                        content_ok = True
                        logger.info("read_to done")
                    except BaseReaderException as e:
                        logger.error(f"Reader failure: {e}")

                    if content_ok and not is_stopped:
                        cc.content = tmp
                        if await self._process_content_helper(cc, session, task.url):
                            no_tagged_content = False
            else:
                if await self._process_content_helper(cc, session, task.url):
                    no_tagged_content = False
                    content_ok = True

        elif content_state.status in (ContentStatus.DOWNLOAD_SUCCESS, ContentStatus.EVALUATION_FAILURE):
            # content was downloaded and put into storage, but not evaluated yet
            logger.info(f"content already downloaded for {cc.url=}")
            with self.storage.get_reader(content_state.storage_id) as r:
                cc.content = r
                if await self._process_content_helper(cc, session, task.url, content_state.storage_id):
                    no_tagged_content = False
                    content_ok = True
        elif content_state.status == ContentStatus.EVALUATION_SUCCESS:
            logger.info(f"content url evaluated already {cc.url=}")
            is_content_ignored = True
        elif content_state.status == ContentStatus.DOWNLOAD_INVALID:
            logger.info(f"content url downloaded earlier, but it's invalid {cc.url=}")
            is_content_ignored = True
        else:
            raise Exception(f"BUG: unknown status {content_state=}")

        # Stats for scheduler decision whether to continue crawling or not
        if is_content_ignored is False:
            if no_tagged_content:
                logger.info("inc_since_last_tagged")
                await session.inc_since_last_tagged()

                await session.set_content_state(
                    cc.url,
                    ContentState(worker_id=self.id, status=ContentStatus.DOWNLOAD_INVALID),
                )
            else:
                logger.info("reset_since_last_tagged")
                await session.reset_since_last_tagged()
            plugin.ctx.yield_result = (
                YieldResult.ContentDownloadSuccess if content_ok else YieldResult.ContentDownloadFailure
            )
        else:
            plugin.ctx.yield_result = YieldResult.ContentIgnored
        # n = await session.get_since_last_tagged()
        # logger.info(f"get_since_last_tagged: {n}")

    async def _add_back_task(self, session_id, task: CrawlerBackTask):
        logger.info(f"sending back task '{task.url=}' in '{session_id=}'")
        await self.reports_queue.push(QueueMessage(session_id, QueueMessageType.Task, task))

    async def _add_delayed_task(self, session_id, task: WorkerTask | DelayedWorkerTask, message):
        if type(task).__name__ == "WorkerTask":  # because of inheritance cannot use isinstance(task, WorkerTask)
            task = DelayedWorkerTask(**task.to_dict(), timestamp=int(time.time()))

        await self._mark_done_message(message)
        # await asyncio.sleep(5)  # avoid frequent pops from the queue
        await self.lp_todo_queue_w.push(QueueMessage(session_id, QueueMessageType.DelayedTask, task))

    def _get_plugin_object(self, cls, session: Session) -> BasePlugin:
        ctx = WorkerContext(session=session)  # type: ignore

        args = [ctx]
        kwargs = {}
        logger.info(f"_get_plugin_object {cls=}")

        # convert class name into config plugins key
        # example: GoogleDrivePlugin => google_drive
        # example: S3Plugin => s3
        (params, __config) = self._get_plugin_config_entry(cls[0])
        if params is not None:
            # plugin config dict keys must match plugin's class __init__ arguments
            kwargs = params

        return cls[1](*args, **kwargs)

    def _get_plugin_config_entry(self, cls_name):
        cap_words = re.sub(r"([A-Z])", r" \1", cls_name).split()
        # logger.info(f'{cap_words=}')
        config_key = "_".join(list(map(lambda x: x.lower(), cap_words[:-1])))
        # logger.info(f'{config_key=}')
        config_entry = self.cfg.plugins_config.get(config_key)
        if config_entry is not None:
            logger.info(config_entry)
            params = {k: v for k, v in config_entry.items() if k != "config"}
            config = config_entry.get("config")
            return (params, config)
        return (None, None)

    async def _get_url_plugin(self, task: WorkerTask, session: Session):

        def get_free_obj(plugin_data: PluginData):
            for obj in plugin_data.objs:
                if not obj.is_busy:
                    return obj
            return None

        for plugin_data in self.plugins:
            if plugin_data.cls[0] != "DefaultPlugin":
                if plugin_data.cls[1].is_supported(task.url):
                    logger.info(f"{plugin_data.cls[0]} supports {task.url}")
                    async with plugin_data.lock:
                        max_instances = None
                        if plugin_data.config is not None:
                            max_instances = plugin_data.config.get("max_instances")
                        if max_instances is None:
                            max_instances = self.cfg.MAX_PLUGIN_INSTANCES_DEFAULT

                        logger.info(f"{plugin_data.cls[0]} {max_instances=}")

                        obj = get_free_obj(plugin_data)
                        if obj is None:
                            if max_instances is not None:
                                busy_count = plugin_data.cls[1].get_busy_count()
                                logger.info(f"{plugin_data.cls[0]} {busy_count=}")
                                if busy_count >= max_instances:
                                    logger.info(f"{plugin_data.cls[0]} max instances reached, {max_instances=}")
                                    return MAX_INSTANCES_ERROR

                            obj = self._get_plugin_object(plugin_data.cls, session)
                            obj.is_busy = True
                            plugin_data.objs.append(obj)
                        else:
                            obj.is_busy = True
                        logger.info(f"returning {obj=}")
                        return obj

        # creating/using existing default plugin
        for plugin_data in self.plugins:
            if plugin_data.cls[0] == "DefaultPlugin":
                if plugin_data.cls[1].is_supported(task.url):
                    async with plugin_data.lock:
                        max_instances = None
                        if plugin_data.config is not None:
                            max_instances = plugin_data.config.get("max_instances")

                        obj = get_free_obj(plugin_data)
                        if obj is None:
                            if max_instances is not None:
                                busy_count = plugin_data.cls[1].get_busy_count()
                                if busy_count >= max_instances:
                                    # logger.info(f"max instances reached, {max_instances=}")
                                    return MAX_INSTANCES_ERROR

                            obj = self._get_plugin_object(plugin_data.cls, session)
                            obj.is_busy = True
                            plugin_data.objs.append(obj)
                        else:
                            obj.is_busy = True
                        return obj
                return None
