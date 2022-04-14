Explicitly state that PlayerGameState's `other_player_states` field is stored in relative turn order.
  - Expanded data definition of PlayerGameState to include ordering information for `other_player_states`
https://github.ccs.neu.edu/CS4500-F21/great-falls/commit/0b95253ab413596792f95496cf06558e8ef064d2

Referee and RefereeGameState had to maintain parallel lists of Player and PlayerGameState.
  - Coupled Players to their game states in RefereeGameState. Now Referee gets information about players from RefereeGamState
https://github.ccs.neu.edu/CS4500-F21/great-falls/commit/ab5f2d13f265e902f6840a014667488d424eb572

RefereeGameState did not hold all needed information to continue the game - did not have the cards.
  - Moved deck maintance from Referee to RefereeGameState
https://github.ccs.neu.edu/CS4500-F21/great-falls/commit/9b72ee857ad7011edf8c0a3c6e5a842c4da16c40

Destination ordering was not consistent across Players' setup calls, because of convertions from sets to lists.
  - Destination ordering is now preserved by removing selected destination from a master list
https://github.ccs.neu.edu/CS4500-F21/great-falls/commit/78a9ffeb8270e837df5dcb508afab77c265f26f7

Variables for file path in Strategy were not descriptive.
  - Changed variable names to be more clear
https://github.ccs.neu.edu/CS4500-F21/great-falls/commit/394a43bc9f336ce59c67deb50daa9c21079cc5b0
