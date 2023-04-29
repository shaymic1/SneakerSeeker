from __future__ import annotations
from sneaker_seeker.game_obj.movable import Movable
from sneaker_seeker.common_types.vec2d import Vec2D


class ROI(Movable):
    """this is the game Region Of Interest. the sneaking game should occur inside.
       +------------------+
       |                  |
     height               |
       |                  |
     (x,y)-----width------|
    """

    def __init__(self, height: int, width: int, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D()) -> None:
        super().__init__(location, speed)
        self.height = height
        self.width = width

    @classmethod
    def from_dict(cls, height: int, width: int, location: dict = None, speed: dict = None) -> ROI:
        loc = Vec2D(**location) if location else Vec2D()
        spd = Vec2D.from_polar(**speed) if speed else Vec2D()
        return cls(height=height, width=width, location=loc, speed=spd)

