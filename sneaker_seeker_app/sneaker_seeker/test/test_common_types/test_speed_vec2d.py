import math
import pytest
from sneaker_seeker.common_types.vec2d import Vec2D


def test_post_init():
    speed_vec = Vec2D(_magnitude=10, _direction=45)
    assert math.isclose(speed_vec.vx, 7.0710678118654755)
    assert math.isclose(speed_vec.vy, 7.0710678118654755)


def test_eq():
    speed_vec1 = Vec2D(_magnitude=10, _direction=45)
    speed_vec2 = Vec2D(_magnitude=10, _direction=45)
    speed_vec3 = Vec2D(_magnitude=5, _direction=45)
    assert speed_vec1 == speed_vec2
    assert speed_vec1 != speed_vec3


def test_magnitude():
    speed_vec = Vec2D(_magnitude=10, _direction=45)
    speed_vec.magnitude = 5
    assert math.isclose(speed_vec.magnitude, 5)
    assert math.isclose(speed_vec.vx, 3.5355339059327378)
    assert math.isclose(speed_vec.vy, 3.5355339059327378)

    with pytest.raises(ValueError):
        speed_vec.magnitude = -5


def test_direction():
    speed_vec = Vec2D(_magnitude=10, _direction=45)
    speed_vec.direction = 90
    assert math.isclose(speed_vec.direction, 90)
    assert speed_vec.vx < 10 ** (-6)
    assert math.isclose(speed_vec.vy, 10)


def test_vx():
    speed_vec = Vec2D(_magnitude=10, _direction=45)
    assert math.isclose(speed_vec.vx, 7.0710678118654755)


def test_vy():
    speed_vec = Vec2D(_magnitude=10, _direction=45)
    assert math.isclose(speed_vec.vy, 7.0710678118654755)


def test_speed_vec_2d_addition():
    v1 = Vec2D(10, 45)
    v2 = Vec2D(10, -45)
    v3 = v1 + v2
    assert v3.magnitude == pytest.approx(14.1421, 0.0001)
    assert v3.direction == pytest.approx(0, 0.0001)


def test_speed_vec_2d_inplace_addition():
    v1 = Vec2D(10, 45)
    v2 = Vec2D(10, -45)
    v1 += v2
    assert v1.magnitude == pytest.approx(14.1421, 0.0001)
    assert v1.direction == pytest.approx(0, 0.0001)


def test_speed_vec_2d_subtraction():
    v1 = Vec2D(10, 45)
    v2 = Vec2D(10, -45)
    v3 = v1 - v2
    assert v3.magnitude == pytest.approx(14.1421, 0.0001)
    assert v3.direction == pytest.approx(90, 0.0001)


def test_speed_vec_2d_inplace_subtraction():
    v1 = Vec2D(10, 45)
    v2 = Vec2D(10, -45)
    v1 -= v2
    assert v1.magnitude == pytest.approx(14.1421, 0.0001)
    assert v1.direction == pytest.approx(90, 0.0001)


def test_speed_vec_2d_magnitude_property():
    v = Vec2D(10, 45)
    assert v.magnitude == 10


def test_speed_vec_2d_magnitude_property_setter():
    v = Vec2D(10, 45)
    v.magnitude = 5
    assert v.magnitude == 5
    assert v.vx == pytest.approx(3.5355, 0.0001)
    assert v.vy == pytest.approx(3.5355, 0.0001)
    assert v.direction == pytest.approx(45, 0.0001)


def test_speed_vec_2d_magnitude_property_setter_negative():
    v = Vec2D(10, 45)
    with pytest.raises(ValueError):
        v.magnitude = -5


def test_speed_vec_2d_direction_property():
    v = Vec2D(10, 45)
    assert v.direction == 45


def test_speed_vec_2d_direction_property_setter():
    v = Vec2D(10, 45)
    v.direction = 90
    assert v.magnitude == pytest.approx(10, 0.0001)
    assert v.vx == pytest.approx(0, 0.0001)
    assert v.vy == pytest.approx(10, 0.0001)
    assert v.direction == pytest.approx(90, 0.0001)


def test_speed_vec_2d_vx_property():
    v = Vec2D(10, 45)
    assert v.vx == pytest.approx(7.0711, 0.0001)


def test_subtract():
    s1 = Vec2D(3, 0)
    s2 = Vec2D(1, 90)
    result = s1 - s2
    assert result.magnitude == pytest.approx(3.162, rel=1e-3)
    assert result.direction == pytest.approx(-18.435, rel=1e-3)
    assert result.vx == pytest.approx(3.0, rel=1e-3)
    assert result.vy == pytest.approx(-1.0, rel=1e-3)


def test_inplace_subtract():
    s1 = Vec2D(3, 0)
    s2 = Vec2D(1, 90)
    s1 -= s2
    assert s1.magnitude == pytest.approx(3.162, rel=1e-3)
    assert s1.direction == pytest.approx(-18.435, rel=1e-3)
    assert s1.vx == pytest.approx(3.0, rel=1e-3)
    assert s1.vy == pytest.approx(-1.0, rel=1e-3)


def test_add():
    s1 = Vec2D(3, 0)
    s2 = Vec2D(1, 90)
    result = s1 + s2
    assert result.magnitude == pytest.approx(3.162, rel=1e-3)
    assert result.direction == pytest.approx(18.43, rel=1e-3)
    assert result.vx == pytest.approx(3, rel=1e-3)
    assert result.vy == pytest.approx(1, rel=1e-3)


def test_inplace_add():
    s1 = Vec2D(3, 0)
    s2 = Vec2D(1, 90)
    s1 += s2
    assert s1.magnitude == pytest.approx(3.162, rel=1e-3)
    assert s1.direction == pytest.approx(18.43, rel=1e-3)
    assert s1.vx == pytest.approx(3, rel=1e-3)
    assert s1.vy == pytest.approx(1, rel=1e-3)
