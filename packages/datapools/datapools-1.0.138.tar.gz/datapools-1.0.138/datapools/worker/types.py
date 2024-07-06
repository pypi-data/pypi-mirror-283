from enum import Enum
from ..common.session_manager import Session


class YieldResult(Enum):
    NoResult = 0
    ContentDownloadSuccess = 1
    ContentDownloadFailure = 2
    ContentIgnored = 3


class WorkerContext:
    session: Session
    yield_result: YieldResult

    def __init__(self, session: Session):
        self.session = session
        self.yield_result = YieldResult.NoResult
