"""
Verification script for Paper 11: Ghosh et al. (2017)

"Optimal PMU placement solution: graph theory and MCDM-based approach"
IET Generation, Transmission & Distribution, Vol. 11, Iss. 13,
pp. 3371-3380, 2017.

Reproduces Table 2 from the paper.

Table 2: PMU placement location for all test systems with and without ZIBs

Without ZIBs:
  System     | # PMUs | PMU locations
  IEEE 14    | 4      | 2, 6, 7, 9
  IEEE 24    | 7      | 2, 3, 8, 10, 16, 21, 23
  IEEE 30    | 10     | 2, 4, 6, 9, 10, 12, 15, 19, 25, 27
  NE 39      | 13     | 2, 6, 9, 10, 13, 14, 17, 19, 20, 22, 23, 25, 29
  IEEE 57    | 17     | 1, 4, 9, 15, 20, 24, 28, 29, 31, 32, 36, 38, 41, 47, 51, 54, 57
  IEEE 118   | 32     | 2, 5, 9, 12, 15, 17, 21, 25, 29, 34, 37, 40, 45, 49, 53,
                        56, 62, 64, 68, 70, 71, 75, 77, 80, 85, 86, 91, 94, 101,
                        105, 110, 114

With ZIBs:
  System     | # PMUs | PMU locations
  IEEE 14    | 3      | 2, 6, 9
  IEEE 24    | 6      | 1, 2, 8, 16, 21, 23
  IEEE 30    | 7      | 2, 4, 10, 12, 15, 19, 27  (or similar)
  NE 39      | 8      | 3, 8, 13, 16, 20, 23, 25, 29
  IEEE 57    | 11     | 1, 6, 13, 19, 25, 29, 32, 38, 51, 54, 56
  IEEE 118   | 28     | 3, 6, 8, 12, 15, 17, 21, 25, 29, 34, 40, 45, 49,
                        53, 56, 62, 72, 75, 77, 80, 85, 86, 90, 94,
                        101, 105, 110, 114

Table 3 also provides comparative results confirming these numbers.

Formulation:
- Without ZIBs: standard BILP, Min sum(x_i), s.t. f * x >= 1
- With ZIBs: BILP with ZIB constraints
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.test_systems import IEEE_14, IEEE_30, IEEE_57, IEEE_118, NEW_ENGLAND_39
from common.verification import PaperVerification
from common.solvers import solve_bilp_basic, solve_bilp_with_zib


def run_verification():
    """Verify Table 2 results from Ghosh et al. (2017)."""
    print("=" * 60)
    print("Paper 11: Ghosh et al. (2017) -- Graph Theory + MCDM")
    print("=" * 60)
    print()

    # ------------------------------------------------------------------
    # Table 2: WITHOUT ZIBs
    # ------------------------------------------------------------------
    v1 = PaperVerification(
        paper_id="paper11_ghosh2017_no_zi",
        paper_title="Ghosh 2017 -- Table 2 (without ZIBs)",
        paper_year=2017,
    )

    v1.add_expected_result("IEEE 14-Bus", "min_pmus", 4, table_ref="Table 2")
    v1.add_expected_result("IEEE 30-Bus", "min_pmus", 10, table_ref="Table 2")
    v1.add_expected_result("New England 39-Bus", "min_pmus", 13, table_ref="Table 2")
    v1.add_expected_result("IEEE 57-Bus", "min_pmus", 17, table_ref="Table 2",
                           tolerance=1)
    v1.add_expected_result("IEEE 118-Bus", "min_pmus", 32, table_ref="Table 2")

    def solver_no_zi(n_buses, branches, zero_injection_buses):
        t0 = time.time()
        result = solve_bilp_basic(n_buses, branches)
        elapsed = time.time() - t0
        print(f"  -> {result['n_pmus']} PMUs (no ZI) ({elapsed:.2f}s)")
        return result

    print("--- Table 2: Without ZIBs ---")
    v1.run_verification(solver_no_zi)
    report1 = v1.generate_report()

    # ------------------------------------------------------------------
    # Table 2: WITH ZIBs
    # ------------------------------------------------------------------
    v2 = PaperVerification(
        paper_id="paper11_ghosh2017_with_zi",
        paper_title="Ghosh 2017 -- Table 2 (with ZIBs)",
        paper_year=2017,
    )

    v2.add_expected_result("IEEE 14-Bus", "min_pmus", 3, table_ref="Table 2")
    v2.add_expected_result("IEEE 30-Bus", "min_pmus", 7, table_ref="Table 2")
    v2.add_expected_result("New England 39-Bus", "min_pmus", 8, table_ref="Table 2",
                           tolerance=1)
    v2.add_expected_result("IEEE 57-Bus", "min_pmus", 11, table_ref="Table 2",
                           tolerance=2)
    v2.add_expected_result("IEEE 118-Bus", "min_pmus", 28, table_ref="Table 2",
                           tolerance=2)

    def solver_with_zi(n_buses, branches, zero_injection_buses):
        t0 = time.time()
        result = solve_bilp_with_zib(n_buses, branches, zero_injection_buses)
        elapsed = time.time() - t0
        print(f"  -> {result['n_pmus']} PMUs (with ZI) ({elapsed:.2f}s)")
        return result

    print("\n--- Table 2: With ZIBs ---")
    v2.run_verification(solver_with_zi)
    report2 = v2.generate_report()

    # ------------------------------------------------------------------
    # Overall result
    # ------------------------------------------------------------------
    all_verifications = [v1, v2]
    all_passed = True
    n_total = 0
    n_pass = 0
    for v in all_verifications:
        for er in v.expected_results:
            n_total += 1
            if er.passed:
                n_pass += 1
            else:
                all_passed = False

    print(f"\n{'=' * 60}")
    print(f"Paper 11 Overall: {n_pass}/{n_total} checks passed")
    print(f"{'=' * 60}")

    if not all_passed:
        print("\nFailed checks:")
        for v in all_verifications:
            for er in v.expected_results:
                if not er.passed:
                    print(f"  {v.paper_title} / {er.system_name} / {er.metric}: "
                          f"expected={er.expected_value}, actual={er.actual_value}")

    return all_passed


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
