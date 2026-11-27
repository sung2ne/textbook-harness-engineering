# 안 좋은 패턴 — 기본 허용
def can_user_see(caller, page):
    if page["visibility"] == "private" and page["owner_id"] != caller["user_id"]:
        return False
    return True  # 알 수 없는 visibility는 허용 — 위험
