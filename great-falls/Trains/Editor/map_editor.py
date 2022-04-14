import math
from tkinter import Tk, Canvas
from collections import defaultdict
from typing import List, Dict, Union
from Trains.Common.map import Map
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.city import City

RADIUS = 10
FONT_SETTINGS = ("Helvetica", "18")
CONNECTION_WIDTH = 4
TEXT_COLOR = "black"


def display_map(map: Map, timeout: Union[int, None] = None) -> None:
    """
    Displays the given map's cities and connections
    :param map: the map to visualize. This defines board size as well
    :param timeout: specifies if the window should close after a specified timeout - defaults to None
    :return: None
    """
    root = Tk()

    if timeout is not None:
        root.after(timeout, lambda: root.destroy())

    canvas = Canvas(root, bg="dark gray", height=map.height, width=map.width, highlightthickness=0)
    _draw_connections(canvas, map)
    _draw_cities(canvas, map.get_cities())
    canvas.pack()
    root.mainloop()


def _draw_cities(canvas: Canvas, cities: List[City]) -> None:
    """
    Draw the given list of cities on the given canvas
    :param canvas: the canvas to draw the cities on
    :param cities: the cities to draw
    :return: None
    """
    for city in cities:
        city_x, city_y = city.position
        _draw_point(canvas, city_x, city_y)
        canvas.create_text(city_x, city_y, text=city.name, fill=TEXT_COLOR, font=FONT_SETTINGS)


def _draw_point(canvas: Canvas, x: int, y: int) -> None:
    """
    Draw a point on the given canvas at the given x and y coordinates
    :param canvas: the canvas to draw the point on
    :param x: the point's x coordinate
    :param y: the point's y coordinate
    :return: None
    """
    canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="orange")


def _draw_connections(canvas: Canvas, map: Map) -> None:
    """
    Draw the given map's connections on the given canvas
    :param canvas: the canvas to draw the connections on
    :param map: the game map whose connections will be drawn
    :return: None
    """
    drawn_cities = set()
    cities = map.get_cities()
    for city in cities:
        connections = map.get_outgoing_connections(city)
        connections_by_to_city = _group_connections_by_to_cities(connections)
        for to_city, to_city_connections in connections_by_to_city.items():
            if to_city not in drawn_cities:
                _draw_connection_lines(canvas, to_city_connections)

        drawn_cities.add(city)


def _group_connections_by_to_cities(outgoing_connections: List[DirectedConnection]) -> \
        Dict[City, List[DirectedConnection]]:
    """
    Group a city's outgoing connections by their to_city city
    :param outgoing_connections: the list of connections to group
    :return: a dictionary of to_city cities to the connections for which that city is a to_city
    """
    grouped_cities = defaultdict(list)
    for connection in outgoing_connections:
        grouped_cities[connection.to_city].append(connection)

    return grouped_cities


def _draw_connection_lines(canvas: Canvas, connections: List[DirectedConnection]) -> None:
    """
    Draws lines on the canvas representing connections. If multiple connections go to the same city, the lines are drawn
    as curving out in the center to not overlap with the other connections
    :param canvas: the canvas to draw the lines on
    :param connections: the connections to draw
    :return: None
    """
    for i in range(0, len(connections)):
        connection = connections[i]
        city_1_x, city_1_y = connection.from_city.position
        city_2_x, city_2_y = connection.to_city.position
        curve_point_x, curve_point_y = _get_connection_curve_point(city_1_x, city_1_y, city_2_x, city_2_y, i)

        canvas.create_line(city_1_x, city_1_y,
                           curve_point_x, curve_point_y,
                           city_2_x, city_2_y,
                           fill=connection.color.value, width=CONNECTION_WIDTH)
        canvas.create_text(curve_point_x, curve_point_y,
                           text=str(connection.length),
                           fill=TEXT_COLOR,
                           font=FONT_SETTINGS)


def _get_connection_curve_point(city_1_x: int, city_1_y: int,
                                city_2_x: int, city_2_y: int,
                                scalar: int) -> (int, int):
    """
    Find the "curve point" between the city_1 and city_2 by some scalar, where a "curve point" represents how far
    out a line between the city_1 and city_2 should curve
    :param city_1_x: x coordinate of the city_1
    :param city_1_y: y coordinate of the city_1
    :param city_2_x: x coordinate of the city_2
    :param city_2_y: y coordinate of the city_2
    :param scalar: a scalar indicating how far out the curve point should be
    :return: the x and y coordinates of the curve point
    """
    midpoint_x, midpoint_y = _get_midpoint(city_1_x, city_1_y, city_2_x, city_2_y)
    distance = _calculate_distance(city_1_x, city_1_y, city_2_x, city_2_y)
    delta_x, delta_y = _get_negative_reciprocal_deltas(city_1_x, city_1_y, city_2_x, city_2_y)
    # We found that .08 is a magic constant that renders the connections nicely at any distance
    adjusted_scalar = scalar / (distance * .08)
    return (int(midpoint_x + (delta_x * adjusted_scalar)),
            int(midpoint_y + (delta_y * adjusted_scalar)))


def _get_negative_reciprocal_deltas(city_1_x: int, city_1_y: int, city_2_x: int, city_2_y: int) -> (int, int):
    """
    Takes the negative reciprocal of delta y / delta x, where y is the change in y between city_2 and city_1 and
    x is the change in x between city_2 and city_1. Essentially gets the slope perpendicular to the slope
    between city_1 and city_2
    :param city_1_x: x coordinate of the city_1
    :param city_1_y: y coordinate of the city_1
    :param city_2_x: x coordinate of the city_2
    :param city_2_y: y coordinate of the city_2
    :return: a tuple of the deltas for x and y
    """
    return -1 * (city_2_y - city_1_y), (city_2_x - city_1_x)


def _get_midpoint(city_1_x: int, city_1_y: int, city_2_x: int, city_2_y: int) -> (int, int):
    """
    Finds the midpoint between two points
    :param city_1_x: x coordinate of the city_1
    :param city_1_y: y coordinate of the city_1
    :param city_2_x: x coordinate of the city_2
    :param city_2_y: y coordinate of the city_2
    :return: a tuple representing the x and y coordinates of the midpoint
    """
    return (city_1_x + city_2_x) / 2, (city_1_y + city_2_y) / 2


def _calculate_distance(city_1_x: int, city_1_y: int, city_2_x: int, city_2_y: int) -> float:
    """
    :param city_1_x: x coordinate of the city_1
    :param city_1_y: y coordinate of the city_1
    :param city_2_x: x coordinate of the city_2
    :param city_2_y: y coordinate of the city_2
    :return: the euclidean distance between the city_1 and city_2 positions
    """
    return math.sqrt((city_1_x - city_2_x) ** 2 +
                     (city_1_y - city_2_y) ** 2)
