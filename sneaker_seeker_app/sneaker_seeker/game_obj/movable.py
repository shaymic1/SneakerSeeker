from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.vec2d import Vec2D


class Movable:
    last_id = 0

    def __init__(self, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D()) -> None:
        Movable.last_id += 1
        self.id = Movable.last_id
        self.location: Vec2D = location
        self.speed: Vec2D = speed

    def move(self, dt: float):
        self.location += (self.speed * dt)

    def steer(self, location: Vec2D):
        self.speed.angle = utils.calc_angle(x=(location.x - self.location.x), y=(location.y - self.location.y))
