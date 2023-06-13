from __future__ import annotations
from typing import Union
from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.utilities import utils


class PathPlannerHeuristic(PathPlanner):
    def __init__(self, dkiz: DKIZ, roi: ROI, offset_from_ends_dkiz_frontal_line: float,
                 delay_launch_time: float, **_ignore) -> None:
        self.dkiz: DKIZ = dkiz
        self.roi: ROI = roi
        self.offset_from_ends_dkiz_frontal_line = offset_from_ends_dkiz_frontal_line
        self.delay_launch_time: float = delay_launch_time
        self.player_finish_phase1: dict[float, bool] = {}
        self.should_set_first_path = True

    def set_path(self, players: list[Union[Sneaker, Seeker]], time:float) -> None:
        if time < self.delay_launch_time:
            return

        if self.should_set_first_path:
            self.__set_destination_to_frontal_dkiz_line(players)
            self.player_finish_phase1 = {p: False for p in players}
            self.should_set_first_path = False

        for player in [p for p in players if not self.player_finish_phase1[p]]:
            if not utils.point_in_roi(player.location, self.roi) and player.state != Seeker.State.CATCH:
                player.stop()
            if player.destination.arrived:
                player.speed.angle = utils.calc_angle(x=-self.dkiz.speed.x, y=-self.dkiz.speed.y)
                player.observation_direction = player.speed.angle
                self.player_finish_phase1[player] = True

    def __set_destination_to_frontal_dkiz_line(self, players: list[Union[Sneaker, Seeker]]):
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
