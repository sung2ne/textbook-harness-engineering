from anthropic import Anthropic

MODEL = "claude-opus-5-5"
client = Anthropic()

response = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=messages,
)

usage = response.usage
print("cache_creation:", usage.cache_creation_input_tokens)
print("cache_read:", usage.cache_read_input_tokens)
