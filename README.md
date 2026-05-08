# AI Seminar

개발팀 AI 지식 공유 세미나 아카이브. 프롬프트 엔지니어링부터 에이전트 구현까지 주제별 문서를 모읍니다.

## 구조

```
ai-seminar/
├── README.md                       # 인덱스 (이 파일)
├── PARTICIPATION.md                # 참여 안내 (역할·기여 방법)
├── CLAUDE.md / GEMINI.md           # Claude Code · Gemini CLI 진입점
├── .github/
│   ├── copilot-instructions.md     # GitHub Copilot 진입점
│   └── prompts/                    # Copilot reusable prompts (/qa, /convert-pdf)
├── .claude/commands/               # Claude Code 슬래시 커맨드 (/qa, /convert-pdf)
├── .gemini/commands/               # Gemini CLI 슬래시 커맨드 (/qa, /convert-pdf)
├── GUIDE.md                        # 슬래시 커맨드 라우팅 테이블
├── guides/                         # 에이전트 공통 규칙 + 스킬 본문
│   ├── GUIDE_CORE.md               # 항상-온 공통 규칙
│   ├── qa.md                       # 질의응답 스킬 본문
│   └── convert-pdf.md              # PDF → MD 변환 스킬 본문
├── topics/                         # 주제별 지식 문서 (개념·발표 자료·Q&A)
│   ├── engineering/
│   ├── rag/
│   ├── agents/
│   ├── models/
│   └── tools/
├── references/                     # 원본 PDF·논문 및 marker 변환 결과
│   ├── pdfs/                       # 원본 투입
│   └── md/                         # 변환 결과 (자동 생성)
├── system-scripts/                 # 파이프라인 스크립트
│   └── convert_pdfs.py
├── pyproject.toml                  # poetry 의존성 정의
└── poetry.lock                     # 버전 고정 (commit 함)
```

## 슬래시 커맨드

세 CLI (Claude Code · Gemini CLI · GitHub Copilot) 에서 동일하게 호출됩니다.

| 커맨드 | 용도 | 본문 |
|--------|------|------|
| `/qa <질문>` | 내부 문서 (`references/md/`, `topics/`) 근거 기반 질의응답 | [`guides/qa.md`](./guides/qa.md) |
| `/convert-pdf [파일/폴더]` | PDF → MD 변환. 첫 실행 시 poetry 환경 자동 셋업 | [`guides/convert-pdf.md`](./guides/convert-pdf.md) |

호출 예:

```
/qa RAG 에서 리랭킹이 언제 필요한가?
/qa attention 메커니즘의 핵심 아이디어는?
/convert-pdf
/convert-pdf paper.pdf
/convert-pdf references/pdfs/sub/
```

새 스킬 추가 절차는 [`topics/engineering/2-convert-pdf-skill-example.md`](./topics/engineering/2-convert-pdf-skill-example.md) 매뉴얼 참조. CLI 별 진입점 (CLAUDE.md / GEMINI.md / .github/copilot-instructions.md) → `GUIDE.md` 라우터 → `guides/<skill>.md` 체인으로 연결됩니다.

## 환경 설정

이 프로젝트는 **poetry** 로 의존성을 관리합니다. `/convert-pdf` 스킬을 호출하면 자동으로 셋업되지만, 수동 셋업도 가능합니다.

### 전제
- Python 3.10 이상 (3.13 이하). `pyenv` 또는 `python.org` 설치본 가능.
- poetry 1.5 이상 (없으면 1단계에서 설치).
- 의존성 관리는 poetry 로 통일합니다. conda·venv·uv 는 사용하지 않습니다.
- GPU 없어도 동작 (CPU에서 느릴 뿐). CUDA 있으면 자동 활용.

### 1단계 — poetry 설치 (한 번만)

poetry 가 없으면:

```bash
# 방법 A — pipx (권장)
pipx install poetry

# 방법 B — pip
python -m pip install --user poetry

# 확인
poetry --version
```

