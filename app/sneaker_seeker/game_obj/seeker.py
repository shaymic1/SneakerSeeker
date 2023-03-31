import matplotlib
import numpy as np

from sneaker_seeker.common_types import Location, Speed
from sneaker_seeker.players.player import Player
from sneaker_seeker.simulation.canvas import Canvas


class Seeker(Player):

    def __init__(self, location: dict, speed: dict, direction: float = None,
                 los: float = 1000, fov: float = 60) -> None:
        super().__init__(location, speed, direction, los, fov)

    def draw(self, canvas: Canvas):
        canvas.ax.add_patch(
            matplotlib.patches.Wedge(center=(self.location.x, self.location.y), r=self.los,
                                     theta1=(self.direction - self.fov / 2),
                                     theta2=(self.direction + self.fov / 2),
                                     facecolor="blue", alpha=0.1))
        canvas.ax.plot(self.location.x, self.location.y,
                marker=(3, 0, self.direction - 90),  # directed triangle
                color="blue",
                markersize=5, markerfacecolor="blue", alpha=.5)
        canvas.ax.plot(self.location.x, self.location.y,
                marker=(2, 0, self.direction-90),  # directed line
                color="blue",
                markersize=10, markerfacecolor="blue", alpha=.4)