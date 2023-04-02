from abc import ABC
from sneaker_seeker.common_types import Location, Speed
import numpy as np


class Player(ABC):
    def __init__(self, location: dict, speed: dict, direction: float = None,
                 los: float = 1000, fov: float = 60) -> None:
        self.location: Location = Location(**location)
        self.speed: Speed = Speed(**speed)
        self.direction: float = direction if direction else np.random.uniform(low=-np.pi, high=np.pi)
        self.los: float = los
        self.fov: float = fov

