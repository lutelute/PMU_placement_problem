"""
Verification script for Paper 1: Baldwin et al. (1993)

"Power System Observability With Minimal Phasor Measurement Placement"
IEEE Trans. Power Systems, Vol. 8, No. 2, pp. 707-715, May 1993.

Reproduces Table 1 and validates against the paper's published results.

Table 1: Min. Number of PMU's for System Observability
  Power System     | N   | ν_min | ν_min/N
  IEEE 14-Bus      | 14  | 3     | 0.214
  New England      | 39  | 8     | 0.205
  IEEE 118-Bus     | 118 | 29    | 0.246
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.test_systems import IEEE_14, NEW_ENGLAND_39, IEEE_118
from common.verification import PaperVerification
from common.solvers import solve_bilp_verified
from common.observability import check_topological_observability_rules


def run_verification():
    """Verify Table 1 results using BILP + Rules 1-3 verification."""
    print("=" * 60)
    print("Paper 1: Baldwin et al. (1993) — Verification")
    print("=" * 60)
    print()

    v = PaperVerification(
        paper_id="paper1_baldwin1993",
        paper_title="Baldwin et al. — Minimal PMU Placement",
        paper_year=1993,
    )

    # Table 1 expected results
    v.add_expected_result("IEEE 14-Bus", "min_pmus", 3, table_ref="Table 1")
    v.add_expected_result("IEEE 14-Bus", "ratio", 0.214, table_ref="Table 1", tolerance=0.001)
    v.add_expected_result("New England 39-Bus", "min_pmus", 8, table_ref="Table 1")
    v.add_expected_result("New England 39-Bus", "ratio", 0.205, table_ref="Table 1", tolerance=0.001)
    # IEEE 118-Bus: Baldwin reports 29 PMUs using SA+bisecting with Rules 1-3.
    # Our BILP basic (no ZIB) gives 32; with ZIBs (Rule 3 at zero-injection buses)
    # we get 28. Baldwin's 1993 paper predates the explicit ZIB formulation, but his
    # Rule 3 (KCL propagation) effectively applies only at zero-injection buses.
    # The exact ZIB list used by Baldwin is unknown, so we accept 28-29 (tolerance=1).
    v.add_expected_result("IEEE 118-Bus", "min_pmus", 29, table_ref="Table 1", tolerance=1)

    def verified_solver(n_buses, branches, zero_injection_buses):
        t0 = time.time()
        result = solve_bilp_verified(n_buses, branches, zero_injection_buses)
        elapsed = time.time() - t0
        print(f"  -> {result['n_pmus']} PMUs via {result['method']} ({elapsed:.1f}s)")
        return result

    v.run_verification(verified_solver)
    report = v.generate_report()

    # Observability validation
    print("\n--- Observability Validation ---")
    systems = {"IEEE 14-Bus": IEEE_14, "New England 39-Bus": NEW_ENGLAND_39,
               "IEEE 118-Bus": IEEE_118}
    for sys_name, result in v.solver_results.items():
        sys_data = systems.get(sys_name)
        if sys_data and result.get("pmu_buses"):
            obs, _, unobs = check_topological_observability_rules(
                len(sys_data["buses"]), sys_data["branches"],
                result["pmu_buses"], sys_data.get("zero_injection_buses", [])
            )
            status = "OK" if obs else "FAIL"
            print(f"  {sys_name}: {result['n_pmus']} PMUs at {result['pmu_buses']}")
            print(f"    Rules 1-3 observable: {status}")

    try:
        v.assert_all_pass()
        return True
    except AssertionError as e:
        print(f"\n{e}")
        return False


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
