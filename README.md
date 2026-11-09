# 이력서·포트폴리오

포트폴리오·이력서 사이트(ko·en·ja·de)와 그 작성 기준을 관리합니다. 개인 이력의 원본과 조사 근거는 로컬 `archive/`에만 둡니다.

## 저장소 구조

```text
.
├── src/                          사이트 코드 (아래 사이트 구조)
├── messages/                     UI 문구
│   ├── ko.json                   기준 언어
│   ├── en.json
│   ├── ja.json
│   └── de.json
├── public/                       이미지 등 정적 파일
├── docs/                         프로젝트 규칙
│   ├── commit-conventions.md
│   └── frontend-conventions.md
├── .claude/
│   └── skills/                   작성·개발 스킬 원본 (.agents/skills는 이 폴더의 링크)
├── archive/                      이력 원본·조사 근거 (Git 제외, 로컬 전용)
├── CLAUDE.md                     에이전트 지침 원본 (AGENTS.md가 안내)
└── README.md
```

루트의 나머지 파일은 패키지·빌드·검사 도구 설정입니다.

## 사이트 구조

Next.js 16(App Router), TypeScript, Tailwind CSS v4, shadcn/ui, next-intl, motion, MDX를 사용합니다.

```text
src/
├── app/
│   ├── [locale]/
│   │   ├── layout.tsx            html lang·폰트·헤더/푸터
│   │   ├── page.tsx              홈: 섹션 조합
│   │   ├── projects/
│   │   │   └── [slug]/
│   │   │       └── page.tsx      프로젝트 상세(사례)
│   │   └── resume/
│   │       └── page.tsx          이력서 (인쇄 스타일로 PDF 저장)
│   ├── favicon.ico
│   └── globals.css               디자인 토큰
├── features/                     화면 단위 섹션
│   ├── hero/                     이름·직무·한 줄 소개
│   ├── projects/                 프로젝트 목록·카드·사례 본문
│   ├── experience/               경력
│   ├── skills/                   기술
│   ├── contact/                  이메일·외부 링크
│   └── resume/                   이력서 레이아웃·인쇄 스타일
├── components/
│   ├── ui/                       shadcn 컴포넌트
│   └── site/                     헤더·푸터·언어 전환
├── content/                      공개용으로 정제한 데이터
│   ├── projects/
│   │   └── <slug>/
│   │       ├── meta.ts           기간·역할·기술·링크
│   │       ├── ko.mdx            사례 본문 (언어별)
│   │       ├── en.mdx
│   │       ├── ja.mdx
│   │       └── de.mdx
│   ├── profile.ts                이름·직무·이메일·링크
│   ├── experience.ts             경력 (홈·이력서 공용)
│   ├── skills.ts                 기술 (홈·이력서 공용)
│   ├── education.ts              학력 (이력서)
│   ├── credentials.ts            자격·수상·교육 (이력서)
│   └── types.ts                  콘텐츠 스키마
├── i18n/
│   ├── routing.ts                지원 언어·기본 언어
│   ├── request.ts                요청별 언어·메시지 로딩
│   ├── navigation.ts             언어 접두사를 유지하는 Link·redirect
│   ├── app-config.d.ts           메시지 키·언어 타입
│   └── messages.test.ts          언어별 메시지 키 누락 검사
├── lib/
│   ├── content.ts                언어별 콘텐츠 조회
│   └── utils.ts                  cn()
├── mdx-components.tsx            MDX 공통 요소
└── proxy.ts                      언어 감지·리다이렉트
```

데이터는 `content/ → lib/content.ts → app/ 페이지 → features/ 섹션(props) → components/` 한 방향으로 흐릅니다. 아직 없는 경로는 해당 기능을 구현할 때 만듭니다.

## 작업 기준

- [프로젝트 에이전트 지침](CLAUDE.md)
- [커밋 규칙](docs/commit-conventions.md)
- [프론트엔드 규칙](docs/frontend-conventions.md)
- [이력서·포트폴리오 공통 기준](.claude/skills/writing-common/SKILL.md)
- [이력서 작성·검토](.claude/skills/writing-resume/SKILL.md)
- [포트폴리오 작성·검토](.claude/skills/writing-portfolio/SKILL.md)

## 개인 기록

`archive/`는 로컬에서만 보관합니다. 새 체크아웃에는 포함되지 않습니다. 자료가 있는 환경에서는 `archive/README.md`로 원본, 선별한 정리 노트, 조사 보고서와 근거를 찾을 수 있습니다.

과거 스펙은 `archive/planning/specs/`에 보관합니다. 스펙을 프로젝트 규칙으로 정제하는 작업은 별도로 진행합니다.
