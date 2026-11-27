import json, hashlib, os

CACHE_DIR = "eval_tool_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def cached_tool_call(tool_name, tool_input, real_call):
    key = hashlib.sha256(
        json.dumps({"tool": tool_name, "input": tool_input}, sort_keys=True).encode()
    ).hexdigest()
    path = f"{CACHE_DIR}/{key}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    result = real_call(tool_name, tool_input)
    with open(path, "w") as f:
        json.dump(result, f)
    return result
