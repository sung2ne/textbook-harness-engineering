from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.anthropic import AnthropicInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor


def setup_tracing(service_name: str, otlp_endpoint: str):
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    AnthropicInstrumentor().instrument()
    OpenAIInstrumentor().instrument()


if __name__ == "__main__":
    setup_tracing(
        service_name="code-review-agent",
        otlp_endpoint="http://otel-collector:4317",
    )
    # 이 시점부터 모든 Anthropic·OpenAI 호출이 자동으로 trace됨
