from .movable import Movable
from sneaker_seeker.common_types.physical_specs import PhysicalSpecs
from sneaker_seeker.common_types.vec2d import Vec2D


class Player(Movable):

    def __init__(self, physical_specs: PhysicalSpecs, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D(),
                 los: float = 100, fov: float = 180, observation_direction: float = None) -> None:
        super().__init__(location, speed)
        self.physical_specs: physical_specs = physical_specs
        self.observation_direction: float = observation_direction
        self.los: float = los
        self.fov: float = fov
