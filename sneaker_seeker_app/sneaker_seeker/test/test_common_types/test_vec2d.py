import math
import pytest
from sneaker_seeker.common_types.vec2d import Vec2D


def test_magnitude():
    v = Vec2D(3, 4)
    assert v.magnitude == 5.0


def test_angle():
    v = Vec2D(1, 1)
    assert math.isclose(v.angle, 45.0, rel_tol=1e-9)


def test_dot():
    v1 = Vec2D(1, 2)
    v2 = Vec2D(3, 4)
    assert v1.dot(v2) == 11.0


def test_subtraction():
    v1 = Vec2D(1, 2)
    v2 = Vec2D(3, 4)
    v3 = v1 - v2
    assert v3.x == -2
    assert v3.y == -2


def test_addition():
    v1 = Vec2D(1, 2)
    v2 = Vec2D(3, 4)
    v3 = v1 + v2
    assert v3.x == 4
    assert v3.y == 6


def test_multiplication():
    v1 = Vec2D(1, 2)
    v2 = v1 * 2
    assert v2.x == 2
    assert v2.y == 4


def test_division():
    v1 = Vec2D(1, 2)
    v2 = v1 / 2
    assert v2.x == 0.5
    assert v2.y == 1.0


def test_modulo():
    v1 = Vec2D(7, 5)
    v2 = v1 % 3
    assert v2.x == 1
    assert v2.y == 2


def test_distance_to():
    v1 = Vec2D(1, 2)
    v2 = Vec2D(4, 6)
    assert math.isclose(v1.distance_to(v2), 5.0, rel_tol=1e-9)


def test_to_polar():
    v = Vec2D(3, 4)
    r, theta = v.to_polar()
    assert math.isclose(r, 5.0, rel_tol=1e-9)
    assert math.isclose(theta, 53.13010235, rel_tol=1e-9)


def test_relative_angle():
    v1 = Vec2D(1, 1)
    v2 = Vec2D(2, 2)
    assert math.isclose(v1.relative_angle(v2), 45.0, rel_tol=1e-9)


def test_init():
    v = Vec2D()
    assert v.x == 0 and v.y == 0
    v = Vec2D(1, 2)
    assert v.x == 1 and v.y == 2


def test_from_polar():
    v = Vec2D.from_polar(1, 0)
    assert v.x == 1 and v.y == 0
    v = Vec2D.from_polar(1, 90)
    assert abs(v.x) < 1e-5 and math.isclose(v.y, 1, rel_tol=1e-9)
    v = Vec2D.from_polar(1, 180)
    assert v.x == -1 and abs(v.y) < 1e-5
    v = Vec2D.from_polar(1, 270)
    assert abs(v.x) < 1e-5 and math.isclose(v.y, -1, rel_tol=1e-9)


def test_magnitude():
    v = Vec2D(3, 4)
    assert math.isclose(v.magnitude, 5)


def test_magnitude_setter():
    v = Vec2D(3, 4)
    v.magnitude = 2
    assert math.isclose(v.magnitude, 2)
    assert math.isclose(v.x, 1.2) and math.isclose(v.y, 1.6)


def test_magnitude_setter_negative():
    v = Vec2D(3, 4)
    try:
        v.magnitude = -1
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"


def test_angle():
    v = Vec2D(1, 1)
    assert math.isclose(v.angle, 45)


def test_angle_setter():
    v = Vec2D(1, 1)
    v.angle = 90
    assert abs(v.x) < 1e-5 and math.isclose(v.y, math.sqrt(2))


def test_dot():
    v1 = Vec2D(1, 2)
    v2 = Vec2D(3, 4)
    assert math.isclose(v1.dot(v2), 11)


def test_sub():
    v1 = Vec2D(1, 2)
    v2 = Vec2D(3, 4)
    v3 = v1 - v2
    assert v3.x == -2 and v3.y == -2


def test_add():
    v1 = Vec2D(1, 2)
    v2 = Vec2D(3, 4)
    v3 = v1 + v2
    assert v3.x == 4 and v3.y == 6


def test_mul():
    v1 = Vec2D(1, 2)
    v2 = v1 * 2
    assert v2.x == 2 and v2.y == 4


def test_rmul():
    v1 = Vec2D(1, 2)
    v2 = 2 * v1
    assert v2.x == 2 and v2.y == 4


def test_neg():
    v1 = Vec2D(1, 2)
    v2 = -v1
    assert v2.x == -1 and v2.y == -2


def test_vec2d_magnitude():
    # Test that the magnitude of a vector is calculated correctly.
    v1 = Vec2D(3, 4)
    assert v1.magnitude == 5.0

    v2 = Vec2D(-3, -4)
    assert v2.magnitude == 5.0

    v3 = Vec2D(0, 0)
    assert v3.magnitude == 0.0
