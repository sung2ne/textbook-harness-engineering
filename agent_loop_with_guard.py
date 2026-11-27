import uuid

from loop_detector import detect_loop
from trajectory import Trajectory

MAX_TOOL_CALLS = 30
DUPLICATE_THRESHOLD = 5

def run_with_guard(user_input: str) -> str:
    trajectory = Trajectory(case_id=uuid.uuid4().hex, user_input=user_input)

    while True:
        if sum(1 for s in trajectory.steps if s["kind"] == "tool_call") > MAX_TOOL_CALLS:
            raise RuntimeError("max_tool_calls_exceeded")
        if detect_loop(trajectory, threshold=DUPLICATE_THRESHOLD):
            raise RuntimeError("infinite_loop_detected")

        # ... 모델 호출 및 도구 실행
