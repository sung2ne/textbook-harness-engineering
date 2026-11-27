PERMISSION_MATRIX = {
    # 도구명 : { 호출자 타입 : 허용 인자 또는 None }
    "read_wiki": {
        "user": "*",        # 모든 인자 허용
        "service": "*",
        "system": "*",
    },
    "create_jira_ticket": {
        "user": {"project_id": ["PUBLIC"]},  # 공개 프로젝트만
        "service": {"project_id": "*"},
        "system": "*",
    },
    "send_email": {
        "user": None,                 # 사용자는 호출 불가
        "service": {"to_domain": ["@company.com"]},  # 사내 이메일만
        "system": "*",
    },
    "execute_shell": {
        "user": None,
        "service": None,
        "system": "*",                # 시스템만 가능, 그것도 사람 승인 후
    },
}
