from trajectory import Trajectory


def detect_hallucination(trajectory: Trajectory) -> bool:
    tool_facts = extract_facts_from_tool_results(trajectory)
    answer_facts = extract_facts_from_answer(trajectory.final_output)
    unsourced = answer_facts - tool_facts
    if len(unsourced) > 0:
        return True  # 도구에서 얻지 않은 사실이 답에 있음
    return False
