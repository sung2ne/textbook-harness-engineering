import json

EXTRACTOR_PROMPT = """\
다음 대화에서 *사용자에 대한 영구적 사실*을 추출하라.
영구적 사실이란: 선호, 신원, 직업, 알레르기, 기술 스택 같은 변화가 적은 정보.
일시적 사실(오늘 일정, 이번 달 기분)은 추출하지 말 것.

대화:
{conversation}

JSON 배열로만 답하라. 예: ["사용자는 Python 5년차", "TypeScript 선호"]
"""

def extract_facts(conversation: list[dict]) -> list[str]:
    response = call_model(EXTRACTOR_PROMPT.format(conversation=conversation)).strip()
    if response.startswith("```"):  # 모델이 json 코드 펜스로 감싸 답하는 경우가 있습니다
        response = response.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(response)
