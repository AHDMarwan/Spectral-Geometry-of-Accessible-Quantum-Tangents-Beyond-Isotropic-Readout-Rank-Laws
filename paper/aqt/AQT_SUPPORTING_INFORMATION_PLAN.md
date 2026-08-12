# AQT Supporting Information Split

Target: keep the main Research Article readable without the Supporting Information while moving derivations and secondary diagnostics out of the central narrative.

## Main article display items

Recommended main-text display set:

1. Framework figure: fixed measurement -> tangent-score covariance -> rank-r readout -> retained mass/orientation.
2. Rank-normalized retention versus covariance anisotropy, including architecture-resolved evidence that near-rank retention does not imply isotropy.
3. Same-rank physical/random/cross-fitted spectral comparison combined with the fixed-shot directional gradient-energy and SNR gains.
4. Sector-corrected U(1) alignment figure showing observed low-weight alignment against the fixed-charge random-orientation null.

A fifth display item is acceptable if needed for readability, but the circuit-family schematic should not displace a central result from the main article.

## Move to Supporting Information

- Full Grassmann projector-moment derivation and null-width diagnostic figure.
- Fixed-weight diagonal readout rank bookkeeping and rank-fraction figure; the exact isotropic law belongs to the separate isotropic-rank paper.
- Individual PennyLane circuit schematics and gate-convention details.
- Full cross-fitting implementation details, calibration/evaluation sample counts, and statistical-unit notes beyond the concise Methods description.
- Additional operational-gain panels.
- Noise-robustness sweeps and their qualification that the aligned subspace is re-estimated after noise.
- U(1) power-versus-exponential fit figure and detailed AICc diagnostics.
- Symmetry-breaking pilot figure and full perturbation table. The main text can retain the numerical result as a sensitivity control.
- Extended architecture-resolved diagnostics and effective-dimension plots not required to establish the main claim.
- Complete reproducibility conventions, frozen-profile identifiers, seeds, and result-to-file provenance table.

## Supporting Information section order

S1. Score-space construction and Fisher normalization
S2. Grassmann random-orientation moments
S3. Full- and fixed-charge readout-rank bookkeeping
S4. Numerical circuit definitions and parameter conventions
S5. Cross-fitting, Ky Fan benchmark, and statistical unit
S6. Finite-shot directional-signal calculation
S7. Extended generic architecture diagnostics
S8. U(1) finite-size model comparison
S9. Symmetry-breaking sensitivity control
S10. Noise and robustness diagnostics
S11. Reproducibility and archived numerical provenance

## Main-text independence test

Before submission, the main article must still establish all of the following without opening the Supporting Information:

- what the parameter-tangent score covariance C represents;
- why R = Tr(PC) is the retained tangent mass;
- why r/N is a random-orientation reference rather than an isotropy claim;
- the coexistence of near-rank retention and strong covariance anisotropy;
- the same-rank physical versus aligned retention gap;
- the fixed-shot 9.584x directional gradient-energy and 3.111x SNR result at n=12;
- the sector-corrected U(1) alignment result;
- the limits of the claim: no supervised-loss theorem and no mechanism identification for the U(1) structure.
