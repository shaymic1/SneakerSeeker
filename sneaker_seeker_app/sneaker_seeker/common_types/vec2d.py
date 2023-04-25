import math
from typing import Tuple
from math import sin, cos
from dataclasses import dataclass


@dataclass
class Vec2D:
    _magnitude: float = 0
    _direction: float = 0
    _vx: float = 0
    _vy: float = 0

    def __post_init__(self):
        self._vx = self._magnitude * cos(math.radians(self.direction))
        self._vy = self._magnitude * sin(math.radians(self.direction))

    def __eq__(self, other: 'Vec2D') -> bool:
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
        self._vx = self.magnitude * cos(math.radians(value))
        self._vy = self.magnitude * sin(math.radians(value))

    @property
    def vx(self):
        return self._vx

    @property
    def vy(self):
        return self._vy

    def to_cartesian(self) -> Tuple[float, float]:
        return self._vx, self._vy

    def __sub__(self, other: 'Vec2D') -> 'Vec2D':
        vx = self._vx - other._vx
        vy = self._vy - other._vy
        magnitude = math.sqrt(vx ** 2 + vy ** 2)
        direction = math.degrees(math.atan2(vy, vx))
        return Vec2D(magnitude, direction)

    def __isub__(self, other: 'Vec2D') -> 'Vec2D':
        self._vx -= other._vx
        self._vy -= other._vy
        self._magnitude = math.sqrt(self._vx ** 2 + self._vy ** 2)
        self._direction = math.degrees(math.atan2(self._vy, self._vx))
        return self

    def __add__(self, other: 'Vec2D') -> 'Vec2D':
        vx = self._vx + other._vx
        vy = self._vy + other._vy
        magnitude = math.sqrt(vx ** 2 + vy ** 2)
        direction = math.degrees(math.atan2(vy, vx))
        return Vec2D(magnitude, direction)

    def __iadd__(self, other: 'Vec2D') -> 'Vec2D':
        self._vx += other._vx
        self._vy += other._vy
        self._magnitude = math.sqrt(self._vx ** 2 + self._vy ** 2)
        self._direction = math.degrees(math.atan2(self._vy, self._vx))
        return self

    def __mul__(self, scalar: float) -> 'Vec2D':
        return Vec2D(self.magnitude * scalar, self.direction)
