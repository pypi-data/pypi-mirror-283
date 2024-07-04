import base64
import io
import sys
from abc import ABCMeta, abstractmethod
from hashlib import md5
from time import time
from typing import AsyncGenerator, Union, Optional, Callable
from urllib.parse import urljoin, urlparse
import magic
from dateutil import parser as date_parser
from datetime import datetime

import dns.resolver
import httpx
from PIL import Image
from PIL.ExifTags import Base as ExifTagsList

from ...common.logger import logger
from ...common.types import (
    BaseCrawlerResult,
    CrawlerBackTask,
    DatapoolContentType,
    WorkerTask,
)
from ..utils import canonicalize_url
from ..types import WorkerContext

MAGIC_MIN_BYTES = 512


try:
    from bs4 import BeautifulSoup
except ImportError:
    pass
try:
    from playwright.async_api import Page
except ImportError:
    pass
import re


class BasePluginException(Exception):
    pass


class UnexpectedContentTypeException(BasePluginException):
    pass


class BaseTag:
    _tag: Optional[str] = None
    _is_keepout: Optional[bool] = None

    def __init__(self, tag, keepout=False):
        self._tag = tag
        self._is_keepout = keepout

    def __str__(self):
        return self._tag

    def __repr__(self):
        return f"BaseTag(tag={self._tag}, keepout={self._is_keepout})"

    def is_keepout(self):
        return self._is_keepout

    def is_valid(self):
        return type(self._tag) is str


class CachedPairs:
    def __init__(self):
        self.data = {}

    def contains(self, key, ttl):
        return key in self.data and time() - self.data[key][1] < ttl

    def set(self, key, value):
        self.data[key] = (value, time())

    def get(self, key):
        return self.data[key][0]


class Cache:
    def __init__(self):
        self.value = None
        self.time = None

    def is_valid(self, ttl):
        return self.time is not None and time() - self.time < ttl

    def set(self, value):
        self.value = value
        self.time = time()

    def get(self):
        return self.value

    def __repr__(self):
        return f"Cache({self.value=}, {self.time=})"


