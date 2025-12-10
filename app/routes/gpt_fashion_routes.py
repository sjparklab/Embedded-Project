from flask import Blueprint, jsonify
from app.services.weather_service import get_weather_data
from app.services.gpt_fashion_service import generate_fashion_text

gpt_fashion_bp = Blueprint("gpt_fashion", __name__)

@gpt_fashion_bp.route("/fashion", methods=["POST"])
def fashion_recommendation():
    # 🌡 STEP 1 — 센서 OR OpenWeather 자동 선택
    weather_data = get_weather_data()  # ← 핵심!!

    # 👗 STEP 2 — GPT로 텍스트 생성
    result_text = generate_fashion_text(weather_data)

    return jsonify({
        "text": result_text
    })