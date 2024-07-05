from isaac_analyzer.logging import getLogger
from isaac_analyzer.plotting.single_chart import pie_chart
from isaac_analyzer.plotting.double_chart import pie_hbar_chart
from isaac_analyzer.utils import (
    add_dicts,
    get_empty_shop_details_dict,
    get_empty_shop_items_dict,
)
from os.path import join

logger = getLogger(__name__)


def get_shop_items(run):
    shop_items = get_empty_shop_items_dict()

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

                if taken_count > 0:
                    shop_items["shop_usage"]["used"] += 1
                else:
                    shop_items["shop_usage"]["ignored"] += 1

                if all_count > 0:
                    shop_items["quality"]["all"] = (
                        (shop_items["quality"]["all"] + (all_quality / all_count)) / 2
                        if shop_items["quality"]["all"] > 0
                        else (all_quality / all_count)
                    )
                if taken_count > 0:
                    shop_items["quality"]["taken"] = (
                        (shop_items["quality"]["taken"] + (taken_quality / taken_count))
                        / 2
                        if shop_items["quality"]["taken"] > 0
                        else (taken_quality / taken_count)
                    )
                if ignored_count > 0:
                    shop_items["quality"]["ignored"] = (
                        (
                            shop_items["quality"]["ignored"]
                            + (ignored_quality / ignored_count)
                        )
                        / 2
                        if shop_items["quality"]["ignored"] > 0
                        else (ignored_quality / ignored_count)
                    )

    return shop_items


def get_shop_details(run):
    logger.debug("Calculating shop greed and visiting rate.")
    shops = get_empty_shop_details_dict()

    for floor in run["floors"]:
        if "shop" in floor:
            if floor["shop"]["visited"]:
                if "boss" in floor["shop"]:
                    shops["visited_boss"] += 1
                else:
                    shops["visited"] += 1
            else:
                shops["skipped"] += 1

    logger.debug(f"Shop details: {shops}")
    return shops


def generate_shop_plot(analyzed_runs, output_path):
    logger.info("Generating shop plot.")
    shops = get_empty_shop_details_dict()

    for analyzed_run in analyzed_runs:
        for run in analyzed_run["runs"]:
            shops = add_dicts(shops, run["analytics"]["shops"])

    values = [shops[key] for key in shops.keys()]
    labels = ["Greed", "Normal", "Skipped"]
    colors = ["yellowgreen", "green", "steelblue"]
    shop_figure = pie_chart(values, labels, colors, "Shops (June 2024)")

    output_file = join(output_path, "shops.png")
    shop_figure.savefig(output_file)
    logger.info(f"Shop plot saved to {output_file}")


def generate_shop_item_plot(analyzed_runs, output_path):
    shop_items = get_empty_shop_items_dict()

    for analyzed_run in analyzed_runs:
        for run in analyzed_run["runs"]:
            shop_items = {
                "shop_usage": add_dicts(
                    shop_items["shop_usage"],
                    run["analytics"]["shop_items"]["shop_usage"],
                ),
                "quality": add_dicts(
                    shop_items["quality"], run["analytics"]["shop_items"]["quality"]
                ),
            }

    shop_item_figure = pie_hbar_chart(
        values_1=[shop_items["shop_usage"][x] for x in shop_items["shop_usage"]],
        labels_1=["items taken", "no items taken"],
        colors_1=["green", "red"],
        title_1="Shop Usage",
        values_2=list(
            reversed(
                [
                    shop_items["quality"][x] / len(analyzed_runs)
                    for x in shop_items["quality"]
                ]
            )
        ),
        labels_2=list(reversed(shop_items["quality"].keys())),
        x_label_2="Quality",
        title_2="Average Quality of Item Groups",
        title="Shop Items (June 2024)",
    )

    output_file = join(output_path, "shop_items.png")
    shop_item_figure.savefig(output_file)
    logger.info(f"Shop plot saved to {output_file}")
