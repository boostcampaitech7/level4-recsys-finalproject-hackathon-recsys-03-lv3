import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("UPSTAGE_TOKEN"),
    base_url="https://api.upstage.ai/v1/solar"
)


def chat_with_solar(messages):
    response = client.chat.completions.create(
        model="solar-pro",
        messages=messages,
        temperature=0.0  # 같은 프롬프트에 대해 항상 유사한 출력
    )
    return json.loads(response.choices[0].message.content)
