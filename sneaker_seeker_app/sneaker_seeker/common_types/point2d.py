from dataclasses import dataclass
from scipy.spatial.distance import euclidean

from sneaker_seeker.utilities import utils


@dataclass
class Point2D:
    x: float = 0
    y: float = 0

    def __add__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: 'Point2D') -> 'Point2D':
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other: 'Point2D') -> 'Point2D':
        self.x -= other.x
        self.y -= other.y
        return self

    def dist(self, other: 'Point2D') -> float:
        return euclidean((self.x, self.y), (other.x, other.y))

    def relative_angle(self, other: 'Point2D') -> float:
        return utils.calc_angle(y=(other.y - self.y), x=(other.x - self.x))
