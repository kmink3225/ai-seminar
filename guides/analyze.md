---
name: analyze
type: skill
version: 1.0
description: 단일 문서 분석·요약
---

# analyze — 문서 분석

## 목적

지정된 `.md` (또는 변환된 논문) 1 개를 깊게 읽고 **요약·핵심 포인트·한계** 를 뽑는다. 선택적으로 결과 문서를 생성한다.

## 입력

- `/analyze references/md/xxx/xxx.md`
- `/analyze papers/2024-xxx.md`

## Step

1. **파일 Read** — 전체 내용을 읽는다 (대용량이면 구간 분할).
2. **메타 추출** — 제목, 저자, 발표/출판 연도, 주제 카테고리 식별.
3. **구조 파악** — 섹션 목차를 뽑는다.
4. **핵심 포인트 5~8 개** — 문서의 주장·기여·결과를 추출한다.
5. **방법 요약** — 접근법·실험 설정·데이터셋을 2~5 줄로 정리.
6. **한계·비판 포인트** — 저자가 밝힌 한계 + 독자 관점 추가 의문.
7. **적용 아이디어** — 팀 작업에 적용 가능한 시나리오 2~3 개.
8. **결과 저장 여부 확인** — 사용자에게 묻는다.
   - `papers/` 하위 → 논문 리뷰 파일 생성 (`YYYY-first-author-short-title.md`)
   - `sessions/<date>-<topic>/` 하위 → 세미나 준비 자료
   - 저장 안 함 → 채팅 응답만

## 출력 템플릿

```yaml
---
title: ...
source: references/md/xxx/xxx.md
authors: [...]
year: YYYY
tags: [...]
reviewed_by: ...
date: YYYY-MM-DD
---
```

```markdown
## 요약
(2~4 문장)

## 핵심 포인트
- …

## 방법
…

## 한계
- …

## 적용 아이디어
- …

## 원문 인용
- … (source:line)
```

## 금지

- 원문을 읽지 않고 제목·초록만으로 요약
- 이모지·수동 번호
