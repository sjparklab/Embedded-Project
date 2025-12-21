import threading

try:
    from sense_hat import SenseHat
    sense = SenseHat()
    SENSEHAT_AVAILABLE = True
except (ImportError, Exception) as e:
    sense = None
    SENSEHAT_AVAILABLE = False
    print(f"Warning: sense_hat library not available ({e}). Using mock data.")

# LED 자동 끄기 타이머 관련
LED_TIMEOUT_SECONDS = 30
_led_timer = None
_led_timer_lock = threading.Lock()

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("Warning: pyserial library not available. CO2 sensor will use mock data.")

# CO2 센서 UART 설정
SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 9600
_serial_lock = threading.Lock()

# 최근 센서 데이터를 저장 (내부적으로 사용)
latest_sensor_data = {
    "temperature": None,
    "humidity": None,
    "co2": None,
    "timestamp": None
}

def read_sensor_data():
    """Sense HAT에서 온도와 습도를 읽고, CO2 센서도 함께 읽어옴"""
    from datetime import datetime
    import random

    # 1. Sense HAT 온도/습도 읽기
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

    # 2. CO2 센서 읽기
    co2_value = _read_co2_internal()

    # 3. 내부적으로 최신 데이터 저장
    latest_sensor_data["temperature"] = round(temp, 2)
    latest_sensor_data["humidity"] = round(humidity, 2)
    latest_sensor_data["co2"] = co2_value
    latest_sensor_data["timestamp"] = datetime.now().isoformat()

    return latest_sensor_data.copy()

def get_latest_sensor_data():
    """저장된 최신 센서 데이터 반환"""
    return latest_sensor_data.copy()

def _read_co2_internal():
    """내부용: CO2 센서 값만 읽어서 반환 (저장하지 않음)"""
    import random

    if SERIAL_AVAILABLE:
        with _serial_lock:
            try:
                # 시리얼 포트 열기
                ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

                # CO2 읽기 명령 (Hex: 11 01 01 ED)
                cmd = bytearray([0x11, 0x01, 0x01, 0xED])

                # 명령 전송
                ser.write(cmd)

                # 응답 데이터 읽기 (8바이트)
                response = ser.read(8)

                if len(response) == 8:
                    # CO2 농도 = DF1 * 256 + DF2
                    co2_value = response[3] * 256 + response[4]
                    print(f"현재 CO2 농도: {co2_value} ppm")
                else:
                    print("[WARNING] CO2 센서 응답 없음. Mock 데이터를 사용합니다.")
                    co2_value = random.randint(400, 1000)

                ser.close()
                return co2_value

            except Exception as e:
                print(f"[ERROR] CO2 센서 읽기 실패: {e}")
                print("[INFO] Mock 데이터를 사용합니다.")
                return random.randint(400, 1000)
    else:
        # pyserial 없을 때 mock 데이터
        print("[INFO] pyserial이 설치되지 않았습니다. Mock 데이터를 사용합니다.")
        return random.randint(400, 1000)

def read_co2_sensor():
    """UART를 통해 CO2 센서에서 데이터를 읽어옴 (API 엔드포인트용)"""
    from datetime import datetime

    # CO2 센서 읽기
    co2_value = _read_co2_internal()

    # 내부적으로 최신 데이터 저장
    latest_sensor_data["co2"] = co2_value
    latest_sensor_data["timestamp"] = datetime.now().isoformat()

    return {
        "co2": co2_value,
        "timestamp": latest_sensor_data["timestamp"]
    }
    
blue = (0, 150, 255)
red = (255, 0, 0)
nothing = (0,0,0)

def umbrella():
    if not SENSEHAT_AVAILABLE:
        print("[MOCK] Displaying umbrella icon")
        return
    B = blue
    O = nothing
    img = [
    O, O, O, B, B, O, O, O,
    O, O, B, B, B, B, O, O,
    O, B, B, B, B, B, B, O,
    B, B, B, B, B, B, B, B,
    O, O, O, O, B, O, O, O,
    O, O, O, O, B, O, O, O,
    O, O, B, O, B, O, O, O,
    O, O, B, B, B, O, O, O
    ]
    sense.set_pixels(img)

