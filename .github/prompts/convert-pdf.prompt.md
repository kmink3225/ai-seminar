---
mode: agent
description: PDF → MD 변환. /convert-pdf 한 줄로 환경 자동 부트스트랩 (기존 환경 재사용, 없으면 poetry 로 자동 셋업) + 변환까지 진행. 인자로 파일/폴더 지정 가능.
---

# /convert-pdf — PDF 일괄 변환

프로젝트 하네싱 체인에 따라 작업한다.

## 실행 순서

1. `../copilot-instructions.md` 를 읽는다 (Copilot 진입점).
2. `../../GUIDE.md` 를 읽는다 (라우팅 테이블).
3. `../../guides/GUIDE_CORE.md` 를 읽는다 (공통 규칙).
4. `../../guides/convert-pdf.md` 를 읽는다 (skill).
5. convert-pdf.md 의 Step 1~6 을 **순서대로** 실행한다.
   - Step 1: 환경 자동 부트스트랩 — 1-A 현재 셸 marker 작동? → 1-B 다른 poetry env·venv·conda env 검색 (있으면 재사용) → 1-C 없으면 사용자 동의 후 poetry 자동 설치 + `poetry install` 일괄 → 1-D 모델 가중치 안내. 결정된 python 을 PYTHON_BIN 으로 저장
   - Step 2: 미변환 PDF 탐지 — 인자 없으면 `references/pdfs/` 전체, 인자 있으면 해당 파일/폴더만
   - Step 3: 배치 권고 메시지 출력 (`GUIDE_CORE.md` §7)
   - Step 4: 사용자 동의 확인 ("지금 변환" / "배치 무시" / "바로 돌려")
   - Step 5: `<PYTHON_BIN> system-scripts/convert_pdfs.py [인자]` 실행 (또는 `poetry run python ...`) — Step 1 의 PYTHON_BIN 으로 호출, 사용자 입력 인자 그대로 전달
   - Step 6: 결과 보고 (`[done] total=N skipped=K failed=L (output: ...)` + 실패 목록 + 경로 에러)
6. 보고 전 `../../guides/GUIDE_CORE.md` §5 Self-Check 를 출력한다.

## 인자

이 스킬은 선택적 인자를 받는다.

- 인자 없음 → references/pdfs/ 전체 변환
- 파일 경로 → 해당 파일 1 개
- 폴더 경로 → 그 폴더 안 모든 PDF
- 여러 개 혼합 가능

사용자가 `/convert-pdf` 뒤에 입력한 텍스트를 그대로 스크립트 인자로 전달한다. 상대경로는 현재 디렉토리 → `references/pdfs/` 순으로 시도된다.
