"""references/pdfs/ 의 PDF 를 references/md/ 로 변환.

변환 결과는 **항상** references/md/<pdf_stem>/<pdf_stem>.md 에 저장된다.
입력 PDF 의 위치와 무관 — 인자로 어디의 PDF 를 지정하든 출력은
references/md/ 한 곳에 모인다.

사용법:
  python system-scripts/convert_pdfs.py
    -> references/pdfs/ 전체 (기본)

  python system-scripts/convert_pdfs.py papers/foo.pdf
    -> 단일 파일

  python system-scripts/convert_pdfs.py references/pdfs/sub/
    -> 특정 폴더 (rglob 으로 *.pdf 모두)

  python system-scripts/convert_pdfs.py a.pdf b.pdf c/
    -> 여러 인자 혼합

상대경로는 현재 디렉토리 기준이며, 그 경로가 없으면
references/pdfs/ 기준 상대경로로도 한 번 더 시도한다.
이미 변환된 파일은 건너뜀 (idempotent).
"""

from __future__ import annotations

import argparse
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
    out = MD_DIR / pdf.stem / f"{pdf.stem}.md"
    print(f"[convert] {pdf.name} -> {out.relative_to(ROOT)}")
    cmd = [
        "marker_single",
        str(pdf),
        "--output_dir",
        str(MD_DIR),
        "--output_format",
        "markdown",
    ]
    return subprocess.run(cmd, check=False).returncode


def resolve_target(arg: str) -> Path | None:
    """인자를 절대 경로로 해석. 현재 디렉토리 -> PDF_DIR 순으로 시도."""
    p = Path(arg)
    if p.exists():
        return p.resolve()
    alt = PDF_DIR / arg
    if alt.exists():
        return alt.resolve()
    return None


def collect_pdfs(targets: list[str]) -> list[Path]:
    """인자 목록을 PDF 파일 경로 목록으로 펼친다.

    인자가 비어 있으면 PDF_DIR 전체 rglob.
    파일 인자는 그대로, 폴더 인자는 rglob *.pdf 로 펼친다.
    .pdf 가 아닌 파일은 무시하고 경고만 출력한다.
    """
    if not targets:
        return sorted(PDF_DIR.rglob("*.pdf"))

    pdfs: list[Path] = []
    for arg in targets:
        target = resolve_target(arg)
        if target is None:
            print(f"[error] 경로 없음: {arg}")
            continue
        if target.is_file():
            if target.suffix.lower() != ".pdf":
                print(f"[error] PDF 아님: {target}")
                continue
            pdfs.append(target)
        elif target.is_dir():
            pdfs.extend(sorted(target.rglob("*.pdf")))
        else:
            print(f"[error] 처리 불가: {target}")
    # 중복 제거 + 정렬
    return sorted(set(pdfs))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="references/pdfs/ 의 PDF 를 marker 로 references/md/ 에 변환",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="변환할 PDF 파일 또는 폴더 경로 (생략 시 references/pdfs/ 전체)",
    )
    args = parser.parse_args()

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    MD_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[output_dir] {MD_DIR}")

    pdfs = collect_pdfs(args.targets)
    if not pdfs:
        print("[info] 변환할 PDF 없음")
        return 0

    skipped = 0
    failed: list[str] = []
    for pdf in pdfs:
        if already_converted(pdf):
            skipped += 1
            continue
        if convert(pdf) != 0:
            failed.append(pdf.name)

    print(
        f"\n[done] total={len(pdfs)} skipped={skipped} failed={len(failed)} "
        f"(output: {MD_DIR})"
    )
    for f in failed:
        print(f"  - FAILED: {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
