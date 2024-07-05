import dataclasses
import inspect
import uuid
from typing import Protocol, Optional, Any, Iterator

from _reusable import Elapsed

WIRETAP_KEY = "_wiretap"


class Activity(Protocol):
    parent: Optional["Activity"]
    id: uuid.UUID
    func: str
    name: str | None
    frame: inspect.FrameInfo
    body: dict[str, Any] | None
    tags: set[str] | None
    elapsed: Elapsed
    correlation: "Correlation"
    depth: int
    context: dict[str, Any]

    def __iter__(self) -> Iterator["Activity"]:
        pass


@dataclasses.dataclass
class Correlation:
    id: Any
    type: str = "default"


@dataclasses.dataclass
class Trace:
    code: str
    name: str | None
    message: str | None


@dataclasses.dataclass
class Entry:
    activity: Activity
    trace: Trace
    body: dict[str, Any]
    tags: set[str]
