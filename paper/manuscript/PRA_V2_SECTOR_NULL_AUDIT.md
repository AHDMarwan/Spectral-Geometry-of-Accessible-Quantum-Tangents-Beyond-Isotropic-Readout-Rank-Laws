# PRA v2: half-filled-sector random-orientation audit

This audit compares the measured low-weight alignment with a random 
rank-$r_1$ subspace drawn inside the **same half-filled score sector**.
It therefore removes the ambiguity between a full $2^n$ score-space null 
and the sector-corrected fixed-charge geometry.

For $A_k=\mathrm{Tr}(P_{\le k}P_{\rm top})/r_1$ the null mean is

$$\mathbb E A_k=r_{\le k}/N_{\rm hf},$$

and the reported null standard deviation is obtained from the exact 
Grassmann second moment used in the manuscript.

| n | k | observed | 95% CI | sector null | null SD | observed/null |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | 1 | 0.551559 | [0.528465, 0.574127] | 0.101449 | 0.0183 | 5.4x |
| 10 | 1 | 0.450288 | [0.431683, 0.470149] | 0.0358566 | 0.00542 | 12.6x |
| 12 | 1 | 0.396099 | [0.381726, 0.409820] | 0.0119177 | 0.00151 | 33.2x |
| 14 | 1 | 0.340603 | [0.331509, 0.349734] | 0.00378898 | 0.000411 | 89.9x |
| 16 | 1 | 0.308828 | [0.299564, 0.318144] | 0.00116559 | 0.00011 | 265.0x |
| 18 | 1 | 0.283586 | [0.277044, 0.290865] | 0.000349658 | 2.91e-05 | 811.0x |
| 8 | 2 | 0.821622 | [0.806329, 0.836072] | 0.391304 | 0.0296 | 2.1x |
| 10 | 2 | 0.699741 | [0.686621, 0.713304] | 0.175299 | 0.0111 | 4.0x |
| 12 | 2 | 0.628310 | [0.617733, 0.639029] | 0.0704225 | 0.00357 | 8.9x |
| 14 | 2 | 0.555950 | [0.549071, 0.563134] | 0.0262314 | 0.00107 | 21.2x |
| 16 | 2 | 0.504575 | [0.497781, 0.511200] | 0.00924703 | 0.000308 | 54.6x |
| 18 | 2 | 0.463538 | [0.457425, 0.469591] | 0.00312635 | 8.68e-05 | 148.3x |

At $n=18$ the one-body and cumulative-through-two alignments are 
811x and 148x their respective sector-null means.

Interpretation: this is a geometric random-orientation control inside 
the fixed-charge support. It does not identify the dynamical mechanism 
responsible for the observed alignment.
