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
- 출력 형식은 반드시 JSON이어야 합니다.
- JSON 키: "keyword", "advice"
- "keyword"는 다음 중 하나 선택: "VENTILATION", "HEATING", "COOLING", "NORMAL"
  - VENTILATION: 환기가 필요할 때 (예: CO2 높음, 습도 높음 등)
  - HEATING: 난방이 필요할 때 (예: 기온 낮음)
  - COOLING: 냉방이 필요할 때 (예: 기온 높음)
  - NORMAL: 특별한 조치가 필요 없을 때
- "advice": 3~5문장의 자연스러운 한국어 조언
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
        # 폴백 처리
        return {"keyword": "NORMAL", "advice": content if 'content' in locals() else "조언을 생성할 수 없습니다."}
