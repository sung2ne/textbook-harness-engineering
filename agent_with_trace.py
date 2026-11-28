from opentelemetry import trace

tracer = trace.get_tracer(__name__)


def run_agent(user_id: str, conversation_id: str, message: str) -> str:
    with tracer.start_as_current_span("agent.run") as span:
        span.set_attribute("app.user.id", user_id)
        span.set_attribute("gen_ai.conversation.id", conversation_id)

        # 자식 LLM 호출이 자동으로 부모 span 아래에 들어감
        result = call_anthropic(message)

        span.set_attribute("app.response.length", len(result))
        return result
