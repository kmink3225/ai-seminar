---
name: GUIDE
type: router
version: 2.1
last_updated: 2026-05-07
description: >
  슬래시 커맨드 라우터. 사용자 명령에 매핑된 가이드만 로드한다.
  공통 규칙은 guides/GUIDE_CORE.md — 이 파일이 로드를 지시한다.
scope: project
---

# GUIDE.md — ai-seminar 진입점

> 이 파일은 **라우터** 다. CLI 진입점이 이 파일을 읽은 뒤, 이 파일이 CORE 와 skill 가이드 로드를 지시한다.
>
> **각 CLI 진입점**:
> - Claude Code → `CLAUDE.md`
> - Gemini CLI → `GEMINI.md`
> - GitHub Copilot (CLI / IDE) → `.github/copilot-instructions.md`

---

## 로드 원칙

```
사용자 입력
    ↓
CLI 진입점 (CLAUDE.md / GEMINI.md / .github/copilot-instructions.md)
    ↓
GUIDE.md  (이 파일 — 라우팅 테이블)
    ↓
guides/GUIDE_CORE.md  (항상-온 공통 규칙)
    ↓
슬래시 커맨드 파싱 → 매핑 테이블 조회
    ↓
해당 skill 가이드만 로드
    ↓
실행
```

슬래시 커맨드가 없으면 자연어로 가장 적합한 행을 추론한다.

---

## 슬래시 커맨드 정의

| 명령어 | 태스크 | 로드할 가이드 (CORE 제외) |
|--------|--------|--------------------------|
| `/qa [question]` | **질의응답** — 내부 문서(`references/md/`, `topics/`) 검색 후 근거 기반 답변. 파일 변경 없음 | `guides/qa.md` |
| `/convert-pdf` | **PDF → MD 변환** — `references/pdfs/` 의 신규 PDF 를 marker 로 `references/md/` 에 일괄 변환. 첫 실행 시 marker 의존성 자동 설치, 배치 권고 후 사용자 동의 시 실행 | `guides/convert-pdf.md` |

### 사용 예시

```
/qa RAG 에서 리랭킹이 언제 필요한가?
/qa chain-of-thought 와 tree-of-thought 의 차이는?
/qa attention 메커니즘의 핵심 아이디어는?
/convert-pdf
```

### 커맨드별 로드 비교

```
/qa RAG에서 리랭킹 필요 시점
  → GUIDE.md (이 파일) + CORE + qa.md
  → skill 가이드는 qa.md 1 개만 로드

/convert-pdf
  → GUIDE.md (이 파일) + CORE + convert-pdf.md
  → skill 가이드는 convert-pdf.md 1 개만 로드
```

**슬래시 커맨드가 없으면**: 일반 질문으로 간주, 가이드 제약 없이 자율 답변. 사용자가 명시적으로 질의응답을 요청하면 `/qa` 를 적용한다.

---

## Skill 행동 원칙 (모든 스킬 공통)

이 프로젝트는 **poetry 로 의존성을 통일 관리** 한다. conda·venv·uv 등 다른 도구는 사용하지 않는다.

스킬은 사용자 환경 상태와 무관하게 **끝까지 도달** 한다. 다음 메시지로 중단하지 않는다.

- "가상환경을 활성화한 뒤 다시 호출하라"
- "README 의 셋업을 먼저 하라"
- "가상환경 셋업이 필요하다. 종료한다"

스킬이 현재 셸의 활성화 상태를 직접 바꿀 수 없다는 사실은 사용자에게 부담을 떠넘기는 근거가 되지 않는다 — **`poetry run` 또는 절대 경로로 그 env 의 python 을 직접 호출** 하면 활성화 없이도 작동한다.

```bash
# 활성화 없이 그 env 의 python 직접 호출 (스킬이 사용하는 패턴)
poetry run python system-scripts/convert_pdfs.py ...
<poetry-env>\Scripts\python.exe system-scripts/convert_pdfs.py ...    # Windows
<poetry-env>/bin/python system-scripts/convert_pdfs.py ...            # Unix
```

### 환경 부트스트랩 표준 절차

스킬이 외부 도구 (marker, langchain 등) 를 호출해야 할 때 다음 순서를 따른다.

1. **현재 셸에서 작동?** → 통과 (가장 빠른 경로)
2. **기존 poetry env 가 있나?** `poetry env info -p` 로 검사 → 발견 + 도구 import 성공 시 그 env 의 python 절대 경로 (또는 `poetry run`) 로 호출 (활성화 X)
3. **없음** → 사용자 동의 1 회 후 자동 셋업:
   - poetry 자체가 미설치라면 먼저 `pipx install poetry` 또는 `python -m pip install --user poetry` 로 설치
   - 이어서 `poetry install` 로 가상환경 + 의존성 일괄 셋업
   - 결정된 env 의 python 경로 (또는 `poetry run`) 로 후속 호출

세 단계 어디서도 "활성화하고 다시 호출하라" 로 종료하지 않는다. 사용자가 알아야 할 명령은 슬래시 한 줄뿐이다.

---

## 폴더 목록

| 폴더 | 용도 |
|------|------|
| `topics/` | 주제별 지식 문서 (engineering, rag, agents, models, tools) — 개념 본문, 발표 자료, Q&A 포함 |
| `references/pdfs/` | 원본 PDF · 논문 (투입) |
| `references/md/` | marker 변환 결과 (자동 생성) |
| `system-scripts/` | 파이프라인 스크립트 (`convert_pdfs.py`) |
| `guides/` | 에이전트 가이드 |

`references/md/` 는 `/convert-pdf` 스킬 (또는 `python system-scripts/convert_pdfs.py` 직접 실행) 로 채운다.

---

## 규칙 우선순위

```
guides/GUIDE_CORE.md  >  에이전트 자체 판단
```

---

## Project Info

- **Repo**: https://github.com/kmink3225/ai-seminar
- **Stack**: Python 3.10+, marker-pdf
- **Setup**: `pip install -e .`
- **PDF 변환**: `/convert-pdf` (또는 `python system-scripts/convert_pdfs.py` 직접)
