import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from prompts import SYSTEM_PROMPT
from cost_tracker import CostTracker
from schema import ReviewInput, ReviewOutput, ReviewDraft

MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")  # 2026-12-11 종료되는 gpt-5의 대체 모델

# MCP 서버 연결: Ch 02에서 띄운 서버(streamable-http, 경로 /mcp)
wiki_mcp = MCPServerStreamableHttp(params={"url": "http://localhost:8765/mcp"})


review_agent = Agent(
    name="code-reviewer",
    instructions=SYSTEM_PROMPT,
    model=MODEL,
    mcp_servers=[wiki_mcp],
    output_type=ReviewDraft,  # summary, comments만 있는 스키마
)


async def _run_async(input: ReviewInput, hooks=None) -> ReviewOutput:
    cost = CostTracker()

    async with wiki_mcp:  # 서버 연결을 열고, 블록을 벗어나면 닫는다
        result = await Runner.run(
            review_agent,
            input=_format_pr_input(input),
            max_turns=30,        # MAX_ITERATIONS와 동일
            hooks=hooks,
        )

    draft: ReviewDraft = result.final_output
    usage = result.context_wrapper.usage
    cached = usage.input_tokens_details.cached_tokens
    # OpenAI의 입력 토큰 수는 캐시에서 읽은 분량을 포함한다. 일반 입력과 캐시 읽기로 나눠 넘긴다
    cost.add_usage(usage.input_tokens - cached, usage.output_tokens, cache_read=cached)
    return ReviewOutput(
        summary=draft.summary,
        comments=draft.comments[:5],
        elapsed_ms=0,            # 외부에서 채움
        cost_usd=cost.total_cost(MODEL),
    )


_loop = asyncio.new_event_loop()  # 평가가 run()을 여러 번 부르므로 이벤트 루프 하나를 계속 쓴다


def run(input: ReviewInput) -> ReviewOutput:
    return _loop.run_until_complete(_run_async(input))


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


from agents.exceptions import UserError
from openai_loop_guard import LoopGuard


def run(input: ReviewInput) -> ReviewOutput:  # 위의 run을 이것으로 바꾼다
    try:
        return _loop.run_until_complete(_run_async(input, hooks=LoopGuard(threshold=5)))
    except UserError as e:  # SDK는 도구 단계의 예외를 UserError로 감싼다. 원래 예외를 꺼내 던진다
        if isinstance(e.__cause__, RuntimeError):
            raise e.__cause__ from None
        raise
