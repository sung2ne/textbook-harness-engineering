import os
from pydantic import AnyHttpUrl
from mcp.server import MCPServer
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings

RESOURCE = "https://wiki-mcp.company.internal:8765/mcp"


class WikiTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        """Bearer 토큰을 검증해 호출자 정보를 돌려준다. 실패하면 None(서버가 401로 응답)."""
        # 실제로는 사내 인증 서비스 호출
        if token == os.environ.get("DEV_TOKEN"):
            return AccessToken(token=token, client_id="dev-client", subject="dev-user", scopes=["wiki:read"], resource=RESOURCE)
        return None


AUTH = AuthSettings(
    issuer_url=AnyHttpUrl("https://auth.company.internal"),
    resource_server_url=AnyHttpUrl(RESOURCE),
    required_scopes=["wiki:read"],
    validate_token_resource=True,
)

mcp = MCPServer(
    "company-wiki",
    token_verifier=WikiTokenVerifier(),
    auth=AUTH,
)


@mcp.tool()
def search_wiki(query: str) -> list[dict]:
    """사내 위키 검색."""
    return []  # 검색 로직은 Ch 02의 search_wiki와 같습니다


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8765, stateless_http=True, json_response=True)
