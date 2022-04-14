class TrainsBaseException(Exception):
    """
    A custom exception raised in modules of :mod:`trains`.
    """
    pass


class InvalidTrainConnectionException(TrainsBaseException):
    """
    A custom exception denoting that illegal options are used in
    trying to create a *connection*.
    """
    pass


class TrainConnectionToSelfException(InvalidTrainConnectionException):
    """
    Raised when attempting to create a *connection* from a place to itself.
    """
    pass


class TrainConnectionLengthException(InvalidTrainConnectionException):
    """
    Raised when attempting to create a *connection* with an illegal length.

    See :const:`trains.constants.TRAIN_CONNECTION_LENGTHS` for valid lengths.
    """
    pass


class AddToMapException(TrainsBaseException):
    """
    A custom exception denoting that the object that is being created on
    this map cannot exist on this map.
    """
    pass


class DuplicateTrainConnectionException(AddToMapException):
    """
    Raised when attempting to create a *connection* between two places when
    there already exists a *connection* between those *places* with the same color.
    """
    pass
