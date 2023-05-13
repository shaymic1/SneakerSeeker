from __future__ import annotations
from dataclasses import dataclass
from sneaker_seeker.common_types.vec2d import Vec2D


@dataclass
class Destination:
    location: Vec2D
    arrival_time: float
    arrived: bool = False

    def __hash__(self):
        return hash(self.location)

    def __eq__(self, other: Destination) -> bool:
        return self.location == other.location

