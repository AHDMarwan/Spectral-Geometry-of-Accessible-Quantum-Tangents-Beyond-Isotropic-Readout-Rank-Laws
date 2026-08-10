from __future__ import annotations

"""Generate publication circuit schematics with PennyLane's draw_mpl.

The gate order mirrors ``src/aqt/core.py``.  The drawings use a small number of
wires/layers only for readability; production simulations use the protocol
specified in the manuscript (typically depth d=6n).

Run from the repository root after installing PennyLane and matplotlib:

    python paper/prx/figure_scripts/draw_circuits_pennylane.py

Outputs are written to ``paper/prx/figures/generated_circuits`` as both PDF and
PNG files.
"""

from pathlib import Path
import math

import matplotlib.pyplot as plt
import numpy as np
import pennylane as qml


OUT = Path("paper/prx/figures/generated_circuits")
OUT.mkdir(parents=True, exist_ok=True)


def _haar_unitary(seed: int, dim: int = 4) -> np.ndarray:
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    phase = np.where(np.abs(d) > 0, d / np.abs(d), 1.0)
    return q @ np.diag(np.conjugate(phase))


def _xy_matrix(theta: float) -> np.ndarray:
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    h_xy = (np.kron(x, x) + np.kron(y, y)) / 4.0
    return (
        np.eye(4, dtype=np.complex128)
        + (math.cos(theta / 2) - 1.0) * (4.0 * h_xy @ h_xy)
        - 2j * math.sin(theta / 2) * h_xy
    )


def _brickwork_pairs(n: int, layer: int) -> list[tuple[int, int]]:
    return [(q, q + 1) for q in range(layer % 2, n - 1, 2)]


def _rot_block(axis_set: tuple[str, ...], n: int, layer: int) -> None:
    # Deterministic non-special angles keep labels compact while making each
    # layer visually distinct. These are schematic values only.
    for q in range(n):
        for j, axis in enumerate(axis_set):
            angle = 0.31 + 0.13 * layer + 0.07 * q + 0.05 * j
            if axis == "X":
                qml.RX(angle, wires=q)
            elif axis == "Y":
                qml.RY(angle, wires=q)
            elif axis == "Z":
                qml.RZ(angle, wires=q)
            else:
                raise ValueError(axis)


def circuit_ry_rz_cz(n: int = 6, layers: int = 2) -> None:
    for layer in range(layers):
        _rot_block(("Y", "Z"), n, layer)
        for q in range(n - 1):
            qml.CZ(wires=[q, q + 1])
        qml.Barrier(wires=range(n), only_visual=True)


def circuit_su2_cnot(n: int = 6, layers: int = 2) -> None:
    for layer in range(layers):
        _rot_block(("X", "Y", "Z"), n, layer)
        for q in range(n - 1):
            qml.CNOT(wires=[q, q + 1])
        qml.Barrier(wires=range(n), only_visual=True)


def circuit_su2_cz_ring(n: int = 6, layers: int = 2) -> None:
    for layer in range(layers):
        _rot_block(("X", "Y", "Z"), n, layer)
        for q in range(n - 1):
            qml.CZ(wires=[q, q + 1])
        if n > 2:
            qml.CZ(wires=[n - 1, 0])
        qml.Barrier(wires=range(n), only_visual=True)


def circuit_su2_cz_random_matching(n: int = 6, layers: int = 2) -> None:
    rng = np.random.default_rng(20260810)
    for layer in range(layers):
        _rot_block(("X", "Y", "Z"), n, layer)
        perm = rng.permutation(n)
        for j in range(0, n - 1, 2):
            qml.CZ(wires=[int(perm[j]), int(perm[j + 1])])
        qml.Barrier(wires=range(n), only_visual=True)


def circuit_su2_haar_u4(n: int = 6, layers: int = 2) -> None:
    seed = 9017
    for layer in range(layers):
        _rot_block(("X", "Y", "Z"), n, layer)
        for pair_id, (q1, q2) in enumerate(_brickwork_pairs(n, layer)):
            u4 = _haar_unitary(seed + 101 * layer + pair_id)
            qml.QubitUnitary(u4, wires=[q1, q2], label=r"$U_4$ (Haar)")
        qml.Barrier(wires=range(n), only_visual=True)


def circuit_u1_rz_xy(n: int = 6, layers: int = 2) -> None:
    # Mirrors core.initial_state for U1-RZ-XY-line: qubits q=0,2,4,... are |1>.
    for q in range(0, n, 2):
        qml.PauliX(wires=q)
    qml.Barrier(wires=range(n), only_visual=True)

    for layer in range(layers):
        for q in range(n):
            qml.RZ(0.37 + 0.11 * layer + 0.05 * q, wires=q)
        for pair_id, (q1, q2) in enumerate(_brickwork_pairs(n, layer)):
            theta = 0.43 + 0.09 * layer + 0.03 * pair_id
            qml.QubitUnitary(_xy_matrix(theta), wires=[q1, q2], label=r"$XY(\theta)$")
        qml.Barrier(wires=range(n), only_visual=True)


CIRCUITS = {
    "circuit_ry_rz_cz": circuit_ry_rz_cz,
    "circuit_su2_cnot": circuit_su2_cnot,
    "circuit_su2_cz_ring": circuit_su2_cz_ring,
    "circuit_su2_cz_random_matching": circuit_su2_cz_random_matching,
    "circuit_su2_haar_u4": circuit_su2_haar_u4,
    "circuit_u1_rz_xy": circuit_u1_rz_xy,
}


def draw_one(name: str, fn, n: int = 6, layers: int = 2) -> None:
    # PennyLane 0.45 uses ``layers`` internally in draw_mpl; passing a circuit
    # argument with the same name can collide. Wrap the circuit with ``reps``
    # to keep the public drawing call unambiguous.
    def wrapped(n: int = 6, reps: int = 2) -> None:
        fn(n=n, layers=reps)

    drawer = qml.draw_mpl(wrapped, decimals=2, style="pennylane", fontsize=10)
    fig, ax = drawer(n=n, reps=layers)
    ax.set_title(name.replace("circuit_", "").replace("_", " ").upper(), pad=14, fontsize=12)
    fig.set_size_inches(12.0, 3.8)
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    for name, fn in CIRCUITS.items():
        draw_one(name, fn)


if __name__ == "__main__":
    main()
