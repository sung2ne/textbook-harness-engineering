import json
from agents import RunHooks


class LoopGuard(RunHooks):
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.history = {}

    async def on_tool_start(self, context, agent, tool):
        # 도구가 호출되기 직전에 불린다. context에 도구 이름과 인자(JSON 문자열)가 들어 있다
        arguments = json.loads(context.tool_arguments or "{}")
        key = f"{context.tool_name}:{json.dumps(arguments, sort_keys=True)}"
        self.history[key] = self.history.get(key, 0) + 1
        if self.history[key] >= self.threshold:
            raise RuntimeError(f"infinite_loop:{context.tool_name}")
