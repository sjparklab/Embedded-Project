from flask import Blueprint, jsonify, request
from flasgger import swag_from
from app.services.weather_service import get_current_weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/current", methods=["GET"])
@swag_from({
    "tags": ["Weather"],
    "description": "현재 날씨 정보를 조회합니다.",
    "parameters": [
        {
            "name": "city",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "도시 이름 (기본값: .env에 설정된 DEFAULT_CITY)"
        }
    ],
    "responses": {
        200: {
            "description": "성공적으로 날씨 정보를 반환합니다.",
            "examples": {
                "application/json": {
                    "name": "Busan",
                    "main": {
                        "temp": 17.3,
                        "humidity": 52
                    },
                    "weather": [
                        {"description": "broken clouds"}
                    ]
                }
            }
        }
    }
})
def current_weather():
    city = request.args.get("city")

    # city=None 이면 weather_service에서 DEFAULT_CITY 사용
    result = get_current_weather(city)

    return jsonify(result)
