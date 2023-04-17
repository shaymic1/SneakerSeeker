import math
from math import sin, cos
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


@dataclass
class PhysicalSpecs:
    cruise_speed: float = 55
    max_speed: float = 100
    max_speed_time: float = 0


@dataclass
class SpeedVec:
    _magnitude: float = 0
    _direction: float = 0
    _vx: float = 0
    _vy: float = 0

    def __post_init__(self):
        self._vx = self._magnitude * cos(math.radians(self.direction))
        self._vy = self._magnitude * sin(math.radians(self.direction))

    def __eq__(self, other: 'SpeedVec') -> bool:
        return self._magnitude == other._magnitude and self.direction == other.direction

    def __repr__(self):
        return f"SpeedVec(_magnitude={self._magnitude}, direction={self.direction})"

    @property
    def magnitude(self):
        return self._magnitude

    @magnitude.setter
    def magnitude(self, value):
        if value < 0:
            raise ValueError("Magnitude cannot be negative")
        self._vx *= (value / self.magnitude)
        self._vy *= (value / self.magnitude)
        self._magnitude = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        self._vx, self._vy = self.magnitude * cos(math.radians(value)), self.magnitude * sin(math.radians(value))

    @property
    def vx(self):
        return self._vx

    @property
    def vy(self):
        return self._vy



