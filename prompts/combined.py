RULE_4_FULL = """\
## 룰 4: 시크릿은 코드, 로그, 설정 파일에 들어가지 않는다.

### 근거 (패턴 6)
한 번 커밋된 시크릿은 git history에 영구히 남는다.

### 검증 가능한 형태 (패턴 1)
- 코드에 다음 패턴이 *있으면 위반*:
  - 'sk-' 또는 'sk_'로 시작하는 문자열 리터럴
  - 'password=' 뒤의 평문 문자열
  - 'AKIA' 뒤에 영문 대문자·숫자 16자가 붙은 20자 문자열 (AWS 액세스 키 ID)

### Do/Don't (패턴 3)
- Do: 환경 변수, secret manager, fixture
- Don't: 코드 리터럴, 평문 설정 파일, 평문 로그

### 충돌 (패턴 2)
- 룰 1(테스트 함께 변경)과 충돌 시 → 룰 4 우선

### 검증 자동화 (패턴 4)
- CI 단계에서 정규식 + truffleHog로 검사
- git pre-commit hook에서 1차 차단

### 예시 페어 (패턴 5)
나쁜 예: AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
좋은 예: 환경 변수에서 읽는다. 예: Java는 System.getenv("AWS_ACCESS_KEY_ID"), Python은 os.environ["AWS_ACCESS_KEY_ID"]
"""
