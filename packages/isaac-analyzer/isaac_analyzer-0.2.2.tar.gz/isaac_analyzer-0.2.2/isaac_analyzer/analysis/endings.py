from isaac_analyzer.logging import getLogger
from isaac_analyzer.plotting.single_chart import pie_chart
from os.path import join

logger = getLogger(__name__)


def get_picture_type(run):
    for floor in run["floors"]:
        if floor["bossRoom"]["boss"] == "Mom":
            for item in floor["bossRoom"]["items"]:
                if item["taken"]:
                    return item["name"]

        if "bossRoomXL" in floor and floor["bossRoomXL"]["boss"] == "Mom":
            for item in floor["bossRoomXL"]["items"]:
                if item["taken"]:
                    return item["name"]


def generate_picture_type_plot(analyzed_runs, output_path):
    picture_type = [0, 0, 0]

    for analyzed_run in analyzed_runs:
        for run in analyzed_run["runs"]:
            if run["analytics"]["picture_type"] == "The Polaroid":
                picture_type[0] += 1
            elif run["analytics"]["picture_type"] == "The Negative":
                picture_type[1] += 1
            else:
                picture_type[2] += 1

    picture_figure = pie_chart(
        values=picture_type,
        labels=["The Polaroid", "The Negative", "None"],
        colors=["whitesmoke", "dimgray", "blue"],
        title="Negative vs Polaroid (June 2024)",
    )

    output_file = join(output_path, "picture_type.png")
    picture_figure.savefig(output_file)
    logger.info(f"Picture type plot saved to {output_file}")
