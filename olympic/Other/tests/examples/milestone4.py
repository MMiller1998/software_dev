from typing import Tuple
import tests.examples.milestone2 as example
from trains.state.player import PlayerState, PlayerStateWrapper
from trains.state.referee import RefereeState
from trains.graph_elements import RailColor


def create_example() -> Tuple[RefereeState, PlayerState, PlayerState, PlayerState, PlayerStateWrapper]:
    player1 = PlayerState(frozenset([
        example.dest_bwi1_lax,
        example.dest_mrtl_iad
    ]))
    player2 = PlayerState(frozenset([
        example.dest_bwi1_bos,
        example.dest_bwi2_bos
    ]))
    player3 = PlayerState(frozenset([
        example.dest_bwi1_bwi2,
        example.dest_lax_bos
    ]))
    player2_state_wrapper = PlayerStateWrapper(player2, [[], []])
    cards = [
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
        RailColor.RED, RailColor.BLUE, RailColor.GREEN, RailColor.WHITE,
    ]
    referee = RefereeState(train_map=example.train_map,
                           players=(player1, player2, player3),
                           cheaters=frozenset(),
                           cards=cards,
                           turns_without_state_change=0)
    return referee, player1, player2, player3, player2_state_wrapper
