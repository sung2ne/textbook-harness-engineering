from dataclasses import dataclass

@dataclass
class Caller:
    type: str        # 'user', 'system', 'service'
    id: str
    org_id: str
    roles: list[str]

def identify_caller(request) -> Caller:
    """API 요청에서 호출자를 식별."""
    # 예시용 단순화입니다. 실제로는 토큰의 서명과 만료를 검증해야 합니다(JWT, OAuth 등).
    token = request.headers.get("Authorization", "")
    if token.startswith("Bearer user-"):
        return _user_from_token(token)
    if token.startswith("Bearer svc-"):
        return _service_from_token(token)
    raise PermissionError("unauthenticated")
