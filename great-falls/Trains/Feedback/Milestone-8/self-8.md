## Self-Evaluation Form for Milestone 8

Indicate below each bullet which file/unit takes care of each task.

The `manager` performs five completely distinct tasks, with one
closely related sub-task. Point to each of them:  

1. inform players of the beginning of the game, retrieve maps

[The manager's setup function](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L37-L53)

2. pick a map with enough destinations
	- including the predicate that decides "enough destinations"

[The function that picks the map](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L57-L69)

[Predicate that decides "enough destinations"](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Other/admin_utils.py#L11-L18)

3. allocating players to a bunch of games per round

[Manager allocates players in run_round function](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L108-L109)

[This function splits the players](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L114-L126)

4. run the tournament and its two major pieces of functionality:
   - run a  round of games

[Manager runs a round](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L100-L112)

  - run all rounds, discover termination conditions

[Manager runs all rounds](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L71-L91)

[Termination conditions](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L128-L138)

5. inform survining players at the very end whether they won the tournament

[Manager ends the tournament](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Admin/manager.py#L140-L151)

Next point to unit tests for:

- testing the `manager` on the same inputs as the `referee`, because
  you know the outcome
  
  We do not have a test for the `referee` and `manager` that share the same input. However, because we mock the `referee`
  in our `manager` tests we are still able to confirm that the communication between the `manager` and the `referee`
  occurs correctly.
  
  [Test for running the tournament](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Other/tests/test_manager.py#L8-L31)

- testing the allocation of players to the games of one round

We do not have unit tests for allocating the players.

Finally, the specification of the `cheat` strategy says "like BuyNow",
which suggests (F II) to derive (`extend`) the base class or re-use some
functionality:

- point to the cheat strategy and how it partially reusess existing code

[Cheat strategy](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Player/cheat.py#L10-L20)

[The cheat strategy inherits from BuyNow strategy](https://github.ccs.neu.edu/CS4500-F21/great-falls/blob/3b8ba5f3257f5f9614d28c2e89babc4c6966400b/Trains/Player/cheat.py#L10)

- point to a unit test that makes sure the requested acquisition is impossible

We do not have a unit test for cheat strategy. We hard-coded the connection the strategy attempts to acquire, because
we were not sure how to dynamically create an illegal connection, so technically a map could be constructed that does contain the hard-coded connection. 
However, we think this is okay because the city names that we used are incredibly unlikely to appear in a real map, and 
because the strategy is only used in a small subset of tests.

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.
