from re import search
from datetime import datetime
from isaac_analyzer.yaml_loader import load_yaml
from isaac_analyzer.items import get_by_id
from isaac_analyzer.logging import getLogger

logger = getLogger(__name__)


def parse_file_name(file_path):
    logger.debug(f"Parsing file name: {file_path}")
    match = search(r"\d{4}-\d{2}-\d{2}_\d+", file_path)
    if not match:
        logger.error(f"Filename {file_path} does not match the expected format.")
        raise ValueError(f"Filename {file_path} does not match the expected format.")

    date_str, run_number = match.group().split("_")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    logger.debug(f"Parsed date: {date}, run_number: {run_number}")
    return date, int(run_number)


def parse_run(raw_run, index):
    logger.debug(f"Parsing run {index}: {raw_run}")
    output = {
        "number": index,
        "type": raw_run["type"],
        "seed": raw_run["seed"],
        "character": raw_run["character"],
        "ending": raw_run["ending"],
        "floors": [parse_floor(floor) for floor in raw_run["floors"]],
    }

    if raw_run["character"] == "Eden" and "startingItems" not in raw_run:
        output["victoryLap"] = True

    if "startingItems" in raw_run:
        output["startingItems"] = parse_items(raw_run["startingItems"])

    logger.debug(f"Parsed run data: {output}")
    return output


def parse_floor(floor):
    logger.debug(f"Parsing floor: {floor}")
    output = {
        "number": floor["number"],
        "type": floor["type"],
        "bossRoom": parse_boss_room(floor["bossRoom"]),
    }

    output["curse"] = bool(floor["curse"])
    if floor["curse"]:
        output["curseType"] = floor["curse"]

    if "itemRoom" in floor:
        output["itemRoom"] = parse_item_room(floor["itemRoom"])

    if "shop" in floor:
        output["shop"] = parse_shop(floor["shop"])

    if "deal" in floor:
        output["deal"] = parse_deal(floor["deal"])

    if "items" in floor:
        output["items"] = parse_items(floor["items"])

    if "bossRoomXL" in floor:
        output["bossRoomXL"] = parse_boss_room(floor["bossRoomXL"])

    if "specialRooms" in floor:
        output["specialRooms"] = parse_special_rooms(floor["specialRooms"])

    logger.debug(f"Parsed floor data: {output}")
    return output


def parse_special_rooms(special_rooms):
    logger.debug(f"Parsing special rooms: {special_rooms}")
    return [parse_special_room(room) for room in special_rooms]


def parse_special_room(special_room):
    logger.debug(f"Parsing special room: {special_room}")
    output = {
        "type": special_room["type"],
        "visited": special_room["visited"],
    }

    if "items" in special_room:
        output["items"] = parse_items(special_room["items"])

    if "number" in special_room:
        output["number"] = special_room["number"]

    logger.debug(f"Parsed special room data: {output}")
    return output


def parse_item_room(item_room):
    logger.debug(f"Parsing item room: {item_room}")
    output = {"visited": item_room["visited"]}

    if item_room["visited"]:
        output.update(
            {
                "rerollMachine": item_room["rerollMachine"],
                "items": parse_items(item_room["items"]),
            }
        )

    logger.debug(f"Parsed item room data: {output}")
    return output


def parse_boss_room(boss_room):
    logger.debug(f"Parsing boss room: {boss_room}")
    output = {"visited": boss_room["visited"]}

    if boss_room["visited"]:
        output.update(
            {
                "boss": boss_room["boss"],
                "champion": boss_room["champion"],
            }
        )
        if "items" in boss_room:
            output["items"] = parse_items(boss_room["items"])

    logger.debug(f"Parsed boss room data: {output}")
    return output


def parse_shop(shop):
    logger.debug(f"Parsing shop: {shop}")
    output = {"visited": shop["visited"]}

    if shop["visited"]:
        if "boss" not in shop:
            output["rerollMachine"] = (shop["rerollMachine"],)
            if "items" in shop:
                output["items"] = parse_items(shop["items"])
        else:
            output["boss"] = shop["boss"]
            if "items" in shop:
                output["items"] = parse_items(shop["items"])

    logger.debug(f"Parsed shop data: {output}")
    return output


def parse_deal(deal):
    logger.debug(f"Parsing deal: {deal}")
    output = {
        "type": deal["type"],
        "chance": deal["chance"],
    }

    if "visited" in deal:
        output["visited"] = deal["visited"]

    if "items" in deal:
        output["items"] = parse_items(deal["items"])

    if "boss" in deal:
        output["boss"] = deal["boss"]

    logger.debug(f"Parsed deal data: {output}")
    return output


def parse_items(items):
    logger.debug(f"Parsing items: {items}")
    return [parse_item(item["id"], item["taken"]) for item in items]


def parse_item(id, taken):
    logger.debug(f"Parsing item with id {id}, taken: {taken}")
    item = get_by_id(id)
    item["taken"] = taken
    logger.debug(f"Parsed item data: {item}")
    return item


def load_run_file(file_path):
    logger.info(f"Loading run file: {file_path}")
    raw_file = load_yaml(file_path)
    date, run_number = parse_file_name(file_path)

    run_data = {
        "date": date,
        "run_number": run_number,
        "runs": [parse_run(run, index) for index, run in enumerate(raw_file["runs"])],
    }

    logger.debug(f"Loaded run file data: {run_data}")
    return run_data
