from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.player import Player


class DeployerLine(Deployer):
    def __init__(self, location: dict, location2: dict, **_ignore) -> None:
        self.location: Vec2D = Vec2D(**location)
        self.location2: Vec2D = Vec2D(**location2)

    def deploy(self, players: list[Player]) -> None:
        for loc, player in zip(self.location2.points_between(self.location, len(players)), players):
            player.location = loc
