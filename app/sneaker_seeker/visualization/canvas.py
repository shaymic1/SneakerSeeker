from pathlib import Path
from typing import Union

import matplotlib
import matplotlib.pyplot as plt

from sneaker_seeker.visualization.visualizer import Visualizer
from sneaker_seeker.game_obj.roi import Roi
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.seeker import Seeker


class Canvas(Visualizer):
    def __init__(self, height: int, width: int, margin: int, name: str,
                 xlabel: str, ylabel: str, figsize: dict) -> None:
        self.height = height
        self.width = width
        self.fig, self.ax = self.__make_fig(**figsize)
        self.margin = margin
        self.name = name
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.__init()

    @staticmethod
    def __make_fig(width: int, height: int) -> Union[any, plt.Axes]:
        fig = plt.figure(figsize=(width, height))
        return fig, fig.add_subplot(1, 1, 1)

    def __init(self) -> None:
        self.ax.cla()
        self.fig.suptitle(self.name)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_xlim([-self.margin, self.width + self.margin])
        self.ax.set_ylim([-self.margin, self.height + self.margin])
        self.ax.set_aspect("auto", adjustable="box", anchor="C")

    def save(self, path: Path):
        plt.savefig(path)

    def clean(self):
        self.__init()

    def make_roi(self, roi: Roi):
        self.ax.add_patch(roi.rectangle)

    def time_stamp(self, curr_time):
        self.ax.set_title(f"time[sec]: {curr_time/1000:.1f}")

    def make_seeker(self, seeker: Seeker):
        self.ax.add_patch(
            matplotlib.patches.Wedge(center=(seeker.location.x, seeker.location.y), r=seeker.los,
                                     theta1=(seeker.direction - seeker.fov / 2),
                                     theta2=(seeker.direction + seeker.fov / 2),
                                     facecolor="blue", alpha=0.1))
        self.ax.plot(seeker.location.x, seeker.location.y,
                     marker=(3, 0, seeker.direction - 90),  # directed triangle
                     color="blue",
                     markersize=5, markerfacecolor="blue", alpha=.5)
        self.ax.plot(seeker.location.x, seeker.location.y,
                     marker=(2, 0, seeker.direction - 90),  # directed line
                     color="blue",
                     markersize=10, markerfacecolor="blue", alpha=.4)

    def make_sneaker(self, sneaker: Sneaker):
        self.ax.add_patch(
            matplotlib.patches.Wedge(center=(sneaker.location.x, sneaker.location.y), r=sneaker.los,
                                     theta1=(sneaker.direction - sneaker.fov / 2),
                                     theta2=(sneaker.direction + sneaker.fov / 2),
                                     facecolor="red", alpha=0.5 if sneaker.detected else 0.1))
        self.ax.plot(sneaker.location.x, sneaker.location.y,
                     marker=(3, 0, sneaker.direction - 90),  # directed triangle
                     color="red",
                     markersize=5, markerfacecolor="red", alpha=.5)
        self.ax.plot(sneaker.location.x, sneaker.location.y,
                     marker=(2, 0, sneaker.direction - 90),  # directed line
                     color="red",
                     markersize=10, markerfacecolor="red", alpha=.4)
