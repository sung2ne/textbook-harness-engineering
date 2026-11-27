def detect_misuse(trajectory: Trajectory) -> list[str]:
    issues = []
    for step in trajectory.steps:
        if step["kind"] != "tool_call":
            continue
        # 1. JSON Schema 검증 실패는 자동 감지
        if not validate_against_schema(step["content"]):
            issues.append(f"schema_violation: {step['content']['name']}")
        # 2. 도구가 에러를 반환했는데 모델이 무시했는지
        if step["content"].get("result_status") == "error":
            next_steps = trajectory.steps[trajectory.steps.index(step)+1:]
            if not any(s["content"].get("references_error") for s in next_steps):
                issues.append("ignored_error")
    return issues
