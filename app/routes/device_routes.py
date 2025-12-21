## 라즈베리파이에서 api 요청

from flask import Blueprint, request, jsonify
from app.services.device_service import read_sensor_data, get_latest_sensor_data, read_co2_sensor
from app.services.person_detection_service import detect_person_from_webcam, get_latest_detection
from app.scheduler import scheduled_person_detection

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

@device_bp.get('/co2')
def get_co2():
    """UART를 통해 CO2 센서에서 데이터를 읽어서 반환"""
    data = read_co2_sensor()
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

@device_bp.get('/person-detect')
def person_detect():
    """웹캠으로 사람이 있는지 감지"""
    data = detect_person_from_webcam()
    return jsonify(data)

@device_bp.post('/person-detect/trigger')
def trigger_person_detect_action():
    """사람 감지 및 환경 조언 로직을 수동으로 트리거"""
    result = scheduled_person_detection()
    return jsonify({
        "message": "Scheduled task triggered manually",
        "detection_result": result
    })

@device_bp.get('/person-detect/latest')
def get_latest_person_detection():
    """저장된 최신 사람 감지 결과 반환 (재감지 없이)"""
    data = get_latest_detection()
    return jsonify(data)

