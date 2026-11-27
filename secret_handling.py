import logging
import os
import re

# 1. 응답 마스킹
SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}"),   # API 키
    re.compile(r"Bearer\s+[a-zA-Z0-9._-]+"),  # Bearer 토큰
]

def mask_secrets(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("***", text)
    return text


# 2. 에러 메시지 sanitization
def safe_error_message(exc: Exception) -> str:
    msg = str(exc)
    return mask_secrets(msg)


# 3. 로그 마스킹
class MaskingFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        return mask_secrets(msg)
