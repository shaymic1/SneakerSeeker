from pathlib import Path

from sneaker_seeker import utils
from sneaker_seeker.game_obj.roi import Roi
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.visualization.visualizer import Visualizer


class Simulator:
    def __init__(self, out_path: Path, scenario: dict, visualizer: Visualizer, path_planners: dict[type, PathPlanner],
                 roi: Roi, seekers: list[Seeker], sneakers: list[Sneaker]) -> None:
        self.out_path: Path = out_path
        self.scenario = scenario
        self.visualizer = visualizer
        self.path_planners = path_planners
        self.roi = roi
        self.seekers = seekers
        self.sneakers = sneakers
        self.players = list(seekers + sneakers)

    def __set_players_path(self):
        for player in self.players:
            self.path_planners[type(player)].set_path(player)

    def __move_players(self, dt: int):
        for player in self.players:
            player.move(dt)

    def __visualize_board(self, curr_time: int) -> 'Simulator':
        self.visualizer.clean()
        self.visualizer.time_stamp(curr_time)
        self.visualizer.make_roi(self.roi)
        for seeker in self.seekers:
            self.visualizer.make_seeker(seeker)
        for sneaker in self.sneakers:
            self.visualizer.make_sneaker(sneaker)

    def __step(self, curr_time: int, should_record_step: bool = True) -> None:
        self.__set_players_path()
        self.__move_players(dt=self.scenario["time_step_ms"] / 1000)
        self.__check_for_detections()
        self.__visualize_board(curr_time)
        if should_record_step:
            step_full_name = utils.append_time_to_path(self.out_path, curr_time)
            self.visualizer.save(step_full_name)

    @utils.my_timer
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
