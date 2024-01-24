class ArtifactsInfo {
  late final List<int> attributes; // Water, Fire, Wind, Light, Dark
  late final List<int> mainStats; // HP, ATK, DEF
  late final List<int> unitStyles; // Attack, Defense, Support, HP

  ArtifactsInfo({
    required this.attributes,
    required this.mainStats,
    required this.unitStyles,
  });
}

class Artifact {
  double rid;
  int slot;
  int type;
  int attribute;
  int unitStyle;
  List<int> priEffects;
  List<List<double>> secEffects;

  Artifact({
    required this.rid,
    required this.slot,
    required this.type,
    required this.attribute,
    required this.unitStyle,
    required this.priEffects,
    required this.secEffects,
  });

  @override
  String toString() {
    String attributeStr = attributeStrings.containsKey(attribute)
        ? attributeStrings[attribute]!
        : "Unknown Attribute";
    String unitStyleStr = unitStyleStrings.containsKey(unitStyle)
        ? unitStyleStrings[unitStyle]!
        : "Unknown Unit Style: $unitStyle";

    String secEffectsStr = secEffects.map((effect) {
      String effectStr = effectStrings.containsKey(effect[0])
          ? effectStrings[effect[0]]!
          : "Unknown Effect";
      return "\t- ${effectStr.replaceAll('{}', effect[1].toString())}";
    }).join('\n');

    if (type == 2) {
      return '$unitStyleStr ${mainStatStrings[priEffects[0]] ?? 'Unknown main stat'} $rid\n'
          'Secondary Effects:\n$secEffectsStr';
    } else {
      return '$attributeStr ${mainStatStrings[priEffects[0]] ?? 'Unknown main stat'} $rid\n'
          'Secondary Effects:\n$secEffectsStr';
    }
  }

  static Artifact fromJson(Map<String, dynamic> artifactData) {
    try {
      double rid = artifactData['rid'];
      int slot = artifactData['slot'];
      int type = artifactData['type'];
      int attribute = artifactData['attribute'];
      int unitStyle = artifactData['unit_style'];
      List<int> priEffects = List<int>.from(artifactData['pri_effects']);
      List<List<double>> secEffects = List<List<double>>.from(
        (artifactData['sec_effects'] as List).map(
          (item) => List<double>.from(item),
        ),
      );

      return Artifact(
        rid: rid,
        slot: slot,
        type: type,
        attribute: attribute,
        unitStyle: unitStyle,
        priEffects: priEffects,
        secEffects: secEffects,
      );
    } catch (e, stacktrace) {
      print('Artifact.fromJson: ${e.toString()} ($artifactData)');
      print(stacktrace);
      return Artifact(
        rid: -1,
        slot: -1,
        type: -1,
        attribute: -1,
        unitStyle: 0,
        priEffects: [],
        secEffects: [],
      );
    }
  }

  static final Map<int, Map<String, int>> matchupChart = {
    1: {"good": 3, "bad": 2}, // Fire
    2: {"good": 1, "bad": 3}, // Water
    3: {"good": 2, "bad": 1}, // Wind
    4: {"good": 5, "bad": 5}, // Light
    5: {"good": 4, "bad": 4}, // Dark
  };

  static final Map<int, String> mainStatStrings = {
    100: "HP",
    101: "ATK",
    102: "DEF",
  };

  static final Map<int, String> attributeStrings = {
    1: "Water",
    2: "Fire",
    3: "Wind",
    4: "Light",
    5: "Dark",
    98: "Intangible",
  };

  static final Map<int, String> unitStyleStrings = {
    1: "Attack",
    2: "Defense",
    3: "HP",
    4: "Support",
  };

  static final Map<int, String> artifactTypeStrings = {
    1: "Attribute",
    2: "Unit Style",
  };

  static final Map<int, String> effectStrings = {
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
  };
}
