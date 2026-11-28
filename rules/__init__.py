from dataclasses import dataclass

@dataclass
class Rule:
    id: int
    name: str
    statement: str
    checks: list[str]          # 패턴 1: 검증 가능한 형태
    rationale: str
    do: list[str]
    dont: list[str]
    overrides: list[int]       # 패턴 2: 충돌 시 이 룰이 이기는 룰 번호
    check_methods: list[str]   # 패턴 4: CI·pre-commit 등 검증 방법
    bad_example: str
    good_example: str

    def render(self) -> str:
        # 위 6가지 패턴 형식으로 자동 렌더링
        ...
