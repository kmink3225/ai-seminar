---
title: "새 스킬 추가하는 법 — convert-pdf 사례 매뉴얼"
subtitle: "ai-seminar 의 Harness 위에 새 슬래시 커맨드를 얹는 표준 절차 (poetry 단일 의존성 관리 + 자동 부트스트랩 + 인자 처리)"
description: |
  1번 글이 qa 스킬이 어떻게 자라났는지의 회고 서사였다면, 이 글은 두 번째 스킬을
  실제로 추가하는 절차를 단계별 매뉴얼 형태로 정리한다. 사례는 convert-pdf —
  references/pdfs/ 의 PDF 를 marker 로 references/md/ 로 변환하는 슬래시 커맨드.
  의존성은 poetry 로 통일 관리하며, 스킬은 프로그래밍 미경험자도 /convert-pdf
  한 줄로 끝까지 도달하도록 환경 부트스트랩 (기존 poetry env 자동 발견·재사용,
  없으면 poetry 자동 셋업) 을 자체 처리한다. 인자로 파일·폴더를 지정해 부분
  변환도 가능하다.
tags: [engineering, harness, skill-engineering, manual, convert-pdf, marker, onboarding, poetry]
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
- **프로그래밍 미경험자 onboarding 자동화** — 새로 clone 한 팀원의 환경에 marker 가 없을 때 스킬이 기존 poetry env 검색 → 발견 시 재사용, 미발견 시 poetry 자동 셋업까지 처리. 신규 팀원은 `/convert-pdf` 한 줄만 알면 된다
- **부분 변환 지원** — 인자로 파일·폴더를 지정하면 그 대상만 변환 (전체 batch 가 부담스러운 경우)

## 추가하는 파일 4 + 수정하는 파일 3

| # | 경로 | 신규/수정 | 역할 |
|---|------|---------|------|
| 1 | `guides/convert-pdf.md` | 신규 | 스킬 본문 (Step 1~6) |
| 2 | `.claude/commands/convert-pdf.md` | 신규 | Claude Code 슬래시 |
| 3 | `.gemini/commands/convert-pdf.toml` | 신규 | Gemini CLI 슬래시 |
| 4 | `.github/prompts/convert-pdf.prompt.md` | 신규 | Copilot prompt |
| 5 | `GUIDE.md` | 수정 | 라우팅 테이블에 `/convert-pdf` 행 추가 + Skill 행동 원칙 (poetry 통일) |
| 6 | `PARTICIPATION.md` | 수정 | Lv1 끝의 "marker 변환" 언급 갱신 |
| 7 | `pyproject.toml` | 수정 | poetry 형식으로 전환 (일회성) |

## Step 1 — 스킬 본문: `guides/convert-pdf.md`

`guides/qa.md` 의 패턴을 그대로 따른다 (frontmatter `name`·`type`·`description` + Step + 금지).

```yaml
---
name: convert-pdf
type: skill
version: 1.5
description: references/pdfs/ 의 PDF 를 marker 로 references/md/ 에 변환. 의존성은 poetry 로 통일 관리. 첫 실행 시 기존 poetry env 자동 발견 → 없으면 poetry 자동 설치 + poetry install 까지 한 번에. 인자로 파일/폴더 지정 가능.
---
```

본문은 6 단계로 구성한다.

| Step | 무엇을 |
|------|------|
| 1 | **환경 자동 부트스트랩 (poetry 통일)** — 1-A 현재 셸 `marker_single --help` 통과? → 1-B `poetry env info -p` 로 기존 poetry env 검사 (있으면 재사용) → 1-C 없으면 사용자 동의 후 poetry 자동 설치 (1-C-pre) + `poetry install` (1-C-main) → 1-D 모델 가중치 안내. 결정된 python 경로를 `PYTHON_BIN` 으로 저장 |
| 2 | 미변환 PDF 탐지 — 인자 없으면 `references/pdfs/` 전체, 인자 있으면 해당 파일/폴더만 |
| 3 | 배치 권고 메시지 출력 (`GUIDE_CORE.md` §7) |
| 4 | 사용자 동의 확인 ("지금 변환" / "배치 무시" / "바로 돌려") |
| 5 | `<PYTHON_BIN> system-scripts/convert_pdfs.py [인자]` 실행 (또는 `poetry run python ...`) — Step 1 의 PYTHON_BIN 사용 |
| 6 | 결과 보고 — `[done] total=N skipped=K failed=L (output: ...)` 한 줄 + 실패 파일 목록 + 경로 에러 |

### Step 1 의 설계 의도 — 한 줄로 끝까지 도달

새 팀원이 리포를 clone 한 직후의 상태는 다양하다.

