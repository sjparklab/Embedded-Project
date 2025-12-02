from flask import Blueprint, jsonify
import json
import os

cities_bp = Blueprint("cities", __name__)

@cities_bp.route("/", methods=["GET"])
def get_cities():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "cities.json")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data)
