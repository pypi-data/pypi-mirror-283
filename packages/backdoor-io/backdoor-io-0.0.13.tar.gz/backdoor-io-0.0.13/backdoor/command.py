# command.py

import json
import os
from uuid import uuid4
from typing import Self, Callable
from dataclasses import dataclass, field, asdict

from dacite import from_dict

from backdoor.action import Action
from backdoor.data import Data, Format, File
from backdoor.execution import SubProcess, SubThread

__all__ = [
    "Command",
    "CommandCapsule",
    "dump_command_json",
    "load_command_json",
    "delete_command_json"
]

JsonValue = str | bytes | dict | list | int | float | bool | None

@dataclass(slots=True)
class Command:

    id: str | None = field(default_factory=lambda: str(uuid4()))
    cwd: str | None = None
    action: Action | None = None
    request: Data = field(default_factory=Data)
    response: Data = field(default_factory=Data)
    memory: dict[str, JsonValue] | None = None
    complete: bool = False
    running: bool = False
    forget: bool = False
    keep_request: bool = True
    message: str | None = None
    error: str | None = None
    executions: list[SubProcess | SubThread] = field(
        init=False, default_factory=list, repr=False
    )

    def __post_init__(self) -> None:

        from backdoor.actions import Actions

        if (
            (self.action is not None) and
            (self.action.type in (Actions.DATA.TYPE, Actions.FILE.TYPE)) and
            (self.request.action is None)
        ):
            self.request.action = self.action.name

        elif (self.action is None) and (self.request.action is not None):
            self.action = Action(
                type=(
                    Actions.FILE.TYPE
                    if isinstance(self.request, File) else
                    Actions.DATA.TYPE
                ),
                name=self.request.action
            )

    @property
    def io(self) -> bool:

        return self.response.io or self.request.io

    @property
    def valid(self) -> bool:

        return self.request.valid and self.response.valid

    def stop(self) -> None:

        for execution in self.executions:
            execution.terminate()

        self.executions.clear()

        self.running = False

    def respond(
            self,
            name: str = None,
            value: JsonValue = None,
            message: str = None,
            error: str = None
    ) -> Data:

        self.response = self.response.copy()

        self.response.payload = value or self.response.payload
        self.response.name = name or self.response.name
        self.message = message or self.message
        self.error = error or self.error

        self.response.format = Format.format(value)

        return self.response

    @classmethod
    def load(cls, data: dict[str, JsonValue | dict[str, JsonValue]]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, JsonValue | dict[str, JsonValue]]:

        data = asdict(self.copy())
        data.pop('executions')

        return data

    def copy(self) -> Self:

        return Command(
            id=self.id,
            action=self.action,
            request=self.request,
            response=self.response,
            complete=self.complete,
            running=self.running,
            error=self.error
        )

@dataclass(slots=True, frozen=True)
class CommandCapsule:

    command: Command
    memory: dict[str, ...] = field(default_factory=dict)
    on_finish: Callable[["CommandCapsule"], ...] = None

def dump_command_json(command: Command, location: str = None) -> None:

    if (location is None) or location.endswith('/'):
        location = ""

    else:
        location += "/"

    os.makedirs(location, exist_ok=True)

    with open(f"{location}{command.id}.json", 'w') as file:
        json.dump(command.dump(), file, indent=4)

def load_command_json(command_id: str, location: str = None) -> Command:

    if (location is None) or location.endswith('/'):
        location = ""

    else:
        location += "/"

    with open(f"{location}{command_id}.json", 'r') as file:
        return Command.load(json.load(file))

def delete_command_json(command_id: str, location: str = None) -> None:

    if (location is None) or location.endswith('/'):
        location = ""

    else:
        location += "/"

    os.remove(f"{location}{command_id}.json")
