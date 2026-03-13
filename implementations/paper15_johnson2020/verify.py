"""
Verification script for Paper 15: Johnson and Moger (2020)

"A critical review of methods for optimal placement of phasor
measurement units"
Int Trans Electr Energ Syst., Vol. 31, e12698, 2021.
DOI: 10.1002/2050-7038.12698

This is a REVIEW paper. It consolidates OPP studies from 2003-2020.
The paper provides:
- Tables 1-2: Conventional methods (ILP, BILP, NLP, etc.) with test systems
- Tables 3-5: Heuristic, meta-heuristic, and hybrid methods
- Table 6: Comparison of method categories

The paper does NOT include specific PMU count tables.
It discusses constraint formulations (Sections 2.2.1-2.2.15) and
classifies methods, but the results are qualitative comparisons.

Since no specific numerical PMU count tables are provided, we verify
the well-known optimal results that the surveyed papers target.
The paper mentions IEEE 14, 24, 30, 39, 57, 118 as standard test systems.

Consensus results from the literature this review covers:
  Without ZI:                    With ZI:
    IEEE 14:  4 PMUs              IEEE 14:  3 PMUs
    IEEE 30:  10 PMUs             IEEE 30:  7 PMUs
    IEEE 57:  17 PMUs             IEEE 57:  11 PMUs
    IEEE 118: 32 PMUs             IEEE 118: 28 PMUs
    NE 39:    13 PMUs             NE 39:    8 PMUs
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.test_systems import IEEE_14, IEEE_30, IEEE_57, IEEE_118, NEW_ENGLAND_39
from common.verification import PaperVerification
from common.solvers import solve_bilp_basic, solve_bilp_with_zib


def run_verification():
    """Verify consensus results referenced by the Johnson 2020 review."""
    print("=" * 60)
    print("Paper 15: Johnson & Moger (2020) -- Critical Review of Methods")
    print("=" * 60)
    print()
    print("This is a review paper. Verifying that our solver reproduces")
    print("the well-known optimal results used as benchmarks in the")
    print("surveyed literature.\n")

    # ------------------------------------------------------------------
    # Consensus: WITHOUT Zero Injections
    # ------------------------------------------------------------------
    v1 = PaperVerification(
        paper_id="paper15_johnson2020_consensus_no_zi",
        paper_title="Johnson 2020 Review -- Consensus (no ZI)",
        paper_year=2020,
    )

    v1.add_expected_result("IEEE 14-Bus", "min_pmus", 4,
                           table_ref="Literature consensus")
    v1.add_expected_result("IEEE 30-Bus", "min_pmus", 10,
                           table_ref="Literature consensus")
    v1.add_expected_result("New England 39-Bus", "min_pmus", 13,
                           table_ref="Literature consensus")
    v1.add_expected_result("IEEE 57-Bus", "min_pmus", 17,
                           table_ref="Literature consensus", tolerance=1)
    v1.add_expected_result("IEEE 118-Bus", "min_pmus", 32,
                           table_ref="Literature consensus", tolerance=2)

    def solver_no_zi(n_buses, branches, zero_injection_buses):
        t0 = time.time()
        result = solve_bilp_basic(n_buses, branches)
        elapsed = time.time() - t0
        print(f"  -> {result['n_pmus']} PMUs (no ZI) ({elapsed:.2f}s)")
        return result

    print("--- Consensus: Without ZI ---")
    v1.run_verification(solver_no_zi)
    report1 = v1.generate_report()

    # ------------------------------------------------------------------
    # Consensus: WITH Zero Injections
    # ------------------------------------------------------------------
    v2 = PaperVerification(
        paper_id="paper15_johnson2020_consensus_with_zi",
        paper_title="Johnson 2020 Review -- Consensus (with ZI)",
        paper_year=2020,
    )

    v2.add_expected_result("IEEE 14-Bus", "min_pmus", 3,
                           table_ref="Literature consensus")
    v2.add_expected_result("IEEE 30-Bus", "min_pmus", 7,
                           table_ref="Literature consensus")
    v2.add_expected_result("New England 39-Bus", "min_pmus", 8,
                           table_ref="Literature consensus", tolerance=1)
    v2.add_expected_result("IEEE 57-Bus", "min_pmus", 11,
                           table_ref="Literature consensus", tolerance=2)
    v2.add_expected_result("IEEE 118-Bus", "min_pmus", 28,
                           table_ref="Literature consensus", tolerance=2)

    def solver_with_zi(n_buses, branches, zero_injection_buses):
        t0 = time.time()
        result = solve_bilp_with_zib(n_buses, branches, zero_injection_buses)
        elapsed = time.time() - t0
        print(f"  -> {result['n_pmus']} PMUs (with ZI) ({elapsed:.2f}s)")
        return result

    print("\n--- Consensus: With ZI ---")
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
    print(f"Paper 15 Overall: {n_pass}/{n_total} checks passed")
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
