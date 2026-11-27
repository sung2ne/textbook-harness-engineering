from dataclasses import dataclass, field

@dataclass
class Trajectory:
    case_id: str
    user_input: str
    steps: list[dict] = field(default_factory=list)  # 각 모델 호출과 도구 호출
    final_output: str = ""
    cost_usd: float = 0.0
    latency_seconds: float = 0.0
    env: dict = field(default_factory=dict)  # 모델·SDK 버전

    def add_step(self, kind: str, content: dict):
        self.steps.append({"kind": kind, "content": content})
