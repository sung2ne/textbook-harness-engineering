def normalize_input(text: str) -> str:
    """평가 입력을 정규화."""
    text = text.strip()
    text = text.replace("\u00a0", " ")  # non-breaking space
    text = text.replace("\u201c", '"').replace("\u201d", '"')  # 스마트 따옴표
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text
