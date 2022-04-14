import unittest
from collections import Callable
from unittest.mock import patch
from Trains.Editor.map_editor import display_map, RADIUS, TEXT_COLOR, FONT_SETTINGS, CONNECTION_WIDTH
from Trains.Common.map import Map
from Trains.Other.color import Color
from Trains.Other.directed_connection import DirectedConnection
from Trains.Other.city import City


class MapEditorTests(unittest.TestCase):
    CITY_NAME_1 = "city1"
    CITY_NAME_2 = "city2"
    CITY_NAME_3 = "city3"
    POSITION_1 = (350, 350)
    POSITION_2 = (400, 400)
    POSITION_3 = (10, 750)
    CITY_1 = City(CITY_NAME_1, POSITION_1)
    CITY_2 = City(CITY_NAME_2, POSITION_2)
    CITY_3 = City(CITY_NAME_3, POSITION_3)

    DIRECTED_CONNECTION_1A = DirectedConnection(CITY_1, CITY_2, 3, Color.RED)
    DIRECTED_CONNECTION_1B = DirectedConnection(CITY_2, CITY_1, 3, Color.RED)
    DIRECTED_CONNECTION_2A = DirectedConnection(CITY_1, CITY_2, 5, Color.BLUE)
    DIRECTED_CONNECTION_2B = DirectedConnection(CITY_2, CITY_1, 5, Color.BLUE)
    DIRECTED_CONNECTION_3A = DirectedConnection(CITY_1, CITY_2, 4, Color.WHITE)
    DIRECTED_CONNECTION_3B = DirectedConnection(CITY_2, CITY_1, 4, Color.WHITE)
    DIRECTED_CONNECTION_4A = DirectedConnection(CITY_1, CITY_2, 4, Color.GREEN)
    DIRECTED_CONNECTION_4B = DirectedConnection(CITY_2, CITY_1, 4, Color.GREEN)
    DIRECTED_CONNECTION_5A = DirectedConnection(CITY_1, CITY_3, 4, Color.WHITE)
    DIRECTED_CONNECTION_5B = DirectedConnection(CITY_3, CITY_1, 4, Color.WHITE)
    DIRECTED_CONNECTION_6A = DirectedConnection(CITY_1, CITY_3, 4, Color.GREEN)
    DIRECTED_CONNECTION_6B = DirectedConnection(CITY_3, CITY_1, 4, Color.GREEN)

    map = Map(800, 800, [CITY_1, CITY_2, CITY_3],
              [DIRECTED_CONNECTION_1A, DIRECTED_CONNECTION_1B,
               DIRECTED_CONNECTION_2A, DIRECTED_CONNECTION_2B,
               DIRECTED_CONNECTION_3A, DIRECTED_CONNECTION_3B,
               DIRECTED_CONNECTION_4A, DIRECTED_CONNECTION_4B,
               DIRECTED_CONNECTION_5A, DIRECTED_CONNECTION_5B,
               DIRECTED_CONNECTION_6A, DIRECTED_CONNECTION_6B])

    @patch('Trains.Editor.map_editor.Canvas')
    @patch('Trains.Editor.map_editor.Tk')
    def test_display_map_draws_cities(self, _, mock_canvas):
        canvas_instance = mock_canvas.return_value
        display_map(self.map)

        canvas_instance.create_oval.assert_any_call(self.POSITION_1[0] - RADIUS, self.POSITION_1[1] - RADIUS,
                                                    self.POSITION_1[0] + RADIUS, self.POSITION_1[1] + RADIUS,
                                                    fill="orange")
        canvas_instance.create_oval.assert_any_call(self.POSITION_2[0] - RADIUS, self.POSITION_2[1] - RADIUS,
                                                    self.POSITION_2[0] + RADIUS, self.POSITION_2[1] + RADIUS,
                                                    fill="orange")
        canvas_instance.create_oval.assert_any_call(self.POSITION_3[0] - RADIUS, self.POSITION_3[1] - RADIUS,
                                                    self.POSITION_3[0] + RADIUS, self.POSITION_3[1] + RADIUS,
                                                    fill="orange")

        canvas_instance.create_text.assert_any_call(self.POSITION_1[0], self.POSITION_1[1],
                                                    text=self.CITY_NAME_1, fill=TEXT_COLOR, font=FONT_SETTINGS)
        canvas_instance.create_text.assert_any_call(self.POSITION_2[0], self.POSITION_2[1],
                                                    text=self.CITY_NAME_2, fill=TEXT_COLOR, font=FONT_SETTINGS)
        canvas_instance.create_text.assert_any_call(self.POSITION_3[0], self.POSITION_3[1],
                                                    text=self.CITY_NAME_3, fill=TEXT_COLOR, font=FONT_SETTINGS)

    @patch('Trains.Editor.map_editor.Canvas')
    @patch('Trains.Editor.map_editor.Tk')
    def test_display_map_draws_connections(self, _, mock_canvas):
        canvas_instance = mock_canvas.return_value
        display_map(self.map)

        canvas_instance.create_line.assert_any_call(self.POSITION_1[0], self.POSITION_1[1],
                                                    375, 375,
                                                    self.POSITION_2[0], self.POSITION_2[1],
                                                    fill="red", width=CONNECTION_WIDTH)
        canvas_instance.create_text.assert_any_call(375, 375,
                                                    text="3",
                                                    fill=TEXT_COLOR,
                                                    font=FONT_SETTINGS)

        canvas_instance.create_line.assert_any_call(self.POSITION_1[0], self.POSITION_1[1],
                                                    366, 383,
                                                    self.POSITION_2[0], self.POSITION_2[1],
                                                    fill="blue", width=CONNECTION_WIDTH)
        canvas_instance.create_text.assert_any_call(366, 383,
                                                    text="5",
                                                    fill=TEXT_COLOR,
                                                    font=FONT_SETTINGS)

        canvas_instance.create_line.assert_any_call(self.POSITION_1[0], self.POSITION_1[1],
                                                    357, 392,
                                                    self.POSITION_2[0], self.POSITION_2[1],
                                                    fill="white", width=CONNECTION_WIDTH)
        canvas_instance.create_text.assert_any_call(357, 392,
                                                    text="4",
                                                    fill=TEXT_COLOR,
                                                    font=FONT_SETTINGS)

        canvas_instance.create_line.assert_any_call(self.POSITION_1[0], self.POSITION_1[1],
                                                    348, 401,
                                                    self.POSITION_2[0], self.POSITION_2[1],
                                                    fill="green", width=CONNECTION_WIDTH)
        canvas_instance.create_text.assert_any_call(348, 401,
                                                    text="4",
                                                    fill=TEXT_COLOR,
                                                    font=FONT_SETTINGS)

        canvas_instance.create_line.assert_any_call(self.POSITION_1[0], self.POSITION_1[1],
                                                    180, 550,
                                                    self.POSITION_3[0], self.POSITION_3[1],
                                                    fill="white", width=CONNECTION_WIDTH)
        canvas_instance.create_text.assert_any_call(180, 550,
                                                    text="4",
                                                    fill=TEXT_COLOR,
                                                    font=FONT_SETTINGS)

        canvas_instance.create_line.assert_any_call(self.POSITION_1[0], self.POSITION_1[1],
                                                    170, 541,
                                                    self.POSITION_3[0], self.POSITION_3[1],
                                                    fill="green", width=CONNECTION_WIDTH)
        canvas_instance.create_text.assert_any_call(170, 541,
                                                    text="4",
                                                    fill=TEXT_COLOR,
                                                    font=FONT_SETTINGS)

    @patch('Trains.Editor.map_editor.Canvas')
    @patch('Trains.Editor.map_editor.Tk')
    def test_display_map_timeout(self, mock_root, _):
        root_instance = mock_root.return_value
        display_map(self.map, 10000)
        self.assertEqual(1, root_instance.after.call_count)
        args, _ = root_instance.after.call_args
        self.assertEqual(10000, args[0])
        self.assertTrue(isinstance(args[1], Callable))

    @patch('Trains.Editor.map_editor.Canvas')
    @patch('Trains.Editor.map_editor.Tk')
    def test_display_map_timeout_not_given(self, mock_root, _):
        root_instance = mock_root.return_value
        display_map(self.map)
        self.assertEqual(0, root_instance.after.call_count)
