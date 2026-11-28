async def execute_with_gate(tool_name, tool_input, caller, session=None):
    # 1. 권한 매트릭스 확인
    elevated = session is not None and session.is_active()  # 만료되면 평소 권한으로 돌아감
    if not is_authorized(tool_name, tool_input, caller, elevated=elevated):
        audit_log.write({"caller": caller.id, "tool": tool_name, "result": "permission_denied"})
        return {"status": "permission_denied", "tool": tool_name}

    # 2. 위험 도구는 사람 승인 요청
    if tool_name in HIGH_RISK_TOOLS:
        approval = await request_human_approval(tool_name, tool_input, caller)
        if not approval.granted:
            audit_log.write({"caller": caller.id, "tool": tool_name, "result": "denied_by_human"})
            return {"status": "denied_by_human", "tool": tool_name}
        audit_log.write({"caller": caller.id, "tool": tool_name, "result": "approved_by_human"})

    # 3. 실행 + 감사 로그
    audit_log.write({"caller": caller.id, "tool": tool_name, "input": tool_input})
    try:
        result = await execute(tool_name, tool_input)
        audit_log.write({"caller": caller.id, "tool": tool_name, "result": "ok"})
        return {"status": "ok", "data": result}
    except Exception as e:
        audit_log.write({"caller": caller.id, "tool": tool_name, "error": str(e)})
        return {"status": "error", "message": str(e)}
