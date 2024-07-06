# backdoor

> A framework for designing, orchestrating and executing backdoor systems, with short and long term memory, dynamic execution, data delivery, multithreading live communication and more.

Installation
-----------
````
pip install backdoor-io
````

example
-----------

Simple commands to execute one by one.
````python
from backdoor import (
    Executor, Command, Data, Actions, Action, DELETE, WRITE, READ, SEARCH
)

commands = [
    Command(request=Data(payload='text', name='value', action=WRITE)),
    Command(request=Data(name='value', action=READ)),
    Command(
        action=Action(type=Actions.EXECUTION.TYPE, name=Actions.EXECUTION.PYTHON),
        request=Data(payload='print(value); result = value * 2;')
    ),
    Command(request=Data(name='value', action=DELETE)),
    Command(request=Data(name='value', action=SEARCH)),
    Command(request=Data(name='result', action=READ)),
    Command(
        action=Action(type=Actions.EXECUTION.TYPE, name=Actions.EXECUTION.CMD),
        request=Data(payload='dir')
    )
]

executor = Executor()

for command in commands:
    print(executor.execute(command), "\n")
````

output
````python
Command(
    id='793f1d0d-641e-45b4-ba2f-dad801c35a3f',
    action=Action(type='data', name='write', repetitions=1, timeout=None, thread=False, wait=True),  
    request=Data(payload='text', format='text', name='value', action='write', timestamp=1710051829.9969397), 
    response=Data(payload="'value' was written to memory in memory.", format='text', name=None, action=None, timestamp=1710051829.9969397), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    id='b5985414-1d9f-4a0e-966b-445b2be92a40',
    action=Action(type='data', name='read', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload='text', format='text', name='value', action='read', timestamp=1710051829.9969397), 
    response=Data(payload='text', format='text', name=None, action=None, timestamp=1710051829.9969397), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    id='958f80d4-e74e-45e6-bf08-0ab6c89ab771',
    action=Action(type='execution', name='python', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload='print(value); result = value * 2;', format='text', name=None, action=None, timestamp=1710051829.9969397), 
    response=Data(payload={'stdout': '', 'stderr': ''}, format='json', name=None, action=None, timestamp=1710051829.9969397), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    action=Action(type='data', name='delete', repetitions=1, timeout=None, thread=False, wait=True), 
    id='b91c39ca-d19f-4322-a209-b5ca4c06dfe5', 
    request=Data(payload=None, format=None, name='value', action=None, timestamp=1710051829.9969397), 
    response=Data(payload="'value' was deleted from memory.", format='text', name=None, action=None, timestamp=1710051829.99794), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    id='a9d47fcf-5266-4a47-b102-ed267b9bbba4',
    action=Action(type='data', name='search', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload=None, format=None, name='value', action=None, timestamp=1710051829.9969397), 
    response=Data(payload=False, format='json', name=None, action=None, timestamp=1710051829.99794), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    id='d9ec5d45-e214-4a36-8d72-f52adb605da3',
    action=Action(type='data', name='read', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload=None, format=None, name='result', action=None, timestamp=1710051829.9969397), 
    response=Data(payload='texttext', format='text', name=None, action=None, timestamp=1710051829.99794), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    id='d5093ce2-0cbf-4d5e-8195-850c27d46e54',
    action=Action(type='execution', name='cmd', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload='dir', format='text', name=None, action=None, timestamp=1710051829.9969397), 
    response=Data(payload={'stdout': ' Volume in drive C is Windows-SSD\n Volume Serial Number is 0C65-337C\n\n Directory of ...', 'stderr': ''}, format='json', name=None, action=None, timestamp=1710051830.0080411), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)
````

Complex commands to run in the background, with timeout and threading.
````python
import time

from backdoor import (
    Executor, Command, Data, Actions, Action, WRITE, File, TEXT, READ
)

c1 = Command(
    action=Action(
        type=Actions.EXECUTION.TYPE,
        name=Actions.EXECUTION.PYTHON,
        wait=False,
        thread=True,
        # timeout=dt.timedelta(seconds=5)
    ),
    request=Data(payload='import time\nfor _ in range(10):\n\ttime.sleep(1)')
)
c2 = Command(
    action=Action(
        type=Actions.MANAGEMENT.TYPE,
        name=Actions.MANAGEMENT.COMMAND,
    ),
    request=Data(name=c1.id)
)

c3 = Command(
    action=Action(
        type=Actions.MANAGEMENT.TYPE,
        name=Actions.MANAGEMENT.STOP,
    ),
    request=Data(name=c1.id)
)

