# Thoughts on _Milestone 2_

This document describes considerations we made regarding our data
representation `TrainMap` and the implementation of its method,
`TrainMap.get_destinations()`.

## Abstract

A `TrainMap` is a
[disjoint union of graphs](https://en.wikipedia.org/wiki/Disjoint_union_of_graphs).

UIDs are used to identify _places_ and _connections_. The solution is flexible,
allowing for two different _places_ to have the same name. `TrainMap` is
well-indexed, meaning data accession is relatively efficient. Most of its
getter methods return structs, hence it interface facilitates object-oriented
programming.

_Destinations_ of a `TrainMap` can be found by computing the Cartesian product
of all _components_, excluding _(n, n)_ pairs.

## Background

During our code walk on 2021-10-14, our implementation of `TrainMap` and
`get_destinations` was absolutely trashed on. Since then we've refactored
`get_destinations` into several recursive functions.

To understand the program you should:

- Have passed and paid attention in CS 3200 ---Algorithms
- Understand features of the Python language, specifically `yield`

There are different schools of thought regarding "readability." If you would
like to see our old, iterative, _"Pythonic"_ implementation, check it out from
commit adf200f99768a482db28d89d6ea1ef332c080ce9

```shell
git checkout adf200f99768a482db28d89d6ea1ef332c080ce9 Other/trains/map.py
```

WARNING: since we renamed everything in
59f32bbe4178ebef72b36808986743cbe6383322,
the old code no longer works as-is.

See also: https://course.ccs.neu.edu/cs2510/lecture30.html

## TrainMap

A `TrainMap` is a representation of the board in the game _Trains_.

### Data Representation

`TrainMap` does not retain information about the game's state (e.g.
whose turn it is) nor any information relevant to visualization (e.g.
the x, y location of places). Think of `TrainMap` as a base, and that
other information as supplemental. Programs which make use of `TrainMap`
should maintain a data structure which relate the elements of `TrainMap`
to whatever specialized functionality (game state or visualization). Such
a design achieves _separation of concerns_.

### Data Structure

`TrainMap` is a graph where nodes are `TrainPlace` and edges are
`TrainConnection`. These two structs, `TrainPlace` and
`TrainConnection`, are doubly-linked, and have unique identifiers
(UID) which relate them to the `TrainMap` they exist on. Our design
facilitates an object-oriented approach to interacting with `TrainMap`.
Getter methods of `TrainMap` usually return objects (`TrainPlace`
and `TrainConnection`): their fields are references to graph
relationships which make graph traversal easy. Our implementation of a
graph using UIDs, ordered list data structures, and doubly-linked structs,
make our graph "well-indexed," that is, accessing information about a
node or edge is efficient (linear, log, or constant time operations).

## `get_destinations`

For a [connected](https://en.wikipedia.org/wiki/Connectivity_%28graph_theory%29),
undirected graph, there exists a
[path](https://en.wikipedia.org/wiki/Path_(graph_theory))
from every node to every other node. Thus, the "destinations" would
simply be the cartesian product of the list of nodes, without the
self _(n, n)_ pairs.

It is possible for the `TrainMap` to be a disconnected graph, that is,
in the game of _Trains_ it is allowed to have two places which are not
connected by a path. (Though, this is not typical for a game of
_Ticket to Ride_.)

### Time Complexity

For a graph _G\[V, E\]_:

Best case is where there are no edges. Identifying all nodes as
individual sub-graphs takes _O(V)_

Worst case is where there is only one graph. The cost is that of BFS,
which is _O(V + E)_

The Cartesian product takes _O(V(V-1)/2)_ per sub-graph to compute.

Overall asymptotic runtime is less than _O(V^2)_.

#### Sets, Everywhere

[set](https://docs.python.org/3.6/library/stdtypes.html#set)
data structure is used for efficient add member and membership check operations.

### `__set_peek(s: Set) -> Any`

This basic functionality is missing from Python's standard library and we
implement it here for the sake of being able to use sets as accumulators
in recursive functions without mutating the accumulator.

An iterative approach of the same algorithm would probably use ``s.pop()``.
It would also be more memory-efficient.
