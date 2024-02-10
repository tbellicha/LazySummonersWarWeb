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
            [{"artifact": {}, "value": 0} for m in range(len(req_sub_stats))]
            for k in range(size)
        ]
        for i, _ in enumerate(Artifact.ATTRIBUTE_STRINGS.items())
    ]
    # List to not duplicate artifacts in the response
    artifacts_list = []
    # Get the best sub_stats of artifacts of each attribute
    for i, attribute in enumerate(Artifact.ATTRIBUTE_STRINGS.items()):
        artifacts_list.clear()
        for k in range(size):
            for m, req_substat in enumerate(req_sub_stats):
                curr_best_value = response[i][k][m]["value"]
                curr_best_artifact = {}
                for artifact in filtered_artifacts:
                    if artifact.attribute != attribute[0]:
                        continue
                    # Get {size} bests artifact for each {req_sub_stats} in each of the {Artifact.ATTRIBUTE_STRINGS.items()}
                    for o, artif_substat in enumerate(artifact.sec_effects):
                        if artif_substat[0] == req_substat:
                            if (
                                artif_substat[1] >= curr_best_value
                                and artifact not in artifacts_list
                            ):
                                response[i][k][m]["artifact"] = artifact.toJSON()
                                if curr_best_artifact in artifacts_list:
                                    artifacts_list.remove(curr_best_artifact)
                                curr_best_value = artif_substat[1]
                                curr_best_artifact = artifact
                                artifacts_list.append(artifact)
                                break
                response[i][k][m]["value"] = curr_best_value
    return jsonify(response)


def artifact_best_unit_styles(filtered_artifacts, req_sub_stats, size):
    response = [
        [
            [{"artifact": {}, "value": 0} for m in range(len(req_sub_stats))]
            for k in range(size)
        ]
        for i, _ in enumerate(Artifact.UNIT_STYLES_STRINGS.items())
    ]
    # List to not duplicate artifacts in the response
    artifacts_list = []
    # Get the best sub_stats of artifacts of each attribute
    for i, unit_style in enumerate(Artifact.UNIT_STYLES_STRINGS.items()):
        artifacts_list.clear()
        for k in range(size):
            for m, req_substat in enumerate(req_sub_stats):
                curr_best_value = response[i][k][m]["value"]
                curr_best_artifact = {}
                for artifact in filtered_artifacts:
                    if artifact.unit_style != unit_style[0]:
                        continue
                    # Get {size} bests artifact for each {req_sub_stats} in each of the {Artifact.ATTRIBUTE_STRINGS.items()}
                    for o, artif_substat in enumerate(artifact.sec_effects):
                        if artif_substat[0] == req_substat:
                            if (
                                artif_substat[1] >= curr_best_value
                                and artifact not in artifacts_list
                            ):
                                response[i][k][m]["artifact"] = artifact.toJSON()
                                if curr_best_artifact in artifacts_list:
                                    artifacts_list.remove(curr_best_artifact)
                                curr_best_value = artif_substat[1]
                                curr_best_artifact = artifact
                                artifacts_list.append(artifact)
                                break
                response[i][k][m]["value"] = curr_best_value
    return jsonify(response)


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
        req_sub_stats = ast.literal_eval(sub_stats_param)
        if not isinstance(req_sub_stats, list) or not all(
            isinstance(stat, int) for stat in req_sub_stats
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
            if curr_substat[0] in req_sub_stats:
                filtered_artifacts.append(artifact)
                break
    if type == 1:
        return artifact_best_attributes(filtered_artifacts, req_sub_stats, size)
    return artifact_best_unit_styles(filtered_artifacts, req_sub_stats, size)
