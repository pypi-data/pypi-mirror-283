# execution.py

import threading
import subprocess
import ctypes
import time
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field

__all__ = [
    "SubProcess",
    "SubThread"
]

def terminate_thread(thread: threading.Thread) -> None:

    thread_id = thread.ident

    if ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit)
    ) > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)

    thread.join()

class BaseSubExecution(metaclass=ABCMeta):

    def timeout(self, timeout: int = None) -> None:

        start = time.time()

        while (
            (
                timeout and
                (timeout > (time.time() - start))
            ) or
            (not timeout and self.is_alive())
        ):
            time.sleep(0.001)

        self.terminate()

    @abstractmethod
    def terminate(self) -> None:

        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:

        raise NotImplementedError

@dataclass(slots=True)
class SubThread(BaseSubExecution):

    execution: threading.Thread | None = field(default=None, repr=False)

    def is_alive(self) -> bool:

        return self.execution.is_alive()

    def terminate(self) -> None:

        terminate_thread(self.execution)

    def run(self, *args, **kwargs) -> None:

        self.execution = self.execution or threading.Thread(*args, **kwargs)
        self.execution.start()

@dataclass(slots=True)
class SubProcess(BaseSubExecution):

    execution: subprocess.Popen | None = field(default=None, repr=False)
    result: subprocess.CompletedProcess | None = field(init=False, default=None, repr=False)

    _running: bool = field(init=False, default=False, repr=False)

    def is_alive(self) -> bool:

        return self._running

    def terminate(self) -> None:

        self.execution.kill()

        self._running = False

    def run(
            self,
            *args,
            data=None,
            capture_output=False,
            timeout=None,
            check=False,
            **kwargs
    ) -> subprocess.CompletedProcess:

        if data is not None:
            if kwargs.get('stdin') is not None:
                raise ValueError('stdin and input arguments may not both be used.')

            kwargs['stdin'] = subprocess.PIPE

        if capture_output:
            if kwargs.get('stdout') is not None or kwargs.get('stderr') is not None:
                raise ValueError(
                    'stdout and stderr arguments may not be used '
                    'with capture_output.'
                )

            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE

        with (self.execution or subprocess.Popen(*args, **kwargs)) as process:
            self._running = True

            self.execution = process

            try:
                stdout, stderr = process.communicate(data, timeout=timeout)

            except subprocess.TimeoutExpired as exc:
                self.terminate()

                # noinspection PyUnresolvedReferences,PyProtectedMember
                if subprocess._mswindows:
                    exc.stdout, exc.stderr = process.communicate()

                else:
                    process.wait()

                raise

            except (
                Exception, SystemExit, SystemError,
                InterruptedError, KeyboardInterrupt
            ) as e:
                self.terminate()

                raise e

            return_code = process.poll()

            if check and return_code:
                raise subprocess.CalledProcessError(
                    return_code, process.args,
                    output=stdout, stderr=stderr
                )

        self.execution = None
        self.result = subprocess.CompletedProcess(
            process.args, return_code, stdout, stderr
        )

        return self.result
