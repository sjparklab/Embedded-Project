# Embedded AI Assistant Project Report

## 1. 프로젝트 개요
이 프로젝트는 **Raspberry Pi 5**와 **SenseHAT**을 기반으로 한 **AI 스마트 비서 시스템**입니다. 실내외 환경 데이터를 분석하여 **ChatGPT(gpt-5-nano)**가 생활 환경(환기/냉난방) 및 외출 복장 조언을 제공하며, **음성 안내(TTS)**와 **LED 매트릭스 시각화**를 통해 사용자와 상호작용합니다.

## 2. 시스템 아키텍처
- **Backend**: Python Flask (REST API Server)
- **Frontend**: React (Vite) - 웹 대시보드
- **AI Engine**: OpenAI GPT-5-nano (Custom Model Name)
- **Hardware**: Raspberry Pi 5, SenseHAT (LED Matrix, Joystick, Env Sensors), CO2 Sensor (UART)

## 3. 핵심 기능 및 구현 세부사항

### A. 환경 데이터 수집 (`weather_service.py`, `device_service.py`)
- **실외**: OpenWeatherMap API를 통해 기온, 습도, 날씨, 풍속 정보 수집
- **실내**: SenseHAT(온도/습도) 및 UART CO2 센서 데이터 수집
- **하이브리드 모드**: 센서 연결 실패 시 Mock 데이터 또는 API 데이터로 자동 대체

### B. AI 조언 생성 (`gpt_environment_service.py`, `gpt_fashion_service.py`)
- **Model**: `gpt-5-nano`
- **프로토콜 변경**: 기존 단순 텍스트 응답에서 **JSON 구조화 응답**으로 변경
  - 응답 형식: `{"keyword": "KEYWORD", "advice": "한국어 조언 텍스트"}`
  - **키워드**:
    - 환경: `VENTILATION`(환기), `HEATING`(난방), `COOLING`(냉방), `NORMAL`
    - 복장: `UMBRELLA`(우산), `COLD`(추위), `HOT`(더위), `NORMAL`

### C. 하드웨어 상호작용 (`joystick_service.py`, `device_service.py`)
- **조이스틱 제어**:
  - **⬅️ 왼쪽 (Left)**: 실내 환경 조언 요청 → GPT 분석 → LED 아이콘(창문/온도계) + TTS 안내
  - **➡️ 오른쪽 (Right)**: 외출 복장 조언 요청 → GPT 분석 → LED 아이콘(우산/해/눈) + TTS 안내
  - **⏺ 가운데 (Middle)**: 동작 중지 (TTS 종료 및 LED 초기화)
- **LED 디스플레이**: GPT가 반환한 `keyword`에 맵핑된 8x8 픽셀 아트 아이콘 출력

### D. 음성 안내 (`tts_service.py`)
- **TTS 엔진**: gTTS (Google TTS) + `ffplay`/`mpg123` (시스템 오디오)
- **백그라운드 처리**: 조언 생성 즉시 비동기적으로 음성 출력

## 4. 최근 보강 사항 (Modification Log)
1.  **GPT 프롬프트 고도화**: 단순 줄글 조언에서 **JSON 파싱**이 가능한 형태로 변경하여, 상황에 맞는 키워드 추출 기능을 추가함.
2.  **SenseHAT 시각화 통합**: `device_service.py`에 키워드 기반 아이콘 출력 함수(`display_icon_by_keyword`) 구현.
3.  **조이스틱 리스너 구현**: `app/services/joystick_service.py`를 신설하여 메인 서버와 별도로 백그라운드에서 조이스틱 입력을 감시하도록 함.
4.  **시스템 자동화**: Flask 앱 구동 시(`run.py` -> `__init__.py`) 조이스틱 리스너가 자동으로 시작되도록 설정.
5.  **API 라우트 수정**: 웹 프론트엔드와의 호환성을 유지하면서, 내부적으로는 딕셔너리(JSON) 형태의 데이터를 처리하도록 로직 개선.

## 5. 실행 방법
```bash
# 가상 환경 활성화 (Windows)
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행 (포트 5050)
python run.py
```

## 6. 향후 개선 가능성
- **웹 연동 강화**: 웹 대시보드에서 '조언 받기' 버튼 클릭 시에도 라즈베리파이의 LED가 반응하도록 소켓 통신 추가 고려.
- **사용자 커스텀**: 알람 시간 설정 시 날씨/복장 브리핑 기능 추가.
