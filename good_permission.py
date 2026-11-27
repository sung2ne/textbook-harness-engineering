# 좋은 패턴 — 기본 거부
def can_user_see(caller, page):
    if page["visibility"] == "public":
        return True
    if page["visibility"] == "team" and page["team_id"] in caller["team_ids"]:
        return True
    if page["visibility"] == "owner" and page["owner_id"] == caller["user_id"]:
        return True
    return False  # 알 수 없는 visibility는 거부
