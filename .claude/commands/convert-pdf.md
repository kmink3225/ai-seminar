---
description: references/pdfs/ 의 PDF 를 references/md/ 로 marker 변환 (첫 실행 시 의존성 자동 설치)
---

프로젝트 하네싱 체인에 따라 작업한다.

## 실행 순서

1. `GUIDE.md` 를 Read 로 읽는다 (라우팅 테이블).
2. `guides/GUIDE_CORE.md` 를 Read 로 읽는다 (공통 규칙).
3. `guides/convert-pdf.md` 를 Read 로 읽는다 (skill).
4. convert-pdf.md 의 Step 1~6 을 **순서대로** 실행한다.
   - Step 1: 환경 점검 — `marker_single --help` 로 설치 확인. 미설치 시 가상환경 검사 → 의존성 설치 (`pip install -e .`, 사용자 동의 후) → 재검증. 첫 변환 시 모델 가중치 (수백 MB) 다운로드를 사용자에게 미리 안내
   - Step 2: 미변환 PDF 탐지·보고 (없으면 즉시 종료)
   - Step 3: 배치 권고 메시지 출력 (`GUIDE_CORE.md` §7)
   - Step 4: 사용자 동의 확인 ("지금 변환" / "배치 무시" / "바로 돌려")
   - Step 5: `python system-scripts/convert_pdfs.py` 실행
   - Step 6: 결과 보고 (`[done] total=N skipped=K failed=L` + 실패 목록)
5. 보고 전 `guides/GUIDE_CORE.md` §5 Self-Check 를 출력한다.

## 인자

이 스킬은 인자를 받지 않는다. `/convert-pdf` 만 호출하면 된다.
