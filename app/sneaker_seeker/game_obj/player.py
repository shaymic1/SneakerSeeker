import math
from abc import ABC
from sneaker_seeker.common_types import Location, PhysicalSpecs, Speed
import numpy as np


class Player(ABC):
    last_id = 0

    def __init__(self, location: dict, physical_specs: dict, direction: float = None,
                 los: float = 1000, fov: float = 60, speed: dict = None) -> None:
        Player.last_id += 1
        self.id = Player.last_id
        self.physical_specs: PhysicalSpecs = PhysicalSpecs(**physical_specs)
        self.location: Location = Location(**location)
        self.speed: Speed = Speed(**speed) if speed else Speed()
        self.direction: float = direction if direction else math.degrees(math.atan(self.speed.vy/self.speed.vy))
        self.los: float = los
        self.fov: float = fov

