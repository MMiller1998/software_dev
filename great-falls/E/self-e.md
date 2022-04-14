## Self-Evaluation Form for TAHBPL/E

A fundamental guideline of Fundamentals I and II is "one task, one
function" or, more generally, separate distinct tasks into distinct
program units.

This assignment comes with three distinct, unrelated tasks.

Indicate below each bullet which file/unit takes care of each task:


1. dealing with command-line arguments

[main.py, the get_port function](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/3073b1852d16593967271a2e9b97217f0512e39e/E/Other/main.py#L19-L25)


2. connecting the client on the specified port to the functionality

[main.py, inside the main function](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/3073b1852d16593967271a2e9b97217f0512e39e/E/Other/main.py#L15-L16)
We instantiate MyTCPServer with the port from get_port which handles the json by delegating to TCPJsonReverser


3. core functionality (either copied or imported from `C`)

[tcp_json_reverser.py, calls out to c.py to reverse input](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/3073b1852d16593967271a2e9b97217f0512e39e/E/Other/tcp_json_reverser.py#L18-L27)

[c.py, handles all the json reversing](https://github.ccs.neu.edu/CS4500-F21/badlands/blob/3073b1852d16593967271a2e9b97217f0512e39e/E/Other/c.py)

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request. If you did *not* factor
out these pieces of functionality into separate functions/methods, say
so.
