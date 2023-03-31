import matplotlib

from sneaker_seeker.game_obj.player import Player

class Seeker(Player):

    def __init__(self, location: dict, speed: dict, direction: float = None,
                 los: float = 1000, fov: float = 60) -> None:
        super().__init__(location, speed, direction, los, fov)
