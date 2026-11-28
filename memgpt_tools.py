from anthropic import beta_tool as tool  # Anthropic SDK의 도구 데코레이터. client.beta.messages.tool_runner에 넘긴다

@tool
def memory_archive(content: str):
    """현재 컨텍스트의 정보를 장기 보관소로 옮긴다."""
    archival_store.add(content)
    return "Archived."

@tool
def memory_recall(query: str) -> str:
    """장기 보관소에서 query와 관련된 정보를 가져온다."""
    return "\n".join(archival_store.search(query, top_k=5))  # tool_result에는 문자열이나 content 블록만 들어갑니다
