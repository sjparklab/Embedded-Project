import os
import json
import requests
from dotenv import load_dotenv

from app.services.settings_service import load_settings
from app.services.device_service import read_sensor_data   # CO₂ + 실내 센서 데이터

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ------------------------------------------------------------
# 1) cities.json 로드
# ------------------------------------------------------------
def load_city_map():
    CITIES_FILE = os.path.join(os.path.dirname(__file__), "../data/cities.json")
    try:
        with open(CITIES_FILE, "r", encoding="utf-8") as f:
            cities = json.load(f)
        return {str(c["id"]): c for c in cities}
    except Exception as e:
        print("❌ ERROR loading cities.json:", e)
        return {}


# ------------------------------------------------------------
# 2) 영어 → 한국어 변환
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# 3) OpenWeather API (기온/습도/압력/날씨/설명/지역)
# ------------------------------------------------------------
def fetch_openweather(city_id: str, unit: str):
    CITY_MAP = load_city_map()

    params = {
        "id": city_id,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric" if unit == "celsius" else "imperial",
        "lang": "en",
    }

    try:
        res = requests.get(BASE_URL, params=params, timeout=5)
        res.raise_for_status()
    except Exception as e:
        return {"error": True, "detail": f"OpenWeather 요청 실패: {e}"}

    raw = res.json()

    main_weather_en = raw["weather"][0]["main"]
    desc_en = raw["weather"][0]["description"]

    city_obj = CITY_MAP.get(str(city_id))
    city_name_ko = city_obj["name_ko"] if city_obj else raw["name"]

    return {
        "temperature": raw["main"]["temp"],
        "humidity": raw["main"]["humidity"],
        "pressure": raw["main"]["pressure"],
        "weather": WEATHER_KO.get(main_weather_en, main_weather_en),
        "description": translate_description(desc_en),
        "location": city_name_ko,
    }


# ------------------------------------------------------------
# 4) React 대시보드 전용: 날씨(API) + 센서 CO₂
# ------------------------------------------------------------
def get_current_weather(city_id: str, unit: str):
    """대시보드용 날씨 데이터"""

    weather = fetch_openweather(city_id, unit)

    if "error" in weather:
        return weather

    # CO₂만 센서에서 가져오기
    try:
        sensor = read_sensor_data()
        co2 = sensor.get("co2")

        if co2 is None:
            raise Exception("센서 CO₂ None")

        print("🌡 CO₂ 센서값 사용:", co2)
        weather["co2"] = co2

    except Exception as e:
        print("⚠ CO₂ 센서 실패 → mock 사용:", e)
        import random
        weather["co2"] = random.randint(400, 1200)

    return weather


# ------------------------------------------------------------
# 5) get_weather_data() → React dashboard에서 사용
# ------------------------------------------------------------
def get_weather_data():
    """
    대시보드용 최종 데이터 생성 함수
    - 날씨 정보 → 무조건 OpenWeather API
    - CO₂ → 센서 우선, 실패 시 mock
    """

    # 1) settings 불러오기
    settings = load_settings()
    city_id = settings.get("location", "1835848")  # default: Seoul
    unit = settings.get("temperatureUnit", "celsius")

    # 2) OpenWeather 데이터 가져오기
    weather = fetch_openweather(city_id, unit)

    # OpenWeather 실패 시 fallback
    if "error" in weather:
        print("⚠ OpenWeather 실패 → fallback 더미 데이터 사용")

        weather = {
            "temperature": 20,
            "humidity": 50,
            "pressure": 1018,
            "weather": "맑음",
            "description": "맑은 하늘",
            "location": "기본 위치"
        }

    # 3) CO₂만 센서에서 가져오기
    try:
        sensor = read_sensor_data()
        co2 = sensor.get("co2")

        if co2 is None:
            raise Exception("CO₂ None")

        print("🌡 센서 CO₂ 사용:", co2)
        weather["co2"] = co2

    except Exception as e:
        print("⚠ 센서 CO₂ 실패 → mock 사용:", e)
        import random
        weather["co2"] = random.randint(400, 1200)

    return weather
