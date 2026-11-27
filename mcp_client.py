import asyncio
import threading

from mcp import Client


class MCPClient:
    """비동기 mcp.Client를 동기 호출처럼 쓰게 감싼다."""

    def __init__(self, url: str):
        self._loop = asyncio.new_event_loop()
        threading.Thread(target=self._loop.run_forever, daemon=True).start()
        self._client = Client(url)
        self._run(self._client.__aenter__())  # 서버에 연결하고 initialize 핸드셰이크를 한다

    @classmethod
    def connect(cls, url: str) -> "MCPClient":
        return cls(url)

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout=60)

    def list_tools(self):
        return self._run(self._client.list_tools()).tools

    def to_anthropic_tool(self, tool) -> dict:
        return {
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": tool.input_schema,
        }

    def call_tool(self, name: str, arguments: dict):
        result = self._run(self._client.call_tool(name, arguments))
        return result.structured_content or [c.text for c in result.content]
