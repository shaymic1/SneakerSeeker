from enum import Enum, auto

import matplotlib

from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types import Speed


class Sneaker(Player):
    class State(Enum):
        UNDETECTED = auto()
        DETECTED = auto()
        DESTROYED = auto()

    def __init__(self, location: dict, physical_specs: dict, direction: float = None,
                 los: float = 100, fov: float = 180, speed: Speed = None) -> None:
        super().__init__(location, physical_specs, direction, los, fov, speed)
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
