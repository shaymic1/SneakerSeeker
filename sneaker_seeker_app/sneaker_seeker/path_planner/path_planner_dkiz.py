from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.dkiz import DKIZ


class PathPlannerDKIZ(PathPlanner):
    def __init__(self, dkiz: DKIZ, **_ignore) -> None:
        self.dkiz: DKIZ = dkiz
        self.tracked_players = {}

    def set_path(self, players: list[Player], time: float, has_detection: bool) -> None:
        # set the player's speed only once using tracked_players dict.
        for player in players:
            if player.id not in self.tracked_players.keys():
                self.tracked_players[player.id] = player.id
                player.speed = self.dkiz.speed
                player.observation_direction = self.dkiz.speed.angle
