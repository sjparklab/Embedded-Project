import threading
import time
from app.services.device_service import SENSEHAT_AVAILABLE, sense, display_icon_by_keyword, clear_display
from app.services.weather_service import get_weather_data
from app.services.gpt_environment_service import generate_environment_text
from app.services.gpt_fashion_service import generate_fashion_text
from app.services.tts_service import play_tts, stop_tts

def show_loading():
    """처리 중임을 알리는 LED 표시 (노란색 점멸 또는 고정)"""
    if SENSEHAT_AVAILABLE and sense:
        # 노란색(R, G, B)으로 화면 중앙에 점 표시 또는 전체 흐릿하게
        Y = (100, 100, 0)
        O = (0, 0, 0)
        # 간단한 모래시계 모양 또는 'L'자
        img = [
            O, O, O, O, O, O, O, O,
            O, O, O, Y, Y, O, O, O,
            O, O, O, Y, Y, O, O, O,
            O, O, O, Y, Y, O, O, O,
            O, O, O, Y, Y, O, O, O,
            O, O, O, Y, Y, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O
        ]
        sense.set_pixels(img)

def handle_joystick():
    """조이스틱 이벤트를 무한 루프로 감시하는 함수"""
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
                # 누름(pressed) 상태일 때 동작 (held는 중복 호출 방지를 위해 제외하거나 필요시 추가)
                if event.action == 'pressed':
                    if event.direction == 'left':
                        print("[JOYSTICK] ⬅️ 왼쪽 감지: 실내 환경 조언 생성 중...")
                        show_loading() # 즉시 피드백
                        process_environment_advice()
                    elif event.direction == 'right':
                        print("[JOYSTICK] ➡️ 오른쪽 감지: 외출 복장 조언 생성 중...")
                        show_loading() # 즉시 피드백
                        process_fashion_advice()
                    elif event.direction == 'middle':
                        print("[JOYSTICK] ⏺ 가운데 감지: 디스플레이 및 TTS 중단")
                        stop_tts()
                        clear_display()
        except Exception as e:
            print(f"[JOYSTICK] 이벤트 처리 중 오류 발생: {e}")

        time.sleep(0.1)

def process_environment_advice():
    try:
        # 1. 데이터 가져오기
        weather_data = get_weather_data()
        
        # 2. GPT 조언 생성
        result = generate_environment_text(weather_data)
        advice = result.get("advice", "")
        keyword = result.get("keyword", "NORMAL")
        
        # 3. SenseHAT 아이콘 표시
        display_icon_by_keyword(keyword)
        
        # 4. TTS 출력
        print(f"[JOYSTICK] 환경 조언: {advice}")
        play_tts(advice)
        
    except Exception as e:
        print(f"[JOYSTICK] 환경 조언 처리 중 오류 발생: {e}")

def process_fashion_advice():
    try:
        # 1. 데이터 가져오기
        weather_data = get_weather_data()
        
        # 2. GPT 조언 생성
        result = generate_fashion_text(weather_data)
        advice = result.get("advice", "")
        keyword = result.get("keyword", "NORMAL")
        
        # 3. SenseHAT 아이콘 표시
        display_icon_by_keyword(keyword)
        
        # 4. TTS 출력
        print(f"[JOYSTICK] 복장 조언: {advice}")
        play_tts(advice)
        
    except Exception as e:
        print(f"[JOYSTICK] 복장 조언 처리 중 오류 발생: {e}")

def start_joystick_listener():
    """백그라운드 스레드에서 조이스틱 리스너 실행"""
    thread = threading.Thread(target=handle_joystick, daemon=True)
    thread.start()
    return thread
