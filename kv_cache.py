# Anthropic은 cache_control을 직접 지정해야 캐시된다(위 cache_demo.py). 지정하지 않으면 캐시되지 않는다
# OpenAI는 지원 모델에서 기본으로 켜져 있어 따로 켤 필요가 없다(1,024토큰 이상인 앞부분). gpt-5.6 이후 모델은 prompt_cache_options로 방식을 바꿀 수 있다
import os

MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")  # 2026-12-11 종료되는 gpt-5의 대체 모델

response = openai_client.chat.completions.create(
    model=MODEL,
    messages=messages,
)
print(getattr(response.usage.prompt_tokens_details, "cached_tokens", 0))  # 캐시에서 읽은 토큰 수(세부 항목이 없으면 0)
