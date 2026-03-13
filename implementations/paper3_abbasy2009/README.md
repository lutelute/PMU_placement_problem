# Paper 3: Abbasy & Ismail (2009) — Unified Approach

**Full Title:** A Unified Approach for the Optimal PMU Location for Power System State Estimation

**Authors:** Nabil H. Abbasy, Hanafy Mahmoud Ismail

**Journal:** IEEE Trans. Power Systems, Vol. 24, No. 2, pp. 806-813, May 2009

## Key Contributions

- **Augmented Bus Merging (ABM) method** for incorporating conventional measurements
- **Local Redundancy (LR) method** for PMU loss (N-1 contingency)
- Unified BILP handling conventional measurements + PMU loss scenarios
- Applied to IEEE 14, 30, 57, 118 bus systems

## Methods

1. **Individual Bus Merging (IBM):** Merges injection bus with associate buses
2. **Augmented Bus Merging (ABM):** Proposed alternative using permutation matrix P
3. **Primary and Backup (P&B):** Two independent PMU sets for PMU loss
4. **Local Redundancy (LR):** Set b >= 2 for single PMU loss tolerance

## Expected Results

### Without Zero Injections (standard BILP)
| System    | PMUs |
|-----------|------|
| IEEE 14   | 4    |
| IEEE 30   | 10   |
| IEEE 57   | 17   |
| IEEE 118  | ~32  |

### With Zero Injections
| System    | PMUs |
|-----------|------|
| IEEE 14   | 3    |
| IEEE 30   | 7    |
| IEEE 57   | 13   |
| IEEE 118  | 29   |

### Single PMU Loss (IEEE 14, no ZI)
| Method | PMUs |
|--------|------|
| P&B    | 9    |
| LR     | 9    |

## Implementation Notes

- Standard BILP results use `common/solvers.py`
- PMU loss (LR method) implemented as BILP with `b >= 2`
- ZIB lists in the paper (Table VI) differ from our standard lists
- Tolerance applied for systems where ZIB definitions may vary

## Running

```bash
cd /tmp/pmu-placement-papers
python implementations/paper3_abbasy2009/verify.py
```
