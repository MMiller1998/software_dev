import copy
from collections import OrderedDict
from trains.editor.constants import \
    BACKGROUND_COLOR, \
    RADIUS, CIRCLE_LINE_COLOR, CIRCLE_LINE_WIDTH, \
    CIRCLE_FILL_COLOR, LINE_WIDTH, \
    RAIL_LABEL_COLOR
from trains.map import TrainMap, TrainPlace, TrainConnection
from typing import Tuple, Dict, List
from trains.map import RailColor
import PySimpleGUI as sg

Posn = Tuple[int, int]
"""
A ``Posn`` represents an x and y position in a plane, where x and y are
natural numbers.
"""


class CartesianTrainMap:
    """
    A ``CartesianTrainMap`` wraps :class:`TrainMap` which stores a
    :ref:`Posn` associated with each place.

    Every place in this ``CartesianTrainMap`` **must have a unique name**.

    The coordinate system's origin is the top-left corner of the viewport.
    In the context of this class's methods, *x* and *y* denote where the
    shape in question should be drawn where *x* is the number of px to the
    right of the origin and *y* is the number of px down from the origin.

    It can draw itself onto :mod:`PySimpleGUI` objects for visualization
    of the :class:`TrainMap` it represents.
    """

    __LexicographicAdjacencyList = Dict[str, Dict[str, List[TrainConnection]]]
    """
    A ``LexicographicAdjacencyList`` is a representation of a Graph where nodes are
    names of places and edges are a 2-tuple of :ref:`Posn`.

    It can efficiently access the edges between any two given nodes.

    It should be a :class:`collections.OrderedDict`. But in Python 3.6,
    the :class:`collections.OrderedDict` cannot be used as a type with
    a generic so here the type hint is just :class:`typing.Dict`.
    """

    def __init__(self, width: int, height: int, key='TrainsVisualizer'):
        """
        Creates an empty ``CartesianTrainMap`` which wraps a :class:`sg.Graph`.

        The parameters width and height are defined here:

        https://www.ccs.neu.edu/home/matthias/4500-f21/3.html

        They must be natural numbers in [10, 800] and [10, 800].

        :param width: width of the visualization
        :param height: height of the visualization
        :param key: key used to identify the PySimpleGUI element in a layout
        :raises ValueError: if width or height are not within range.
        """
        self.__dim_in_range(width)
        self.__dim_in_range(height)

        self._map = TrainMap()
        self._posns: Dict[str, Posn] = dict()
        self.width = width
        self.height = height

        self.graph = sg.Graph(
            canvas_size=(self.width, self.height),
            graph_bottom_left=(0, self.height),
            graph_top_right=(self.width, 0),
            background_color=BACKGROUND_COLOR, key=key
        )

    @staticmethod
    def __dim_in_range(num: int):
        """
        :param num: value to check
        :raises ValueError: if num is not an int or if num is outside
                            the range [10, 800]
        """
        if not isinstance(num, int):
            raise ValueError('Given a width or height value which is not an int.')
        if num > 800 or num < 10:
            raise ValueError('Given a width or height outside the range [10, 800].')

    def add_place(self, name: str, x: int, y: int) -> TrainPlace:
        """
        Adds a place to this map at the given x and y coordinates.

        :param name: name of the place, must be unique on this map
        :param x: x position of where a shape representing this place should
                  be drawn
        :param y: y position of where a shape representing this place should
                  be drawn
        :return: the newly added place
        """
        # TODO check x and y data type is Nat
        place = self._map.add_place(name)
        self._posns[place.name] = (x, y)
        return place

    def add_connection(self, place1: TrainPlace, place2: TrainPlace, color: RailColor, length: int) -> TrainConnection:
        """
        Wrapper around :meth:`TrainMap.add_connection`.

        :param place1: one of the places which this connection connects
        :param place2: the other place which this connection connects
        :param color: the color of this connection
        :param length: the length of the connection, must be either 3, 4, or 5
        :return: an struct representing the newly created connection
        """
        return self._map.add_connection(place1, place2, color, length)

    def get_positions(self) -> Dict[str, Posn]:
        """
        :return: a shallow copy of the positions of each place
        """
        return copy.copy(self._posns)

    def get_map(self) -> TrainMap:
        """
        :return: a shallow copy of the map
        """
        return copy.copy(self._map)

    def draw(self):
        """
        Paints a visualization of its :class:`TrainMap` onto its :class:`sg.Graph`.

        This method should be called after populating the :class:`TrainMap`,
        adding the ``graph`` to a *PySimpleGUI* ``window``, and calling
        ``finalize()`` on the ``window``.
        """
        connection_pairs = self._as_lexicographic_adjacency_list()

        # draw connections as lines
        for place1, connected_places in connection_pairs.items():
            posn1 = self._posns[place1]
            for place2, connections in connected_places.items():
                posn2 = self._posns[place2]
                self._draw_connections_between(posn1, posn2, connections)

        for place_name, posn in self.get_positions().items():
            self._draw_place(place_name, posn)

    def _draw_connections_between(self, posn1: Posn, posn2: Posn, connections: List[TrainConnection]):
        """
        Draw lines between two given ``Posn`` and label the midpoint between the two given ``Posn``
        with information about the color and length of the given ``TrainConnection``.

        :param posn1: position of one place
        :param posn2: position of a second place
        :param connections: all connections which exist between the two given places
        :return:
        """
        if not connections:
            return

        # lines are going to overlap anyways, so we just draw one of them
        # Matthias said he didn't care to implement an offset
        self.graph.draw_line(
            point_from=posn1,
            point_to=posn2,
            color=connections[0].color.value,
            width=LINE_WIDTH
        )

        self.graph.draw_text(
            location=self.__midpoint(posn1, posn2),
            text='\n'.join(f'{c.color.value},{c.length}' for c in connections),
            color=RAIL_LABEL_COLOR
        )

    def _draw_place(self, place_name: str, posn: Posn):
        """
        Draw a circle at a given location with text inside, which visualizes a *place*.

        :param place_name: text to draw inside circle
        :param posn: location to draw circle
        """
        self.graph.draw_circle(
            center_location=posn,
            radius=RADIUS,
            fill_color=CIRCLE_FILL_COLOR,
            line_color=CIRCLE_LINE_COLOR,
            line_width=CIRCLE_LINE_WIDTH
        )
        self.graph.draw_text(
            text=place_name,
            location=posn
        )

    def _as_lexicographic_adjacency_list(self) -> __LexicographicAdjacencyList:
        """
        A helper method for reconstructing the :class:`TrainMap` in a different
        graph representation so that it is easy to get all the connections between
        two cities.
        """
        # would builder pattern be helpful instead of reconstruction?
        connection_pairs: CartesianTrainMap.__LexicographicAdjacencyList = OrderedDict()

        place_names = list(self._posns.keys())
        place_names.sort()

        for i, origin in enumerate(place_names):
            connection_pairs[origin] = OrderedDict()
            for end in place_names[i + 1:]:
                connection_pairs[origin][end] = []

        for connection in self._map.get_all_connections():
            place_pair = [place.name for place in connection.get_places()]
            place_pair.sort()
            place1, place2 = place_pair
            connection_pairs[place1][place2].append(connection)

        return connection_pairs

    @staticmethod
    def __midpoint(posn1: Posn, posn2: Posn) -> Posn:
        x1, y1 = posn1
        x2, y2 = posn2
        return (
            int((x1 + x2) / 2),
            int((y1 + y2) / 2)
        )
