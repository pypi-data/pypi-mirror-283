from isaac_analyzer.logging import getLogger
from isaac_analyzer.plotter import plot_curses
from isaac_analyzer.utils import add_dicts, get_empty_curses_dict
from os.path import join

logger = getLogger(__name__)


def get_curse_distribution(run):
    logger.debug("Calculating curse distribution for run.")
    curses = get_empty_curses_dict()

    for floor in run["floors"]:
        curse_type = floor.get("curseType", "No Curse")
        curses[curse_type] += 1
        if curse_type != "No Curse":
            curses["Total curses"] += 1

    logger.debug(f"Curse distribution: {curses}")
    return curses


def generate_curses_plot(analyzed_runs, output_path):
    logger.info("Generating curses plot.")
    curses = get_empty_curses_dict()

    for analyzed_run in analyzed_runs:
        for run in analyzed_run["runs"]:
            curses = add_dicts(curses, run["analytics"]["curses"])

    curses_figure = plot_curses(curses, title="Curses (June 2024)")
    output_file = join(output_path, "curses.png")
    curses_figure.savefig(output_file)
    logger.info(f"Curses plot saved to {output_file}")
