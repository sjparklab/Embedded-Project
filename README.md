# 🌤️ Embedded Project – Flask 기반 GPT / Weather API 서버

라즈베리파이에서 실행 가능한 경량 Flask 백엔드 프로젝트입니다.  
HTML 한 장(index.html)으로 UI를 구성하고, Flask API를 통해  
GPT 질의응답, 날씨 조회, 디바이스 센서 연동 등을 제공합니다.

---

## ✨ 제공 기능

### 🤖 GPT-5 Nano Streaming API
- `/api/gpt/ask`  
- OpenAI GPT-5 Nano 모델 응답을 *실시간 스트리밍* 형태로 제공  
- index.html UI에서 바로 사용 가능

### 🌤 OpenWeather 날씨 API
- `/api/weather/current`  
- 기본 도시 또는 쿼리 파라미터로 날씨 조회

### 🔧 디바이스 API (라즈베리파이 확장)
- `/api/device/...`  
- 센서 데이터 처리, GPIO 연동 등 확장용 라우트

### 📝 Swagger 문서 제공
- `/docs` → `/apidocs/` 로 이동  
- API 테스트 및 문서 자동화

---

## 📁 프로젝트 구조
Embedded-Project/
│── app/
│ ├── routes/
│ │ ├── gpt_routes.py
│ │ ├── weather_routes.py
│ │ └── device_routes.py
│ ├── services/
│ │ ├── gpt_service.py
│ │ ├── weather_service.py
│ │ └── device_service.py
│ └── init.py
│
│── index.html # GPT 질문 UI (fetch 기반)
│── run.py # 서버 실행 엔트리
│── requirements.txt
│── .env (깃허브 미포함 → 디스코드에서 다운로드 필수)

---

## 🔑 환경 변수 (.env)

> ⚠️ `.env` 파일은 보안상 저장소에 포함되지 않습니다.  
> 반드시 **디스코드에서 다운로드 후 프로젝트 루트에 배치하세요.**

예시:
      OPENWEATHER_API_KEY=YOUR_OPENWEATHER_KEY
      DEFAULT_CITY=Busan
      OPENAI_API_KEY=YOUR_OPENAI_KEY


---

## 🚀 실행 방법

### 1. 패키지 설치
pip install -r requirements.txt

### 2. 서버 실행
python run.py

정상 실행 시:

- http://127.0.0.1:5050  
- http://<PC or Raspberry Pi IP>:5050  

두 주소 모두 접속 가능.

---

## 🖥 웹 UI 사용 방법

브라우저에서 `/` 로 접속하면 아래 기능 제공:

- 질문 입력 → GPT 스트리밍 응답 표시
- HTML + JS(fetch) 기반 단일 페이지 UI
- React/Vue 없이 완전 심플한 구조

---

## 🔌 API 명세

### 🤖 GPT Streaming
POST /api/gpt/ask
Body:
{
"prompt": "질문 내용"
}

→ 응답이 `text/plain` 스트리밍으로 실시간 전송됨.

---

### 🌤 현재 날씨 조회
GET /api/weather/current
GET /api/weather/current?city=Seoul

---

### 🔧 디바이스 API (추가 구현 예정)

---

## 📘 Swagger 문서

Swagger UI:
http://127.0.0.1:5050/docs

Spec(JSON):
http://127.0.0.1:5050/apispec.json

---

## 🧪 CURL 테스트 예시 (GPT)
curl -X POST http://127.0.0.1:5050/api/gpt/ask

-H "Content-Type: application/json"
-d "{"prompt":"테스트"}"
