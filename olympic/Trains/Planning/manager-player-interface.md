# Tournament Manager Design Task

draft
2021-11-03

## Overview

A _tournament manager_ (_manager_) manages _player_ requests to sign up for games,
observers wishing to observe games, and the spawning of _referees_ to run games.

### Expanded Player API

```
get_ready: PlayerGameInfo --> Void
// informs this player that they will soon be involved in a game with a referee
```

### Tournament Manager API

```
signup: PlayerInfo --> bool
// informs this manager that a player would like to sign up for a tournament
// the Player sends the manager the tournament entrance fee
// returns: True if player successfully signed up.

list_scheduled_games: --> PublicGameInfo[]
// query the manager for what games are soon to start
```


## Sign-Up

_Players_ will connect to a _tournament manager_ (or _manager_) to sign up
for a game. _Observers_ may also contact the _manager_ to request observation
of a game to take place.

### Sign-Up Diagram

```
                tournament
                 manager                         player (p_1)    . . .    player (p_n)
                    |                                 |                        |
                    |                                 |                        |
                    |           signup(info)          |                        |
                    | <------------------------------ |                        |
                    |                                 |                        |
                    |                                 |     signup(info)       |
                    | <------------------------------------------------------- |
    .               |                                 |                        |
    .               |                                 |                        |
    .               |                                 |                        |
 after enough       |                                 |                        |
 players sign up    |         get_ready(game1)        |                        |
                    | ------------------------------> |                        |
                    |         get_ready(game1)        |                        |
                    | -------------------------------------------------------> |
                    |                                 |                        |
 waiting for        |                                 |                        |                      observer (o_n)
 game to start      |                                 |                        |                              |
                    |                                 |                        |   list_scheduled_games()     |
                    | <---------------------------------------------------------------------------------------|
                    |              games[]            |                        |                              |
                    | ======================================================================================> |
                    |                                 |                        |                              |
                    |                                 |                        |      subscribe(game1)        |
                    | <---------------------------------------------------------------------------------------|
 manager spawns     |                                 |                        |                              |
 a referee          |                                 |                        |                              |
                    |       referee                   |                        |                              |
                    |          |                      |                        |                              |
                    |          |  setup(map,r,cards)  |                        |                              |
                    |          | -------------------> |                        |                              |
                    |          |                      |                        |                              |
                    |          |  setup(map,r,cards)  |                        |                              |
                    |          | --------------------------------------------> |                              |
                    |          |                      |                        |                              |
                    |          |                      |                        |                              |
                    |          |    notify(state)     |                        |                              |
                    |          | ---------------------------------------------------------------------------> |
                    |          |                      |                        |                              |
   .
   .   continued in https://www.ccs.neu.edu/home/matthias/4500-f21/local_protocol.html#%28part._g76999%29
   .
```

### Protocol

A _manager_ listens for incoming requests from _players_ indicating the desire to participate in a future game.
When some/enough _players_ have asked to sign up such that there are enough _players_ to run a _tournament_
(one or more games), the _manager_ calls `get_ready(game_info)` on _players_ to inform that they will be
participating in a game.

Between when a game is scheduled and when it actually starts, _observers_ may query the _manager_ by calling
`list_scheduled_games()`. The _manager_ responds with `games[]`, the scheduled games.


## Starting A Game

A _manager_ starts a game by spawning a _referee) to oversee and run the game. The referee calls _players_
as [previously described](https://www.ccs.neu.edu/home/matthias/4500-f21/local_protocol.html#%28part._g76999%29).
The _referee_ also pushes public information about the game state to _observers_ via `notify(state)`.

## Ending A Game

The _referee_ informs the _manager_ about a game's `outcome`.
The _referee_ terminates.
_Players_ might persist if they are playing more games in the tournament.
The _manager_ aggregates statistics on all game `outcome`.

### End Game Diagram
```
manager         referee                        player (p_1) . . . player (p_n)    observer (o_n)
   |              |                                |                 |                 |
   |              |                                |                 |                 |
   |              |     win(Boolean)               |                 |                 |
   |              | -----------------------------> |                 |                 |
   |              |     win(Boolean)               |                 |                 |
   |              | -----------------------------------------------> |                 |
   |              |                                |                 |                 |
   |              |                                |                 |                 |
   |  outcome     |     outcome                    |                 |                 |
   | <------------| -----------------------------------------------------------------> |
   |              |                                |                 |                 |
   |              +                                |                 |                 +
   |                                               |                 |
   |                                               |                 |
   |                                               |                 |
   |                                               |                 |
   |   
```

## Manager Spec

```
TournamentManager(TournamentMatching, playersPerTournamnet, signupTimeout)
```

A `TournametMatching` is a function which assigns _players_ to games. For example, it can be
"round robin" or "bracket".

`playersPerTournament` is a Nat in the range `[2, 100000)` indicating how many _players_
are to participate per _tournament_.

`signupTimeout` is a number representing the window of time _players_ have to call `signup`.

A _manager_ terminates after every game of the tournament is over. It returns total money
made from the tournament.
