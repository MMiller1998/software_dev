### Player API Updates
The player API should be extended with the following methods to support tournament 
manager operations:
```
def confirm_signup(datetime: int) -> None
"""
Confirms that the player has been signed up for the tournament and should expect to 
hear from a referee to setup the game soon.
:param datetime: the time in Unix epoch seconds 
"""
def game_result(ranking: int, continue: bool) -> None
"""
Informs the player of its ranking from the game it just played and whether it
is moving on in the tournament. If the player receives a True for continue, it should
expect to be placed into another game and hear from the Referee. Otherwise, it should
expect to hear about its tournament placing.
:param ranking: the ranking of the player for the previous game
:param continue: whether the player is moving to the next game
"""
def tournament_placing(placing: int) -> None
"""
Informs the player of its ranking in the entire tournament.
:param placing: the overall placing in the tournament
"""
```
### Player Protocol Updates
See the diagram below for the manager-player protocol. The diagram only shows one player, but it can be extrapolated to N players. To summarize:
  1. The manager confirms the request of a Player's signup by responding with the time of the registration. This call will only be made during the initial signup period
  2. Once the signup period is over, the player will be placed into a game. Once the player's game has concluded, the manager will communicate with the Player by giving it its ranking for the game and whether it is continuing in the tournament
     1. If the player is continuing in the tournament, the Referee will communicate with it and play the next game it belongs in, repeating step 2 once the next game ends
     2. If the player is out of the tournament, the manager will send it its overall ranking in the tournament, marking the last call that will be made to the player  

![alt text](https://raw.github.ccs.neu.edu/CS4500-F21/badlands/master/Trains/Other/images/manager-player-sd.svg?token=AAACH35WXPD2FUC52R7ERTDBRRKHG)

### Tournament Manager Spec
The tournament manager is responsible for organizing players into games as part of a larger series of games known as the 
tournament. To allow for player signups, the manager should receive signups for a specified amount of time, until 
signups close, at which point further player attempts to sign up are rejected. The manager will confirm to a player that
it has successfully signed up in the tournament with the time it was registered in Unix epoch seconds. 
As players sign up, the manager is responsible for putting them in a game queue that is sorted by age, where the oldest 
player is the one who signed up first. Any age ties are broken by which players are processed first.

Once the signup period is over, the tournament manager will begin the tournament. The tournament is run in rounds. A 
round is a series of sequential games where each player plays in exactly one game. As games complete, players who continue in the 
tournament will be put back into the queue for the next round, preserving their current sorted order. The tournament is 
over at the conclusion of a round that contains only one game.

To pick players for a game, the manager will greedily take eight players from the round queue until there are nine or 
fewer players. If there are nine players left in the queue, the manager will create two games with four
and five players respectively. If there are 8 or fewer, the manager will create a game with all the remaining players.

To create a game, the manager will generate a valid map for up to eight players and create a referee to run the game
with the players chosen with the method described above. When the game concludes, the referee will inform the manager
of the game's result, including surviving player rankings and cheaters. The manager will then send surviving players 
their respective game rankings and whether they will continue in the tournament. When the player does not continue in the tournament,
the manager will send them their placing in the overall tournament and end communications.

At any point, tournament managers may receive a signup from an observer. The observer is then subscribed to the next
available referee. They will be subscribed to any subsequent games after their initial game's conclusion.
