class RAGSystem:
    """공통 지식 검색."""
    def __init__(self, kb_store):
        self.store = kb_store

    def search(self, query: str) -> list[str]:
        return self.store.query(embed(query), top_k=5)


class UserMemory:
    """사용자별 개인 메모리."""
    def __init__(self, user_id: str, mem_store):
        self.user_id = user_id
        self.store = mem_store

    def recall(self, query: str) -> list[str]:
        return self.store.query(
            embed(query),
            filter={"user_id": self.user_id},  # 강제 필터
            top_k=5,
        )
