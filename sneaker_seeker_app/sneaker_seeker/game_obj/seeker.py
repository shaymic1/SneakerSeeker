from __future__ import annotations
from enum import StrEnum, auto

from sneaker_seeker.common_types.physical_specs import PhysicalSpecs
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.vec2d import Vec2D


class Seeker(Player):
    class State(StrEnum):
        SEEK = auto()
        CATCH = auto()

    def __init__(self, physical_specs: PhysicalSpecs, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D(),
                 los: float = 100, fov: float = 180, catch_dist: float = 50,
                 observation_direction: float = None) -> None:
        super().__init__(physical_specs=physical_specs, location=location, speed=speed, los=los, fov=fov,
                         observation_direction=observation_direction)
        self.catch_dist = catch_dist
        self.state = Seeker.State.SEEK

    @classmethod
    def from_dict(cls, physical_specs: dict, location: dict = None, speed: dict = None,
                  los: float = 100, fov: float = 180, catch_dist: float = 50,
                  observation_direction: float = None) -> Seeker:
        loc = Vec2D(**location) if location else Vec2D()
        spd = Vec2D.from_polar(**speed) if speed else Vec2D()
        specs = PhysicalSpecs(**physical_specs)
        obser_dir = observation_direction if observation_direction else spd.angle
        return cls(physical_specs=specs, location=loc, speed=spd, los=los, fov=fov, catch_dist=catch_dist,
                   observation_direction=obser_dir)

    def can_see(self, location: Vec2D) -> bool:
        if self.location.distance_to(location) > self.los:
            return False
        lower_bound_ang = self.observation_direction - self.fov / 2
        upper_bound_ang = self.observation_direction + self.fov / 2
        return lower_bound_ang <= self.location.relative_angle(location) <= upper_bound_ang
