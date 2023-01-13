import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import colorcet as cc
import matplotlib


def new_fig(nrows=1, ncols=1, **kwargs):
    """Create a new matplotlib figure containing one axis

    Return:
      (fig, ax) or (fig, list[ax])
    """
    fig = Figure(**kwargs)
    FigureCanvas(fig)
    if nrows == 1 and ncols == 1:
        # Create a single axis
        ax = fig.add_subplot(1, 1, 1)
        return fig, ax
    else:
        # Create a list of axes
        axs = [fig.add_subplot(nrows, ncols, index) for index in
               range(1, nrows*ncols+1)]
        return fig, axs


def add_grade_legend(ax, list_of_grades, cmap=cc.cm.rainbow):
    # Construct custom legend
    import matplotlib.lines as mlines
    handles = []
    for i, g in enumerate(list_of_grades):
        color = cmap(i/(len(list_of_grades)-1))
        marker = mlines.Line2D(
            [], [], marker='o', linestyle='None', label=g, color=color,
            markeredgewidth=0.5, markeredgecolor='k')
        handles.append(marker)
    ax.legend(handles=handles, loc='right', bbox_to_anchor=(1.2, 0.5))


number_to_letter_dict = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
}

letter_to_number_dict = {
    v: k for k, v in number_to_letter_dict.items()}


def desc_to_coords(desc):
    '''
    Parse description to coordinates starting from (0, 0) e.g. E6 -> (4, 5)
    '''
    # Separate letter and digits
    letter = desc[0]
    digits = int(desc[1:])
    # Return coordinates
    try:
        coordinates = (letter_to_number_dict[letter], digits-1)
    except KeyError:
        print(f"letter:{letter}")
        return None

    return coordinates


def plot_problem(list_of_moves):
    fig, ax = new_fig(figsize=(8.82, 13.56))
    ax.set_aspect('equal')
    img = plt.imread("gpx/empty_moonboard_2016.png")
    ax.imshow(img, extent=(-1.9, 10+1.14, -1.28, 17+1.77))

    for move in list_of_moves:
        desc = move.description
        coords = desc_to_coords(desc)
        if move.isStart:
            color = 'lime'
        elif move.isEnd:
            color = 'red'
        else:
            color = 'blue'

        if coords is not None:
            ax.scatter(
                *coords, s=3800, alpha=0.9, facecolors='none',
                edgecolors=color, linewidth=8)

    fig.tight_layout()
    plt.axis('off')
    fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)

    return fig, ax


def plot_frequency(holds_sum_dict, image_file="gpx/MoonBoard 2016 .png",
                   color='red'):
    fig, ax = new_fig(figsize=(8.82, 13.56))
    ax.set_aspect('equal')
    img = plt.imread(image_file)
    ax.imshow(img, extent=(-1.9, 10+1.14, -1.28, 17+1.77))
    maximum = np.max(list(holds_sum_dict.values()))
    scale = 4e+3/maximum
    for description, value in holds_sum_dict.items():
        coords = desc_to_coords(description)
        if coords is not None:
            ax.scatter(
                coords[0], coords[1], s=scale*value, alpha=0.5,
                color=color, edgecolors='black', linewidth=2)

    fig.tight_layout()
    plt.axis('off')
    fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    return fig, ax


def progression_plot(dates, num_problems, colors=None, suptitle=None):
    '''
    Benchmark progression plot: scatter of dates v num_problems
    '''
    # Create figure and axis
    fig, ax = new_fig()

    # Setup grid
    ax.set_axisbelow(True)
    ax.grid(which='minor', linewidth=0.5)
    ax.grid(which='major', linewidth=1.5)

    # Plot scatter plot
    ax.scatter(dates, num_problems, color=colors, edgecolors='k',
               linewidth=0.5)

    # Setup axis labels, tics etc.
    ax.set_xlabel('Date')
    ax.set_ylabel('Benchmark problems')
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
    if suptitle:
        fig.suptitle(suptitle)

    return fig, ax
