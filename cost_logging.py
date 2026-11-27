# 토큰 1개당 USD. 2026-11-26 공식 가격표 기준이며 가격은 자주 바뀝니다.
# Anthropic: https://platform.claude.com/docs/en/about-claude/pricing (claude-haiku-5-5는 프롬프트 10만 토큰 이하 단가)
# OpenAI: https://developers.openai.com/api/docs/pricing (캐시 쓰기 요금이 없어 input_cache_write는 input과 같게 둠)
# thinking 토큰은 출력 토큰으로 청구되므로 output 단가를 적용합니다.
COST_TABLE = {
    "claude-opus-5-5": {
        "input": 4.0 / 1_000_000,
        "input_cached": 0.20 / 1_000_000,       # 캐시 읽기
        "input_cache_write": 5.0 / 1_000_000,   # 5분 캐시 쓰기
        "output": 20.0 / 1_000_000,
    },
    "claude-haiku-5-5": {
        "input": 0.10 / 1_000_000,
        "input_cached": 0.01 / 1_000_000,
        "input_cache_write": 0.125 / 1_000_000,
        "output": 0.50 / 1_000_000,
    },
    "claude-haiku-4-5": {
        "input": 1.0 / 1_000_000,
        "input_cached": 0.10 / 1_000_000,
        "input_cache_write": 1.25 / 1_000_000,
        "output": 5.0 / 1_000_000,
    },
    "gpt-6.1-sol": {
        "input": 2.0 / 1_000_000,
        "input_cached": 0.10 / 1_000_000,
        "input_cache_write": 2.0 / 1_000_000,
        "output": 10.0 / 1_000_000,
    },
    "gpt-6.1-terra": {
        "input": 1.0 / 1_000_000,
        "input_cached": 0.05 / 1_000_000,
        "input_cache_write": 1.0 / 1_000_000,
        "output": 5.0 / 1_000_000,
    },
}


def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
) -> float:
    """input_tokens는 캐시 토큰을 뺀 입력 토큰입니다(Anthropic 응답의 usage.input_tokens).

    OpenAI의 usage.prompt_tokens는 캐시 읽기를 포함하므로, 캐시 읽기를 빼서 넘깁니다.
    """
    rates = COST_TABLE[model]
    return (
        input_tokens * rates["input"]
        + cache_read_tokens * rates["input_cached"]
        + cache_write_tokens * rates["input_cache_write"]
        + output_tokens * rates["output"]
    )
