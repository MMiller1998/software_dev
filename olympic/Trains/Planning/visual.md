To: Codemanistan
<br />
From: Brian Rego and Jennings Zhang
<br />
Date: October 6th, 2021
<br />
Subject: Design Plan for Trains visualization

The purpose of this memo is to describe our plan for how to design a program
which visualizes the map of the game we are developing, _Trains_.

Create the program with a file structure which conforms with the criteria
described here:

https://www.ccs.neu.edu/home/matthias/4500-f21/delivery.html

The program should be a Python module supporting Python version 3.6 on Linux.
The module should be named `codemanistan.trains`. It should provide a
function with the following signature:

```python
import trains.map

def show_visual(m: trains.map.TrainMap) -> None:
    """
    Opens a window which visualizes a given map board.

    m: data model of a map given in the ``Other/`` directory
    """
    ...
```

The function opens a window which visualizes a map of the game _Trains_.
The window should close when a user clicks on the "Close Window" button in
the title bar, or presses the key combination <kbd>ALT+F4</kbd>.

The background color of this window should be `#3b3b3b`. Any text inside the
window should be `#eeeeee`, with a font-size of 12pt, and in the system default
font.

`trains.map.TrainPlace` should be represented by circles with a 2px white stroke
and no fill. A circle's radius should be 20px. Somewhere near the circle,
show the text `f'{place.name},{place.id}` in a location which overlaps other visual
elements as little as possible. The bounding box of the text should be no more
than 5px from the closest point on the circle.

`trains.map.TrainConnection` should be represented by lines with 1px thickness. If there
exists one connection between two places, the line should be straight, otherwise the
line should be an arc.
They should be colored according to the value for `connection.color`. The length of the
line should be `10 * connection.length`. Somewhere near the midpoint of the line,
show the text
`f'{connection.id},{connection.color},{connection.length}\n{connection.acquiree},{connection.occupant}'`.

Use or implement an open-source library which does
[force-directed graph drawing](https://en.wikipedia.org/wiki/Force-directed_graph_drawing)
for determining the placement of _places_ and _connections_. If the library provides
defaults for the sizes of circles and width of lines, then you may disregard our above specification
on how to size the shapes. But in this case, the length of the lines between circles must
still use `connection.length` as a coefficient. Likewise, if the library provides functionality for
labeling shapes using text, then you may disregard our specification on how to position the text
and use the library's functionality instead.
