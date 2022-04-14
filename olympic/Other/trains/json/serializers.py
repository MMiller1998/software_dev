from typing import List, Iterable

from trains.map import TrainMap
from trains.graph_elements import Destination, RailColor
from trains.json.types import JSONValue
from trains.graph_elements import TrainPlace, TrainConnection
from trains.state.player import PlayerStateWrapper, PlayerState
from trains.state.action import ActionOption, WantCards, Acquire
from trains.state.cardsholder import CardDeck, CardHand
from trains.game.player import PlayerActor
from trains.game.types import Rank
from trains.strategy.lexico import lexicographically_sorted_places, lexicographically_sorted_destinations
from trains.tournament.types import TournamentResult


def serialize_place(place: TrainPlace) -> JSONValue:
    """
    Serialize a `TrainPlace` to a Python tuple in the shape of a `City` as
    specified in the milestone 3 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/3.html#%28tech._city%29
    """
    return place.name, (place.x_coord, place.y_coord)


def serialize_connections(connections: List[TrainConnection]) -> JSONValue:
    """
    Serialize a `List[TrainConnection]` to a Python object in the shape
    of a `Connections` as specified in the milestone 3 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/3.html#%28tech._connection%29
    """
    serialized_connections = dict()

    for conn in connections:
        place1, place2 = conn.get_places()
        lex1, lex2 = lexicographically_sorted_places([place1, place2])

        # ensure Target for Name is in Connections
        if lex1.name not in serialized_connections:
            serialized_connections[lex1.name] = dict()

        # ensure Segment for Name is in Target
        if lex2.name not in serialized_connections[lex1.name]:
            serialized_connections[lex1.name][lex2.name] = dict()

        serialized_connections[lex1.name][lex2.name][conn.color.value] = conn.length

    return serialized_connections


def serialize_connection_to_acquired(connection: TrainConnection) -> JSONValue:
    """
    Serialize a `TrainConnection` to a Python tuple in the shape of an
    `Acquired` as specified in the milestone 5 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._acquired%29
    """
    lex1, lex2 = lexicographically_sorted_places(connection.get_places())
    return (lex1.name, lex2.name, connection.color.value, connection.length)


def serialize_connections_to_player(connections: List[TrainConnection]) -> JSONValue:
    """
    Serialize a `List[TrainConnection]` to a Python list in the shape
    of a `Player` as specified in the milestone 5 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._player%29
    """
    return [serialize_connection_to_acquired(conn) for conn in connections]


def serialize_other_player_acquireds(other_player_occupieds: List[List[TrainConnection]]) -> JSONValue:
    """
    Serialize a `List[List[TrainConnection]]` to a Python list in the shape of a list of `Player` as specified in
    the milestone 5 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._player%29
    """
    return [serialize_connections_to_player(occupied) for occupied in other_player_occupieds]


def serialize_train_map(train_map: TrainMap) -> JSONValue:
    """
    Serialize a `TrainMap` to a Python object in the shape of a `Map` as specified
    in the milestone 3 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/3.html#%28tech._map%29
    """
    return {
        "width": train_map.width,
        "height": train_map.height,
        "cities": [serialize_place(place) for place in train_map.get_all_places()],
        "connections": serialize_connections(train_map.get_all_connections())
    }


def serialize_rail_color(rail_color: RailColor) -> JSONValue:
    """
    Serialize a `RailColor` to a Python string version of `Color` as
    specified in "The Game: Trains":
    https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html#%28tech._color%29
    """
    return rail_color.value

def serialize_card_deck(card_deck: CardDeck) -> JSONValue:
    """
    Serialize a `CardDeck` to a Python list of `Color`s as specified
    in "The Game: Trains":
    https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html#%28tech._color%29
    """
    return [serialize_rail_color(rail_color) for rail_color in card_deck]


def serialize_card_hand(card_hand: CardHand) -> JSONValue:
    """
    Serialize a `CardHand` to a Python dict inthe shape of a `Card*` as
    specified in the milestone 5 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._card%2A%29
    """
    return {serialize_rail_color(rail_color): count for rail_color, count in card_hand.items()}


def serialize_acquire(acquire: Acquire) -> JSONValue:
    """
    Serialize an `Acquire` action to a Python tuple in the shape of an `Acquired`
    as specified in the milestone 5 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._acquired%29
    """
    conn = acquire.connection
    place1, place2 = conn.get_places()
    lex1, lex2 = lexicographically_sorted_places([place1, place2])
    return (lex1.name, lex2.name, conn.color.value, conn.length)


def serialize_action(action: ActionOption) -> JSONValue:
    """
    Serialize a `ActionOption` to a Python value in the shape of an `Action` as
    specified in the milestone 6 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/6.html#%28tech._action%29

    :raises ValueError: if an unrecognized `ActionOption` subclass is passed
    """
    if type(action) == WantCards:
        return 'more cards'
    elif type(action) == Acquire:
        return serialize_acquire(action)

    raise ValueError('unrecognized action type')


def serialize_destination(destination: Destination) -> JSONValue:
    """
    Serialize a `Destination` to a Python tuple in the shape of a `Destination`
    as specified in the milestone 5 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._destination%29
    """
    return tuple(sorted([place.name for place in destination]))


def serialize_destinations(destinations: Iterable[Destination]) -> JSONValue:
    """
    Serialize a sequence of `Destination`s to a Python list in the shape of a
    JSON list of `Destination` as specified in the milestone 5 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._destination%29
    """
    return [serialize_destination(dest) for dest in destinations]


def serialize_rank(rank: Rank[PlayerActor]) -> JSONValue:
    """
    Serialize a `Rank` or `PlayerActor`s to a Python tuple in the shape of
    a `Rank` as specied in the milestone 8 testing task:
    https://www.ccs.neu.edu/home/matthias/4500-f21/8.html#%28tech._rank%29
    """
    return sorted([player.name for player in rank])


def serialize_tournament_result(result: TournamentResult) -> JSONValue:
    """
    Serialize a `TournamentResult` to a Python tuple in the shape of a
    `Rank` of winners and a `Rank` of cheaters.
    https://www.ccs.neu.edu/home/matthias/4500-f21/9.html
    """
    winners, cheaters = result
    return (serialize_rank(winners), serialize_rank(cheaters))


def serialize_player_state(ps: PlayerState) -> JSONValue:
    """
    Serialize a `PlayerState` to a a Python dict in the shape of a `ThisPlayer`
    as specified in milestone 5:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._thisplayer%29
    """
    destination1, destination2 = lexicographically_sorted_destinations(ps.destinations)
    return {
        "destination1": serialize_destination(destination1),
        "destination2": serialize_destination(destination2),
        "rails": ps.num_rails,
        "cards": serialize_card_hand(ps.cards),
        "acquired": serialize_connections_to_player(ps.occupied)
    }


def serialize_player_state_wrapper(psw: PlayerStateWrapper) -> JSONValue:
    """
    Serialize a `PlayerStateWrapper` to a Python dict in the shape of a `PlayerState`
    as specified in milestone 5:
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._playerstate%29
    """
    return {
        "this": serialize_player_state(psw.player_state),
        "acquired": serialize_other_player_acquireds(psw.other_player_acquireds)
    }
