# Paper 4: Gou & Kavasseri (2014) — Observability + Bad Data Detection

**Full Title:** Unified PMU Placement for Observability and Bad Data Detection in State Estimation

**Authors:** Bei Gou, Rajesh G. Kavasseri

**Journal:** IEEE Trans. Power Systems, Vol. 29, No. 6, pp. 2573-2580, Nov. 2014

## Key Contributions

- **Reduced-order ILP** for observability based on rank deficiency of gain matrix
- **Critical measurement identification** via sensitivity matrix K
- **Critical pair identification** via Lemma for Critical Pairs
- **Unified Algorithm III** combining observability + bad data detection iteratively

## Algorithms

### Algorithm I (Observability)
1. Compute D from LDL^T factorization of gain matrix G = H^T H
2. Identify zero diagonals in D -> candidate buses for PMU placement
3. Solve reduced ILP (dimension governed by rank deficiency, not bus count)

### Algorithm II (Bad Data Detection)
1. Form sensitivity matrix K = H_r * H_e^{-1}
2. Identify critical measurements (null columns in K)
3. Identify critical pairs (columns with single non-zero entry)
4. Place PMUs to convert critical sets to non-critical

### Algorithm III (Unified)
Iterate Algorithms I and II until system is observable AND no critical measurements/pairs exist.

## Expected Results

### IEEE 14-Bus (with 24 branch flow + 8 injection measurements)
| Iteration | Action | PMU Buses |
|-----------|--------|-----------|
| v=0 | Observability | 13 |
| v=1 | Fix critical meas | 9 |
| v=2 | Fix critical pairs | 7, 9, 11 |
| **Final** | **All** | **7, 9, 11, 13** (4 locations) |

### IEEE 118-Bus (with 179 branch flow + 38 injection measurements)
| Iteration | PMU Buses |
|-----------|-----------|
| v=0 | 10, 32, 75, 80 (4 buses) |
| v=1 | 10, 12, 32, 80, 116 (5 buses) |
| v=2 | 11, 12, 22, 23, 27, 67, 68, 75 (8 buses) |

## Implementation Notes

- Full Jacobian-based analysis (LDL^T factorization, sensitivity matrix K) is not implemented
- Verification uses paper-reported results for the conventional-measurement cases
- Baseline BILP (no conventional measurements) is verified computationally
- The reduced ILP is a key advantage: dimension = rank_deficiency x candidate_buses

## Running

```bash
cd /tmp/pmu-placement-papers
python implementations/paper4_gou2014/verify.py
```
