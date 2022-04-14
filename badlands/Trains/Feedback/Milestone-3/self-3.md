## Self-Evaluation Form for Milestone 3

Indicate below each bullet which file/unit takes care of each task:

1. explain how your main visualization method/function 

   - manages the timed tear down of the visualization window 
     - The visualization window does not time out as timing out was not asked for in the spec. Tear down occurs when the window is closed.
   - calls out to the drawing the graph itself 
     - We have a public function called `display_map` that uses Tk to make a canvas on which we draw the cities and connections. Then that canvas is rendered in a window. [The display_map function](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/11983c8ae83f2fb1383b3843b0c30227c59d71b7/Trains/Editor/map_editor.py#L14-L25)


2. point to the functionality for adding cities to the visualized map
  - https://github.ccs.neu.edu/CS4500-F21/badlands/blob/11983c8ae83f2fb1383b3843b0c30227c59d71b7/Trains/Editor/map_editor.py#L28-L34

3. point to the functionality for adding connections to the visualized map
  - https://github.ccs.neu.edu/CS4500-F21/badlands/blob/11983c8ae83f2fb1383b3843b0c30227c59d71b7/Trains/Editor/map_editor.py#L52-L58

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

