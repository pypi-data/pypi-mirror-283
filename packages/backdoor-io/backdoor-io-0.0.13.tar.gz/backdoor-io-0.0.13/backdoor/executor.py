# executor.py

import os
from uuid import uuid4
from dataclasses import dataclass, field, asdict
from typing import Callable, Self

from dacite import from_dict

from backdoor.command import Command, CommandCapsule
from backdoor.action import Action
from backdoor.data import DataCapsul
from backdoor.actions import Actions

__all__ = [
    "Executor"
]

JsonValue = str | bytes | dict | list | int | float | bool | None
ActionsDict = dict[str, Callable[[CommandCapsule], DataCapsul]]

class BaseError(Exception):

    pass

class ActionValidationError(BaseError):

    pass

class MemoryValidationError(BaseError):

    pass

class DataValidationError(BaseError):

    pass

def tree(path: str = '.') -> dict[str, ...]:

    data = {}

    for sub_path in os.listdir(path):
        p = os.path.join(path, sub_path)

        if os.path.isdir(p):
            data[sub_path] = tree(p)

        else:
            data[sub_path] = None

    return data

@dataclass(slots=True)
class Executor:

    id: str = field(default_factory=lambda: str(uuid4()))
    history: list[str] = field(default_factory=list)
    running: list[str] = field(default_factory=list)
    commands: dict[str, Command] = field(default_factory=dict)
    memory: dict[str, ...] = field(default_factory=dict)
    actions: dict[str, ActionsDict] = field(init=False, default_factory=dict)
    custom: dict[str, Command | None] = field(default_factory=dict)
    root_location: str = field(default_factory=os.getcwd)
    current_location: str = field(default_factory=os.getcwd)
    dump_command: Callable[[Command], ...] = None
    load_command: Callable[[str], Command] = None
    delete_command: Callable[[str], ...] = None

    def __post_init__(self) -> None:

        if self.id is None:
            self.id = str(uuid4())

        actions = Actions()

        management = actions.management
        system = actions.system
        execution = actions.execution
        file = actions.file

        file.actions[file.TREE] = self._tree

        execution.actions[execution.CUSTOM] = self._custom

        management.actions[management.RERUN] = lambda c: self._rerun()
        management.actions[management.CLEAN] = lambda c: self._clean()
        management.actions[management.LAST] = lambda c: self._last()
        management.actions[management.RUNNING] = lambda c: self._running()
        management.actions[management.COMMAND] = self._command
        management.actions[management.STOP] = self._stop
        management.actions[management.FORGET] = self._forget
        management.actions[management.DELETE] = self._delete
        management.actions[management.ADD] = self._add

        system.actions[system.ROOT] = lambda c: self._root()
        system.actions[system.CWD] = lambda c: self._cwd()
        system.actions[system.CD] = self._cd

        self.actions.update(actions.actions)

        for group in (management, system, execution, file):
            self.actions[group.TYPE] = group.actions

    def clean(self) -> None:

        self.history.clear()
        self.memory.clear()
        self.commands.clear()
        self.custom.clear()

    def _clean(self) -> DataCapsul:

        self.clean()

        return DataCapsul()

    def _rerun(self) -> DataCapsul:

        return DataCapsul(self.execute(self.last_command).response.data())

    def _cwd(self) -> DataCapsul:

        return DataCapsul(self.current_location)

    def _cd(self, capsul: CommandCapsule) -> DataCapsul:

        self.current_location = capsul.command.request.data()

        os.chdir(self.current_location)

        return DataCapsul()

    def _root(self) -> DataCapsul:

        self.current_location = self.root_location

        os.chdir(self.current_location)

        return DataCapsul()

    @property
    def last_command(self) -> Command:

        if not self.history:
            raise ValueError("Commands history is empty.")

        return self.commands[self.history[-1]]

    def _last(self) -> DataCapsul:

        return DataCapsul(self.last_command.dump())

    def _tree(self, capsul: CommandCapsule) -> DataCapsul:

        return DataCapsul(
            tree(
                capsul.command.request.name or
                capsul.command.request.data() or
                self.current_location
            )
        )

    def _command(self, capsul: CommandCapsule) -> DataCapsul:

        command_id = capsul.command.request.data() or capsul.command.request.name

        if command_id not in self.commands:
            raise ValueError(f"No command found with id: '{command_id}'.")

        return DataCapsul(self.commands[command_id].dump())

    def _add(self, capsul: CommandCapsule) -> DataCapsul:

        try:
            command = Command.load(capsul.command.request.data())

        except (ValueError, TypeError):
            raise TypeError("Invalid custom command data.")

        self.add_custom(command)

        return DataCapsul(message=f"Custom command named '{command.id}' was added.")

    def _custom(self, capsul: CommandCapsule) -> DataCapsul:

        command_id = capsul.command.request.data() or capsul.command.request.name

        if command_id not in self.custom:
            raise ValueError(f"No custom command found with id: '{command_id}'.")

        if self.custom[command_id] is None:
            if self.load_command:
                try:
                    self.custom[command_id] = self.load_command(command_id)

                except Exception as e:
                    raise RuntimeError(
                        f"Failed to load custom command '{command_id}': {e}"
                    )

            else:
                raise ValueError(
                    "A loader must be defined to set and "
                    "run preexisting custom command."
                )

        return DataCapsul(self.execute(self.custom[command_id]).dump())

    def _delete(self, capsul: CommandCapsule) -> DataCapsul:

        command_id = capsul.command.request.data() or capsul.command.request.name

        if command_id not in self.custom:
            raise ValueError(f"No custom command found with id: '{command_id}'.")

        self.custom.pop(command_id)

        error = None

        if self.delete_command:
            try:
                self.delete_command(command_id)

            except Exception as e:
                error = str(e)

        message = f"Custom command named '{command_id}' was deleted."

        if error:
            message += f" Failed to run the custom delete operation: {error}"

        return DataCapsul(message=message)

    def _stop(self, capsul: CommandCapsule) -> DataCapsul:

        command_id = capsul.command.request.data() or capsul.command.request.name

        if command_id is None:
            stopped = self.running.copy()

            self.stop()

            return DataCapsul(stopped)

        if isinstance(command_id, str):
            ids = [command_id]

        else:
            ids = command_id

        stopped = []

        for command_id in ids:
            if command_id not in self.commands:
                continue

            self.commands[command_id].stop()

            stopped.append(command_id)

        return DataCapsul(stopped)

    def _forget(self, capsul: CommandCapsule) -> DataCapsul:

        command_id = capsul.command.request.data() or capsul.command.request.name

        if command_id not in self.commands:
            raise ValueError(f"No command found with id: '{command_id}'.")

        self.commands.pop(command_id).stop()

        if command_id in self.history:
            self.history.remove(command_id)

        if command_id in self.running:
            self.running.remove(command_id)

        return DataCapsul(message="Command was stopped and deleted from history.")

    def _running(self) -> DataCapsul:

        return DataCapsul([self.commands[command_id] for command_id in self.running])

    def remove(self, command: Command) -> None:

        command_id = command.id

        if command_id not in self.custom:
            raise ValueError(f"No custom command found with id: '{command_id}'.")

        self.custom.pop(command_id)

        if self.delete_command:
            self.delete_command(command_id)

    def stop(self) -> None:

        for command_id in self.running:
            if command_id in self.commands:
                self.commands[command_id].stop()

    def add_custom(self, command: Command) -> None:

        self.custom[command.id] = command

        if self.dump_command:
            try:
                self.dump_command(command)

            except Exception as e:
                raise RuntimeError(
                    f"Failed to save custom command '{command.id}': {e}"
                )

    def action(self, action: Action) -> Callable[[CommandCapsule], DataCapsul]:

        if action.type not in self.actions:
            error = (
                f"Unrecognized action type: '{action.type}'. "
                f"Valid action types: "
                f"{', '.join(map(lambda s: f"'{s}'", self.actions))}"
            )

        else:
            if action.name not in self.actions[action.type]:
                error = (
                    f"Unrecognized action type: '{action.name}'. "
                    f"Valid action types: "
                    f"{', '.join(map(lambda s: f"'{s}'", self.actions[action.type]))}"
                )

            else:
                return self.actions[action.type][action.name]

        raise ActionValidationError(error)

    def start(self, command: Command) -> None:

        self.running.append(command.id)

        self.commands[command.id] = command

    def finish(self, command: Command) -> None:

        command.stop()

        self.register(command)

    def register(self, command: Command) -> None:

        if not (command.error or command.running):
            command.complete = True

        if command.complete:
            command.running = False

            command.response.update(self.memory)

            if command.id in self.running:
                self.running.remove(command.id)

            if not command.forget:
                self.history.append(command.id)

            if not command.keep_request:
                command.request = None

        if not command.forget:
            self.commands[command.id] = command

    def respond(
            self,
            command: Command,
            name: str = None,
            value: JsonValue = None,
            message: str = None,
            error: str = None
    ) -> Command:

        command.respond(
            value=value, name=name,
            error=error, message=message
        )

        self.register(command)

        return command

    def execute(self, command: Command) -> Command:

        values = None
        error = None
        message = None

        self.start(command)

        try:
            if not command.valid:
                raise DataValidationError(
                    'A name must be given with data for read/write actions'
                )

            try:
                command.request.upload(self.memory)

            except KeyError:
                raise MemoryValidationError(
                    f"'{command.request.name}' could not be found in memory."
                )

            command.request.update(self.memory)

            action = self.action(command.action)

            capsul = CommandCapsule(
                memory=command.memory or self.memory, command=command,
                on_finish=lambda c: self.finish(c.command)
            )

            repetitions = command.action.repetitions

            value = [action(capsul) for _ in range(repetitions)]
            values = [v.payload for v in value]
            messages = [v.message for v in value if v.message is not None]

            if messages:
                message = '. '.join(messages)

            if repetitions == 1:
                values = values[0]

        except BaseError as e:
            error = f"An error raised before execution: {e}"

        except Exception as e:
            error = f"An error raised on execution: {e}"

        return self.respond(
            command=command, value=values, error=error, message=message
        )

    def dump(self, memory: bool = True) -> dict[str, ...]:

        data = asdict(self)

        data.pop('save')
        data.pop('load')
        data.pop('delete')

        if not memory:
            data.pop('memory')

        return data

    @classmethod
    def load(cls, data: dict[str, ...]) -> Self:

        return from_dict(cls, data)
