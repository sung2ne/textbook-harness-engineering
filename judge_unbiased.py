import os

from openai import OpenAI

from judge_basic import JUDGE_PROMPT

client = OpenAI()
JUDGE_MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")  # 후보(Claude)와 다른 가족의 판정 모델


def call_judge(prompt: str) -> str:
    """판정 모델에 묻고 답의 첫 글자("A" 또는 "B")만 돌려준다"""
    response = client.responses.create(model=JUDGE_MODEL, input=prompt)
    return response.output_text.strip()[:1]


def judge(response_a, response_b, diff) -> str:
    # 1차: A가 먼저
    result_1 = call_judge(JUDGE_PROMPT.format(
        diff=diff, response_a=response_a, response_b=response_b
    ))

    # 2차: B가 먼저
    result_2 = call_judge(JUDGE_PROMPT.format(
        diff=diff, response_a=response_b, response_b=response_a
    ))

    # 두 번 모두 같은 후보를 골랐으면 그 후보 승
    if result_1 == "A" and result_2 == "B":  # 둘 다 *원래 A* 선택
        return "A"
    if result_1 == "B" and result_2 == "A":  # 둘 다 *원래 B* 선택
        return "B"
    return "tie"  # 결과가 일관되지 않으면 무승부
