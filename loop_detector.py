import json

from trajectory import Trajectory


def detect_loop(trajectory: Trajectory, threshold: int = 5) -> bool:
    counts = {}
    for step in trajectory.steps:
        if step["kind"] != "tool_call":
            continue
        key = f"{step['content']['name']}:{json.dumps(step['content']['input'], sort_keys=True)}"
        counts[key] = counts.get(key, 0) + 1
        if counts[key] >= threshold:
            return True
    return False