| 상태 | 빈도 | 스킬 행동 |
|------|------|---------|
| 셸이 이미 marker 있는 환경 (예: `poetry shell` 후) | 흔함 | 1-A 통과 → 즉시 변환 |
| 기존 poetry env 가 있는데 활성화 안 됨 | 흔함 | 1-B 발견 → 그 env 재사용 (셸 활성화 불필요, `poetry run` 또는 절대 경로 호출) |
| 어디에도 marker 없음 | 신규 머신 | 1-C 동의 1 회 → poetry 자동 설치 + `poetry install` (가상환경·의존성 일괄) |

세 경우 모두 사용자가 알아야 할 명령은 단 하나: `/convert-pdf`. README 의 환경 셋업 섹션을 읽지 않아도 된다.

핵심 트릭은 **셸 활성화 없이 그 env 의 python 을 직접 호출** 하는 것이다.

```bash
# 셸 활성화 패턴 (사용자가 직접 할 때)
poetry shell
python system-scripts/convert_pdfs.py paper.pdf

# 절대 경로 호출 (스킬이 자동으로 할 때)
poetry run python system-scripts/convert_pdfs.py paper.pdf
```

후자는 셸 상태를 건드리지 않으므로 스킬이 안전하게 사용할 수 있다.

### 왜 poetry 단일인가

- pyproject.toml 한 파일에 의존성·버전·메타데이터 모두 정리됨
- `poetry install` 한 줄이 가상환경 자동 생성 + 의존성 설치를 묶어 처리 → 신규 팀원 onboarding 마찰 최소
- `poetry run` prefix 로 셸 활성화 없이 그 환경의 명령 호출 가능
- `poetry.lock` 으로 팀원 간 버전 재현성 보장
- conda·venv·uv 같은 다른 도구를 섞지 않음으로써 "어느 도구로 깔아야 하나" 분기 자체를 제거 — 신규 팀원은 README 1단계·2단계만 따라하면 됨

이전에 conda env 등에 marker 를 깔아둔 적이 있더라도, 이 프로젝트의 의존성은 poetry 로 통일 관리한다. 스킬도 poetry env 만 검색·재사용하며, 그 외 도구로 설치된 환경은 무시한다.

### 인자 처리 — 전체 vs 부분 변환

스킬은 사용자 인자를 그대로 스크립트에 전달한다. 스크립트 (`system-scripts/convert_pdfs.py`) 는 `argparse.nargs="*"` 로 0~N 개 인자를 받는다.

| 호출 | 동작 |
|------|------|
| `/convert-pdf` | `references/pdfs/` 전체를 rglob 으로 펼쳐 변환 (배치 모드) |
| `/convert-pdf paper.pdf` | 단일 파일 |
| `/convert-pdf references/pdfs/sub/` | 그 폴더 안 모든 PDF |
| `/convert-pdf a.pdf b.pdf sub/` | 여러 인자 혼합 |

상대경로는 현재 디렉토리 → `references/pdfs/` 순으로 시도되므로, 어디서 호출하든 PDF 이름만 맞으면 작동한다. 출력은 어느 경우든 `references/md/<stem>/<stem>.md` 한 곳에 모인다.

## Step 2 — Claude Code 슬래시: `.claude/commands/convert-pdf.md`

`.claude/commands/qa.md` 의 패턴. frontmatter `description` + 실행 순서 (라우터 → CORE → 스킬 → 실행 → Self-Check).

`$ARGUMENTS` 를 prompt 본문에 두어 사용자가 `/convert-pdf` 뒤에 입력한 인자를 받는다. 인자 없이 호출되면 `$ARGUMENTS` 가 빈 문자열이 되어 스크립트는 전체 모드로 동작한다.

## Step 3 — Gemini CLI 슬래시: `.gemini/commands/convert-pdf.toml`

`.gemini/commands/qa.toml` 의 패턴. TOML 의 `description` + `prompt` 두 키만 있으면 된다. `{{args}}` 를 prompt 본문에 두어 인자를 받는다.

## Step 4 — Copilot prompt: `.github/prompts/convert-pdf.prompt.md`

`.github/prompts/qa.prompt.md` 의 패턴. frontmatter `mode: agent` + `description`. 경로 참조는 `.github/prompts/` 기준 상대경로 (`../copilot-instructions.md`, `../../GUIDE.md`, `../../guides/...`). Copilot 은 `$ARGUMENTS`·`{{args}}` 같은 명시적 변수 치환은 안 하므로, prompt 본문에 "사용자가 `/convert-pdf` 뒤에 입력한 텍스트를 그대로 스크립트 인자로 전달한다" 고 명시한다.

## Step 5 — 라우팅 등록: `GUIDE.md` 수정

라우팅 테이블에 한 행 추가하고, `Skill 행동 원칙` 섹션에서 "poetry 통일 관리" 와 "활성화 안내 후 종료 금지" 를 명시한다.

