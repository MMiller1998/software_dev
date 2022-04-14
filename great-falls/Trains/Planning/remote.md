**[UML Sequence diagram](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/master/Trains/Other/images/interaction_diagram_player_admins.svg)**

**JSON definitions**:
- _Map_ (See [3 - The Image](https://www.ccs.neu.edu/home/matthias/4500-f21/3.html))
- _Card*_ (See [5 - The Strategy](https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._card%2A%29))
- _Destination_ (See [5 - The Strategy](https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._card%2A%29))
- _PlayerState_ (See [5 - The Strategy](https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._card%2A%29))
- _Acquired_ (See [5 - The Strategy](https://www.ccs.neu.edu/home/matthias/4500-f21/5.html#%28tech._card%2A%29))
- _Action_ (see [6 - Game!](https://www.ccs.neu.edu/home/matthias/4500-f21/6.html))

The client and server communicate by exchanging json objects. We represent these 
objects in the diagram as keys to a specific value (if value is in quotes) or keys
to the type of the value it should have. When the type of a value is a list with
a known length, this is represented as `[Type] * expected_length`. The server and client are responsible
for translating received json objects into implementations that the components can handle,
and translating the component's output back into json to send over the wire.


Control flow has 5 components (Manager, Referee, Server, Client, Player) and is as follows:</br>
(**Note:** Any interaction between Manager/Referee and Player goes through translation
by the Server and Client. For brevity's sake we do not explicitly state these interactions between local and remote components):
1. The client signs up for a tournament by giving its name to the Server
2. After the Server receives enough signups, it will pass them to the Manager in descending age order
3. The Manager informs the Players that it is beginning the tournament
   1. Players return game maps that the manager can use for the tournament
4. The Manager creates Referees and assigns players and a Map to these Referees
5. The Referee runs the game (see spec for control flow) and returns winning players and cheaters to the Manager
6. If the tournament should continue, go back to step 4. Otherwise:
7. Inform all noncheating Players whether they won the tournament

