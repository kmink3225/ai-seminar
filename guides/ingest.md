---
name: ingest
type: skill
version: 1.0
description: PDF → MD 변환 파이프라인 실행
---

# ingest — PDF 변환

## 목적

`references/pdfs/` 의 신규 PDF 를 marker 로 `references/md/` 에 변환한다.

## Step

1. **환경 확인** — Python 3.10~3.13, `marker-pdf` 설치 여부.
   - 미설치 시 `pip install -e .` 안내.
2. **대상 목록 확인** — `references/pdfs/**/*.pdf` 개수와 `references/md/` 기존 변환물 개수 보고.
3. **스크립트 실행**
   ```bash
   python scripts/convert_pdfs.py
   ```
4. **결과 보고** — `total=N skipped=S failed=F`. 실패 파일명 나열.
5. **후속 제안** — 신규 변환 파일이 있으면 `/search` 또는 `/analyze` 대상으로 사용자 확인.

## 규칙

- `references/md/` 하위를 수작업 편집하지 않는다 (자동 재생성물).
- idempotent — 이미 변환된 파일은 건너뛴다 (스크립트가 처리).
- 대량 변환은 시간이 걸린다. 사용자에게 예상 규모 보고 후 진행.

## 금지

- `scripts/convert_pdfs.py` 우회하여 marker CLI 직접 호출 (경로 규약 깨짐)
- 실패 파일을 숨기고 성공만 보고
