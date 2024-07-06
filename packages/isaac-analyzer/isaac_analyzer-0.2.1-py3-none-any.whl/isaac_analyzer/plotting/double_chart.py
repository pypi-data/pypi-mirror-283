import numpy as np
from isaac_analyzer.logging import getLogger
import matplotlib.pyplot as plt

logger = getLogger(__name__)


def calculate_percentages(values_bottom, values_upper, buckets):
    totals = [values_bottom[i] + values_upper[i] for i in range(len(buckets))]
    percentage_bottom = [
        values_bottom[i] / totals[i] * 100 if totals[i] != 0 else 0
        for i in range(len(buckets))
    ]
    percentage_upper = [
        values_upper[i] / totals[i] * 100 if totals[i] != 0 else 0
        for i in range(len(buckets))
    ]
    return percentage_bottom, percentage_upper


def pie_hbar_chart(
    values_1,
    labels_1,
    colors_1,
    title_1,
    values_2,
    labels_2,
    x_label_2,
    title_2,
    title,
):
    fig, plots = plt.subplots(nrows=1, ncols=2, layout="constrained", figsize=(9, 5))

    ### Plot1
    plot_1 = plots[0]
    logger.debug("Creating plot1")

    def func(pct, allvals):
        absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    plot_1.pie(
        values_1,
        labels=labels_1,
        colors=colors_1,
        autopct=lambda pct: func(pct, values_1),
        labeldistance=None,
    )

    plot_1.set_title(title_1)
    plot_1.legend(loc="upper right")
    logger.debug("plot2 created")

    fig.suptitle(title, size="x-large", weight="bold")
    logger.debug("Figure created successfully")

    plot_2 = plots[1]

    y_pos = np.arange(len(labels_2))

    hbars = plot_2.barh(y_pos, values_2, align="center")
    plot_2.bar_label(hbars, label_type="center", fmt="%1.2f")
    plot_2.set_yticks(y_pos, labels=labels_2)
    plot_2.set_xlabel(x_label_2)
    plot_2.set_title(title_2)

    return fig


