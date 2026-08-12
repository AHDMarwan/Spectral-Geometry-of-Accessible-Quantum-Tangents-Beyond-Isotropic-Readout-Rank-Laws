# AQT Related-Work Audit: Gross & Rieser (arXiv:2602.18377)

## Why this paper must be discussed explicitly

Gross and Rieser study measurement-limited visibility in quantum extreme learning machines using a Pauli-transfer-matrix (PTM) representation. Their effective readout map exposes a row space in Pauli-feature coordinates, and their decodability score is constructed from the projector R^+R. They also state a local-injectivity condition requiring the effective readout to remain injective on the tangent space of the classical input feature map.

This creates genuine conceptual overlap with any broad claim that a restricted readout can miss tangent or feature directions. The AQT manuscript must therefore avoid presenting subspace visibility, projector geometry, or readout rank by themselves as new ideas.

## Distinction that should appear on page 1

Gross-Rieser problem:

- model: QELM/QRC with initial-state encoding and fixed reservoir dynamics;
- varying object: classical input u;
- representation: encoded Pauli-feature vector phi(u);
- readout map: effective PTM R acting on Pauli-feature/operator space;
- main geometric question: which encoded features can be decoded or reconstructed from the row space exposed by the reservoir and measurements;
- local tangent condition: injectivity of R on im J_phi(u).

Present AQT paper:

- model: trainable variational quantum circuit;
- varying object: circuit parameters theta;
- representation: Fisher-normalized derivatives of a fixed measurement distribution;
- geometric object: parameter-tangent score covariance C = E[u_v u_v^T];
- readout map: projector P acting inside the centered score space of the fixed measurement record;
- main question: how much covariance-weighted parameter-tangent mass Tr(PC) is retained at fixed readout rank;
- intervention: physical, random rank-matched, and cross-fitted aligned readouts compared at identical rank;
- operational test: finite-shot directional signal at a fixed quantum measurement and evaluation shot budget.

## Claims to avoid

Do not write:

- "We introduce the idea that a readout can miss tangent directions."
- "We are the first to formulate readout visibility as a subspace projection."
- "Readout rank alone has not previously been studied as an expressivity constraint."
- "Observable subspace orientation is entirely unexplored in quantum machine learning."

These formulations are too broad after Gross & Rieser and other observability/decodability work.

## Defensible novelty statement

Preferred formulation:

"For a fixed measurement of a trainable variational circuit, the projected objects are Fisher-normalized parameter tangents rather than encoded input features. Their covariance spectrum supplies a non-isotropic weighting of score directions. The contribution is a rank-controlled comparison of physical, random, and cross-fitted readouts in this measurement-induced parameter-tangent geometry, together with a finite-shot test in which the quantum measurement, readout rank, and evaluation resources are held fixed."

## Discussion-level comparison

The related-work paragraph should acknowledge that Gross & Rieser also discuss covariance-sensitive predictability beyond their geometric decodability score. The distinction should therefore not be stated as "they ignore covariance." The safer distinction is the object and stage of the pipeline: input Pauli-feature decodability in a fixed reservoir versus parameter-tangent score covariance after a fixed measurement of a trainable VQC.

## Citation requirement

Add a direct bibliography entry for:

M. Gross and H.-M. Rieser, "Theory and interpretability of Quantum Extreme Learning Machines: a Pauli-transfer matrix approach," arXiv:2602.18377 [quant-ph] (2026).

The AQT introduction should cite this work before presenting the present spectral-orientation problem.
