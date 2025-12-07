from flask import Blueprint, request, jsonify
from flasgger import swag_from
import logging

tts_bp = Blueprint('tts', __name__)
logger = logging.getLogger(__name__)

@tts_bp.route('/speak', methods=['POST'])
def speak():
    """
    TTS 음성 재생 (라즈베리파이 스피커 출력)
    ---
    tags:
      - TTS
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              description: 음성으로 변환할 텍스트
              example: "오늘의 날씨는 맑고 기온은 20도입니다."
    responses:
      200:
        description: 음성 재생 성공
        schema:
          type: object
          properties:
            message:
              type: string
              example: "TTS 재생 완료"
      400:
        description: 잘못된 요청
      500:
        description: 서버 오류
    """
    try:
        data = request.get_json()
        text = data.get('text')

        if not text:
            return jsonify({"error": "텍스트가 필요합니다."}), 400

        # TTS 서비스 호출
        from app.services.tts_service import play_tts
        play_tts(text)

        return jsonify({"message": "TTS 재생 완료"}), 200

    except Exception as e:
        logger.error(f"TTS 재생 오류: {str(e)}")
        return jsonify({"error": str(e)}), 500
