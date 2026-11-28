
## 프로젝트
사내 ML 데이터 파이프라인. 매일 자정에 BigQuery에서 데이터를 긁어와 가공한 뒤
ML 학습용 Parquet으로 떨어뜨림.

## 스택
- Python 3.12, uv (패키지 매니저), Ruff (lint+format)
- FastAPI 0.129 (모니터링 API용), Pandas 2.x, PyArrow
- BigQuery 클라이언트, GCS 클라이언트
- Airflow 2.10 (스케줄링)

## 구조
- `pipelines/` — 파이프라인 정의 (Airflow DAG)
- `transforms/` — 데이터 변환 함수 (순수 함수 권장)
- `io/` — BigQuery·GCS 입출력
- `tests/` — pytest 기반 테스트

## 스타일
- 모든 함수는 *타입 힌트 필수*.
- 데이터프레임을 인자로 받는 함수는 *원본 변경 금지*. 항상 새 객체 반환.
- 1만 행 이상을 처리하는 코드는 *반드시* 처리량 측정 주석 추가.

## 테스트
- 변경 시 `pytest -q` 통과.
- 데이터 변환 함수는 *작은 가짜 데이터프레임으로 단위 테스트* 필수.

## 절대 금지 (데이터 보안)
- 운영 BigQuery에 직접 쓰기 금지. 무조건 staging 거쳐야 함.
- 개인정보(PII) 컬럼을 평문 로그에 남기기 금지.
- `.env`, 서비스 계정 JSON을 커밋 금지.
- ML 학습 데이터를 회사 외부 저장소에 업로드 금지.
- Pandas의 `eval()`, `query()`에 외부 입력을 직접 넘기기 금지 (SQL injection과 유사한 위험).
