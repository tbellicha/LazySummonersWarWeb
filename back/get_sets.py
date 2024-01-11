from values import Set, nbRunesForSet
from flask import Blueprint, request, jsonify

get_sets_blueprint = Blueprint("get_sets", __name__, url_prefix="/api")


@get_sets_blueprint.route("/get_sets", methods=["GET"])
def get_sets():
    sets = []
    for set in Set:
        sets.append({"set": set.name, "nbRunes": nbRunesForSet[set]})
    return jsonify(sets)
