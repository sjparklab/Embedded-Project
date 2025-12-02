import os
import json
import requests
from dotenv import load_dotenv
from app.services.settings_service import load_settings

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# -------------------------------
# 1) cities.json 로드
# -------------------------------
CITIES_FILE = os.path.join(os.path.dirname(__file__), "../data/cities.json")

try:
    with open(CITIES_FILE, "r", encoding="utf-8") as f:
        CITIES = json.load(f)

    CITY_MAP = {str(c["id"]): c for c in CITIES}  # id → city object
except Exception as e:
    print("❌ ERROR loading cities.json:", e)
    CITY_MAP = {}


# -------------------------------
# 2) 날씨 영어 → 한국어 변환 매핑
# -------------------------------
WEATHER_KO = {
    "Clear": "맑음",
    "Clouds": "흐림",
    "Rain": "비",
    "Drizzle": "이슬비",
    "Thunderstorm": "천둥번개",
    "Snow": "눈",
    "Mist": "안개",
    "Fog": "짙은 안개",
    "Haze": "실안개",
}

def translate_description(desc_en: str):
    return (
        desc_en.replace("clear sky", "맑은 하늘")
               .replace("few clouds", "구름 조금")
               .replace("scattered clouds", "흩어진 구름")
               .replace("broken clouds", "구름 많음")
               .replace("overcast clouds", "흐린 하늘")
    )


# -------------------------------
# 3) 메인 날씨 함수
# -------------------------------
def get_current_weather(city_id: 
    str, unit: str):
    """
    city_id 직접 전달 가능
    없으면 settings.json에서 city_id 불러옴
    """

    # CITY ID 가져오기
    if not city_id:
        settings = load_settings()
        city_id = settings.get("location")

    if not city_id:
        return {"error": True, "detail": "city_id가 제공되지 않았습니다."}

    # OpenWeather 요청 파라미터
    params = {
        "id": city_id,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric" if unit == "celsius" else "imperial",
        "lang": "en"  # 영어 기반으로 받고 변환
    }

    try:
        res = requests.get(BASE_URL, params=params)
    except Exception as e:
        return {"error": True, "detail": str(e)}

    if res.status_code != 200:
        return {"error": True, "detail": res.text}

    raw = res.json()

    # 기본 날씨 영어 데이터
    main_weather_en = raw["weather"][0]["main"]
    desc_en = raw["weather"][0]["description"]
    city_name_en = raw["name"]

    # ⚡ 한국어 도시명 매핑
    city_obj = CITY_MAP.get(str(city_id))
    city_name_ko = city_obj["name_ko"] if city_obj else city_name_en

    # 최종 변환 데이터
    result = {
        "temperature": raw["main"]["temp"],
        "humidity": raw["main"]["humidity"],
        "pressure": raw["main"]["pressure"],
        "co2": 420,  # 센서 없으니 임시 값
        "weather": WEATHER_KO.get(main_weather_en, main_weather_en),
        "description": translate_description(desc_en),
        "location": city_name_ko,
    }

    return result
