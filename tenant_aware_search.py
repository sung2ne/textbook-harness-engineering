# wiki_mcp_auth.py의 mcp에 이어 붙이는 조각이다. wiki_db와 lookup_caller는 서버가 구현한다
from mcp.server.auth.middleware.auth_context import get_access_token


@mcp.tool()
def search_wiki(query: str) -> list[dict]:
    """사내 위키 검색. 호출자의 org_id 안에서만 검색한다."""
    token = get_access_token()  # 검증기가 확인한 호출자
    if token is None or token.subject is None:
        return []  # 호출자를 모르면 기본 거부
    caller = lookup_caller(token.subject)  # 토큰의 sub(사용자)로 org_id·team_ids 조회. client_id는 호스트 앱 식별자라 쓰지 않는다
    org_id = caller["org_id"]

    # org_id 기반으로 검색 범위를 자동 제한
    results = wiki_db.search(query=query, org_id=org_id)

    # 추가 권한 체크
    visible = [r for r in results if can_user_see(caller, r)]
    return visible


def can_user_see(caller: dict, page: dict) -> bool:
    """페이지의 가시성 정책에 따라 사용자가 볼 수 있는지 판단."""
    if page["visibility"] == "public":
        return True
    if page["visibility"] == "team":
        return page["team_id"] in caller["team_ids"]
    if page["visibility"] == "owner":
        return page["owner_id"] == caller["user_id"]
    return False
