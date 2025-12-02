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

    prompt = f"""
당신은 기상전문가 & 스타일리스트입니다.

다음 정보를 기반으로 옷차림 추천을 한국어로 작성하세요.

도시: {location}
기온: {temperature}°C
날씨: {weather}
상세 설명: {description}

지침:
- 최대 4~6문장
- 겉옷/상의/하의 구체적 추천
- 필요한 소품 제안(우산, 모자 등)
- 활동성/체감 온도 언급
- 자연스럽고 짧은 한국어 문장으로 작성
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # OpenAI 응답 본문
    return response.choices[0].message.content.strip()
