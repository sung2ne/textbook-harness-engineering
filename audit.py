import json
import logging
import time

audit = logging.getLogger("audit")
audit.setLevel(logging.INFO)
audit.addHandler(logging.FileHandler("audit.log"))  # 핸들러가 있어야 기록된다


def log_call(caller: dict, tool_name: str, input_summary: dict, status: str):
    audit.info(json.dumps({
        "ts": time.time(),
        "caller_id": caller["user_id"],
        "org_id": caller["org_id"],
        "tool": tool_name,
        "input_summary": input_summary,  # 시크릿 제외
        "status": status,
    }))
