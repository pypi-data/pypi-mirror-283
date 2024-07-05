def add_item_analysis_dicts(dict1, dict2):
    result = {"quality": {}, "type": {}}

    # Sum the 'quality' part of the dictionaries
    for key in dict1["quality"]:
        result["quality"][key] = {
            "ignored": dict1["quality"][key]["ignored"]
            + dict2["quality"][key]["ignored"],
            "taken": dict1["quality"][key]["taken"] + dict2["quality"][key]["taken"],
        }

    # Sum the 'type' part of the dictionaries
    for key in dict1["type"]:
        result["type"][key] = {
            "ignored": dict1["type"][key]["ignored"] + dict2["type"][key]["ignored"],
            "taken": dict1["type"][key]["taken"] + dict2["type"][key]["taken"],
        }

    return result


def add_dicts(dict1, dict2):
    result_dict = {}
    for key in dict1:
        result_dict[key] = dict1[key] + dict2[key]
    return result_dict


def get_empty_item_analysis_dict():
    return {
        "quality": {
            "0": {"ignored": 0, "taken": 0},
            "1": {"ignored": 0, "taken": 0},
            "2": {"ignored": 0, "taken": 0},
            "3": {"ignored": 0, "taken": 0},
            "4": {"ignored": 0, "taken": 0},
        },
        "type": {
            "active": {"ignored": 0, "taken": 0},
            "passive": {"ignored": 0, "taken": 0},
        },
    }


def get_empty_curses_dict():
    return {
        "Curse of the Blind": 0,
        "Curse of Darkness": 0,
        "Curse of the Lost": 0,
        "Curse of the Maze": 0,
        "Curse of the Unknown": 0,
        "Curse of the Labyrinth": 0,
        "Curse of the Cursed": 0,
        "Curse of the Giant": 0,
        "No Curse": 0,
        "Total curses": 0,
    }


def get_empty_deal_chance_dict():
    return {
        "<0.25": {"hit": 0, "miss": 0},
        "<0.50": {"hit": 0, "miss": 0},
        "<0.75": {"hit": 0, "miss": 0},
        ">0.75": {"hit": 0, "miss": 0},
    }


def get_empty_shop_details_dict():
    return {"visited_boss": 0, "visited": 0, "skipped": 0}


def get_empty_shop_items_dict():
    return {
        "shop_usage": {"used": 0, "ignored": 0},
        "quality": {"all": 0, "taken": 0, "ignored": 0},
    }


def get_empty_itemRoom_items_dict():
    return {
        "type": {"active": 0, "passive": 0},
        "quality": {"all": 0, "taken": 0, "ignored": 0},
    }
