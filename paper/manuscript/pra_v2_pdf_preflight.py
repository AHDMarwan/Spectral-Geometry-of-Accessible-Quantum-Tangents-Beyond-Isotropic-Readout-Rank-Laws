from __future__ import annotations

"""Automated render/preflight checks for the PRA-v2 canonical manuscript PDF.

This is deliberately a technical QA gate, not a substitute for human visual review.
It checks that the PDF can be rendered, has embedded fonts, has no nearly blank
pages, and has no rasterized ink touching the physical page boundary.
"""

import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "paper" / "manuscript" / "spectral_geometry_rewrite.pdf"
LOG = ROOT / "paper" / "manuscript" / "spectral_geometry_rewrite.log"
REPORT = ROOT / "paper" / "manuscript" / "PRA_V2_PDF_PREFLIGHT.md"


def run(*args: str) -> str:
    p = subprocess.run(args, check=True, text=True, capture_output=True)
    return p.stdout


def parse_page_count(pdfinfo: str) -> int:
    m = re.search(r"^Pages:\s+(\d+)\s*$", pdfinfo, re.MULTILINE)
    if not m:
        raise RuntimeError("could not parse page count from pdfinfo")
    return int(m.group(1))


def check_fonts(pdf: Path) -> tuple[int, list[str]]:
    out = run("pdffonts", str(pdf))
    lines = out.splitlines()
    if len(lines) < 2:
        raise RuntimeError("pdffonts returned no font table")

    header_idx = next((i for i, line in enumerate(lines) if "emb" in line and "sub" in line), None)
    if header_idx is None:
        raise RuntimeError("could not locate pdffonts header")
    header = lines[header_idx]
    emb_start = header.index("emb")
    sub_start = header.index("sub", emb_start + 3)

    font_lines = [line for line in lines[header_idx + 2 :] if line.strip()]
    not_embedded = []
    for line in font_lines:
        emb = line[emb_start:sub_start].strip().lower()
        if emb != "yes":
            not_embedded.append(line.rstrip())
    return len(font_lines), not_embedded


def page_metrics(path: Path) -> dict[str, float | int]:
    with Image.open(path) as im:
        gray = im.convert("L")
        w, h = gray.size
        pix = gray.load()
        threshold = 248

        xs: list[int] = []
        ys: list[int] = []
        dark = 0
        border_dark = 0
        border = 3
        for y in range(h):
            for x in range(w):
                if pix[x, y] < threshold:
                    dark += 1
                    xs.append(x)
                    ys.append(y)
                    if x < border or x >= w - border or y < border or y >= h - border:
                        border_dark += 1

        if dark == 0:
            return {
                "width": w,
                "height": h,
                "ink_fraction": 0.0,
                "border_dark": 0,
                "left_margin": w,
                "right_margin": w,
                "top_margin": h,
                "bottom_margin": h,
            }

        return {
            "width": w,
            "height": h,
            "ink_fraction": dark / float(w * h),
            "border_dark": border_dark,
            "left_margin": min(xs),
            "right_margin": (w - 1) - max(xs),
            "top_margin": min(ys),
            "bottom_margin": (h - 1) - max(ys),
        }


def main() -> None:
    if not PDF.is_file() or PDF.stat().st_size == 0:
        raise RuntimeError(f"missing compiled PDF: {PDF}")

    info = run("pdfinfo", str(PDF))
    pages = parse_page_count(info)
    fonts, not_embedded = check_fonts(PDF)
    if not_embedded:
        raise RuntimeError("non-embedded fonts detected:\n" + "\n".join(not_embedded))

    if LOG.exists():
        log_text = LOG.read_text(encoding="utf-8", errors="replace")
        overfull = [line for line in log_text.splitlines() if "Overfull" in line]
        undefined = [
            line
            for line in log_text.splitlines()
            if "undefined citations" in line.lower() or "undefined references" in line.lower()
        ]
    else:
        overfull = []
        undefined = []

    if undefined:
        raise RuntimeError("undefined citation/reference warnings remain in LaTeX log")

    with tempfile.TemporaryDirectory(prefix="pra-v2-render-") as td:
        prefix = Path(td) / "page"
        subprocess.run(
            ["pdftoppm", "-png", "-r", "120", str(PDF), str(prefix)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        images = sorted(Path(td).glob("page-*.png"))
        if len(images) != pages:
            raise RuntimeError(f"rendered {len(images)} pages but pdfinfo reports {pages}")

        metrics = [page_metrics(p) for p in images]

    blankish = [i + 1 for i, m in enumerate(metrics) if float(m["ink_fraction"]) < 0.00035]
    boundary_touch = [i + 1 for i, m in enumerate(metrics) if int(m["border_dark"]) > 0]
    min_margin = min(
        min(int(m[k]) for k in ("left_margin", "right_margin", "top_margin", "bottom_margin"))
        for m in metrics
    )

    if blankish:
        raise RuntimeError(f"nearly blank rendered pages detected: {blankish}")
    if boundary_touch:
        raise RuntimeError(f"ink touches the outer 3-pixel page boundary on pages: {boundary_touch}")
    if min_margin < 6:
        raise RuntimeError(f"minimum rendered ink margin is only {min_margin} pixels at 120 dpi")

    lines = [
        "# PRA v2 PDF automated preflight",
        "",
        "Status: PASS",
        "",
        f"- PDF: `{PDF.relative_to(ROOT)}`",
        f"- Pages: {pages}",
        f"- File size: {PDF.stat().st_size:,} bytes",
        f"- Fonts reported by `pdffonts`: {fonts}; all embedded.",
        f"- Rendered pages checked at 120 dpi: {pages}",
        f"- Minimum raster ink margin: {min_margin} px",
        f"- Nearly blank pages: none",
        f"- Ink touching outer 3-pixel page boundary: none",
        f"- LaTeX overfull-box warnings: {len(overfull)}",
        "",
        "This automated preflight checks renderability, font embedding, gross clipping/boundary contact, and blank-page anomalies. It does not replace a human page-by-page visual inspection for caption wrapping, legend collisions, or aesthetic readability.",
    ]
    if overfull:
        lines += ["", "## Overfull-box warnings", ""]
        lines.extend(f"- `{line.strip()}`" for line in overfull[:30])

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
