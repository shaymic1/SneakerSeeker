from .movable import Movable
from sneaker_seeker.common_types.physical_specs import PhysicalSpecs


class Player(Movable):
    last_id = 0

    def __init__(self, physical_specs: dict, location: dict = None, observation_direction: float = None,
                 los: float = 1000, fov: float = 60, speed: dict = None) -> None:
        super().__init__(location, speed)
        Player.last_id += 1

        self.id = Player.last_id
        self.physical_specs: PhysicalSpecs = PhysicalSpecs(**physical_specs)
        self.observation_direction: float = observation_direction if observation_direction else self.speed.direction
        self.los: float = los
        self.fov: float = fov

