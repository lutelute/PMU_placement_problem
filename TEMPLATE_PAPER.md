# Paper Implementation Template

## Directory Structure

```
implementations/paper{N}_{author}{year}/
├── verify.py           # Verification script (REQUIRED)
├── README.md           # Paper summary + results table
├── python/
│   └── solver.py       # Paper-specific algorithm implementation
├── matlab/
│   └── main.m          # MATLAB implementation
├── html/
│   └── index.html      # Interactive demo (解説 + デモ tabs)
└── data/               # Any paper-specific data files
```

## verify.py Template

```python
"""
Verification for Paper N: Author et al. (Year)
"Paper Title"
Journal, Vol. X, No. Y, pp. Z1-Z2, Year.

Table/Figure references for expected results:
  - Table X: [description]
  - Figure Y: [description]
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.test_systems import IEEE_14, IEEE_30, NEW_ENGLAND_39, IEEE_118
from common.verification import PaperVerification
from common.solvers import solve_bilp_verified  # or paper-specific solver


def run_verification():
    v = PaperVerification('paperN', 'Author et al.', YEAR)

    # Register expected results from paper's tables/figures
    v.add_expected_result('IEEE 14-Bus', 'min_pmus', X, table_ref='Table N')
    v.add_expected_result('IEEE 30-Bus', 'min_pmus', Y, table_ref='Table N')

    # Define solver (use paper-specific implementation)
    def solver(n_buses, branches, zero_injection_buses):
        return solve_bilp_verified(n_buses, branches, zero_injection_buses)

    v.run_verification(solver)
    v.generate_report()

    try:
        v.assert_all_pass()
        return True
    except AssertionError as e:
        print(f"\n{e}")
        return False


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
```

## Checklist for Each Paper

- [ ] Read PDF and extract:
  - [ ] Mathematical formulation (objective, constraints)
  - [ ] Algorithm (pseudocode if available)
  - [ ] Test systems used
  - [ ] Results tables with exact numbers
- [ ] Create `verify.py` with expected results from paper
- [ ] Implement paper-specific solver in `python/solver.py`
- [ ] Run verification and confirm all results match
- [ ] Create MATLAB implementation
- [ ] Create interactive HTML demo
- [ ] Update README.md with verification status
- [ ] Register in `run_all_verifications.py`

## Key Principles

1. **Reproducibility first**: Every number in verify.py must reference a specific
   table/figure in the paper.
2. **Exact algorithms**: Implement the paper's method, not a generic solver.
3. **Verified observability**: All solutions checked with Baldwin's Rules 1-3
   (topological observability with KCL propagation at ZIBs).
4. **Standard test systems**: Use `common/test_systems.py` for consistent data.
5. **Tolerance where needed**: Some results may differ by ±1 PMU due to
   ZIB definitions or solver heuristics. Document any discrepancies.
