from flask import Flask, request, jsonify
from flask_cors import CORS
from load_json import load_json_blueprint, auto_load_json
from get_sets import get_sets_blueprint
from get_bests_artifacts import get_bests_artifacts_blueprint
from classes import *
from values import *

app = Flask("localhost")
CORS(app)

app.register_blueprint(load_json_blueprint)
app.register_blueprint(get_sets_blueprint)
app.register_blueprint(get_bests_artifacts_blueprint)


def main(argc, argv):
    auto_load_json()
    app.run(debug=True)
