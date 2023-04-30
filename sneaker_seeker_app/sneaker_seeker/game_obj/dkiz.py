from __future__ import annotations
import math
import numpy as np
from typing import Tuple, Optional

from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.common_types.point import Point
from .movable import Movable


class DKIZ(Movable):
    """this is the Dynamic Keep-in Zone of the sneakers"""

    def __init__(self, type: str, dimensions: dict, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D(),
                 uncertainty_radius: float = None) -> None:
        super().__init__(location, speed)
        self.type: str = type
        self.dimensions: dict = dimensions
        self.max_dist_from_center = max(self.dimensions.values())
        self.uncertainty_radius = uncertainty_radius if uncertainty_radius else self.max_dist_from_center
        self.l_frontal_line, self.r_frontal_line = self.__frontal_line_section()

    @classmethod
    def from_dict(cls, shape: dict, location: dict = None, speed: dict = None,
                  uncertainty_radius: float = None) -> DKIZ:
        loc = Vec2D(**location) if location else Vec2D()
        spd = Vec2D.from_polar(**speed) if speed else Vec2D()
        return cls(type=shape["type"], dimensions=shape[shape["type"]], location=loc, speed=spd,
                   uncertainty_radius=uncertainty_radius)

    def move(self, dt: float):
        super().move(dt)
        self.l_frontal_line.move(dt)
        self.r_frontal_line.move(dt)

    def contains(self, other_location: Vec2D):
        if self.type == 'circle':
            return self.location.distance_to(other_location) < self.dimensions['radius']

    def generate_points_inside(self, num_of_points: int, min_dist_between: float) -> list[Vec2D]:
        chosen_points = []
        for _ in range(num_of_points):
            while True:
                theta = np.random.uniform(0, 2 * np.pi)
                rho = np.random.uniform(0, self.max_dist_from_center)
                dx_from_center = rho * math.cos(theta)
                dy_from_center = rho * math.sin(theta)
                candidate_p = Vec2D(dx_from_center, dy_from_center) + self.location
                if self.contains(candidate_p) and not self.is_close_to_any_other_point(candidate_p, chosen_points,
                                                                                       min_dist_between):
                    chosen_points.append(candidate_p)
                    break
        return chosen_points

    @staticmethod
    def is_close_to_any_other_point(candidate_point: Vec2D, chosen_points: list[Vec2D], min_dist: float) -> bool:
        if len(chosen_points) == 0:
            return False
        return any([candidate_point.distance_to(chosen_p) < min_dist for chosen_p in chosen_points])

    def __frontal_line_section(self) -> Tuple[Optional[Point], Optional[Point]]:
        """return (left_point, right_point) of the frontal line of advancing DKIZ from DKIZ point of view."""
        if self.speed.magnitude == 0:
            return Point(location=self.location, speed=self.speed), Point(location=self.location, speed=self.speed)
        front_right_loc = self.location + Vec2D.from_polar(magnitude=math.sqrt(2) * self.uncertainty_radius,
                                                           angle=self.speed.angle - 45)
        front_left_loc = self.location + Vec2D.from_polar(magnitude=math.sqrt(2) * self.uncertainty_radius,
                                                          angle=self.speed.angle + 45)
        return Point(location=front_left_loc, speed=self.speed), Point(location=front_right_loc, speed=self.speed)
