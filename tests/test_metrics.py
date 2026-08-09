import math

import numpy as np

from aqt.core import hamming_weight_support
from aqt.metrics import (
    apply_independent_bitflip_channel,
    covariance_spectrum,
    direct_readout_retention,
    pairwise_purity_and_deff,
    random_rank_subspace_null,
    third_spectral_moment,
    walsh_readout_basis,
)


def test_support_correct_readout_ranks():
    n = 6
    full = np.arange(2**n)
    p = np.ones(2**n) / 2**n
    _, r1, _ = walsh_readout_basis(p, full, n, 1)
    _, r2, _ = walsh_readout_basis(p, full, n, 2)
    assert r1 == n
    assert r2 == n + math.comb(n, 2)

    supp = hamming_weight_support(n, n // 2)
    pu = np.ones(len(supp)) / len(supp)
    _, u1, _ = walsh_readout_basis(pu, supp, n, 1)
    _, u2, _ = walsh_readout_basis(pu, supp, n, 2)
    assert u1 == 5
    assert u2 == 14


def test_pairwise_and_third_moment_for_isotropic_scores():
    rng = np.random.default_rng(8)
    m, n = 2500, 31
    U = rng.normal(size=(m, n))
    U /= np.linalg.norm(U, axis=1, keepdims=True)
    purity, deff = pairwise_purity_and_deff(U)
    tr3 = third_spectral_moment(U)
    assert abs(purity - 1 / n) < 0.002
    assert abs(deff - n) < 2.0
    assert abs(tr3 - 1 / n**2) < 4e-4


def test_random_subspace_null_recovers_rank_law():
    rng = np.random.default_rng(9)
    m, support, rank = 300, 32, 5
    sqrtp = np.ones(support) / np.sqrt(support)
    U = rng.normal(size=(m, support))
    U -= (U @ sqrtp)[:, None] * sqrtp[None, :]
    U /= np.linalg.norm(U, axis=1, keepdims=True)
    draws = random_rank_subspace_null(U, sqrtp, rank, 300, 10)
    assert abs(draws.mean() - rank / (support - 1)) < 0.015


def test_bitflip_channel_preserves_normalization_and_zero_sum_tangent():
    rng = np.random.default_rng(10)
    n = 5
    p = rng.random(2**n)
    p /= p.sum()
    dp = rng.normal(size=(3, 2**n))
    dp -= dp.mean(axis=1, keepdims=True)
    q, dq = apply_independent_bitflip_channel(p, dp, n, 0.03)
    np.testing.assert_allclose(q.sum(), 1.0, atol=1e-13)
    np.testing.assert_allclose(dq.sum(axis=1), 0.0, atol=1e-12)


def test_sample_covariance_deviation_bound_for_projector():
    rng = np.random.default_rng(123)
    m, nscore, rank = 80, 19, 5
    U = rng.normal(size=(m, nscore))
    U /= np.linalg.norm(U, axis=1, keepdims=True)
    C = (U.T @ U) / m
    Q, _ = np.linalg.qr(rng.normal(size=(nscore, rank)), mode="reduced")
    P = Q @ Q.T
    retention = float(np.trace(P @ C))
    baseline = rank / nscore
    purity = float(np.trace(C @ C))
    rhs = np.sqrt(rank * (1 - rank / nscore) * max(0.0, purity - 1 / nscore))
    assert abs(retention - baseline) <= rhs + 1e-12
