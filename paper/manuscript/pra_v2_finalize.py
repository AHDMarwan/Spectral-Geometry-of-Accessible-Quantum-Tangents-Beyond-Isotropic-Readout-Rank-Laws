from __future__ import annotations

"""Apply the referee-facing PRA v2 manuscript revision.

This pass is intentionally deterministic and idempotent. It does not alter any
numerical outcome. All inserted quantitative values are read from frozen
paper-facing data or frozen experiment profiles.
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "paper" / "manuscript" / "spectral_geometry_rewrite.tex"
SECTOR_NULL = ROOT / "paper" / "manuscript" / "data" / "pra_v2_u1_sector_null.csv"
BRIDGE_PROFILE = ROOT / "profiles" / "trainability_bridge_v1.json"
MARKER = "% PRA-V2-AUTOMATED-REVISION"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one replacement target, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")

    # Journal target: this revision is explicitly prepared as a PRA regular article.
    text = text.replace(
        r"\documentclass[aps,prx,reprint,superscriptaddress,nofootinbib,longbibliography]{revtex4-2}",
        r"\documentclass[aps,pra,reprint,superscriptaddress,nofootinbib,longbibliography]{revtex4-2}",
        1,
    )

    if MARKER not in text:
        text = text.replace("\\begin{document}\n", "\\begin{document}\n" + MARKER + "\n", 1)

    # Put the same-rank operational result before the reader can misidentify the
    # standard Grassmann identity as the novelty claim.
    abstract_anchor = (
        "We use this identity as a null model rather than as a new random-projection theorem."
    )
    abstract_insert = (
        abstract_anchor
        + " The decisive comparison holds the circuit, measurement record, readout rank, and shot budget fixed: "
        + "a cross-fitted leading tangent subspace of the same rank can retain substantially more tangent mass and "
        + "produce a larger finite-shot directional signal than the physical low-weight readout."
    )
    text = replace_once(text, abstract_anchor, abstract_insert, "abstract emphasis")

    null = pd.read_csv(SECTOR_NULL)
    n18 = null[null["n"] == 18].set_index("walsh_order")
    if not {1, 2}.issubset(n18.index):
        raise RuntimeError("sector-null table is missing n=18, k=1/2")
    mu1 = float(n18.loc[1, "sector_null_mean"])
    mu2 = float(n18.loc[2, "sector_null_mean"])
    ratio1 = float(n18.loc[1, "observed_over_null"])
    ratio2 = float(n18.loc[2, "observed_over_null"])

    alignment_anchor = (
        "to quantify how much of the leading tangent subspace lies in low-weight sectors. "
        "This is a VQC-specific use of a standard projector/subspace-overlap construction rather than a claim that subspace overlap itself is new"
    )
    alignment_insert = (
        "to quantify how much of the leading tangent subspace lies in low-weight sectors. "
        "A sector-corrected random-orientation control is available without assuming full-space isotropy. "
        "If $P_{\\rm top}$ is Haar-random inside the same half-filled centered score sector, then "
        "$\\mathbb E A_k=r_{\\le k}/N_{\\rm hf}$; its exact variance follows from Eq.~\\eqref{eq:exact-var} "
        "by setting $C=P_{\\le k}/r_{\\le k}$ and the random projector rank to $r_1$. "
        "At $n=18$ the corresponding null means are "
        f"${mu1:.3g}$ for $k=1$ and ${mu2:.3g}$ for $k\\le2$, while the observed overlaps are "
        f"approximately ${ratio1:.0f}\\times$ and ${ratio2:.0f}\\times$ larger, respectively. "
        "Thus the persistent alignment is not an artifact of comparing a fixed-charge family with the full $2^n$ score-space rank scale. "
        "This is a VQC-specific use of a standard projector/subspace-overlap construction rather than a claim that subspace overlap itself is new"
    )
    text = replace_once(text, alignment_anchor, alignment_insert, "sector-corrected null paragraph")

    figure_anchor = (
        "Each size uses 20 independent circuit instances \\cite{AitHaddou2026MeasurementAccessible}.\n\n"
        "Over the tested window $n=8$--$18$"
    )
    figure_block = (
        "Each size uses 20 independent circuit instances \\cite{AitHaddou2026MeasurementAccessible}.\n\n"
        "\\begin{figure*}[t]\n"
        "\\centering\n"
        "\\includegraphics[width=.95\\textwidth]{production/fig_u1_sector_null.pdf}\n"
        "\\caption{Sector-corrected random-orientation control for the half-filled $U(1)$ alignment statistic. "
        "The null draws the leading rank-$r_1$ subspace randomly inside the same half-filled centered score sector, "
        "rather than comparing with the full computational-basis score space. Points are the measured cross-fitted "
        "alignment means with circuit-bootstrap intervals; dashed curves are the exact random-orientation means and "
        "shaded bands show two null standard deviations from Grassmann projector moments. The observed alignment remains "
        "orders of magnitude above the sector null at the largest sizes.}\n"
        "\\label{fig:u1-sector-null}\n"
        "\\end{figure*}\n\n"
        "Over the tested window $n=8$--$18$"
    )
    text = replace_once(text, figure_anchor, figure_block, "sector-null figure")

    profile = json.loads(BRIDGE_PROFILE.read_text(encoding="utf-8"))
    align_tangents = int(profile["align_tangents"])
    eval_tangents = int(profile["eval_tangents"])
    shots = int(profile["shots"])
    fd_dirs = int(profile["fd_directions"])
    default_instances = int(profile["instances"]["default"])
    u1_instances = int(profile["instances"]["U1-RZ-XY-line"])

    crossfit_anchor = (
        "This separation prevents the same tangent samples from both selecting and evaluating the subspace.  "
        "By contrast, the same-sample Ky Fan quantity"
    )
    crossfit_insert = (
        "This separation prevents the same tangent samples from both selecting and evaluating the subspace. "
        "The frozen operational profile uses "
        f"{align_tangents} alignment tangents and {eval_tangents} independent evaluation tangents per circuit; "
        f"the generic Haar-$U(4)$ cells use {default_instances} circuits per size and the $U(1)$ cells use {u1_instances}, "
        f"with a ${shots:,}$-shot finite-shot evaluation model and {fd_dirs} held-out finite-difference directions. "
        "The alignment sample is therefore a separate calibration resource: the fixed-shot comparison isolates the "
        "effect of readout orientation at fixed evaluation resources, but it is not an end-to-end claim that learning "
        "the aligned projector is free. A hardware implementation should account separately for the shots or derivative "
        "queries required to estimate $P_{\\rm xfit}$.  By contrast, the same-sample Ky Fan quantity"
    )
    text = replace_once(text, crossfit_anchor, crossfit_insert, "cross-fit resource accounting")

    MANUSCRIPT.write_text(text, encoding="utf-8")
    print(f"updated {MANUSCRIPT}")


if __name__ == "__main__":
    main()
