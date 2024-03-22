from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.vec2d import Vec2D


class PathPlannerStraightLine(PathPlanner):
    def __init__(self, angle: float, **_ignore) -> None:
        self.angle: float = angle
        self.tracked_players = {}

    def set_path(self, players: list[Player], time: float, has_detection: bool) -> None:
        # set the player's speed only once using tracked_players dict.
        for player in players:
            if player.id not in self.tracked_players.keys():
                self.tracked_players[player.id] = player.id
                player.speed = Vec2D.from_polar(magnitude=player.physical_specs.max_speed, angle=self.angle)
                player.observation_direction = player.speed.angle
