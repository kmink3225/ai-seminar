---
title: "새 스킬 추가하는 법 — convert-pdf 사례 매뉴얼"
subtitle: "ai-seminar 의 Harness 위에 새 슬래시 커맨드를 얹는 표준 절차 (의존성 자동 onboarding 포함)"
description: |
  1번 글이 qa 스킬이 어떻게 자라났는지의 회고 서사였다면, 이 글은 두 번째 스킬을
  실제로 추가하는 절차를 단계별 매뉴얼 형태로 정리한다. 사례는 convert-pdf —
  references/pdfs/ 의 PDF 를 marker 로 references/md/ 로 변환하는 슬래시 커맨드.
  이 스킬은 새 머신에서 처음 호출될 때 marker 의존성과 모델 가중치 안내까지
  자동으로 처리해 신규 팀원의 onboarding 비용을 0 에 가깝게 줄인다.
tags: [engineering, harness, skill-engineering, manual, convert-pdf, marker, onboarding]
author: Kwangmin Kim
date: 05/07/2026
---

# 새 스킬 추가하는 법 — convert-pdf 사례 매뉴얼

## 배경

1번 글 (`1-skill-based-prompt-example.md`) 은 ai-seminar 의 첫 스킬 `/qa` 가 어떻게 만들어졌는지를 단계 0 → 3 진화 서사로 보여줬다. 그 결과로 자리잡은 인프라가 있다.

| 층 | 자리잡은 파일 |
|----|------------|
| Harness 진입점 | `CLAUDE.md` / `GEMINI.md` / `.github/copilot-instructions.md` |
| Harness 라우터 | `GUIDE.md` |
| Harness 공통 규칙 | `guides/GUIDE_CORE.md` |
| 슬래시 커맨드 정의 | `.claude/commands/qa.md` / `.gemini/commands/qa.toml` / `.github/prompts/qa.prompt.md` |
| 스킬 본문 | `guides/qa.md` |

이 인프라가 잘 짜여 있을 때 두 번째·세 번째 스킬 추가는 작은 작업이다. 이 글은 그것을 매뉴얼 형식으로 정리한다.

## 사례 선정: convert-pdf

`references/pdfs/` 의 PDF 를 marker 로 `references/md/` 에 markdown 으로 변환하는 작업을 슬래시 커맨드로 만든다. 이미 `system-scripts/convert_pdfs.py` 스크립트는 있다 — 이걸 슬래시 커맨드로 묶고 `GUIDE_CORE.md §7` 의 배치 권고를 자동으로 강제하는 게 목표다.

왜 이 작업을 스킬화하나:

- github 엔 파일용량 제한이 있어 pdf 를 바로 올리는 것은 바람직하지 않다 (변환된 markdown 만 archive 에 남기는 흐름이 강제된다)
- 변환은 수 분 이상 걸리는 배치 작업 — 대화 도중 즉시 실행하면 흐름이 끊긴다
- 사용자가 매번 스크립트 경로를 기억하지 않아도 된다 (`/convert-pdf` 한 줄)
- `GUIDE_CORE.md §7` 의 권고 메시지가 자동으로 출력된다
- **새 머신 onboarding 자동화** — 새로 clone 한 팀원의 환경에 marker 가 없을 때 스킬이 자동으로 가상환경 점검 → 의존성 설치 → 모델 가중치 안내까지 처리하므로, 신규 팀원은 `/convert-pdf` 한 줄만 알면 된다

## 추가하는 파일 4 + 수정하는 파일 2

| # | 경로 | 신규/수정 | 역할 |
|---|------|---------|------|
| 1 | `guides/convert-pdf.md` | 신규 | 스킬 본문 (Step 1~6) |
| 2 | `.claude/commands/convert-pdf.md` | 신규 | Claude Code 슬래시 |
| 3 | `.gemini/commands/convert-pdf.toml` | 신규 | Gemini CLI 슬래시 |
| 4 | `.github/prompts/convert-pdf.prompt.md` | 신규 | Copilot prompt |
| 5 | `GUIDE.md` | 수정 | 라우팅 테이블에 `/convert-pdf` 행 추가 |
| 6 | `PARTICIPATION.md` | 수정 | Lv1 끝의 "marker 변환" 언급 갱신 |

