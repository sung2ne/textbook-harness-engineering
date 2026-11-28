try:
    result = execute_tool(tool_name, tool_input)
    tool_result = {"status": "success", "data": result}
except TimeoutError:
    tool_result = {"status": "error", "error": "timeout", "retry_after": 5}
except PermissionError:
    tool_result = {"status": "error", "error": "permission_denied", 
                   "message": "이 도구는 관리자 승인이 필요합니다."}
except Exception as e:
    tool_result = {"status": "error", "error": "unknown", "message": str(e)}
