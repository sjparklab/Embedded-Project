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
- 출력 형식은 반드시 JSON이어야 합니다.
- JSON 키: "keyword", "advice"
- "keyword"는 다음 중 하나 선택: "UMBRELLA", "COLD", "HOT", "NORMAL"
  - UMBRELLA: 비나 눈이 와서 우산이 필요할 때
  - COLD: 날씨가 추워 따뜻한 옷차림이 필요할 때
  - HOT: 날씨가 더워 가벼운 옷차림이 필요할 때
  - NORMAL: 평범한 날씨일 때
- "advice": 3~5문장의 구체적인 한국어 옷차림 추천 (겉옷/상의/하의/소품 등)
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    import json
    try:
        content = response.choices[0].message.content.strip()
        result = json.loads(content)
        return result
    except Exception as e:
        print(f"JSON parsing failed: {e}")
        return {"keyword": "NORMAL", "advice": content if 'content' in locals() else "추천을 생성할 수 없습니다."}
