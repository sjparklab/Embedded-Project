from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services.weather_service import get_current_weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/current", methods=["GET"])
@swag_from({
    "tags": ["Weather"],
    "description": "현재 날씨 정보를 조회하는 API",
    "parameters": [
        {
            "name": "city",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "조회할 도시 이름 (기본값: .env 의 DEFAULT_CITY)"
        }
    ],
    "responses": {
        200: {
            "description": "성공적으로 조회된 현재 날씨 정보",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "main": {
                        "type": "object",
                        "properties": {
                            "temp": {"type": "number"},
                            "humidity": {"type": "number"}
                        }
                    },
                    "weather": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
})
def current_weather():
    city = request.args.get("city")
    result = get_current_weather(city)
    return jsonify(result)
