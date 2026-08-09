from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import beta, kstest


def run_isotropic_controls(output_dir: str | Path, seed: int = 20260809, samples: int = 30000):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    rows = []
    for d, r in [(31, 5), (63, 8), (255, 10)]:
        g = rng.normal(size=(samples, d))
        g /= np.linalg.norm(g, axis=1, keepdims=True)
        x = np.sum(g[:, :r] ** 2, axis=1)
        a, b = r / 2.0, (d - r) / 2.0
        ks = kstest(x, beta(a, b).cdf)
        rows.append(
            {
                "control": "rank_projector_beta",
                "d": d,
                "r": r,
                "samples": samples,
                "mean_empirical": float(x.mean()),
                "mean_exact": r / d,
                "var_empirical": float(x.var(ddof=1)),
                "var_exact": float(beta(a, b).var()),
                "ks_statistic": float(ks.statistic),
                "ks_pvalue": float(ks.pvalue),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(out / "isotropic_beta_controls.csv", index=False)
    (out / "control_metadata.json").write_text(
        json.dumps({"seed": seed, "samples": samples}, indent=2), encoding="utf-8"
    )
    return df
