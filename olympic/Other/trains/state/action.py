import abc

from trains.graph_elements import TrainConnection


class ActionOption(abc.ABC):
    """
    An ``ActionOption`` is an *action* a *player* may attempt on their turn.
    """
    pass


class AGameOfTrains(abc.ABC):
    """
    A ``AGameOfTrains`` is a turn-based game where a *player* may take their
    turn by doing one of two possible *actions*:

    - ask the *referee* for *colored cards*
    - spend *colored cards* and *rails* to acquire a *connection*

    After taking a turn, the turn is changed to the next player in order of
    player age.
    """

    @abc.abstractmethod
    def attempt_request_cards(self) -> 'AGameOfTrains':
        """
        Give the current *player* two random colored cards from the *referee*'s
        draw pile, if any.
        """
        ...

    @abc.abstractmethod
    def attempt_acquire_connection(self, connection: TrainConnection) -> 'AGameOfTrains':
        """
        Deduct the current *player*'s *rails* and *colored cards* to grant them
        ownership of the specified *connection*.
        """
        ...

    @abc.abstractmethod
    def is_game_over(self) -> bool:
        ...

    @abc.abstractmethod
    def next_turn(self) -> 'AGameOfTrains':
        """
        Change the turn so that the next :class:`ActionOption` accepted will affect
        the player after the current.

        In a game, this method should not be invoked manually by clients, it should
        only be called by :meth:`ActionOption.accept`.
        """
        ...


class WantCards(ActionOption):
    """
    An indication to get more cards.
    """
    def __repr__(self) -> str:
        return 'WantCards'


class Acquire(ActionOption):
    """
    An attempt made by a *player* on their turn to acquire a :class:`TrainConnection`.
    """
    def __init__(self, connection: TrainConnection):
        self.connection = connection

    def __repr__(self) -> str:
        return f'Acquire {self.connection}'
