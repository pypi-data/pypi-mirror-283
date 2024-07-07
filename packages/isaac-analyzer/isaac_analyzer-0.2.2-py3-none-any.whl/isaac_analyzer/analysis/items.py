from isaac_analyzer.logging import getLogger
from isaac_analyzer.utils import (
    add_dicts,
    add_item_analysis_dicts,
    get_empty_item_analysis_dict,
    get_empty_itemRoom_items_dict,
)
from isaac_analyzer.plotting.double_chart import (
    double_stacked_bar_chart,
    pie_hbar_chart,
)
from os.path import join

logger = getLogger(__name__)


def analyze_items_list(items):
    logger.debug("Analyzing items list")
    item_stats = get_empty_item_analysis_dict()

    for item in items:
        status = "taken" if item["taken"] else "ignored"
        item_quality = str(item["quality"])
        item_type = item["type"]

        item_stats["quality"][item_quality][status] += 1
        item_stats["type"][item_type][status] += 1

    logger.debug("Items list analysis complete")
    return item_stats


def get_itemRoom_items_statistics(run):
    logger.info("Generating itemRoom item statistics for a run")
    itemRoom_items = get_empty_itemRoom_items_dict()

    for floor in run["floors"]:
        shop = floor.get("shop")
        if shop and shop.get("visited") and "boss" not in shop:
            items = shop.get("items", [])
            if items:
                all_quality = sum(item["quality"] for item in items)
                all_count = len(items)
                taken_items = [item for item in items if item["taken"]]
                ignored_items = [item for item in items if not item["taken"]]

                taken_count = len(taken_items)
                ignored_count = all_count - taken_count
                taken_quality = sum(item["quality"] for item in taken_items)
                ignored_quality = sum(item["quality"] for item in ignored_items)

                for item in items:
                    itemRoom_items["type"][item["type"]] += 1

                if all_count > 0:
                    itemRoom_items["quality"]["all"] = (
                        (itemRoom_items["quality"]["all"] + (all_quality / all_count))
                        / 2
                        if itemRoom_items["quality"]["all"] > 0
                        else (all_quality / all_count)
                    )
                if taken_count > 0:
                    itemRoom_items["quality"]["taken"] = (
                        (
                            itemRoom_items["quality"]["taken"]
                            + (taken_quality / taken_count)
                        )
                        / 2
                        if itemRoom_items["quality"]["taken"] > 0
                        else (taken_quality / taken_count)
                    )
                if ignored_count > 0:
                    itemRoom_items["quality"]["ignored"] = (
                        (
                            itemRoom_items["quality"]["ignored"]
                            + (ignored_quality / ignored_count)
                        )
                        / 2
                        if itemRoom_items["quality"]["ignored"] > 0
                        else (ignored_quality / ignored_count)
                    )

    logger.debug("ItemRoom items statistics generation complete")
    return itemRoom_items


def get_all_items_statistic(run):
    logger.info("Generating item statistics for a run")
    item_stats = get_empty_item_analysis_dict()

    for floor in run["floors"]:
        logger.debug(f"Processing floor: {floor}")
        if "itemRoom" in floor and floor["itemRoom"]["visited"]:
            item_stats = add_item_analysis_dicts(
                item_stats, analyze_items_list(floor["itemRoom"]["items"])
            )

        if "shop" in floor and floor["shop"]["visited"] and "items" in floor["shop"]:
            item_stats = add_item_analysis_dicts(
                item_stats, analyze_items_list(floor["shop"]["items"])
            )

        if "items" in floor:
            item_stats = add_item_analysis_dicts(
                item_stats, analyze_items_list(floor["items"])
            )

        if (
            "bossRoom" in floor
            and floor["bossRoom"]["visited"]
            and "items" in floor["bossRoom"]
        ):
            item_stats = add_item_analysis_dicts(
                item_stats, analyze_items_list(floor["bossRoom"]["items"])
            )

        if "specialRooms" in floor:
            for special_room in floor["specialRooms"]:
                if special_room["visited"] and "items" in special_room:
                    item_stats = add_item_analysis_dicts(
                        item_stats, analyze_items_list(special_room["items"])
                    )

    logger.info("Item statistics generation complete")
    return item_stats


def generate_all_items_plot(analyzed_runs, output_path):
    logger.info("Generating all items plot")
    item_stats = get_empty_item_analysis_dict()

    for analyzed_run in analyzed_runs:
        logger.debug("Processing analyzed run")
        for run in analyzed_run["runs"]:
            item_stats = add_item_analysis_dicts(
                item_stats, run["analytics"]["all_items"]
            )

    all_items_fig = double_stacked_bar_chart(
        buckets_1=list(item_stats["quality"].keys()),
        xLabel_1="Item Quality",
        yLabel_1="Count",
        values_bottom_1=[
            item_stats["quality"][bucket]["taken"] for bucket in item_stats["quality"]
        ],
        values_upper_1=[
            item_stats["quality"][bucket]["ignored"] for bucket in item_stats["quality"]
        ],
        color_bottom_1="green",
        color_upper_1="red",
        title_1="Items taken and ignored by quality",
        legend_bottom_1="Taken",
        legend_upper_1="Ignored",
        buckets_2=list(item_stats["type"].keys()),
        xLabel_2="Item Type",
        yLabel_2="Count",
        values_bottom_2=[
            item_stats["type"][bucket]["taken"] for bucket in item_stats["type"]
        ],
        values_upper_2=[
            item_stats["type"][bucket]["ignored"] for bucket in item_stats["type"]
        ],
        color_bottom_2="green",
        color_upper_2="red",
        title_2="Items taken and ignored by type",
        legend_bottom_2="Taken",
        legend_upper_2="Ignored",
        title="All Items (June 2024)",
    )

    output_file = join(output_path, "all_items.png")
    all_items_fig.savefig(output_file)
    logger.info(f"All items plot saved to {output_file}")


def generate_itemRoom_item_plot(analyzed_runs, output_path):
    itemRoom_items = get_empty_itemRoom_items_dict()

    for analyzed_run in analyzed_runs:
        logger.debug(f"Processing analyzed run: {analyzed_run}")
        for run in analyzed_run["runs"]:
            logger.debug(f"Processing run: {run}")
            itemRoom_items = {
                "type": add_dicts(
                    itemRoom_items["type"], run["analytics"]["itemRoom_items"]["type"]
                ),
                "quality": add_dicts(
                    itemRoom_items["quality"],
                    run["analytics"]["itemRoom_items"]["quality"],
                ),
            }

    itemRoom_item_figure = pie_hbar_chart(
        values_1=[itemRoom_items["type"][x] for x in itemRoom_items["type"]],
        labels_1=itemRoom_items["type"].keys(),
        colors_1=["red", "green"],
        title_1="Item Type",
        values_2=list(
            reversed(
                [
                    itemRoom_items["quality"][x] / len(analyzed_runs)
                    for x in itemRoom_items["quality"]
                ]
            )
        ),
        labels_2=list(reversed(itemRoom_items["quality"].keys())),
        x_label_2="Quality",
        title_2="Average Quality of Item Groups",
        title="ItemRoom Items (June 2024)",
    )

    output_file = join(output_path, "itemRoom_items.png")
    itemRoom_item_figure.savefig(output_file)
    logger.info(f"Shop plot saved to {output_file}")
