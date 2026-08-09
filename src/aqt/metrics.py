from __future__ import annotations

from itertools import combinations

import numpy as np


def probability_tangent_batch(psi: np.ndarray, phis: np.ndarray):
    p = np.abs(psi) ** 2
    dp = 2 * np.real(np.conjugate(psi)[None, :] * phis)
    return p, dp


def _apply_binary_channel_batch(values: np.ndarray, channel: np.ndarray, q: int, n: int):
    m = values.shape[0]
    tensor = values.reshape((m,) + (2,) * n)
    moved = np.moveaxis(tensor, q + 1, 1)
    out = np.einsum("ab,mb...->ma...", channel, moved, optimize=True)
    out = np.moveaxis(out, 1, q + 1)
    return out.reshape(m, -1)


def apply_independent_bitflip_channel(
    p: np.ndarray, dp: np.ndarray, n: int, eta: float
) -> tuple[np.ndarray, np.ndarray]:
    """Exact classical readout bit-flip channel applied to p and all tangents."""
    if not (0.0 <= eta < 0.5):
        raise ValueError("eta must satisfy 0 <= eta < 0.5")
    if eta == 0.0:
        return p.copy(), dp.copy()
    k = np.array([[1.0 - eta, eta], [eta, 1.0 - eta]], dtype=float)
    batch = np.vstack([p[None, :], dp])
    for q in range(n):
        batch = _apply_binary_channel_batch(batch, k, q, n)
    return batch[0], batch[1:]


def normalized_visible_scores_from_pdp(
    p: np.ndarray,
    dp: np.ndarray,
    FQ: np.ndarray,
    probability_floor: float = 1e-13,
    tangent_floor: float = 1e-13,
):
    support = p > probability_floor
    if np.any(np.abs(dp[:, ~support]) > 1e-9):
        raise RuntimeError("nonregular probability tangent outside numerical support")
    ps = p[support]
    dps = dp[:, support]
    Ffull = np.sum(dps * dps / ps[None, :], axis=1)
    regular = (
        (Ffull > tangent_floor)
        & (FQ > tangent_floor)
        & np.isfinite(Ffull)
        & np.isfinite(FQ)
    )
    U = dps[regular] / np.sqrt(ps)[None, :]
    U = U / np.sqrt(Ffull[regular])[:, None]
    return {
        "p": p,
        "support": support,
        "p_support": ps,
        "Ffull": Ffull,
        "FQ": FQ,
        "regular": regular,
        "U": U,
    }


def normalized_visible_scores(
    psi: np.ndarray,
    phis: np.ndarray,
    probability_floor: float = 1e-13,
    bitflip_rate: float = 0.0,
):
    p, dp = probability_tangent_batch(psi, phis)
    FQ = 4.0 * np.sum(np.abs(phis) ** 2, axis=1).real
    if bitflip_rate:
        n = int(round(np.log2(len(p))))
        p, dp = apply_independent_bitflip_channel(p, dp, n, bitflip_rate)
    return normalized_visible_scores_from_pdp(p, dp, FQ, probability_floor)


def covariance_spectrum(U: np.ndarray) -> np.ndarray:
    m, s = U.shape
    gram = (U @ U.T) / m if m <= s else (U.T @ U) / m
    eig = np.linalg.eigvalsh((gram + gram.T) / 2.0)
    eig = np.sort(np.clip(eig, 0.0, None))[::-1]
    eig = eig[eig > 1e-13]
    if eig.sum() > 0:
        eig = eig / eig.sum()
    return eig


def pairwise_purity_and_deff(U: np.ndarray):
    """Unbiased U-statistic for Tr(C^2); reciprocal is only a diagnostic."""
    m = U.shape[0]
    if m < 2:
        return np.nan, np.nan
    g = U @ U.T
    off = (np.sum(g * g) - np.sum(np.diag(g) ** 2)) / (m * (m - 1))
    purity = max(float(off), 1e-15)
    return purity, 1.0 / purity


