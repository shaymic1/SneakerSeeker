from dataclasses import dataclass


@dataclass
class PhysicalSpecs:
    cruise_speed: float = 55
    max_speed: float = 100
    max_speed_time: float = 0
    min_dist_between_eachother: float = 100
    turn_radius: float = 0
