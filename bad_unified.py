# 안 좋은 패턴 — RAG와 메모리를 한 인덱스로
class UnifiedKnowledge:
    def add(self, text: str, source: str):
        self.store.upsert(embed(text), metadata={"source": source})

    def search(self, query: str) -> list[str]:
        return self.store.query(embed(query), top_k=5)
