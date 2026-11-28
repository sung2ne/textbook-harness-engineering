import os
from anthropic import Anthropic
from mcp_client import MCPClient
from review_prompts import SYSTEM_PROMPT
from cost_tracker import CostTracker
from schema import ReviewInput, ReviewOutput, ReviewComment
import json

MODEL = os.environ.get("ANTHROPIC_AGENT_MODEL", "claude-opus-5-5")
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
mcp = MCPClient.connect("http://localhost:8765/mcp")  # 위에서 띄운 streamable-http 서버


mcp_tools = mcp.list_tools()
anthropic_tools = [mcp.to_anthropic_tool(t) for t in mcp_tools]


MAX_ITERATIONS = 30
DUPLICATE_THRESHOLD = 5


def run(input: ReviewInput) -> ReviewOutput:
    cost = CostTracker()
    messages = [{
        "role": "user",
        "content": _format_pr_input(input),
    }]
    iterations = 0
    tool_call_history = {}

    while True:
        iterations += 1
        if iterations > MAX_ITERATIONS:
            raise RuntimeError("max_iterations_exceeded")

        response = client.messages.create(
            model=MODEL,
            max_tokens=16000,  # thinking 토큰도 max_tokens 안에서 쓰인다
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            tools=anthropic_tools,
            messages=messages,
        )
        cost.add_call(response)

        if response.stop_reason == "end_turn":
            return _parse_output(response, cost, iterations)

        if response.stop_reason == "tool_use":
            # 한 응답에 tool_use가 여러 개일 수 있다. 모두 실행하고 tool_result를 한 user 메시지에 모은다
            tool_results = []
            for tool_use in (b for b in response.content if b.type == "tool_use"):
                key = f"{tool_use.name}:{json.dumps(tool_use.input, sort_keys=True)}"
                tool_call_history[key] = tool_call_history.get(key, 0) + 1
                if tool_call_history[key] >= DUPLICATE_THRESHOLD:
                    raise RuntimeError(f"infinite_loop:{tool_use.name}")

                tool_result = mcp.call_tool(tool_use.name, tool_use.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(tool_result),
                })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            continue

        raise RuntimeError(f"unexpected_stop_reason: {response.stop_reason}")


def _format_pr_input(input: ReviewInput) -> str:
    return f"""\
[PR Metadata]
Repo: {input.metadata.repo}
PR: #{input.metadata.pr_number}
Title: {input.metadata.title}
Description: {input.metadata.description}

[Diff]
{input.diff.raw_text}
"""


def _strip_json_fence(text: str) -> str:
    """모델이 json 코드 펜스로 감싸 답하면 펜스를 걷어 낸다."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return text


def _parse_output(response, cost: CostTracker, iterations: int) -> ReviewOutput:
    text = next(b.text for b in response.content if b.type == "text")  # 첫 블록이 thinking일 수 있다
    parsed = json.loads(_strip_json_fence(text))
    comments = [ReviewComment(**c) for c in parsed["comments"]]
    return ReviewOutput(
        summary=parsed["summary"],
        comments=comments[:5],   # 최대 5개
        elapsed_ms=0,            # 외부에서 채움
        cost_usd=cost.total_cost(MODEL),
    )
