from pathlib import Path
from typing import Union, Tuple, Optional
from dataclasses import dataclass

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.text import Text

from sneaker_seeker.game_obj.player import Player
from sneaker_seeker.visualization.visualizer import Visualizer
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.common_types.destination import Destination


def circle_dkiz_updater(dkiz_patch: matplotlib.patches, dkiz: DKIZ) -> None:
    dkiz_patch[0].set_center((dkiz.location.x, dkiz.location.y))
    dkiz_patch[1].set_data([dkiz.l_frontal_line.location.x, dkiz.r_frontal_line.location.x],
                           [dkiz.l_frontal_line.location.y, dkiz.r_frontal_line.location.y])


def circle_dkiz_creator(ax: plt.Axes, dkiz: DKIZ, appearance: dict) -> Tuple[matplotlib.patches.Circle, plt.Line2D]:
    circle = ax.add_patch(matplotlib.patches.Circle(xy=(dkiz.location.x, dkiz.location.y),
                                                    **dkiz.dimensions, **appearance["inner_circle"]))
    line_x_data = [dkiz.l_frontal_line.location.x, dkiz.r_frontal_line.location.x]
    line_y_data = [dkiz.l_frontal_line.location.y, dkiz.r_frontal_line.location.y]
    line: list[plt.Line2D] = ax.plot(line_x_data, line_y_data, **appearance["frontal_line"])
    return circle, line[0]


PlayerCanvasObj = Tuple[matplotlib.patches.Wedge, plt.Line2D, plt.Line2D]
DKIZCanvasObj = Tuple[Union[matplotlib.patches.Circle, any], plt.Line2D]
ROICanvasObj = matplotlib.patches.Rectangle
CanvasObj = Union[PlayerCanvasObj, DKIZCanvasObj, ROICanvasObj]


