# data.py

import json
import time
from typing import Literal, Self
from dataclasses import dataclass, field, asdict

from dacite import from_dict

from backdoor.labels import (
    DELETE, WRITE, SEARCH, READ, TEXT, JSON, BYTES
)

__all__ = [
    "Format",
    "Data",
    "File",
    "DataCapsul"
]

Formatter = Literal['text', 'json', 'bytes']
JsonValue = str | bytes | dict | list | int | float | bool | None

class Format:

    TEXT = TEXT
    BYTES = BYTES
    JSON = JSON

    FORMATS = {TEXT, BYTES, JSON}

    @staticmethod
    def encode(data: JsonValue) -> str:

        if not isinstance(data, (str, bytes)):
            data = json.dumps(data)

        if isinstance(data, str):
            return data

        if isinstance(data, bytes):
            return data.decode()

        raise TypeError(f"invalid data type: {type(data)}")

    @staticmethod
    def decode(data: str, f: str | Formatter) -> JsonValue:

        if f == Format.BYTES:
            return data.encode()

        if f == Format.TEXT:
            return data

        if f == Format.JSON:
            return json.loads(data)

        raise TypeError(f"invalid format: {f}")

    @staticmethod
    def format(data: JsonValue) -> str:

        if isinstance(data, bytes):
            return Format.BYTES

        elif isinstance(data, str):
            return Format.TEXT

        elif isinstance(data, (int, float, type(None), dict, list, tuple)):
            return Format.JSON

        raise TypeError(f"invalid data type: {type(data)}")

@dataclass(slots=True)
class Data:

    payload: JsonValue = None
    format: str | Formatter | None = None
    name: str | None = None
    action: Literal['read', 'write', 'delete', 'search'] | None = None
    timestamp: float = field(default_factory=time.time)

    def __post_init__(self) -> None:

        self.data()

    @property
    def file(self) -> bool:

        return isinstance(self, File)

    @property
    def io(self) -> bool:

        return self.action is not None

    @property
    def read(self) -> bool:

        return self.action == READ

    @property
    def write(self) -> bool:

        return self.action == WRITE

    @property
    def delete(self) -> bool:

        return self.action == DELETE

    @property
    def search(self) -> bool:

        return self.action == SEARCH

    @property
    def valid(self) -> bool:

        return not (self.io and (not self.name))

    def data(self) -> JsonValue:

        if (self.format is None) and (self.payload is not None):
            self.format = Format.format(self.payload)

        elif (self.format is not None) and (self.format != Format.format(self.payload)):
            # noinspection PyTypeChecker
            self.payload = Format.decode(self.payload, self.format)

        return self.payload

    def upload(self, memory: dict[str, ...]) -> bool:

        if self.name and self.read and not self.file:
            self.payload = memory[self.name]

            return True

        return False

    def update(self, memory: dict[str, ...], value: ... = Ellipsis) -> bool:

        if value == Ellipsis:
            value = self.data()

        if self.name and not self.file:
            if self.write:
                memory[self.name] = value

                return True

        return False

    @classmethod
    def load(cls, data: dict[str, JsonValue]) -> Self:

        data = data.copy()

        if None not in (data['payload'], data['format']):
            data['payload'] = Format.decode(data['payload'], data['format'])

        return from_dict(cls, data)

    def dump(self) -> dict[str, JsonValue]:

        data = asdict(self)
        data['payload'] = Format.encode(data['payload'])

        return data

    def copy(self) -> Self:

        data = self.dump()
        data.pop('timestamp')

        new = type(self).load(data)

        return new

@dataclass(slots=True)
class File(Data):

    position: int = 0
    size: int = None
    buffer: int = None

@dataclass(slots=True)
class DataCapsul:

    payload: JsonValue = None
    message: str | None = None
