To: Visualization Code Designers</br>
From: Matthew Miller and David Zhang</br>
Date: October 6, 2021</br>
Subject: Specifications for Trains Game Board Visualization

**ORGANIZATION:**</br>
Create a package called `map_visualizer`, with a public function called
`display_map` that takes in an instance of our `Map` class as defined in our data definition
(_map-design.md_). It will display the entire map.


**Output:**</br>
`display_map` should pop up a _Size_ x _Size_ window with a black background, where _Size_ is defined 
by the `size` attribute in `Map`.
Cities, as contained in a list by the `cities` attribute in Map, should be drawn as orange dots
with their names overlaid on the dots in tan text. The dot should be drawn at the city's `position` attribute.
Connections, as given per `City` as outgoing connections by the `get_outgoing_connections` method on `Map`, should be equally segmented lines 
between their `origin` and `destination` cities, 
where the number of segments is equal to the `length` attribute on `DirectedConnection`. The color of the line should be 
the `color` attribute in `DirectedConnection`. Note that a pair of directed connections (meaning the connections
from A to B and B to A that share the same `color` and `length`) should be displayed as a single 
segmented line, representing an undirected connection on the map between two cities. 


