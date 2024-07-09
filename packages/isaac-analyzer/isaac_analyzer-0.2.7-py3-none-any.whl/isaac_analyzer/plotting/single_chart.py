from isaac_analyzer.logging import getLogger
import matplotlib.pyplot as plt
import numpy as np

from isaac_analyzer.utils import calculate_percentages

logger = getLogger(__name__)


def stacked_bar(
    buckets,
    values_bottom,
    values_upper,
    legend_bottom,
    legend_upper,
    color_bottom,
    color_upper,
    xLabel,
    yLabel,
    title,
):
    fig, plot = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize=(18, 5))

    percentage_bottom_1, percentage_upper_1 = calculate_percentages(
        values_bottom, values_upper, buckets
    )

    lower_bars_1 = plot.bar(
        buckets, values_bottom, label=legend_bottom, color=color_bottom
    )
    upper_bars_1 = plot.bar(
        buckets,
        values_upper,
        bottom=values_bottom,
        label=legend_upper,
        color=color_upper,
    )

    plot.set_xlabel(xLabel)
    plot.set_ylabel(yLabel)
    plot.legend()
    plot.tick_params(axis="x", labelrotation=90)
    # for label in plot.get_xticklabels():
    #     label.set(rotation=45)
    logger.debug("Plot1 created")

    for i in range(len(buckets)):
        if values_bottom[i] > 0:
            plot.annotate(
                f"{percentage_bottom_1[i]:.1f}%\n({values_bottom[i]})",
                xy=(
                    lower_bars_1[i].get_x() + lower_bars_1[i].get_width() / 2,
                    values_bottom[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
                fontsize=8,
            )
        if values_upper[i] > 0:
            plot.annotate(
                f"{percentage_upper_1[i]:.1f}%\n({values_upper[i]})",
                xy=(
                    upper_bars_1[i].get_x() + upper_bars_1[i].get_width() / 2,
                    values_bottom[i] + values_upper[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
                fontsize=8,
            )
    logger.debug("Annotations added to plot1")

    fig.suptitle(title, size="x-large", weight="bold")
    logger.debug("Figure created successfully")

    return fig


def hbars(values, labels, x_label, title):
    logger.info("Generating hbar chart")
    fig, plot = plt.subplots(nrows=1, ncols=1, layout="constrained", figsize=(9, 5))

    y_pos = np.arange(len(labels))

    hbars = plot.barh(y_pos, values, align="center")
    plot.bar_label(hbars, label_type="center", fmt="%1.2f", color="white")
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
        textprops={"color": "white"},
    )

    plot.legend(loc="upper right", bbox_to_anchor=(1.25, 1))
    fig.suptitle(title, size="x-large", weight="bold")

    logger.debug("Pie chart figure created successfully")
    return fig
