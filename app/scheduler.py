"""
백그라운드 스케줄러 설정
APScheduler를 사용하여 주기적인 작업 수행
"""
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.person_detection_service import detect_person_from_webcam
from app.services.joystick_service import process_environment_advice, reset_stop_request
import atexit

# 스케줄러 인스턴스
scheduler = None

def scheduled_person_detection():
    """1시간마다 실행되는 사람 감지 작업 - 사람이 있으면 환경 조언 제공"""
    print("[SCHEDULER] 정기 사람 감지 시작")
    result = detect_person_from_webcam()
    print(f"[SCHEDULER] 감지 결과: {result['message']}")

    # 사람이 감지되면 실내 환경 조언 실행
    if result.get("person_detected"):
        print("[SCHEDULER] 사람 감지됨 → 실내 환경 조언 실행")
        try:
            # 중단 요청 플래그 초기화 (이전 중단 명령이 남아있을 수 있음)
            reset_stop_request()
            process_environment_advice()
        except Exception as e:
            print(f"[SCHEDULER] 환경 조언 실행 중 오류: {e}")

def start_scheduler():
    """스케줄러 시작"""
    global scheduler

    if scheduler is not None:
        print("[WARNING] 스케줄러가 이미 실행 중입니다.")
        return

    scheduler = BackgroundScheduler()

    # 1시간(3600초)마다 사람 감지 작업 실행
    scheduler.add_job(
        func=scheduled_person_detection,
        trigger="interval",
        hours=1,  # 1시간 간격
        id='person_detection_job',
        name='사람 감지 정기 작업',
        replace_existing=True
    )

    # 스케줄러 시작
    scheduler.start()
    print("[INFO] 백그라운드 스케줄러가 시작되었습니다.")
    print("[INFO] 사람 감지 작업이 1시간 간격으로 실행됩니다.")

    # 앱 종료 시 스케줄러도 종료
    atexit.register(lambda: scheduler.shutdown())

def stop_scheduler():
    """스케줄러 중지"""
    global scheduler
    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None
        print("[INFO] 백그라운드 스케줄러가 중지되었습니다.")
