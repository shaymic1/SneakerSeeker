from __future__ import annotations

import math
from enum import Enum, auto

from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.common_types.destination import Destination


class Movable:
    last_id = 0

    class Steer(Enum):
        RIGHT = auto()
        LEFT = auto()


    def __init__(self, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D(), turn_radius: float = 0) -> None:
        Movable.last_id += 1
        self.id = Movable.last_id
        self.location: Vec2D = location
        self.speed: Vec2D = speed
        self.turn_radius = turn_radius
        self.destination: Destination = None

    def __hash__(self):
        return self.id.__hash__()

    def __eq__(self, other):
        return isinstance(other, Movable) and self.id == other.id

    def advance(self, dt: float) -> None:
        self.location += (self.speed * dt)
        if self.destination:
            self.destination.arrival_time -= dt
            self.destination.arrived = (self.destination.arrival_time < dt)

    def steer_to_destination(self, location: Vec2D) -> None:
        self.speed.angle = utils.calc_angle(x=(location.x - self.location.x), y=(location.y - self.location.y))

    def steer(self, dt: float, direction: Movable.Steer):
        if self.turn_radius <= 0:
            raise Exception("cannot steer when there is no turn radius.")
        dx = (dt/1000) * self.speed.magnitude
        delta_theta = 360 * (dx / (2 * math.pi * self.turn_radius))
        if direction == Movable.Steer.RIGHT:
            delta_theta *= -1
        self.speed.angle = (self.speed.angle + delta_theta) % 360

    def set_destination(self, dst: Vec2D, new_speed: float = None, arrival_time: float = None) -> None:
        self.speed.angle = utils.calc_angle(x=(dst.x - self.location.x), y=(dst.y - self.location.y))
        if new_speed:
            self.speed.magnitude = new_speed
        if not arrival_time:
            arrival_time = self.location.distance_to(dst) / self.speed.magnitude
        self.destination = Destination(location=dst, arrival_time=arrival_time)

    def halt(self) -> None:
        self.speed.magnitude = 0.01

    def is_getting_closer(self, other: Movable) -> bool:
        rel_speed = other.speed - self.speed
        rel_location = other.location - self.location
        return rel_speed.dot(rel_location) < 0 and rel_speed.magnitude > 0 and rel_location.magnitude > 0
