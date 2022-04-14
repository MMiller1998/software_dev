## Self-Evaluation Form for Milestone 6

Indicate below each bullet which file/unit takes care of each task:

1. In the player component, identify the following pieces of functionality:

  - `setup`, the function/method for receiving the game map etc.
    - [setup method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Player/player.py#L44) 
  - `pick`, the function/method for picking destinations from given alternatives
    - [pick method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Player/player.py#L49) 
  - `play`, the function/method for taking a turn
    - [play method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Player/player.py#L52) 
  - `more_cards`, the function/method for receiving more cards (if available)
    - [more_cards method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Player/player.py#L55) 
    - Our Player implementation does not need to do anything for more_cards
  - `win`, the function/method for receiving information about the outcome of the game
    - [win method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Player/player.py#L61) 
    - Our Player implementation does not need to do anything for win

2. In the referee component, identify the following pieces of major functionality:

  - a start-up phase, i.e., for setting up players with maps and destinations
    - [setup method to handle the entire start-up phase](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee.py#L100)
  - a play-turns phase, i.e., for running the game proper 
    - [run_turns method to handle the entire play-turns phase](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee.py#L120)
  - a shut down phase, i.e., for informing players of the outcome 
    - [end_game method to handle the entire shut down phase](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee.py#L139)


3. In the referee component, identify the following pieces of scoring functionality and their unit tests: 

[Scoring in the Referee component delegates to its game state](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee.py#L145). The
links below go to the game state methods

  - the functionality for granting points for segments per connection
    - [method to calculate score for segments](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee_game_state.py#L132)
    - [unit tests](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Other/tests/test_referee_game_state.py#L136)
  - the functionality for granting points for longest path
    - [method to calculate score for longest path](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee_game_state.py#L166)
    - [unit tests](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Other/tests/test_referee_game_state.py#L164)
  - the functionality for granting points for destinations connected
    - [method to calculate score for destinations connected](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee_game_state.py#L155)
    - [unit tests](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Other/tests/test_referee_game_state.py#L136-L161)

4. In the referee component, identify the functionality for ranking players

  - [The Referee scores the players, and then delegates ranking functionality to the GameResult class](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee.py#L144-L148)
    - [GameResult logic to rank players](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Other/game_result.py#L21-L28)

5. In the referee component, identify the functionality for eliminating misbehaving players 
  - [The Referee has many places where it will call this method, but this is the method that is responsible for removing cheaters](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/master/Trains/Admin/referee.py#L254)


The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.
