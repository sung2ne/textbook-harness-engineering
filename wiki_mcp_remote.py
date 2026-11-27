from mcp.server import MCPServer

mcp = MCPServer("company-wiki")

# (도구 정의는 wiki_mcp.py와 동일)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8765, stateless_http=True, json_response=True)
