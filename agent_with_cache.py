from anthropic import Anthropic
from prompts.code_reviewer import SYSTEM_PROMPT

MODEL = "claude-opus-5-5"
client = Anthropic()

response = client.messages.create(
    model=MODEL,
    max_tokens=4096,  # thinking 토큰도 max_tokens 안에서 쓰인다
    system=[
        {
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": "다음 PR 디프를 리뷰해 줘.\n(디프 내용)"}],
)

usage = response.usage
print("cache_creation:", usage.cache_creation_input_tokens)
print("cache_read:", usage.cache_read_input_tokens)
