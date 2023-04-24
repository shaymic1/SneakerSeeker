# import math
# import unittest
# from math import isclose
# from sneaker_seeker.common_types.speed_vec import SpeedVec
#
#
# class TestSpeedVec(unittest.TestCase):
#
#     def test_post_init(self):
#         speed_vec = SpeedVec(_magnitude=10, _direction=45)
#         self.assertAlmostEqual(speed_vec.vx, 7.0710678118654755)
#         self.assertAlmostEqual(speed_vec.vy, 7.0710678118654755)
#
#     def test_eq(self):
#         speed_vec1 = SpeedVec(_magnitude=10, _direction=45)
#         speed_vec2 = SpeedVec(_magnitude=10, _direction=45)
#         speed_vec3 = SpeedVec(_magnitude=5, _direction=45)
#         self.assertEqual(speed_vec1, speed_vec2)
#         self.assertNotEqual(speed_vec1, speed_vec3)
#
#     def test_magnitude(self):
#         speed_vec = SpeedVec(_magnitude=10, _direction=45)
#         speed_vec.magnitude = 5
#         self.assertAlmostEqual(speed_vec.magnitude, 5)
#         self.assertAlmostEqual(speed_vec.vx, 3.5355339059327378)
#         self.assertAlmostEqual(speed_vec.vy, 3.5355339059327378)
#
#         with self.assertRaises(ValueError):
#             speed_vec.magnitude = -5
#
#     def test_direction(self):
#         speed_vec = SpeedVec(_magnitude=10, _direction=45)
#         speed_vec.direction = 90
#         self.assertAlmostEqual(speed_vec.direction, 90)
#         self.assertAlmostEqual(speed_vec.vx, 0)
#         self.assertAlmostEqual(speed_vec.vy, 10)
#
#     def test_vx(self):
#         speed_vec = SpeedVec(_magnitude=10, _direction=45)
#         self.assertAlmostEqual(speed_vec.vx, 7.0710678118654755)
#
#     def test_vy(self):
#         speed_vec = SpeedVec(_magnitude=10, _direction=45)
#         self.assertAlmostEqual(speed_vec.vy, 7.0710678118654755)


import math
from math import isclose
import pytest
from sneaker_seeker.common_types.speed_vec import SpeedVec


def test_post_init():
    speed_vec = SpeedVec(_magnitude=10, _direction=45)
    assert math.isclose(speed_vec.vx, 7.0710678118654755)
    assert math.isclose(speed_vec.vy, 7.0710678118654755)


def test_eq():
    speed_vec1 = SpeedVec(_magnitude=10, _direction=45)
    speed_vec2 = SpeedVec(_magnitude=10, _direction=45)
    speed_vec3 = SpeedVec(_magnitude=5, _direction=45)
    assert speed_vec1 == speed_vec2
    assert speed_vec1 != speed_vec3


def test_magnitude():
    speed_vec = SpeedVec(_magnitude=10, _direction=45)
    speed_vec.magnitude = 5
    assert math.isclose(speed_vec.magnitude, 5)
    assert math.isclose(speed_vec.vx, 3.5355339059327378)
    assert math.isclose(speed_vec.vy, 3.5355339059327378)

    with pytest.raises(ValueError):
        speed_vec.magnitude = -5


def test_direction():
    speed_vec = SpeedVec(_magnitude=10, _direction=45)
    speed_vec.direction = 90
    assert math.isclose(speed_vec.direction, 90)
    assert speed_vec.vx < 10**(-6)
    assert math.isclose(speed_vec.vy, 10)


def test_vx():
    speed_vec = SpeedVec(_magnitude=10, _direction=45)
    assert math.isclose(speed_vec.vx, 7.0710678118654755)


def test_vy():
    speed_vec = SpeedVec(_magnitude=10, _direction=45)
    assert math.isclose(speed_vec.vy, 7.0710678118654755)
