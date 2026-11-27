import argparse
import glob
import importlib
import json
import os
import time

import yaml

from schema import PRMetadata, PRDiff, ReviewInput, ReviewOutput


# 점수 함수는 규칙 기반의 최소 구현입니다. 채점 기준은 위 표의 5개 차원입니다.
def score_detect_rate(comments, expected) -> float:
    """정답 위반 중 같은 rule_id의 코멘트가 있는 비율 x 30"""
    if not expected:
        return 30.0
    found = {c.rule_id for c in comments}
    return 30 * sum(v["rule_id"] in found for v in expected) / len(expected)


def score_false_positive(comments, expected) -> float:
    """정답에 없는 rule_id로 제기한 코멘트가 많을수록 20에서 깎는다"""
    if not comments:
        return 20.0
    wanted = {v["rule_id"] for v in expected}
    return 20 * sum(c.rule_id in wanted for c in comments) / len(comments)


def score_tone(comments) -> float:
    """LLM judge 자리를 규칙 검사로 대신한 최소 구현. 실제 평가는 PART 05 Ch 03의 판정관으로 바꾼다"""
    rude = ("멍청", "엉망", "쓰레기", "한심")
    return max(0.0, 20 - 10 * sum(any(w in c.message for w in rude) for c in comments))


def score_specificity(comments) -> float:
    """파일, 라인, 수정 제안 코드가 모두 있는 코멘트의 비율 x 15"""
    if not comments:
        return 0.0
    full = sum(bool(c.file) and c.line_start > 0 and bool(c.suggested_code) for c in comments)
    return 15 * full / len(comments)


def score_rule_match(comments, expected) -> float:
    """정답 위반 중 rule_id와 severity가 모두 같은 코멘트가 있는 비율 x 15"""
    if not expected:
        return 15.0
    got = {(c.rule_id, c.severity) for c in comments}
    return 15 * sum((v["rule_id"], v["severity"]) in got for v in expected) / len(expected)


def evaluate(case_path: str, agent_run_fn) -> dict:
    with open(case_path, encoding="utf-8") as f:
        case = yaml.safe_load(f)

    # 입력 구성
    input = ReviewInput(
        metadata=PRMetadata(
            repo=case["repo"], pr_number=case["pr_number"],
            title=case["title"], description=case.get("description", ""),
            author=case.get("author", ""), base_branch=case.get("base_branch", "main"),
            files_changed=list(case.get("files", [])),
        ),
        diff=PRDiff(raw_text=case["diff"], files={}),  # 파일별 디프가 있으면 여기에 채운다
    )

    # 에이전트 실행
    start = time.time()
    output: ReviewOutput = agent_run_fn(input)
    elapsed_ms = int((time.time() - start) * 1000)

    # 점수화
    detect = score_detect_rate(output.comments, case["expected_violations"])
    fp = score_false_positive(output.comments, case["expected_violations"])
    tone = score_tone(output.comments)  # LLM judge
    spec = score_specificity(output.comments)
    rule = score_rule_match(output.comments, case["expected_violations"])

    return {
        "case_id": case["case_id"],
        "scores": {
            "detect": detect, "false_positive": fp, "tone": tone,
            "specificity": spec, "rule_match": rule,
            "total": detect + fp + tone + spec + rule,
        },
        "elapsed_ms": elapsed_ms,
        "cost_usd": output.cost_usd,
    }


def evaluate_all(agent_run_fn, agent_name: str, limit: int = 50) -> dict:
    paths = sorted(glob.glob("golden/case_*.yaml"))[:limit]  # golden/에 있는 케이스 수까지만 돈다
    results, failures = [], {}
    for path in paths:
        try:
            results.append(evaluate(path, agent_run_fn))
        except Exception as e:  # max_iterations_exceeded, infinite_loop:도구이름 같은 사유별로 센다
            reason = str(e).split(":")[0] if isinstance(e, RuntimeError) else type(e).__name__
            failures[reason] = failures.get(reason, 0) + 1

    n = max(len(results), 1)
    keys = ("detect", "false_positive", "tone", "specificity", "rule_match")
    return {
        "agent": agent_name,
        "cases": len(paths),
        "n": len(results),
        "avg_total": sum(r["scores"]["total"] for r in results) / n,
        "avg_scores": {k: sum(r["scores"][k] for r in results) / n for k in keys},
        "avg_elapsed_ms": sum(r["elapsed_ms"] for r in results) / n,
        "total_cost_usd": sum(r["cost_usd"] for r in results),
        "failures": failures,
        "by_case": results,
    }


def print_summary(a: dict) -> None:
    s, n = a["avg_scores"], max(a["n"], 1)
    reasons = ", ".join(f"{v} {k}" for k, v in a["failures"].items())
    print(f"{a['agent']} 평가 결과 ({a['cases']} cases)")
    print("─" * 37)
    print(f"Avg total score:       {a['avg_total']:.1f} / 100")
    print(f"Avg detect rate:       {s['detect']:.1f} / 30")
    print(f"Avg false positive:    {s['false_positive']:.1f} / 20")
    print(f"Avg tone:              {s['tone']:.1f} / 20")
    print(f"Avg specificity:       {s['specificity']:.1f} / 15")
    print(f"Avg rule match:        {s['rule_match']:.1f} / 15")
    print()
    print(f"Avg latency:           {a['avg_elapsed_ms']:,.0f} ms")
    print(f"Total cost:            ${a['total_cost_usd']:.2f}")
    print(f"Cost per case:         ${a['total_cost_usd'] / n:.3f}")
    print()
    print(f"Failures:              {sum(a['failures'].values())}" + (f" ({reasons})" if reasons else ""))


AGENTS = {  # --agent 이름 -> (모듈, 표시 이름). 각 모듈은 run(input) 함수를 가진다
    "anthropic": ("agent_anthropic", "Anthropic SDK"),
    "openai": ("agent_openai", "OpenAI Agents SDK"),
    "langgraph": ("agent_langgraph", "LangGraph"),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", choices=AGENTS, required=True)
    parser.add_argument("--cases", type=int, default=50)
    parser.add_argument("--output")
    args = parser.parse_args()

    module, label = AGENTS[args.agent]
    aggregate = evaluate_all(importlib.import_module(module).run, label, args.cases)
    print_summary(aggregate)
    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(aggregate, f, ensure_ascii=False, indent=2)
