import json
from values import Set, Stat, Stars, Quality
from efficiency import calc_efficiency


class Monster:
    def __init__(self, monster, all_monsters):
        file_monster = next(
            (
                sub
                for sub in all_monsters
                if sub["com2us_id"] == monster["unit_master_id"]
            ),
            None,
        )
        self.entity_unique_id = monster["unit_id"]
        self.monster_id = monster["unit_master_id"]
        self.level = monster["unit_level"]
        self.current_stars = monster["class"]
        if self.monster_id == 14314:  ## Skips the Rainbowmons
            self.name = "Rainbowmons"
            self.element = "Light"
            self.natural_stars = 0
            self.awaken_level = 0
            self.image_filename = "missing.jpg"
        else:
            try:
                self.name = file_monster["name"]
                self.element = file_monster["element"]
                self.natural_stars = file_monster["natural_stars"]
                self.awaken_level = file_monster["awaken_level"]
                self.image_filename = file_monster["image_filename"]
            except TypeError:
                self.name = "Unknown monster"
                self.element = "Unknown monster"
                self.natural_stars = "Unknown monster"
                self.awaken_level = "Unknown monster"
                self.image_filename = "Unknown monster"
                raise TypeError

    def __str__(self) -> str:
        if self.awaken_level == 0:
            return f"{self.name} ({self.element})"
        else:
            return f"{self.name}"

    def toJSON(self):
        return json.dumps(
            {
                "entity_unique_id": self.entity_unique_id,
                "monster_id": self.monster_id,
                "level": self.level,
                "current_stars": self.current_stars,
                "name": self.name,
                "element": self.element,
                "natural_stars": self.natural_stars,
                "awaken_level": self.awaken_level,
                "image_filename": self.image_filename,
            },
            indent=4,
        )


class RuneStat:
    def __init__(self, substats):
        self.stat_id = substats[0]
        self.value = substats[1]
        self.third = substats[2]
        self.grind = substats[3]

    def __str__(self) -> str:
        return f"{self.value + self.grind} (+{self.grind}) {Stat(self.stat_id).name}"

    def toJSON(self):
        return json.dumps(
            {
                "stat_id": self.stat_id,
                "value": self.value,
                "third": self.third,
                "grind": self.grind,
            },
            indent=4,
        )


class Rune:
    def __init__(self, rune):
        self.rune_id = rune["rune_id"]
        self.equipped = rune["occupied_type"]
        self.slot = rune["slot_no"]
        self.quality = rune["rank"]
        self.nb_stars = rune["class"]
        self.set = rune["set_id"]
        self.main_stat_id = rune["pri_eff"][0]
        self.innate_stat_id = rune["prefix_eff"][0]
        self.innate_stat_value = rune["prefix_eff"][1]
        self.substats = []
        self.efficiency = 0
        self.max_grind_efficiency = 0
        self.max_gem_efficiency = 0
        self.gem = Modifier
        for substat in rune["sec_eff"]:
            self.substats.append(RuneStat(substat))
        self.efficiency = calc_efficiency(self)

    def __str__(self) -> str:
        if len(self.substats) == 1:
            return (
                f"{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n"
                f"{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n"
                f"{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n"
                f"Efficiency: {self.efficiency}"
            )
        if len(self.substats) == 2:
            return (
                f"{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n"
                f"{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n"
                f"{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n"
                f"{self.substats[1].value + self.substats[1].grind} (+{self.substats[1].grind}) {Stat(self.substats[1].stat_id).name}\n"
                f"Efficiency: {self.efficiency}"
            )
        if len(self.substats) == 3:
            return (
                f"{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n"
                f"{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n"
                f"{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n"
                f"{self.substats[1].value + self.substats[1].grind} (+{self.substats[1].grind}) {Stat(self.substats[1].stat_id).name}\n"
                f"{self.substats[2].value + self.substats[2].grind} (+{self.substats[2].grind}) {Stat(self.substats[2].stat_id).name}\n"
                f"Efficiency: {self.efficiency}"
            )
        if len(self.substats) == 4:
            return (
                f"{Set(self.set).name} {Stat(self.main_stat_id).name} {self.slot} {Stars(self.nb_stars).name}\n"
                f"{self.innate_stat_value} {Stat(self.innate_stat_id).name}\n"
                f"{self.substats[0].value + self.substats[0].grind} (+{self.substats[0].grind}) {Stat(self.substats[0].stat_id).name}\n"
                f"{self.substats[1].value + self.substats[1].grind} (+{self.substats[1].grind}) {Stat(self.substats[1].stat_id).name}\n"
                f"{self.substats[2].value + self.substats[2].grind} (+{self.substats[2].grind}) {Stat(self.substats[2].stat_id).name}\n"
                f"{self.substats[3].value + self.substats[3].grind} (+{self.substats[3].grind}) {Stat(self.substats[3].stat_id).name}\n"
                f"Efficiency: {self.efficiency}"
            )

    def toJSON(self):
        return json.dumps(
            {
                "rune_id": self.rune_id,
                "equipped": self.equipped,
                "slot": self.slot,
                "quality": self.quality,
                "nb_stars": self.nb_stars,
                "set": self.set,
                "main_stat_id": self.main_stat_id,
                "innate_stat_id": self.innate_stat_id,
                "innate_stat_value": self.innate_stat_value,
                "substats": [substat.toJSON() for substat in self.substats],
                "efficiency": self.efficiency,
                "max_grind_efficiency": self.max_grind_efficiency,
                "max_gem_efficiency": self.max_gem_efficiency,
            },
            indent=4,
        )


