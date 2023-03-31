import matplotlib

from sneaker_seeker.game_obj.player import Player


class Sneaker(Player):

    def __init__(self, location: dict, speed: dict, direction: float = None,
                 los: float = 100, fov: float = 180) -> None:
        super().__init__(location, speed, direction, los, fov)
        self.detected = False
        self.id = None


