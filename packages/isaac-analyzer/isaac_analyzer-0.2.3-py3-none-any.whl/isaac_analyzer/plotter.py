from isaac_analyzer.logging import getLogger
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch

logger = getLogger(__name__)


def plot_curses(curses: dict, title):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)

    total_curses = curses["Total curses"]
    overall = [curses["Total curses"], curses["No Curse"]]
    labels = ["Curse", "No Curse"]
    explode = [0.1, 0]
    angle = -45

    def func(pct, allvals):
        absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    wedges, *_ = ax1.pie(
        overall,
        autopct=lambda pct: func(pct, overall),
        startangle=angle,
        labels=labels,
        explode=explode,
        colors=["darkred", "darkgreen"],
        textprops={"color": "white"},
    )

    ax1.legend(loc="upper left")

    del curses["No Curse"]
    del curses["Total curses"]

    detail_values = [curses[key] / total_curses for key in curses.keys()]
    detail_labels = curses.keys()
    bottom = 1
    width = 0.2

    # Adding from the top matches the legend.
    for j, (height, label) in enumerate(reversed([*zip(detail_values, detail_labels)])):
        if height > 0:
            bottom -= height
            bc = ax2.bar(
                0,
                height,
                width,
                bottom=bottom,
                color="darkred",
                label=label,
                alpha=0.125 * j,
            )
            ax2.bar_label(
                bc, labels=[f"{height:.0%}"], label_type="center", color="white"
            )

    ax2.set_title("Curse Type")
    ax2.legend(loc="upper right", bbox_to_anchor=(1.25, 1))
    ax2.axis("off")
    ax2.set_xlim(-2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(detail_values)

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(
        xyA=(-width / 2, bar_height),
        coordsA=ax2.transData,
        xyB=(x, y),
        coordsB=ax1.transData,
    )
    con.set_color([0, 0, 0])
    con.set_linewidth(4)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(
        xyA=(-width / 2, 0), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData
    )
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(4)

    fig.suptitle(title, size="x-large", weight="bold")
    return fig
