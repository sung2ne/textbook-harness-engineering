from prompts.refusal import REFUSAL_TEMPLATE
from prompts.escalation import ESCALATION_TEMPLATE
from prompts.fallback import FALLBACK_TEMPLATE
from prompts.combined import RULE_4_FULL
from prompts.do_dont import DO_DONT
from prompts.example_pairs import EXAMPLE_PAIRS

ROLE = "너는 한국어 코드 리뷰어다."
CONTEXT = "이 저장소는 Spring Boot 3.5 + Java 21 백엔드 API다."
GOLDEN_RULES = RULE_4_FULL + "\n" + DO_DONT
EXAMPLES = EXAMPLE_PAIRS

SYSTEM_PROMPT = f"""\
## 역할
{ROLE}

## 맥락
{CONTEXT}

## 제약
{GOLDEN_RULES}

{REFUSAL_TEMPLATE}

{ESCALATION_TEMPLATE}

{FALLBACK_TEMPLATE}

## 예시
{EXAMPLES}
"""
