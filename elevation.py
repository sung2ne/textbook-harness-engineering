import time


class ElevatedSession:
    """짧은 시간 동안만 권한이 승격된 세션."""
    def __init__(self, caller, reason, duration_seconds=300):
        self.caller = caller
        self.reason = reason
        self.expires_at = time.time() + duration_seconds
        audit_log.write({"event": "elevation_start", 
                         "caller": caller.id, 
                         "reason": reason})

    def is_active(self) -> bool:
        return time.time() < self.expires_at

    def __enter__(self):
        return self

    def __exit__(self, *args):
        audit_log.write({"event": "elevation_end", "caller": self.caller.id})


async def emergency_rollback(caller, reason):
    with ElevatedSession(caller, reason, duration_seconds=600) as session:
        # 평소에는 막혀 있는 운영 DB 직접 변경이 가능해진다.
        await rollback_database(session)
