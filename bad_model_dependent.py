def review_pr(pr_text: str) -> str:
    response = anthropic.messages.create(
        model="claude-3-opus-20240229",  # 2026-01-05 종료. 지금은 404
        ...
    )
    return response.content[0].text
