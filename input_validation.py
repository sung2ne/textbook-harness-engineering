SUSPICIOUS_PATTERNS = [
    "이전 지시", "ignore previous", "system:", "assistant:",
    "<|im_start|>", "<|im_end|>",  # OpenAI ChatML 구분자
    "Human:", "Assistant:",         # 옛 Anthropic Text Completions 형식의 구분자
]


def detect_injection_attempt(text: str) -> bool:
    lower = text.lower()
    return any(p.lower() in lower for p in SUSPICIOUS_PATTERNS)
