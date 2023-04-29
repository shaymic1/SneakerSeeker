from sneaker_seeker.game_obj.movable import Movable
from sneaker_seeker.common_types.vec2d import Vec2D


class Point(Movable):
    "moving point in space 2D"

    def __init__(self, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D()) -> None:
        super().__init__(location, speed)
