import random
from abc import ABC

from sneaker_seeker.common_types import Location, PhysicalSpecs, SpeedVec


class Player(ABC):
    last_id = 0

    def __init__(self, physical_specs: dict, location: dict = None, observation_direction: float = None,
                 los: float = 1000, fov: float = 60, speed: dict = None) -> None:
        Player.last_id += 1
        self.id = Player.last_id
        self.physical_specs: PhysicalSpecs = PhysicalSpecs(**physical_specs)
        self.location: Location = Location(**location) if location else Location()
        self.speed: SpeedVec = SpeedVec(**speed) if speed else SpeedVec()
        self.observation_direction: float = observation_direction if observation_direction else self.speed.direction
        self.los: float = los
        self.fov: float = fov

    def move(self, dt: float):
        self.location.x += self.speed.vx * dt
        self.location.y += self.speed.vy * dt
