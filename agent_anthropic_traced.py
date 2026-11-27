from opentelemetry import trace

from agent_anthropic import run
from schema import ReviewInput, ReviewOutput

tracer = trace.get_tracer(__name__)


def run_traced(input: ReviewInput) -> ReviewOutput:
    with tracer.start_as_current_span("agent.review") as span:
        span.set_attribute("agent.repo", input.metadata.repo)
        span.set_attribute("agent.pr_number", input.metadata.pr_number)
        span.set_attribute("agent.implementation", "anthropic_sdk")

        result = run(input)

        span.set_attribute("agent.cost_usd", result.cost_usd)
        span.set_attribute("agent.comment_count", len(result.comments))
        return result
