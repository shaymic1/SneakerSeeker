from abc import ABC
from sneaker_seeker.common_types import Location, Speed


class Player(ABC):
    def __init__(self, location: Location, speed: Speed) -> None:
        self.location: Location = location
        self.speed: Speed = speed
