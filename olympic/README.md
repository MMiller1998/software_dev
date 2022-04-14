# Trains

This repository contains code, design documents, questions about designs, and
other files which pertain to the development of
[The Game: Trains](https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html).

## Setup

Python version 3.6 or greater is required.

To install this project, simply use `make`.

```bash
make
```

You can specify a specific version of Python using an override.
By default, the `python3` interpreter is used.

```shell
make -e PYTHON=python3.9
```

## Usage

### Running Python Modules

`make` creates a Python venv in `Other/venv`. To call Python modules directly,
you must activate the venv before anything else.

```shell
source Other/venv/bin/activate
```

## Testing

Tests are written using the standard Python `unittest` module.

```shell
# run all tests using a helper script
Train/xtest

cd Other
source venv/bin/activate

# run all tests
python3 -m unittest

# run a specific test called test_empty_map
python3 -m unittest trains.tests.test_map.TestTrainMap.test_empty_map
```

GUI tests can be skipped by masking the `DISPLAY` environment variable.

```shell
env DISPLAY= Train/xtest
```

## Development

Documentation can be opened in a browser window.

```shell
cd Other
pydoc -b
```

## Project Structure

All Python source code is found in `Other/trains`, unit tests in `Other/tests`,
and some examples in `Other/tests/examples`.

`trains.map.TrainMap` represents just the details about a _map_. It is a graph of
`trains.graph_elements.TrainPlace` and `trains.graph_elements.TrainConnection`.
`trains.map.TrainMap` does not store anything about game state nor visualization.

`trains.graph_elements.TrainPlace` and `trains.graph_elements.TrainConnection` are
"doubly-linked" facilitating graph-traversal using object-oriented syntax.

`trains.editor.visualizer.CartesianTrainMap` is an extension of `trains.map.TrainMap`
which stores positional information on the `trains.graph_elements.TrainPlace` and
it can be rendered in a GUI using `PySimpleGUI`.

`trains.state.player.PlayerState` and `trains.state.referee.RefereeState` are both
immutable structs (so much as Python 3.6 could allow for immutability). A state
change is coded as the creation of a new state object, with different values.

`trains.state.player.Player` is a superclass to `trains.state.player.PlayerState`.
It is not currently used by itself, but it represents public information about
what anyone (_observer_, opponent _player_) can know about a _player_. A potential
strategy might use `trains.state.player.Player` to keep track of their opponents'
decisions.
