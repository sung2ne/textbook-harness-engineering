from cost_logging import COST_TABLE  # PART 05 Ch 04에서 정의한 단가표 하나를 함께 씁니다


def estimate_cost(span: dict) -> float:
    rates = COST_TABLE[span["gen_ai.request.model"]]
    cached = span.get("gen_ai.usage.cache_read.input_tokens", 0)
    # 캐시 쓰기 속성은 계측마다 이름이 다릅니다(SDK span은 cache_write, Traceloop span은 cache_creation)
    written = span.get(
        "gen_ai.usage.cache_write.input_tokens",
        span.get("gen_ai.usage.cache_creation.input_tokens", 0),
    )
    # 규약상 input_tokens는 캐시 토큰을 포함하므로 빼서 일반 입력만 남깁니다(이중 청구 방지)
    plain = span.get("gen_ai.usage.input_tokens", 0) - cached - written
    return (
        plain * rates["input"]
        + cached * rates["input_cached"]
        + written * rates["input_cache_write"]
        + span.get("gen_ai.usage.output_tokens", 0) * rates["output"]
    )
