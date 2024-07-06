from isaac_analyzer.logging import getLogger
from isaac_analyzer.utils import get_empty_deal_chance_dict
from isaac_analyzer.plotting.double_chart import stacked_bar_pie_chart
from os.path import join

logger = getLogger(__name__)


def get_deal_chances(run):
    logger.debug("Calculating deal chances for run.")
    deal_buckets = get_empty_deal_chance_dict()

    for floor in run["floors"]:
        if "deal" in floor:
            chance = floor["deal"]["chance"]
            deal_type_present = bool(floor["deal"]["type"])
            bucket = (
                "<0.25"
                if chance <= 0.25
                else "<0.50"
                if chance <= 0.50
                else "<0.75"
                if chance <= 0.75
                else ">0.75"
            )
            deal_buckets[bucket]["hit" if deal_type_present else "miss"] += 1

    logger.debug(f"Deal chances calculated: {deal_buckets}")
    return deal_buckets


def get_deal_type(run):
    logger.debug("Calculating deal types for run.")
    deals = {"total": 0, "angel": 0, "devil": 0}

    for floor in run["floors"]:
        if "deal" in floor and floor["deal"]["type"]:
            deal_type = floor["deal"]["type"]
            deals[deal_type] += 1
            deals["total"] += 1

    logger.debug(f"Deal types calculated: {deals}")
    return deals


def generate_deal_plot(analyzed_runs, output_path):
    logger.info("Generating deal plot.")
    deal_count = [0, 0]
    deal_chances = get_empty_deal_chance_dict()

    for analyzed_run in analyzed_runs:
        for run in analyzed_run["runs"]:
            deal_count[0] += run["analytics"]["deals"]["devil"]
            deal_count[1] += run["analytics"]["deals"]["angel"]
            for bucket in deal_chances:
                deal_chances[bucket]["hit"] += run["analytics"]["dealChance"][bucket][
                    "hit"
                ]
                deal_chances[bucket]["miss"] += run["analytics"]["dealChance"][bucket][
                    "miss"
                ]

    deal_figure = stacked_bar_pie_chart(
        buckets_1=[
            "0% - 25%",
            "25% - 50%",
            "50% - 75%",
            "75% - 100%",
        ],  # list(deal_chances.keys()),
        xLabel_1="Deal Chance",
        yLabel_1="Count",
        values_bottom_1=[deal_chances[bucket]["hit"] for bucket in deal_chances],
        values_upper_1=[deal_chances[bucket]["miss"] for bucket in deal_chances],
        color_bottom_1="green",
        color_upper_1="red",
        title_1="Hit or Miss of a deal based on chance",
        legend_bottom_1="Hit",
        legend_upper_1="Miss",
        values_2=deal_count,
        labels_2=["devil", "angel"],
        colors_2=["dimgray", "whitesmoke"],
        title_2="Deal type and count",
        title="Devil and Angel Deals (June 2024)",
    )

    output_file = join(output_path, "deals.png")
    deal_figure.savefig(output_file)
    logger.info(f"Deal plot saved to {output_file}")
