import numpy as np

from aqt.metrics import random_rank_subspace_null
from aqt.rigorous import (
    _haar_rank_null_moments,
    _prefix_view,
    _simulate_visible_scores_batched,
    build_schedule,
)


def _small_cfg(batch_size):
    return {
        "name": "unit",
        "master_seed": 77124999,
        "families": ["RY-RZ-CZ-line"],
        "n_values": [3],
        "depth_factors": [1.0],
        "instances": 1,
        "tangents": 8,
        "tangent_prefixes": [8],
        "simulation_batch_size": batch_size,
        "readout_orders": [1, 2],
        "direction_samplers": ["gaussian"],
        "measurement_bases": ["Z"],
        "bitflip_rates": [0.0],
        "probability_floor": 1e-13,
    }


def test_schedule_is_deterministic_and_explicit():
    cfg = _small_cfg(4)
    first = build_schedule(cfg)
    second = build_schedule(cfg)
    assert first == second
    assert len(first) == 1
    assert first[0]["n"] == 3
    assert first[0]["depth"] == 3
    assert first[0]["tangents"] == 8


def test_tangent_batching_is_numerically_equivalent():
    job = build_schedule(_small_cfg(8))[0]
    full = _simulate_visible_scores_batched(_small_cfg(8), job)
    batched = _simulate_visible_scores_batched(_small_cfg(2), job)
    np.testing.assert_allclose(full["p"], batched["p"], rtol=0.0, atol=5e-13)
    np.testing.assert_array_equal(full["regular_indices"], batched["regular_indices"])
    np.testing.assert_allclose(full["U"], batched["U"], rtol=0.0, atol=2e-12)
    np.testing.assert_allclose(
        full["Ffull_regular"], batched["Ffull_regular"], rtol=0.0, atol=2e-11
    )
    np.testing.assert_allclose(
        full["FQ_regular"], batched["FQ_regular"], rtol=0.0, atol=2e-11
    )


def test_prefix_view_is_nested_not_resampled():
    job = build_schedule(_small_cfg(4))[0]
    bundle = _simulate_visible_scores_batched(_small_cfg(4), job)
    u4, _, _ = _prefix_view(bundle, 4)
    u8, _, _ = _prefix_view(bundle, 8)
    np.testing.assert_allclose(u4, u8[: len(u4)], rtol=0.0, atol=0.0)


def test_haar_null_is_exactly_degenerate_for_isotropic_covariance():
    nscore, rank = 31, 7
    mean, std = _haar_rank_null_moments(rank, nscore, 1.0 / nscore)
    np.testing.assert_allclose(mean, rank / nscore, rtol=0.0, atol=1e-15)
    np.testing.assert_allclose(std, 0.0, rtol=0.0, atol=1e-15)


def test_analytic_haar_null_matches_low_dimensional_monte_carlo():
    rng = np.random.default_rng(1234)
    support = 8
    nscore = support - 1
    rank = 2
    m = 40
    sqrtp = np.ones(support) / np.sqrt(support)
    U = rng.normal(size=(m, support))
    U -= (U @ sqrtp)[:, None] * sqrtp[None, :]
    U /= np.linalg.norm(U, axis=1, keepdims=True)
    gram = U @ U.T
    sample_purity = np.sum(gram * gram) / m**2
    analytic_mean, analytic_std = _haar_rank_null_moments(
        rank, nscore, sample_purity
    )
    draws = random_rank_subspace_null(U, sqrtp, rank, 4000, 5678)
    assert abs(draws.mean() - analytic_mean) < 0.008
    assert abs(draws.std(ddof=1) - analytic_std) < 0.008
