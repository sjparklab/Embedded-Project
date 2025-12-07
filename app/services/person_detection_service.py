"""
웹캠을 사용한 사람 감지 서비스
"""
import cv2
import os
from datetime import datetime

# OpenCV 사용 가능 여부
OPENCV_AVAILABLE = True
try:
    import cv2
except ImportError:
    OPENCV_AVAILABLE = False
    print("Warning: opencv-python library not available. Person detection will use mock data.")

# 최근 감지 결과 저장
latest_detection_result = {
    "person_detected": False,
    "timestamp": None
}

def detect_person_from_webcam():
    """
    웹캠으로 사진을 찍어 사람이 있는지 감지

    Returns:
        dict: {
            "person_detected": bool,  # 사람 감지 여부
            "message": str,           # "있다" 또는 "없다"
            "timestamp": str          # ISO 포맷 타임스탬프
        }
    """
    import random

    if not OPENCV_AVAILABLE:
        # OpenCV가 없을 경우 mock 데이터
        print("[INFO] OpenCV가 설치되지 않았습니다. Mock 데이터를 사용합니다.")
        person_detected = random.choice([True, False])
        result = {
            "person_detected": person_detected,
            "message": "있다" if person_detected else "없다",
            "timestamp": datetime.now().isoformat()
        }
        _update_latest_detection(result)
        return result

    try:
        # 웹캠 열기
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("[ERROR] 웹캠을 열 수 없습니다.")
            result = {
                "person_detected": False,
                "message": "없다",
                "error": "웹캠 접근 실패",
                "timestamp": datetime.now().isoformat()
            }
            _update_latest_detection(result)
            return result

        # 프레임 읽기
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            print("[ERROR] 프레임을 읽을 수 없습니다.")
            result = {
                "person_detected": False,
                "message": "없다",
                "error": "프레임 읽기 실패",
                "timestamp": datetime.now().isoformat()
            }
            _update_latest_detection(result)
            return result

        # 사람 감지
        person_detected = _detect_person_in_frame(frame)

        result = {
            "person_detected": person_detected,
            "message": "있다" if person_detected else "없다",
            "timestamp": datetime.now().isoformat()
        }

        _update_latest_detection(result)
        return result

    except Exception as e:
        print(f"[ERROR] 사람 감지 중 오류 발생: {e}")
        result = {
            "person_detected": False,
            "message": "없다",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        _update_latest_detection(result)
        return result

def _detect_person_in_frame(frame):
    """
    프레임에서 사람을 감지

    Args:
        frame: OpenCV 프레임

    Returns:
        bool: 사람이 감지되면 True, 아니면 False
    """
    try:
        # Haar Cascade 분류기 로드 (전신 감지)
        cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'

        if not os.path.exists(cascade_path):
            # 전신 감지가 없으면 상반신 감지 사용
            cascade_path = cv2.data.haarcascades + 'haarcascade_upperbody.xml'

        if not os.path.exists(cascade_path):
            print("[WARNING] Haar Cascade 파일을 찾을 수 없습니다. HOG descriptor를 사용합니다.")
            # HOG (Histogram of Oriented Gradients) 사용
            hog = cv2.HOGDescriptor()
            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

            # 사람 감지
            (humans, _) = hog.detectMultiScale(frame,
                                               winStride=(4, 4),
                                               padding=(8, 8),
                                               scale=1.05)

            return len(humans) > 0

        # Haar Cascade로 감지
        body_cascade = cv2.CascadeClassifier(cascade_path)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 사람 감지
        bodies = body_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(30, 30)
        )

        # 추가로 HOG detector로도 체크 (더 정확한 감지)
        if len(bodies) == 0:
            try:
                hog = cv2.HOGDescriptor()
                hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
                (humans, _) = hog.detectMultiScale(frame,
                                                   winStride=(4, 4),
                                                   padding=(8, 8),
                                                   scale=1.05)
                return len(humans) > 0
            except Exception as e:
                print(f"[WARNING] HOG 감지 실패: {e}")

        return len(bodies) > 0

    except Exception as e:
        print(f"[ERROR] 프레임 분석 중 오류: {e}")
        return False

def _update_latest_detection(result):
    """최근 감지 결과 업데이트"""
    global latest_detection_result
    latest_detection_result["person_detected"] = result["person_detected"]
    latest_detection_result["timestamp"] = result["timestamp"]
    print(f"[INFO] 사람 감지 결과: {result['message']} (시각: {result['timestamp']})")

def get_latest_detection():
    """저장된 최신 감지 결과 반환"""
    return latest_detection_result.copy()
