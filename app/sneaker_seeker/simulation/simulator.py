from pathlib import Path

from sneaker_seeker import utils
from sneaker_seeker.game_obj.roi import Roi
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.visualization.visualizer import Visualizer



class Simulator:
    def __init__(self, scenario: dict, visualizer: Visualizer,
                 seekers: list[Seeker], sneakers: list[Sneaker]) -> None:
        self.scenario = scenario
        self.visualizer = visualizer
        self.seekers = seekers
        self.sneakers = sneakers

    def __visualize_board(self) -> 'Simulator':
        self.visualizer.clean()
        self.visualizer.make_roi(Roi(**self.scenario["roi"]))
        for seeker in self.seekers:
            self.visualizer.make_seeker(seeker)
        for sneaker in self.sneakers:
            self.visualizer.make_sneaker(sneaker)

    def step(self, out_path: Path, curr_time: int) -> None:
        self.__visualize_board()
        fig_full_name = utils.append_time_to_path(out_path, curr_time)
        self.visualizer.save(fig_full_name)

    def run(self, out_path: Path) -> None:
        curr_time = 0
        time_step = self.scenario["time_step_ms"]
        while curr_time <= self.scenario["time_goal_ms"]:
            self.step(out_path, curr_time)
            curr_time += time_step