def third_spectral_moment(U: np.ndarray) -> float:
    """Unbiased distinct-triple U-statistic for Tr(C^3)."""
    m = U.shape[0]
    if m < 3:
        return np.nan
    g = U @ U.T
    tr_g3 = float(np.trace(g @ g @ g))
    sum_g2 = float(np.sum(g * g))
    distinct = tr_g3 - 3.0 * sum_g2 + 2.0 * m
    return distinct / (m * (m - 1) * (m - 2))


def walsh_readout_basis(
    p_support: np.ndarray,
    support_indices: np.ndarray,
    n: int,
    k: int,
    svd_tolerance: float = 1e-10,
):
    bits = (support_indices[:, None] >> (n - 1 - np.arange(n))) & 1
    z = 1 - 2 * bits
    cols = []
    labels = []
    for order in range(1, k + 1):
        for subset in combinations(range(n), order):
            cols.append(np.prod(z[:, subset], axis=1).astype(float))
            labels.append(subset)
    if not cols:
        return np.zeros((len(p_support), 0)), 0, labels
    f = np.column_stack(cols)
    means = p_support @ f
    w = np.sqrt(p_support)[:, None] * (f - means[None, :])
    q, s, _ = np.linalg.svd(w, full_matrices=False)
    threshold = svd_tolerance * max(1.0, s[0] if len(s) else 1.0)
    rank = int(np.sum(s > threshold))
    return q[:, :rank], rank, labels


def direct_readout_retention(
    U: np.ndarray,
    p_support: np.ndarray,
    support_indices: np.ndarray,
    n: int,
    k: int,
    svd_tolerance: float = 1e-10,
):
    q, rank, _ = walsh_readout_basis(
        p_support, support_indices, n, k, svd_tolerance
    )
    if rank == 0:
        return 0.0, 0, np.nan
    coeff = U @ q
    retention = float(np.mean(np.sum(coeff * coeff, axis=1)))
    nscore = len(p_support) - 1
    baseline = rank / nscore if nscore > 0 else np.nan
    return retention, rank, baseline


def repeated_crossfit_kyfan(
    U: np.ndarray,
    ranks: list[int],
    seed: int,
    repeats: int = 20,
    train_fraction: float = 0.5,
):
    m = U.shape[0]
    if m < 8:
        return {int(r): np.nan for r in ranks}
    rng = np.random.default_rng(seed)
    acc = {int(r): [] for r in ranks}
    cut = max(2, min(m - 2, int(round(train_fraction * m))))
    for _ in range(repeats):
        perm = rng.permutation(m)
        train, test = U[perm[:cut]], U[perm[cut:]]
        _, _, vh = np.linalg.svd(train, full_matrices=False)
        for r in ranks:
            rr = min(int(r), vh.shape[0])
            if rr < 1:
                continue
            proj = test @ vh[:rr].T
            acc[int(r)].append(float(np.mean(np.sum(proj * proj, axis=1))))
    return {r: (float(np.mean(v)) if v else np.nan) for r, v in acc.items()}


def random_rank_subspace_null(
    U: np.ndarray,
    sqrt_p: np.ndarray,
    rank: int,
    draws: int,
    seed: int,
):
    """Haar-random rank-r subspaces in the centered score space."""
    if rank <= 0:
        return np.zeros(draws)
    s = U.shape[1]
    nscore = s - 1
    if rank > nscore:
        raise ValueError("rank exceeds centered score dimension")
    rng = np.random.default_rng(seed)
    out = np.empty(draws, dtype=float)
    w = sqrt_p / np.linalg.norm(sqrt_p)
    for b in range(draws):
        a = rng.normal(size=(s, rank))
        a = a - w[:, None] * (w @ a)[None, :]
        q, _ = np.linalg.qr(a, mode="reduced")
        coeff = U @ q[:, :rank]
        out[b] = np.mean(np.sum(coeff * coeff, axis=1))
    return out
