import json
from enum import Enum
from typing import Optional, Any, Dict, Union
from ..types import BaseMessage

# from ..logger import logger


class QueueRole(Enum):
    Publisher = 1
    Receiver = 2


class QueueMessageType(Enum):
    Task = 1
    ReportTaskStatus = 2  # to scheduler
    StorageInvalidation = 3
    Stop = 4
    ProcessIteration = 5
    DelayedTask = 6
    ReportEvaluation = 7  # to scheduler


class QueueMessage:
    session_id: str
    type: QueueMessageType
    data: Optional[Union[BaseMessage, Dict[Any, Any]]] = None

    def __init__(self, session_id: str, message_type: QueueMessageType, data=None):
        self.session_id = session_id
        self.type = message_type
        self.data = data

    def encode(self):
        # logger.info( f'encoding {self.type=} {self.data=}')
        return json.dumps(
            {
                "session_id": self.session_id,
                "type": self.type.value,
                "data": json.dumps(self.data.to_dict() if isinstance(self.data, BaseMessage) else self.data),
            }
        ).encode()

    @staticmethod
    def decode(binary):
        j = json.loads(binary.decode())
        res = QueueMessage(
            session_id=j["session_id"], message_type=QueueMessageType(j["type"]), data=json.loads(j["data"])
        )
        return res


class QueueTopicMessage:
    def __init__(self, topic, data: BaseMessage):
        self.topic = topic.split(".")
        self.data = data

    def encode(self):
        # logger.info( f'encoding {self.type=} {self.data=}')
        return json.dumps({"data": json.dumps(self.data.to_dict())}).encode()

    @staticmethod
    def decode(topic, binary):
        j = json.loads(binary.decode())
        res = QueueTopicMessage(topic=topic, data=json.loads(j["data"]))
        return res
