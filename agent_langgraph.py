import json
import os
from typing import TypedDict
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from cost_tracker import CostTracker
from mcp_client import MCPClient
from schema import ReviewInput, ReviewOutput, ReviewComment


class ReviewState(TypedDict):
    input: ReviewInput
    diff_analysis: str
    related_policies: list[str]
    summary: str
    draft_comments: list[ReviewComment]
    validation_errors: list[str]
    final_output: ReviewOutput | None
    iterations: int
    cost: CostTracker


from review_prompts import SYSTEM_PROMPT

MODEL = os.environ.get("ANTHROPIC_AGENT_MODEL", "claude-opus-5-5")
llm = ChatAnthropic(model=MODEL, max_tokens=16000)  # thinking 토큰도 max_tokens 안에서 쓰인다
mcp = MCPClient.connect("http://localhost:8765/mcp")  # Ch 02에서 띄운 서버


def _strip_json_fence(text: str) -> str:
    """모델이 json 코드 펜스로 감싸 답하면 펜스를 걷어 낸다."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return text


def _track(cost: CostTracker, response):
    # LangChain의 input_tokens는 캐시 읽기·쓰기를 포함한 총 입력이다. 따로 빼서 넘긴다
    usage = response.usage_metadata
    details = usage.get("input_token_details", {})
    cache_read = details.get("cache_read", 0)
    cache_write = details.get("cache_creation", 0) + details.get("ephemeral_5m_input_tokens", 0) + details.get("ephemeral_1h_input_tokens", 0)  # TTL별 값이 있으면 cache_creation은 0이 된다
    cost.add_usage(usage["input_tokens"] - cache_read - cache_write, usage["output_tokens"], cache_read, cache_write)


def parse_input(state: ReviewState) -> ReviewState:
    return state  # 입력은 이미 ReviewInput 형식


def analyze_diff(state: ReviewState) -> ReviewState:
    diff = state["input"].diff.raw_text
    response = llm.invoke([
        ("system", "PR 디프를 분석해 변경 의도와 영향 범위를 요약하라."),
        ("user", diff),
    ])
    _track(state["cost"], response)
    return {**state, "diff_analysis": response.text}  # content는 thinking 블록이 섞인 목록일 수 있다


def search_related_policies(state: ReviewState) -> ReviewState:
    # PART 04 MCP 서버의 search_wiki. 위키 검색은 부분 문자열 일치라서 디프 분석문 대신 정해 둔 키워드로 찾는다
    found = mcp.call_tool("search_wiki", {"query": "코드 리뷰"})["result"]
    policies = [f"{p['title']}: {p['snippet']}" for p in found]
    return {**state, "related_policies": policies}


def _format_for_generate(state: ReviewState) -> str:
    text = (
        f"[PR 디프]\n{state['input'].diff.raw_text}\n\n"
        f"[디프 분석]\n{state['diff_analysis']}\n\n"
        "[관련 정책]\n" + "\n".join(state["related_policies"])
    )
    if state.get("validation_errors"):
        # 재시도: 지난 시도의 검증 오류를 알려 줘야 같은 실수를 되풀이하지 않는다
        text += "\n\n[이전 시도의 검증 오류. 고쳐서 다시 답하라]\n" + "\n".join(state["validation_errors"])
    return text


def generate_comments(state: ReviewState) -> ReviewState:
    iterations = state.get("iterations", 0) + 1
    if iterations > 3:
        raise RuntimeError("max_iterations_exceeded")

    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("user", _format_for_generate(state)),
    ])
    _track(state["cost"], response)

    try:
        parsed = json.loads(_strip_json_fence(response.text))
        summary, comments = parsed["summary"], [ReviewComment(**c) for c in parsed["comments"]]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        # 형식이 틀리면 예외로 끝내지 않고 오류를 상태에 남겨 재시도로 넘긴다
        return {**state, "draft_comments": [], "validation_errors": [f"형식 오류: {e}"], "iterations": iterations}
    return {**state, "summary": summary, "draft_comments": comments,
            "validation_errors": [], "iterations": iterations}


def validate_output(state: ReviewState) -> ReviewState:
    errors = list(state["validation_errors"])
    for c in state["draft_comments"]:
        if c.rule_id not in range(1, 7):
            errors.append(f"invalid rule_id: {c.rule_id}")
        if c.severity not in ["blocker", "warning", "suggestion"]:
            errors.append(f"invalid severity: {c.severity}")

    if not errors:
        final = ReviewOutput(
            summary=state["summary"],
            comments=state["draft_comments"][:5],
            elapsed_ms=0,
            cost_usd=state["cost"].total_cost(MODEL),
        )
        return {**state, "final_output": final, "validation_errors": []}

    return {**state, "validation_errors": errors}


def should_retry(state: ReviewState) -> str:
    if state["validation_errors"]:
        return "generate_comments"
    return END


graph = StateGraph(ReviewState)
graph.add_node("parse_input", parse_input)
graph.add_node("analyze_diff", analyze_diff)
graph.add_node("search_related_policies", search_related_policies)
graph.add_node("generate_comments", generate_comments)
graph.add_node("validate_output", validate_output)

graph.add_edge(START, "parse_input")
graph.add_edge("parse_input", "analyze_diff")
graph.add_edge("analyze_diff", "search_related_policies")
graph.add_edge("search_related_policies", "generate_comments")
graph.add_edge("generate_comments", "validate_output")
graph.add_conditional_edges("validate_output", should_retry, ["generate_comments", END])  # 갈 수 있는 노드를 적어야 그래프 그림에 재시도 엣지가 나온다

review_graph = graph.compile()


def run(input: ReviewInput) -> ReviewOutput:
    initial = {"input": input, "iterations": 0, "validation_errors": [], "cost": CostTracker()}
    final_state = review_graph.invoke(initial)
    return final_state["final_output"]
