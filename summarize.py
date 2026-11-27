def summarize_old_messages(messages: list[dict], keep_recent: int = 10) -> list[dict]:
    """오래된 메시지를 요약 메시지 1개로 대체."""
    if len(messages) <= keep_recent + 1:  # +1은 system
        return messages

    system = [m for m in messages if m["role"] == "system"]
    non_system = [m for m in messages if m["role"] != "system"]
    old, recent = non_system[:-keep_recent], non_system[-keep_recent:]
    # recent의 맨 앞이 짝 없는 tool_result가 되지 않도록 턴 경계에서 자르는 일은 위 sliding window와 같습니다

    summary = call_summarizer(old)
    summary_message = {
        "role": "user",  # Anthropic은 messages에 system 역할이 없습니다(OpenAI라면 "system")
        "content": f"[이전 대화 요약]\n{summary}"
    }

    return system + [summary_message] + recent
