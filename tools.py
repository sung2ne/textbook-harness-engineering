def get_weather(city: str, unit: str = "celsius") -> dict:
    """날씨 조회의 가짜 구현. 실제로는 외부 API 호출."""
    fake_data = {
        "Seoul": {"temp": 18, "condition": "흐림"},
        "Tokyo": {"temp": 22, "condition": "맑음"},
        "New York": {"temp": 12, "condition": "비"},
    }
    data = fake_data.get(city, {"temp": 20, "condition": "알 수 없음"})
    temp = data["temp"]
    if unit == "fahrenheit":
        temp = temp * 9 / 5 + 32
    return {"city": city, "temperature": temp, "unit": unit, "condition": data["condition"]}


# Anthropic SDK 형식 도구 정의
ANTHROPIC_TOOL = {
    "name": "get_weather",
    "description": (
        "특정 도시의 현재 날씨를 조회한다. "
        "사용자가 날씨, 기온, 강수, 바람을 물을 때 사용한다. "
        "한 번에 한 도시만 조회 가능."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "도시명(영어). 예: 'Seoul', 'Tokyo'."},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["city"],
    },
}

# OpenAI SDK(Responses API) 형식 도구 정의
OPENAI_TOOL = {
    "type": "function",
    "name": "get_weather",
    "description": (
        "특정 도시의 현재 날씨를 조회한다. "
        "사용자가 날씨, 기온, 강수, 바람을 물을 때 사용한다. "
        "한 번에 한 도시만 조회 가능."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "도시명(영어). 예: 'Seoul', 'Tokyo'."},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["city"],
    },
    "strict": False,  # unit이 선택 인자라 엄격 모드를 쓰지 않는다
}
