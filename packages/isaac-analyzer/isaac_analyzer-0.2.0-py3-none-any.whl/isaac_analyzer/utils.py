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


def get_empty_boss_count_dict():
    return {
        "Monstro": 0,
        "Gemini": 0,
        "Steven": 0,
        "Dingle": 0,
        "Gurglings": 0,
        "Larry Jr.": 0,
        "The Duke of Flies": 0,
        "Widow": 0,
        "Blighted Ovum": 0,
        "The Haunt": 0,
        "Pin": 0,
        "Famine": 0,
        "Fistula": 0,
        "Chub": 0,
        "C.H.A.D": 0,
        "Gurdy": 0,
        "Mega Fatty": 0,
        "Mega Maw": 0,
        "Gurdy Jr.": 0,
        "Peep": 0,
        "The Husk": 0,
        "The Hollow": 0,
        "Carrion Queen": 0,
        "Dark One": 0,
        "Polycephalus": 0,
        "The Wretched": 0,
        "Pestilence": 0,
        "Monstro II": 0,
        "Gish": 0,
        "The Cage": 0,
        "The Gate": 0,
        "Loki": 0,
        "The Advesary": 0,
        "The Bloat": 0,
        "Mask of Infamy": 0,
        "War": 0,
        "Blastocyst": 0,
        "Mama Gurdy": 0,
        "Scolex": 0,
        "Mr. Fred": 0,
        "Lokii": 0,
        "Daddy Long Legs": 0,
        "Triachnid": 0,
        "Teratoma": 0,
        "Death": 0,
        "Conquest": 0,
        "Headless Horseman": 0,
        "The Fallen": 0,
        "Dangle": 0,
        "Turdlings": 0,
        "Little Horn": 0,
        "Rag Man": 0,
        "The Stain": 0,
        "The Forsaken": 0,
        "The Frail": 0,
        "Brownie": 0,
        "Big Horn": 0,
        "Rag Mega": 0,
        "Sisters Vis": 0,
        "The Matriarch": 0,
        "Baby Plum": 0,
        "Bumbino": 0,
        "Reap Creep": 0,
        "The Pile": 0,
        "The Rainmaker": 0,
        "Min-Min": 0,
        "Lil Blub": 0,
        "Wormwood": 0,
        "Clog": 0,
        "Colostomia": 0,
        "Turdlet": 0,
        "Tuff Twins": 0,
        "Hornfel": 0,
        "Great Gideon": 0,
        "Singe": 0,
        "The Shell": 0,
        "Clutch": 0,
        "The Siren": 0,
        "The Heretic": 0,
        "The Visage": 0,
        "The Horny Boys": 0,
        "Chimera": 0,
        "The Scourge": 0,
        "Rotgut": 0,
        "Ultra Famine": 0,
        "Ultra Pestilence": 0,
        "Ultra War": 0,
        "Ultra Death": 0,
        "Mom": 0,
        "Mom's Heart": 0,
        "It Lives": 0,
        "Satan": 0,
        "Isaac": 0,
        "The Lamb": 0,
        "???": 0,
        "Mega Satan": 0,
        "Hush": 0,
        "Delirium": 0,
        "Mother": 0,
        "Dogma": 0,
        "The Beast": 0,
        "Ultra Greed": 0,
        "Ultra Greedier": 0,
    }
