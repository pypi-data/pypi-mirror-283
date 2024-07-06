# action.py

import datetime as dt
from typing import Self
from dataclasses import dataclass, asdict

from dacite import from_dict

__all__ = [
    "Action"
]

@dataclass(slots=True)
class Action:

    type: str
    name: str
    repetitions: int = 1
    timeout: dt.timedelta | None = None
    thread: bool = False
    wait: bool = True

    @classmethod
    def load(cls, data: dict[str, ...]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, str | int]:

        return asdict(self)
