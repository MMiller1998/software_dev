from typing import Tuple, Union

from trains.game.player import PlayerActor
from trains.game.types import Rank


TournamentResult = Tuple[Rank[PlayerActor], Rank[PlayerActor]]
# A TournamentResult is a tuple containing a Rank of winners and a Rank
# of cheaters.
