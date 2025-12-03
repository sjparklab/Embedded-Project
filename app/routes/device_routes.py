## 라즈베리파이에서 api 요청

from flask import Blueprint, request, jsonify
from app.services.device_service import read_sensor_data, get_latest_sensor_data

device_bp = Blueprint('device', __name__, url_prefix='/api/device')

@device_bp.get('/sensor')
def get_sensor():
    """Sense HAT에서 온도/습도를 읽어서 반환"""
    data = read_sensor_data()
    return jsonify(data)

@device_bp.get('/sensor/latest')
def get_latest_sensor():
    """저장된 최신 센서 데이터 반환 (센서 재읽기 없이)"""
    data = get_latest_sensor_data()
    return jsonify(data)

@device_bp.post('/temperature')
def receive_temp():
    data = request.json
    print('Raspberry Pi temperature:', data)
    return jsonify({'status': 'received'})

# api 호출 테스트
@device_bp.route("/test", methods=["GET"])
def test():
    return {"message": "API OK"}

