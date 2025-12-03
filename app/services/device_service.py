# 라즈베리파이 센서 제어 및 API 제작시 여기 삽입

try:
    from sense_hat import SenseHat
    sense = SenseHat()
    SENSEHAT_AVAILABLE = True
except ImportError:
    SENSEHAT_AVAILABLE = False
    print("Warning: sense_hat library not available. Using mock data.")

# 최근 센서 데이터를 저장 (내부적으로 사용)
latest_sensor_data = {
    "temperature": None,
    "humidity": None,
    "timestamp": None
}

def read_sensor_data():
    """Sense HAT에서 온도와 습도를 읽어옴"""
    from datetime import datetime
    import random

    if SENSEHAT_AVAILABLE:
        try:
            temp = sense.get_temperature()
            humidity = sense.get_humidity()
        except Exception as e:
            print(f"[ERROR] Sense HAT 센서 읽기 실패: {e}")
            print("[INFO] Mock 데이터를 사용합니다.")
            temp = round(20 + random.uniform(-5, 5), 2)
            humidity = round(50 + random.uniform(-10, 10), 2)
    else:
        # 개발 환경용 목(mock) 데이터
        print("[INFO] Sense HAT이 연결되지 않았습니다. Mock 데이터를 사용합니다.")
        temp = round(20 + random.uniform(-5, 5), 2)
        humidity = round(50 + random.uniform(-10, 10), 2)

    # 내부적으로 최신 데이터 저장
    latest_sensor_data["temperature"] = round(temp, 2)
    latest_sensor_data["humidity"] = round(humidity, 2)
    latest_sensor_data["timestamp"] = datetime.now().isoformat()

    return latest_sensor_data.copy()

def get_latest_sensor_data():
    """저장된 최신 센서 데이터 반환"""
    return latest_sensor_data.copy()
