from flask import Blueprint, jsonify, request
from app.services.gpt_environment_service import generate_environment_text
from app.services.gpt_fashion_service import generate_fashion_text
from app.services.device_service import display_icon_by_keyword

demo_bp = Blueprint("demo", __name__)

@demo_bp.route("/execute", methods=["POST"])
def execute_demo():
    """
    데모용 엔드포인트
    프론트엔드로부터 받은 '가상 날씨 데이터'로 GPT를 호출하고
    SenseHAT 아이콘을 업데이트함.
    """
    data = request.json
    mode = data.get("mode") # 'environment' 또는 'fashion'
    fake_weather = data.get("weatherData")

    if not mode or not fake_weather:
        return jsonify({"error": "Missing mode or weatherData"}), 400

    try:
        if mode == "environment":
            result = generate_environment_text(fake_weather)
        elif mode == "fashion":
            result = generate_fashion_text(fake_weather)
        else:
            return jsonify({"error": "Invalid mode"}), 400

        # 결과 처리 (딕셔너리 or 문자열)
        if isinstance(result, dict):
            advice = result.get("advice", "")
            keyword = result.get("keyword", "NORMAL")
        else:
            advice = result
            keyword = "NORMAL"

        # SenseHAT 업데이트 (핵심: 가상 데이터로 실제 하드웨어 제어)
        display_icon_by_keyword(keyword)

        return jsonify({
            "success": True,
            "text": advice,
            "keyword": keyword
        })

    except Exception as e:
        print(f"[DEMO] Error executing demo: {e}")
        return jsonify({"error": str(e)}), 500
