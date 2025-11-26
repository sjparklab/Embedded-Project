## 라즈베리파이에서 api 요청

from flask import Blueprint, request, jsonify

device_bp = Blueprint('device', __name__, url_prefix='/api/device')

@device_bp.post('/temperature')
def receive_temp():
    data = request.json
    print('Raspberry Pi temperature:', data)
    return jsonify({'status': 'received'})

# api 호출 테스트
@device_bp.route("/test", methods=["GET"])
def test():
    return {"message": "API OK"}

