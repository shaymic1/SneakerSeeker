import math
from pathlib import Path

import numpy as np

from sneaker_seeker.utilities import utils
from sneaker_seeker.common_types.point2d import Point2D
from sneaker_seeker.common_types.speed_vec import SpeedVec
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

    def __set_initial_deployment(self):
        min_dist = self.sneakers[0].physical_specs.min_dist_between_eachother
        points = self.points_inside_DKIZ(len(self.sneakers), self.dkiz, min_dist)
        self.dkiz.speed = SpeedVec(**self.scenario["sneaker"]["speed"])
        for sneaker, point in zip(self.sneakers, points):
            sneaker.location = point
            sneaker.speed = SpeedVec(**self.scenario["sneaker"]["speed"])

    def points_inside_DKIZ(self, num_of_points: int, dkiz: DKIZ, min_dist: float) -> list[Point2D]:
        chosen_points = []
        for _ in range(num_of_points):
            p = Point2D()
            while True:
                theta = np.random.uniform(0, 2 * np.pi)
                rho = np.random.uniform(0, self.dkiz.max_dist_from_center)
                dx_from_center_dkiz = rho * math.cos(theta)
                dy_from_center_dkiz = rho * math.sin(theta)
                p = Point2D(dx_from_center_dkiz, dy_from_center_dkiz) + self.dkiz.location
                if self.dkiz.contains(p) and not self.is_close_to_any_point(p, chosen_points, min_dist):
                    chosen_points.append(p)
                    break
        return chosen_points

    def is_close_to_any_point(self, p, chosen_points, min_dist):
        if len(chosen_points) == 0:
            return False
        return any([p.dist(chosen_p) < min_dist for chosen_p in chosen_points])
