from trains.graph_elements import RailColor
from trains.state.referee import RefereeState


def give_player_cards(referee: RefereeState, color: RailColor, number_of_cards: int):
    player = referee.current_player
    cards = player.cards
    cards[color] += number_of_cards
    return referee.update_current_player(
        player.update(cards=cards)
    )


def change_rail_count(referee: RefereeState, num_rails: int):
    return referee.update_current_player(
        referee.current_player.update(num_rails=num_rails)
    )
