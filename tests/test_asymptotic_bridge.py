import math

import numpy as np
import pandas as pd

from aqt.asymptotic_bridge import (
    add_population_bridge_columns,
    haar_rank_law_variance_bound,
    haar_rank_law_variance_rho,
    low_weight_readout_rank,
)


def test_isotropic_covariance_has_zero_orientation_variance():
    N = 63
    r = 6
    assert haar_rank_law_variance_rho(N, r, 1.0 / N) == 0.0


def test_variance_obeys_deff_bound():
    N = 255
    r = 36
    purity = 0.02
    exact = haar_rank_law_variance_rho(N, r, purity)
    bound = haar_rank_law_variance_bound(r, purity)
    assert 0.0 <= exact <= bound


def test_fixed_weight_rank_formula():
    assert low_weight_readout_rank(18, 1) == 18
    assert low_weight_readout_rank(18, 2) == 171


def test_bridge_uses_pairwise_population_purity_not_sample_purity():
    frame = pd.DataFrame(
        {
            "profile": ["test"],
            "circuit_id": ["c0"],
            "family": ["A"],
            "n": [8],
            "k": [1],
            "score_dimension": [255],
            "readout_rank": [8],
            "enhancement": [0.95],
            "pairwise_purity": [0.01],
            "sample_covariance_purity": [0.2],
        }
    )
    out = add_population_bridge_columns(frame).iloc[0]
    expected_var = haar_rank_law_variance_rho(255, 8, 0.01)
    assert math.isclose(out.haar_population_var_rho, expected_var)
    assert math.isclose(out.deff_from_pairwise_purity, 100.0)
    assert math.isclose(out.r_times_deff, 800.0)
    assert math.isclose(
        out.population_orientation_z,
        (0.95 - 1.0) / math.sqrt(expected_var),
    )


def test_invalid_u_stat_purity_is_flagged_not_clipped():
    N = 255
    frame = pd.DataFrame(
        {
            "profile": ["test"],
            "circuit_id": ["c0"],
            "family": ["A"],
            "n": [8],
            "k": [1],
            "score_dimension": [N],
            "readout_rank": [8],
            "enhancement": [1.0],
            "pairwise_purity": [0.5 / N],
        }
    )
    out = add_population_bridge_columns(frame).iloc[0]
    assert not bool(out.population_purity_estimate_valid)
    assert np.isnan(out.haar_population_var_rho)
    assert np.isnan(out.population_orientation_z)
