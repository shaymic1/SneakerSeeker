import matplotlib as plt

def prepare_figure_and_axes_for_testing():
    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(2, 3, 1)
    axs = [ax1]
    return fig, axs




if __name__ == "__main__":
    fig, axs = prepare_figure_and_axes_for_testing()
    ax = axs[0]
    ax.cla()
    ax.set_title(f'SneakerSeeker')

    # Create a Rectangle patch, represents the map boundaries
    boundaries = plt.patches.Rectangle((0, 0), Configuration.WORLD_SIZE_X, Configuration.WORLD_SIZE_Y,
                                              linewidth=1, edgecolor='grey', facecolor='none')

    ax.set_xlim([-Configuration.world_plot_margin,
                 Configuration.WORLD_SIZE_X + Configuration.world_plot_margin])
    ax.set_ylim([-Configuration.world_plot_margin, Configuration.WORLD_SIZE_Y + Configuration.world_plot_margin])
