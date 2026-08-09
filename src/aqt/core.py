from __future__ import annotations

import hashlib
import math

import numpy as np

I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
HADAMARD = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2.0)
S_DAG = np.diag([1.0, -1j]).astype(np.complex128)
PAULI = {"X": X, "Y": Y, "Z": Z}
H_XY = (np.kron(X, X) + np.kron(Y, Y)) / 4.0
CZ4 = np.diag([1, 1, 1, -1]).astype(np.complex128)
CNOT4 = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    dtype=np.complex128,
)

FAMILIES = (
    "RY-RZ-CZ-line",
    "SU2-CNOT-line",
    "SU2-CZ-ring",
    "SU2-CZ-random-matching",
    "SU2-HaarU4-brickwork",
    "U1-RZ-XY-line",
)


def stable_seed(label: str, master_seed: int) -> int:
    payload = f"{master_seed}|{label}".encode()
    return int.from_bytes(hashlib.blake2b(payload, digest_size=8).digest(), "little")


def rotation(axis: str, theta: float) -> np.ndarray:
    p = PAULI[axis]
    return math.cos(theta / 2) * I2 - 1j * math.sin(theta / 2) * p


def xy_gate(theta: float) -> np.ndarray:
    return (
        np.eye(4, dtype=np.complex128)
        + (math.cos(theta / 2) - 1.0) * (4.0 * H_XY @ H_XY)
        - 2j * math.sin(theta / 2) * H_XY
    )


def haar_unitary(rng: np.random.Generator, dim: int) -> np.ndarray:
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    phase = np.where(np.abs(d) > 0, d / np.abs(d), 1.0)
    return q @ np.diag(np.conjugate(phase))


def haar_u4(rng: np.random.Generator) -> np.ndarray:
    return haar_unitary(rng, 4)


def apply_1q_batch(states: np.ndarray, gate: np.ndarray, q: int, n: int) -> np.ndarray:
    m = states.shape[0]
    tensor = states.reshape((m,) + (2,) * n)
    moved = np.moveaxis(tensor, q + 1, 1)
    out = np.einsum("ab,mb...->ma...", gate, moved, optimize=True)
    out = np.moveaxis(out, 1, q + 1)
    return out.reshape(m, -1)


def apply_2q_batch(
    states: np.ndarray, gate: np.ndarray, q1: int, q2: int, n: int
) -> np.ndarray:
    if q1 == q2:
        raise ValueError("q1 and q2 must differ")
    m = states.shape[0]
    tensor = states.reshape((m,) + (2,) * n)
    moved = np.moveaxis(tensor, (q1 + 1, q2 + 1), (1, 2))
    mat = moved.reshape(m, 4, -1)
    out = np.einsum("ab,mbk->mak", gate, mat, optimize=True)
    out = out.reshape((m, 2, 2) + (2,) * (n - 2))
    out = np.moveaxis(out, (1, 2), (q1 + 1, q2 + 1))
    return out.reshape(m, -1)


def brickwork_pairs(n: int, layer: int) -> list[tuple[int, int]]:
    return [(q, q + 1) for q in range(layer % 2, n - 1, 2)]


def initial_state(n: int, family: str) -> np.ndarray:
    psi = np.zeros(2**n, dtype=np.complex128)
    if family == "U1-RZ-XY-line":
        index = 0
        for q in range(0, n, 2):
            index |= 1 << (n - 1 - q)
        psi[index] = 1.0
    else:
        psi[0] = 1.0
    return psi


def parameter_layers(n: int, depth: int, family: str):
    if family not in FAMILIES:
        raise ValueError(f"Unknown family {family!r}")
    layers = []
    cursor = 0
    for layer in range(depth):
        if family == "RY-RZ-CZ-line":
            axes = ("Y", "Z")
        elif family in (
            "SU2-CNOT-line",
            "SU2-CZ-ring",
            "SU2-CZ-random-matching",
            "SU2-HaarU4-brickwork",
        ):
            axes = ("X", "Y", "Z")
        else:
            axes = ("Z",)
        entries = []
        for q in range(n):
            for axis in axes:
                entries.append((cursor, "rotation", axis, q, -1))
                cursor += 1
        if family == "U1-RZ-XY-line":
            for q1, q2 in brickwork_pairs(n, layer):
                entries.append((cursor, "xy", "XY", q1, q2))
                cursor += 1
        layers.append(entries)
    return layers, cursor


