import pytest
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.dkiz import DKIZ


@pytest.fixture
def dkiz():
    # Create a DKIZ object with some default values for testing purposes
    args = {
        "shape": {
            "type": "circle",
            "circle": {"radius": 1}
        },
        "uncertainty_radius": 1,
        "location": {"x": 0, "y": 0},
        "speed": {"magnitude": 50, "angle": 210}
    }
    return DKIZ.from_dict(**args)


def test_contains_circle(dkiz):
    assert dkiz.contains(Vec2D(0.5, 0.5)) == True
    assert dkiz.contains(Vec2D(1.5, 1.5)) == False


def test_generate_points_inside(dkiz):
    # Check that generated points are inside the DKIZ and have the expected minimum distance between them
    points = dkiz.generate_points_inside(5, 0.1)
    assert all([dkiz.contains(p) for p in points])
    assert all([p1.distance_to(p2) >= 0.1 for i, p1 in enumerate(points) for p2 in points[i + 1:]])
