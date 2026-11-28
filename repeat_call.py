import os

import anthropic

MODEL = os.environ.get("ANTHROPIC_AGENT_MODEL", "claude-opus-5-5")
client = anthropic.Anthropic()


def run_once(messages: list[dict]) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,  # thinking 토큰도 max_tokens 안에서 쓰인다
        messages=messages,
    )
    return next((b.text for b in response.content if b.type == "text"), "")  # thinking이 max_tokens를 다 쓰면 빈 답


def agreement(messages: list[dict], n: int = 5) -> float:
    """같은 입력을 n번 돌려 가장 많이 나온 답의 비율을 돌려줍니다."""
    answers = [run_once(messages) for _ in range(n)]
    return max(answers.count(a) for a in set(answers)) / n
