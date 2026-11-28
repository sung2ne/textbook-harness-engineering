from sliding_window import drop_thinking, is_plain_user


def summarize_old_messages(messages: list[dict], keep_recent: int = 10) -> list[dict]:
    """오래된 메시지를 요약 메시지 1개로 대체."""
    if len(messages) <= keep_recent + 1:  # +1은 system
        return messages
    if not is_plain_user(messages[-1]):  # 도구 호출이 진행 중일 때는 요약하지 않습니다
        return messages

    system = messages[:1] if messages[0]["role"] == "system" else []
    non_system = messages[len(system):]
    old, recent = non_system[:-keep_recent], non_system[-keep_recent:]
    # recent의 맨 앞이 짝 없는 tool_result가 되지 않도록 턴 경계에서 자르는 일은 위 sliding window와 같습니다
    while not is_plain_user(recent[0]):
        old.append(recent.pop(0))

    summary = call_summarizer(old)
    summary_message = {
        "role": "user",  # Anthropic은 messages 맨 앞에 system 역할을 둘 수 없습니다(OpenAI라면 "system")
        "content": f"[이전 대화 요약]\n{summary}"
    }

    return system + [summary_message] + drop_thinking(recent)  # 요약 뒤에 남긴 턴의 thinking은 prefix check를 통과하지 못합니다