## Step 1 — 스킬 본문: `guides/convert-pdf.md`

`guides/qa.md` 의 패턴을 그대로 따른다 (frontmatter `name`·`type`·`description` + Step + 금지).

```yaml
---
name: convert-pdf
type: skill
version: 1.1
description: references/pdfs/ 의 신규 PDF 를 marker 로 references/md/ 에 일괄 변환. 첫 실행 시 marker 의존성·모델 가중치 자동 설치.
---
```

본문은 6 단계로 구성한다.

| Step | 무엇을 |
|------|------|
| 1 | **환경 점검** — `marker_single --help` 확인. 미설치면 가상환경 검사 (1-A) → `pip install -e .` (1-B, 사용자 동의 후) → 재검증. 첫 변환 시 모델 가중치 (수백 MB) 다운로드 안내 (1-C) |
| 2 | 미변환 PDF 탐지 — `references/pdfs/` vs `references/md/` 비교 |
| 3 | 배치 권고 메시지 출력 (`GUIDE_CORE.md` §7) |
| 4 | 사용자 동의 확인 ("지금 변환" / "배치 무시" / "바로 돌려") |
| 5 | `python system-scripts/convert_pdfs.py` 실행 |
| 6 | 결과 보고 — `[done] total=N skipped=K failed=L` 한 줄 + 실패 파일 목록 |

### Step 1 의 설계 의도 — 새 머신 onboarding

새 팀원이 리포를 clone 한 직후의 상태를 가정해 보자.

- marker 가 시스템에 없다 (`pyproject.toml` 의 dependency 만 선언되어 있을 뿐)
- 모델 가중치도 없다 (첫 marker 호출 시 자동 다운로드)
- 가상환경을 활성화하지 않았을 수도 있다 (시스템 python 오염 위험)

이 세 상황을 사용자가 일일이 README 를 읽어가며 처리하라고 하면 onboarding 마찰이 크다. 그래서 Step 1 이 다음을 자동화한다.

| 상황 | 스킬 행동 |
|------|---------|
| 가상환경 미활성화 | README 안내 후 종료 (시스템 python 오염 방지) |
| 가상환경 OK + marker 미설치 | `pip install -e .` 권고 → 사용자 동의 시 실행 → 재검증 |
| marker 설치 OK | 모델 가중치 첫 다운로드 안내 후 Step 2 로 |

신규 팀원이 알아야 할 것은 단 한 줄: `/convert-pdf`.

## Step 2 — Claude Code 슬래시: `.claude/commands/convert-pdf.md`

`.claude/commands/qa.md` 의 패턴. frontmatter `description` + 실행 순서 (라우터 → CORE → 스킬 → 실행 → Self-Check).

```markdown
---
description: references/pdfs/ 의 PDF 를 references/md/ 로 marker 변환 (첫 실행 시 의존성 자동 설치)
---

프로젝트 하네싱 체인에 따라 작업한다.

## 실행 순서

1. `GUIDE.md` 를 Read 로 읽는다 (라우팅 테이블).
...
```

`$ARGUMENTS` 는 이 스킬에서 의미 없으므로 (변환은 인자 안 받음) 사용하지 않는다. 사용자가 `/convert-pdf` 만 호출하면 된다.

## Step 3 — Gemini CLI 슬래시: `.gemini/commands/convert-pdf.toml`

`.gemini/commands/qa.toml` 의 패턴. TOML 의 `description` + `prompt` 두 키만 있으면 된다.

```toml
description = "references/pdfs/ 의 PDF 를 references/md/ 로 marker 변환 (첫 실행 시 의존성 자동 설치)"

prompt = """
프로젝트 하네싱 체인에 따라 작업한다.
...
"""
```

