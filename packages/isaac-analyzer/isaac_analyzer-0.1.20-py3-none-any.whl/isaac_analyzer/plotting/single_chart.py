from isaac_analyzer.logging import getLogger
import matplotlib.pyplot as plt
import numpy as np

logger = getLogger(__name__)


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
