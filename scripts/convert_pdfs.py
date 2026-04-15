"""references/pdfs/ 의 신규 PDF를 references/md/ 로 변환.

이미 변환된 파일은 건너뜀 (idempotent).
사용법: python scripts/convert_pdfs.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "references" / "pdfs"
MD_DIR = ROOT / "references" / "md"


def already_converted(pdf: Path) -> bool:
    # marker_single 은 <md_dir>/<pdf_stem>/<pdf_stem>.md 형태로 출력
    return (MD_DIR / pdf.stem / f"{pdf.stem}.md").exists()


def convert(pdf: Path) -> int:
    print(f"[convert] {pdf.name}")
    cmd = [
        "marker_single",
        str(pdf),
        "--output_dir",
        str(MD_DIR),
        "--output_format",
        "markdown",
    ]
    return subprocess.run(cmd, check=False).returncode


def main() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    MD_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(PDF_DIR.rglob("*.pdf"))
    if not pdfs:
        print(f"[info] PDF 없음: {PDF_DIR}")
        return 0

    skipped = 0
    failed: list[str] = []
    for pdf in pdfs:
        if already_converted(pdf):
            skipped += 1
            continue
        if convert(pdf) != 0:
            failed.append(pdf.name)

    print(f"\n[done] total={len(pdfs)} skipped={skipped} failed={len(failed)}")
    for f in failed:
        print(f"  - FAILED: {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
