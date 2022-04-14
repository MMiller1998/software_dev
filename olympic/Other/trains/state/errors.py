from trains.errors import TrainsBaseException


class GameStateException(TrainsBaseException):
    """
    Raised when something illegal happens during the setup or play of a game.
    """
    pass


class GameOverException(GameStateException):
    """
    Raised when a *player* tries to take a turn after the game has ended.
    """
    pass


class CantAcquireException(GameStateException):
    """
    Raised when a *player* attempts to acquire a *destination* but it is
    illegal to do so.
    """
    pass
