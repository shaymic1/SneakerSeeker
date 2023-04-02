from abc import ABC, abstractmethod
from pathlib import Path

from sneaker_seeker.game_obj.roi import Roi
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.seeker import Seeker


class Visualizer(ABC):
    @abstractmethod
    def save(self, path: Path):
        pass

    def clean(self):
        pass

    def make_roi(self, roi: Roi):
        pass

    def make_seeker(self, seeker: Seeker):
        pass

    def make_sneaker(self, sneaker: Sneaker):
        pass
