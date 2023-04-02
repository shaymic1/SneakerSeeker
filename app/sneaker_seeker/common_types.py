from dataclasses import dataclass


@dataclass
class Location:
    x: int = 0
    y: int = 0


@dataclass
class Speed:
    curr_speed: float = 50
    cruise: float = 55
    max: float = 100
    max_time: float = 20
