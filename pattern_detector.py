from prometheus_client import Gauge

SUSPICIOUS_PATTERNS = [
    "I cannot help",
    "안전하지 않",
    "관련 없는 내용",
]

suspicious_rate = Gauge("suspicious_output_ratio", "문제 패턴이 든 출력의 비율", ["model"])


def count_suspicious(output: str) -> int:
    return sum(1 for p in SUSPICIOUS_PATTERNS if p in output)


# 운영 중 비율을 메트릭으로 export
def export_rate(model: str, outputs: list[str]):
    count = sum(1 for o in outputs if count_suspicious(o) > 0)
    suspicious_rate.labels(model=model).set(count / len(outputs))
