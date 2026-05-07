---
name: convert-pdf
type: skill
version: 1.1
description: references/pdfs/ 의 신규 PDF 를 marker 로 references/md/ 에 일괄 변환. 첫 실행 시 marker 의존성·모델 가중치 자동 설치.
---

# convert-pdf — PDF → MD 변환

## 목적

`references/pdfs/` 에 누적된 PDF 를 `marker` 로 `references/md/` 에 markdown 으로 일괄 변환한다. 이미 변환된 파일은 건너뛴다 (idempotent). 변환은 GPU 없이도 동작하지만 모델 추론에 수 분 ~ 수십 분이 걸린다 — 따라서 **배치 작업** 으로 다룬다.

새로운 머신에서 처음 실행할 때 marker 가 설치되지 않았을 수 있다. 이 스킬은 그 경우를 자동으로 감지하고 의존성·모델 가중치 안내까지 처리한 뒤 변환으로 진행한다.

## Step

### Step 1 — 환경 점검 (첫 실행 시 자동 onboarding)

다음 명령으로 marker 가 활성 환경에 설치되어 있는지 확인한다.

```bash
marker_single --help
```

종료 코드 0 으로 도움말이 출력되면 통과 → Step 2 로. 명령이 실패하거나 `command not found` 가 나오면 의존성 미설치 상태다. 다음 절차로 진행한다.

#### 1-A. 가상환경 확인

먼저 현재 활성화된 가상환경이 있는지 확인한다.

- `python -c "import sys; print(sys.prefix)"` 출력이 시스템 경로 (`/usr`, `C:\Python*`, `C:\Program Files\*`) 면 가상환경 미활성화
- conda 환경이면 `$CONDA_DEFAULT_ENV` 또는 `%CONDA_DEFAULT_ENV%` 가 `base` 또는 빈 값이면 별도 환경 미활성화

가상환경이 없으면 사용자에게 다음 메시지를 출력하고 종료한다 (시스템 python 오염을 막기 위함).

```text
[환경 셋업 필요] 가상환경이 활성화되어 있지 않다.
README.md 의 환경 셋업 섹션 (방법 A conda / B venv / C uv 중 하나) 을 먼저 수행한 뒤
같은 셸에서 환경을 활성화하고 /convert-pdf 를 다시 호출해 달라.
```

#### 1-B. 의존성 설치

가상환경이 활성화되어 있으면 사용자에게 다음 메시지를 출력한다.

```text
[의존성 설치 권고] 활성 환경에 marker 가 설치되어 있지 않다.
다음 명령으로 marker-pdf (>=1.10.0) 를 설치한다 (수십 MB 다운로드, 1~3 분):

  pip install -e .

설치를 진행하려면 "설치" 라고 답해 달라.
```

- "설치" / "OK" / "go" → `pip install -e .` 실행
- 동의 없음 → 종료

설치 후 `marker_single --help` 로 재검증한다. 재검증 실패 시 사용자에게 에러 메시지 그대로 보고하고 종료.

#### 1-C. 모델 가중치 안내

marker 자체가 설치돼도 첫 변환 시 모델 가중치 (수백 MB) 가 자동 다운로드된다. 이 다운로드는 Step 5 의 첫 PDF 변환 시점에 일어난다 — 따라서 **첫 실행이 평소보다 5~10 분 더 길다** 는 점을 사용자에게 미리 안내한다.

### Step 2 — 미변환 PDF 탐지

`references/pdfs/` 와 `references/md/` 를 비교해 미변환 PDF 목록을 만든다.

- `references/pdfs/**/*.pdf` 전체 나열
- 각 PDF 에 대해 `references/md/<stem>/<stem>.md` 존재 확인
- 미변환 목록과 개수를 사용자에게 한 줄로 보고

미변환 PDF 가 0 개면 "변환할 PDF 없음" 으로 보고 후 즉시 종료.

### Step 3 — 배치 권고 메시지 출력

`guides/GUIDE_CORE.md` §7 의 PDF 변환 운영 규칙에 따라 권고 메시지를 출력한다.

```text
[PDF 변환 권고] marker 변환은 수 분 이상 걸리는 배치 작업이다.
지금 바로 돌리기보다 다음 타이밍에 한 번에 처리하기를 권장한다:
  - 점심시간 시작 직전 또는 퇴근 직전
  - 신규 PDF 가 3 개 이상 쌓였을 때
  - 마지막 변환 이후 24 시간 이상 지났을 때
지금 바로 실행이 필요하면 "지금 변환" 이라고 답해 달라.
```

### Step 4 — 사용자 동의 확인

- "지금 변환" / "배치 무시" / "바로 돌려" → Step 5 진행
- 동의 없음 → 변환 보류, 종료

### Step 5 — 변환 실행

```bash
python system-scripts/convert_pdfs.py
```

스크립트는 idempotent — 이미 변환된 파일은 자동으로 건너뛴다.

**첫 실행 주의**: marker 모델 가중치를 처음 다운로드하는 경우 추가 시간이 든다 (수백 MB, 5~10 분). Step 1-C 에서 이미 사용자에게 안내했어야 한다.

### Step 6 — 결과 보고

스크립트 출력의 마지막 한 줄 `[done] total=N skipped=K failed=L` 을 사용자에게 그대로 전달한다. 실패 파일이 있으면 파일명 목록도 같이 보고한다.

## 금지

- `references/md/` 의 결과 markdown 을 직접 수정 (다음 변환 때 덮어써짐)
- 가상환경 활성화 없이 `pip install -e .` 강행 (시스템 python 오염)
- 배치 권고 없이 즉시 변환 실행
- 사용자 동의 없는 force 실행 또는 force 설치
- 인자 없이 호출됐다는 이유로 "변환할 게 있는지 모르겠다" 로 종료 — Step 2 탐지는 항상 자동 수행
