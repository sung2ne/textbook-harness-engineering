import os
import json
from openai import OpenAI
from tools import get_weather, OPENAI_TOOL

MODEL = os.environ.get("OPENAI_MODEL", "gpt-6.1-sol")  # 환경 변수로 모델을 바꾼다
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def run(user_message: str) -> str:
    input_items = [{"role": "user", "content": user_message}]

    while True:
        response = client.responses.create(
            model=MODEL,
            tools=[OPENAI_TOOL],
            input=input_items,
        )

        input_items += response.output

        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            return response.output_text

        for call in calls:
            tool_result = get_weather(**json.loads(call.arguments))
            input_items.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(tool_result),
            })


if __name__ == "__main__":
    print(run("서울과 도쿄 중 어디가 더 따뜻해?"))