def stacked_bar_pie_chart(
    buckets_1,
    values_bottom_1,
    values_upper_1,
    legend_bottom_1,
    legend_upper_1,
    color_bottom_1,
    color_upper_1,
    xLabel_1,
    yLabel_1,
    title_1,
    values_2,
    labels_2,
    colors_2,
    title_2,
    title,
):
    fig, plots = plt.subplots(nrows=1, ncols=2, layout="constrained", figsize=(9, 5))

    percentage_bottom_1, percentage_upper_1 = calculate_percentages(
        values_bottom_1, values_upper_1, buckets_1
    )

    # Plot1
    plot_1 = plots[0]
    logger.debug("Creating plot1")

    lower_bars_1 = plot_1.bar(
        buckets_1, values_bottom_1, label=legend_bottom_1, color=color_bottom_1
    )
    upper_bars_1 = plot_1.bar(
        buckets_1,
        values_upper_1,
        bottom=values_bottom_1,
        label=legend_upper_1,
        color=color_upper_1,
    )

    plot_1.set_xlabel(xLabel_1)
    plot_1.set_ylabel(yLabel_1)
    plot_1.set_title(title_1)
    plot_1.legend()
    logger.debug("Plot1 created")

    for i in range(len(buckets_1)):
        if values_bottom_1[i] > 0:
            plot_1.annotate(
                f"{percentage_bottom_1[i]:.1f}%",
                xy=(
                    lower_bars_1[i].get_x() + lower_bars_1[i].get_width() / 2,
                    values_bottom_1[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
            )
        if values_upper_1[i] > 0:
            plot_1.annotate(
                f"{percentage_upper_1[i]:.1f}%",
                xy=(
                    upper_bars_1[i].get_x() + upper_bars_1[i].get_width() / 2,
                    values_bottom_1[i] + values_upper_1[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
            )
    logger.debug("Annotations added to plot1")

    ### Plot2
    ### Deals plot
    plot_2 = plots[1]
    logger.debug("Creating plot2")

    def func(pct, allvals):
        absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"

    plot_2.pie(
        values_2,
        labels=labels_2,
        colors=colors_2,
        autopct=lambda pct: func(pct, values_2),
        labeldistance=None,
    )

    plot_2.set_title(title_2)
    plot_2.legend(loc="upper right")
    logger.debug("plot2 created")

    fig.suptitle(title, size="x-large", weight="bold")
    logger.debug("Figure created successfully")

    return fig


def double_stacked_bar_chart(
    buckets_1,
    values_bottom_1,
    values_upper_1,
    legend_bottom_1,
    legend_upper_1,
    color_bottom_1,
    color_upper_1,
    xLabel_1,
    yLabel_1,
    title_1,
    buckets_2,
    values_bottom_2,
    values_upper_2,
    legend_bottom_2,
    legend_upper_2,
    color_bottom_2,
    color_upper_2,
    xLabel_2,
    yLabel_2,
    title_2,
    title,
):
    logger.info("Generating double stacked bar chart")

    fig, plots = plt.subplots(nrows=1, ncols=2, layout="constrained", figsize=(9, 5))

    percentage_bottom_1, percentage_upper_1 = calculate_percentages(
        values_bottom_1, values_upper_1, buckets_1
    )
    percentage_bottom_2, percentage_upper_2 = calculate_percentages(
        values_bottom_2, values_upper_2, buckets_2
    )

    # Plot1
    plot_1 = plots[0]
    logger.debug("Creating plot1")

    lower_bars_1 = plot_1.bar(
        buckets_1, values_bottom_1, label=legend_bottom_1, color=color_bottom_1
    )
    upper_bars_1 = plot_1.bar(
        buckets_1,
        values_upper_1,
        bottom=values_bottom_1,
        label=legend_upper_1,
        color=color_upper_1,
    )

    plot_1.set_xlabel(xLabel_1)
    plot_1.set_ylabel(yLabel_1)
    plot_1.set_title(title_1)
    plot_1.legend()
    logger.debug("Plot1 created")

    for i in range(len(buckets_1)):
        if values_bottom_1[i] > 0:
            plot_1.annotate(
                f"{percentage_bottom_1[i]:.1f}%",
                xy=(
                    lower_bars_1[i].get_x() + lower_bars_1[i].get_width() / 2,
                    values_bottom_1[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
            )
        if values_upper_1[i] > 0:
            plot_1.annotate(
                f"{percentage_upper_1[i]:.1f}%",
                xy=(
                    upper_bars_1[i].get_x() + upper_bars_1[i].get_width() / 2,
                    values_bottom_1[i] + values_upper_1[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
            )
    logger.debug("Annotations added to plot1")

    # Plot2
    plot_2 = plots[1]
    logger.debug("Creating plot2")

    lower_bars_2 = plot_2.bar(
        buckets_2, values_bottom_2, label=legend_bottom_2, color=color_bottom_2
    )
    upper_bars_2 = plot_2.bar(
        buckets_2,
        values_upper_2,
        bottom=values_bottom_2,
        label=legend_upper_2,
        color=color_upper_2,
    )

    plot_2.set_xlabel(xLabel_2)
    plot_2.set_ylabel(yLabel_2)
    plot_2.set_title(title_2)
    plot_2.legend()
    logger.debug("Plot2 created")

    for i in range(len(buckets_2)):
        if values_bottom_2[i] > 0:
            plot_2.annotate(
                f"{percentage_bottom_2[i]:.1f}%",
                xy=(
                    lower_bars_2[i].get_x() + lower_bars_2[i].get_width() / 2,
                    values_bottom_2[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
            )
        if values_upper_2[i] > 0:
            plot_2.annotate(
                f"{percentage_upper_2[i]:.1f}%",
                xy=(
                    upper_bars_2[i].get_x() + upper_bars_2[i].get_width() / 2,
                    values_bottom_2[i] + values_upper_2[i] / 2,
                ),
                xytext=(0, 0),
                textcoords="offset points",
                ha="center",
                va="center",
                color="white",
            )
    logger.debug("Annotations added to plot2")

    fig.suptitle(title, size="x-large", weight="bold")
    logger.debug("Figure created successfully")

    return fig
