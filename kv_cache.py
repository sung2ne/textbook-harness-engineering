# Anthropic은 cache_control을 직접 지정해야 캐시된다(위 cache_demo.py). 지정하지 않으면 캐시되지 않는다
# OpenAI는 지원 모델에서 기본으로 켜져 있어 켜는 옵션이 없다. 같은 앞부분(prefix)이 반복되면 자동으로 적용된다
import os

MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")  # 2026-12-11 종료되는 gpt-5의 대체 모델

response = openai_client.chat.completions.create(
    model=MODEL,
    messages=messages,
)
print(response.usage.prompt_tokens_details.cached_tokens)  # 캐시에서 읽은 토큰 수