def sample_parameter_directions(
    rng: np.random.Generator, count: int, p: int, sampler: str = "gaussian"
) -> np.ndarray:
    sampler = sampler.lower()
    if sampler == "gaussian":
        v = rng.normal(size=(count, p))
    elif sampler == "rademacher":
        v = rng.choice(np.array([-1.0, 1.0]), size=(count, p))
    elif sampler == "coordinate":
        if count > p:
            raise ValueError("coordinate sampler requires count <= parameter count")
        idx = rng.choice(p, size=count, replace=False)
        v = np.zeros((count, p), dtype=float)
        v[np.arange(count), idx] = 1.0
        return v
    else:
        raise ValueError(f"Unknown direction sampler {sampler!r}")
    norm = np.linalg.norm(v, axis=1, keepdims=True)
    if np.any(norm == 0):
        raise RuntimeError("zero random direction")
    return v / norm


def simulate_vqc_tangent_batch(
    n: int,
    depth: int,
    family: str,
    theta: np.ndarray,
    directions: np.ndarray,
    architecture_seed: int,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Forward-mode directional derivatives for a fixed VQC."""
    layers, pcount = parameter_layers(n, depth, family)
    if len(theta) != pcount or directions.shape[1] != pcount:
        raise ValueError("theta/directions do not match parameter count")
    m = directions.shape[0]
    psi = initial_state(n, family)
    phis = np.zeros((m, 2**n), dtype=np.complex128)
    rng_arch = np.random.default_rng(architecture_seed)

    for layer, entries in enumerate(layers):
        for pidx, kind, axis, q1, q2 in entries:
            angle = float(theta[pidx])
            coeff = directions[:, pidx]
            gate = rotation(axis, angle) if kind == "rotation" else xy_gate(angle)
            combined = np.vstack([psi[None, :], phis])
            if kind == "rotation":
                combined = apply_1q_batch(combined, gate, q1, n)
            else:
                combined = apply_2q_batch(combined, gate, q1, q2, n)
            psi_new, phis_new = combined[0], combined[1:]
            if np.any(coeff):
                if kind == "rotation":
                    gpsi = apply_1q_batch(psi_new[None, :], PAULI[axis], q1, n)[0]
                    phis_new += (-0.5j) * coeff[:, None] * gpsi[None, :]
                else:
                    gpsi = apply_2q_batch(psi_new[None, :], H_XY, q1, q2, n)[0]
                    phis_new += (-1j) * coeff[:, None] * gpsi[None, :]
            psi, phis = psi_new, phis_new

        if family == "RY-RZ-CZ-line":
            pairs = [(q, q + 1) for q in range(n - 1)]
            gates = [CZ4] * len(pairs)
        elif family == "SU2-CNOT-line":
            pairs = [(q, q + 1) for q in range(n - 1)]
            gates = [CNOT4] * len(pairs)
        elif family == "SU2-CZ-ring":
            pairs = [(q, q + 1) for q in range(n - 1)]
            if n > 2:
                pairs.append((n - 1, 0))
            gates = [CZ4] * len(pairs)
        elif family == "SU2-CZ-random-matching":
            perm = rng_arch.permutation(n)
            pairs = [
                (int(perm[j]), int(perm[j + 1])) for j in range(0, n - 1, 2)
            ]
            gates = [CZ4] * len(pairs)
        elif family == "SU2-HaarU4-brickwork":
            pairs = brickwork_pairs(n, layer)
            gates = [haar_u4(rng_arch) for _ in pairs]
        else:
            pairs, gates = [], []
        for (q1, q2), gate in zip(pairs, gates):
            combined = np.vstack([psi[None, :], phis])
            combined = apply_2q_batch(combined, gate, q1, q2, n)
            psi, phis = combined[0], combined[1:]

    overlaps = phis @ np.conjugate(psi)
    phis = phis - overlaps[:, None] * psi[None, :]
    return psi, phis, pcount


def measurement_basis_gates(
    n: int, basis: str, seed: int | None = None
) -> list[np.ndarray]:
    basis = basis.upper()
    if basis == "Z":
        return [I2] * n
    if basis == "X":
        return [HADAMARD] * n
    if basis == "Y":
        return [HADAMARD @ S_DAG] * n
    if basis in {"RANDOM_LOCAL", "HAAR_LOCAL"}:
        if seed is None:
            raise ValueError("random local basis requires a seed")
        rng = np.random.default_rng(seed)
        return [haar_unitary(rng, 2) for _ in range(n)]
    raise ValueError(f"Unknown measurement basis {basis!r}")


def rotate_measurement_basis(
    psi: np.ndarray,
    phis: np.ndarray,
    n: int,
    basis: str,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    gates = measurement_basis_gates(n, basis, seed)
    combined = np.vstack([psi[None, :], phis])
    for q, gate in enumerate(gates):
        combined = apply_1q_batch(combined, gate, q, n)
    return combined[0], combined[1:]


def hamming_weight_support(n: int, weight: int) -> np.ndarray:
    return np.array([x for x in range(2**n) if x.bit_count() == weight], dtype=int)
