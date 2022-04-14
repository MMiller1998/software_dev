```
def select_destinations(destinations: Set[Destination], train_map: Map) -> Set[Destination]: 
""" 
Choose two destinations from the given set of destinations. This method should only be called once. This call must be during the game's setup phase 
:param destinations: The set of 5 destinations to choose from 
:param train_map: The train map with the cities and their connections, so the player can make an informed choice about their destinations 
:returns A set of two destinations that will be this player's destinations 
"""

def get_turn(game_state: PlayerGameState) -> Union[UndirectedConnection, None]: 
""" 
Gets this player's action for their turn based on the player's state. This method should be called repeatedly throughout the game on the player's turn.
If the player does not return a valid turn in time, they will be removed from the game
:param game_state: The current player's game state, allowing this player to make an informed turn
:returns an undirected connection representing an attempt to acquire that connection,
or None if the player wants cards 
"""

def end_game(ranking: int) -> None: 
""" 
Informs the player that the game has ended, and tells them their final ranking. This method should only be called once when the game is over. The player should receive no calls after this method is called 
:param ranking: the place this player finished in 
:returns None 
"""
```