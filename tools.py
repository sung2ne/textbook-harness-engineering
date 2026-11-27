get_weather_tool = {
    "name": "get_weather",
    "description": "특정 도시의 현재 날씨를 조회한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "도시명. 예: 'Seoul', 'Tokyo'."
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "온도 단위. 기본 'celsius'."
            }
        },
        "required": ["city"]
    }
}
