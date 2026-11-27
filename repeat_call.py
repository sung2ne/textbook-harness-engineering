import os

import anthropic

MODEL = os.environ.get("ANTHROPIC_AGENT_MODEL", "claude-opus-5-5")
client = anthropic.Anthropic()


def run_once(messages: list[dict]) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=messages,
    )
    return next(b.text for b in response.content if b.type == "text")


def agreement(messages: list[dict], n: int = 5) -> float:
    """같은 입력을 n번 돌려 가장 많이 나온 답의 비율을 돌려줍니다."""
    answers = [run_once(messages) for _ in range(n)]
    return max(answers.count(a) for a in set(answers)) / n
