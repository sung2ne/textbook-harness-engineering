from cost_logging import COST_TABLE  # PART 05 Ch 04의 cost_logging.py. 단가표는 한 곳에서만 정의한다


class CostTracker:
    def __init__(self):
        self.input_tokens = 0         # 캐시 읽기·쓰기를 뺀 일반 입력
        self.output_tokens = 0        # thinking 토큰도 출력으로 청구된다
        self.cached_input_tokens = 0  # 캐시 읽기
        self.cache_write_tokens = 0   # 캐시 쓰기

    def add_usage(self, input_tokens, output_tokens, cache_read=0, cache_write=0):
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.cached_input_tokens += cache_read
        self.cache_write_tokens += cache_write

    def add_call(self, response):  # Anthropic 응답의 usage 모양
        usage = response.usage
        self.add_usage(
            usage.input_tokens,
            usage.output_tokens,
            usage.cache_read_input_tokens or 0,
            usage.cache_creation_input_tokens or 0,
        )

    def total_cost(self, model: str) -> float:
        rates = COST_TABLE[model]
        return (
            self.input_tokens * rates["input"]
            + self.output_tokens * rates["output"]
            + self.cached_input_tokens * rates["input_cached"]
            + self.cache_write_tokens * rates["input_cache_write"]
        )
