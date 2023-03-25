import matplotlib as plt

from sneaker_seeker.scenario import Scenario
from sneaker_seeker.players.seeker import Seeker


class Simulator:
    def __init__(self, scenario: Scenario) -> None:
        self.scenario = scenario
        self.fig, self.axs = Simulator.__make_fig()


    def step(self, seekers: list[Seeker]):
        pass



    @staticmethod
    def __make_fig(self):
        fig = plt.figure(figsize=(15, 15))
        ax1 = fig.add_subplot(1, 1, 1)
        axs = [ax1]
        return fig, axs


if __name__ == "__main__":
    ax.cla()
    ax.set_title(f'SneakerSeeker')

    # Create a Rectangle patch, represents the map boundaries
    boundaries = plt.patches.Rectangle((0, 0), self.scenario.board_width, self.scenario.board_height,
                                              linewidth=1, edgecolor='grey', facecolor='none')

    ax.set_xlim([-Configuration.world_plot_margin,
                 Configuration.WORLD_SIZE_X + Configuration.world_plot_margin])
    ax.set_ylim([-Configuration.world_plot_margin, Configuration.WORLD_SIZE_Y + Configuration.world_plot_margin])
