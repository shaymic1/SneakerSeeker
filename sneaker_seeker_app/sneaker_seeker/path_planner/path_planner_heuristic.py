from __future__ import annotations
from enum import Enum, auto
from typing import Union, Callable

from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.vec2d import Vec2D


class PlayerPhase(Enum):
    HEADED_TO_FRONTAL_DKIZ_LINE = auto()
    ALIGN_TO_HEAD_ON_SEARCH = auto()
    BACK_TO_BASE = auto()


class PlannerPhase(Enum):
    DELAY_LAUNCH = auto()
    SET_FIRST_PATH = auto()
    ON_AIR = auto()


class PathPlannerHeuristic(PathPlanner):

    def __init__(self, dkiz: DKIZ, roi: ROI, offset_from_ends_dkiz_frontal_line: float,
                 delay_launch_time: float, **_ignore) -> None:
        self.dkiz: DKIZ = dkiz
        self.roi: ROI = roi
        self.offset_from_ends_dkiz_frontal_line = offset_from_ends_dkiz_frontal_line
        self.curr_time = None
        self.players_base: Vec2D()
        self.delay_launch_time: float = delay_launch_time
        self.planner_phase: PlannerPhase = self.starting_phase(delay_launch_time)
        self.player_phase: dict[Seeker, PlayerPhase] = {}
        self.phase_func: dict[PlannerPhase, Callable] = {
            PlannerPhase.DELAY_LAUNCH: self.__delay_launch,
            PlannerPhase.SET_FIRST_PATH: self.__set_first_path,
            PlannerPhase.ON_AIR: self.__on_air
        }

    def set_path(self, players: list[Seeker], time: float) -> None:
        self.curr_time = time
        self.phase_func[self.planner_phase](players)

    def __delay_launch(self, players) -> None:
        if self.curr_time < self.delay_launch_time:
            return
        next_phase = PlannerPhase.DELAY_LAUNCH.value + 1
        self.planner_phase = PlannerPhase(next_phase)
        self.phase_func[self.planner_phase](players)

    def __set_first_path(self, players: list[Seeker]):
        self.players_base = players[0].location
        self.__set_destination_to_frontal_dkiz_line(players)
        self.planner_phase = PlannerPhase(self.planner_phase.value + 1)
        for p in players:
            self.player_phase[p] = PlayerPhase.HEADED_TO_FRONTAL_DKIZ_LINE

    def __on_air(self, players: list[Seeker]):
        for p in players:

            if self.player_phase[p] == PlayerPhase.HEADED_TO_FRONTAL_DKIZ_LINE:
                if not utils.point_in_roi(p.location, self.roi) and p.state != Seeker.State.CATCH:
                    p.halt()
                    p.state = Seeker.State.HALT
                if p.destination.arrived:
                    p.speed.angle = utils.calc_angle(x=-self.dkiz.speed.x, y=-self.dkiz.speed.y)
                    p.observation_direction = p.speed.angle
                    self.player_phase[p] = PlayerPhase.ALIGN_TO_HEAD_ON_SEARCH

            if self.player_phase[p] == PlayerPhase.ALIGN_TO_HEAD_ON_SEARCH:
                if self.__is_passed_DKIZ(p):
                    p.set_destination(self.players_base)
                    self.player_phase[p] = PlayerPhase.BACK_TO_BASE
                    p.state = Seeker.State.BACK_TO_BASE


    def __set_destination_to_frontal_dkiz_line(self, players: list[Seeker]):
        p1, p2 = self.dkiz.r_frontal_line.location, self.dkiz.l_frontal_line.location
        middle_points = p1.points_between(other=p2, num_points=len(players),
                                          offset_from_ends=self.offset_from_ends_dkiz_frontal_line)
        for player, loc in zip(players, middle_points):
            player_speed = player.physical_specs.cruise_speed
            collision_point, arrival_time = utils.calc_possible_collision_point_and_time(
                trgt_loc=loc, trgt_spd=self.dkiz.speed, friendly_loc=player.location,
                friendly_spd=player_speed)
            player.set_destination(dst=collision_point, new_speed=player_speed, arrival_time=arrival_time)
            player.observation_direction = player.speed.angle

    @staticmethod
    def starting_phase(delay_launch_time):
        return PlannerPhase.DELAY_LAUNCH if delay_launch_time > 0 else PlannerPhase.SET_FIRST_PATH

    def __is_passed_DKIZ(self, player: Seeker):
        is_outside_DKIZ = player.location.distance_to(self.dkiz.location) > self.dkiz.max_dist_from_center
        return is_outside_DKIZ and not player.is_getting_closer(self.dkiz)
