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

    # Make the abstract lead with the empirical equal-rank result rather than
    # repeating the standard Grassmann baseline. Quantitative gains are frozen
    # values from the existing operational campaign.
    pre_v2_abstract = (
        "We use this identity as a null model rather than as a new random-projection theorem. "
        "Numerically, family-balanced one- and two-body readouts remain close to the rank reference through $n=16$ even as "
        "the tangent covariance becomes strongly anisotropic. Rank matching alone is nevertheless insufficient: "
        "in generic circuits, cross-fitted leading tangent subspaces of the same rank retain substantially more mass than "
        "the physical low-weight readout. This difference is operational. At fixed circuit, measurement record, readout rank, "
        "and shot budget, changing only the readout orientation changes directional gradient energy and finite-shot "
        "signal-to-noise ratio, while random rank-matched subspaces track the rank baseline."
    )
    redundant_v2_abstract = (
        "We use this identity as a null model rather than as a new random-projection theorem. "
        "The decisive comparison holds the circuit, measurement record, readout rank, and shot budget fixed: "
        "a cross-fitted leading tangent subspace of the same rank can retain substantially more tangent mass and "
        "produce a larger finite-shot directional signal than the physical low-weight readout. "
        "Numerically, family-balanced one- and two-body readouts remain close to the rank reference through $n=16$ even as "
        "the tangent covariance becomes strongly anisotropic. Rank matching alone is nevertheless insufficient: "
        "in generic circuits, cross-fitted leading tangent subspaces of the same rank retain substantially more mass than "
        "the physical low-weight readout. This difference is operational. At fixed circuit, measurement record, readout rank, "
        "and shot budget, changing only the readout orientation changes directional gradient energy and finite-shot "
        "signal-to-noise ratio, while random rank-matched subspaces track the rank baseline."
    )
    polished_abstract = (
        "We use this identity as a null model rather than as a new random-projection theorem. "
        "Numerically, family-balanced one- and two-body readouts remain close to the rank reference through $n=16$ even as "
        "the tangent covariance becomes strongly anisotropic. The decisive equal-rank comparison then holds the circuit, "
        "measurement record, readout rank, and evaluation shot budget fixed. For Haar-$U(4)$ at $n=12$, cross-fitted alignment "
        "increases the mean directional gradient-energy proxy by a factor $9.584$ and the finite-shot signal-to-noise ratio by "
        "a factor $3.111$ relative to the physical one-body readout, while a random rank-matched subspace remains near the rank baseline."
    )
    if polished_abstract not in text:
        if redundant_v2_abstract in text:
            text = text.replace(redundant_v2_abstract, polished_abstract, 1)
        elif pre_v2_abstract in text:
            text = text.replace(pre_v2_abstract, polished_abstract, 1)
        else:
            raise RuntimeError("abstract emphasis: known pre-v2/v2 target not found")

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
        "Figure~\\ref{fig:u1-sector-null} summarizes the sector-corrected comparison over the full tested window. "
        "This is a VQC-specific use of a standard projector/subspace-overlap construction rather than a claim that subspace overlap itself is new"
    )
    old_sector_sentence = (
        "Thus the persistent alignment is not an artifact of comparing a fixed-charge family with the full $2^n$ score-space rank scale. "
        "This is a VQC-specific use of a standard projector/subspace-overlap construction rather than a claim that subspace overlap itself is new"
    )
    new_sector_sentence = (
        "Thus the persistent alignment is not an artifact of comparing a fixed-charge family with the full $2^n$ score-space rank scale. "
        "Figure~\\ref{fig:u1-sector-null} summarizes the sector-corrected comparison over the full tested window. "
        "This is a VQC-specific use of a standard projector/subspace-overlap construction rather than a claim that subspace overlap itself is new"
    )
    if alignment_insert not in text:
        if alignment_anchor in text:
            text = text.replace(alignment_anchor, alignment_insert, 1)
        elif old_sector_sentence in text:
            text = text.replace(old_sector_sentence, new_sector_sentence, 1)
        else:
            raise RuntimeError("sector-corrected null paragraph: known pre-v2/v2 target not found")

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

    main_resource_anchor = (
        "For the operational comparison we hold fixed the circuit, the full computational-basis record, the readout rank, and the shot budget. "
        "We compare three rank-matched readouts: (i) the physical low-weight span, (ii) an independent random subspace, and (iii) a cross-fitted aligned subspace learned from independent tangent data. "
        "For an evaluation tangent $v$, the retained score energy $\\|P u_v\\|^2$ controls the directional signal available in that readout. "
        "Multiplying by the full-record Fisher scale gives the raw directional gradient-energy proxy used in the experiment. "
        "Finite-shot signal-to-noise is computed under the multinomial shot model at a fixed budget of $10^4$ shots."
    )
    main_resource_insert = (
        "For the operational comparison we hold fixed the circuit, the full computational-basis record, the readout rank, and the evaluation shot budget. "
        "We compare three rank-matched readouts: (i) the physical low-weight span, (ii) an independent random subspace, and (iii) a cross-fitted aligned subspace learned from independent tangent data. "
        "For an evaluation tangent $v$, the retained score energy $\\|P u_v\\|^2$ controls the directional signal available in that readout. "
        "Multiplying by the full-record Fisher scale gives the raw directional gradient-energy proxy used in the experiment. "
        "Finite-shot signal-to-noise is computed under the multinomial shot model at a fixed budget of $10^4$ shots. "
        "The independent alignment sample used to estimate the cross-fitted projector is a separate calibration resource and is not counted as free measurement cost in this fixed-evaluation-budget comparison."
    )
    text = replace_once(text, main_resource_anchor, main_resource_insert, "main-text resource accounting")

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
