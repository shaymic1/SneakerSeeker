from .movable import Movable
from sneaker_seeker.common_types.physical_specs import PhysicalSpecs
from sneaker_seeker.common_types.vec2d import Vec2D


class Player(Movable):

    def __init__(self, physical_specs: PhysicalSpecs, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D(),
                 los: float = 100, fov: float = 180, observation_direction: float = None) -> None:
        super().__init__(location, speed)
        self.physical_specs: PhysicalSpecs = physical_specs
        self.observation_direction: float = observation_direction
        self.los: float = los
        self.fov: float = fov

    def set_destination(self, dst: Vec2D, new_speed: float = None, arrival_time: float = None,
                        observation_direction: float = None) -> None:
        super().set_destination(dst=dst, new_speed=new_speed, arrival_time=arrival_time)
        self.observation_direction = observation_direction if observation_direction else self.speed.angle

    def observe_to_location(self, trgt: Vec2D):
        self.observation_direction = self.location.relative_angle(trgt)