class BasePlugin(metaclass=ABCMeta):
    license_filename = "LICENSE.txt"
    _busy_count = 0
    _is_busy = False
    _regexps = {
        re.compile(r"(?:^|.*\s)(?:https://)*openlicense.ai/(n/|t/|\b)(\w+)(?:$|\s)"): True,
        # re.compile("olai\:(\w+)"): False,
    }
    copyright_tags_cache = CachedPairs()
    platform_tag_cache = Cache()

    def __init__(self, ctx: WorkerContext):
        self.ctx = ctx
        self._is_busy = False

    def __del__(self):
        if self._is_busy:
            self.is_busy = False  # calling @is_busy.setter
            logger.warning("was busy on destruction!!")

    @property
    def is_busy(self):
        return self._is_busy

    @is_busy.setter
    def is_busy(self, b: bool):
        self._is_busy = b
        if b:
            BasePlugin._busy_count += 1
            logger.info(f"busy count of plugins is {self._busy_count} (incremented)")
        else:
            BasePlugin._busy_count -= 1
            logger.info(f"busy count of plugins is {self._busy_count} (decremented)")

    @classmethod
    def get_busy_count(cls):
        return cls._busy_count

    async def download(self, url, headers={}, follow_redirects=True, max_redirects=5):
        logger.info(f"BasePlugin.download {url=}")
        try:
            async with httpx.AsyncClient(max_redirects=max_redirects) as client:
                r = await client.get(url, follow_redirects=follow_redirects, headers=headers)
                return r.content

        except Exception as e:
            logger.error(f"failed get content of {url}: {e}")

    async def async_read_url(
        self,
        url,
        expected_type: Optional[DatapoolContentType] = None,
        headers={},
        follow_redirects=True,
        max_redirects=5,
    ):
        logger.info(f"BasePlugin.async_read_url {url=}")

        # will try to check content type by http content-type header or ( if header check fails ) by content itself
        is_header_checked = False
        is_content_checked = False
        is_type_ok = False
        type_bytes = bytes()
        async with httpx.AsyncClient(max_redirects=max_redirects) as client:
            async with client.stream("GET", url, follow_redirects=follow_redirects, headers=headers) as stream:
                async for chunk in stream.aiter_bytes():

                    if expected_type and not is_type_ok:
                        type_bytes += chunk

                        resp_type = None
                        if not is_header_checked:
                            # check by content-type header
                            ct = stream.headers.get("content-type")
                            if ct:
                                is_header_checked = True
                                try:
                                    resp_type = self.get_content_type_by_mime_type(ct)
                                    logger.info(f"async_read_url:{resp_type=} by header")
                                    if resp_type == expected_type:
                                        is_type_ok = True
                                except UnexpectedContentTypeException:
                                    pass

                        # then try to check by content itself
                        if not is_content_checked and not is_type_ok:
                            if len(type_bytes) >= MAGIC_MIN_BYTES:
                                is_content_checked = True
                                try:
                                    resp_type = self.get_content_type_by_content(type_bytes)
                                    logger.info(f"async_read_url:{resp_type=} by content")
                                    if resp_type == expected_type:
                                        is_type_ok = True
                                except UnexpectedContentTypeException:
                                    pass

                        # if both header and content check and both do not match then raise
                        if is_header_checked and is_content_checked and not is_type_ok:
                            raise UnexpectedContentTypeException(
                                f"Unexpected content type: {expected_type} vs {resp_type}"
                            )
                    else:
                        if type_bytes:
                            yield type_bytes
                            type_bytes = bytes()

                        yield chunk
                if type_bytes:
                    yield type_bytes

    @staticmethod
    def parse_url(url):
        return urlparse(url)

    @staticmethod
    @abstractmethod
    def is_supported(url):
        pass

    @staticmethod
    def is_same_or_subdomain(dom1, dom2):
        if dom1 == dom2:
            return True
        s1 = dom1.split(".")
        s2 = dom2.split(".")
        return s1[-len(s2) : :] == s2

    @staticmethod
    def get_local_url(href, page_url):
        pc = urlparse(page_url)
        p = urlparse(href)
        if p.netloc == "" or BasePlugin.is_same_or_subdomain(p.netloc, pc.netloc):
            return urljoin(page_url, href)
        return False

    @staticmethod
    def merge_head_tail(head, tail):
        # returns intersection length
        m = len(head)
        n = len(tail)

        for i in range(max(0, m - n), m):
            head_slice = head[i:]
            tail_slice = tail[0 : m - i]
            # print(i, head_slice, tail_slice)

            if head_slice == tail_slice:
                return head + tail[i:]
        return head + tail

    @abstractmethod
    async def process(self, task: WorkerTask) -> AsyncGenerator[BaseCrawlerResult, None]:
        pass

    @staticmethod
    def is_imported(module):
        return module in sys.modules

    @classmethod
    def parse_dns_tag(cls, domain) -> Union[BaseTag, None]:
        logger.info(f"parse_dns_tag {domain=}")
        try:
            records = dns.resolver.resolve(domain, "TXT")
            logger.info(f"{records=}")
            for record in records:
                tag = BasePlugin.parse_tag_in_str(str(record))
                if tag is not None:
                    return tag
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.LifetimeTimeout:
            pass
        return None

    @classmethod
    async def parse_meta_tag(cls, content, meta_name) -> Union[BaseTag, None]:
        if BasePlugin.is_imported("bs4") and type(content) is BeautifulSoup:
            return BasePlugin.parse_tag_in_bs_content(content, "meta")
        if BasePlugin.is_imported("playwright.async_api") and type(content) is Page:
            metas = content.locator(f'meta[name="{meta_name}"]')
            for meta in await metas.all():
                c = await meta.get_attribute("content")

                tag = BasePlugin.parse_tag_in_str(c)
                if tag is not None:
                    return tag
        return None

    @classmethod
    def parse_tag_in_str(cls, string) -> Union[BaseTag, None]:
        logger.info(f"parse_tag_in_str {string=}")
        for regexp, keepout in BasePlugin._regexps.items():
            tag = regexp.match(string)
            if tag is not None:
                # logger.info(tag.group(1))
                # logger.info(tag.group(2))

                if keepout is False:
                    return BaseTag(tag.group(1))
                else:
                    return BaseTag(tag.group(2), tag.group(1) == "n/")
        return None

    @classmethod
    def parse_tag_in_bs_content(cls, content: BeautifulSoup, locator: str) -> Union[BaseTag, None]:
        for regexp, deniable in BasePlugin._regexps.items():
            tag = content.find(locator, attrs={"content": regexp})
            if tag is not None:
                if deniable is False:
                    return BaseTag(tag.group(1))
                else:
                    return BaseTag(tag.group(2), tag.group(1) == "n/")
        return None

    @classmethod
    async def parse_tag_in(cls, content, locator: str = "") -> Union[BaseTag, None]:
        if type(content) is str:
            return BasePlugin.parse_tag_in_str(content)
        elif BasePlugin.is_imported("bs4") and type(content) is BeautifulSoup:
            return BasePlugin.parse_tag_in_bs_content(content, locator)

        elif BasePlugin.is_imported("playwright.async_api") and type(content) is Page:
            elems = content.locator(locator)
            for elem in await elems.all():
                c = await elem.text_content()
                if c is not None:
                    return BasePlugin.parse_tag_in_str(c)
        return None

    @staticmethod
    def get_content_type_by_mime_type(mime) -> DatapoolContentType:
        # logger.info(f"{mime=}")
        parts = mime.split("/")
        if parts[0] == "image":
            return DatapoolContentType.Image
        if parts[0] == "video" or mime == "application/mxf":
            return DatapoolContentType.Video
        if parts[0] == "audio":
            return DatapoolContentType.Audio
        if parts[0] == "text" or mime == "application/json":
            return DatapoolContentType.Text

        raise UnexpectedContentTypeException(f"not supported {mime=}")

    @staticmethod
    def get_content_type_by_content(content: Union[bytes, io.IOBase]) -> DatapoolContentType:
        if isinstance(content, bytes):
            buffer = content
        elif isinstance(content, io.IOBase):
            content.seek(0, 0)
            buffer = content.read(MAGIC_MIN_BYTES)  # TODO: enough?
        mime = magic.from_buffer(buffer, mime=True)
        if mime:
            return BasePlugin.get_content_type_by_mime_type(mime)
        raise BasePluginException("not supported content")

    @classmethod
    def parse_image_tag(cls, content: Union[bytes, io.IOBase]) -> Union[BaseTag, None]:
        # load image from bytes content, parse Copyright exif field for a license tag
        try:
            if isinstance(content, bytes):
                image = Image.open(io.BytesIO(content))
            elif isinstance(content, io.IOBase):
                image = Image.open(content)
            exifdata = image.getexif()
            cp = exifdata.get(ExifTagsList.Copyright)
            # logger.info( f'{cp=} {type(cp)=}')

            if type(cp) is str:
                return cls.parse_tag_in_str(cp)
        except Exception as e:
            logger.error(f"Failed process image: {e}")
        return None

    async def get_platform_tag(self, domain, content, ttl=3600, meta_name=None) -> Union[BaseTag, None]:
        # logger.info( f'get_platform_tag {self.platform_tag_cache=}')
        # logger.info(f'now={time()}' )
        # logger.info(f'diff={time() - self.platform_tag_cache.time if self.platform_tag_cache.time is not None else "nan"}')

        if not self.platform_tag_cache.is_valid(ttl):
            dns_tag = BasePlugin.parse_dns_tag(domain)
            if dns_tag:
                self.platform_tag_cache.set(dns_tag)
            else:
                # check if <meta/> tag exists with our tag
                header_tag = await BasePlugin.parse_meta_tag(content, meta_name)
                self.platform_tag_cache.set(header_tag)
        return self.platform_tag_cache.get()


    @staticmethod
    async def get_webpage_image_bytes(img_locator):
        """for playwright only"""
        b64 = await img_locator.evaluate(
            '(img) => {\
            img.crossOrigin="anonymous";\
            var canvas = document.createElement("canvas");\
            canvas.width = img.width;\
            canvas.height = img.height;\
            var ctx = canvas.getContext("2d");\
            ctx.drawImage(img, 0, 0);\
            var dataURL = canvas.toDataURL("image/png");\
            return dataURL;\
        }'
        )
        n = len("data:image/png;base64,")
        return base64.b64decode(b64[n:])

    # TODO: make this function more generic ( support bs4 too )
    # TODO: or maybe don't use bs4 at all?
    async def parse_links(self, page: Page):
        """gather all links on the page and yield them as subtasks. Only current domain urls are counted"""
        hrefs = await page.locator("a").all()
        for href_loc in hrefs:
            href = await href_loc.get_attribute("href")
            if href is not None:
                # logger.info( f'parse_link {href=} {type(href)=} {page.url} {type(page.url)=}')

                full_local_url = BasePlugin.get_local_url(href, page.url)
                if full_local_url:
                    # strict constraint on urls, else may get endless recursions etc
                    full_local_url = canonicalize_url(full_local_url)
                    # logger.info(full_local_url)

                    # logger.info( f'---------yielding {video_url=}')
                    yield CrawlerBackTask(url=full_local_url)
                    # logger.info( f'---------yielded {video_url=}')
                else:
                    # logger.info(f"non local: {href=} {page.url=}")
                    pass

    @staticmethod
    def make_text_storage_value(body, header=None, excerpt=None):
        data = (header + "\n" if header else "") + (excerpt + "\n" if excerpt else "") + body
        return data

    @staticmethod
    def gen_demo_tag(user_name):
        return "demo_" + md5(user_name.encode()).hexdigest()[-6:]

    @staticmethod
    async def parse_time_tag(page: Page, loc) -> int | None:
        """
        Works only with <time> html tag.
        Returns unix timestamp
        """
        res = None
        time_link = await page.locator(f"time{loc}").all()
        if len(time_link):
            dt = await time_link[0].get_attribute("datetime")
            if dt is not None:
                return BasePlugin.parse_datetime(dt)
        return res

    @staticmethod
    def parse_datetime(raw: str) -> int:
        return int((date_parser.parse(raw) - datetime(1970, 1, 1, 0, 0, 0)).total_seconds())


class BaseReader:
    @abstractmethod
    async def read_to(self, f: io.IOBase, stopper: Callable): ...


class BaseReaderException(Exception):
    pass


class ConnectionFailed(BaseReaderException):
    pass


class AuthFailed(BaseReaderException):
    pass


class ReadFailed(BaseReaderException):
    pass
