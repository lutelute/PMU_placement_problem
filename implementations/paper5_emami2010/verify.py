"""
Verification script for Paper 5: Emami & Abur (2010)

"Robust Measurement Design by Placing Synchronized Phasor
Measurements on Network Branches"
IEEE Trans. Power Systems, Vol. 25, No. 1, pp. 38-43, Feb. 2010.

This paper introduces "branch PMUs" - PMUs placed on branches (lines)
rather than buses. A branch PMU monitors a single branch by measuring
the voltage and current phasors at one end of the monitored branch.

Key differences from bus PMU model:
- Decision variable x_i is per-branch, not per-bus
- Each branch PMU observes the two endpoint buses of its branch
- Minimum branch PMUs for N-bus system: ceil((N-1)/2)
- Bus-to-branch incidence matrix T replaces bus connectivity matrix

Results from the paper:

Table I: Optimal Branch PMU Placement for IEEE 14-Bus System
  7 branch PMUs placed on branches:
    PMU 1: branch (2,1)
    PMU 2: branch (3,4)
    PMU 3: branch (5,6)
    PMU 4: branch (7,8)
    PMU 5: branch (9,14)
    PMU 6: branch (10,11)
    PMU 7: branch (12,13)

Table II: Original and Backup PMU Placements for IEEE 30-Bus System
  15 original branch PMUs + additional backup PMUs

For verification:
1. We implement the branch PMU BILP formulation
2. Verify minimum branch PMU count for IEEE 14-bus = 7
3. Verify minimum branch PMU count for IEEE 30-bus = 15
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
from scipy.optimize import linprog

from common.test_systems import IEEE_14, IEEE_30
from common.verification import PaperVerification
from common.observability import _adjacency


# ===================================================================
# Paper-specific solver: Branch PMU placement
# ===================================================================

def build_bus_branch_incidence(n_buses, branches):
    """Build the bus-to-branch incidence matrix T (N x L).

    T[i][j] = 1 if bus (i+1) is an endpoint of branch j, 0 otherwise.

    This is the matrix T from eq. (1) of Emami 2010.
    Each branch PMU placed on branch j makes both endpoint buses observable.
    """
    # Deduplicate branches, keeping order
    unique_branches = []
    seen = set()
    for i, j in branches:
        key = (min(i, j), max(i, j))
        if key not in seen:
            seen.add(key)
            unique_branches.append((i, j))

    n_branches = len(unique_branches)
    T = np.zeros((n_buses, n_branches), dtype=int)
    for idx, (bi, bj) in enumerate(unique_branches):
        T[bi - 1, idx] = 1
        T[bj - 1, idx] = 1

    return T, unique_branches


def solve_branch_pmu_basic(n_buses, branches):
    """Solve the branch PMU placement problem (Emami 2010, eq. 1).

    min  sum(rho_i * x_i)  for i = 1..L
    s.t. T * X >= 1  (each bus observed by at least one branch PMU)
         x_i in {0, 1}

    where L is the number of branches, T is bus-branch incidence matrix.
    Assumes uniform cost rho_i = 1.
    """
    T, unique_branches = build_bus_branch_incidence(n_buses, branches)
    n_branches = len(unique_branches)

    c = np.ones(n_branches)
    A_ub = -T.astype(float)
    b_ub = -np.ones(n_buses)
    bounds = [(0, 1)] * n_branches
    integrality = np.ones(n_branches)

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
                     integrality=integrality, method="highs")

    if result.success:
        x = np.round(result.x).astype(int)
        pmu_branches = []
        for idx in range(n_branches):
            if x[idx] == 1:
                pmu_branches.append(unique_branches[idx])
        return {
            "n_pmus": int(sum(x)),
            "pmu_buses": [],  # not applicable for branch PMUs
            "pmu_branches": pmu_branches,
            "objective": result.fun,
            "success": True
        }
    return {"n_pmus": None, "pmu_buses": [], "pmu_branches": [],
            "objective": None, "success": False}


def solve_branch_pmu_backup(n_buses, branches, original_pmu_branches):
    """Solve for backup branch PMUs (Emami 2010, Section V).

    Given the original set of branch PMUs, find additional branch PMUs
    to serve as backups in case of PMU failure.

    The paper's approach:
    1. Partition branches into D (assigned to original PMUs) and P (remaining)
    2. If P has null rows, add branches from D to P
    3. Solve IP with modified P matrix to find backup set
    """
    # For simplicity, we solve a redundancy version:
    # each bus must be covered by at least 2 branch PMUs
    T, unique_branches = build_bus_branch_incidence(n_buses, branches)
    n_branches = len(unique_branches)

    c = np.ones(n_branches)
    A_ub = -T.astype(float)
    b_ub = -np.ones(n_buses) * 2  # each bus covered by >= 2 PMUs
    bounds = [(0, 1)] * n_branches
    integrality = np.ones(n_branches)

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
                     integrality=integrality, method="highs")

    if result.success:
        x = np.round(result.x).astype(int)
        pmu_branches = []
        for idx in range(n_branches):
            if x[idx] == 1:
                pmu_branches.append(unique_branches[idx])
        return {
            "n_pmus": int(sum(x)),
            "pmu_branches": pmu_branches,
            "objective": result.fun,
            "success": True
        }
    return {"n_pmus": None, "pmu_branches": [],
            "objective": None, "success": False}


def run_verification():
    """Verify results from Emami & Abur (2010)."""
    print("=" * 60)
    print("Paper 5: Emami & Abur (2010) — Branch PMU Placement")
    print("=" * 60)
    print()

    all_passed = True

    # ------------------------------------------------------------------
    # Part 1: Basic branch PMU placement (observability only)
    # Table I: IEEE 14-bus = 7 branch PMUs
    # Table II: IEEE 30-bus = 15 original branch PMUs
    # ------------------------------------------------------------------
    v1 = PaperVerification(
        paper_id="paper5_emami2010_branch_pmu",
        paper_title="Emami 2010 — Branch PMU Observability",
        paper_year=2010,
    )
    v1.add_expected_result("IEEE 14-Bus", "min_pmus", 7,
                           table_ref="Table I")
    v1.add_expected_result("IEEE 30-Bus", "min_pmus", 15,
                           table_ref="Table II")

    def solver_branch_pmu(n_buses, branches, zero_injection_buses):
        t0 = time.time()
        result = solve_branch_pmu_basic(n_buses, branches)
        elapsed = time.time() - t0
        print(f"  -> {result['n_pmus']} branch PMUs ({elapsed:.2f}s)")
        if result['pmu_branches']:
            print(f"     Branches: {result['pmu_branches']}")
        return result

    print("--- Branch PMU Placement (no ZI, no backup) ---")
    v1.run_verification(solver_branch_pmu)
    report1 = v1.generate_report()

    for er in v1.expected_results:
        if not er.passed:
            all_passed = False

    # ------------------------------------------------------------------
    # Part 2: Theoretical minimum check
    # For N buses, minimum branch PMUs = ceil((N-1)/2)
    # IEEE 14: ceil(13/2) = 7 (matches)
    # IEEE 30: ceil(29/2) = 15 (matches)
    # ------------------------------------------------------------------
    print("\n--- Theoretical Minimum Verification ---")
    import math
    for sys_name, sys_data in [("IEEE 14-Bus", IEEE_14), ("IEEE 30-Bus", IEEE_30)]:
        n = len(sys_data["buses"])
        theoretical_min = math.ceil((n - 1) / 2)
        print(f"  {sys_name}: ceil(({n}-1)/2) = {theoretical_min}")

    # ------------------------------------------------------------------
    # Part 3: Verify specific branch locations for IEEE 14
    # Paper Table I: branches at (2,1), (3,4), (5,6), (7,8), (9,14), (10,11), (12,13)
    # ------------------------------------------------------------------
    v2 = PaperVerification(
        paper_id="paper5_emami2010_14bus_locations",
        paper_title="Emami 2010 — IEEE 14-Bus Branch Locations",
        paper_year=2010,
    )

    # Verify that 7 branch PMUs cover all 14 buses
    paper_branches_14 = [(2, 1), (3, 4), (5, 6), (7, 8), (9, 14), (10, 11), (12, 13)]
    covered_buses = set()
    for bi, bj in paper_branches_14:
        covered_buses.add(bi)
        covered_buses.add(bj)
    all_14_covered = covered_buses == set(range(1, 15))
    print(f"\n  Paper's 7 branches cover all 14 buses: {all_14_covered}")
    print(f"  Covered buses: {sorted(covered_buses)}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    all_verifications = [v1]
    n_total = sum(len(v.expected_results) for v in all_verifications)
    n_pass = sum(1 for v in all_verifications for er in v.expected_results if er.passed)

    print(f"\n{'=' * 60}")
    print(f"Paper 5 Overall: {n_pass}/{n_total} checks passed")
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
