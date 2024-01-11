from enum import Enum


#  ===============  JSON Related  ===============
#  set_id
class Set(Enum):
    ENERGY = 1
    GUARD = 2
    SWIFT = 3
    BLADE = 4
    RAGE = 5
    FOCUS = 6
    ENDURE = 7
    FATAL = 8
    DESPAIR = 10
    VAMPIRE = 11
    VIOLENT = 13
    NEMESIS = 14
    WILL = 15
    SHIELD = 16
    REVENGE = 17
    DESTROY = 18
    FIGHT = 19
    DETERMINATION = 20
    ENHANCE = 21
    ACCURACY = 22
    TOLERANCE = 23
    SEAL = 24
    INTANGIBLE = 25


#  first value of prefix_eff/sec_eff
class Stat(Enum):
    NONE = 0
    HP = 1
    HP_PERCENT = 2
    ATK = 3
    ATK_PERCENT = 4
    DEF = 5
    DEF_PERCENT = 6
    SPD = 8
    CRIT_RATE = 9
    CRIT_DMG = 10
    RES = 11
    ACC = 12


#  rank
class Quality(Enum):
    NORMAL = 1
    MAGIC = 2
    RARE = 3
    HERO = 4
    LEGEND = 5
    NORMAL_ANTIC = 11
    MAGIC_ANTIC = 12
    RARE_ANTIC = 13
    HERO_ANTIC = 14
    LEGEND_ANTIC = 15


#  class
class Stars(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    ONE_ANTIC = 11
    TWO_ANTIC = 12
    THREE_ANTIC = 13
    FOUR_ANTIC = 14
    FIVE_ANTIC = 15
    SIX_ANTIC = 16


#  craft_type
class CraftType(Enum):
    ENCHANTED_GEM = 1
    GRINDSTONE = 2
    IMMEMORIAL_GEM = 3
    IMMEMORIAL_GRINDSTONE = 4
    ANCIENT_GEM = 5
    ANCIENT_GRINDSTONE = 6


#  ===============  Max Values  ===============
coeff_flat = 0.5


class MaxValueStat6(Enum):
    HP = 375 / coeff_flat
    HP_PERCENT = 8
    ATK = 20 / coeff_flat
    ATK_PERCENT = 8
    DEF = 20 / coeff_flat
    DEF_PERCENT = 8
    SPD = 6
    CRIT_RATE = 6
    CRIT_DMG = 7
    RES = 8
    ACC = 8


class MaxValueStat5(Enum):
    HP = 300 / coeff_flat
    HP_PERCENT = 7
    ATK = 15 / coeff_flat
    ATK_PERCENT = 7
    DEF = 15 / coeff_flat
    DEF_PERCENT = 7
    SPD = 5
    CRIT_RATE = 5
    CRIT_DMG = 5
    RES = 7
    ACC = 7


#  ===============  Const Values  ===============
elements = ["Fire", "Water", "Wind", "Light", "Dark"]
parameters = {
    elements[0]: {
        "min_natural_stars": 4,
        "min_current_stars": 6,
        "min_awake_level": 1,
    },
    elements[1]: {
        "min_natural_stars": 4,
        "min_current_stars": 6,
        "min_awake_level": 1,
    },
    elements[2]: {
        "min_natural_stars": 4,
        "min_current_stars": 6,
        "min_awake_level": 1,
    },
    elements[3]: {
        "min_natural_stars": 4,
        "min_current_stars": 6,
        "min_awake_level": 1,
    },
    elements[4]: {
        "min_natural_stars": 4,
        "min_current_stars": 6,
        "min_awake_level": 1,
    },
}

nbRunesForSet = {
    Set.ENERGY: 2,
    Set.GUARD: 2,
    Set.SWIFT: 4,
    Set.BLADE: 2,
    Set.RAGE: 4,
    Set.FOCUS: 2,
    Set.ENDURE: 2,
    Set.FATAL: 4,
    Set.DESPAIR: 4,
    Set.VAMPIRE: 4,
    Set.VIOLENT: 4,
    Set.NEMESIS: 2,
    Set.WILL: 2,
    Set.SHIELD: 2,
    Set.REVENGE: 2,
    Set.DESTROY: 2,
    Set.FIGHT: 2,
    Set.DETERMINATION: 2,
    Set.ENHANCE: 2,
    Set.ACCURACY: 2,
    Set.TOLERANCE: 2,
    Set.SEAL: 2,
    Set.INTANGIBLE: 1,
}

podValues = {
    "Sets": {
        "ALL": 1,
        "DESPAIR": 2,
        "DESTROY": 2,
        "VIOLENT": 3,
        "WILL": 3,
    },
    "Eff": {
        "130": 4,
        "120": 3,
        "110": 2,
        "100": 1,
    },
}