`{{args}}` 는 인자가 없으므로 본문에 넣지 않는다.

## Step 4 — Copilot prompt: `.github/prompts/convert-pdf.prompt.md`

`.github/prompts/qa.prompt.md` 의 패턴. frontmatter `mode: agent` + `description`. 경로 참조는 `.github/prompts/` 기준 상대경로 (`../copilot-instructions.md`, `../../GUIDE.md`, `../../guides/...`).

## Step 5 — 라우팅 등록: `GUIDE.md` 수정

라우팅 테이블에 한 행 추가.

```diff
| 명령어 | 태스크 | 로드할 가이드 (CORE 제외) |
|--------|--------|--------------------------|
| `/qa [question]` | 질의응답 ... | `guides/qa.md` |
+| `/convert-pdf` | PDF → MD 변환 ... | `guides/convert-pdf.md` |
```

사용 예시 섹션과 "커맨드별 로드 비교" 섹션에도 한 줄씩 추가한다.

## Step 6 — `PARTICIPATION.md` 한 줄 갱신

§3.1 Lv1 끝 부분:

```diff
-추후 누군가 marker 변환을 돌리면 `references/md/` 에 자동 변환된 markdown 이 생성된다.
+추후 누군가 `/convert-pdf` 스킬을 호출하면 `references/md/` 에 자동 변환된 markdown 이 생성된다.
```

## 검증 — 스킬이 작동하는가

세 CLI 에서 차례로 호출해 본다.

- Claude Code: `/convert-pdf`
- Gemini CLI: `/convert-pdf`
- Copilot Chat / CLI: `/convert-pdf`

각 환경에서 다음을 확인한다.

1. 라우팅 (`GUIDE.md`) → 공통 규칙 (`GUIDE_CORE.md`) → 스킬 본문 (`convert-pdf.md`) 로드 체인이 작동하는가
2. **Step 1 환경 점검 — marker 미설치 머신에서 `pip install -e .` 권고 → 동의 → 설치 → 재검증** 흐름이 자동으로 도는가
3. Step 2 미변환 PDF 탐지 후 Step 3 배치 권고 메시지가 자동으로 뜨는가
4. 사용자 동의 후 Step 5 변환이 실행되는가
5. Step 6 결과 한 줄이 사용자에게 그대로 전달되는가

특히 (2) 검증을 위해 marker 가 설치되지 않은 새 가상환경에서 한 번 호출해 보면 onboarding 흐름의 실효성을 가장 빠르게 확인할 수 있다.

## 결론

| 항목 | 값 |
|------|---|
| 신규 파일 | 4 (스킬 본문 1 + CLI 진입점 3) |
| 수정 파일 | 2 (`GUIDE.md`, `PARTICIPATION.md`) |
| 작업 시간 | 30~60 분 (스킬 본문 작성에 가장 많이 듦) |
| 추가 라이브러리 | 없음 (기존 `marker-pdf`, `convert_pdfs.py` 그대로 사용) |
| onboarding 효과 | 신규 팀원이 README 셋업 안내를 읽지 않아도 `/convert-pdf` 한 줄로 환경 점검·설치·변환까지 자동 진행 |

세 번째 스킬 (예: `/summarize`, `/translate`, `/citation-format`, `/glossary-add`) 도 같은 6 단계 절차로 추가된다. **다음 사람은 이 글을 그대로 복사해 자기 스킬 이름으로 치환하면 된다.**

이 글의 가치는 convert-pdf 자체가 아니다. **"새 스킬 추가에는 이 6 개 슬롯만 채우면 된다"** 는 표준 절차를 박제해 두는 것이 목적이다. Harness 가 잘 짜여 있을 때 새 스킬 추가가 얼마나 작은 작업인지 — 이걸 다음 사람이 검색해 찾을 수 있도록.

## Q&A

(빈 슬롯 — 발표 후 채운다)

## 다음 회

- 발표자: TBD
- 주제: TBD
- 일정: TBD
