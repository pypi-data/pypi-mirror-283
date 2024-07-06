from isaac_analyzer.analysis.boss import generate_boss_plot, get_boss_type
from isaac_analyzer.analysis.curses import generate_curses_plot, get_curse_distribution
from isaac_analyzer.analysis.endings import generate_picture_type_plot, get_picture_type
from isaac_analyzer.analysis.items import (
    generate_all_items_plot,
    generate_itemRoom_item_plot,
    get_all_items_statistic,
    get_itemRoom_items_statistics,
)
from isaac_analyzer.analysis.shop import (
    generate_shop_plot,
    get_shop_details,
    get_shop_items,
    generate_shop_item_plot,
)
from isaac_analyzer.logging import getLogger
from isaac_analyzer.run_loader import load_run_file
from isaac_analyzer.analysis.deals import (
    get_deal_type,
    get_deal_chances,
    generate_deal_plot,
)
from os.path import join
from glob import glob
from PIL import Image
import math

logger = getLogger(__name__)


def analyze_run_file(run_file):
    logger.info(f"Analyzing run file with run number {run_file['run_number']}.")
    for run in run_file["runs"]:
        analytics = {
            "deals": get_deal_type(run),
            "dealChance": get_deal_chances(run),
            "curses": get_curse_distribution(run),
            "shops": get_shop_details(run),
            "shop_items": get_shop_items(run),
            "itemRoom_items": get_itemRoom_items_statistics(run),
            "all_items": get_all_items_statistic(run),
            "picture_type": get_picture_type(run),
            "bosses": get_boss_type(run),
        }
        run["analytics"] = analytics
    logger.debug(f"Run file analysis complete: {run_file}")
    return run_file


def analyze_single_run(file_path, output_path):
    logger.info(f"Analyzing single run from file: {file_path}")
    run_file = load_run_file(file_path)
    analyzed_run_file = analyze_run_file(run_file)
    logger.info(f"Single run analysis complete. Results: {analyzed_run_file}")
    logger.warn(analyze_run_file["analytics"])


def analyze_runs(directory_path, output_path):
    logger.info(f"Analyzing all runs in directory: {directory_path}")
    yaml_files = glob(join(directory_path, "*.y*ml"))
    analyzed_runs = []

    for yaml_file in yaml_files:
        logger.info(f"Loading run file: {yaml_file}")
        run_file = load_run_file(yaml_file)
        analyzed_run = analyze_run_file(run_file)
        analyzed_runs.append(analyzed_run)
        logger.info(f"Run file {yaml_file} analyzed.")

    logger.info("All run files analyzed. Generating plots.")
    generate_plots(analyzed_runs, output_path)
    logger.info("Plot generation complete.")


def generate_plots(analyzed_runs, output_path):
    generate_deal_plot(analyzed_runs, output_path)
    generate_curses_plot(analyzed_runs, output_path)
    generate_shop_plot(analyzed_runs, output_path)
    generate_all_items_plot(analyzed_runs, output_path)
    generate_shop_item_plot(analyzed_runs, output_path)
    generate_itemRoom_item_plot(analyzed_runs, output_path)
    generate_picture_type_plot(analyzed_runs, output_path)
    generate_boss_plot(analyzed_runs, output_path)
    # combine_plots(output_path)
    combine_images_2_column_grid(
        [
            "deals.png",
            "curses.png",
            "shops.png",
            "shop_items.png",
            "itemRoom_items.png",
            "all_items.png",
            "picture_type.png",
            "boss.png",
        ],
        output_path,
    )


def combine_images_2_column_grid(image_files, output_path):
    # Open all images and determine the size for the grid
    images = [Image.open(join(output_path, image_file)) for image_file in image_files]
    widths, heights = zip(*(image.size for image in images))

    # Calculate the grid dimensions
    max_width = max(widths)
    max_height = max(heights)
    num_images = len(images)
    num_rows = math.ceil(num_images / 2)

    # Create a new blank image with a white background
    grid_width = 2 * max_width
    grid_height = num_rows * max_height
    grid_image = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

    # Paste images into the grid
    for index, image in enumerate(images):
        x_offset = (index % 2) * max_width
        y_offset = (index // 2) * max_height
        grid_image.paste(image, (x_offset, y_offset))

    # Save the combined image
    grid_image.save(join(output_path, "isaac_statistics.png"))


def combine_plots(output_path):
    logger.info("Combining plots into a single image.")
    image1 = Image.open(join(output_path, "deals.png"))
    image2 = Image.open(join(output_path, "curses.png"))
    image3 = Image.open(join(output_path, "shops.png"))
    image4 = Image.open(join(output_path, "all_items.png"))

    height = image1.height + image2.height + image3.height + image4.height
    width = max(image1.width, image2.width, image3.width)

    combined = Image.new("RGB", (width, height))
    combined.paste(image1, (0, 0))
    combined.paste(image2, (0, image1.height))
    combined.paste(image3, (0, image1.height + image2.height))
    combined.paste(image4, (0, image1.height + image2.height + image3.height))

    combined.save(join(output_path, "combined.png"))
    logger.info("Combined plot saved.")
