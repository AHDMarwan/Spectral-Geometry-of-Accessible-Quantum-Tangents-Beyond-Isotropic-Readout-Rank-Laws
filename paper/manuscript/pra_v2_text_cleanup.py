from __future__ import annotations

"""Small idempotent prose cleanup for the PRA-v2 production manuscript."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "paper" / "manuscript" / "spectral_geometry_rewrite.tex"


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")

    duplicated = (
        "The source code, frozen experiment profiles, aggregate tables, shard-level outputs, and paper-facing result summaries used for the numerical claims are archived in the public reproducibility release \\cite{AitHaddou2026MeasurementAccessible}. "
        "The source code, frozen experiment profiles, aggregate tables, shard-level outputs, and paper-facing result summaries used for the numerical claims are archived in the public reproducibility repository \\cite{AitHaddou2026MeasurementAccessible}."
    )
    cleaned = (
        "The source code, frozen experiment profiles, aggregate tables, shard-level outputs, and paper-facing result summaries used for the numerical claims are archived in the public reproducibility repository \\cite{AitHaddou2026MeasurementAccessible}."
    )

    if duplicated in text:
        text = text.replace(duplicated, cleaned, 1)
    elif cleaned not in text:
        raise RuntimeError("reproducibility paragraph: expected source text not found")

    if text.count(cleaned) != 1:
        raise RuntimeError("reproducibility paragraph should occur exactly once")

    MANUSCRIPT.write_text(text, encoding="utf-8")
    print(f"cleaned {MANUSCRIPT}")


if __name__ == "__main__":
    main()
