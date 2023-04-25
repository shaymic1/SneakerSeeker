from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.common_types.point2d import Point2D


class Movable:
    last_id = 0

    def __init__(self, point: dict = None, speed: dict = None) -> None:
        Movable.last_id += 1
        self.id = Movable.last_id
        self.location: Point2D = Point2D(**point) if point else Point2D()
        self.speed: Vec2D = Vec2D(**speed) if speed else Vec2D()

    def move(self, dt: float):
        self.location.x += self.speed.vx * dt
        self.location.y += self.speed.vy * dt

    def steer(self, point: Point2D):
        self.speed.direction = utils.calc_angle(x=(point.x - self.location.x), y=(point.y - self.location.y))
