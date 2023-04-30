import pytest
from sneaker_seeker.common_types.physical_specs import PhysicalSpecs
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.player import Player


@pytest.fixture
def player():
    return Player(
        physical_specs=PhysicalSpecs(**{"cruise_speed": 50, "max_speed": 100, "max_speed_time": 20}),
        location=Vec2D(**{"x": 0, "y": 0}),
        observation_direction=0,
        los=1000,
        fov=60,
        speed=Vec2D.from_polar(**{"magnitude": 10, "angle": 0})
    )


def test_player_creation(player):
    assert player.id > 0
    assert isinstance(player.physical_specs, PhysicalSpecs)
    assert isinstance(player.location, Vec2D)
    assert isinstance(player.speed, Vec2D)
    assert player.speed.magnitude == 10
    assert player.speed.angle == 0


def test_player_move(player):
    player.move(1)
    assert player.location.x == 10
    assert player.location.y == 0
