## Self-Evaluation Form for Milestone 10

Indicate below each bullet which file/unit takes care of each task.

The `remote proxy patterns` and `server-client` implementation calls for several
different design-implementation tasks. Point to each of the following: 

1. the implementation of the `remote-proxy-player`

	With one sentence explain how it satisfies the player interface. 
	
[RemotePlayerActor](https://github.ccs.neu.edu/CS4500-F21/olympic/blob/f24df4603e0b332042be553baa75dd24c2b2eb9c/Other/trains/remote/remote_player_actor.py#L25-L92) is our proxy player. Our player "interface" is not a proper interface but rather just the API and fields of our `PlayerActor` class, so `RemotePlayerActor` subclasses `PlayerActor` and overwrites its methods.

2. the unit tests for the `remote-proxy-player` 

We unfortunately did not get to implementing unit tests for `RemotePlayerActor`. We do have unit tests for (most) serialization and deserialization functions which `RemotePlayerActor` relies on, which is where most of our issues were, but that is different so we will not link it here (they should be easy to find).

3. the `server` and especially the following two pieces of factored-out
   functionality: 
   
The server logic is contained in [server.py](https://github.ccs.neu.edu/CS4500-F21/olympic/blob/f24df4603e0b332042be553baa75dd24c2b2eb9c/Other/trains/remote/server.py).

   - signing up enough players in at most two rounds of waiting 

[check_signups_after_wait_periods](https://github.ccs.neu.edu/CS4500-F21/olympic/blob/f24df4603e0b332042be553baa75dd24c2b2eb9c/Other/trains/remote/server.py#L77-L88)

   - signing up a single player (connect, check name, create proxy)
 
[handle_client_connect](https://github.ccs.neu.edu/CS4500-F21/olympic/blob/f24df4603e0b332042be553baa75dd24c2b2eb9c/Other/trains/remote/server.py#L57-L75) signs up a connected player as long as there are spots left. We do not check the name, whoops. During the signup phase we simply store client names and channels of communication, [proxies are created just before instanciating the tournament manager](https://github.ccs.neu.edu/CS4500-F21/olympic/blob/f24df4603e0b332042be553baa75dd24c2b2eb9c/Other/trains/remote/server.py#L107-L110).


4. the `remote-proxy-manager-referee`

[server_proxy](https://github.ccs.neu.edu/CS4500-F21/olympic/blob/f24df4603e0b332042be553baa75dd24c2b2eb9c/Other/trains/remote/client.py#L19-L83)

With one sentence, explain how it deals with all calls from the manager and referee on the server side.  

`server_proxy` is a coroutine that opens a connection to a Trains server, starts a loop to receive JSON messages via a coroutine on a small class named `JSONStreamParser.decode_next_value` (returns `None` if EOF is reached, which breaks from the loop and closes the connection), and then depending on the JSON message, deserializes the argument, executes the relevant player API call, then serializes and sends back the response.


<!--
The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.
-->

