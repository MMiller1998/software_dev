1. Referee asks a player to choose their destinations by calling `select_destinations` on the player, passing in a set 
of 5 destinations and the game map containing all the cities and connections. 
   1. The player returns a set of two destinations. 
2. The ref performs step 1 on all N players in the game before proceeding to the next step.
3. The ref will call `get_turn` on the player whose turn is next, passing in a `PlayerGameState` that contains the 
most recent game information available to that player. 
   1. This player returns their action for the turn. 
4. The ref performs step 3 on all the players sequentially, looping through each of them in order and passing in a `PlayerGameState` 
that contains all the information from the previous players' turns. This continues until the game termination condition 
is reached, and all the players have made their final turn.
5. Once the last round of turns is completed, the ref will score and rank the players, and call `end_game` on each of 
the players providing their rank. This will be the last call between the ref and the player.

The following sequence diagram illustrates this protocol for a game with 3 players, but is expandable to N players:

![Trains/Other/images/player_protocol_sd](https://raw.github.ccs.neu.edu/CS4500-F21/badlands/master/Trains/Other/images/player_protocol_sd.svg?token=AAACH36CXPZXHMTB4FGCGT3BRRKA2)
