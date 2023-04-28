from sneaker_seeker.game_obj.movable import Movable
import pytest


def test_move():
    initial_location = {'x': 0, 'y': 0}
    initial_speed = {'magnitude': 10, 'angle': 45}
    movable = Movable(location=initial_location, speed=initial_speed)
    dt = 1.0
    movable.move(dt)
    assert movable.location.x == pytest.approx(7.071, rel=1e-3)
    assert movable.location.y == pytest.approx(7.071, rel=1e-3)
