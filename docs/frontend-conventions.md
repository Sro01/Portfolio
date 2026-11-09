# 프론트엔드 규칙

이 규칙은 포트폴리오 사이트 코드(`src/`)와 그 설정 파일에 적용합니다. 스택은 Next.js App Router, TypeScript strict, Tailwind CSS v4, shadcn/ui, next-intl, motion, MDX, Vitest, Prettier입니다. 저장소와 사이트의 전체 구조는 [README](../README.md)에 있습니다.

Next.js 16 API는 학습 데이터와 다를 수 있습니다. Next.js 코드를 작성하기 전에 `node_modules/next/dist/docs/`의 해당 문서를 확인합니다. `next.config.ts`의 `agentRules: false`는 `next dev`가 `AGENTS.md`에 같은 안내를 자동으로 추가하지 않게 막는 설정입니다.

패키지 매니저는 pnpm만 사용합니다(`package.json`의 `packageManager`).

ESLint·TypeScript로 강제할 수 있는 규칙은 이 문서가 아니라 설정 파일에 둡니다. 이 문서에는 도구가 판단할 수 없는 기준만 적습니다. `eslint.config.mjs`가 막는 것은 계층 간 역방향·기능 간 import, `components/ui/` 밖의 프리미티브 직접 import, `features/`·`components/`의 `content/` 직접 import, 기본 팔레트 색상·임의값·`space-*` 클래스, JSX 문자열입니다. 위반 메시지에 대안이 적혀 있습니다.

## 구조와 의존 방향

```text
src/
  app/[locale]/     페이지 진입점(홈·프로젝트 상세·이력서). 데이터를 조회해 섹션에 넘기기만 한다
  features/<기능>/   화면 단위 섹션과 그 기능에서만 쓰는 컴포넌트·훅
  components/ui/    shadcn이 생성한 범용 UI
  components/site/  헤더·푸터·언어 전환 등 여러 화면 공통 컴포넌트
  content/          공개용으로 정제한 콘텐츠 데이터와 스키마(types.ts)
  lib/              순수 함수, 외부 라이브러리 래퍼, 콘텐츠 조회(content.ts), cn()
  i18n/             언어 목록·요청 설정·언어 접두사를 유지하는 navigation
  mdx-components.tsx  MDX 공통 요소·스타일 (App Router에서 @next/mdx 필수 파일)
  proxy.ts          언어 감지·리다이렉트 (Next 16의 middleware)
messages/           UI 문구 (ko.json 기준, en·ja·de)
```

- 계층은 `app → features → components → lib` 순서입니다. 다른 기능의 코드가 필요하면 `components/`나 `lib/`로 옮깁니다.
- 한 기능에서만 쓰는 파일은 그 기능 폴더에 둡니다. 두 번째 기능에서 필요해질 때 공통 위치로 옮깁니다.
- 배럴 `index.ts`는 만들지 않습니다.
- 프리미티브 외의 외부 라이브러리는 `lib/`에 래퍼를 두고 사용합니다.
- `lib/`는 역할별 파일(`lib/date.ts`, `lib/slug.ts`)로 나눕니다. `lib/utils.ts`에는 shadcn의 `cn()`만 둡니다.
- 훅은 쓰는 기능 폴더에 두고, 두 기능 이상에서 쓰일 때 `src/hooks/`로 옮깁니다(shadcn CLI가 만드는 위치와 같습니다). 타입은 데이터·컴포넌트 옆에 두고 `src/types/`는 만들지 않습니다.

## 콘텐츠

