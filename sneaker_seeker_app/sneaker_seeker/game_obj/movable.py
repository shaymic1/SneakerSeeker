from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.vec2d import Vec2D


class Movable:
    last_id = 0

    def __init__(self, location: dict = None, speed: dict = None) -> None:
        Movable.last_id += 1
        self.id = Movable.last_id
        self.location: Vec2D = Vec2D(**location) if location else Vec2D()
        self.speed: Vec2D = Vec2D.from_polar(**speed) if speed else Vec2D()

    def move(self, dt: float):
        self.location += (self.speed * dt)

    def steer(self, location: Vec2D):
        self.speed.angle = utils.calc_angle(x=(location.x - self.location.x), y=(location.y - self.location.y))
