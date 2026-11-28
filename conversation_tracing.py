from opentelemetry import trace

tracer = trace.get_tracer(__name__)


def call_in_conversation(conv_id: str, message: str):
    with tracer.start_as_current_span("agent.turn") as span:
        span.set_attribute("gen_ai.conversation.id", conv_id)
        # set_attribute는 이 span에만 붙는다. 자식 span에도 필요하면 자식마다 붙이거나 baggage→attribute 복사 프로세서를 둔다
        return run_agent_logic(message)
