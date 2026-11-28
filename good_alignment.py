# 올바른 정렬 - 고정 부분을 앞 블록에 두고 그 끝에 캐시 표시, 사용자 정보는 뒤 블록
system = [
    {"type": "text", "text": f"{COMPANY_POLICY}\n{AGENT_DEFINITION}",
     "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": f"[사용자 맥락]\n이름: {user.name}"},
]
