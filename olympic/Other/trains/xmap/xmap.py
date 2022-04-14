from typing import TextIO
from trains.parsing import StatefulSpacedJSONParser
from trains.utils import build_visual_map


def xmap(infile: TextIO, outfile: TextIO) -> int:
    """
    Consumes a JSON *Map* from the given input stream and command-line arguments
    which mention two city names. Prints "true" or "false" to the given output
    stream depending on whether the two places specified form a *Destination*.

    If the number of command-line arguments after the executable's name is not 2,
    then the command-line usage help text is printed instead and the program exits.

    :param infile: input stream
    :param outfile: output stream
    :return: 0 if program was successful, 1 in case of any usage error
    """
    parser = StatefulSpacedJSONParser(infile.read())
    city1 = parser.read_string()
    city2 = parser.read_string()
    train_map = build_visual_map(parser.read_object())

    # convert structs which represent cities into just their names as str
    destinations = map(
        lambda s: {place.name for place in s},
        train_map.get_map().get_destinations()
    )

    # In class on 2020-10-13, a pair was criticized during their code walk that
    # computing all destinations to test whether one destination is inefficient.
    #
    # Remember, our solution to computing destinations is by finding the
    # Cartesian product of sub-graphs, not based on finding paths i.e. graph
    # traversal. If we care any more about efficiency, use PyPy.

    if {city1, city2} in destinations:
        outfile.write('true\n')
    else:
        outfile.write('false\n')
    return 0
