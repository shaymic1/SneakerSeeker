from enum import Enum, auto

import matplotlib

from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types import SpeedVec


class Sneaker(Player):
    class State(Enum):
        UNDETECTED = auto()
        DETECTED = auto()
        DESTROYED = auto()

    def __init__(self, physical_specs: dict, location: dict = None, observation_direction: float = None,
                 los: float = 100, fov: float = 180, speed: SpeedVec = None) -> None:
        super().__init__(physical_specs, location, observation_direction, los, fov, speed)
        self.state = Sneaker.State.UNDETECTED

    def detect(self):
        self.state = Sneaker.State.DETECTED

    def destroy(self):
        self.state = Sneaker.State.DESTROYED

    def is_undetected(self):
        return self.state == Sneaker.State.UNDETECTED

    def is_detected(self):
        return self.state == Sneaker.State.DETECTED

    def is_destroyed(self):
        return self.state == Sneaker.State.DESTROYED
