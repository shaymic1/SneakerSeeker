from abc import ABC, abstractmethod
from sneaker_seeker.game_obj.player import Player


class Deployer(ABC):
    @abstractmethod
    def deploy(self, players: list[Player]):
        pass

