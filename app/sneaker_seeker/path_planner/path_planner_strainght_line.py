import random

from .path_planner import PathPlanner
from sneaker_seeker.game_obj.ROI import ROI
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.speed_vec import SpeedVec
from sneaker_seeker import utils


class PathPlannerStraightLine(PathPlanner):
    def __init__(self, roi: ROI, **_ignore) -> None:
        self.roi = roi
        self.tracked_players = {}

    def set_path(self, player: Player) -> None:
        # set the player's speed only once using tracked_players dict.
        if player.id not in self.tracked_players.keys():
            self.tracked_players[player.id] = player.id
            if player.speed.magnitude == 0:
                player.speed = SpeedVec(_magnitude=player.physical_specs.max_speed, _direction=random.uniform(0, 360))
                player.observation_direction = utils.calc_angle(y=player.speed.vy, x=player.speed.vx)
