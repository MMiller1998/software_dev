from trains.errors import TrainsBaseException


class PlayerMisbehaveException(TrainsBaseException):
    pass


class NotEnoughDestinationsException(TrainsBaseException):
    """
    Raised when there are not enough ``Destination`` for the referee to offer
    enough to every player.
    """
    pass


class DestinationChoiceException(PlayerMisbehaveException):
    """
    Raised when a player makes an invalid destination selection.
    """
    pass


class TooManyPlayersException(PlayerMisbehaveException):
    pass


class TooFewPlayersException(PlayerMisbehaveException):
    pass


class PlayerTimeoutException(PlayerMisbehaveException):
    pass

class CardDeckSizeException(TrainsBaseException):
    """
    Raised when the card deck passed to the *referee* is not the right size.
    """
    pass
