JUDGE_PROMPT = """\
다음 PR 리뷰 두 개 중 어느 쪽이 더 적절한가?

[입력 PR 디프]
{diff}

[리뷰 A]
{response_a}

[리뷰 B]
{response_b}

A 또는 B로만 답하시오.
"""
