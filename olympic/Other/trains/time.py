import signal
import time
from typing import Optional, ContextManager, Callable
from contextlib import contextmanager


class Timer(ContextManager['Timer']):
    """
    A ``Timer`` is a helper which records how long something took.
    """

    def __init__(self):
        self.__start: Optional[float] = None
        self.__end: Optional[float] = None

    def __enter__(self) -> 'Timer':
        """
        Starts this timer.
        """
        self.__start = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stops the timer.
        """
        self.__end = time.monotonic()

    def get_elapsed(self) -> float:
        """
        :return: number of seconds this context manager was open for
        """
        if not self.__start:
            return 0.0

        end = self.__end if self.__end else time.monotonic()
        return end - self.__start


@contextmanager
def timeout(seconds: int, callback: Callable[[], None]) -> Timer:
    """
    A context manager which uses ``SIGALRM`` to fire a given function
    after a fixed amount of time. The function is not executed
    if the ``with`` block exits before the specified time window.

    This is useful for timeouts. Provide ``timeout`` with a
    function which raises an exception. The exception will be
    raised if your code takes too long to run. When exceptions
    are raised, Python will still attempt to clean up any
    resources wrapped by other context managers.

    The context manager produces a :class:`Timer` which produces the
    elapsed time during this context manager.

    Protocol --- requirements and conditions:

    - Your OS must support `SIGALRM`; most UNIXes do.
    - Within the context manager, you must not use `SIGALRM`
    - Only the main thread can use (:mod:`signal` and thus) ``timeout``

    :param seconds: number of seconds before dispatching the callback
    :param callback: code to run after specified amount of time passes
    """
    signal.signal(signal.SIGALRM, lambda signum, fame: callback())
    signal.alarm(seconds)

    with Timer() as t:
        try:
            yield t
        finally:
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            signal.alarm(0)
