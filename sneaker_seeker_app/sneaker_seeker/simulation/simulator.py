import math
from pathlib import Path
from typing import Optional
import numpy as np

from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.point2d import Point2D
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.ROI import ROI
from sneaker_seeker.game_obj.DKIZ import DKIZ
from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.visualization.visualizer import Visualizer


class Simulator:
    def __init__(self, out_path: Path, scenario: dict, visualizer: Visualizer, path_planners: dict[type, PathPlanner],
                 roi: ROI, dkiz: DKIZ, seekers: list[Seeker], sneakers: list[Sneaker]) -> None:
        self.out_path: Path = out_path
        self.scenario = scenario
        self.visualizer = visualizer
        self.path_planners = path_planners
        self.roi = roi
        self.dkiz = dkiz
        self.seekers = seekers
        self.sneakers = sneakers
        self.players = list(seekers + sneakers)
        self.__set_initial_deployment()

    def __set_players_path(self):
        for player in self.players:
            self.path_planners[type(player)].set_path(player)

    def __move_objects(self, dt: int):
        self.dkiz.move(dt)
        for player in self.players:
            player.move(dt)

    def __visualize_board(self, curr_time: int) -> 'Simulator':
        self.visualizer.time_stamp(curr_time)
        self.visualizer.make_ROI(self.roi)
        self.visualizer.make_DKIZ(self.dkiz)
        for seeker in self.seekers:
            self.visualizer.make_seeker(seeker)
        for sneaker in self.sneakers:
            self.visualizer.make_sneaker(sneaker)

    def __step(self, curr_time: int, should_record_step: bool = True) -> None:
        self.__set_players_path()
        self.__move_objects(dt=self.scenario["time_step_ms"] / 1000)
        self.__check_for_detections()
        if should_record_step:
            self.__visualize_board(curr_time)
            step_full_name = utils.append_time_to_path(self.out_path, curr_time)
            self.visualizer.save(step_full_name)

    def run(self, save_frame_every_n_step: int) -> None:
        curr_time = 0
        time_step, time_goal = self.scenario["time_step_ms"], self.scenario["time_goal_ms"]
        while curr_time <= time_goal:
            self.__step(curr_time, should_record_step=curr_time % (time_step * save_frame_every_n_step) == 0)
            curr_time += time_step

    def __check_for_detections(self):
        still_unknown_sneakers = [s for s in self.sneakers if s.is_undetected()]
        for sneaker in still_unknown_sneakers:
            for seeker in self.seekers:
                if seeker.can_see(sneaker.location):
                    sneaker.detect()
        return any([s.is_detected() for s in still_unknown_sneakers])

    def __calc_pip(self, target: DKIZ, friendly: Seeker) -> Optional[Point2D]:
        dist2d: Point2D = target.location - friendly.location
        relative_speed_vec: Vec2D = target.speed
        dt_until_pip = self.__aim_ahead(dist2d, relative_speed_vec, friendly.speed.magnitude)
        return target.location + Point2D(*(target.speed * dt_until_pip).to_cartesian()) if dt_until_pip > 0 else None

    def __aim_ahead(self, dist: Point2D, relative_speed_vec: Vec2D, friendly_speed_magnitude: float):
        # Quadratic equation coefficients a*t^2 + b*t + c = 0
        a = relative_speed_vec.magnitude ** 2 - friendly_speed_magnitude ** 2
        b = 2 * (relative_speed_vec.vx * dist.x + relative_speed_vec.vy * dist.y)
        c = (dist.x ** 2 + dist.y ** 2)

        desc = b ** 2 - 4 * a * c

        # If the discriminant is negative, then there is no solution
        if desc < 0:
            return -1

        return (2 * c) / (math.sqrt(desc) - b)

    def __set_initial_deployment(self):
        min_dist = self.sneakers[0].physical_specs.min_dist_between_eachother
        points = self.dkiz.generate_points_inside(num_of_points=len(self.sneakers), min_dist_between=min_dist)
        self.dkiz.speed = Vec2D(**self.scenario["sneaker"]["speed"])
        for sneaker, point in zip(self.sneakers, points):
            sneaker.location = point
            sneaker.speed = Vec2D(**self.scenario["sneaker"]["speed"])

        for seeker in self.seekers:
            pip = self.__calc_pip(self.dkiz, seeker)
            seeker.steer(pip if pip else Point2D(x=0, y=0))
            seeker.observation_direction = seeker.speed.direction
