from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.game_obj.player import Player

import numpy as np


class PathPlannerRandomWalk(PathPlanner):
    def __init__(self, **_ignore) -> None:
        pass

    def set_path(self, players: list[Player]):
        for player in players:
            player.speed.magnitude = np.random.uniform(low=0, high=player.physical_specs.cruise_speed)
            player.speed.angle = np.random.uniform(low=0, high=np.pi * 2)
