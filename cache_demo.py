from anthropic import Anthropic

MODEL = "claude-opus-5-5"
client = Anthropic()

response = client.messages.create(
    model=MODEL,
    max_tokens=4096,  # thinking 토큰도 max_tokens 안에서 쓰인다
    system=[
        {
            "type": "text",
            "text": LONG_POLICY_DOCUMENT,  # 50,000 토큰
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=messages,
)
print(response.usage.cache_creation_input_tokens, response.usage.cache_read_input_tokens)
