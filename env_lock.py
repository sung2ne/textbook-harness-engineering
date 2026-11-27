import sys
from importlib.metadata import version

env = {
    "anthropic_sdk": version("anthropic"),
    "openai_sdk": version("openai"),
    "mcp_sdk": version("mcp"),
    "python": sys.version,
}
print(env)
