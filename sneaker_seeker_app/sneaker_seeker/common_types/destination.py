from dataclasses import dataclass
from sneaker_seeker.common_types.vec2d import Vec2D


@dataclass
class Destination:
    location: Vec2D
    arrival_time: float
    arrived: bool = False
