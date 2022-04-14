from enum import Enum
from typing import Union, Tuple, Any, Callable


class MethodStatus(Enum):
    """
    Enum for indicating method call status.

    Specifically, this is used as an indicator of valid/invalid player
    actions, as an invalid player action could include raising an exception.
    """
    OK = 'ok'
    ERROR = 'error'


def safe_player_call(call: Callable) -> Union[Tuple[MethodStatus, Any], MethodStatus]:
    """
    Executes a lambda which makes calls to `PlayerActor` methods safely.

    :return: either a tuple indicating success and the return value, or an error indicator
    """
    try:
        return MethodStatus.OK, call()
    except:
        return MethodStatus.ERROR
