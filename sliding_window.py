def _block_type(b) -> str:
    return b["type"] if isinstance(b, dict) else b.type  # dict와 SDK가 돌려준 블록 객체를 모두 받습니다


def is_plain_user(m: dict) -> bool:
    """tool_result가 없는 user 메시지인지 봅니다(content가 문자열이든 블록 목록이든)."""
    return m["role"] == "user" and not (
        isinstance(m["content"], list) and any(_block_type(b) == "tool_result" for b in m["content"])
    )


def drop_thinking(messages: list[dict]) -> list[dict]:
    """앞부분을 잘라 낸 뒤 남은 assistant 메시지에서 thinking 블록을 뺍니다."""
    return [
        {**m, "content": [b for b in m["content"] if _block_type(b) not in ("thinking", "redacted_thinking")]}
        if m["role"] == "assistant" and isinstance(m["content"], list) else m
        for m in messages
    ]


def trim_messages(messages: list[dict], max_turns: int = 10) -> list[dict]:
    """맨 앞 system 메시지(OpenAI 형식)를 유지하고 최근 max_turns 턴만 남김. Anthropic은 처음 system 프롬프트를 messages 밖에 두므로 이때 system은 빈 리스트."""
    if not messages or not is_plain_user(messages[-1]):  # 도구 호출이 진행 중일 때는 자르지 않습니다
        return messages
    system = messages[:1] if messages[0]["role"] == "system" else []  # 대화 중에 넣은 role "system" 메시지는 제자리에 둡니다
    non_system = messages[len(system):]
    window = non_system[-(max_turns * 2):]  # user + assistant 페어
    # 맨 앞이 짝 없는 tool_result이면 API가 400을 돌려줍니다(실측). 일반 user 메시지가 나올 때까지 앞을 버립니다.
    while window and not is_plain_user(window[0]):
        window = window[1:]
    return system + (drop_thinking(window) if len(window) < len(non_system) else window)
