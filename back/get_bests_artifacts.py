# Import necessary modules and data
from classes import Artifact
from flask import Blueprint, request, jsonify
from load_json import all_account_artifacts
import ast

# Create Blueprint
get_bests_artifacts_blueprint = Blueprint(
    "get_bests_artifacts", __name__, url_prefix="/api"
)


def artifact_best_attributes(filtered_artifacts, req_sub_stats, size):
    response = [
        [
            [{"artifact": {}, "value": 0} for i in range(size)]
            for k in range(len(req_sub_stats))
        ]
        for m in range(len(Artifact.ATTRIBUTE_STRINGS.items()))
    ]
    # Get the best sub_stats of artifacts of each attribute
    for artifact in filtered_artifacts:
        for i, (attribute_id, attribute_string) in enumerate(
            Artifact.ATTRIBUTE_STRINGS.items()
        ):
            # if the current artifact is of the current attribute
            if artifact.attribute == attribute_id:
                for k, req_substat in enumerate(req_sub_stats):
                    # if the current artifact has the current substat
                    for m, substat_effect in enumerate(artifact.sec_effects):
                        if substat_effect[0] == req_substat:
                            # if the current artifact has a better value for the current substat than the worst artifact in the list
                            if substat_effect[1] > response[i][k][size - 1]["value"]:
                                # if the current artifact is not already in the list
                                if artifact not in response[i][k]:
                                    response[i][k].append(
                                        {
                                            "artifact": artifact.toJSON(),
                                            "value": substat_effect[1],
                                        }
                                    )
                                    response[i][k].sort(
                                        key=lambda x: x["value"], reverse=True
                                    )
                                    response[i][k] = response[i][k][:size]
                                    break
    return jsonify(response)


def artifact_best_unit_styles():
    response = [[]]
    return


# Sort the artifacts by the substat received in the request, and return the best ones
@get_bests_artifacts_blueprint.route("/get_bests_artifacts", methods=["GET"])
def get_bests_artifacts():
    size = request.args.get("size", default=0, type=int)
    if size == 0:
        return "Error: size not found in request", 400
    mainstat = request.args.get("main_stat", 0, type=int)
    sub_stats_param = request.args.get("sub_stats", "", type=str)
    type = request.args.get("type", 0, type=int)
    try:
        sub_stats = ast.literal_eval(sub_stats_param)
        if not isinstance(sub_stats, list) or not all(
            isinstance(stat, int) for stat in sub_stats
        ):
            raise ValueError("Invalid value for 'sub_stats'")
    except (ValueError, SyntaxError):
        return jsonify({"error": "Invalid 'sub_stats' parameter"}), 400

    # Filter and sort artifacts based on the specified parameters
    filtered_artifacts = []
    for artifact in all_account_artifacts:
        if (type != 0 and artifact.type != type) or (
            mainstat != 0 and artifact.pri_effects[0] != mainstat
        ):
            continue
        for i, curr_substat in enumerate(artifact.sec_effects):
            if curr_substat[0] in sub_stats:
                filtered_artifacts.append(artifact)
                break
    if type == 1:
        return artifact_best_attributes(filtered_artifacts, sub_stats, size)
    return artifact_best_unit_styles(filtered_artifacts, sub_stats, size)

    # for i, artifact in enumerate(filtered_artifacts):
    #     if artifact.attribute == 1:
    #         if len(fire) < size:
    #             fire.append(artifact)
    #         else:
    #             for artifact in fire:
    #                 print(artifact)
    #             for curr_best_artif in reversed(fire):
    #                 for k, substat_effect in enumerate(curr_best_artif.sec_effects):
    #                     if substat in Artifact.EFFECT_STRINGS.get(
    #                         substat_effect[0], ""
    #                     ):
    #                         if (
    #                             substat_effect[1]
    #                             > artifact.sec_effects[subs_indexes[i]][1]
    #                         ):
    #                             fire.remove(curr_best_artif)
    #                             fire.append(artifact)
    #                             break
    #             for artifact in fire:
    #                 print(artifact)
    #             break
