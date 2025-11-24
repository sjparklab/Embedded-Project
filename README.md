# 🌤️ Weather Embedded Backend (Flask)

라즈베리파이와 연동되는 Flask 기반 간단 날씨 API 서버입니다.  
OpenWeather API를 사용하며 Swagger UI 문서(`/apidocs`)를 제공합니다.

---

## 🚀 기능
- 현재 날씨 조회 (`/weather/current`)
- Swagger 문서 자동 생성 (`/apidocs`)
- 환경변수(.env) 기반 API KEY 보관
- React · Raspberry Pi 연동 가능 (CORS 허용)

---

## 📦 설치 방법

### 1) 가상환경 생성 & 활성화
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) 패키지 설치
```bash
pip install -r requirements.txt
```

### 3) `.env` 파일 생성
```env
OPENWEATHER_API_KEY=YOUR_KEY
DEFAULT_CITY=Busan
```

---

## ▶️ 실행
```bash
source venv/bin/activate
python run.py
```

성공적으로 실행되면:
```
http://127.0.0.1:5050
http://10.0.24.130:5050
```

---

## 📘 Swagger 문서
```
http://127.0.0.1:5050/apidocs
```

---

## 🌤️ API 사용

### ✔ 현재 날씨 조회
```
GET /weather/current
```

### ✔ 특정 도시 날씨 조회
```
GET /weather/current?city=Seoul
```

응답 예시:
```json
{
  "name": "Busan",
  "main": { "temp": 17.3, "humidity": 52 },
  "weather": [ { "description": "broken clouds" } ]
}
```

---

## 🤝 Raspberry Pi 사용 예시
```python
import requests
res = requests.get("http://10.0.24.130:5050/weather/current")
print(res.json())
```

---

## 🗂️ 프로젝트 구조
```
weather_embedded_project/
│── app/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── __init__.py
│
│── run.py
│── .env
│── requirements.txt
│── venv/
```
