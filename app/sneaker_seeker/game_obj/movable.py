from sneaker_seeker.common_types.speed_vec import SpeedVec
from sneaker_seeker.common_types.point2d import Point2D


class Movable:

    def __init__(self, point: dict = None, speed: dict = None) -> None:
        self.location: Point2D = Point2D(**point) if point else Point2D()
        self.speed: SpeedVec = SpeedVec(**speed) if speed else SpeedVec()

    def move(self, dt: float):
        self.location.x += self.speed.vx * dt
        self.location.y += self.speed.vy * dt



