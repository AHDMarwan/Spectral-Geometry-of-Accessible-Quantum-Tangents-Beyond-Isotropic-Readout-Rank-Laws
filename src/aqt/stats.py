from __future__ import annotations

import numpy as np
import pandas as pd


def bootstrap_mean_ci(values, seed: int, n_resamples: int = 5000, confidence: float = 0.95):
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return np.nan, np.nan, np.nan
    if len(x) == 1:
        return float(x[0]), np.nan, np.nan
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_resamples, len(x)))
    means = x[idx].mean(axis=1)
    alpha = (1.0 - confidence) / 2.0
    return float(x.mean()), float(np.quantile(means, alpha)), float(np.quantile(means, 1 - alpha))


def stratified_bootstrap_mean_ci(
    frame: pd.DataFrame,
    value_col: str,
    strata_col: str,
    seed: int,
    n_resamples: int = 5000,
    confidence: float = 0.95,
):
    groups = [g[value_col].to_numpy(float) for _, g in frame.groupby(strata_col)]
    groups = [x[np.isfinite(x)] for x in groups if len(x)]
    if not groups:
        return np.nan, np.nan, np.nan
    observed = float(np.mean(np.concatenate(groups)))
    rng = np.random.default_rng(seed)
    means = np.empty(n_resamples)
    for b in range(n_resamples):
        pieces = [rng.choice(x, size=len(x), replace=True) for x in groups]
        means[b] = np.mean(np.concatenate(pieces))
    alpha = (1.0 - confidence) / 2.0
    return observed, float(np.quantile(means, alpha)), float(np.quantile(means, 1 - alpha))


def bootstrap_ratio_ci(
    numerator,
    denominator,
    seed: int,
    n_resamples: int = 5000,
    confidence: float = 0.95,
):
    a = np.asarray(numerator, float)
    b = np.asarray(denominator, float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    ratios = np.empty(n_resamples)
    for i in range(n_resamples):
        aa = rng.choice(a, len(a), replace=True).mean()
        bb = rng.choice(b, len(b), replace=True).mean()
        ratios[i] = aa / bb
    observed = float(a.mean() / b.mean())
    alpha = (1 - confidence) / 2
    return observed, float(np.quantile(ratios, alpha)), float(np.quantile(ratios, 1 - alpha))
