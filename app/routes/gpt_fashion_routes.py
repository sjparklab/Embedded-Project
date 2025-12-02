from flask import Blueprint, request, jsonify
from app.services.gpt_fashion_service import generate_fashion_text

gpt_fashion_bp = Blueprint("gpt_fashion", __name__)

@gpt_fashion_bp.route("/fashion", methods=["POST"])
def fashion_recommendation():
    weather_data = request.get_json()
    result_text = generate_fashion_text(weather_data)

    return jsonify({
        "text": result_text
    })
