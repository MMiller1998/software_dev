# Player Interface

draft
2021-10-20

## `PlayerId`

A `PlayerId` is an `int` which uniquely identifies a _player_ for a game.

## Communication Protocols

All the following methods described might raise a `RefereeGoneException`
if the _referee_ does not respond to the _player_. This would probably
happen if the _player_ gets kicked from the game for doing nothing for
too long (which would otherwise cause a denial of service). It might
also happen if the _referee_ experiences an internal error.

## `PlayerSetup`

A `PlayerSetup` is an interface between a _player_ and the _referee_.
Its methods describe the protocol by how _player_ communicates with
_referee_ during setup of a game of _Trains_.

`PlayerSetup` is instantiated by the _player_ (client) after negotiating
with the _tournament manager_, but before setup of a game. Its methods
are only to be called during setup.

### `PlayerSetup.get_id() -> PlayerId`

Asks the _referee_ what `PlayerId` was assigned to this _player_.

### `PlayerSetup.get_map() -> TrainMap`

`get_map` is a method which asks the _referee_ for an object which
represents the _map_. This representation is from our solution to
Milestone 2, it only contains information  about places and connections.

### `PlayerSetup.get_total_participants() -> Nat`

Returns a natural number representing the total number of participants.

### `PlayerSetup.get_offered_destinations() -> FrozenSet[Destination]`

Asks the referee to identify 5 _destinations_ which the player may choose from.
These 5 _destinations_ are returned by `get_offered_destinations`.

### `PlayerSetup.pick_destinations(Destination, Destination)`

Informs the referee of the two _destinations_ the _player_ has chosen.
The two parameters should be members of the `frozenset` returned by
`PlayerSetup.get_offered_destinations()`.

May only be called once.

### `PlayerSetup.receive_rails() -> Nat`

Returns the number of rails the _player_ should start with.

May only be called once.

### `PlayerSetup.receive_cards() -> Dict[RailColor, int]`

Returns the number of each colored card the _player_ is given to start with.

May only be called once.

### `PlayerSetup.attempt_start_game() -> Optional[GamePlayer]`

To be called by the _player_ when they want to start the game.
Returns `None` if other _players_ are not ready to start.
Returns a `GamePlayer` is all _players_ are ready to start.

### Player Ready State

The referee considers the _player_ "ready to start" after they've called
`receive_rails`, `receive_cards`, and `pick_destinations` each at least once.

## `GamePlayer`

A `GamePlayer` is an interface between a _player_ and the _referee_.
Its methods describe the protocol by how _player_ communicates with
_referee_ during play of a game of _Trains_.

### `GamePlayer.acquire_connection(TrainConnection)`

Called by the _player_ on their turn when they want to acquire a _connection_.
Should only be called if _player_ can acquire the specified _connection_.
If they can't, a `CheatingException` is raised.

### `GamePlayer.draw_cards() -> List[RailColor]`

Called by the _player_ on their turn when they want to get cards from the
_referee_. Returns the colored cards the _referee_ hands to them.
Might raise a `CheatingException` is called out-of-turn.

### `GamePlayer.is_my_turn() -> bool`

Asks the _referee_ if this _player_ may take their turn next.

### `GamePlayer.is_game_over() -> Optional[EndGame]`

Asks the _referee_ whether the game is over.
Returns `None` is the game is still running.
Returns an `EndGame` if the game is over.

## `EndGame`

A `EndGame` is an interface between a _player_ and the _referee_.
Its methods describe the protocol by how _player_ communicates with
_referee_ during the end of a game of _Trains_.

### `EndGame.get_ranking() -> List[PlayerId]`

Returns the `PlayerId` of all participating _players_ ordered from
the one who scored the most points to the one who scored the least.

May only be called once.
