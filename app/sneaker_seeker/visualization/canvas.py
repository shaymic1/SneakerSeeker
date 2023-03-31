from pathlib import Path
from typing import Union
import matplotlib.pyplot as plt


class Canvas:
    def __init__(self, height: int, width: int, margin: int, name: str,
                 xlabel: str, ylabel: str, figsize: int) -> None:
        self.height = height
        self.width = width
        self.fig, self.ax = self.__make_fig(figsize)
        self.margin = margin
        self.name = name
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.__init()


    @staticmethod
    def __make_fig(figsize) -> Union[any, plt.Axes]:
        fig = plt.figure(figsize=(figsize, figsize))
        return fig, fig.add_subplot(1, 1, 1)

    def __init(self) -> None:
        self.ax.cla()
        self.ax.set_title(self.name)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.set_xlim([-self.margin, self.width+self.margin])
        self.ax.set_ylim([-self.margin, self.height+self.margin])

    def show(self) -> None:
        plt.show()

    def save(self, path: Path):
        plt.savefig(path)

    def clean(self):
        self.__init()