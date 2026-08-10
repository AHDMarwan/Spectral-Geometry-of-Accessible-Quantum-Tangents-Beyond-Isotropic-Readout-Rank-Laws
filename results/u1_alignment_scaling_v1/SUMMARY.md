# U(1) alignment scaling extension

Primary statistic: fraction of the cross-fitted leading rank-r1 tangent subspace inside the cumulative Walsh span of weight <= k.

The n=8,10,12 cells are archived data from `u1_alignment_mechanism_v1`; n=14,16,18 are new runs with the same d=6n and 128/128 cross-fit tangent protocol.

| n | k | aligned-subspace fraction | 95% bootstrap CI | circuits |
|---:|---:|---:|---:|---:|
| 8 | 1 | 0.551559 | [0.528465, 0.574127] | 20 |
| 10 | 1 | 0.450288 | [0.431683, 0.470149] | 20 |
| 12 | 1 | 0.396099 | [0.381726, 0.409820] | 20 |
| 14 | 1 | 0.340603 | [0.331509, 0.349734] | 20 |
| 16 | 1 | 0.308828 | [0.299564, 0.318144] | 20 |
| 18 | 1 | 0.283586 | [0.277044, 0.290865] | 20 |
| 8 | 2 | 0.821622 | [0.806329, 0.836072] | 20 |
| 10 | 2 | 0.699741 | [0.686621, 0.713304] | 20 |
| 12 | 2 | 0.628310 | [0.617733, 0.639029] | 20 |
| 14 | 2 | 0.555950 | [0.549071, 0.563134] | 20 |
| 16 | 2 | 0.504575 | [0.497781, 0.511200] | 20 |
| 18 | 2 | 0.463538 | [0.457425, 0.469591] | 20 |

## Finite-size scaling discrimination

Both candidate models have two fitted parameters and are fit in log-overlap space. Positive Delta AICc = AICc(exp) - AICc(power) favors the power law. LOOCV is also reported in `fits.csv`.

| k | window | power alpha | 95% CI | exp rate b | 95% CI | Delta AICc (exp-power) | bootstrap P(power AICc lower) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | n8_to_n18 | 0.8223 | [0.7694, 0.8735] | 0.06583 | [0.06172, 0.06990] | 14.392 | 0.996 |
| 1 | tail_n12_to_n18 | 0.8188 | [0.7147, 0.9178] | 0.05502 | [0.04807, 0.06159] | 4.364 | 0.957 |
| 2 | n8_to_n18 | 0.7041 | [0.6798, 0.7281] | 0.05665 | [0.05471, 0.05855] | 12.818 | 0.988 |
| 2 | tail_n12_to_n18 | 0.7488 | [0.6974, 0.7974] | 0.05047 | [0.04705, 0.05371] | 9.789 | 0.956 |

Interpretation rule: this experiment can support finite-size polynomial-vs-exponential scaling evidence. It does not by itself prove an asymptotic lower bound or a hydrodynamic theorem.
