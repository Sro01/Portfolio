# 이력서·포트폴리오 작업 공간

개인 이력과 프로젝트 근거를 보관하고, 이력서·포트폴리오 작성 기준을 관리합니다.

## 구조

```text
.claude/skills/       스킬 원본
.agents/skills       ../.claude/skills를 가리키는 디렉터리 링크
docs/                프로젝트 규칙
archive/             개인 기록·조사 근거·과거 스펙 (Git 제외)
.gitignore
README.md
AGENTS.md            CLAUDE.md 안내
CLAUDE.md            에이전트 지침 원본
```

## 작업 기준

- [프로젝트 에이전트 지침](CLAUDE.md)
- [커밋 규칙](docs/commit-conventions.md)
- [이력서·포트폴리오 공통 기준](.claude/skills/writing-common/SKILL.md)
- [이력서 작성·검토](.claude/skills/writing-resume/SKILL.md)
- [포트폴리오 작성·검토](.claude/skills/writing-portfolio/SKILL.md)

## 개인 기록

`archive/`는 로컬에서만 보관합니다. 새 체크아웃에는 포함되지 않습니다. 자료가 있는 환경에서는 `archive/README.md`로 원본, 선별한 정리 노트, 조사 보고서와 근거를 찾을 수 있습니다.

과거 스펙은 `archive/planning/specs/`에 보관합니다. 스펙을 프로젝트 규칙으로 정제하는 작업은 별도로 진행합니다.
