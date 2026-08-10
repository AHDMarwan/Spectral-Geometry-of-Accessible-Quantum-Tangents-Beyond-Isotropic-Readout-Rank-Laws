# Figure visual QA checklist

This checklist is the publication-quality pass for the canonical PRX manuscript PDF.
The goal is not to add scientific claims; it is to make every figure legible at the
actual two-column PDF scale and to keep schematics faithful to the implementation.

## Global checks

- [ ] All axis labels, tick labels, panel letters, legends, and annotations remain readable at 100% PDF zoom on a phone-sized viewport and at normal desktop zoom.
- [ ] No legend overlaps data, confidence intervals, annotations, fit curves, or panel titles.
- [ ] Shared legends are preferred for multi-panel figures when the entries are common across panels.
- [ ] Marker shape and line style remain sufficient to distinguish series in grayscale.
- [ ] Captions are self-contained: what is plotted, what the error bars mean, what the reference line means, and what conclusion is justified.
- [ ] No caption makes an asymptotic or causal claim stronger than the data support.
- [ ] Vector PDF is used for all plotted figures and circuit schematics; PNG is only a convenience artifact.
- [ ] Figure widths match the manuscript environment (single-column versus figure*); nothing is scaled so aggressively that labels become unreadable.

## Fig. 1 — Framework / rank-orientation schematic

- [ ] Panel labels are visually distinct from titles.
- [ ] The meaning of C, P, r/N, and Tr(PC) is readable without the main text.
- [ ] The fixed-weight rank-fraction panel has a legend that does not hide low-n data.
- [ ] The caption explicitly separates the rank-only null model from physical circuit orientation.

## Fig. 2 / canonical rank-typicality figure

- [ ] Generic aggregate legend is legible and does not obscure the confidence region.
- [ ] Architecture-resolved legend is placed where it does not cover error bars; move outside the axes if needed.
- [ ] n=18 Haar-U(4) stress point is visually identifiable without relying only on color.
- [ ] The anisotropy panel clearly labels N Tr(C^2) and the corresponding rho values.
- [ ] The caption states finite-size evidence only and does not imply Haar convergence of physical ansatzes.

## Fig. 3 — PennyLane circuit families

- [x] Remove numerical gate parameters from all boxes.
- [ ] Single-qubit gates display only RX, RY, RZ (and X for initialization where applicable).
- [ ] Two-qubit generic Haar gates display only U; no matrix entries or parameters.
- [ ] U(1) circuit is clearly distinguishable from generic SU(2)/Haar families.
- [ ] Circuit titles are readable but subordinate to the circuit itself.
- [ ] Wire spacing and layer spacing prevent gate-label collisions.
- [ ] Caption states that the shown size/depth is schematic and that production simulations use the protocol specified in the Methods.
- [ ] Caption states that diagrams are generated with PennyLane from constructors mirroring src/aqt/core.py.

## Fig. 4 — Rank-normalized retention and anisotropy

- [ ] Legend font is large enough at final PDF scale.
- [ ] Legends in panels (a) and (b) do not overlap data/error bars.
- [ ] Panel (c) system-size annotations do not collide with markers.
- [ ] Horizontal rho=1 reference is visually distinct from uncertainty bands.
- [ ] Caption explains how rank-typical retention coexists with anisotropy.

## Fig. 5 — Same-rank spectral comparison

- [ ] physical / cross-fit / same-sample Ky-Fan legend is centered and readable.
- [ ] Legend does not consume plotting area or collide with x-axis labels.
- [ ] Same-rank nature of the three comparisons is explicit in the caption.
- [ ] Log-axis tick labels are readable and not clipped.
- [ ] U(1) and Haar-U(4) groups are visually separated.

## Fig. 6 — U(1) finite-size scaling

- [x] Use one shared legend outside the two plotting panels.
- [x] Distinguish data, power fit, and exponential fit by marker/line style as well as color.
- [ ] Legend remains fully inside the figure bounding box after LaTeX inclusion.
- [ ] Delta-AICc boxes do not cover data or fit curves.
- [ ] Both panel titles are readable at two-column width.
- [ ] Error bars at n=18 remain visible.
- [ ] Caption states that model comparison is finite-size descriptive evidence, not an asymptotic theorem or hydrodynamic exponent.

## Fig. 7 — Symmetry-breaking control

- [x] Move legend outside the data region.
- [x] Shorten legend labels to preserve U(1), break U(1), and rank reference semantics.
- [ ] The epsilon=0, 0.03, 0.1, 0.3, 1 ticks remain readable with the symlog axis.
- [ ] The rank reference line and the epsilon=0.3/1 breaking points remain visually separable.
- [ ] Error bars are visible for both perturbation families.
- [ ] Caption says sensitivity control, not mechanism identification.
- [ ] Caption makes clear that 8/255 is a visual full-score-space rank reference after charge breaking, not a sector-Haar null.

## Fixed-weight rank fraction production figure

- [x] Move legend above/outside the axes.
- [ ] Both weight <=1 and weight <=2 series remain readable on the logarithmic y-axis.
- [ ] Title does not collide with the external legend.

## Final PDF inspection

- [ ] Compile the canonical spectral_geometry.pdf from spectral_geometry_rewrite.tex.
- [ ] Inspect every page visually after GitHub Actions produces the canonical PDF.
- [ ] Verify no figure is clipped at page/column boundaries.
- [ ] Verify no caption is cut off or separated awkwardly from its figure.
- [ ] Verify all references to figure numbers match the rendered numbering.
- [ ] Verify circuit gate labels contain no numerical parameters.
- [ ] Verify all legends are readable at actual manuscript scale.
- [ ] Only after the rendered PDF passes this checklist should the visual pass be considered complete.
