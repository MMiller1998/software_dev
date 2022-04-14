- The `test_scores` function in the `trains.game.rank` module was not taking into account the longest path bonus. There was no unit test for this prior to the fix, so we've linked the newly written unit test after fixing.
  - Failing unit test prior to fix: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/blob/7911321062469b36bc71a8faccc61346d4983ad1/Other/tests/test_rank.py#L75-L100
  - Fix: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/commit/7911321062469b36bc71a8faccc61346d4983ad1

- The visualization was not displaying city names.
  - Failing test: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/blob/master/4/Vis/1.json
  - Fix: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/commit/bd410429222dbbe37a50604ea8bc0e587d9c9b3a
  - The problem had to do with the visualization library being designed for Tcl/Tk 8.6, while the Khoury system version of Tcl/Tk is 8.5. The library passes an option to `create_text` which is not recognized by Tcl/Tk 8.5, and therefore the text would not be drawn. My fix removes that code from the library, and adds the raw library module to our codebase rather than fetching it from PIP. For the actual changed code, the `angle` parameter is removed on lines 5437 and 5465.

- The visualization was not displaying multiple connections between two cities.
  - Failing test: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/blob/master/4/Vis/1.json
  - Fix: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/commit/bd410429222dbbe37a50604ea8bc0e587d9c9b3a

- A previous reworking of our state representation had left the xlegal method broken, xlegal has been modified to work with the new code structure
  - Failing test: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/blob/master/5/Tests/1-in.json
  - Fix: https://github.ccs.neu.edu/CS4500-F21/hammond-pond/commit/37bbb0c1680a9e60bef89a06ec8a03846afa1734
