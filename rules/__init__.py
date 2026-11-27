from dataclasses import dataclass

@dataclass
class Rule:
    id: int
    name: str
    statement: str
    rationale: str
    do: list[str]
    dont: list[str]
    auto_check: bool
    bad_example: str
    good_example: str

    def render(self) -> str:
        # 위 6가지 패턴 형식으로 자동 렌더링
        ...
