import sys
import unittest
from io import StringIO
import os
import json

from unittest.mock import Mock
from trains.editor.visualizer import CartesianTrainMap
from trains.editor.app import run_visualizer
import PySimpleGUI as sg

from trains.time import timeout
from tests.examples.milestone3 import AIRPORTS

# It is easier to mock the sg.Graph object and assert whether draw_*
# was called instead of testing whether a real sg.Graph object contains
# the figures it should because a real sg.Graph object wants to belong
# to a finalized sg.Window before draw_* can be called.


class TestCartesianTrainMap(unittest.TestCase):
    def test_create_graph(self):
        train_map = CartesianTrainMap(width=600, height=700, key='test-key')
        self.assertEqual(train_map.graph.Key, 'test-key')
        self.assertTupleEqual(train_map.graph.CanvasSize, (600, 700))
        self.assertTupleEqual(train_map.graph.BottomLeft, (0, 700))
        self.assertTupleEqual(train_map.graph.TopRight, (600, 0))

    def test_empty_draws_nothing(self):
        train_map = CartesianTrainMap(width=600, height=700)
        train_map.graph = Mock(spec=sg.Graph)
        train_map.draw()

        train_map.graph.draw_circle.assert_not_called()
        train_map.graph.draw_line.assert_not_called()

    @unittest.skipUnless(
        condition=(sys.platform == 'linux' and 'DISPLAY' in os.environ and len(os.environ['DISPLAY']) > 0),
        reason='Not running on a Linux system or DISPLAY is not set.'
    )
    def test_window_closes_automatically(self):
        infile = StringIO(json.dumps(AIRPORTS))
        msg = 'Window should have closed after 3s, but did not close after 5s.'
        with timeout(5, lambda: self.fail(msg)) as t:
            run_visualizer(infile, duration=3)

        msg = 'Window should have closed after 3s, but closed before 3s.'
        self.assertGreaterEqual(t.get_elapsed(), 3, msg)


if __name__ == '__main__':
    unittest.main()
