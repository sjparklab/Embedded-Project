# OpenAI API 호출 형식 및 제어

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt_stream(prompt: str):
    stream = client.chat.completions.create(
        model="gpt-5-nano",
        stream=True,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta:
            text = chunk.choices[0].delta.content
            if text:
                yield text