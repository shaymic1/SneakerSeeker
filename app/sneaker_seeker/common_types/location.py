from dataclasses import dataclass
from scipy.spatial.distance import euclidean

from sneaker_seeker import utils


@dataclass
class Location:
    x: float = 0
    y: float = 0

    def dist(self, other: 'Location') -> float:
        return euclidean((self.x, self.y), (other.x, other.y))

    def relative_angle(self, other: 'Location') -> float:
        return utils.calc_angle(y=(other.y - self.y), x=(other.x - self.x))

