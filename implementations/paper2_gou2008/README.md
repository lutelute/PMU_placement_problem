# Paper 2: Gou (2008) — Generalized Integer Linear Programming

**Full Title:** Generalized Integer Linear Programming Formulation for Optimal PMU Placement

**Authors:** Bei Gou

**Journal:** IEEE Trans. Power Systems, Vol. 23, No. 3, pp. 1099-1104, Aug. 2008

## Key Contributions

- Extends the basic BILP formulation with **depth-of-unobservability** concept
- Introduces handling of **zero-injection buses (ZIB)** in the ILP formulation
- Provides a unified framework for complete and incomplete observability

## Formulations

1. **Complete observability (no ZI):** Standard BILP — `Min Σx_k, s.t. T_PMU·X >= 1`
2. **Depth-of-1 (no ZI):** `A·T_PMU·X >= 1` where A is the branch-to-node incidence matrix
3. **Depth-of-2 (no ZI):** `B·T_PMU·X >= 1` where B covers all triples of connected buses
4. **With ZI:** Remove/relax constraints for zero-injection buses

## Expected Results

### Table I (WITHOUT Zero Injections)

| System   | Complete Obs | Depth-of-1 | Depth-of-2 |
|----------|-------------|-----------|-----------|
| IEEE 14  | 4           | 2         | 2         |
| IEEE 30  | 10          | 4         | 3         |
| IEEE 57  | 17          | 11        | 8         |

### Table II (WITH Zero Injections)

| System   | # ZI | Complete Obs | Depth-of-1 | Depth-of-2 |
|----------|------|-------------|-----------|-----------|
| IEEE 14  | 1    | 3           | 2         | 2         |
| IEEE 30  | 7    | 7           | 4         | 3         |
| IEEE 57  | 17   | 11          | 9         | 8         |

## Implementation Notes

- Complete observability uses `common/solvers.py` (`solve_bilp_basic`, `solve_bilp_with_zib`)
- Depth-of-1 and depth-of-2 solvers are implemented in `verify.py` using new constraint matrices
- The branch-to-node incidence matrix A has M1 rows (one per unique branch)
- The triple incidence matrix B has M2 rows (one per connected triple of buses)

## Running

```bash
cd /tmp/pmu-placement-papers
python implementations/paper2_gou2008/verify.py
```
