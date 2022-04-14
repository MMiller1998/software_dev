## Self-Evaluation Form for Milestone 5

Indicate below each bullet which file/unit takes care of each task:

1. the general interface/type/signatures for strategies
  - Since Python uses duck typing it does not have interfaces, so we assume all strategies will implement the `select_destinations` and `get_turn` methods
    - the [select_destinations method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Player/strategy.py#L15) 
    - the [get_turn method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Player/strategy.py#L26) 


2. the common container/abstract class (see Fundamentals II)  for the buy algorithm; in an FP approach, the common algoritnm
  - We do not have a common container or abstract class



3. the method/function for setting-up decisions, plus unit tests 
  - BuyNow:
    - the [select_destinations method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Player/strategy.py#L15)
    - [unit test](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/tests/test_buy_now_strategy.py#L25)
  - HoldTen:
    - the [select_destinations method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Player/strategy.py#L50)
    - [unit test](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/tests/test_hold_ten_strategy.py#L25) 



4. the method/function for take-turn decisions, plus unit tests 
  - BuyNow:
    - the [get_turn method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Player/strategy.py#L61)
    - [unit test](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/tests/test_buy_now_strategy.py#L29-L41)
  - HoldTen:
    - the [get_turn method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Player/strategy.py#L26)
    - [unit test](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/tests/test_hold_ten_strategy.py#L29-L49) 




5. the methods/functions for lexical-order comparisions of destinations, plus unit tests
  - [Comparison method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/city_pair.py#L41)
  - [unit tests](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/tests/test_city_pair.py#L37-L47)



6. the methods/functions for lexical-order comparisions of connections, plus unit tests 
  - [Comparison method](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/undirected_connection.py#L54)
  - [unit tests](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/6ff5c4cc2ae33187baf3f41a819661a698f8260f/Trains/Other/tests/test_undirected_connection.py#L50-L63)




The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.
