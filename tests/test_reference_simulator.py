"""Independent small-n reference implementation using explicit full matrices.

This deliberately does not use the tensor-application routines being tested.
"""

import numpy as np
import pytest

from aqt.core import (
    CNOT4,
    CZ4,
    H_XY,
    I2,
    PAULI,
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


def embed_1q(gate, q, n):
    ops = [gate if j == q else I2 for j in range(n)]
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def embed_2q(gate, q1, q2, n):
    d = 2**n
    out = np.zeros((d, d), complex)
    for col in range(d):
        bits = [(col >> (n - 1 - q)) & 1 for q in range(n)]
        pin = 2 * bits[q1] + bits[q2]
        for pout in range(4):
            amp = gate[pout, pin]
            if amp == 0:
                continue
            bb = bits.copy()
            bb[q1], bb[q2] = (pout >> 1) & 1, pout & 1
            row = 0
            for b in bb:
                row = (row << 1) | b
            out[row, col] += amp
    return out


def reference_state(n, depth, family, theta, architecture_seed):
    layers, pcount = parameter_layers(n, depth, family)
    assert len(theta) == pcount
    psi = initial_state(n, family)
    rng_arch = np.random.default_rng(architecture_seed)
    for layer, entries in enumerate(layers):
        for pidx, kind, axis, q1, q2 in entries:
            gate = rotation(axis, float(theta[pidx])) if kind == "rotation" else xy_gate(float(theta[pidx]))
            full = embed_1q(gate, q1, n) if kind == "rotation" else embed_2q(gate, q1, q2, n)
            psi = full @ psi
        if family == "RY-RZ-CZ-line":
            pairs, gates = [(q, q + 1) for q in range(n - 1)], [CZ4] * (n - 1)
        elif family == "SU2-CNOT-line":
            pairs, gates = [(q, q + 1) for q in range(n - 1)], [CNOT4] * (n - 1)
        elif family == "SU2-CZ-ring":
            pairs = [(q, q + 1) for q in range(n - 1)] + ([(n - 1, 0)] if n > 2 else [])
            gates = [CZ4] * len(pairs)
        elif family == "SU2-CZ-random-matching":
            perm = rng_arch.permutation(n)
            pairs = [(int(perm[j]), int(perm[j + 1])) for j in range(0, n - 1, 2)]
            gates = [CZ4] * len(pairs)
        elif family == "SU2-HaarU4-brickwork":
            pairs = brickwork_pairs(n, layer)
            gates = [haar_u4(rng_arch) for _ in pairs]
        else:
            pairs, gates = [], []
        for pair, gate in zip(pairs, gates):
            psi = embed_2q(gate, *pair, n) @ psi
    return psi


@pytest.mark.parametrize("family", ["RY-RZ-CZ-line", "SU2-CNOT-line", "SU2-HaarU4-brickwork", "U1-RZ-XY-line"])
def test_fast_simulator_against_explicit_matrix_reference(family):
    n, depth = 3 if family != "U1-RZ-XY-line" else 4, 2
    rng = np.random.default_rng(stable_seed("reference|" + family, 20260809))
    _, pcount = parameter_layers(n, depth, family)
    theta = rng.uniform(-np.pi, np.pi, pcount)
    direction = sample_parameter_directions(rng, 1, pcount)
    arch = stable_seed("reference-arch|" + family, 20260809)
    psi, phis, _ = simulate_vqc_tangent_batch(n, depth, family, theta, direction, arch)
    ref = reference_state(n, depth, family, theta, arch)
    np.testing.assert_allclose(psi, ref, atol=2e-12, rtol=2e-12)
    eps = 2e-7
    rp = reference_state(n, depth, family, theta + eps * direction[0], arch)
    rm = reference_state(n, depth, family, theta - eps * direction[0], arch)
    phi_fd = (rp - rm) / (2 * eps)
    phi_fd = phi_fd - np.vdot(ref, phi_fd) * ref
    np.testing.assert_allclose(phis[0], phi_fd, atol=2e-7, rtol=2e-6)
