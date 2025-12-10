import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_fashion_text(weather_data):
    temperature = weather_data.get("temperature")
    weather = weather_data.get("weather")
    description = weather_data.get("description")
    location = weather_data.get("location")

    # description이 None일 경우 GPT가 이해하도록 기본 문구 제공
    desc_str = description if description not in (None, "None") else "날씨 정보 제공 없음"

    prompt = f"""
당신은 기상전문가 & 스타일리스트입니다.

다음 날씨 정보를 기반으로 옷차림 추천을 한국어로 작성하세요.

도시: {location}
기온: {temperature}°C
날씨: {weather}
상세 설명: {desc_str}

지침:
- 최대 4~6문장
- 겉옷/상의/하의/소품 구체적으로 추천
- 체감 온도, 활동성도 고려
- 자연스럽고 짧은 한국어 문장으로 작성
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
