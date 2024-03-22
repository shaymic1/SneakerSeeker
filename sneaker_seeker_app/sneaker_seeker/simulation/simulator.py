from pathlib import Path
from typing import Tuple, Any, Optional

from sneaker_seeker.common_types.result import Results
from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.utilities import utils
from sneaker_seeker.visualization.visualizer import Visualizer


class Simulator:
    def __init__(self, out_path: Path, visualizer: Visualizer, path_planners: dict[type, list[PathPlanner]],
                 deployers: dict[type, list[Deployer]], roi: ROI, dkiz: DKIZ, seekers: list[list[Seeker]],
                 sneakers: list[list[Sneaker]]) -> None:
        self.out_path: Path = out_path
        self.visualizer: Visualizer = visualizer
        self.path_planners: dict[type, list[PathPlanner]] = path_planners
        self.deployers: dict[type, list[Deployer]] = deployers
        self.roi: ROI = roi
        self.dkiz: DKIZ = dkiz
        self.seekers: list[list[Seeker]] = seekers
        self.sneakers: list[(int, list[Sneaker])] = sneakers
        self.seekers_group_num = [s.group_num for s in utils.flat(seekers)]
        self.sneakers_group_num = [s.group_num for s in utils.flat(sneakers)]
        self.results: Results = Results(seeker_start=utils.ll_count(self.seekers),
                                        sneaker_start=utils.ll_count(self.sneakers))
        self.last_group_detection_idx = -1
        self.keep_running = True
        self.visulizer_on = True

    def __deploy_players(self):
        for i, seeker_group in enumerate(self.seekers):
            self.deployers[Seeker][i].deploy(seeker_group)
        for i, sneaker_group in enumerate(self.sneakers):
            self.deployers[Sneaker][i].deploy(sneaker_group)

    def __set_players_next_location(self, curr_time):
        for i, (group_num, seeker_group) in enumerate(zip(self.seekers_group_num, self.seekers)):
            self.path_planners[Seeker][i].set_path(seeker_group, curr_time, self.should_launch(group_num))
        for i, (group_num, sneaker_group) in enumerate(zip(self.sneakers_group_num, self.sneakers)):
            self.path_planners[Sneaker][i].set_path(sneaker_group, curr_time, self.should_launch(group_num))

    def __advance_objects(self, dt: float):
        self.dkiz.advance(dt)
        for sneaker in utils.flat(self.sneakers):
            sneaker.advance(dt)
        for seeker in utils.flat(self.seekers):
            seeker.advance(dt)

    def __visualize_board(self, curr_time: float) -> None:
        self.visualizer.parameters_stamp(curr_time, utils.ll_count(self.seekers), utils.ll_count(self.sneakers))
        self.visualizer.make_ROI(self.roi)
        self.visualizer.make_DKIZ(self.dkiz)
        for seeker in utils.flat(self.seekers):
            self.visualizer.make_seeker(seeker)
        for sneaker in utils.flat(self.sneakers):
            self.visualizer.make_sneaker(sneaker)

    def __step(self, curr_time: float, t_step: float, should_record_step: bool = True) -> None:
        self.__set_players_next_location(curr_time)
        self.__advance_objects(dt=t_step / 1000)
        if self.__is_new_detection_found():
            if assignments := self.__best_assignments():
                self.__set_assignments(assignments)
        self.__handle_catches()
        self.keep_running = self.__should_keep_run()
        if should_record_step or not self.keep_running:
            self.__visualize_board(curr_time)
            step_full_name = utils.append_time_to_path(self.out_path, curr_time)
            self.visualizer.save(step_full_name)

    def run(self, t_step: float, t_goal: float, save_frame_every_n_step: int = None,
            progress_bar_on: bool = True) -> Results:
        self.__initialize_board()
        self.visulizer_on = save_frame_every_n_step is not None
        t_curr = 0
        while t_curr <= t_goal and self.keep_running:
            if progress_bar_on:
                utils.progress_bar(progress=t_curr, total=t_goal)
            should_record_step = self.visulizer_on and (t_curr % (t_step * save_frame_every_n_step) == 0)
            self.__step(t_curr, t_step, should_record_step=should_record_step)
            t_curr += t_step
        self.results.seekers_left = utils.ll_count(self.seekers)
        self.results.sneaker_left = utils.ll_count(self.sneakers)
        return self.results

    def __is_new_detection_found(self) -> bool:
        rv = False
        for group_num, seeker_group in zip(self.seekers_group_num, self.seekers):
            for sneaker in self.__still_unknown_sneakers_for_this_group(group_num):
                for seeker in seeker_group:
                    if seeker.can_see(sneaker.location):
                        sneaker.state = Sneaker.State.DETECTED
                        sneaker.detected_by_seekers_group_numbers.append(group_num)
                        self.last_group_detection_idx = max(group_num, self.last_group_detection_idx)
                        self.first_detection = True
                        rv = True
        return rv

    def __initialize_board(self):
        self.__deploy_players()

    def __best_assignments(self) -> Optional[dict[Seeker, Tuple[Sneaker, Vec2D, float]]]:
        assignments = {}
        detected_sneakers = [s for s in utils.flat(self.sneakers) if s.state == Sneaker.State.DETECTED]
        for sneaker in detected_sneakers:
            seekers_time_for_collision: dict[Seeker, (Vec2D, float)] = {}
            for seeker in self.__available_seekers(sneaker.detected_by_seekers_group_numbers):
                if possible_result := utils.calc_possible_collision_point_and_time(sneaker.location, sneaker.speed,
                                                                                   seeker.location,
                                                                                   seeker.physical_specs.max_speed):
                    point, time = possible_result
                    if point.x > 0 and point.y > 0:
                        seekers_time_for_collision[seeker] = (point, time)

            if seekers_time_for_collision.keys().__len__() > 0:
                fastest_seeker = min(seekers_time_for_collision, key=lambda k: seekers_time_for_collision[k][1])
                point, time = seekers_time_for_collision[fastest_seeker]
                assignments[fastest_seeker] = (sneaker, point, time)
        if assignments.keys().__len__() > 0:
            return assignments
        return None

    def __handle_catches(self):
        for seeker in [s for s in utils.flat(self.seekers) if
                       s.destination and s.destination.arrived and s.state.CATCH]:
            for sneaker in utils.flat(self.sneakers):
                if seeker.location.distance_to(sneaker.location) <= seeker.catch_dist:
                    utils.remove_from_list_of_list(self.sneakers, sneaker)
                    utils.remove_from_list_of_list(self.seekers, seeker)
                    if self.visulizer_on:
                        self.visualizer.remove_player(sneaker)
                        self.visualizer.remove_player(seeker)

    def __should_keep_run(self) -> bool:
        if len(self.seekers) == 0 or len(self.sneakers) == 0:
            print(f"The ended with only {len(self.sneakers)} sneakers left.")
            return False
        return True

    @staticmethod
    def __set_assignments(assignments: dict[Seeker, Tuple[Sneaker, Vec2D, float]]):
        for seeker, (sneaker, point, time) in assignments.items():
            seeker.state = Seeker.State.CATCH
            seeker.form = Seeker.Form.DRONE
            sneaker.state = Sneaker.State.TARGETED
            seeker.set_destination(dst=point, new_speed=seeker.physical_specs.max_speed, arrival_time=time)

    def __available_seekers(self, possible_seeker_group_nums: list[int]) -> list[Seeker]:
        available_seekers = []
        for group_num, seeker_group in zip(self.seekers_group_num, self.seekers):
            if group_num in possible_seeker_group_nums:
                available_seekers.extend([s for s in seeker_group if s.state != Seeker.State.CATCH])
        return available_seekers

    def __still_unknown_sneakers_for_this_group(self, seeker_group_num) -> list[Sneaker]:
        still_unknown_sneakers = []
        for sneaker_group in self.sneakers:
            for sneaker in sneaker_group:
                if seeker_group_num not in sneaker.detected_by_seekers_group_numbers:
                    still_unknown_sneakers.append(sneaker)
        return still_unknown_sneakers

    def should_launch(self, group_num):
        is_my_front_group_detected_something = group_num - 1 <= self.last_group_detection_idx
        return is_my_front_group_detected_something
