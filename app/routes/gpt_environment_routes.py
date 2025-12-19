from flask import Blueprint, jsonify
from app.services.weather_service import get_weather_data
from app.services.gpt_environment_service import generate_environment_text
from app.services.device_service import display_icon_by_keyword

gpt_environment_bp = Blueprint("gpt_environment", __name__)

@gpt_environment_bp.route("/environment", methods=["POST"])
def environment_recommendation():
    # 🌡 STEP 1 — 센서 OR OpenWeather 자동 선택
    weather_data = get_weather_data()  # ← 핵심!!

    # 🌧 STEP 2 — GPT로 조언 생성
    result = generate_environment_text(weather_data)

    # 문자열 또는 딕셔너리 대응
    if isinstance(result, dict):
        advice = result.get("advice", "")
        keyword = result.get("keyword", "NORMAL")
    else:
        advice = result
        keyword = "NORMAL"

    # 💡 STEP 3 — SenseHAT 아이콘 표시 (웹 요청 시에도 반영)
    display_icon_by_keyword(keyword)

    return jsonify({
        "text": advice,
        "keyword": keyword
    })

