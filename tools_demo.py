@mcp.tool()
def create_jira_ticket(project: str, title: str, description: str) -> dict:
    """Jira에 새 티켓을 생성한다.

    사용자가 버그 보고, 기능 요청, 작업 등록을 원할 때 사용한다.
    project는 사용자 권한이 있는 프로젝트만 가능.
    """
    # ... Jira API 호출
    return {"ticket_id": "PROJ-123", "url": "https://..."}
