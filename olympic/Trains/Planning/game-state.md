# Game State Representation

changed
2021-10-19

first draft
2021-10-12

## `Deck`

A `Deck` is a `Dict[RailColor, int]` which counts how many cards of which color an entity has.

## `PlayerNumber`

A `PlayerNumber` is an `int` which represents a _player_'s turn order.

## `BoardState`

A `BoardState` represents the public information about the game's state which any player, observer or referee can see.

It has the fields:

- `BoardState.map`, a `TrainMap`
- `BoardState.owners`, a `Dict[TrainConnectionId, PlayerNumber]` mapping connections to who owns them
- `BoardState.turn`, a `PlayerNumber` representing who may make the next move
- `BoardState.total_players`, the total number of _players_ in the game involving this board.

## `PlayerState`

A `PlayerState` is the state of the game which an AI player (user) knows about.

- `PlayerState.cards`, a `Deck` representing the amount of each colored card the _player_ has in their hand
- `PlayerState.destinations`, a `FrozenSet[Destination]` representing the destinations the _player_ chose at the beginning of the game
- `PlayerState.num_rails`, an `int` representing the number of rails that the _player_ currently has
- `PlayerState.board`, a `BoardState` containing information about the board and the `PlayerNumber` of their opponents.

## `RefereeGameState`

A `RefereeGameState` is the state of the game which the _referee_ can see.
It has data on all the players, which is private information that players
may not know about one another. (Hence, it is necessary for players and
referees to have different representations of state.)

It has

- `RefereeGameState.players`, a `list[PlayerState]` containing data for all _players_
- `RefereeGameState.board`, a `BoardState`
- `RefereeGameState.draw_pile`, a `Deck` which counts how many colored cards are left which may be given out to players upon request
- `RefereeGameState.ending_player`, a `PlayerNumber` which, when it comes to their turn, the game ends before the turn.

## Referee Operations

The `RefereeGameState` is also the manager and ground truth of how the game is being run.

When players attempt to make moves, methods are called on an instance of `RefereeGameState`.

### `attempt_acquire_connection(connection: TrainConnectionId)`

Called when a player is attempting to make an acquisition of a _connection_ on their turn.

If the game is already over, raises `GameOverException`.

Returns `False` if the move was illegal. Otherwise, returns `True` if the move
was legal and the state was changes.

An acquisition move is legal if and only if:

- the player's number of cards for the same color as the connection is greater or equal to
  the length of the _connection_
- the player's number of rails is greater or equal to the length of the _connection_

If all conditions are met, return `True`. The following state changes are applied:

- `turn` is changed to the next `PlayerNumber` in order of `players`
- the _player's_ number of cards for that color and their number of rails is deducted
  by the length of the _connection_
- `board` is updated to reflect the _player's_ ownership of the _connection_ 

### `attempt_request_cards(player: PlayerNumber, connection: TrainConnectionId) -> List[RailColor]`

Called when the current _player_ is attempting to request cards from the _referee_ during their turn.

If the game is already over, raises `GameOverException`.

The return value is a list of length 0, 1, or 2, which contains random `RailColor`
depending on what is left in the `RefereeGameState.bank`. The counts in
`RefereeGameState.bank` are deducted appropriately.

### `is_game_over(current_player: PlayerNumber) -> bool`

A method which decides whether the game is over. It should be called after each successful acquisition-type move.
If the _player_ who made the most recent valid acquisition has 0, 1, or 2 rails remaining, `is_game_over` will
set `RefereeGameState.ending_player` to `current_player`.

Returns `True` if `RefereeGameState.ending_player` is not `None` and it is `ending_player`'s turn.
