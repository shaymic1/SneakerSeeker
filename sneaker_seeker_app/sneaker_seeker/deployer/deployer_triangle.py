from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.player import Player


class DeployerTriangle(Deployer):
    def __init__(self, location: dict, location2: dict, mid: dict, **_ignore) -> None:
        self.location: Vec2D = Vec2D(**location)
        self.location2: Vec2D = Vec2D(**location2)
        self.mid: Vec2D = Vec2D(**mid)

    def deploy(self, players: list[Player]) -> None:
        players_num = len(players)
        if players_num.__mod__(2) == 0:
            self.__deploy_even(players, players_num)
        self.__deploy_odd(players, players_num)

    def __deploy_odd(self, players: list[Player], players_num: int):
        line1_points = self.location2.points_between(self.mid, (players_num // 2) + 1)
        line2_points_without_vertex = self.mid.points_between(self.location, (players_num // 2) + 1)[1:]
        for loc, player in zip(line1_points + line2_points_without_vertex, players):
            player.location = loc

    def __deploy_even(self, players, players_num):
        raise Exception("not implemented")

