Pair: great-falls

Commit: [`3b8ba5`](https://github.ccs.neu.edu/CS4500-F21/great-falls/tree/3b8ba5f3257f5f9614d28c2e89babc4c6966400b) 

Score: 140/155

Grader: Eshwari

20/20: accurate self eval

`cheat strategy`

12/15 

- 10/10 proper design: (derive (extend) the BuyNow class and override the turn method) 
- 2/5: a unit test that makes sure that the requested acquisition is not on the map 
  - acknowledged on self-eval that you don't have this => 40% credit

`manager`

88/100 

The manager performs five totally distinct tasks:

- 10/10 pts: inform players of the beginning of the tournament, retrieve maps
- 20/20 pts: check that there are maps with enough destinations and pick one of those for the games 
	- 10/10pts: it doesn't matter how the manager picks a "good" map 
	- 10/10 pts:  the **same** predicate is used in both the `manager` and the `referee` (not copied code)
- 10/10 pts: allocating players to a bunch of games per round
- 30/30 pts: running the tournament, separate two functions
 	- 15/15: run a round of games
	- 15/15: run all rounds	
- 10/10 pts: inform surviving players at the very end whether they won the tournament

The points are for the existence of separate methods/functions _and_ well-chosen
names and/or purpose statements.

- 8/20 points for tests of the manager as a whole:
  - 4/10 for testing a single game (they know what the ref does, the manager must compute the same result (same inputs))
    - acknowledged in self eval this test is not present 
  - 4/10 for testing the allocation of players to games per round
    - acknowledged in self eval this test is not present => 40%

`remote.md`

20/20 

- 5/5 points for diagrams that incorporate a proxy layer in between logical components and mention for the exact same scenarios as in
  - [Logical Interactions](https://www.ccs.neu.edu/home/matthias/4500-f21/local_protocol.html)
  - [Logical Interactions 2](https://www.ccs.neu.edu/home/matthias/4500-f21/manager_protocol.html)

- 5/5 points for JSON format definitions, for each call and return in these diagrams

- 10/10 a "helpful" English explanation (as in helps you navigate their description)



