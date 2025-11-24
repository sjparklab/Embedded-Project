import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Busan")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_current_weather(city=None):
    if city is None:
        city = DEFAULT_CITY

    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        print(">>> Request params:", params)

        res = requests.get(BASE_URL, params=params)

        print(">>> STATUS:", res.status_code)
        print(">>> RESPONSE TEXT:", res.text[:300])

        if res.status_code != 200:
            return {"error": "Failed to fetch weather data", "detail": res.text}

        return res.json()

    except Exception as e:
        print(">>> EXCEPTION:", e)
        return {"error": "Exception occurred", "detail": str(e)}