class Modifier:
    """Modifier class
    type: CraftType (ENCHANTED_GEM to ANCIENT_GRINDSTONE)
    set: Set (ENERGY to TOLERANCE)
    stat: Stat (NONE to ACC)
    quality: Quality (NORMAL to LEGEND_ANTIC)
    quantity: int
    """

    def __init__(self, modifier):
        max_char = len(str(modifier["craft_type_id"]))
        self.type = modifier["craft_type"]
        self.set = int(str(modifier["craft_type_id"])[0 : max_char - 4])
        self.stat = int(str(modifier["craft_type_id"])[max_char - 4 : max_char - 2])
        self.quality = int(str(modifier["craft_type_id"])[max_char - 2 : max_char])
        self.quantity = modifier["amount"]

    def __str__(self) -> str:
        if self.type % 2 == 0:
            return f"Grind: {Stat(self.stat).name} {Set(self.set).name} {Quality(self.quality).name}"
        if self.type % 2 == 1:
            return f"Gem: {Stat(self.stat).name} {Set(self.set).name} {Quality(self.quality).name}"

    def toJSON(self):
        return json.dumps(
            {
                "type": self.type,
                "set": self.set,
                "stat": self.stat,
                "quality": self.quality,
                "quantity": self.quantity,
            },
            indent=4,
        )


