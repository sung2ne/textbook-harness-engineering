from dataclasses import dataclass


@dataclass(frozen=True)
class RequestContext:
    org_id: str  # 인증을 통과한 요청에서 서버가 만든 값. 모델이 채우는 도구 인자가 아니다


class MultiTenantRAG:
    def search(self, query: str, ctx: RequestContext) -> list[str]:
        return self.store.query(
            embed(query),
            filter={"org_id": ctx.org_id},  # 강제 필터
            top_k=5,
        )
