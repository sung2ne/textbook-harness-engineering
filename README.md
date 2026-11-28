# 깊이 파는 하네스 엔지니어링 실습 코드

교재: https://text.ibetter.kr/harness-engineering

이 저장소는 교재 본문의 코드 블록을 책 순서대로 모은 것입니다. 본문이 기준이고, 이 저장소가 본문과 다르면 본문을 따릅니다. 본문을 고치면 이 저장소를 다시 만듭니다.

## 브랜치

`part{PART 번호}/chapter-{장 번호}` 브랜치는 그 장까지의 코드가 누적된 상태입니다. 예를 들어 `part08/chapter-02`는 PART 08 Ch 02를 끝낸 시점의 파일 전체입니다. 코드 블록이 없는 장에는 브랜치가 없습니다. `main`은 책 끝 시점의 전체 파일입니다.

```bash
git clone https://github.com/sung2ne/textbook-harness-engineering.git
cd textbook-harness-engineering
git checkout part08/chapter-02
```

## 만든 규칙

- 첫 줄이 `# 파일: 이름`인 코드 블록만 파일이 됩니다. 그 첫 줄은 파일에 넣지 않습니다.
- 같은 장 안에서 같은 이름의 블록이 또 나오면 앞 블록 뒤에 이어 붙입니다. 다른 장에서 같은 이름이 나오면 새 내용으로 바꿉니다.
- 파일 이름이 같아도 PART 02의 첫 하네스 예제와 PART 08의 실전 프로젝트는 서로 다른 코드입니다. 뒤 장이 앞 장의 파일을 바꿉니다.
- `bad_`로 시작하는 파일은 안티패턴을 보여 주려는 나쁜 예입니다. 일부는 일부러 비워 둔 자리(`...`)가 있어 실행되지 않습니다.
- 모델 호출 코드는 환경 변수 `ANTHROPIC_API_KEY`·`OPENAI_API_KEY`로 키를 읽습니다. 키는 파일에 적지 않습니다.
- 설치할 패키지와 판 번호, 실행 순서는 본문 PART 08에 적힌 대로 따릅니다.
