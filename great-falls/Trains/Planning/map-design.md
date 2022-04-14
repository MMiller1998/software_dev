A Color is one of:
- "red"
- "blue"
- "green"
- "white"

and represents the colors a train segment can have

A Length is one of:
- 3
- 4
- 5

and represents the number of segments a connection can have


A City is a Class with fields [_name: String, position: (Int, Int)_] 
- where _name_ is the unique name of a city
- _position_ is a tuple of an x and y coordinate in pixels, where (0,0) is the top left

and represents a city in the Trains game 

A DirectedConnection is a Class with fields [_from_city: String, to_city: String, length: Length, color: Color_]
- where _from_city_ is the name of the city that the connection is coming from
- _to_city_ is the name of the city that the connection is going to
- _length_ is how many segments the connection has
- _color_ is what color the connection is


and represents a directed connection between two cities in the Trains game

A Map is a Class with fields [_width: Int, height: Int, cities: [List-of City], adj_list: Dict[City, [List-of Connection]_]
- where _width_ is the width of the map in pixels
- where _height_ is the height of the map in pixels
- _cities_ is a list of all the cities on the game's board. City position coordinates must be < _size_.
- _adj_list_ is the mapping from cities to their outgoing connections. Outgoing connections with the same 
destination must have distinct colors


and represents a Trains game board with cities and their connections
