from sneaker_seeker.common_types.point2d import Point2D
import pytest


def test_location_distance():
    loc1 = Point2D(x=0, y=0)
    loc2 = Point2D(x=3, y=4)
    assert loc1.dist(loc2) == 5


def test_location_relative_angle():
    loc1 = Point2D(x=0, y=0)
    loc2 = Point2D(x=1, y=1)
    assert loc1.relative_angle(loc2) == pytest.approx(45.0, rel=1e-3)
