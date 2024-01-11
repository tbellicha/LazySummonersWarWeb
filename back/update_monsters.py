import json
import time

import pip
from main import app, prefix_url

@app.route(f'{prefix_url}/update/monsters', methods=['POST'])
def func_name(foo):
    nb = 0
    curr_computed = 0
    f = open("monsters.json", "w")
    while 1:
        try:
            nb += 1
            response = pip._vendor.requests.get(
                "https://swarfarm.com/api/v2/monsters/?id__in=&com2us_id=&family_id=&base_stars=&base_stars__lte=&base_stars__gte=&natural_stars=&natural_stars__lte=&natural_stars__gte=2&obtainable=&fusion_food=&homunculus=&name=&order_by=&page="
                + str(nb)
            )
            api_json = response.json()
            count = api_json["count"]
            curr_computed += len(api_json["results"])
            to_remove = []
            for i, curr in enumerate(api_json["results"]):
                del curr["url"]
                del curr["obtainable"]
                del curr["can_awaken"]
                del curr["awaken_bonus"]
                del curr["skills"]
                del curr["leader_skill"]
                del curr["homunculus_skills"]
                del curr["base_hp"]
                del curr["base_attack"]
                del curr["base_defense"]
                del curr["speed"]
                del curr["crit_rate"]
                del curr["crit_damage"]
                del curr["resistance"]
                del curr["accuracy"]
                del curr["raw_hp"]
                del curr["raw_attack"]
                del curr["raw_defense"]
                del curr["max_lvl_hp"]
                del curr["max_lvl_attack"]
                del curr["max_lvl_defense"]
                del curr["awakens_from"]
                del curr["awakens_to"]
                del curr["awaken_cost"]
                del curr["source"]
                del curr["fusion_food"]
                del curr["homunculus"]
                del curr["craft_cost"]
                del curr["craft_materials"]
                res_str = ""
                for c in curr["name"]:
                    curr_char = str(c.encode("utf-8", "ignore"))
                    if len(curr_char) > 4:
                        to_remove.append(i)
                        break
                    res_str += curr_char
                for count, elem in enumerate(to_remove):
                    del api_json["results"][to_remove[count] - count]
                f.write(json.dumps(api_json["results"], indent=4))
                if not api_json["next"]:
                    break
            return 0
        except Exception as e:
            return e