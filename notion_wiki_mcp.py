import os
from mcp.server import MCPServer
from notion_client import Client

mcp = MCPServer("notion-wiki")
notion = Client(auth=os.environ["NOTION_API_KEY"])


@mcp.tool()
def search_wiki(query: str) -> list[dict]:
    """사내 Notion 위키에서 페이지를 검색한다."""
    res = notion.search(query=query, filter={"property": "object", "value": "page"})
    return [
        {
            "id": r["id"],
            "title": next((p["title"][0]["plain_text"] for p in r["properties"].values() if p["type"] == "title" and p["title"]), ""),
            "url": r["url"],
        }
        for r in res["results"][:5]
    ]


if __name__ == "__main__":
    mcp.run()
