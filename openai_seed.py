import os

import openai

MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")  # 2026-12-11 종료되는 gpt-5의 대체 모델
client = openai.OpenAI()

messages = [{"role": "user", "content": "한 문장으로 자기소개를 해 주세요."}]
response = client.chat.completions.create(
    model=MODEL,
    seed=42,
    messages=messages,
)
fingerprint = response.system_fingerprint  # 백엔드 설정이 바뀌었는지 감시하는 값
