---
name: convert-pdf
type: skill
version: 1.4
description: references/pdfs/ 의 PDF 를 marker 로 references/md/ 에 변환. 첫 실행 시 기존 환경 자동 발견 → 없으면 poetry 로 자동 설치까지 한 번에. 인자로 파일/폴더 지정 가능.
---

# convert-pdf — PDF → MD 변환

## 목적

`references/pdfs/` 에 누적된 PDF 를 `marker` 로 `references/md/` 에 markdown 으로 변환한다. 이미 변환된 파일은 건너뛴다 (idempotent).

이 스킬은 **프로그래밍 미경험자도 `/convert-pdf` 한 줄로 끝까지 도달** 하도록 설계됐다.

- 이미 marker 가 깔린 환경이 있으면 자동으로 발견해 재사용
- 없으면 사용자 동의 1 회 후 poetry 로 자동 셋업 (가상환경 + 의존성 설치 일괄)
- 모든 단계는 "이미 있는가?" 를 먼저 검사 → 있으면 스킵

호출 인자에 따라 두 가지 모드로 동작한다.

- **인자 없음** → `references/pdfs/` 전체 (배치 모드)
- **인자 있음** (파일·폴더 경로, 여러 개 혼합 가능) → 지정 대상만 (선택 모드)

## Step

### Step 1 — 환경 자동 부트스트랩

목표: 변환 가능한 python 경로 (`PYTHON_BIN`) 를 결정한다. 이미 설치된 게 있으면 즉시 통과, 없으면 poetry 로 자동 생성. 단계는 빠른 경로부터 차례로 시도한다.

#### 1-A. 현재 셸에서 marker 가 작동하는가 (가장 빠른 통과)

```bash
marker_single --help
```

종료 코드 0 → `PYTHON_BIN` = 현재 셸의 python (`python` 또는 `sys.executable`). Step 2 로.

#### 1-B. 다른 환경에 marker 가 이미 깔려 있는가

현재 PATH 에 없어도 다른 가상환경에 깔려 있을 수 있다. 다음을 차례로 검사한다.

1. **poetry env** (이 프로젝트 기준):
   ```bash
   poetry env info -p
   ```
   출력이 있으면 그 경로의 python (`<env>/Scripts/python.exe` 또는 `<env>/bin/python`) 으로 `python -c "import marker"` 시도
2. **프로젝트 로컬 venv**:
   - Windows: `.venv\Scripts\python.exe`
   - Unix: `.venv/bin/python`
3. **conda envs**:
   - `conda env list --json` 으로 모든 env 경로 나열 (conda 가용 시에만)
   - 각 env 의 python 으로 `python -c "import marker"` 시도

발견 시 사용자에게 한 줄로 보고:

```text
[env] 기존 환경 발견: C:\...\miniconda3\envs\blog\Scripts\python.exe (marker 설치됨, 재사용)
```

→ Step 1-D 로.

발견되지 않으면 → Step 1-C 로.

#### 1-C. poetry 로 자동 셋업 (사용자 동의 1 회)

##### 1-C-pre. poetry 설치 확인

```bash
poetry --version
```

작동하지 않으면 사용자에게 다음 메시지로 설치 안내:

```text
[poetry 설치 권고] 의존성 관리는 poetry 로 한다. 현재 머신에 poetry 가 없다.
다음 중 한 가지로 설치한다:

  pipx install poetry            (pipx 가 있으면 권장)
  python -m pip install --user poetry  (pipx 가 없을 때)

설치를 진행하려면 "pipx" 또는 "pip" 로 답해 달라.
```

- "pipx" → `pipx install poetry` 실행
- "pip" → `python -m pip install --user poetry` 실행
- 동의 없음 → 종료

설치 후 `poetry --version` 재검증. 실패 시 에러 보고하고 종료.

##### 1-C-main. 의존성 설치

```text
[자동 셋업 안내] poetry 로 가상환경과 의존성을 한 번에 설치한다.

  poetry install
    → 가상환경 자동 생성 (없으면)
    → marker-pdf (>=1.10.0) 등 의존성 설치 (수십 MB, 1~3 분)

이후 첫 변환 시 모델 가중치 다운로드 (수백 MB, 5~10 분).
총 약 10~15 분 소요. 진행하려면 "설치" 또는 "go" 라고 답해 달라.
```

