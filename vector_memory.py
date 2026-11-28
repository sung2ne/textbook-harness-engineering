import hashlib
import time


class VectorMemory:
    def __init__(self, user_id: str, vector_store):
        self.user_id = user_id
        self.store = vector_store

    def remember(self, fact: str):
        embedding = embed(fact)
        fact_id = hashlib.sha256(fact.encode("utf-8")).hexdigest()[:16]  # hash()는 프로세스마다 값이 달라 같은 사실이 중복 저장됩니다
        self.store.upsert(
            id=f"{self.user_id}:{fact_id}",
            vector=embedding,
            metadata={"user_id": self.user_id, "text": fact, "ts": time.time()},
        )

    def recall(self, query: str, top_k: int = 5) -> list[str]:
        query_embedding = embed(query)
        return self.store.query(
            vector=query_embedding,
            filter={"user_id": self.user_id},
            top_k=top_k,
        )