c4 = Command(
    request=File(
        payload="hello world", name="hello.txt",
        action=WRITE
    )
)
c5 = Command(request=File(name="hello.txt", format=TEXT, action=READ))

executor = Executor()

print(executor.execute(c1), "\n")
print("waiting for 3 seconds...")

time.sleep(3)

print(executor.execute(c2), "\n")
print("waiting for 3 seconds...")

time.sleep(3)

print(executor.execute(c3), "\n")
print(executor.execute(c2), "\n")

print('written a file named "hello.txt" with content "hello world"')

print(executor.execute(c4), "\n")
print(executor.execute(c5))
````

output
````python
Command(
    id='3c9da903-028c-4dd0-b583-f15ccaed1280', 
    action=Action(type='execution', name='python', repetitions=1, timeout=None, thread=True, wait=False), 
    request=Data(payload='import time\nfor _ in range(10):\n\ttime.sleep(1)', format='text', name=None, action=None, timestamp=1710052480.8686686), 
    response=Data(payload={}, format='json', name=None, action=None, timestamp=1710052480.8705611), 
    memory=None, complete=False, running=True, forget=False, keep_request=True, message=None, error=None
)

waiting for 3 seconds...

Command(
    id='df96ff69-16d2-4c42-a5a9-f16c390f15ee', 
    action=Action(type='management', name='command', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload='3c9da903-028c-4dd0-b583-f15ccaed1280', format='text', name=None, action=None, timestamp=1710052480.8686686), 
    response=Data(payload={'id': '3c9da903-028c-4dd0-b583-f15ccaed1280', 'action': {'type': 'execution', 'name': 'python', 'repetitions': 1, 'timeout': None, 'thread': True, 'wait': False}, 'request': {'payload': 'import time\nfor _ in range(10):\n\ttime.sleep(1)', 'format': 'text', 'name': None, 'action': None, 'timestamp': 1710052480.8686686}, 'response': {'payload': {}, 'format': 'json', 'name': None, 'action': None, 'timestamp': 1710052480.8705611}, 'memory': None, 'complete': False, 'running': True, 'error': None}, format='json', name=None, action=None, timestamp=1710052483.8717408), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

waiting for 3 seconds...

Command(
    id='d6e7faea-6c1a-410e-89b7-3652ca914cc0', 
    action=Action(type='management', name='stop', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload='3c9da903-028c-4dd0-b583-f15ccaed1280', format='text', name=None, action=None, timestamp=1710052480.8686686), 
    response=Data(payload='Command was stopped.', format='text', name=None, read=False, write=False, timestamp=1710052486.8754737), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    id='df96ff69-16d2-4c42-a5a9-f16c390f15ee', 
    action=Action(type='management', name='command', repetitions=1, timeout=None, thread=False, wait=True), 
    request=Data(payload='3c9da903-028c-4dd0-b583-f15ccaed1280', format='text', name=None, action=None, timestamp=1710052480.8686686), 
    response=Data(payload={'id': '3c9da903-028c-4dd0-b583-f15ccaed1280', 'action': {'type': 'execution', 'name': 'python', 'repetitions': 1, 'timeout': None, 'thread': True, 'wait': False}, 'request': {'payload': 'import time\nfor _ in range(10):\n\ttime.sleep(1)', 'format': 'text', 'name': None, 'action': None, 'timestamp': 1710052480.8686686}, 'response': {'payload': {}, 'format': 'json', 'name': None, 'action': None, 'timestamp': 1710052480.8705611}, 'memory': None, 'complete': False, 'running': False, 'error': None}, format='json', name=None, action=None, timestamp=1710052486.8764887),
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

written a file named "hello.txt" with content "hello world"

Command(
    id='f45da0d9-feee-41b8-8686-1024bfb70fc0', 
    action=Action(type='file', name='write', repetitions=1, timeout=None, thread=False, wait=True), 
    request=File(payload='hello world', format='text', name='hello.txt', action='write', timestamp=1710090057.4463112, position=11, size=11, buffer=None), 
    response=Data(payload="Data was added to the end of file: 'hello.txt'.", format='text', name=None, action=None, timestamp=1710090064.4521823), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

Command(
    id='2d5a4f9a-6467-41e2-88ab-119626ef0fb1', 
    action=Action(type='file', name='read', repetitions=1, timeout=None, thread=False, wait=True), 
    request=File(payload=None, format='text', name='hello.txt', action='read', timestamp=1710147070.8170629, position=11, size=11, buffer=None), 
    response=Data(payload='hello world', format='text', name=None, action=None, timestamp=1710147070.8180661), 
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)
````

Constructing a Command object:
````python
# The id of the command, can also be a plaintext name.
id: str = str(uuid4())
# Describes the type and name of action to preform.
action: Action | None = None
# Describes the input (request) data and output (response) data,
# and what to do with them.
request: Data = Data()
response: Data = Data()
# a dedicated memory dictionary for the command, 
# rather than using the shared memory of the executor's.
memory: dict[str, JsonValue] = None
````

Additional attributes:
````python
# Id the command is still running: complete: False, running: True.
complete: bool = False
running: bool = False
# When an error is raised, it is saved here.
error: str | None = None
````

Constructing an Action object:
````python
# The type of action, from the Actions class.
type: str
# The name of the action from the type from the Actions class.
name: str
# The amount of times to commit the action in a row.
repetitions: int = 1
# A timeout to stop the action.
timeout: dt.timedelta = None
# A value to specify that the action is to be executed in a different thread.
# This means that the action will return back the command as usual, 
# but will specify that the command is not complete and still running.
thread: bool = False
# A value to make the executor wait to the action to finish.
wait: bool = True
````

Constructing a Data object:
````python
# The bytes | json valid payload to contain.
payload: JsonValue = None
# The format of the data. Can be inferred automatically.
format: str | Literal['text', 'bytes', 'json'] | None = None
# The name of the data, with which the data can be 
# saved to or read from the memory of the command/executor.
name: str | None = None
# The memory action to take with the data: read/write/delete/search
action: Literal['read', 'write', 'delete', 'search'] | None = None
````

Additional attributes:
````python
# The timestamp of creation of the object.
timestamp: float = time.time()
````

Simple Json-valid I/O:
````python
from backdoor import Command, Action, Data

c1 = Command(
    id='793f1d0d-641e-45b4-ba2f-dad801c35a3f',
    action=Action(type='data', name='write', repetitions=1, timeout=None, thread=False, wait=True),
    request=Data(payload='text', format='text', name='value', action='write', timestamp=1710051829.9969397),
    response=Data(payload="'value' was written to memory in memory.", format='text', name=None, action=None, timestamp=1710051829.9969397),
    memory=None, complete=True, running=False, forget=False, keep_request=True, message=None, error=None
)

print(c1.dump())
print("same data:", c1 == Command.load(c1.dump()))
````

output:
````python
{
    'id': '793f1d0d-641e-45b4-ba2f-dad801c35a3f', 
    'action': {'type': 'data', 'name': 'write', 'repetitions': 1, 'timeout': None, 'thread': False, 'wait': True}, 
    'request': {'payload': 'text', 'format': 'text', 'name': 'value', 'action': 'write', 'timestamp': 1710051829.9969397}, 
    'response': {'payload': "'value' was written to memory in memory.", 'format': 'text', 'name': None, 'action': None, 'timestamp': 1710051829.9969397}, 
    'memory': None, 'complete': True, 'running': False, 'forget': False, 'keep_request': True, 'message': None, 'error': None
}
same data: True
````

Executor Construction:
````python
# Saves the id of the commands executed.
history: list[str] = []
# Saves the id of the commands being executed.
running: list[str] = []
# Contains all command object.
commands: dict[str, Command] = {}
# Shared memory of data and variables from and for the execution of commands.
memory: dict[str, ...] = {}
# Contains custom command objects.
custom: dict[str, Command | None] = {}
# Specifies the initial and current locations of the system to execute in.
root_location: str = os.getcwd
current_location: str = os.getcwd
# Callables to save/load/delete command data/objects.
save: Callable[[Command], str] = None
load: Callable[[str], Command] = None
delete: Callable[[str], ...] = None
````

Executor Interface:
````python
from backdoor import Executor, Command

executor = Executor()

# simple execution

c1 = Command(...)

c1_copy = c1.copy()

c1_return = executor.execute(c1)

assert c1 is c1_return
assert c1_copy != c1_return

# adding a custom command

custom_command = Command(...)

# method 1:
executor.add(custom_command)

# method 2:
from backdoor import Action, Data, Actions

custom_command_adder = Command(
    action=Action(type=Actions.MANAGEMENT.TYPE, name=Actions.MANAGEMENT.ADD),
    request=Data(payload=custom_command.dump())
)

executor.execute(custom_command_adder)

# running the custom command

custom_command_return = executor.execute(
    Command(
        action=Action(type=Actions.EXECUTION.TYPE, name=Actions.MANAGEMENT.CLEAN),
        request=Data(payload=custom_command.id)
    )
)
````