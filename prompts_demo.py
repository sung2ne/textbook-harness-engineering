@mcp.prompt()
def code_review(diff_url: str) -> list[dict]:
    """PR 디프 URL을 받아 표준 리뷰 절차를 시작한다."""
    return [
        {
            "role": "user",
            "content": f"""\
다음 PR 디프를 검토해 주세요.

URL: {diff_url}

검토 절차:
1. 골든 룰 6개를 우선 점검합니다.
2. 보안 위반(시크릿, SQL injection, XSS)을 점검합니다.
3. 성능 회귀(N+1, 잠금 경합)를 점검합니다.
4. 가독성·테스트 적절성을 마지막으로 점검합니다.

의견은 5개 이내, 정중한 톤으로 작성해 주세요.
""",
        }
    ]
