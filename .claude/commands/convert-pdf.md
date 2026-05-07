---
description: PDF → MD 변환. /convert-pdf 한 줄로 환경 자동 부트스트랩 (기존 환경 재사용, 없으면 poetry 로 자동 셋업) + 변환까지 진행. 인자로 파일/폴더 지정 가능.
---

프로젝트 하네싱 체인에 따라 작업한다.

## 실행 순서

1. `GUIDE.md` 를 Read 로 읽는다 (라우팅 테이블).
2. `guides/GUIDE_CORE.md` 를 Read 로 읽는다 (공통 규칙).
3. `guides/convert-pdf.md` 를 Read 로 읽는다 (skill).
4. convert-pdf.md 의 Step 1~6 을 **순서대로** 실행한다.
   - Step 1: 환경 자동 부트스트랩 (poetry 통일) — 1-A 현재 셸에서 marker 작동? → 1-B `poetry env info -p` 로 기존 poetry env 검사 (있으면 재사용) → 1-C 없으면 사용자 동의 1 회 후 poetry 자동 설치 (필요 시 1-C-pre 에서 poetry 자체도 설치) + `poetry install` 로 가상환경·의존성 일괄 → 1-D 모델 가중치 안내. 결정된 python 경로를 `PYTHON_BIN` 으로 저장
   - Step 2: 미변환 PDF 탐지 — 인자 없으면 `references/pdfs/` 전체, 인자 있으면 해당 파일/폴더만
   - Step 3: 배치 권고 메시지 출력 (`GUIDE_CORE.md` §7)
   - Step 4: 사용자 동의 확인 ("지금 변환" / "배치 무시" / "바로 돌려")
   - Step 5: `<PYTHON_BIN> system-scripts/convert_pdfs.py $ARGUMENTS` 실행 (또는 `poetry run python ...`) — Step 1 의 PYTHON_BIN 으로 호출, 사용자 인자 그대로 전달
   - Step 6: 결과 보고 (`[done] total=N skipped=K failed=L (output: ...)` + 실패 목록 + 경로 에러)
5. 보고 전 `guides/GUIDE_CORE.md` §5 Self-Check 를 출력한다.

## 인자

이 스킬은 선택적 인자를 받는다.

- **인자 없음** (`/convert-pdf`) → `references/pdfs/` 전체 변환
- **파일 경로** (`/convert-pdf paper.pdf`) → 해당 파일 1 개만 변환
- **폴더 경로** (`/convert-pdf references/pdfs/sub/`) → 해당 폴더 안 모든 PDF
- **여러 개 혼합** (`/convert-pdf a.pdf b.pdf sub/`) → 모두 한 번에

상대경로는 현재 디렉토리 기준 → 실패 시 `references/pdfs/` 기준으로도 시도된다.

사용자가 전달한 인자:

```text
$ARGUMENTS
```