동의 후:

```bash
poetry install
```

설치 완료 후 PYTHON_BIN 결정:

```bash
# poetry env 의 python 경로 추출
poetry env info -p
```

- Windows: `<env>\Scripts\python.exe`
- Unix: `<env>/bin/python`

또는 모든 후속 호출에 `poetry run` prefix 사용:

```bash
poetry run python system-scripts/convert_pdfs.py [args]
```

설치 후 `poetry run python -c "import marker"` 로 재검증. 실패 시 에러 그대로 보고하고 종료.

#### 1-D. 모델 가중치 안내

PYTHON_BIN 이 결정되었다. 단, marker 가 모델 가중치를 다운로드한 적이 있는지 스킬은 알 수 없다. 첫 변환 시점에 자동 다운로드되며, 이때 5~10 분 추가 소요될 수 있음을 미리 안내한다.

### Step 2 — 미변환 PDF 탐지

사용자 호출에 인자가 있는지 확인한다.

- **인자 없음** → `references/pdfs/` 전체를 대상
- **인자 있음** (파일 또는 폴더 경로, 여러 개 가능) → 그 대상만. 폴더는 rglob 으로 펼친다. 상대경로는 현재 디렉토리 기준 → 실패 시 `references/pdfs/` 기준으로 한 번 더 시도

대상 PDF 목록에 대해:

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

선택 모드 (소수 파일 변환) 일 때는 권고 메시지를 1 줄로 줄여도 된다.

### Step 4 — 사용자 동의 확인

- "지금 변환" / "배치 무시" / "바로 돌려" → Step 5 진행
- 동의 없음 → 변환 보류, 종료

### Step 5 — 변환 실행

Step 1 에서 결정한 `PYTHON_BIN` 으로 스크립트를 호출한다. 사용자 인자도 그대로 전달.

```bash
# 1-A 통과: 현재 셸 python 사용
python system-scripts/convert_pdfs.py [사용자 인자]

# 1-B 발견: 그 환경의 python 직접 호출 (셸 활성화 불필요)
<conda-prefix>\envs\blog\Scripts\python.exe system-scripts/convert_pdfs.py [args]
# 또는
conda run -n blog python system-scripts/convert_pdfs.py [args]

# 1-C 새 셋업 (poetry): poetry run 사용
poetry run python system-scripts/convert_pdfs.py [사용자 인자]
```

스크립트는 idempotent — 이미 변환된 파일은 자동으로 건너뛴다.

**첫 실행 주의**: marker 모델 가중치를 처음 다운로드하는 경우 추가 시간이 든다 (수백 MB, 5~10 분). Step 1-D 에서 이미 사용자에게 안내했어야 한다.

### Step 6 — 결과 보고

스크립트 출력의 마지막 한 줄 `[done] total=N skipped=K failed=L (output: <path>)` 를 사용자에게 그대로 전달한다. 출력 위치는 항상 `references/md/` 다 (`[output_dir]` 메시지로도 확인됨). 실패 파일이 있으면 파일명 목록도 같이 보고한다. 잘못된 경로 인자가 있었던 경우 `[error] 경로 없음: ...` 메시지도 함께 정리해 보고한다.

## 금지

- `references/md/` 의 결과 markdown 을 직접 수정 (다음 변환 때 덮어써짐)
- 사용자 동의 없이 poetry 자동 설치 또는 `poetry install` 실행 (자동 셋업은 1-C-pre·1-C-main 의 명시 동의 후에만)
- 시스템 python 에 marker 직접 설치 (`pip install marker-pdf` 강행 금지) — poetry 가 가상환경 격리를 담당
- 배치 권고 없이 즉시 변환 실행
- 인자가 없다는 이유로 "변환할 게 있는지 모르겠다" 로 종료 — 인자 없음은 "전체 모드" 의 정상 입력
- 1-B 의 기존 환경 검색을 건너뛰고 1-C 새 셋업으로 직행 (이미 깔린 환경 재사용이 우선)