### 2단계 — 의존성 설치

```bash
poetry install
```

이 한 줄이 가상환경을 자동으로 만들고 `marker-pdf` 를 포함한 모든 의존성을 설치합니다. `poetry.lock` 은 commit 합니다 (팀원 간 버전 재현성 보장).

### 설치 확인

```bash
poetry run marker_single --help
```

### PDF 변환 실행

```bash
# references/pdfs/ 에 PDF 넣은 뒤 — 전체 변환
poetry run python system-scripts/convert_pdfs.py

# 단일 파일
poetry run python system-scripts/convert_pdfs.py paper.pdf

# 폴더
poetry run python system-scripts/convert_pdfs.py references/pdfs/sub/

# 여러 인자 혼합
poetry run python system-scripts/convert_pdfs.py a.pdf b.pdf sub/
```

또는 슬래시 커맨드로 한 줄 실행:

```
/convert-pdf
/convert-pdf paper.pdf
```

결과는 `references/md/<파일명>/<파일명>.md` 로 생성됩니다. 이미 변환된 파일은 건너뜁니다.

#### 출력 예시

```text
[output_dir] C:\Users\...\references\md
[convert] paper.pdf -> references\md\paper\paper.md
[time] paper.pdf: 87.3s (ok)

[done] total=1 skipped=0 failed=0 elapsed=87.3s (output: C:\Users\...\references\md)
```

`[time]` 줄로 PDF 1 개당 소요 시간, `elapsed=` 로 전체 시간을 확인할 수 있습니다. 변환 시간은 환경에 따라 다릅니다 — GPU 가 있으면 페이지당 0.3~2 초, CPU 만 있으면 5~15 초 범위입니다.

> 처음 실행 시 marker가 모델 가중치를 다운로드합니다 (수백 MB, 5~10 분). 네트워크 필요.

## 기여 방법

운영자·참여자 역할별 상세 안내는 [PARTICIPATION.md](./PARTICIPATION.md) 참조. AI 엔지니어링이 익숙하지 않아도 PR 환영합니다 (Lv1 의 "자기 도메인 PDF 던지기" 는 1 분 안에 가능).

빠른 요약:

1. 주제에 맞는 폴더에 마크다운 파일 추가
2. 파일명: `kebab-case.md`
3. 문서 상단에 메타데이터 (작성자, 날짜, 태그) 포함 권장
4. 아래 인덱스에 링크 추가

## 주제별 문서

### Engineering
- [0. Skill-based Prompt Engineering](./topics/engineering/0-skill-based-prompt-engineering.md) — Prompt · Context · Harness 3 층 정의 + Claude Code vs Copilot CLI 하네스 비교
- [1. AI 학습 공동체에 Agent 가 스며드는 과정](./topics/engineering/1-skill-based-prompt-example.md) — ai-seminar 자체가 3 층을 거친 진화 서사 (`/qa` 스킬 emergence)
- [2. 새 스킬 추가하는 법 — convert-pdf 사례 매뉴얼](./topics/engineering/2-convert-pdf-skill-example.md) — Harness 위에 새 슬래시 커맨드를 얹는 표준 절차 (poetry 자동 부트스트랩 포함)

### RAG
- _문서 추가 예정_

### Agents
- _문서 추가 예정_

### Models
- _문서 추가 예정_

### Tools
- _문서 추가 예정_

## 검색 팁

- 파일명 검색은 `t` 키로 빠르게 접근
- 새 슬래시 커맨드 추가는 [`GUIDE.md`](./GUIDE.md) 라우팅 테이블에서 시작 (절차는 위 Engineering §2 매뉴얼 참조)
- 에이전트 공통 규칙은 [`guides/GUIDE_CORE.md`](./guides/GUIDE_CORE.md) (한다 체·이모지 금지·근거 인용 등)
