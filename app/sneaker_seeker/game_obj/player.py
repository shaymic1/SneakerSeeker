from abc import ABC
from sneaker_seeker.common_types import Location, Speed
from sneaker_seeker.simulation.drawable import Drawable
import numpy as np


class Player(Drawable, ABC):
    def __init__(self, location: dict, speed: dict, direction: float = None,
                 los: float = 1000, fov: float = 60) -> None:
        self.location: Location = Location(**location)
        self.speed: Speed = Speed(**speed)
        self.direction: float = direction if direction else np.random.uniform(low=-np.pi, high=np.pi)
        self.los: float = los
        self.fov: float = fov
