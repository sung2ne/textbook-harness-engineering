import os
from anthropic import Anthropic
from tools import get_weather, ANTHROPIC_TOOL

MODEL = os.environ.get("ANTHROPIC_AGENT_MODEL", "claude-opus-5-5")
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def run(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=[ANTHROPIC_TOOL],
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return next(b.text for b in response.content if b.type == "text")

        if response.stop_reason == "tool_use":
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            results = [
                {"type": "tool_result", "tool_use_id": t.id, "content": str(get_weather(**t.input))}
                for t in tool_uses
            ]

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": results})
            continue

        return f"unexpected stop_reason: {response.stop_reason}"


if __name__ == "__main__":
    print(run("서울과 도쿄 중 어디가 더 따뜻해?"))