```diff
| 명령어 | 태스크 | 로드할 가이드 (CORE 제외) |
|--------|--------|--------------------------|
| `/qa [question]` | 질의응답 ... | `guides/qa.md` |
+| `/convert-pdf [target]` | PDF → MD 변환 ... | `guides/convert-pdf.md` |
```

## Step 6 — `PARTICIPATION.md` 한 줄 갱신

§3.1 Lv1 끝 부분:

```diff
-추후 누군가 marker 변환을 돌리면 `references/md/` 에 자동 변환된 markdown 이 생성된다.
+추후 누군가 `/convert-pdf` 스킬을 호출하면 `references/md/` 에 자동 변환된 markdown 이 생성된다 (첫 실행 시 marker 의존성도 자동 설치됨).
```

## Step 7 (선택) — `pyproject.toml` 을 poetry 형식으로

기존 setuptools 기반 PEP 621 형식에서 poetry 형식으로 전환한다. 이 단계는 일회성 (이미 전환된 후라면 건너뛴다).

```toml
[tool.poetry]
name = "ai-seminar"
version = "0.1.0"
description = "AI 지식 공유 세미나 아카이브 및 PDF→MD 변환 파이프라인"
readme = "README.md"
authors = ["Kwangmin Kim"]
package-mode = false

[tool.poetry.dependencies]
python = ">=3.10,<3.14"
marker-pdf = ">=1.10.0"

[tool.poetry.group.dev.dependencies]
ruff = ">=0.6.0"

[build-system]
requires = ["poetry-core>=1.5.0"]
build-backend = "poetry.core.masonry.api"
```

`package-mode = false` 가 핵심 — ai-seminar 는 라이브러리가 아니라 환경 정의용 프로젝트라, poetry 가 패키지 빌드를 시도하지 않도록 명시한다.

## 검증 — 스킬이 작동하는가

세 CLI 에서 차례로 호출해 본다.

- Claude Code: `/convert-pdf`, `/convert-pdf paper.pdf`
- Gemini CLI: `/convert-pdf`, `/convert-pdf paper.pdf`
- Copilot Chat / CLI: `/convert-pdf`, `/convert-pdf paper.pdf`

세 가지 시나리오 모두에서 스킬이 끝까지 도달하는지 확인한다.

| 시나리오 | 환경 상태 | 기대 동작 |
|----------|---------|---------|
| (a) 활성 셸이 poetry env | `poetry shell` 후 호출 | 1-A 통과 → 즉시 변환 |
| (b) poetry env 는 있으나 활성화 안 됨 | 시스템 셸에서 호출 | 1-B 발견 → `poetry run` 또는 절대 경로로 변환 |
| (c) 어디에도 marker 없음 | 새 머신 | 1-C 동의 → poetry 설치 (필요 시) + `poetry install` → 변환 |

(c) 시나리오는 새 가상 머신 또는 깨끗한 사용자 계정에서만 검증 가능하다. 발표 자리에서 시연이 어렵다면, 기존 머신에서 (b) 시나리오만 시연해도 "기존 환경 자동 재사용" 동작을 충분히 보여줄 수 있다.

## 결론

| 항목 | 값 |
|------|---|
| 신규 파일 | 4 (스킬 본문 1 + CLI 진입점 3) |
| 수정 파일 | 3 (`GUIDE.md`, `PARTICIPATION.md`, `pyproject.toml`) |
| 작업 시간 | 30~60 분 (스킬 본문 작성에 가장 많이 듦) |
| 추가 라이브러리 | 없음 (기존 `marker-pdf`, `convert_pdfs.py` 그대로 사용. poetry 는 의존성 관리 도구) |
| onboarding 효과 | 신규 팀원이 README 셋업 안내를 읽지 않아도 `/convert-pdf` 한 줄로 환경 검색·생성·설치·변환까지 자동 진행 |
| 부분 변환 | 인자로 파일·폴더 지정 가능 — 전체 batch 부담을 줄임 |

세 번째 스킬 (예: `/summarize`, `/translate`, `/citation-format`, `/glossary-add`) 도 같은 6 단계 절차로 추가된다. **다음 사람은 이 글을 그대로 복사해 자기 스킬 이름으로 치환하면 된다.**

이 글의 가치는 convert-pdf 자체가 아니다. **"새 스킬 추가에는 이 6 개 슬롯만 채우면 된다"** 는 표준 절차를 박제해 두는 것이 목적이다. Harness 가 잘 짜여 있을 때 새 스킬 추가가 얼마나 작은 작업인지 — 이걸 다음 사람이 검색해 찾을 수 있도록.

## Q&A

(빈 슬롯 — 발표 후 채운다)

## 다음 발표자 / 발표 자료

홍길동 - `TBD`