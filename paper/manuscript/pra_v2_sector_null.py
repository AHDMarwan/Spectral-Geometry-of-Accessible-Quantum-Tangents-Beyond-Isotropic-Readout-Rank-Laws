from __future__ import annotations

"""Build the half-filled-sector random-orientation null used by the PRA v2 revision.

For the cross-fitted leading rank-r1 tangent subspace P_top and a fixed
low-weight projector P_{<=k},

    A_k = Tr(P_{<=k} P_top) / r1.

If P_top is Haar-uniform inside the *same half-filled score sector*, then

    E[A_k] = r_{<=k} / N_hf,

with N_hf = binom(n,n/2)-1, r1=n-1 and r_{<=2}=binom(n,2)-1.
The exact variance follows from the Grassmann projector moment formula by
setting C=P_{<=k}/r_{<=k}.
"""

from math import comb, sqrt
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "paper" / "manuscript" / "data"
SUMMARY = DATA / "u1_alignment_scaling_summary.csv"
OUT_CSV = DATA / "pra_v2_u1_sector_null.csv"
OUT_MD = ROOT / "paper" / "manuscript" / "PRA_V2_SECTOR_NULL_AUDIT.md"


def sector_dimensions(n: int, walsh_order: int) -> tuple[int, int, int]:
    if n % 2:
        raise ValueError("half-filled sector requires even n")
    if walsh_order not in (1, 2):
        raise ValueError("this audit is defined for walsh_order 1 or 2")
    n_hf = comb(n, n // 2) - 1
    r1 = n - 1
    r_k = r1 if walsh_order == 1 else comb(n, 2) - 1
    if not (0 < r1 <= r_k < n_hf):
        raise ValueError((n, walsh_order, n_hf, r1, r_k))
    return n_hf, r1, r_k


def exact_null_moments(n: int, walsh_order: int) -> tuple[float, float]:
    n_hf, r1, r_k = sector_dimensions(n, walsh_order)
    mean = r_k / n_hf

    # Apply the manuscript's exact Grassmann formula to C=P_low/r_k.
    # For rho=A_k/mean, Tr(C^2)=1/r_k.
    var_rho = (
        2.0
        * (n_hf - r1)
        * (n_hf / r_k - 1.0)
        / (r1 * (n_hf - 1) * (n_hf + 2))
    )
    sd = mean * sqrt(max(var_rho, 0.0))
    return mean, sd


def build_table() -> pd.DataFrame:
    df = pd.read_csv(SUMMARY)
    d = df[
        (df["family"] == "U1-RZ-XY-line")
        & (df["metric"] == "cumulative_aligned_subspace_overlap")
        & (df["walsh_order"].isin([1, 2]))
    ].copy()
    if d.empty:
        raise RuntimeError("U(1) alignment summary rows not found")

    rows: list[dict] = []
    for row in d.itertuples(index=False):
        n = int(row.n)
        k = int(row.walsh_order)
        n_hf, r1, r_k = sector_dimensions(n, k)
        null_mean, null_sd = exact_null_moments(n, k)
        observed = float(row.mean)
        ci_low = float(row.ci_low)
        ci_high = float(row.ci_high)
        rows.append(
            {
                "n": n,
                "walsh_order": k,
                "N_hf": n_hf,
                "r_top": r1,
                "r_low": r_k,
                "observed_mean": observed,
                "observed_ci_low": ci_low,
                "observed_ci_high": ci_high,
                "sector_null_mean": null_mean,
                "sector_null_sd": null_sd,
                "observed_over_null": observed / null_mean,
                "ci_low_over_null": ci_low / null_mean,
                "null_plus_5sd": null_mean + 5.0 * null_sd,
            }
        )

    out = pd.DataFrame(rows).sort_values(["walsh_order", "n"]).reset_index(drop=True)

    # The paper's qualitative claim requires a very strong separation from the
    # sector-corrected orientation null at every reported size. Fail CI if that
    # invariant ever stops being true.
    if not (out["observed_ci_low"] > out["null_plus_5sd"]).all():
        bad = out[out["observed_ci_low"] <= out["null_plus_5sd"]]
        raise RuntimeError(
            "PRA-v2 sector-null separation failed for rows:\n" + bad.to_string(index=False)
        )
    return out


def write_markdown(df: pd.DataFrame) -> None:
    lines = [
        "# PRA v2: half-filled-sector random-orientation audit",
        "",
        "This audit compares the measured low-weight alignment with a random ",
        "rank-$r_1$ subspace drawn inside the **same half-filled score sector**.",
        "It therefore removes the ambiguity between a full $2^n$ score-space null ",
        "and the sector-corrected fixed-charge geometry.",
        "",
        "For $A_k=\\mathrm{Tr}(P_{\\le k}P_{\\rm top})/r_1$ the null mean is",
        "",
        "$$\\mathbb E A_k=r_{\\le k}/N_{\\rm hf},$$",
        "",
        "and the reported null standard deviation is obtained from the exact ",
        "Grassmann second moment used in the manuscript.",
        "",
        "| n | k | observed | 95% CI | sector null | null SD | observed/null |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in df.itertuples(index=False):
        lines.append(
            f"| {row.n:d} | {row.walsh_order:d} | {row.observed_mean:.6f} | "
            f"[{row.observed_ci_low:.6f}, {row.observed_ci_high:.6f}] | "
            f"{row.sector_null_mean:.6g} | {row.sector_null_sd:.3g} | "
            f"{row.observed_over_null:.1f}x |"
        )

    n18 = df[df["n"] == 18].set_index("walsh_order")
    if {1, 2}.issubset(n18.index):
        lines += [
            "",
            "At $n=18$ the one-body and cumulative-through-two alignments are ",
            f"{n18.loc[1, 'observed_over_null']:.0f}x and "
            f"{n18.loc[2, 'observed_over_null']:.0f}x their respective sector-null means.",
            "",
            "Interpretation: this is a geometric random-orientation control inside ",
            "the fixed-charge support. It does not identify the dynamical mechanism ",
            "responsible for the observed alignment.",
        ]

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    table = build_table()
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_CSV, index=False)
    write_markdown(table)
    print(table.to_string(index=False))
    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()
