# Player error handling

There are a few types of issues that can occur from getting player input:
1. Player takes too long and times out
2. Player raises an exception
3. Player makes an illegal move

Because the player can raise an exception, there must be some kind of try-catch around calls to the player. Due to this, we consolidate the error handling by raising exceptions for timeouts and illegal moves as well, because any of these events (and only these events) mean we should remove the player for "cheating". This means we can bubble up misbehavior and re-use cheater removal logic no matter what kind of issue a player component runs into.

Note that at the time of writing this, PlayerActor calls happen without `with` statements protecting against timeout errors. This is because the player proxy will be responsible for handling this, and will be implemented before the next milestone is due.
