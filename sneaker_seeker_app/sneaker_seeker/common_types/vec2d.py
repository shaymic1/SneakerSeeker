from __future__ import annotations
import math
from typing import Tuple, List


class Vec2D:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x, self.y = x, y

    @classmethod
    def from_polar(cls, magnitude: float, angle: float) -> Vec2D:
        """an other Ctor to enable the creation from magnitude and angle."""
        return cls(x=magnitude * math.cos(math.radians(angle)),
                   y=magnitude * math.sin(math.radians(angle)))

    @property
    def magnitude(self):
        return abs(self)

    @magnitude.setter
    def magnitude(self, value):
        old_mag = abs(self)
        if value < 0:
            raise ValueError("Magnitude cannot be negative")
        self.x *= (value / old_mag)
        self.y *= (value / old_mag)

    @property
    def angle(self):
        return math.degrees(math.atan2(self.y, self.x))

    @angle.setter
    def angle(self, value: float) -> None:
        mag = self.magnitude
        mag = 0.01 if mag == 0 else mag
        self.x = mag * math.cos(math.radians(value))
        self.y = mag * math.sin(math.radians(value))

    def __str__(self) -> str:
        return '{:g}i + {:g}j'.format(self.x, self.y)

    def __repr__(self) -> str:
        return repr((self.x, self.y))

    def __eq__(self, other: Vec2D) -> bool:
        if isinstance(other, Vec2D):
            return math.isclose(self.x, other.x, abs_tol=1e-10) and math.isclose(self.y, other.y, abs_tol=1e-10)
        return False

    def __sub__(self, other: Vec2D) -> Vec2D:
        return Vec2D(self.x - other.x, self.y - other.y)

    def __add__(self, other: Vec2D) -> Vec2D:
        return Vec2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Vec2D:
        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vec2D(self.x * scalar, self.y * scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __rmul__(self, scalar: float) -> Vec2D:
        return self.__mul__(scalar)

    def __neg__(self) -> Vec2D:
        return Vec2D(-self.x, -self.y)

    def __truediv__(self, scalar: float) -> Vec2D:
        return Vec2D(self.x / scalar, self.y / scalar)

    def __mod__(self, scalar: float) -> Vec2D:
        return Vec2D(self.x % scalar, self.y % scalar)

    def __abs__(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dot(self, other: Vec2D) -> float:
        """The scalar (dot) product of self and other. Both must be vectors."""
        if not isinstance(other, Vec2D):
            raise TypeError('Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y

    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot

    def distance_to(self, other: Vec2D) -> float:
        return abs(self - other)

    def to_polar(self) -> Tuple[float, float]:
        return abs(self), math.degrees(math.atan2(self.y, self.x))

    def to_cartesian(self) -> Tuple[float, float]:
        return self.x, self.y

    def relative_angle(self, other: Vec2D, radian=False) -> float:
        if radian:
            return math.atan2((other.y - self.y), (other.x - self.x))
        return math.degrees(math.atan2((other.y - self.y), (other.x - self.x)))

    def middle_point(self, other: Vec2D) -> Vec2D:
        return Vec2D(x=(self.x + other.x) / 2, y=(self.y + other.y) / 2)

    def points_between(self, other: Vec2D, num_points: int, offset_from_ends: float = 0) -> List[Vec2D]:
        if num_points == 1:
            return [self.middle_point(other)]
        angle = self.relative_angle(other, radian=True)
        p1 = Vec2D(x=self.x + offset_from_ends * math.cos(angle), y=(self.y + offset_from_ends * math.sin(angle)))
        pn = Vec2D(x=other.x - offset_from_ends * math.cos(angle), y=(other.y - offset_from_ends * math.sin(angle)))
        dist_between = p1.distance_to(pn) / (num_points - 1)
        points = [p1]
        for i in range(1, num_points - 1):
            points.append(Vec2D(x=p1.x + i * (dist_between * math.cos(angle)),
                                y=p1.y + i * (dist_between * math.sin(angle))))
        points.append(pn)
        return points
