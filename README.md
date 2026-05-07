# AI Seminar

개발팀 AI 지식 공유 세미나 아카이브. 프롬프트 엔지니어링부터 에이전트 구현까지 주제별 문서를 모읍니다.

## 구조

```
ai-seminar/
├── README.md                  # 인덱스
├── topics/                    # 주제별 지식 문서 (개념 본문·발표 자료·Q&A)
│   ├── engineering/
│   ├── rag/
│   ├── agents/
│   ├── models/
│   └── tools/
└── references/                # 원본 PDF·논문 및 marker 변환 결과
    ├── pdfs/
    └── md/
```

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

이 한 줄이 가상환경을 자동으로 만들고 `marker-pdf` 를 포함한 모든 의존성을 설치합니다.

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
```

또는 슬래시 커맨드로 한 줄 실행:

```
/convert-pdf
/convert-pdf paper.pdf
```

결과는 `references/md/<파일명>/<파일명>.md` 로 생성됩니다. 이미 변환된 파일은 건너뜁니다.

> 처음 실행 시 marker가 모델 가중치를 다운로드합니다 (수백 MB, 5~10 분). 네트워크 필요.

## 기여 방법

운영자·참여자 역할별 상세 안내는 [PARTICIPATION.md](./PARTICIPATION.md) 참조. AI 엔지니어링이 익숙하지 않아도 PR 환영한다 (Lv1 의 "자기 도메인 PDF 던지기" 는 1 분 안에 가능).

빠른 요약:

1. 주제에 맞는 폴더에 마크다운 파일 추가
2. 파일명: `kebab-case.md`
3. 문서 상단에 메타데이터 (작성자, 날짜, 태그) 포함 권장
4. 아래 인덱스에 링크 추가

## 주제별 문서

### Engineering
- _문서 추가 예정_

### RAG
- _문서 추가 예정_

### Agents
- _문서 추가 예정_

### Models
- _문서 추가 예정_

### Tools
- _문서 추가 예정_

## 검색 팁

- GitHub 상단 검색창에 `repo:kmink3225/ai-seminar <키워드>` 로 전체 검색
- 파일명 검색은 `t` 키로 빠르게 접근
