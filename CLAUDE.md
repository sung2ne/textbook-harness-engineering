
## 이 프로젝트에 대해
이 저장소는 Next.js 15 App Router 기반의 학생 대시보드입니다. 주 사용자는 대학생이고, 모바일 비중이 70%입니다. 따라서 모든 UI는 *모바일 우선*으로 설계합니다.

## 기술 스택
- Next.js 15 (App Router, React Server Components)
- React 19, TypeScript 5.8 strict mode
- TailwindCSS 4.x, shadcn/ui
- Prisma 6.x, PostgreSQL 16
- 인증: NextAuth.js v5

## 디렉토리 컨벤션
- `app/` — App Router 페이지와 API 라우트
- `components/ui/` — shadcn/ui 베이스 컴포넌트
- `components/feature/` — 기능별 컴포넌트
- `lib/` — 클라이언트·서버 공용 유틸
- `prisma/` — 스키마와 마이그레이션

## 작성 스타일
- *기본은 서버 컴포넌트*. `"use client"`는 진짜 필요할 때만.
- 데이터 조회는 서버 컴포넌트나 Route Handler에서. 클라이언트에서 직접 fetch 금지.
- 폼은 React Hook Form + Zod 조합 권장.
- 색상은 Tailwind 토큰만. 인라인 hex 금지.

## 검증
- 변경 후 `pnpm typecheck`와 `pnpm lint` 모두 통과해야 함.
- E2E는 Playwright. 새 페이지 추가 시 happy path 테스트 1개 필수.

## 절대 금지
- `dangerouslySetInnerHTML` 신규 사용 금지.
- API 라우트에서 인증 체크 누락 금지.
- 마이그레이션 없이 Prisma 스키마 수정 금지.
