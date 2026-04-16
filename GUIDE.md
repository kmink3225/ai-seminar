---
name: GUIDE
type: router
version: 2.0
last_updated: 2026-04-16
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

### 사용 예시

```
/qa RAG 에서 리랭킹이 언제 필요한가?
/qa chain-of-thought 와 tree-of-thought 의 차이는?
/qa attention 메커니즘의 핵심 아이디어는?
```

### 커맨드별 로드 비교

```
/qa RAG에서 리랭킹 필요 시점
  → GUIDE.md (이 파일) + CORE + qa.md
  → skill 가이드는 qa.md 1 개만 로드
```

**슬래시 커맨드가 없으면**: 일반 질문으로 간주, 가이드 제약 없이 자율 답변. 사용자가 명시적으로 질의응답을 요청하면 `/qa` 를 적용한다.

---

## 폴더 목록

| 폴더 | 용도 |
|------|------|
| `topics/` | 주제별 지식 문서 (engineering, rag, agents, models, tools) — 개념 본문, 발표 자료, Q&A 포함 |
| `references/pdfs/` | 원본 PDF · 논문 (투입) |
| `references/md/` | marker 변환 결과 (자동 생성) |
| `scripts/` | 파이프라인 스크립트 (`convert_pdfs.py`) |
| `guides/` | 에이전트 가이드 |

`references/md/` 는 `python scripts/convert_pdfs.py` 로 채운다 (PDF→MD 변환).

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
- **PDF 변환**: `python scripts/convert_pdfs.py`
