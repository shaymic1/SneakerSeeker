from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.location import Location
from sneaker_seeker.common_types.speed_vec import SpeedVec


class Seeker(Player):

    def __init__(self, physical_specs: dict, location: dict = None, observation_direction: float = None,
                 los: float = 1000, fov: float = 60, speed: SpeedVec = None) -> None:
        super().__init__(physical_specs, location, observation_direction, los, fov, speed)

    def can_see(self, loc: Location) -> bool:
        if self.location.dist(loc) > self.los:
            return False

        lower_bound_ang = self.observation_direction - self.fov / 2
        upper_bound_ang = self.observation_direction + self.fov / 2
        return lower_bound_ang <= self.location.relative_angle(loc) <= upper_bound_ang

