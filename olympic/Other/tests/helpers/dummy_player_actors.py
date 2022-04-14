from trains.game.player import PlayerActor


class StartRaisePlayerActor(PlayerActor):
    def __init__(self):
        pass

    def start(self, participating: bool):
        raise Exception('raised from StartRaisePlayerActor.start')
