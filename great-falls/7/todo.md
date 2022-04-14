###Referee/RefereeGameState Changes
[x] Represent player and player state lists together, so we don't have to maintain parallel data
  - [x] Move player list from Referee to RefereeGameState (tupled with PlayerGameStates)
    - [x] Fix RefereeGameStateConstructor to accept players
    - [x] Use RefereeGameState to get Players
    - [x] Use passed in players during setup instead of Referee field for players
  - [x] Expose getter in RefereeGameState for Players so that ref can still handle talking to Players

[x] Move Referee deck into RefereeGameState

[] Create helper to remove try/except blocks

###PlayerGameState
[x] A PlayerGameState's `other_player_states` field is stored in relative turn order. Make this explicit

###Player
[x] Make sure ordering is consistent when a player returns the destinations it does not want

###Player Strategy
[x] Use more descriptive variable names when creating a strategy from a file
