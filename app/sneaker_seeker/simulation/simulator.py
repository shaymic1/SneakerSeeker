from pathlib import Path

from sneaker_seeker import utils
from sneaker_seeker.game_obj.roi import Roi
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.visualization.visualizer import Visualizer


class Simulator:
    def __init__(self, scenario: dict, visualizer: Visualizer, path_planners: dict[type, PathPlanner], roi: Roi,
                 seekers: list[Seeker], sneakers: list[Sneaker]) -> None:
        self.scenario = scenario
        self.visualizer = visualizer
        self.path_planners = path_planners
        self.roi = roi
        self.seekers = seekers
        self.sneakers = sneakers
        self.players = list(seekers + sneakers)

    def __set_players_direction_and_speed(self):
        for player in self.players:
            self.path_planners[type(player)].set_path(player)

    def __move_players(self, time_sec: int):
        for player in self.players:
            player.location.x += player.speed.vx * time_sec
            player.location.y += player.speed.vy * time_sec

    def __visualize_board(self, curr_time: int) -> 'Simulator':
        self.visualizer.clean()
        self.visualizer.time_stamp(curr_time)
        self.visualizer.make_roi(self.roi)
        for seeker in self.seekers:
            self.visualizer.make_seeker(seeker)
        for sneaker in self.sneakers:
            self.visualizer.make_sneaker(sneaker)

    def __step(self, out_path: Path, curr_time: int, should_record_step: bool = True) -> None:
        self.__set_players_direction_and_speed()
        self.__move_players(self.scenario["time_step_ms"]/1000)
        self.__visualize_board(curr_time)
        if should_record_step:
            fig_full_name = utils.append_time_to_path(out_path, curr_time)
            self.visualizer.save(fig_full_name)

    @utils.my_timer
    def run(self, out_path: Path, save_frame_every_n_step: int) -> None:
        curr_time = 0
        time_step = self.scenario["time_step_ms"]
        while curr_time <= self.scenario["time_goal_ms"]:
            self.__step(out_path, curr_time, should_record_step=curr_time % (time_step * save_frame_every_n_step) == 0)
            curr_time += time_step





