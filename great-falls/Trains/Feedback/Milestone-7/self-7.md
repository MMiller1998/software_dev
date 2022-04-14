## Self-Evaluation Form for Milestone 7

Please respond to the following items with

1. the item in your `todo` file that addresses the points below.

2. a link to a git commit (or set of commits) and/or git diffs the resolve
   bugs/implement rewrites: 

It is possible that you had "perfect" data definitions/interpretations
(purpose statement, unit tests, etc) and/or responded to feedback in a
timely manner. In that case, explain why you didn't have to add this
to your `todo` list.

These questions are taken from the rubric and represent some of 
critical elements of the project, though by no means all of them.

If there is anything special about any of these aspects below, you may also point to your `reworked.md` and/or `bugs.md` files. 

### Game Map 

- a proper data definition with an _interpretation_ for the game _map_
  - We were satisfied with our representation and interpreation of the game map, and did not have feedback to implement about it. 
    - [Our game map and interpretation](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Common/map.py#L10-L25)

### Game States 

- a proper data definition and an _interpretation_ for the player game state
  - We were satisfied with our representation and interpreation of the a player game state, and did not have feedback to implement about it. 
    - [Our player game state and interpretation](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Common/player_game_state.py#L7-L22)

- a purpose statement for the "legality" functionality on states and connections 
  - We were satisfied with our method to check legality, and did not have feedback to implement about it. 
    - [The method in `RefereeGameState` to check legality](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Admin/referee_game_state.py#L74-L79)
    - [The method in `PlayerGameState` to get legally acquirable connections](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Common/player_game_state.py#L38-L47)

- at least _two_ unit tests for the "legality" functionality on states and connections 
  - [RefereeGameState tests](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Other/tests/test_referee_game_state.py#L112-L124)
  - [PlayerGameState tests](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Other/tests/test_player_game_state.py#L83-L94)

### Referee and Scoring a Game

The functionality for computing scores consists of 4 distinct pieces of functionality:

  - awarding players for the connections they connected
    - [Method](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Admin/referee_game_state.py#L157)
    - [Test](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Other/tests/test_referee_game_state.py#L194)

  - awarding players for destinations connected
    - [Method](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Admin/referee_game_state.py#L167)
    - [Test](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Other/tests/test_referee_game_state.py#L209)

  - awarding players for constructing the longest path(s)
    - [Method](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Admin/referee_game_state.py#L191)
    - [Test](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Other/tests/test_referee_game_state.py#L224)

  - ranking the players based on their scores
    - A referee constructs a `GameResult` that ranks the players
      - [Where the referee makes the constructor call](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Admin/referee.py#L155)
      - [Where the players are ranked](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Other/game_result.py#L20-L29)
        - [Tests for the `GameResult` constructor](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/Trains/Other/tests/test_game_result.py#L8-L13)

Point to the following for each of the above: 

  - piece of functionality separated out as a method/function:
  - a unit test per functionality

### Bonus

Explain your favorite "debt removal" action via a paragraph with
supporting evidence (i.e. citations to git commit links, todo, `bug.md`
and/or `reworked.md`).

Our favorite debt removal action was moving the `Referee`'s player list into the `RefereeGameState`. When we first implemented players ([Commit in the old repo](https://github.ccs.neu.edu/CS4500-F21/badlands/commit/1cbe6d6890f7323db5191b4e6cab54cae1fe1c95#diff-2a5b0bd6ae6de3fe3e7e4d82577a6e5b3478664f72967b8baeeebd47791c346c)), we maintained separate lists because that was the easiest option to implement, despite knowing that parallel lists were a design flaw. Coupling these lists together simplified our turn rotation logic ([Lines 94-103 in the diff for `Referee.__progress_turn`](https://github.ccs.neu.edu/CS4500-F21/great-falls/commit/ab5f2d13f265e902f6840a014667488d424eb572#diff-3cccaa7edfccbf58e8dc07be0c37bb997d70d1f32e0d350a27f8a80c2cc177e6L94-R103)) and moved our `RefereeGameState` closer to being an object that fully represents the game at any given turn.
- This was the first task in our [todo.md](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/7/todo.md)
- And the second task we completed [reworked.md](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/94f12b6aaa86caba4efc00a60d080bf0c6874248/7/reworked.md)




