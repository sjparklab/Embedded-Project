from flask import Blueprint, jsonify
from app.services.weather_service import get_weather_data
from app.services.gpt_environment_service import generate_environment_text

gpt_environment_bp = Blueprint("gpt_environment", __name__)

@gpt_environment_bp.route("/environment", methods=["POST"])
def environment_recommendation():
    # 🌡 STEP 1 — 센서 OR OpenWeather 자동 선택
    weather_data = get_weather_data()  # ← 핵심!!

    # 🌧 STEP 2 — GPT로 조언 생성
    result_text = generate_environment_text(weather_data)

    return jsonify({
        "text": result_text
    })