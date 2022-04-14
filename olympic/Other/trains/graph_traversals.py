from typing import Set, Optional

from trains.graph_elements import TrainPlace, TrainConnection


def get_longest_path_from_place_length(
    origin: TrainPlace, occupied: Set[TrainConnection], visited: Optional[Set[TrainPlace]] = None
) -> int:
    """
    Find the length of the longest path along occupied connections from the given *place*.

    :param origin: The *place* to start the traversal from
    :param occupied: The ``TrainConnection``s occupied by the player being considered
    :param visited: Accumulator for *places* already visited in the traversal
    """
    if visited is None:
        visited = set()

    max_path_length = 0
    for neighbor in origin.get_neighbors(connection_filter=occupied):
        if neighbor not in visited:
            longest_path_between = max(origin.get_connections_between(neighbor, connection_filter=occupied), key=lambda p: p.length)
            path_length = longest_path_between.length + get_longest_path_from_place_length(neighbor, occupied, visited=visited.union({origin}))

            if path_length > max_path_length:
                max_path_length = path_length

    return max_path_length
