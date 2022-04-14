import json
from typing import TextIO
import PySimpleGUI as sg

from trains.utils import build_visual_map
from trains.editor.constants import AUTO_CLOSE_DURATION_SECONDS


def run_visualizer(infile: TextIO, duration=AUTO_CLOSE_DURATION_SECONDS):
    """
    Display a GUI visualizing a representation of a *Map*.

    The data is received from a text input stream as a JSON *Map* as defined here:

    https://www.ccs.neu.edu/home/matthias/4500-f21/3.html

    The GUI window closes itself after some time.

    :param infile: input stream from which the map can be read as well-formed, valid JSON
    :param duration: number of seconds before the window closes itself (default: 10)
    """
    map_representation = json.load(infile)
    train_map = build_visual_map(map_representation)

    window = sg.Window(
        title='Trains Editor (Milestone 3)',
        layout=[[train_map.graph]],
        finalize=True,
        auto_close=True,
        auto_close_duration=duration
    )
    train_map.draw()
    window.read(close=True)
