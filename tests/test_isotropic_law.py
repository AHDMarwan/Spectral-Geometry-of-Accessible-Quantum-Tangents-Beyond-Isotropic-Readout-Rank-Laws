import numpy as np
from scipy.stats import beta, kstest


def test_rank_projector_beta_law_numerically():
    rng = np.random.default_rng(20260809)
    d, r, m = 31, 6, 20000
    g = rng.normal(size=(m, d))
    g /= np.linalg.norm(g, axis=1, keepdims=True)
    x = np.sum(g[:, :r] ** 2, axis=1)
    expected_mean = r / d
    assert abs(x.mean() - expected_mean) < 0.004
    ks = kstest(x, beta(r / 2, (d - r) / 2).cdf)
    # This is a stochastic diagnostic with a fixed seed; keep the threshold loose.
    assert ks.statistic < 0.02
