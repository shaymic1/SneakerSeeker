from pathlib import Path
from typing import Tuple, Any

from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.utilities import utils
from sneaker_seeker.visualization.visualizer import Visualizer


def flat(list_of_list: list[list[Any]]) -> list[Any]:
    return [e for inner_list in list_of_list for e in inner_list]


def remove_from_list_of_list(list_of_list: list[list[Any]], element):
    for inner_list in list_of_list:
        if element in inner_list:
            inner_list.remove(element)


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
        self.sneakers: list[list[Sneaker]] = sneakers
        self.keep_running = True

    def __deploy_players(self):
        for i, seeker_group in enumerate(self.seekers):
            self.deployers[Seeker][i].deploy(seeker_group)
        for i, sneaker_group in enumerate(self.sneakers):
            self.deployers[Sneaker][i].deploy(sneaker_group)

    def __set_players_next_location(self, curr_time):
        for i, seeker_group in enumerate(self.seekers):
            self.path_planners[Seeker][i].set_path(seeker_group, curr_time)
        for i, sneaker_group in enumerate(self.sneakers):
            self.path_planners[Sneaker][i].set_path(sneaker_group, curr_time)

    def __advance_objects(self, dt: float):
        self.dkiz.advance(dt)
        for sneaker in flat(self.sneakers):
            sneaker.advance(dt)
        for seeker in flat(self.seekers):
            seeker.advance(dt)

    def __visualize_board(self, curr_time: float) -> None:
        self.visualizer.parameters_stamp(curr_time, sum(len(s) for s in self.seekers),
                                         sum(len(s) for s in self.sneakers))
        self.visualizer.make_ROI(self.roi)
        self.visualizer.make_DKIZ(self.dkiz)
        for seeker in flat(self.seekers):
            self.visualizer.make_seeker(seeker)
        for sneaker in flat(self.sneakers):
            self.visualizer.make_sneaker(sneaker)

    def __step(self, curr_time: float, t_step: float, should_record_step: bool = True) -> None:
        self.__set_players_next_location(curr_time)
        self.__advance_objects(dt=t_step / 1000)
        if self.__is_new_detection_found():
            assignments = self.__best_assignments()
            self.__set_assignments(assignments)
        self.__handle_catches()
        self.keep_running = self.__should_keep_run()
        if should_record_step or not self.keep_running:
            self.__visualize_board(curr_time)
            step_full_name = utils.append_time_to_path(self.out_path, curr_time)
            self.visualizer.save(step_full_name)

    def run(self, t_step: float, t_goal: float, save_frame_every_n_step: int = 1) -> None:
        self.__initialize_board()
        t_curr = 0
        while t_curr <= t_goal and self.keep_running:
            utils.progress_bar(progress=t_curr, total=t_goal)
            self.__step(t_curr, t_step, should_record_step=t_curr % (t_step * save_frame_every_n_step) == 0)
            t_curr += t_step

    def __is_new_detection_found(self) -> bool:
        still_unknown_sneakers = [s for s in flat(self.sneakers) if s.state == Sneaker.State.UNDETECTED]
        for sneaker in still_unknown_sneakers:
            for seeker in flat(self.seekers):
                if seeker.can_see(sneaker.location):
                    sneaker.state = Sneaker.State.DETECTED
        return any([s.state == Sneaker.State.DETECTED for s in still_unknown_sneakers])

    def __initialize_board(self):
        self.__deploy_players()

    def __best_assignments(self) -> dict[Seeker, Tuple[Sneaker, Vec2D, float]]:
        assignments = {}
        for sneaker in [s for s in flat(self.sneakers) if s.state == Sneaker.State.DETECTED]:
            seekers_time_for_collision: dict[Seeker, (Vec2D, float)] = {}
            available_seekers = [s for s in flat(self.seekers) if s.state == Seeker.State.SEEK]
            for seeker in available_seekers:
                point, time = utils.calc_possible_collision_point_and_time(sneaker.location, sneaker.speed,
                                                                           seeker.location,
                                                                           seeker.physical_specs.max_speed)
                seekers_time_for_collision[seeker] = (point, time)
            fastest_seeker = min(seekers_time_for_collision, key=lambda k: seekers_time_for_collision[k][1])
            point, time = seekers_time_for_collision[fastest_seeker]
            assignments[fastest_seeker] = (sneaker, point, time)
        return assignments

    def __handle_catches(self):
        for seeker in [s for s in flat(self.seekers) if s.destination and s.destination.arrived and s.state.CATCH]:
            for sneaker in flat(self.sneakers):
                if seeker.location.distance_to(sneaker.location) <= seeker.catch_dist:
                    self.visualizer.remove_player(sneaker)
                    self.visualizer.remove_player(seeker)
                    remove_from_list_of_list(self.sneakers, sneaker)
                    remove_from_list_of_list(self.seekers, seeker)

    def __should_keep_run(self) -> bool:
        if len(self.seekers) == 0 or len(self.sneakers) == 0:
            print(f"The ended with only {len(self.sneakers)} sneakers left.")
            return False
        return True

    @staticmethod
    def __set_assignments(assignments: dict[Seeker, Tuple[Sneaker, Vec2D, float]]):
        for seeker, (sneaker, point, time) in assignments.items():
            seeker.set_destination(dst=point, new_speed=seeker.physical_specs.max_speed, arrival_time=time)
            seeker.state = Seeker.State.CATCH
            sneaker.state = Sneaker.State.TARGETED
