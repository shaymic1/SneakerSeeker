import math
from typing import Tuple


class Vec2D:
    """A two-dimensional vector with Cartesian coordinates."""

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x, self.y = x, y

    @classmethod
    def from_polar(cls, magnitude: float, angle: float) -> 'Vec2D':
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
        self.x = mag * math.cos(math.radians(value))
        self.y = mag * math.sin(math.radians(value))

    def __str__(self) -> str:
        return '{:g}i + {:g}j'.format(self.x, self.y)

    def __repr__(self) -> str:
        return repr((self.x, self.y))

    def dot(self, other: 'Vec2D') -> float:
        """The scalar (dot) product of self and other. Both must be vectors."""
        if not isinstance(other, Vec2D):
            raise TypeError('Can only take dot product of two Vector2D objects')
        return self.x * other.x + self.y * other.y

    # Alias the __matmul__ method to dot so we can use a @ b as well as a.dot(b).
    __matmul__ = dot

    def __sub__(self, other: 'Vec2D') -> 'Vec2D':
        return Vec2D(self.x - other.x, self.y - other.y)

    def __add__(self, other: 'Vec2D') -> 'Vec2D':
        return Vec2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> 'Vec2D':
        if isinstance(scalar, int) or isinstance(scalar, float):
            return Vec2D(self.x * scalar, self.y * scalar)
        raise NotImplementedError('Can only multiply Vector2D by a scalar')

    def __rmul__(self, scalar: float) -> 'Vec2D':
        return self.__mul__(scalar)

    def __neg__(self) -> 'Vec2D':
        return Vec2D(-self.x, -self.y)

    def __truediv__(self, scalar: float) -> 'Vec2D':
        return Vec2D(self.x / scalar, self.y / scalar)

    def __mod__(self, scalar: float) -> 'Vec2D':
        return Vec2D(self.x % scalar, self.y % scalar)

    def __abs__(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def distance_to(self, other: 'Vec2D') -> float:
        return abs(self - other)

    def to_polar(self) -> Tuple[float, float]:
        return abs(self), math.degrees(math.atan2(self.y, self.x))

    def relative_angle(self, other: 'Vec2D') -> float:
        return math.degrees(math.atan2((other.y - self.y), (other.x - self.x)))
