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

```
Embedded-Project/
├── app/                      # Flask 백엔드
│   ├── routes/              # API 라우트
│   ├── services/            # 비즈니스 로직
│   └── static/dist/         # 빌드된 React 앱 (자동 생성)
│
├── client/                  # React 프론트엔드
│   ├── src/                 # React 소스 코드
│   ├── package.json
│   └── vite.config.ts
│
├── run.py                   # Flask 서버 실행 엔트리
├── requirements.txt         # Python 패키지
├── Caddyfile               # Caddy 리버스 프록시 설정
├── dev.bat / dev.sh        # 개발 모드 실행
├── prod.bat / prod.sh      # 프로덕션 모드 실행
└── .env                    # 환경 변수 (깃허브 미포함)
```

### 배포 아키텍처

**개발 모드:**
```
React Dev Server :3000 → Flask API :5050
```

**프로덕션 모드:**
```
Caddy :443 (HTTPS) → 정적파일 + Flask API :5050
```



## 🔑 환경 변수 (.env)

> ⚠️ `.env` 파일은 보안상 저장소에 포함되지 않습니다.  
> 반드시 **디스코드에서 다운로드 후 프로젝트 루트에 배치하세요.**

예시:
      OPENWEATHER_API_KEY=YOUR_OPENWEATHER_KEY
      DEFAULT_CITY=Busan
      OPENAI_API_KEY=YOUR_OPENAI_KEY


---

## 🚀 빠른 시작

### 개발 모드 (일상적인 개발)

**Windows:**
```bash
dev.bat
```

**Linux/Mac/라즈베리파이:**
```bash
chmod +x dev.sh  # 최초 1회만
./dev.sh
```

자동으로 React Dev Server(3000) + Flask API(5050)가 실행됩니다.
접속: http://localhost:3000

### 프로덕션 모드 (시연/배포)

**Windows:**
```bash
prod.bat
```

**Linux/Mac/라즈베리파이:**
```bash
chmod +x prod.sh  # 최초 1회만
./prod.sh
```

React 앱을 빌드한 후 Flask 서버에서 통합 서빙합니다.
접속: http://localhost:5050

### Caddy로 HTTPS 사용 (외부 접속)

```bash
# 1. Caddy 설치 (최초 1회)
# Windows: https://caddyserver.com/download
# Linux: sudo apt install caddy

# 2. 프로덕션 모드 실행
./prod.sh  # 또는 prod.bat

# 3. 별도 터미널에서 Caddy 실행
caddy run

# 접속: https://localhost (자동 HTTPS)
```

---

## 📖 상세 실행 방법

### 최초 설정

1. **환경 변수 설정**
   `.env` 파일을 프로젝트 루트에 생성 (디스코드에서 다운로드)
   ```
   OPENWEATHER_API_KEY=YOUR_KEY
   DEFAULT_CITY=Busan
   OPENAI_API_KEY=YOUR_KEY
   ```

2. **백엔드 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **프론트엔드 패키지 설치**
   ```bash
   cd client
   npm install
   cd ..
   ```

### 수동 실행 (고급)

**백엔드만 실행:**
```bash
python run.py
# 접속: http://localhost:5050
```

**프론트엔드만 실행 (개발):**
```bash
cd client
npm run dev
# 접속: http://localhost:3000
```

**프론트엔드 빌드:**
```bash
cd client
npm run build
# 결과물: app/static/dist/
```

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
