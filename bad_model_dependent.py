import anthropic

client = anthropic.Anthropic()


def review_pr(pr_text: str) -> str:
    response = client.messages.create(
        model="claude-3-opus-20240229",  # 2026-01-05 종료. 지금은 404
        max_tokens=1024,
        messages=[{"role": "user", "content": pr_text}],
    )
    return response.content[0].text
