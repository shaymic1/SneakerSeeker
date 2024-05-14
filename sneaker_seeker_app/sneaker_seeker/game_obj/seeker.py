from __future__ import annotations
from enum import StrEnum, auto

from sneaker_seeker.common_types.physical_specs import PhysicalSpecs
from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.common_types.vec2d import Vec2D


class Seeker(Player):
    class Form(StrEnum):
        PLAIN = auto()
        DRONE = auto()

    class State(StrEnum):
        MOVE = auto()
        HALT = auto()
        SWAY = auto()
        SEEK = auto()
        CATCH = auto()
        BACK_TO_BASE = auto()

    def __init__(self, physical_specs: PhysicalSpecs, group_num: int, location: Vec2D = Vec2D(), speed: Vec2D = Vec2D(),
                 los: float = 100, fov: float = 180, catch_dist: float = 50,
                 observation_direction: float = None) -> None:
        super().__init__(physical_specs=physical_specs, group_num=group_num, location=location, speed=speed, los=los,
                         fov=fov, observation_direction=observation_direction)
        self.sway_mid_axis = observation_direction
        self.max_sway_tilt_from_axis = (180 - self.fov) / 2
        self.swaying_theta_dot = 10  # [degree/ms]
        self.swaying_clockwise = 1  # should be 1 or -1
        self.drone_formation_time = 3
        self.catch_dist = catch_dist
        self._state = Seeker.State.SEEK
        self._form = Seeker.Form.PLAIN

    @classmethod
    def from_dict(cls, physical_specs: dict, group_num: int, location: dict = None, speed: dict = None,
                  los: float = 100, fov: float = 180, catch_dist: float = 50,
                  observation_direction: float = None) -> Seeker:
        loc = Vec2D(**location) if location else Vec2D()
        spd = Vec2D.from_polar(**speed) if speed else Vec2D()
        specs = PhysicalSpecs(**physical_specs)
        obser_dir = observation_direction if observation_direction else spd.angle
        return cls(physical_specs=specs, group_num=group_num, location=loc, speed=spd, los=los, fov=fov,
                   catch_dist=catch_dist, observation_direction=obser_dir)

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, new_form: Seeker.State):
        self._form = new_form
        if new_form == Seeker.Form.PLAIN:
            self.turn_radius = 250
        if new_form == Seeker.Form.DRONE:
            self.turn_radius = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: Seeker.State):
        if self._state == Seeker.State.SWAY:
            self.sway_mid_axis = self.observation_direction
        else:
            self.observation_direction = self.sway_mid_axis
        # if new_state == Seeker.State.CATCH:
        #     self.fov = 40
        self._state = new_state

    def can_see(self, location: Vec2D) -> bool:
        if self.location.distance_to(location) > self.los:
            return False
        lower_bound_ang = self.observation_direction - self.fov / 2
        upper_bound_ang = self.observation_direction + self.fov / 2
        return lower_bound_ang <= self.location.relative_angle(location) <= upper_bound_ang

    def advance(self, dt: float) -> None:
        super().advance(dt)

    #     if self.state == Seeker.State.SWAY:
    #         self.sway(dt)

    # TODO: fix the swaying function.
    def sway(self, dt):
        delta_theta = dt * self.swaying_theta_dot * self.swaying_clockwise
        if abs((delta_theta + self.observation_direction) - self.sway_mid_axis) > self.max_sway_tilt_from_axis:
            self.swaying_clockwise *= -1
            delta_theta *= self.swaying_clockwise
        self.observation_direction += delta_theta
