import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_environment_text(weather_data):
    temperature = weather_data.get("temperature")
    humidity = weather_data.get("humidity")
    co2 = weather_data.get("co2")
    weather = weather_data.get("weather")
    description = weather_data.get("description")
    location = weather_data.get("location")

    # -----------------------------
    # CO2 값이 없으면 자동으로 설명으로 대체
    # -----------------------------
    co2_str = f"{co2}ppm" if co2 is not None else "센서 미연결 또는 실외 데이터 기반"

    prompt = f"""
당신은 실내/실외 환경 전문가입니다.

다음 정보를 기반으로 쾌적한 환경을 위한 생활 조언을 한국어로 작성하세요.

도시: {location}
기온: {temperature}°C
습도: {humidity}%
CO2 농도: {co2_str}
날씨: {weather}
상세 설명: {description}

지침:
- 최대 4~6문장
- 실내 센서 데이터가 존재하면 환기/습도/CO2 중심으로 조언
- 센서가 없으면 실외 날씨 및 활동 조언 중심
- 건강과 쾌적함에 초점을 맞추어 자연스럽고 짧은 한국어 문장으로 작성
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
