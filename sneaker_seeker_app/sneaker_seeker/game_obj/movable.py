from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.common_types.destination import Destination


class Movable:
    last_id = 0

    def __init__(self, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D()) -> None:
        Movable.last_id += 1
        self.id = Movable.last_id
        self.location: Vec2D = location
        self.speed: Vec2D = speed
        self.destination = None

    def __hash__(self):
        return self.id.__hash__()

    def __eq__(self, other):
        return isinstance(other, Movable) and self.id == other.id

    def advance(self, dt: float) -> None:
        self.location += (self.speed * dt)
        if self.destination:
            self.destination.arrival_time -= dt
            self.destination.arrived = (abs(self.destination.arrival_time) < dt)

    def steer_to(self, location: Vec2D) -> None:
        self.speed.angle = utils.calc_angle(x=(location.x - self.location.x), y=(location.y - self.location.y))

    def set_destination(self, dst: Vec2D, new_speed: float = None, arrival_time: float = None) -> None:
        self.speed.angle = utils.calc_angle(x=(dst.x - self.location.x), y=(dst.y - self.location.y))
        if new_speed:
            self.speed.magnitude = new_speed
        if not arrival_time:
            arrival_time = self.location.distance_to(dst) / self.speed.magnitude
        self.destination = Destination(location=dst, arrival_time=arrival_time)

    def stop(self) -> None:
        self.speed.magnitude = 0.01
