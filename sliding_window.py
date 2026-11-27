def trim_messages(messages: list[dict], max_turns: int = 10) -> list[dict]:
    """system 메시지를 유지하고 최근 max_turns 턴만 남김. Anthropic은 system을 messages에 넣지 않으므로 이때 system은 빈 리스트."""
    system = [m for m in messages if m["role"] == "system"]
    non_system = [m for m in messages if m["role"] != "system"]
    window = non_system[-(max_turns * 2):]  # user + assistant 페어
    # 맨 앞이 짝 없는 tool_result이면 API가 400을 돌려줍니다(실측). 일반 user 메시지가 나올 때까지 앞을 버립니다.
    while window and not (window[0]["role"] == "user" and isinstance(window[0]["content"], str)):
        window = window[1:]
    return system + window
