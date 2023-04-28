import math

import numpy as np

from sneaker_seeker.common_types.vec2d import Vec2D
import matplotlib
from matplotlib.patches import Circle
from .movable import Movable


class DKIZ(Movable):
    """this is the Dynamic Keep-in Zone of the sneakers"""

    def __init__(self, shape: dict, location: dict = None, speed: dict = None, **args: dict) -> None:
        super().__init__(location, speed)
        self.type: str = shape["type"]
        self.dimensions: dict = shape[self.type]
        self.max_dist_from_center = max(self.dimensions.values())

    def contains(self, other_location: Vec2D):
        if self.type == 'circle':
            return self.location.distance_to(other_location) < self.dimensions['radius']

    def generate_points_inside(self, num_of_points: int, min_dist_between: float) -> list[Vec2D]:
        chosen_points = []
        for _ in range(num_of_points):
            p = Vec2D()
            while True:
                theta = np.random.uniform(0, 2 * np.pi)
                rho = np.random.uniform(0, self.max_dist_from_center)
                dx_from_center = rho * math.cos(theta)
                dy_from_center = rho * math.sin(theta)
                p = Vec2D(dx_from_center, dy_from_center) + self.location
                if self.contains(p) and not self.is_close_to_any_point(p, chosen_points, min_dist_between):
                    chosen_points.append(p)
                    break
        return chosen_points

    @staticmethod
    def is_close_to_any_point(candidate_point: Vec2D, chosen_points: list[Vec2D], min_dist: float) -> bool:
        if len(chosen_points) == 0:
            return False
        return any([candidate_point.distance_to(chosen_p) < min_dist for chosen_p in chosen_points])