- 콘텐츠는 `src/content/`에 두고 스키마는 `content/types.ts`에 정의합니다. 페이지가 `lib/content.ts`로 조회해 섹션에 props로 넘깁니다.
- 언어별로 다른 짧은 필드(제목·요약·역할)는 `Record<Locale, string>` 타입으로 네 언어를 함께 둡니다. 번역 누락은 타입 검사에서 실패합니다.
- 프로젝트 사례 본문은 `content/projects/<slug>/<언어>.mdx`에 쓰고 페이지에서 동적 import로 불러옵니다. MDX는 페이지 라우트로 쓰지 않으므로 `pageExtensions`는 바꾸지 않습니다. 기간·기술·링크처럼 언어와 무관한 값은 같은 폴더의 `meta.ts`에 둡니다. 증거(도식·표·코드)는 주장 곁에 배치합니다.
- 경력·기술 데이터는 홈과 이력서가 함께 씁니다. 같은 사실을 두 곳에 따로 적지 않고, 문서별로 표현이 달라야 하면 같은 항목 안에 필드를 나눕니다.
- 사이트에 공개하는 연락처는 이메일과 외부 링크(GitHub 등)뿐입니다. 전화번호와 주소는 넣지 않습니다.
- 이력서 페이지는 인쇄 스타일(`@media print`)로 브라우저의 PDF 저장을 지원합니다. 별도 PDF 파일을 따로 관리하지 않습니다.
- 콘텐츠의 사실·근거 기준은 [writing-portfolio](../.claude/skills/writing-portfolio/SKILL.md)를 따릅니다. 코드 작업 중 내용을 추정해 채우지 않습니다.

## 다국어

- 지원 언어는 ko(기준)·en·ja·de이고, 모든 URL에 언어 접두사(`/ko/...`)를 붙입니다.
- 화면에 보이는 문구는 `messages/<언어>.json`에 두고 `useTranslations`·`getTranslations`로 불러옵니다. `alt`, `aria-label` 같은 속성 문구는 ESLint가 검사하지 않지만 마찬가지로 메시지로 둡니다.
- 공개 전에는 네 언어가 모두 있어야 합니다. 누락은 `Record<Locale, string>` 타입 검사와 `src/i18n/messages.test.ts`가 잡습니다.
- 문구·콘텐츠는 한국어부터 작성합니다. 한국어 결과를 `pnpm dev`의 `/ko` 화면으로 보여 주고 사용자 승인을 받은 뒤, en·ja·de 작성은 별도 작업으로 진행합니다. 승인 전에 다른 언어를 미리 쓰지 않습니다.
- 한국어만 작성한 단계에서는 번역 누락 때문에 `pnpm check`가 실패하는 것이 정상입니다. 이때는 `pnpm lint`와 `/ko` 화면으로 확인하고, 실패 항목이 번역 누락뿐인지 보고합니다. 커밋은 네 언어 작성과 `pnpm check` 통과 후에 합니다. 사용자가 한국어 단계의 커밋을 따로 요청하면 그 요청을 따릅니다.
- 내부 링크와 이동은 `next/link`가 아니라 `@/i18n/navigation`의 `Link`·`redirect`·`useRouter`를 씁니다.
- `[locale]` 아래 페이지와 레이아웃은 정적 렌더링을 위해 `setRequestLocale(locale)`을 호출합니다.
- 번역은 원문 의미를 유지합니다. 번역하면서 사실·수치를 보태거나 바꾸지 않습니다.
- 이력서 페이지는 네 언어 모두 같은 구조로 제공하고, 날짜 형식(next-intl의 날짜 포맷)과 섹션 이름만 언어에 맞춥니다. 일본·독일 기업 제출용 양식(履歴書, Lebenslauf)은 사이트 범위가 아닙니다.

## 컴포넌트

- `components/`의 UI 컴포넌트는 props만으로 렌더링되어야 합니다. 상태, 데이터 접근, 브라우저 API는 커스텀 훅이나 `lib/` 함수로 분리합니다.
- 기능 컴포넌트는 UI 조합과 콘텐츠 연결을 맡고, 계산 로직은 `lib/`의 순수 함수로 뺍니다.
- 새 UI를 작성하기 전에 shadcn 컴포넌트로 구성할 수 있는지 확인합니다.
- `components/ui/`는 디자인 시스템 전체에 적용할 변경(variant 추가 등)일 때만 수정합니다. 프로젝트 전용 모양은 기능 컴포넌트에서 조합으로 만듭니다. shadcn 업데이트는 `add <component> --diff`로 비교한 뒤 병합합니다.
- 같은 코드가 세 번 반복될 때 추상화합니다. boolean prop이 늘어나면 `variant` 하나나 `children` 조합으로 바꿉니다.
- 서버 컴포넌트를 기본으로 합니다. `"use client"`는 상호작용이 필요한 가장 작은 컴포넌트에만 붙입니다.
- 자바스크립트 애니메이션 라이브러리는 motion(`motion/react`)만 사용합니다. framer-motion·GSAP 등은 추가하지 않습니다. CSS 전환과 motion 중 무엇을 쓸지는 motion 스킬의 `best-practices/css-or-motion.md` 기준을 따릅니다. shadcn 컴포넌트의 CSS 애니메이션(`tw-animate-css`)은 그대로 둡니다.
- motion 컴포넌트는 클라이언트 컴포넌트이므로 애니메이션이 필요한 부분만 작은 컴포넌트로 분리합니다. 사용자의 동작 줄이기 설정(`prefers-reduced-motion`)을 존중합니다.

