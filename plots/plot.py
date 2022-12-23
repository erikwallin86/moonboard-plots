import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


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


def plot_frequency(holds_sum_dict):
    fig, ax = plt.subplots(figsize=(8.82, 13.56))
    ax.set_aspect('equal')
    img = plt.imread("gpx/empty_moonboard_2016.png")
    ax.imshow(img, extent=(-1.9, 10+1.14, -1.28, 17+1.77))
    maximum = np.max(list(holds_sum_dict.values()))
    scale = 4e+3/maximum
    for description, value in holds_sum_dict.items():
        coords = desc_to_coords(description)
        if coords is not None:
            ax.scatter(coords[0], coords[1], s=scale*value, alpha=0.5, c='red')
    fig.tight_layout()
    plt.axis('off')
    fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    return fig, ax
