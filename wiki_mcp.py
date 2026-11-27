from mcp.server import MCPServer

mcp = MCPServer("company-wiki")

# 가짜 위키 데이터
FAKE_WIKI = {
    "harness-engineering": {
        "title": "하네스 엔지니어링 도입 가이드",
        "content": "Agent = Model + Harness. 가이드, 센서, 데이터 파이프라인 3분할로 구성한다.",
    },
    "code-review-policy": {
        "title": "코드 리뷰 정책",
        "content": "PR당 의견 5개 이내. 골든 룰 6개 우선 점검. 비밀 노출 시 즉시 차단.",
    },
    "incident-response": {
        "title": "사고 대응 절차",
        "content": "사고 인지 → 1차 격리 → 영향 범위 평가 → 복구 → 사후 회고.",
    },
}


@mcp.tool()
def search_wiki(query: str) -> list[dict]:
    """사내 위키에서 키워드를 포함하는 페이지를 검색한다.

    사용자가 사내 정책, 가이드, 절차를 물을 때 사용한다.
    예: '하네스 엔지니어링', '코드 리뷰'.
    """
    results = []
    q = query.lower()
    for slug, page in FAKE_WIKI.items():
        if q in page["title"].lower() or q in page["content"].lower():
            results.append({
                "slug": slug,
                "title": page["title"],
                "snippet": page["content"][:80] + "...",
            })
    return results


if __name__ == "__main__":
    mcp.run()
