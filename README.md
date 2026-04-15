# AI Seminar

개발팀 AI 지식 공유 세미나 아카이브. 프롬프트 엔지니어링부터 에이전트 구현까지 주제별 문서를 모읍니다.

## 구조

```
ai-seminar/
├── README.md                  # 인덱스
├── sessions/                  # 세미나 회차별 자료 (날짜-주제)
│   └── YYYY-MM-DD-topic/
│       ├── README.md          # 발표 요약
│       └── assets/            # 이미지, 슬라이드 등
├── topics/                    # 주제별 지식 문서
│   ├── prompt-engineering/
│   ├── rag/
│   ├── agents/
│   ├── models/
│   └── tools/
├── papers/                    # 논문 리뷰
└── references/                # 외부 링크/자료 모음
```

## 환경 설정

PDF → Markdown 변환(marker) 파이프라인을 사용하려면 아래 1회 세팅이 필요합니다.

### 전제
- Python 3.10 이상 (3.13 이하). `pyenv` / `conda` / `python.org` 설치본 모두 가능.
- GPU 없어도 동작 (CPU에서 느릴 뿐). CUDA 있으면 자동 활용.

### 방법 A — conda (권장, 팀원 간 재현성 좋음)

```bash
conda create -n ai-seminar python=3.11 -y
conda activate ai-seminar
pip install -e .
```

### 방법 B — venv

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -e .
```

### 방법 C — uv (빠름)

```bash
uv venv
uv pip install -e .
```

### 설치 확인

```bash
marker_single --help
```

### PDF 변환 실행

```bash
# references/pdfs/ 에 PDF 넣은 뒤
python scripts/convert_pdfs.py
```

결과는 `references/md/<파일명>/<파일명>.md` 로 생성됩니다. 이미 변환된 파일은 건너뜁니다.

> 처음 실행 시 marker가 모델 가중치를 다운로드합니다(수백 MB). 네트워크 필요.

## 기여 방법

1. 주제에 맞는 폴더에 마크다운 파일 추가
2. 파일명: `kebab-case.md`
3. 문서 상단에 메타데이터 (작성자, 날짜, 태그) 포함 권장
4. 아래 인덱스에 링크 추가

## 세미나 세션

<!-- 새 세션은 최신순으로 위에 추가 -->

- _아직 세션이 없습니다._

## 주제별 문서

### Prompt Engineering
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
