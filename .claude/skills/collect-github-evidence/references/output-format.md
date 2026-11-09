# 출력 형식

## 폴더

```text
archive/research/github/<YYYY-MM-DD>/<owner>-<name>/
├── collection.json   수집 메타데이터: 시각, 계정·이메일 판정, 집계, 한계
├── commits.json      본인 커밋 원장
├── commits.csv       commits.json의 훑어보기용 요약
├── prs.json          본인이 만들었거나 본인 커밋이 포함된 PR
└── report.md         기여 정리 (에이전트 작성)
```

## commits.json 항목

기존 묶음(`2026-11-05/commits.json`)의 `repository`, `sha`, `url`, `authored_at`, `title`을 그대로 쓰고 다음을 더한다.

| 필드 | 의미 |
|---|---|
| `delivery` | `pr` · `pr_merge_commit` · `direct_push` · `branch_only` |
| `prs` | 이 커밋을 포함하거나 병합한 PR 번호 |
| `role` | `author` 또는 `co_author` |
| `branches`, `on_default_branch` | 이 커밋을 포함한 브랜치 |
| `is_merge` | 병합 커밋 여부 |
| `files`, `additions`, `deletions` | `--numstat`을 썼을 때만 |

## report.md

```markdown
# <owner/name> GitHub 기여 기록

수집: <날짜 시각> · 계정: <login> · 기본 브랜치: <branch> · 비공개 여부: <예/아니요>

## 집계
| 항목 | 값 |
|---|---:|
| 본인 커밋 (전체 브랜치) | |
| PR 경유 / PR 병합 커밋 / 직접 push / 브랜치 전용 | |
| 본인 작성 PR / 본인 커밋이 포함된 PR | |
| 기간 (첫 커밋 ~ 마지막 커밋) | |
| 기존 묶음과의 차이 | |

## 기능 묶음
### <기능 이름>
- 무엇을 바꿨는지: <커밋·코드로 확인한 변경> [검증됨]
- 근거: <SHA 앞 7자리>, PR #<n>, <경로:줄>
- 다른 기여자와의 범위: <본인 / 동료 / 공동>
- 확인하지 못한 것: <효과·원인·운영 결과 등>

## 직접 push한 커밋
<SHA, 날짜, 제목, 리뷰 기록 없음>

## 확인 범위와 한계
- 확인한 것 / 확인하지 못한 것 / 사용자 확인이 필요한 것
```
