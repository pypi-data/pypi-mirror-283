from tabulate import tabulate
from isaac_analyzer.logging import getLogger
from isaac_analyzer.yaml_loader import load_yaml_resource

logger = getLogger(__name__)

item_list = []


def load_items():
    global item_list
    if len(item_list) == 0:
        logger.debug("Loading items from items.yaml")
        data = load_yaml_resource("items.yaml")
        item_list = data.get("items", [])
        logger.debug(f"{len(item_list)} items loaded from items.yaml")
    else:
        logger.debug("Items already loaded, using cached list")
    return item_list


def print_items():
    """Print items from items.yaml"""
    logger.debug("Printing all items from items.yaml")
    items = load_items()
    if isinstance(items, list) and all(isinstance(item, dict) for item in items):
        table = tabulate(items, headers="keys", tablefmt="github")
        logger.debug("Items formatted into table")
        print(table)
    else:
        logger.warning("Items list is not in the expected format")


def get_by_id(id):
    logger.debug(f"Getting item with id: {id}")
    items = load_items()
    item = next((item.copy() for item in items if item["id"] == str(id)), None)
    if item:
        logger.debug(f"Item found: {item}")
    else:
        logger.warning(f"No item found with id: {id}")
    return item
