import os


def review(input):
    if input.complexity_score < 0.3:
        return call_with_model(input, os.environ["MODEL_SIMPLE"])  # 단순 케이스: 저렴
    elif input.complexity_score < 0.7:
        return call_with_model(input, os.environ["MODEL_MEDIUM"])  # 보통: 중간
    else:
        return call_with_model(input, os.environ["MODEL_COMPLEX"])  # 복잡: 고가
