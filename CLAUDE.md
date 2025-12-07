# CLAUDE.md

이 문서는 Claude AI가 이 프로젝트를 이해하고 협업하는 데 필요한 가이드라인을 제공합니다.

---

## 📌 프로젝트 개요

**Embedded Project**는 라즈베리파이에서 실행 가능한 Flask 기반 백엔드 프로젝트입니다.

### 주요 기능
- GPT-5 Nano 스트리밍 API
- OpenWeather 날씨 조회 API
- 라즈베리파이 센서/디바이스 연동 확장

### 기술 스택
- **백엔드**: Python 3.x, Flask
- **프론트엔드**: React (TypeScript, Vite)
- **API**: OpenAI GPT, OpenWeather API
- **문서화**: Swagger/Flasgger

---

## 🏗 프로젝트 구조

```
Embedded-Project/
├── app/                      # Flask 백엔드
│   ├── routes/              # API 라우트
│   │   ├── gpt_fashion_routes.py
│   │   ├── weather_routes.py
│   │   ├── cities_routes.py
│   │   └── settings_routes.py
│   ├── services/            # 비즈니스 로직
│   │   ├── gpt_fashion_service.py
│   │   ├── weather_service.py
│   │   └── settings_service.py
│   ├── utils/               # 유틸리티 함수
│   └── static/dist/         # 빌드된 React 앱 (자동 생성)
│
├── client/                  # React 프론트엔드
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   └── styles/         # CSS 스타일
│   ├── package.json
│   └── vite.config.ts      # Vite 빌드 설정
│
├── run.py                  # Flask 서버 실행
├── requirements.txt        # Python 의존성
├── Caddyfile              # Caddy 리버스 프록시 설정
├── dev.bat / dev.sh       # 개발 모드 실행 스크립트
├── prod.bat / prod.sh     # 프로덕션 모드 실행 스크립트
└── .env                   # 환경 변수 (미포함)
```

## 🔄 배포 아키텍처

### 개발 모드
```
React Dev Server (Vite) :3000
         ↓ (프록시)
    Flask API :5050
```

### 프로덕션 모드
```
     Caddy :443 (HTTPS)
         ↓
    ┌─────────┬──────────┐
정적파일(빌드)  Flask API :5050
```

---

## 🔑 중요 규칙

### 1. 환경 변수
- `.env` 파일은 **절대 커밋하지 않습니다**
- 필요한 키:
  - `OPENAI_API_KEY`: OpenAI API 키
  - `OPENWEATHER_API_KEY`: OpenWeather API 키
  - `DEFAULT_CITY`: 기본 도시 설정

### 2. 코드 스타일
- **Python**: PEP 8 준수
- **TypeScript/React**: ESLint 규칙 준수
- 함수와 변수명은 명확하고 설명적으로 작성
- 주석은 한국어로 작성

### 3. API 설계
- RESTful 원칙을 따릅니다
- 엔드포인트는 `/api/{기능}/{작업}` 형식을 사용
- 모든 새 API는 Swagger 문서에 추가

### 4. Git 관리
- `main` 브랜치가 메인 브랜치입니다
- 기능 추가 시 별도 브랜치 생성 권장
- 커밋 메시지는 명확하게 작성

---

## 🛠 개발 가이드

### 새 API 추가 시
1. `app/routes/`에 라우트 파일 생성 또는 수정
2. `app/services/`에 비즈니스 로직 구현
3. Swagger 문서 업데이트 (데코레이터 사용)
4. 테스트 후 커밋

### 프론트엔드 컴포넌트 추가 시
1. `client/src/components/`에 컴포넌트 생성
2. TypeScript 타입 정의 필수
3. shadcn/ui 컴포넌트 활용 권장

### 센서/하드웨어 연동 시
- 라즈베리파이 GPIO 사용 시 별도 문서화
- 테스트 환경과 실제 환경 분리

---

## 📝 코드 변경 시 주의사항

### 이 문서 업데이트 필수 사항
다음 변경이 발생하면 **CLAUDE.md를 함께 업데이트**해주세요:

1. **프로젝트 구조 변경**
   - 새 디렉토리/모듈 추가
   - 기존 파일/폴더 이동 또는 삭제

2. **새로운 환경 변수 추가**
   - `.env`에 필요한 새 키가 추가된 경우

3. **주요 기술 스택 변경**
   - 새 라이브러리/프레임워크 도입
   - 기존 기술 스택 교체

4. **API 엔드포인트 변경**
   - 새 API 추가
   - 기존 API 경로 변경

5. **코딩 컨벤션 변경**
   - 새로운 규칙이나 가이드라인 도입

6. **배포/실행 방법 변경**
   - 서버 실행 명령어 변경
   - 새로운 빌드 프로세스 도입

---

## 🚀 실행 방법

### 개발 모드 (권장)
개발 중에는 프론트엔드와 백엔드를 별도로 실행합니다.

**Windows:**
```bash
dev.bat
```

**Linux/Mac/라즈베리파이:**
```bash
chmod +x dev.sh  # 최초 1회만
./dev.sh
```

자동으로 다음이 실행됩니다:
- React Dev Server (포트 3000) - HMR 지원
- Flask API (포트 5050)

접속: http://localhost:3000

### 프로덕션 모드
시연이나 배포 시 사용합니다. 프론트엔드를 빌드한 후 Flask에서 통합 서빙합니다.

**Windows:**
```bash
prod.bat
```

**Linux/Mac/라즈베리파이:**
```bash
chmod +x prod.sh  # 최초 1회만
./prod.sh
```

자동으로 다음이 실행됩니다:
1. React 앱 빌드 → `app/static/dist/`
2. Flask 서버 시작 (포트 5050)

접속: http://localhost:5050

### Caddy 리버스 프록시 (선택)
외부 접속 및 HTTPS가 필요한 경우:

```bash
# Caddy 설치 (최초 1회)
# Windows: https://caddyserver.com/download
# Linux: sudo apt install caddy

# Caddy 실행 (프로덕션 모드와 함께)
caddy run
```

접속: https://localhost (자동 HTTPS)

### 수동 실행

**백엔드만:**
```bash
pip install -r requirements.txt
python run.py
```

**프론트엔드만 (개발):**
```bash
cd client
npm install
npm run dev
```

**프론트엔드만 (빌드):**
```bash
cd client
npm run build
```

---

## 🔍 참고 문서

- README.md: 프로젝트 전체 개요
- `/docs`: Swagger API 문서
- `client/README.md`: 프론트엔드 가이드

---

## 💬 협업 시 요청사항

Claude AI와 협업할 때 다음을 요청해주세요:

1. **컨텍스트 제공**: 작업하려는 기능이나 파일을 명확히 지정
2. **목적 설명**: 변경하려는 이유와 목표 설명
3. **범위 제한**: 필요한 변경사항만 최소한으로 요청
4. **검증 요청**: 변경 후 테스트나 확인이 필요한 부분 명시

---

**마지막 업데이트**: 2025-12-07 (배포 아키텍처 개선)
