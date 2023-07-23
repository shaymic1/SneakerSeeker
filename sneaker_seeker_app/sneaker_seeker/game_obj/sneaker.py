from __future__ import annotations
from enum import StrEnum, auto

from sneaker_seeker.common_types.physical_specs import PhysicalSpecs
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.vec2d import Vec2D


class Sneaker(Player):
    class State(StrEnum):
        UNDETECTED = auto()
        DETECTED = auto()
        TARGETED = auto()

    def __init__(self, physical_specs: PhysicalSpecs, group_num: int, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D(),
                 los: float = 100, fov: float = 180, observation_direction: float = None) -> None:
        super().__init__(physical_specs=physical_specs, group_num=group_num, location=location, speed=speed, los=los,
                         fov=fov, observation_direction=observation_direction)
        self.state = Sneaker.State.UNDETECTED
        self.detected_by_seekers_group_numbers: list[int] = []

    @classmethod
    def from_dict(cls, physical_specs: dict, group_num: int, location: dict = None, speed: dict = None,
                  los: float = 100, fov: float = 180, observation_direction: float = None) -> Sneaker:
        loc = Vec2D(**location) if location else Vec2D()
        spd = Vec2D.from_polar(**speed) if speed else Vec2D()
        specs = PhysicalSpecs(**physical_specs)
        obser_dir = observation_direction if observation_direction else spd.angle
        return cls(physical_specs=specs, group_num=group_num, location=loc, speed=spd, los=los, fov=fov,
                   observation_direction=obser_dir)