def window():
    if not SENSEHAT_AVAILABLE:
        print("[MOCK] Displaying window icon")
        return
    B = blue
    O = nothing
    img = [
    O, O, O, O, O, O, O, O,
    O, B, B, B, O, B, B, B,
    O, B, B, B, O, B, B, B,
    O, B, B, B, O, B, B, B,
    O, O, O, O, O, O, O, O,
    O, B, B, B, O, B, B, B,
    O, B, B, B, O, B, B, B,
    O, B, B, B, O, B, B, B
    ]
    sense.set_pixels(img)

def cold():
    if not SENSEHAT_AVAILABLE:
        print("[MOCK] Displaying cold icon")
        return
    B = blue
    O = nothing
    img = [
    O, B, O, O, B, O, O, B,
    O, O, B, O, B, O, B, O,
    O, O, O, B, B, B, O, O,
    O, B, B, B, B, B, B, B,
    O, O, O, B, B, B, O, O,
    O, O, B, O, B, O, B, O,
    O, B, O, O, B, O, O, B,
    O, O, O, O, O, O, O, O
    ]
    sense.set_pixels(img)

def hot():
    if not SENSEHAT_AVAILABLE:
        print("[MOCK] Displaying hot icon")
        return
    B = red
    O = nothing
    img = [
    O, B, O, O, B, O, O, B,
    O, O, B, O, B, O, B, O,
    O, O, O, B, B, B, O, O,
    O, B, B, B, B, B, B, B,
    O, O, O, B, B, B, O, O,
    O, O, B, O, B, O, B, O,
    O, B, O, O, B, O, O, B,
    O, O, O, O, O, O, O, O
    ]
    sense.set_pixels(img)

def clear_display():
    """LED 디스플레이를 끕니다."""
    if SENSEHAT_AVAILABLE:
        sense.clear()
    else:
        print("[MOCK] Clearing display")

def _cancel_led_timer():
    """기존 LED 타이머가 있으면 취소합니다."""
    global _led_timer
    with _led_timer_lock:
        if _led_timer is not None:
            _led_timer.cancel()
            _led_timer = None

def _start_led_timer():
    """LED를 15초 후 자동으로 끄는 타이머를 시작합니다."""
    global _led_timer
    _cancel_led_timer()
    with _led_timer_lock:
        _led_timer = threading.Timer(LED_TIMEOUT_SECONDS, _auto_clear_display)
        _led_timer.daemon = True
        _led_timer.start()
        print(f"[LED] 타이머 시작: {LED_TIMEOUT_SECONDS}초 후 자동 꺼짐")

def _auto_clear_display():
    """타이머에 의해 호출되어 LED를 끕니다."""
    global _led_timer
    with _led_timer_lock:
        _led_timer = None
    print("[LED] 타이머 만료: 디스플레이 끄기")
    if SENSEHAT_AVAILABLE:
        sense.clear()
    else:
        print("[MOCK] Auto-clearing display after timeout")

def display_icon_by_keyword(keyword):
    """GPT 키워드에 따라 SenseHAT에 아이콘을 표시하고 15초 후 자동으로 끕니다."""
    if not SENSEHAT_AVAILABLE:
        print(f"[MOCK] Displaying icon for keyword: {keyword}")
        # Mock 환경에서도 타이머 동작 테스트
        if keyword not in ("NORMAL", None, ""):
            _start_led_timer()
        return

    if keyword == "VENTILATION":
        window()
        _start_led_timer()
    elif keyword == "HEATING":
        hot()  # 난방 (따뜻함)
        _start_led_timer()
    elif keyword == "COOLING":
        cold() # 냉방 (시원함)
        _start_led_timer()
    elif keyword == "UMBRELLA":
        umbrella()
        _start_led_timer()
    elif keyword == "COLD":
        cold()
        _start_led_timer()
    elif keyword == "HOT":
        hot()
        _start_led_timer()
    else:
        _cancel_led_timer()
        clear_display()
