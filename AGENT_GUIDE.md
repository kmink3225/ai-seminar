---
name: AGENT_GUIDE
type: router
version: 1.0
last_updated: 2026-04-16
description: >
  슬래시 커맨드 라우터. 사용자 명령에 매핑된 가이드만 로드한다.
  공통 규칙은 guides/AGENT_GUIDE_CORE.md — 모든 태스크에서 먼저 로드한다.
scope: project
---

# AGENT_GUIDE.md — ai-seminar 진입점

> 모든 공통 규칙은 `guides/AGENT_GUIDE_CORE.md` 에 있다. 작업 전 반드시 먼저 읽는다.
>
> **각 CLI 진입점**:
> - Claude Code → `CLAUDE.md`
> - Gemini CLI → `GEMINI.md`
> - GitHub Copilot (CLI / IDE) → `.github/copilot-instructions.md`
>
> 각 진입점은 CLI 별 Phase 프로토콜·절대 규칙만 담고, 라우팅·저장 규칙·프로젝트 정보는 이 파일이 canonical 이다.

---

## 로드 원칙

```
사용자 입력
    ↓
CLI 진입점 (CLAUDE.md / GEMINI.md / .github/copilot-instructions.md)
    ↓
AGENT_GUIDE.md  (이 파일 — 라우팅 테이블)
    ↓
guides/AGENT_GUIDE_CORE.md  (항상-온 공통 규칙)
    ↓
슬래시 커맨드 파싱 → 매핑 테이블 조회
    ↓
해당 skill 가이드만 로드
    ↓
실행
```

이 파일은 **진입점 바로 다음 단계**다. 진입점에서 이 파일을 읽은 뒤, 이 파일이 `guides/AGENT_GUIDE_CORE.md` 로드를 지시하고, 이어서 커맨드 매핑에 따라 필요한 skill 가이드만 로드한다.

슬래시 커맨드가 없으면 자연어로 가장 적합한 행을 추론한다.

---

## 슬래시 커맨드 정의

| 명령어 | 태스크 | 로드할 가이드 (CORE 제외) |
|--------|--------|--------------------------|
| `/search [query]` | **검색** — `references/md/`, `topics/`, `papers/`, `sessions/` 전체 Grep → 관련 문서 목록·근거 스니펫 반환 (파일 변경 없음) | `guides/search.md` |
| `/qa [question]` | **질의응답** — 내부 문서 검색 → 근거 기반 통합 답변. 근거 부족 시 "모름" 명시 (파일 변경 없음) | `guides/search.md` + `guides/qa.md` |
| `/analyze [file]` | **문서 분석** — 지정 md/pdf 1개를 읽고 요약·핵심 포인트·한계 도출. 결과를 `sessions/` 또는 `papers/` 하위에 저장 가능 | `guides/analyze.md` |
| `/code [description]` | **코드 구현** — 내부 문서 또는 사용자 설명을 바탕으로 실행 가능한 예제 코드 작성. 결과는 관련 `topics/` 또는 `sessions/` 하위에 저장 | `guides/search.md` + `guides/code.md` |
| `/ingest` | **PDF → MD 변환** — `references/pdfs/` 신규 PDF 를 `references/md/` 로 변환 (`scripts/convert_pdfs.py` 실행). idempotent | `guides/ingest.md` |

### 사용 예시

| 명령어 | 예시 |
|--------|------|
| `/search` | `/search chain-of-thought` |
| `/qa` | `/qa RAG 에서 리랭킹이 언제 필요한가?` |
| `/analyze` | `/analyze references/md/attention-is-all-you-need/attention-is-all-you-need.md` |
| `/code` | `/code tool-use 루프를 Anthropic SDK 로 구현` |
| `/ingest` | `/ingest` |

### 커맨드별 로드 비교

```
/search chain-of-thought
  → CORE + search
  → 로드 안 함: qa, analyze, code, ingest

/qa RAG에서 리랭킹 필요 시점
  → CORE + search + qa
  → 로드 안 함: analyze, code, ingest

/analyze papers/xxx.md
  → CORE + analyze
  → 로드 안 함: search, qa, code, ingest

/code tool-use 루프 구현
  → CORE + search + code
  → 로드 안 함: qa, analyze, ingest

/ingest
  → CORE + ingest
  → 로드 안 함: search, qa, analyze, code
```

**슬래시 커맨드가 없으면**: 일반 질문(General Inquiry)으로 간주, 가이드 제약 없이 자율 답변. 사용자가 검색·분석·수정·작성을 명시하면 위 테이블의 해당 커맨드를 적용한다.

---

## 폴더 목록

| 폴더 | 용도 |
|------|------|
| `sessions/` | 세미나 회차별 자료 (YYYY-MM-DD-topic) |
| `topics/` | 주제별 지식 문서 (prompt-engineering, rag, agents, models, tools) |
| `papers/` | 논문 리뷰 |
| `references/pdfs/` | 원본 PDF (투입) |
| `references/md/` | marker 변환 결과 (자동 생성) |
| `scripts/` | 파이프라인 스크립트 |
| `guides/` | 에이전트 가이드 |

---

## 규칙 우선순위

```
guides/AGENT_GUIDE_CORE.md  >  에이전트 자체 판단
```

---

## Project Info

- **Repo**: https://github.com/kmink3225/ai-seminar
- **Stack**: Python 3.10+, marker-pdf
- **Setup**: `pip install -e .`
- **PDF 변환**: `python scripts/convert_pdfs.py`
