from dataclasses import dataclass

@dataclass
class PRMetadata:
    repo: str
    pr_number: int
    title: str
    description: str
    author: str
    base_branch: str
    files_changed: list[str]


@dataclass
class PRDiff:
    files: dict[str, str]   # 파일명 → 디프 텍스트
    raw_text: str           # 디프 전체 텍스트


@dataclass
class ReviewInput:
    metadata: PRMetadata
    diff: PRDiff


@dataclass
class ReviewComment:
    file: str             # 어느 파일에 대한 의견인가
    line_start: int       # 코멘트가 가리키는 라인 시작
    line_end: int
    rule_id: int          # 어느 골든 룰 위반인가 (1~6)
    severity: str         # "blocker", "warning", "suggestion"
    message: str          # 자연어 의견
    suggested_code: str | None = None  # 수정 제안 코드 (선택)


@dataclass
class ReviewDraft:
    """모델이 채우는 부분. elapsed_ms와 cost_usd는 모델이 알 수 없으므로 여기에 넣지 않는다."""
    summary: str
    comments: list[ReviewComment]  # 최대 5개


@dataclass
class ReviewOutput:
    summary: str
    comments: list[ReviewComment]  # 최대 5개
    elapsed_ms: int  # 실행이 끝난 뒤 하네스가 채운다
    cost_usd: float  # 실행이 끝난 뒤 하네스가 채운다
