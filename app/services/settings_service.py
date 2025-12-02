import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "location": "1835848",
    "temperatureUnit": "celsius",
    "autoRefresh": True,
    "refreshInterval": 30,
    "ttsEnabled": True,
    "ttsSpeed": 1.0,
    "ttsPitch": 1.0,
}

def load_settings():
    """settings.json 파일을 읽어서 반환"""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS


def save_settings(data: dict):
    """settings.json 파일에 저장"""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
