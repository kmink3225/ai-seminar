---
description: 내부 문서 근거 기반 질의응답
---

프로젝트 하네싱 체인에 따라 작업한다.

## 실행 순서

1. `GUIDE.md` 를 Read 로 읽는다 (라우팅 테이블).
2. `guides/GUIDE_CORE.md` 를 Read 로 읽는다 (공통 규칙).
3. `guides/qa.md` 를 Read 로 읽는다 (skill).
4. qa.md 의 Step 1~5 를 **순서대로** 실행한다.
   - Step 1: 쿼리 핵심어 분해 (동의어·영문 포함)
   - Step 2: `references/md/`, `topics/` 2 개 레이어 병렬 Grep
   - Step 3: 근거 충분성 판정 (부족하면 종료하고 보고)
   - Step 4: 결론 → 근거(path:line) → 한계 구조로 답변 작성
   - Step 5: 추가 읽을거리 2~3 건 링크 제시
5. 답변 전 `guides/GUIDE_CORE.md` §5 Self-Check 를 출력한다.

## 질문

$ARGUMENTS
