import math

import numpy as np
import pytest

from aqt.core import (
    CZ4,
    FAMILIES,
    H_XY,
    I2,
    X,
    Y,
    Z,
    brickwork_pairs,
    haar_u4,
    initial_state,
    parameter_layers,
    rotation,
    sample_parameter_directions,
    simulate_vqc_tangent_batch,
    stable_seed,
    xy_gate,
)
from aqt.metrics import normalized_visible_scores, probability_tangent_batch


def test_basic_gates_are_unitary():
    for axis in "XYZ":
        u = rotation(axis, 0.731)
        np.testing.assert_allclose(u.conj().T @ u, I2, atol=1e-13)
    u = xy_gate(-1.27)
    np.testing.assert_allclose(u.conj().T @ u, np.eye(4), atol=1e-13)
    rng = np.random.default_rng(3)
    u = haar_u4(rng)
    np.testing.assert_allclose(u.conj().T @ u, np.eye(4), atol=1e-13)


def test_xy_gate_derivative():
    theta = 0.43
    eps = 1e-7
    fd = (xy_gate(theta + eps) - xy_gate(theta - eps)) / (2 * eps)
    exact = -1j * H_XY @ xy_gate(theta)
    np.testing.assert_allclose(fd, exact, atol=2e-9)


def test_direction_samplers_are_normalized():
    rng = np.random.default_rng(7)
    for name in ["gaussian", "rademacher", "coordinate"]:
        v = sample_parameter_directions(rng, 8, 20, name)
        np.testing.assert_allclose(np.linalg.norm(v, axis=1), 1.0, atol=1e-13)


def test_u1_half_filling_and_information_contraction():
    n, depth, family = 6, 4, "U1-RZ-XY-line"
    rng = np.random.default_rng(11)
    _, pcount = parameter_layers(n, depth, family)
    theta = rng.uniform(-np.pi, np.pi, size=pcount)
    directions = sample_parameter_directions(rng, 5, pcount)
    psi, phis, _ = simulate_vqc_tangent_batch(n, depth, family, theta, directions, 19)
    info = normalized_visible_scores(psi, phis)
    assert info["support"].sum() == math.comb(n, n // 2)
    assert np.all(info["Ffull"] <= info["FQ"] * (1 + 2e-10))
    np.testing.assert_allclose(np.sum(np.abs(psi) ** 2), 1.0, atol=1e-12)
    np.testing.assert_allclose(phis @ np.conjugate(psi), 0.0, atol=1e-12)


@pytest.mark.parametrize("family", ["RY-RZ-CZ-line", "SU2-CNOT-line", "SU2-HaarU4-brickwork", "U1-RZ-XY-line"])
def test_probability_directional_tangent_matches_finite_difference(family):
    n, depth = 4, 2
    seed = stable_seed("fd|" + family, 20260809)
    rng = np.random.default_rng(seed)
    _, pcount = parameter_layers(n, depth, family)
    theta = rng.uniform(-np.pi, np.pi, pcount)
    direction = sample_parameter_directions(rng, 1, pcount)
    arch = stable_seed("arch|" + family, 20260809)
    psi, phis, _ = simulate_vqc_tangent_batch(n, depth, family, theta, direction, arch)
    _, dp = probability_tangent_batch(psi, phis)
    eps = 1e-6
    zero = np.zeros_like(direction)
    psi_p, _, _ = simulate_vqc_tangent_batch(n, depth, family, theta + eps * direction[0], zero, arch)
    psi_m, _, _ = simulate_vqc_tangent_batch(n, depth, family, theta - eps * direction[0], zero, arch)
    dp_fd = (np.abs(psi_p) ** 2 - np.abs(psi_m) ** 2) / (2 * eps)
    np.testing.assert_allclose(dp[0], dp_fd, atol=2e-7, rtol=2e-6)
