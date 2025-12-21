import threading
import time
from app.services.device_service import SENSEHAT_AVAILABLE, sense, display_icon_by_keyword, clear_display
from app.services.weather_service import get_weather_data
from app.services.gpt_environment_service import generate_environment_text
from app.services.gpt_fashion_service import generate_fashion_text
from app.services.tts_service import play_tts, stop_tts

def handle_joystick():
    """조이스틱 이벤트를 무한 루프로 감시하는 함수"""
    global stop_requested

    if not SENSEHAT_AVAILABLE:
        print("[JOYSTICK] SenseHAT을 사용할 수 없어 조이스틱 핸들러를 시작하지 않습니다.")
        return

    if sense is None:
        print("[JOYSTICK] sense 객체가 None입니다. 조이스틱 핸들러를 시작하지 않습니다.")
        return

    print("[JOYSTICK] 조이스틱 핸들러 시작됨 (왼쪽: 환경 조언, 오른쪽: 복장 조언)")

    while True:
        try:
            # 이벤트를 하나씩 가져옴 (block=True로 설정하면 이벤트가 올 때까지 대기)
            for event in sense.stick.get_events():
                # 누름(pressed) 또는 누르고 있음(held) 상태일 때 동작
                if event.action in ('pressed', 'held'):
                    if event.direction == 'left':
                        print("[JOYSTICK] ⬅️ 왼쪽 감지: 실내 환경 조언 생성 중...")
                        stop_requested = False
                        threading.Thread(target=process_environment_advice).start()
                    elif event.direction == 'right':
                        print("[JOYSTICK] ➡️ 오른쪽 감지: 외출 복장 조언 생성 중...")
                        stop_requested = False
                        threading.Thread(target=process_fashion_advice).start()
                    elif event.direction == 'middle':
                        print("[JOYSTICK] ⏺ 가운데 감지: 디스플레이 및 TTS 중단")
                        stop_requested = True
                        stop_tts()
                        clear_display()
        except Exception as e:
            print(f"[JOYSTICK] 이벤트 처리 중 오류 발생: {e}")

        time.sleep(0.1)

# 중단 요청 플래그
stop_requested = False

def reset_stop_request():
    """외부에서 중단 요청을 초기화할 수 있도록 함"""
    global stop_requested
    stop_requested = False

def process_environment_advice():
    global stop_requested
    try:
        if stop_requested: return

        # 1. 데이터 가져오기
        weather_data = get_weather_data()
        
        if stop_requested: return

        # 2. GPT 조언 생성
        result = generate_environment_text(weather_data)
        if stop_requested: return

        advice = result.get("advice", "")
        keyword = result.get("keyword", "NORMAL")
        
        # 3. SenseHAT 아이콘 표시
        display_icon_by_keyword(keyword)
        
        # 4. TTS 출력
        if stop_requested: 
            clear_display()
            return

        print(f"[JOYSTICK] 환경 조언: {advice}")
        play_tts(advice)
        
    except Exception as e:
        print(f"[JOYSTICK] 환경 조언 처리 중 오류 발생: {e}")

def process_fashion_advice():
    global stop_requested
    try:
        if stop_requested: return

        # 1. 데이터 가져오기
        weather_data = get_weather_data()

        if stop_requested: return
        
        # 2. GPT 조언 생성
        result = generate_fashion_text(weather_data)
        if stop_requested: return

        advice = result.get("advice", "")
        keyword = result.get("keyword", "NORMAL")
        
        # 3. SenseHAT 아이콘 표시
        display_icon_by_keyword(keyword)
        
        # 4. TTS 출력
        if stop_requested: 
            clear_display()
            return

        print(f"[JOYSTICK] 복장 조언: {advice}")
        play_tts(advice)
        
    except Exception as e:
        print(f"[JOYSTICK] 복장 조언 처리 중 오류 발생: {e}")

def start_joystick_listener():
    """백그라운드 스레드에서 조이스틱 리스너 실행"""
    thread = threading.Thread(target=handle_joystick, daemon=True)
    thread.start()
    return thread
