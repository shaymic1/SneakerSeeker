from sneaker_seeker.game_obj.movable import Movable
from sneaker_seeker.common_types.vec2d import Vec2D
import pytest


def test_move():
    initial_location = {'x': 0, 'y': 0}
    initial_speed = {'magnitude': 10, 'angle': 45}
    movable = Movable(location=Vec2D(**initial_location), speed=Vec2D.from_polar(**initial_speed))
    dt = 1.0
    movable.advance(dt)
    assert movable.location.x == pytest.approx(7.071, rel=1e-3)
    assert movable.location.y == pytest.approx(7.071, rel=1e-3)
