import sys
import time

print("--- SenseHAT 조이스틱 진단 도구 ---")

try:
    from sense_hat import SenseHat
    print("[OK] SenseHat 라이브러리 임포트 성공")
except ImportError:
    print("[ERROR] SenseHat 라이브러리가 설치되지 않았거나 찾을 수 없습니다.")
    sys.exit(1)

try:
    sense = SenseHat()
    print("[OK] SenseHat 하드웨어 초기화 성공")
except Exception as e:
    print(f"[ERROR] SenseHat 초기화 실패: {e}")
    print("  -> I2C가 활성화되어 있는지 확인하세요 (sudo raspi-config).")
    print("  -> SenseHAT이 GPIO 핀에 올바르게 장착되었는지 확인하세요.")
    sys.exit(1)

print("\n>>> 조이스틱 테스트 시작 (Ctrl+C로 종료) <<<")
print("조이스틱을 아무 방향이나 눌러보세요. 화면에 문자가 표시됩니다.")

# 초기화: 화면 끄기
sense.clear()

try:
    while True:
        # 이벤트를 모두 가져옵니다
        events = sense.stick.get_events()
        
        if not events:
            pass
            
        for event in events:
            print(f"[감지됨] 동작: {event.action:8} | 방향: {event.direction}")
            
            # 눌렀을 때만 LED 표시
            if event.action == 'pressed':
                if event.direction == 'left':
                    # 빨간색 L
                    sense.show_letter("L", text_colour=[255, 0, 0])
                elif event.direction == 'right':
                    # 파란색 R
                    sense.show_letter("R", text_colour=[0, 0, 255])
                elif event.direction == 'middle':
                    # 초록색 M
                    sense.show_letter("M", text_colour=[0, 255, 0])
                elif event.direction == 'up':
                    sense.show_letter("U", text_colour=[255, 255, 255])
                elif event.direction == 'down':
                    sense.show_letter("D", text_colour=[255, 255, 255])
                
                # 0.5초 보여주고 끄기
                time.sleep(0.5)
                sense.clear()
        
        # CPU 점유율을 낮추기 위한 대기
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n--- 테스트 종료 ---")
    sense.clear()
