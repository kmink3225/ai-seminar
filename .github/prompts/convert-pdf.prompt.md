---
mode: agent
description: references/pdfs/ 의 PDF 를 references/md/ 로 marker 변환 (첫 실행 시 의존성 자동 설치)
---

# /convert-pdf — PDF 일괄 변환

프로젝트 하네싱 체인에 따라 작업한다.

## 실행 순서

1. `../copilot-instructions.md` 를 읽는다 (Copilot 진입점).
2. `../../GUIDE.md` 를 읽는다 (라우팅 테이블).
3. `../../guides/GUIDE_CORE.md` 를 읽는다 (공통 규칙).
4. `../../guides/convert-pdf.md` 를 읽는다 (skill).
5. convert-pdf.md 의 Step 1~6 을 **순서대로** 실행한다.
   - Step 1: 환경 점검 — marker 설치 확인, 미설치 시 가상환경 검사 후 `pip install -e .` (사용자 동의 후), 모델 가중치 안내
   - Step 2: 미변환 PDF 탐지·보고 (없으면 즉시 종료)
   - Step 3: 배치 권고 메시지 출력 (`GUIDE_CORE.md` §7)
   - Step 4: 사용자 동의 확인 ("지금 변환" / "배치 무시" / "바로 돌려")
   - Step 5: `python system-scripts/convert_pdfs.py` 실행
   - Step 6: 결과 보고 (`[done] total=N skipped=K failed=L` + 실패 목록)
6. 보고 전 `../../guides/GUIDE_CORE.md` §5 Self-Check 를 출력한다.

이 스킬은 인자를 받지 않는다. `/convert-pdf` 만 호출하면 된다.
