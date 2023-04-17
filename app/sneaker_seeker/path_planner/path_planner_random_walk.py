from .path_planner import PathPlanner
from sneaker_seeker.game_obj import Roi, Player

import numpy as np


class PathPlannerRandomWalk(PathPlanner):
    def __init__(self, roi: Roi, **_ignore) -> None:
        self.roi = roi

    def set_path(self, player: Player):
        player.speed.vx = np.random.uniform(low=0, high=player.physical_specs.cruise_speed)
        player.speed.vy = player.physical_specs.cruise_speed - player.speed.vx
