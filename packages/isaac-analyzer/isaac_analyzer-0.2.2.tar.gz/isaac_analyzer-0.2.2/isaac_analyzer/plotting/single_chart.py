from isaac_analyzer.logging import getLogger
import matplotlib.pyplot as plt
import numpy as np

logger = getLogger(__name__)


def hbars(values, labels, x_label, title):
    logger.info("Generating hbar chart")
    fig, plot = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize=(9, 5))

    y_pos = np.arange(len(labels))

    hbars = plot.barh(y_pos, values, align="center")
    plot.bar_label(hbars, label_type="center", fmt="%1.2f")
    plot.set_yticks(y_pos, labels=labels)
    plot.set_xlabel(x_label)
    fig.suptitle(title, size="x-large", weight="bold")
    return fig


def pie_chart(values, labels, colors, title):
    logger.info("Generating pie chart")
    fig, plot = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize=(9, 5))

    def func(pct, allvals):
        absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    plot.pie(
        values,
        labels=labels,
        colors=colors,
        autopct=lambda pct: func(pct, values),
        labeldistance=None,
    )

    plot.legend(loc="upper right", bbox_to_anchor=(1.25, 1))
    fig.suptitle(title, size="x-large", weight="bold")

    logger.debug("Pie chart figure created successfully")
    return fig