class Artifact:
    def __init__(self, artifact):
        self.rid = artifact["rid"]
        self.slot = artifact["slot"]
        self.type = artifact["type"]
        self.attribute = artifact["attribute"]
        self.unit_style = artifact["unit_style"]
        self.pri_effects = artifact["pri_effect"]
        self.sec_effects = artifact["sec_effects"]

    def __str__(self):
        attribute_str = Artifact.ATTRIBUTE_STRINGS.get(
            self.attribute, "Unknown Attribute"
        )
        uni_type_str = Artifact.UNIT_STYLES_STRINGS.get(
            self.unit_style, f"Unknown Unit Type: {self.unit_style}"
        )

        sec_effects_str = "\n".join(
            f"  - {Artifact.EFFECT_STRINGS.get(effect[0], 'Unknown Effect').format(effect[1])}"
            for effect in self.sec_effects
        )
        if self.type == 2:  ## If it's a TYPE artifact
            return (
                f"{uni_type_str} {Artifact.MAIN_STAT_STRINGS.get(self.pri_effects[0], 'Unknown main stat')} {self.rid}\n"
                "Secondary Effects:\n" + sec_effects_str
            )
        else:  ## If it's an ATTRIBUTE artifact
            return (
                f"{attribute_str} {Artifact.MAIN_STAT_STRINGS.get(self.pri_effects[0], 'Unknown main stat')} {self.rid}\n"
                "Secondary Effects:\n" + sec_effects_str
            )

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    matchup_chart = {
        1: {"good": 3, "bad": 2},  # Fire
        2: {"good": 1, "bad": 3},  # Water
        3: {"good": 2, "bad": 1},  # Wind
        4: {"good": 5, "bad": 5},  # Light
        5: {"good": 4, "bad": 4},  # Dark
    }

    MAIN_STAT_STRINGS = {
        100: "HP",
        101: "ATK",
        102: "DEF",
    }

    ATTRIBUTE_STRINGS = {
        1: "Water",
        2: "Fire",
        3: "Wind",
        4: "Light",
        5: "Dark",
        98: "Intangible",
    }

    UNIT_STYLES_STRINGS = {
        1: "Attack",
        2: "Defense",
        3: "HP",
        4: "Support",
    }

    EFFECT_STRINGS = {
        200: "ATK+ Proportional to Lost HP up to {}%",
        201: "DEF+ Proportional to Lost HP up to {}%",
        202: "SPD+ Proportional to Lost HP up to {}%",
        203: "SPD Under Inability +{}%",
        204: "ATK Increasing Effect +{}%",
        205: "DEF Increasing Effect +{}%",
        206: "SPD Increasing Effect +{}%",
        207: "CRIT Rate Increasing Effect +{}%",
        208: "Damage Dealt by Counterattack +{}%",
        209: "Damage Dealt by Attacking Together +{}%",
        210: "Bomb Damage +{}%",
        211: "Damage Dealt by Reflect DMG +{}%",
        212: "Crushing Hit DMG +{}%",
        213: "Damage Received Under Inability -{}%",
        214: "CRIT DMG Received -{}%",
        215: "Life Drain +{}%",
        216: "HP when Revived +{}%",
        217: "Attack Bar when Revived +{}%",
        218: "Additional Damage by {}% of HP",
        219: "Additional Damage by {}% of ATK",
        220: "Additional Damage by {}% of DEF",
        221: "Additional Damage by {}% of SPD",
        222: "CRIT DMG+ up to {}% as the enemy's HP condition is good",
        223: "CRIT DMG+ up to {}% as the enemy's HP condition is bad",
        224: "Single-target skill CRIT DMG +{}% on your turn",
        225: "Damage Dealt by Counterattack/Attacking Together +{}%",
        226: "ATK/DEF Increasing Effect +{}%",
        300: "Damage Dealt on Fire +{}%",
        301: "Damage Dealt on Water +{}%",
        302: "Damage Dealt on Wind +{}%",
        303: "Damage Dealt on Light +{}%",
        304: "Damage Dealt on Dark +{}%",
        305: "Damage Received from Fire -{}%",
        306: "Damage Received from Water -{}%",
        307: "Damage Received from Wind -{}%",
        308: "Damage Received from Light -{}%",
        309: "Damage Received from Dark -{}%",
        400: "[Skill 1] CRIT DMG +{}%",
        401: "[Skill 2] CRIT DMG +{}%",
        402: "[Skill 3] CRIT DMG +{}%",
        403: "[Skill 4] CRIT DMG +{}%",
        404: "[Skill 1] Recovery +{}%",
        405: "[Skill 2] Recovery +{}%",
        406: "[Skill 3] Recovery +{}%",
        407: "[Skill 1] Accuracy +{}%",
        408: "[Skill 2] Accuracy +{}%",
        409: "[Skill 3] Accuracy +{}%",
        410: "[Skill 3/4] CRIT DMG +{}%",
        411: "First Attack CRIT DMG +{}%",
    }
