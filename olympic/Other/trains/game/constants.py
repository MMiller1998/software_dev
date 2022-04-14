from trains.game.types import ScorePoint

POINTS_PER_ACQUIRED_SEGMENT = ScorePoint(1)

POINTS_FOR_CONNECTED_DESTINATION = ScorePoint(10)
POINTS_FOR_DISCONNECTED_DESTINATION = ScorePoint(-10)

POINTS_FOR_LONGEST_PATH = ScorePoint(20)


MIN_PLAYERS_IN_GAME = 2
MAX_PLAYERS_IN_GAME = 8

STARTING_DESTINATION_OFFER_COUNT = 5
"""
Number of destinations offered to a player at the beginning of the game.
"""

STARTING_DESTINATION_TAKE_COUNT = 2
"""
Number of destinations a player can pick at the start of the game.
"""

STARTING_DESTINATION_RETURN_COUNT = STARTING_DESTINATION_OFFER_COUNT - STARTING_DESTINATION_TAKE_COUNT
"""
Number of destinations to not take and return to the referee.
"""

STARTING_CARD_COUNT = 4
"""
The number of *colored cards* the *referee* should offer to a *player*
while setting up a game.
"""

TOTAL_CARD_DECK_SIZE = 250

STARTING_RAIL_COUNT = 45

SECONDS_TO_TAKE_ACTION = 5
"""
Number of seconds a *player* has to make a decision on its turn.
"""
