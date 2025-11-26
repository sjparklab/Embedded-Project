# OpenAI API 호출

from flask import Blueprint, request, jsonify
from app.services.gpt_service import ask_gpt

gpt_bp = Blueprint("gpt", __name__)

@gpt_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    result = ask_gpt(prompt)
    return jsonify({"response": result})