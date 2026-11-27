from agents import add_trace_processor
from agents.tracing import TracingProcessor

from agent_openai import run
from schema import ReviewInput, ReviewOutput


class PrintProcessor(TracingProcessor):
    """span이 끝날 때마다 종류와 이름을 찍는다. OTel로 보내려면 on_span_end에서 OTel span을 만든다."""

    def on_trace_start(self, trace): pass
    def on_trace_end(self, trace): pass
    def on_span_start(self, span): pass
    def on_span_end(self, span):
        print(f"span: {span.span_data.type} {getattr(span.span_data, 'name', '')}")
    def shutdown(self): pass
    def force_flush(self): pass


add_trace_processor(PrintProcessor())  # 기본 처리기(OpenAI Traces 대시보드로 전송)에 더해진다


def run_traced(input: ReviewInput) -> ReviewOutput:
    return run(input)
