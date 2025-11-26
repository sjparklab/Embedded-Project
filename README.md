🌤️ Embedded Project – Flask 기반 GPT/Weather API 서버

라즈베리파이에서 실행 가능한 경량 Flask 백엔드 서버입니다.
다음 기능을 제공합니다:

🌤 OpenWeatherMap 기반 날씨 API

🤖 GPT-5 Nano 스트리밍 기반 질문 응답

🔧 디바이스(센서/하드웨어) 확장 가능

🖥 단일 HTML 페이지(index.html) UI 제공

⚠️ .env 파일은 보안상 저장소에 포함되어 있지 않습니다.
반드시 디스코드에서 다운로드 후 프로젝트 루트에 배치하세요.

📁 프로젝트 구조

Embedded-Project/
│── app/
│ ├── routes/
│ │ ├── weather_routes.py
│ │ ├── device_routes.py
│ │ └── gpt_routes.py
│ ├── services/
│ │ ├── weather_service.py
│ │ ├── device_service.py
│ │ └── gpt_service.py
│ └── init.py
│
│── index.html
│── run.py
│── requirements.txt
│── .env (✔ 디스코드에서 다운로드)

🔧 설치 방법
1. 패키지 설치

Python 3.10 이상 권장

pip install -r requirements.txt

🔑 2. 환경변수 설정 (.env)

디스코드에서 받은 .env 파일을 프로젝트 루트에 넣어야 합니다.

예시:

OPENWEATHER_API_KEY=YOUR_OPENWEATHER_KEY
DEFAULT_CITY=Busan
OPENAI_API_KEY=YOUR_OPENAI_KEY

▶️ 3. 서버 실행

python run.py

성공적으로 실행되면 다음 주소로 접속할 수 있습니다:

http://127.0.0.1:5050

http://<PC-또는-라즈베리파이-IP>:5050

🖥️ 웹 UI 사용

브라우저에서 아래 주소로 들어가면 GPT 질문 웹 UI가 뜹니다.

http://127.0.0.1:5050/

기능:

질문 입력

GPT-5 Nano 스트리밍 응답

단일 HTML + fetch로 동작

📡 API 목록
1) GPT 스트리밍

POST /api/gpt/ask
Body (JSON):
{ "prompt": "라즈베리파이가 뭐야?" }

응답
텍스트 스트리밍 (text/plain)
→ index.html에서 실시간 타이핑처럼 출력됨

2) 현재 날씨 조회

GET /api/weather/current
GET /api/weather/current?city=Seoul

3) 디바이스 API

(라즈베리파이 GPIO/센서 로직 확장 가능)

경로 예시:
/api/device/…

📝 기술 스택

Python 3.11

Flask

Flask-CORS

Flasgger (Swagger)

OpenWeatherMap API

OpenAI GPT-5 Nano

HTML + JS(fetch)

⚠️ 주의사항

.env 없으면 GPT/Weather 기능 모두 작동하지 않습니다.

Windows 환경은 느릴 수 있으며, 라즈베리파이(Linux) 에서 최적화됨.

Flask는 개발용 서버이므로 실서비스 시 WSGI(Gunicorn 등) 필요.

🧪 curl 테스트 예시

curl -X POST http://127.0.0.1:5050/api/gpt/ask
 -H "Content-Type: application/json" -d "{"prompt":"테스트"}"