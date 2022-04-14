To: Game state developer</br>
From: Matthew Miller and David Zhang</br>
Date: October 13, 2021</br>
Subject: Specifications for Trains Game Game State

**Data Representation**

An UndirectedConnection is an Object with fields [_city_1: City, city_2: City, color: Color, length: int]
- where _city_1_ represents the city in the connection whose name is lexicographically least
- and _city_2_ represents the other city in the connection
- and _color_ represents the color of the connection
- and _length_ represents how many segments the connection has between 3 and 5

and represents an undirected connection that has been acquired by a player

A PublicPlayerState is an Object with fields [_acquired_connections: Set[UndirectedConnection]_]
- where _acquired_connections_ represents the connections that the player has acquired

and represents player state that is visible to all entities in the game

A PrivatePlayerState is an Object with fields 
[_cards: Dict[Color, int], destinations: Set(Destination), public_state: PublicPlayerState, num_rails: int_]
- where _cards_ is a mapping between color and positive integer, representing how many cards of that color the player has
- and _destinations_ is a collection of destinations that the player has
- and _public_state_ is the public information about a player's state
- and _num_rails_ represents the number of rails that the player has

and represents a player state only visible to the player and the referee

A PlayerGameState is an Object with fields [_map: Map, own_state: PrivatePlayerState, other_player_states: List[PublicPlayerState]_]
- where _map_ represents the map of the game
- and _own_state_ represents the player's own player state
- and _other_player_states_ represents the information about the other players

and represents the game state that a player has access to

A RefereeGameState is an Object with fields [_map: Map, player_states: List[PrivatePlayerState], cards: Dict[Color, int]. active_player: int_]
- where _map_ represents the map of the game
- and _player_states_ is a list of player states ordered by player turn
- and _cards_ is a mapping between color and positive integer, representing how many cards of that color the 
- and _active_player_ represents the currently active player by turn number
referee has left

and represents the game state that the referee has access to

**Data Operations**

Getters for all fields of RefereeGameState, PlayerGameState, PrivatePlayerState, and PublicPlayerState</br>
**create_new_game**: (map: Map, num_players: int, player_destinations: List[Set[(City, City)]]) -> RefereeGameState</br>
Create a state with default settings/start values. player_destinations is ordered by player turn</br>
**create_player_game_state**: (ref_state: RefereeGameState, player_turn_number: int) -> PlayerGameState</br>
Return a PlayerGameState for the player whose turn order position is player_turn_number using the player states in ref_state</br>
**acquire_connection_for_player**: (ref_state: RefereeGameState, player_turn_number: int, city1: City, city2: City2, color: Color) -> RefereeGameState</br>
Update the given player's state with the newly acquired connection and new card/rail counts</br>
**can_acquire_connection**: (ref_state: RefereeGameState, player_turn_number: int, city1: City, city2: City2, color: Color) -> boolean 
Verify that the given player has enough cards and rails to acquire the connection between city1 and city2, and that the 
connection has not been acquired yet</br>
**give_player_cards**: (ref_state: RefereeGameState, player_turn_number: int) -> RefereeGameState</br>
Returns a new RefereeGameState where the given player has two additional random cards, or no additional cards if none are left</br>
**count_connected_destinations**: (ref_state: RefereeGameState) -> List[int]</br>
Count the number of destinations that each player successfully connected</br>
**should_terminate_game**: (ref_state: RefereeGameState) -> bool</br>
Checks if the game has reached the termination condition</br>
**remove_player**: (ref_state: RefereeGameState, player_number: int) -> RefereeGameState</br>
Remove the given player from the game state</br>
**perform_turn**: (player_state: PlayerGameState) -> Union[(city1: City, city2: City2, color: Color), None]</br>
Performs a player turn. Returns a 3-tuple representing a connection to acquire, or None to represent receiving cards
