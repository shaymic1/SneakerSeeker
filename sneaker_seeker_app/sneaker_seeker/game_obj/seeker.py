from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.point2d import Point2D
from sneaker_seeker.common_types.vec2d import Vec2D


class Seeker(Player):

    def __init__(self, physical_specs: dict, location: dict = None, observation_direction: float = None,
                 los: float = 1000, fov: float = 60, speed: Vec2D = None) -> None:
        super().__init__(physical_specs, location, observation_direction, los, fov, speed)

    def can_see(self, location: Point2D) -> bool:
        if self.location.dist(location) > self.los:
            return False

        lower_bound_ang = self.observation_direction - self.fov / 2
        upper_bound_ang = self.observation_direction + self.fov / 2
        return lower_bound_ang <= self.location.relative_angle(location) <= upper_bound_ang

