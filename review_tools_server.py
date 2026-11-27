from wiki_mcp import mcp  # PART 04 Ch 02의 서버. search_wiki가 이미 등록되어 있다

# 가짜 데이터. 실제 서비스에서는 GitHub API 같은 저장소 호출로 바꾼다
PR_DIFFS = {
    "https://github.com/company/payment-api/pull/4521": (
        '+    @PostMapping("/register")\n'
        "+    public User register(@RequestBody Map<String, String> body) {\n"
        '+        String pwd = body.get("password");\n'
        '+        return userRepo.save(new User(body.get("email"), pwd));\n'
        "+    }"
    ),
}
COVERAGE = {"UserController.java": 0.42}


@mcp.tool()
def fetch_pr_diff(pr_url: str) -> str:
    """PR 디프를 가져온다. 이미 받았다면 캐시된 것을 돌려준다."""
    return PR_DIFFS.get(pr_url, "(해당 PR 디프를 찾을 수 없다)")


@mcp.tool()
def read_file_at_revision(repo: str, sha: str, path: str) -> str:
    """특정 시점(sha)의 파일 전체를 읽는다."""
    return f"// {repo}@{sha[:7]} {path}\n(가짜 구현: 실제로는 저장소에서 파일을 읽는다)"


@mcp.tool()
def check_test_coverage(file: str) -> dict:
    """변경된 파일의 테스트 커버리지를 조회한다."""
    return {"file": file, "coverage": COVERAGE.get(file, 0.0)}


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8765, stateless_http=True, json_response=True)
