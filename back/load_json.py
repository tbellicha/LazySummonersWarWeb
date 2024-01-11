import json
import sys
from classes import *
from values import *
from flask import Blueprint, request, jsonify

load_json_blueprint = Blueprint("load_json", __name__, url_prefix="/api")

player_name = ""
all_account_runes = []
all_account_modifiers = []
all_account_monsters = []
all_account_artifacts = []


@load_json_blueprint.route("/load_json", methods=["POST"])
def load_json():
    data = request.json  # Assuming JSON data is being sent in the request
    file_name = data.get("file_name", "")
    file_content = data.get("file_content", "")
    if file_name == "" or file_content == "":
        return "Error: file_name or file_content not found in request", 400
    print(f"File Name: {file_name}")
    data = file_content

    interesting_monsters = []
    all_account_runes.clear()
    all_account_modifiers.clear()
    all_account_monsters.clear()
    all_account_artifacts.clear()
    compute_json(data)
    for monster in all_account_monsters:
        if (
            monster.natural_stars >= parameters[monster.element]["min_natural_stars"]
            and monster.current_stars
            >= parameters[monster.element]["min_current_stars"]
            and monster.awaken_level >= parameters[monster.element]["min_awake_level"]
        ):
            interesting_monsters.append(monster)
    total_score = 0
    map_score = [[0 for i in podValues["Eff"]] for i in podValues["Sets"]]
    map_sets = [x for x in podValues["Sets"]]
    map_eff = [x for x in podValues["Eff"]]
    for r, rune in enumerate(all_account_runes):
        curr_score = 0
        for e, podEff in enumerate(podValues["Eff"]):
            if rune.efficiency >= int(podEff):
                curr_score += int(podValues["Eff"][podEff])
                if Set(rune.set).name in podValues["Sets"]:
                    curr_score *= podValues["Sets"][Set(rune.set).name]
                    map_score[map_sets.index(Set(rune.set).name)][e] += 1
                else:
                    curr_score *= podValues["Sets"]["ALL"]
                    map_score[map_sets.index("ALL")][e] += 1
                break
        total_score += curr_score
    table = []
    map_eff.reverse()
    for c, x in enumerate(map_sets):
        map_score[c].reverse()
        for i in range(len(map_score[c])):
            table.append([x, map_eff[i], map_score[c][i]])

    response = {
        "name": player_name,
        "score": total_score,
        "runes": [rune.toJSON() for rune in all_account_runes],
        "table": table,
        "modifiers": [modifier.toJSON() for modifier in all_account_modifiers],
        "monsters": [monster.toJSON() for monster in interesting_monsters],
        "artifacts": [artifact.toJSON() for artifact in all_account_artifacts],
    }
    return response


def compute_json(data):
    player_name = data["wizard_info"]["wizard_name"]
    #  Runes from monsters
    for monster in data["unit_list"]:
        for rune in monster["runes"]:
            crune = Rune(rune)
            all_account_runes.append(crune)
        for artifacts in monster["artifacts"]:
            cartifact = Artifact(artifacts)
            all_account_artifacts.append(cartifact)
    #  Runes from inventory
    for rune in data["runes"]:
        crune = Rune(rune)
        all_account_runes.append(crune)
    all_account_runes.sort(key=lambda x: x.efficiency, reverse=True)
    #  Runes from inventory
    for artifact in data["artifacts"]:
        cartifact = Artifact(artifact)
        all_account_artifacts.append(cartifact)
    #  Modifiers from inventory
    for modifier in data["rune_craft_item_list"]:
        cmodifier = Modifier(modifier)
        all_account_modifiers.append(cmodifier)
    #  Get game monsters
    f = open("monsters.json", "r")
    all_monsters = json.loads(f.read())
    #  Monsters
    for monster in data["unit_list"]:
        try:
            cmonster = Monster(monster, all_monsters)
            all_account_monsters.append(cmonster)
        except TypeError:
            continue
    all_account_monsters.sort(
        key=lambda x: (x.element, x.natural_stars, x.name), reverse=True
    )
    all_account_modifiers.sort(key=lambda x: x.quality, reverse=True)
    print(f"Artifacts: {len(all_account_artifacts)}")
