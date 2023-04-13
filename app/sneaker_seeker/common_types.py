from dataclasses import dataclass


@dataclass
class Location:
    x: float = 0
    y: float = 0


@dataclass
class PhysicalSpecs:
    cruise_speed: float = 55
    max_speed: float = 100
    max_speed_time: float = 20


@dataclass
class Speed:
    vx: float = 1
    vy: float = 1
