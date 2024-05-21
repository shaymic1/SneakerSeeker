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
    HEADED_TO_CIRCLE = auto()
    AROUND_THE_CIRCLE = auto()
    BACK_TO_BASE = auto()


class PlannerPhase(Enum):
    DELAY_LAUNCH = auto()
    SET_FIRST_PATH = auto()
    ON_AIR = auto()


class PathPlannerCircle(PathPlanner):

    def __init__(self, dkiz: DKIZ, roi: ROI, delay_launch_time: float, delay_launch_detection=False, **_ignore) -> None:
        self.dkiz: DKIZ = dkiz
        self.roi: ROI = roi
        self.prev_time = None
        self.curr_time = None
        self.players_base: Vec2D()
        self.delay_launch_time: float = delay_launch_time
        self.has_detection: bool = False
        self.planner_phase: PlannerPhase = self.__starting_phase(delay_launch_time, delay_launch_detection)
        self.player_phase: dict[Seeker, PlayerPhase] = {}
        self.phase_func: dict[PlannerPhase, Callable] = {
            PlannerPhase.DELAY_LAUNCH: self.__delay_launch,
            PlannerPhase.SET_FIRST_PATH: self.__set_first_path,
            PlannerPhase.ON_AIR: self.__on_air
        }

    def set_path(self, players: list[Seeker], time: float, has_detection: bool) -> None:
        self.prev_time = self.curr_time
        self.curr_time = time
        self.has_detection = has_detection
        self.phase_func[self.planner_phase](players)

    def __delay_launch(self, players) -> None:
        if self.curr_time < self.delay_launch_time or not self.has_detection:
            return
        next_phase = PlannerPhase.DELAY_LAUNCH.value + 1
        self.planner_phase = PlannerPhase(next_phase)
        self.phase_func[self.planner_phase](players)

    def __set_first_path(self, players: list[Seeker]):
        self.players_base = players[0].location
        self.__set_destination_to_circle(players)
        self.planner_phase = PlannerPhase(self.planner_phase.value + 1)
        for p in players:
            self.player_phase[p] = PlayerPhase.HEADED_TO_CIRCLE

    def __on_air(self, players: list[Seeker]):
        for p in players:
            if self.player_phase[p] is PlayerPhase.HEADED_TO_CIRCLE:
                x1, y1 = self.roi.location.x, self.roi.location.y
                x2, y2 = x1 + self.roi.width, y1 + self.roi.height
                if not utils.point_in_roi(p.location, x1, x2, y1, y2) and p.state != Seeker.State.CATCH:
                    p.halt()
                if p.destination is not None and p.destination.arrived:
                    self.player_phase[p] = PlayerPhase.AROUND_THE_CIRCLE
            if self.player_phase[p] is PlayerPhase.AROUND_THE_CIRCLE and p.state != Seeker.State.CATCH:
                p.steer(dt=self.curr_time-self.prev_time, direction=Seeker.Steer.LEFT)
                p.observation_direction = p.speed.angle

    def __calc_frontal_line_for_circle_centers(self, turn_radius: float, group_num: int):
        x = (self.roi.location.x + self.roi.width - turn_radius * (1 + ((group_num - 1) * 6)))
        p1_lower = Vec2D(x=x, y=(self.roi.location.y + turn_radius*2))
        p2_upper = Vec2D(x=x, y=(self.roi.location.y + self.roi.height - turn_radius*2))
        return p1_lower, p2_upper

    def __set_destination_to_circle(self, players: list[Seeker]):
        p1, p2 = self.__calc_frontal_line_for_circle_centers(players[0].turn_radius, players[0].group_num)
        middle_points = p1.points_between(other=p2, num_points=len(players))
        for player, loc in zip(players, middle_points):
            player.set_destination(dst=loc, new_speed=player.physical_specs.cruise_speed)
            player.observation_direction = player.speed.angle

    @staticmethod
    def __starting_phase(delay_launch_time, delay_launch_detection):
        if delay_launch_time > 0 or delay_launch_detection:
            return PlannerPhase.DELAY_LAUNCH
        return PlannerPhase.SET_FIRST_PATH