## 상태

- 계산할 수 있는 값은 state로 두지 않습니다.
- state는 그 값을 쓰는 가장 가까운 컴포넌트에 둡니다. 필터·탭처럼 공유하거나 뒤로가기로 돌아올 수 있어야 하는 상태는 URL 쿼리에 둡니다.
- 테마처럼 앱 전체에 필요한 값은 Context 하나로 처리합니다. 전역 상태 라이브러리는 사용자 확인 없이 도입하지 않습니다.

## 과설계 금지

- `domain/`, `usecase/`, `repository/` 같은 계층을 만들지 않습니다.
- 구현체가 하나뿐인 인터페이스나, 아직 없는 요구를 위한 추상화를 만들지 않습니다.

## 스타일과 토큰

- 토큰 원본은 `src/app/globals.css` 하나입니다. 토큰 값을 문서나 컴포넌트에 옮겨 적지 않습니다.
- 색상은 의미 기반 토큰(`bg-background`, `text-muted-foreground`)을 씁니다. 토큰에 없는 값이 필요하면 `@theme`에 토큰으로 등록합니다.
- 다크 모드는 토큰으로 처리하고 `dark:` 클래스로 색을 덮어쓰지 않습니다.
- 모양은 컴포넌트 variant를 먼저 사용합니다. `className`은 배치(margin, flex, grid)에만 씁니다.
- 반복되는 클래스 묶음은 `@apply` 대신 컴포넌트나 `cva` variant로 추출합니다.
- 테마는 tweakcn의 Sage Green이고, 값과 사용 기준은 루트 `DESIGN.md`에 있습니다. 폰트는 라틴 문자 Plus Jakarta Sans(본문·UI), Lora(세리프), IBM Plex Mono(코드), 한글 Pretendard, 일본어 Pretendard JP입니다. `globals.css`의 `--font-cjk`와 `[locale]/layout.tsx`의 폰트 로딩이 이를 맡습니다.
- 테마(tweakcn 등)를 교체할 때는 `globals.css`의 변수만 바뀌는지 확인합니다. `--spacing`, 글꼴 변수가 바뀌면 전체 간격과 폰트 로딩에 영향이 있으므로 적용 전에 사용자에게 알립니다. 교체 후 `--font-sans`·`--font-serif`가 `var(--font-<라틴 글꼴>), var(--font-cjk), ...` 형태를 유지하는지 확인합니다. tweakcn 명령은 글꼴 변수를 글꼴 이름 문자열로 덮어쓰므로 교체 후 다시 맞춥니다.

## 검증과 변경

- 작업을 마치기 전에 `pnpm check`(타입 검사, ESLint, Prettier, Vitest)를 실행하고 결과를 보고합니다. 포맷 오류는 `pnpm format`으로 고칩니다.
- 테스트는 대상 옆에 `*.test.ts(x)`로 둡니다. `lib/` 순수 함수의 단위 테스트와 주요 페이지 렌더링 스모크 테스트까지만 작성합니다.
- 화면을 바꾼 작업은 접근성(키보드 조작, 대체 텍스트, 대비)과 Lighthouse 성능 점수가 나빠지지 않았는지 확인합니다.
- 같은 위반이 반복되면 이 문서에 문장을 추가하기보다 ESLint 규칙으로 옮길 수 있는지 먼저 검토합니다.
- 규칙 변경은 이 파일에 반영합니다.
