from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services.weather_service import get_current_weather, get_weather_data
from app.services.settings_service import load_settings

weather_bp = Blueprint("weather", __name__)


# ============================
# ⭐ 기존 /current API (그대로 유지)
# ============================
@weather_bp.route("/current", methods=["GET"])
@swag_from({
    "tags": ["Weather"],
    "description": "선택된 도시의 날씨 + 센서 CO₂ 데이터를 반환",
    "parameters": [
        {
            "name": "city_id",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "OpenWeather 도시 ID (없으면 settings.json 사용)"
        }
    ],
    "responses": {
        200: {
            "description": "대시보드에서 사용하는 데이터",
            "schema": {
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"},
                    "humidity": {"type": "number"},
                    "pressure": {"type": "number"},
                    "co2": {"type": "number"},
                    "weather": {"type": "string"},
                    "description": {"type": "string"},
                    "location": {"type": "string"}
                }
            }
        }
    }
})
def current_weather():
    city_id = request.args.get("city_id")
    unit = request.args.get("unit", "celsius")

    if not city_id:
        settings = load_settings()
        city_id = settings.get("location")

    weather = get_current_weather(city_id, unit)
    return jsonify(weather)


# ============================
# ⭐ 신규 /dashboard API
# React에서는 이걸 사용해야 함
# ============================
@weather_bp.route("/dashboard", methods=["GET"])
def dashboard_weather():
    """
    React 대시보드에서 사용하는 데이터 반환
    (get_weather_data()가 이미 프론트에서 기대하는 키 구조를 맞춰줌)
    """
    data = get_weather_data()
    return jsonify(data)