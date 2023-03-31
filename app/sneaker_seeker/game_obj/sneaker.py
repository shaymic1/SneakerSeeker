import matplotlib

from sneaker_seeker.players.player import Player
from sneaker_seeker.simulation.canvas import Canvas


class Sneaker(Player):

    def __init__(self, location: dict, speed: dict, direction: float = None,
                 los: float = 100, fov: float = 180) -> None:
        super().__init__(location, speed, direction, los, fov)
        self.detected = False
        self.id = None

    def draw(self, canvas: Canvas):
        canvas.ax.add_patch(
            matplotlib.patches.Wedge(center=(self.location.x, self.location.y), r=self.los,
                                     theta1=(self.direction - self.fov / 2),
                                     theta2=(self.direction + self.fov / 2),
                                     facecolor="red", alpha=0.5 if self.detected else 0.1))
        canvas.ax.plot(self.location.x, self.location.y,
                       marker=(3, 0, self.direction - 90),  # directed triangle
                       color="red",
                       markersize=5, markerfacecolor="red", alpha=.5)
        canvas.ax.plot(self.location.x, self.location.y,
                       marker=(2, 0, self.direction-90),  # directed line
                       color="red",
                       markersize=10, markerfacecolor="red", alpha=.4)
