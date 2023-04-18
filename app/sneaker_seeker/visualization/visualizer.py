from abc import ABC, abstractmethod
from pathlib import Path

from sneaker_seeker.game_obj import Seeker, Sneaker, ROI, DKIZ


class Visualizer(ABC):
    @abstractmethod
    def save(self, path: Path):
        pass

    def clean(self):
        pass

    def make_ROI(self, roi: ROI):
        pass

    def make_DKIZ(self, dkiz: DKIZ):
        pass

    def make_seeker(self, seeker: Seeker):
        pass

    def make_sneaker(self, sneaker: Sneaker):
        pass

    def time_stamp(self, curr_time):
        pass
