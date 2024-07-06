# manager.py

from uuid import uuid4
from dataclasses import dataclass, field, asdict
from typing import Self

from dacite import from_dict

from backdoor.command import Command

__all__ = [
    "Manager"
]

@dataclass(slots=True)
class Manager:

    id: str = field(default_factory=lambda: str(uuid4()))
    sent: list[str] = field(default_factory=list)
    received: list[str] = field(default_factory=list)
    history: list[str] = field(default_factory=list)
    commands: dict[str, Command] = field(default_factory=dict)

    def add(self, command: Command) -> Command:

        self.commands[command.id] = command

        self.history.append(command.id)

        return command

    def send(self, command: Command) -> Command:

        self.add(command)

        self.sent.append(command.id)

        return command

    def receive(self, command: Command) -> Command:

        self.add(command)

        self.received.append(command.id)

        return command

    def dump(self) -> dict[str, ...]:

        return asdict(self)

    @classmethod
    def load(cls, data: dict[str, ...]) -> Self:

        return from_dict(cls, data)