class Canvas(Visualizer):
    @dataclass
    class Texts:
        title: Text
        seeker_num: Text
        sneaker_num: Text
        scenario_time: Text

    __dkiz_shape_creator: dict[str, callable] = {"circle": circle_dkiz_creator}
    __dkiz_shape_updater: dict[str, callable] = {"circle": circle_dkiz_updater}

    def __init__(self, height: int, width: int, margin: int, name: str, x_label: str, y_label: str, fig_size: dict,
                 object_appearance: dict, frame_format: str = "jpg") -> None:
        self.height = height
        self.width = width
        self.fig, self.ax = self.__make_fig(**fig_size)
        self.margin = margin
        self.name = name
        self.frame_format = frame_format
        self.x_label = x_label
        self.y_label = y_label
        self.object_appearance: dict = object_appearance
        self.objects: dict[int, CanvasObj] = {}
        self.objects_pip: dict[int, Tuple[plt.Line2D, Destination]] = {}
        self.texts = self.__init()

    @staticmethod
    def __make_fig(width: int, height: int) -> Union[any, plt.Axes]:
        fig = plt.figure(figsize=(width, height))
        return fig, fig.add_subplot(1, 1, 1)

    def __init(self) -> Texts:
        self.ax.cla()
        self.ax.set_aspect('equal')
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.set_xlim([-self.margin, self.width + self.margin])
        self.ax.set_ylim([-self.margin, self.height + self.margin])
        self.ax.set_aspect("auto", adjustable="box", anchor="C")
        return Canvas.Texts(
            title=self.ax.text(self.width * 0.5, self.height * 1.1, self.name, ha='center', fontsize=20),
            seeker_num=self.ax.text(self.width * 0.05, self.height * 1.03, f"Seekers: ", color="blue", fontsize=20),
            sneaker_num=self.ax.text(self.width * 0.8, self.height * 1.03, f"Sneaker: ", color="red", fontsize=20),
            scenario_time=self.ax.text(self.width * 0.5, self.height * 1.03, f"Time[sec]: ", fontsize=15, ha='center')
        )

    def save(self, path: Path) -> None:
        self.fig.savefig(f"{path}.{self.frame_format}",
                         format="jpeg" if self.frame_format == "jpg" else self.frame_format)

    def __make_player(self, player: Union[Sneaker, Seeker], appearance: dict) -> PlayerCanvasObj:
        wedge = self.ax.add_patch(
            matplotlib.patches.Wedge(center=(player.location.x, player.location.y), r=player.los,
                                     theta1=(player.observation_direction - player.fov / 2),
                                     theta2=(player.observation_direction + player.fov / 2),
                                     **appearance["wedge"]))
        triangle: list[plt.Line2D] = self.ax.plot(player.location.x, player.location.y,
                                                  marker=(3, 0, player.speed.angle - 90),  # directed triangle
                                                  **appearance["triangle"])
        line: list[plt.Line2D] = self.ax.plot(player.location.x, player.location.y,
                                              marker=(2, 0, player.speed.angle - 90),  # directed line
                                              **appearance["line"])
        return wedge, triangle[0], line[0]

    def __update_player(self, player: Union[Sneaker, Seeker], appearance: dict) -> None:
        player_canvas_obj: PlayerCanvasObj = self.objects[player.id]
        player_canvas_obj[0].set_center((player.location.x, player.location.y))
        player_canvas_obj[0].set_theta1(player.observation_direction - player.fov / 2)
        player_canvas_obj[0].set_theta2(player.observation_direction + player.fov / 2)
        player_canvas_obj[0].set_facecolor(appearance["wedge"]["facecolor"])
        player_canvas_obj[0].set_alpha(appearance["wedge"]["alpha"])
        player_canvas_obj[1].set_data([player.location.x], [player.location.y])
        player_canvas_obj[1].set_marker((3, 0, player.speed.angle - 90))  # set triangle angle
        player_canvas_obj[1].set_color(appearance["triangle"]["color"])
        player_canvas_obj[1].set_alpha(appearance["triangle"]["alpha"])
        player_canvas_obj[2].set_data([player.location.x], [player.location.y])
        player_canvas_obj[2].set_marker((2, 0, player.speed.angle - 90))  # set line angle
        player_canvas_obj[2].set_color(appearance["line"]["color"])
        player_canvas_obj[2].set_alpha(appearance["line"]["alpha"])

    def __update_pip(self, player, appearance):
        pip_obj, dst = self.objects_pip[player.id]
        pip_obj.set_data([player.destination.location.x], [player.destination.location.y])
        pip_obj.set_color(appearance["color"])
        pip_obj.set_markersize(appearance["markersize"])
        pip_obj.set_marker(appearance["marker"])

    def __remove_pip(self, seeker):
        pip_obj, dst = self.objects_pip.get(seeker.id)
        pip_obj.set_data([0], [0])

    def __create_pip(self, player, appearance):
        pip_obj = self.ax.plot(player.destination.location.x, player.destination.location.y, **appearance)[0]
        self.objects_pip[player.id] = (pip_obj, player.destination)

    def __print_pip(self, player, appearance):
        if player.destination and not player.destination.arrived:
            if player.id not in self.objects_pip:
                self.__create_pip(player=player, appearance=appearance)
            else:
                pip_obj, dst = self.objects_pip[player.id]
                if dst != player.destination:
                    self.__update_pip(player=player, appearance=appearance)
        if player.destination and player.destination.arrived:
            self.__remove_pip(player)

    def __print_player_to_canvas(self, player: Union[Sneaker, Seeker],
                                 appearance: dict) -> None:
        if player.id not in self.objects:
            self.objects[player.id] = self.__make_player(player, appearance)
        else:
            self.__update_player(player=player, appearance=appearance)

    def make_seeker(self, seeker: Seeker) -> None:
        appearance = self.object_appearance["seeker"][seeker.state.lower()]
        self.__print_player_to_canvas(seeker, appearance)
        self.__print_pip(player=seeker, appearance=appearance["pip"])

    def make_sneaker(self, sneaker: Sneaker) -> None:
        appearance = self.object_appearance["sneaker"][sneaker.state.lower()]
        self.__print_player_to_canvas(sneaker, appearance)

    def make_ROI(self, roi: ROI) -> None:
        self.ax.add_patch(matplotlib.patches.Rectangle(xy=(roi.location.x, roi.location.y),
                                                       width=roi.width,
                                                       height=roi.height,
                                                       **self.object_appearance["roi"]))

    def make_DKIZ(self, dkiz: DKIZ) -> None:
        dkiz_canvas_obj: Union[matplotlib.patches.Circle, any] = self.objects.get(dkiz.id)
        if dkiz_canvas_obj is None:  # create new object
            self.objects[dkiz.id] = Canvas.__dkiz_shape_creator[dkiz.type](ax=self.ax, dkiz=dkiz,
                                                                           appearance=self.object_appearance["dkiz"])
        else:  # update existing object
            Canvas.__dkiz_shape_updater[dkiz.type](dkiz_canvas_obj, dkiz)

    def parameters_stamp(self, curr_time, num_seekers: int, num_sneakers: int) -> None:
        self.texts.scenario_time.set_text(f"time[sec]: {curr_time / 1000:.1f}")
        self.texts.seeker_num.set_text(f"Seekers: {num_seekers}")
        self.texts.sneaker_num.set_text(f"Sneakers: {num_sneakers}")

    def remove_player(self, player: Player) -> None:
        player_canvas_obj: Optional[PlayerCanvasObj] = self.objects.get(player.id)
        player_canvas_obj[0].remove()
        player_canvas_obj[1].remove()
        player_canvas_obj[2].remove()
