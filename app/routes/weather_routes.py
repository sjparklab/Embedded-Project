from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services.weather_service import get_current_weather
from app.services.settings_service import load_settings

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/current", methods=["GET"])
@swag_from({
    "tags": ["Weather"],
    "description": "선택된 도시의 날씨를 조회하는 API",
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
            "description": "React WeatherCard가 사용하는 구조의 데이터",
            "schema": {
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"},
                    "humidity": {"type": "number"},
                    "pressure": {"type": "number"},
                    "co2": {"type": "number"},
                    "weather_main": {"type": "string"},
                    "weather_description": {"type": "string"},
                    "location_ko": {"type": "string"}
                }
            }
        }
    }
})
def current_weather():
    city_id = request.args.get("city_id")
    unit = request.args.get("unit", "celsius")

    settings = load_settings()
    if not city_id:
        city_id = settings.get("location")

    weather_data = get_current_weather(city_id, unit)
    return jsonify(weather_data)
