# Trainability-bridge robustness summary

Primary contrast: cross-fitted tangent-aligned / physical readout, same circuit and rank.

| family | n | bit-flip rate | gradient-signal gain | 95% CI |
|---|---:|---:|---:|---:|
| SU2-HaarU4-brickwork | 8 | 0.0% | 2.963x | [2.871, 3.060] |
| SU2-HaarU4-brickwork | 8 | 1.0% | 2.426x | [2.348, 2.511] |
| SU2-HaarU4-brickwork | 8 | 3.0% | 1.898x | [1.839, 1.959] |
| SU2-HaarU4-brickwork | 8 | 5.0% | 1.589x | [1.541, 1.637] |
| SU2-HaarU4-brickwork | 10 | 0.0% | 4.638x | [4.482, 4.809] |
| SU2-HaarU4-brickwork | 10 | 1.0% | 3.586x | [3.469, 3.712] |
| SU2-HaarU4-brickwork | 10 | 3.0% | 2.573x | [2.491, 2.661] |
| SU2-HaarU4-brickwork | 10 | 5.0% | 1.970x | [1.909, 2.034] |
| SU2-HaarU4-brickwork | 12 | 0.0% | 9.584x | [9.360, 9.830] |
| SU2-HaarU4-brickwork | 12 | 1.0% | 6.919x | [6.760, 7.102] |
| SU2-HaarU4-brickwork | 12 | 3.0% | 4.491x | [4.394, 4.604] |
| SU2-HaarU4-brickwork | 12 | 5.0% | 3.127x | [3.059, 3.204] |
| U1-RZ-XY-line | 8 | 0.0% | 1.148x | [1.119, 1.179] |
| U1-RZ-XY-line | 8 | 1.0% | 1.271x | [1.240, 1.304] |
| U1-RZ-XY-line | 8 | 3.0% | 1.254x | [1.227, 1.284] |
| U1-RZ-XY-line | 8 | 5.0% | 1.233x | [1.210, 1.257] |
| U1-RZ-XY-line | 10 | 0.0% | 1.189x | [1.157, 1.222] |
| U1-RZ-XY-line | 10 | 1.0% | 1.269x | [1.239, 1.300] |
| U1-RZ-XY-line | 10 | 3.0% | 1.225x | [1.199, 1.250] |
| U1-RZ-XY-line | 10 | 5.0% | 1.187x | [1.166, 1.208] |
| U1-RZ-XY-line | 12 | 0.0% | 1.210x | [1.187, 1.234] |
| U1-RZ-XY-line | 12 | 1.0% | 1.264x | [1.242, 1.287] |
| U1-RZ-XY-line | 12 | 3.0% | 1.201x | [1.183, 1.220] |
| U1-RZ-XY-line | 12 | 5.0% | 1.150x | [1.135, 1.165] |

Interpretation: the aligned subspace is re-estimated after the specified classical readout-noise channel, so this is a noise-aware geometry test.
