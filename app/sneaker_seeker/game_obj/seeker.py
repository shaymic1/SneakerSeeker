import matplotlib

from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types import Speed

class Seeker(Player):

    def __init__(self, location: dict, physical_specs: dict, direction: float = None,
                 los: float = 1000, fov: float = 60, speed: Speed = None) -> None:
        super().__init__(location, physical_specs, direction, los, fov, speed)
