
## /test
이 저장소의 테스트를 다음 절차로 실행한다.

1. `pnpm typecheck` 실행. 실패 시 즉시 중단하고 오류 보고.
2. `pnpm lint` 실행. 경고는 무시 가능, 오류는 중단.
3. `pnpm test --run` 실행. 실패한 테스트의 이름과 메시지를 정리.
4. 모두 통과하면 한 줄로 "all checks passed" 출력.

ARGUMENTS: $ARGUMENTS (선택적 테스트 패턴)
