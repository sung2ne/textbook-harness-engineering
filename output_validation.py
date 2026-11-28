import re

SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9_-]{20,}"),    # API 키(sk-ant-api03-…, sk-proj-… 포함)
    re.compile(r"AKIA[A-Z0-9]{16}"),         # AWS Access Key
    re.compile(r"-----BEGIN.*PRIVATE KEY"),  # 개인키
]

DANGEROUS_COMMANDS = ["rm -rf", "DROP TABLE", "git push --force", "git push -f"]


def is_safe_output(text: str) -> tuple[bool, str]:
    for p in SECRET_PATTERNS:
        if p.search(text):
            return (False, "secret_detected")
    for cmd in DANGEROUS_COMMANDS:
        if cmd.lower() in text.lower():
            return (False, "dangerous_command")
    return (True, "")
