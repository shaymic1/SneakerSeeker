import math
from abc import ABC, abstractmethod

import numpy as np

from sneaker_seeker.common_types import Speed
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.game_obj.roi import Roi


class PathPlanner(ABC):
    @abstractmethod
    def set_path(self, player: Player):
        pass


class StraightLinePathPlanner(PathPlanner):
    def __init__(self, roi: Roi, **_ignore) -> None:
        self.roi = roi
        self.tracked_players = {}

    def set_path(self, player: Player) -> None:
        if player.id not in self.tracked_players.keys():
            self.tracked_players[player.id] = player.id
            if player.speed.vx == player.speed.vy == 0:
                vx = math.sqrt(player.physical_specs.cruise_speed)
                vy = math.sqrt(player.physical_specs.cruise_speed)
                player.speed = Speed(vx, vy)
                player.direction = math.degrees(math.atan(vy/vy))
                print(player.direction)

class RandomPathPlanner(PathPlanner):
    def __init__(self, roi: Roi, **_ignore) -> None:
        self.roi = roi

    def set_path(self, player: Player):
        player.speed.vx = np.random.uniform(low=0, high=player.physical_specs.cruise_speed)
        player.speed.vy = player.physical_specs.cruise_speed - player.speed.vx


class PathPlannerFactory:
    @staticmethod
    def create_path_planner(planner_type: str, **kwargs) -> PathPlanner:
        if planner_type == 'straight_line':
            return StraightLinePathPlanner(**kwargs)
        elif planner_type == 'random_walk':
            return RandomPathPlanner(**kwargs)
        else:
            raise ValueError(f'Invalid planner_type: {planner_type}')

