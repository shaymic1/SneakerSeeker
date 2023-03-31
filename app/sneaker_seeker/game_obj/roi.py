import matplotlib
from sneaker_seeker.simulation.canvas import Canvas
from sneaker_seeker.simulation.drawable import Drawable


class Roi(Drawable):
    def __init__(self, **kwargs) -> None:
        self.rectangle = matplotlib.patches.Rectangle(**kwargs, xy=(kwargs["x"], kwargs["y"]))

    def draw(self, canvas: Canvas):
        canvas.ax.add_patch(self.rectangle)
