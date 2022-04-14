# Map Data Representation

draft
2021-09-30

### How to read this document

We are using Python(-ish) syntax. Data definitions are ultimately represented
with structures that are natively defined in the Python language. Syntax also
(somewhat) follows Python syntax. For example, a `Graph[V, E]` is a Python
representation of a
[graph](https://wikipedia.org/wiki/Graph_(abstract_data_type)?lang=en).
In this context, square brackets denote the generic types. This graph has
vertices of type `V` and edges of type `E`.

## `TrainMap`

A `TrainMap` is a `Graph[TrainPlace, TrainConnection]`

### `TrainPlace`

A `TrainPlace` is a struct which has:

- `TrainPlace.name`, a `str` representing the _place_'s name
- `TrainPlace.id`, a value which uniquely identifies the _place_ on the _map_

### `TrainConnection`

A `TrainConnection` is a struct which has:

- `TrainConnection.id`, a value which uniquely identifies this _connection_ on the _map_
- `TrainConnection.color`
- `TrainConnection.length`
- `TrainConnection.occupant`
- `TrainConnection.acquiree`

#### `TrainConnection.color`

A `TrainConnection.color` is an enum of the values:

- `RED`
- `BLUE`
- `GREEN`
- `WHITE`

#### `TrainConnection.length`

A `TrainConnection.length` is one of:

- `3`
- `4`
- `5`

#### `TrainConnection.occupant`, `TrainConnection.acquiree`

We are unable to design representations for these fields because the
[description](https://www.ccs.neu.edu/home/matthias/4500-f21/trains.html) is
vague.

Depending on how the co-CEOs clarify the description, we anticipate that
`TrainConnection.occupant` and `TrainConnection.acquiree` will be `Optional[Player]`
where `Player` is a struct which is not described in this document.

