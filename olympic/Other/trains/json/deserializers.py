from typing import Set, List

from trains.map import TrainMap
from trains.graph_elements import RailColor, Destination, TrainPlace, TrainConnection
from trains.errors import InvalidTrainConnectionException
from trains.state.player import PlayerStateWrapper, PlayerState
from trains.state.action import ActionOption, WantCards, Acquire
from trains.state.cardsholder import CardDeck, CardHand, create_hand
from trains.json.types import JSONValue
from trains.game.player import PlayerActor, create_player_actor_from_strategy_name_via_path


def deserialize_map(data: JSONValue) -> TrainMap:
    """
    Deserialize a `Map`-shaped JSON value to a `TrainMap`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/3.html#%28tech._map%29

    :raises Exception: if `data` does not match the `Map` shape
    """
    train_map = TrainMap(int(data['width']), int(data['height']))
    nodes = dict()

    for city, posn in data['cities']:
        node = train_map.add_place(city, posn[0], posn[1])
        nodes[city] = node

    for place1, connections in data['connections'].items():
        for place2, segments in connections.items():
            for color_name, length in segments.items():
                color = RailColor(color_name)
                train_map.add_connection(nodes[place1], nodes[place2], color, length)

    return train_map


def deserialize_destination(train_map: TrainMap, data: JSONValue) -> Destination:
    """
    Deserialize a `Destination`-shaped JSON value to a `Destination`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._destination%29

    :param train_map: used as reference to find `TrainPlace`s matching `Name`s in
        the given `data`
    :raises ValueError: if the names from `data` are not places on the given `TrainMap`
    """

    return frozenset(map(lambda name: _name_to_place(name, train_map), data))


def deserialize_destinations(train_map: TrainMap, data: JSONValue) -> Set[Destination]:
    """
    Deserialize a list of `Destination`-shaped JSON values to a `Set[Destination]`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._destination%29

    :param train_map: used as reference to find `TrainPlace`s matching `Name`s in
        the given `data`
    """
    return {deserialize_destination(train_map, json_dest) for json_dest in data}


def deserialize_player_instance(train_map: TrainMap, data: JSONValue) -> PlayerActor:
    player_name, strategy_name = data
    return create_player_actor_from_strategy_name_via_path(player_name, strategy_name, train_map)


def deserialize_player_instances(train_map: TrainMap, data: JSONValue) -> List[PlayerActor]:
    return [deserialize_player_instance(train_map, player_instance) for player_instance in data]


def deserialize_color(data: JSONValue) -> RailColor:
    """
    Deserialize a `Color` as described in "The Game: Trains" to a `RailColor`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html#%28tech._color%29
    """
    return RailColor(data)


def deserialize_colors(data: JSONValue) -> CardDeck:
    """
    Deserialize a list of `Color`s as described in "The Game: Trains" to a `CardDeck`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html#%28tech._color%29
    """
    return [deserialize_color(c) for c in data]


def deserialize_card_star(data: JSONValue) -> CardHand:
    """
    Deserialize a `Card*`-shaped JSON value to a `CardHand`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._card%2A%29
    """
    card_hand = create_hand(0)
    for rail_color, count in data.items():
        card_hand[deserialize_color(rail_color)] = count
    return card_hand


def deserialize_action_option(train_map: TrainMap, data: JSONValue) -> ActionOption:
    """
    Deserialize an `Action` as described in milestone 6 to an `ActionOption`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/6.html#%28tech._action%29
    """
    if type(data) == str:
        return WantCards()
    else:
        connection = deserialize_acquired(train_map, data)
        return Acquire(connection)


def _find_connection(
    train_map: TrainMap, color: RailColor, length: int, place1_name: str, place2_name: str
) -> TrainConnection:
    """
    Find a connection within `train_map`. If no such connection exists, raise `InvalidTrainConnectionException`.
    """
    place_names = {place1_name, place2_name}
    for connection in train_map.get_all_connections():
        checking_place_names = {p.name for p in connection.get_places()}
        if place_names == checking_place_names and color == connection.color and length == connection.length:
            return connection

    raise InvalidTrainConnectionException()


def deserialize_acquired(train_map: TrainMap, data: JSONValue) -> TrainConnection:
    """
    Deserialize an `acquired` as described in milestone 5 to a `TrainConnection`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html
    """
    place1_name, place2_name, color, length = data
    return _find_connection(train_map, RailColor(color), length, place1_name, place2_name)


def deserialize_player(train_map: TrainMap, data: JSONValue) -> List[TrainConnection]:
    """
    Deserialize a `Player` as described in milestone 5 to a `List[TrainConnection]`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html
    """
    return [deserialize_acquired(train_map, acquired) for acquired in data]


def deserialize_this_player(train_map: TrainMap, data: JSONValue) -> PlayerState:
    """
    Deserialize a `ThisPlayer` as described in milestone 5 to a `PlayerState`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._thisplayer%29
    """
    dest1 = deserialize_destination(train_map, data["destination1"])
    dest2 = deserialize_destination(train_map, data["destination2"])
    num_rails = data["rails"]
    cards = deserialize_card_star(data["cards"])
    occupied = deserialize_player(train_map, data["acquired"])
    return PlayerState(frozenset([dest1, dest2]), occupied, cards, num_rails)


def deserialize_other_players(train_map: TrainMap, data: JSONValue) -> List[List[TrainConnection]]:
    """
    Deserialize a list of `Player` as described in milestone 5 to a `List[List[TrainConnection]]`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html
    """
    return [deserialize_player(train_map, player) for player in data]


def deserialize_player_state(train_map: TrainMap, data: JSONValue) -> PlayerStateWrapper:
    """
    Deserialize a `PlayerState` as described in milestone 5 to a `PlayerStateWrapper`.
    https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._playerstate%29
    """
    this_player = data["this"]
    other_players = data["acquired"]
    player_state = deserialize_this_player(train_map, this_player)
    other_player_acquireds = deserialize_other_players(train_map, other_players)
    return PlayerStateWrapper(player_state, other_player_acquireds)


def _name_to_place(name: str, train_map: TrainMap) -> TrainPlace:
    for place in train_map.get_all_places():
        if place.name == name:
            return place
    raise ValueError(f'{name} not associated to a city')
