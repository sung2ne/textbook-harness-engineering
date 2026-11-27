from mcp.server import MCPServer

mcp = MCPServer("policy-server")


@mcp.resource("policy://golden-rules")
def golden_rules() -> str:
    """회사의 골든 룰 6개를 마크다운으로 반환한다."""
    return """\
# 골든 룰

1. 변경한 코드 경로마다 테스트가 함께 변경된다.
2. 외부 입력은 경계에서 검증된다.
3. 데이터 변경은 트랜잭션 안에서만 일어난다.
4. 비밀은 코드, 로그, 설정 파일에 들어가지 않는다.
5. 한 PR은 한 가지 변경 의도만 담는다.
6. 운영 환경은 자동화된 게이트를 통해서만 변경된다.
"""


@mcp.resource("schema://users")
def users_schema() -> str:
    """users 테이블의 스키마를 반환한다."""
    return """\
table users
  id        bigint  primary key
  email     text    unique not null
  name      text
  created_at timestamptz
"""
