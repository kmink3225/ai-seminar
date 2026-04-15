# References

외부 참고자료 아카이브. PDF는 marker로 Markdown 변환 후 검색/조회/분석에 사용.

## 구조

```
references/
├── pdfs/   # 원본 PDF 투입 위치
└── md/     # marker 변환 결과 (자동 생성)
    └── <pdf_stem>/
        ├── <pdf_stem>.md
        └── <이미지/메타>
```

## 사용 흐름

1. 새 PDF를 `references/pdfs/` 에 넣는다 (하위 폴더 가능)
2. 프로젝트 루트에서 변환 스크립트 실행

```bash
python scripts/convert_pdfs.py
```

- 이미 변환된 파일은 자동으로 건너뜀 (idempotent)
- 실패한 파일은 요약에 표시됨

## 최초 환경 설정

[프로젝트 루트 README](../README.md#환경-설정) 의 "환경 설정" 참조.

## 외부 링크 모음

PDF로 보관하지 않는 링크/블로그/강의는 아래에 추가.

- _항목 추가 예정_
