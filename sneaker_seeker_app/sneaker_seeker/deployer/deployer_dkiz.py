from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.game_obj.dkiz import DKIZ


class DeployerDKIZ(Deployer):
    def __init__(self, dkiz: DKIZ, **_ignore) -> None:
        self.dkiz: DKIZ = dkiz

    def deploy(self, players: list[Player]) -> None:
        min_dist = players[0].physical_specs.min_dist_between_eachother
        initial_points = self.dkiz.generate_points_inside(num_of_points=len(players), min_dist_between=min_dist)
        for player, point in zip(players, initial_points):
            player.location = point
