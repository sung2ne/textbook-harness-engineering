@tool
def memory_archive(content: str):
    """현재 컨텍스트의 정보를 장기 보관소로 옮긴다."""
    archival_store.add(content)
    return "Archived."

@tool
def memory_recall(query: str) -> list[str]:
    """장기 보관소에서 query와 관련된 정보를 가져온다."""
    return archival_store.search(query, top_k=5)
