# Data Definitions

All data is represented as JSON. JSON data definitions are re-used from the various specifications in milestone testing tasks.

The `Destination` name is shortened to `Dest` for diagram convenience.

The pieces of data not defined in milestones are:
- A `*Boolean*` is a JSON boolean, `true` or `false`
- An `*Integer*` is a JSON *number* with no *fraction*

Please see https://www.json.org/json-en.html for further JSON specification details.

The notation `DataType[]` means "an array of arbitrary size with elements `DataType`.

The notation `[DataType1, DataType2]` means "an array of length 2 where the first element is a `DataType1` and the second element is a `DataType2`.

# Client-Server Interactions

## Tournaments

### Starting a tournament
```
server <---------------------- client (c_1) . . . client (c_n)
  |                                |                 |
  |                                |                 |
  |                                |                 |
  |                                |                 |
  |     start(Boolean)             |                 | % true means the tournament
  | -----------------------------> |                 | % is about to start
  |     Map                        |                 |
  | <============================  |                 | % player submits a map
  .                                .                 . % in response
  .                                .                 .
  .                                .                 .
  |     start(Boolean)             |                 |
  | -----------------------------------------------> |
  |                                |                 |
  |     Map                        |                 |
  | <=============================================== |
```

### Running a tournament

```
server                         client (c_1) . . . player (c_n)
  |                                |                 |
  |  new(Map, PlayerName[])        |                 |
  | -----------------> referee     |                 |
  |                      |         |                 |
  .                      .         .                 .
  .                      .         .                 . % play a game
  .                      .         .                 . % (see below)
  .                      .         .                 .
  .                      .         .                 .
  |                      |         |                 | % the ranking
  |    Ranking, Rank     |         |                 | % & cheaters
  | <=================== |         |                 |
  .                     ___        .                 .
  .                                .                 .
  .                                .                 . % as long as
  .                                .                 . % one game can
  .                                .                 . % be played
  .                                .                 .
  |                                |                 |
  |  new(Map, PlayerName[])        |                 |
  | -----------------> referee     |                 |
  |                      |         |                 |
  .                      .         .                 .
  .                      .         .                 . % play last game
  .                      .         .                 .
  .                      .         .                 .
  |                      |         |                 |
  |                      |         |                 | % the ranking
  |    Ranking, Rank     |         |                 | % the "cheaters"
  | <=================== |         |                 |
  .                     ___        .                 .
  |                                |                 |
  |                                |                 |
```

### Terminating a tournament

```
server                        client (c_1) . . . player (c_n)
  |                                |                 |
  |                                |                 |
  |     end(Boolean)               |                 |
  | -----------------------------> |                 | % true means "winner"
  |                                |                 | % false means "loser"
  .                                .                 .
  .                                .                 .
  .                                .                 .
  .                                .                 .
  |     end(Boolean)               |                 |
  | -----------------------------------------------> |
  |                                |                 |
  |                                |                 |
```

## Games

### Starting a game
```
server                           client (c_1) . . . client (c_n)
  |                                  |                 |
  |                                  |                 |
  |     setup(Map,Integer,Card*)    |                 | % the map for this game
  | -------------------------------> |                 | % the number of rails
  |                                  |                 |
  | pick([Dest,Dest,Dest,Dest,Dest]) |                 | % given these 5 destinations,
  | -------------------------------> |                 | % where does the player
  |     [Dest, Dest, Dest]           |                 | % want to go (return 3)
  | <=============================== |                 |
  |                                  |                 |
  .                                  .                 .
  .                                  .                 . % repeat down age
  .                                  .                 .
  |                                  |                 |
  |     setup(Map,Integer,Card*)     |                 |
  | -------------------------------------------------> |
  |                                  |                 |
  | pick([Dest,Dest,Dest,Dest,Dest]) |                 |
  | -------------------------------> |                 |
  |     [Dest, Dest, Dest]           |                 |
  | <================================================= |
  |                                  |                 |
```

### Playing a game
```
   server                        client (c_1) . . . player (c_n)
      |                                |                 |
      |   play(PlayerState)            |                 | % player receives:
      | -----------------------------> |                 | % - current state

action 1:
      |     "more_cards"               |                 |
      | <============================  |                 | % request cards
      |     more(Card*)               |                 |
      | -----------------------------> |                 | % if there are cards
      |                                |                 |
      |                                |                 | % no cards available
      .        . .
action 2:
      |     Connection                 |                 | % acquire connection
  +-- | <============================  |                 |
  |   .                                .                 . % if legal:
  |   .                                .                 . % referee modifies game state
  +-> .                                .                 . % otherwise:
      .                                .                 . % kick player out
      .                                .                 .
      |   play(PlayerState)            |                 |
      | -----------------------------------------------> |
      |     Action                     |                 |
      | <=============================================== |
      |                                |                 |
      .                                .                 .
      .                                .                 .
      .                                .                 . % play until end condition:
      .                                .                 .
      .                                .                 . % When one of the player’s number of
      .                                .                 . % rails drops to 2, 1, or 0 at the
      .                                .                 . % end of a turn, each of the all
      .                                .                 . % other remaining players get to
      .                                .                 . % take one more turn.
      .                                .                 .
      .                                .                 . % The game also ends if every
      .                                .                 . % remaining player has had an
      |                                |                 | % opportunity to play a turn and the
      |   play(PlayerState)            |                 | % state of the game does not change.
      | -----------------------------> |                 |
      |     Action                     |                 |
      | <============================  |                 |
```

### Scoring a game

```
server                        client (c_1) . . . player (c_n)
  |                                |                 |
  |                                |                 |
  |     win(Boolean)               |                 |
  | -----------------------------> |                 | % true means "winner"
  |                                |                 | % false means "loser"
  .                                .                 .
  .                                .                 .
  .                                .                 .
  .                                .                 .
  |     win(Boolean)               |                 |
  | -----------------------------------------------> |
  |                                |                 |
  |                                |                 |
```

# Explanations

The `server` calling methods on `client`s will work via [remote method invocation](https://en.wikipedia.org/wiki/Proxy_pattern#Remote_proxy).

The `server` and `client`s in the diagrams represent two new components. These components will live on separate machines: the `server` on the same system as `RefereeActor` and `TournamentManager`, and `client`s on the same machines as `PlayerActor`s. The `server` and `client`s will communicate with one-another via remote method invocation and JSON according to the protocol defined above.

The `server` component will expose an API for a `RefereeActor` or `TournamentManager` (or other future server-side component) to call to interact with a `PlayerActor`. When called, the `server` will serialize input to JSON, send it to a `client`, which in turn de-serializes the information and calls the `PlayerActor` accordingly. If there is a response, the `client` serializes it, sends it to the `server`, where it is de-serialized and handled accordingly.

Further mechanics of tournaments (organization, who advances, rules of games, end conditions, etc) are specified across the class site.
