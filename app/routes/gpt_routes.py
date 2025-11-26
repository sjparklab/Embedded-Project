# OpenAI API 호출

from flask import Blueprint, request, Response
from flasgger import swag_from
from app.services.gpt_service import ask_gpt_stream

gpt_bp = Blueprint("gpt", __name__)

# GPT 스트리밍 API
@gpt_bp.route("/ask", methods=["POST"])
@swag_from({
    "tags": ["GPT"],
    "description": "GPT-5 Nano 스트리밍 응답 API",
    "consumes": ["application/json"],
    "produces": ["text/plain"],
    "parameters": [
        {
            "name": "prompt",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "스트리밍 텍스트 응답"
        }
    }
})
def ask_stream():
    data = request.get_json()
    prompt = data.get("prompt", "")
    return Response(ask_gpt_stream(prompt), mimetype="text/plain")
