def cohens_kappa(rater_1: list[int], rater_2: list[int]) -> float:
    """두 라벨러의 라벨 리스트를 받아 Cohen's κ를 계산."""
    assert len(rater_1) == len(rater_2)
    n = len(rater_1)

    # 실제 일치 비율
    agree = sum(1 for a, b in zip(rater_1, rater_2) if a == b)
    p_o = agree / n

    # 우연 일치 비율
    categories = set(rater_1) | set(rater_2)
    p_e = 0
    for c in categories:
        p1 = rater_1.count(c) / n
        p2 = rater_2.count(c) / n
        p_e += p1 * p2

    if p_e == 1:
        return 1.0 if p_o == 1 else 0.0  # 한 범주만 쓴 경우
    return (p_o - p_e) / (1 - p_e)
