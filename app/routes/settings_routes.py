from flask import Blueprint, request, jsonify
from app.services.settings_service import load_settings, save_settings

settings_bp = Blueprint("settings", __name__)

# ------------------------
# GET /api/settings  /api/settings/
# ------------------------
@settings_bp.route("", methods=["GET"])
@settings_bp.route("/", methods=["GET"])
def get_settings():
    settings = load_settings()
    return jsonify(settings)


# ------------------------
# POST /api/settings  /api/settings/
# ------------------------
@settings_bp.route("", methods=["POST"])
@settings_bp.route("/", methods=["POST"])
def update_settings():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    save_settings(data)
    return jsonify({"message": "Settings updated successfully"})
