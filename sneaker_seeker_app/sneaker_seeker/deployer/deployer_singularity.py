from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.player import Player


class DeployerSingularity(Deployer):
    def __init__(self, location: dict, **_ignore) -> None:
        self.location: Vec2D = Vec2D(**location)

    def deploy(self, players: list[Player]) -> None:
        for player in players:
            player.location = self.location
