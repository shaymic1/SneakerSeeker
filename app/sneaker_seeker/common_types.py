from dataclasses import dataclass


@dataclass
class Location:
    x: int = 0
    y: int = 0


@dataclass
class Speed:
    cruse: float
    max: float
    max_time: float
