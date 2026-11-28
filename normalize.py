def normalize_input(text: str) -> str:
    """평가 입력을 정규화."""
    text = text.strip()
    text = text.replace("\u00a0", " ")  # non-breaking space
    text = text.replace("\u201c", '"').replace("\u201d", '"')  # 스마트 큰따옴표
    text = text.replace("\u2018", "'").replace("\u2019", "'")  # 스마트 작은따옴표
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text
