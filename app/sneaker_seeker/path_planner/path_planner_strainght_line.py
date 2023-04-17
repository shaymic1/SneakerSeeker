from .path_planner import PathPlanner
from sneaker_seeker.game_obj import Roi, Player
from sneaker_seeker.common_types import Speed
from sneaker_seeker import utils
import math


class PathPlannerStraightLine(PathPlanner):
    def __init__(self, roi: Roi, **_ignore) -> None:
        self.roi = roi
        self.tracked_players = {}

    def set_path(self, player: Player) -> None:
        # set the player's speed only once using tracked_players dict.
        if player.id not in self.tracked_players.keys():
            self.tracked_players[player.id] = player.id
            if player.speed.vx == player.speed.vy == 0:
                vx = math.sqrt(player.physical_specs.cruise_speed)
                vy = math.sqrt(player.physical_specs.cruise_speed)
                player.speed = Speed(vx, vy)
                player.direction = utils.calc_angle(y=vy, x=vx)
