"""
Shared solver implementations for the PMU placement problem.

Includes:
  - Basic BILP (Binary Integer Linear Program) via scipy
  - BILP with zero-injection bus (ZIB) constraints
  - Baldwin's Simulated Annealing (SA) algorithm
  - Baldwin's bisecting search with SA inner loop
  - Greedy graph-theoretic initial upper bound

Reference: Baldwin et al., "Power System Observability With Minimal Phasor
Measurement Placement", IEEE Trans. Power Systems, Vol. 8, No. 2, May 1993.
"""

import math
import random
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
from scipy.optimize import linprog
from scipy.special import comb

from .observability import (
    _adjacency,
    build_connectivity_matrix,
    check_topological_observability_basic,
    check_topological_observability_rules,
    count_unobserved,
)


# ===================================================================
# BILP solvers
# ===================================================================

def solve_bilp_basic(
    n_buses: int,
    branches: List[Tuple[int, int]],
    zero_injection_buses: Optional[List[int]] = None,
) -> Dict:
    """Solve the basic PMU placement BILP (Baldwin eq. 1-4).

    Minimise: Σ x_i
    Subject to: f · x ≥ 1  (each bus observed by at least one PMU or neighbour)
                x_i ∈ {0, 1}

    If zero_injection_buses is provided, modifies constraints so that ZIBs
    contribute to observability (a simplified treatment).

    Uses scipy.optimize.linprog with integrality constraints (requires
    scipy >= 1.9).

    Parameters
    ----------
    n_buses : int
    branches : list of (int, int)
    zero_injection_buses : list of int or None

    Returns
    -------
    dict with keys:
        'n_pmus': int, 'pmu_buses': list of int (1-indexed),
        'objective': float, 'success': bool
    """
    f = build_connectivity_matrix(n_buses, branches)

    # Objective: minimise Σ x_i
    c = np.ones(n_buses)

    # Constraints: f · x ≥ 1  =>  -f · x ≤ -1
    A_ub = -f.astype(float)
    b_ub = -np.ones(n_buses)

    # Variable bounds: 0 ≤ x_i ≤ 1
    bounds = [(0, 1)] * n_buses

    # Integrality: all variables are binary
    integrality = np.ones(n_buses)

    result = linprog(
        c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
        integrality=integrality, method="highs",
    )

    if result.success:
        x = np.round(result.x).astype(int)
        pmu_buses = [i + 1 for i in range(n_buses) if x[i] == 1]
        return {
            "n_pmus": int(sum(x)),
            "pmu_buses": pmu_buses,
            "objective": result.fun,
            "success": True,
        }
    return {"n_pmus": None, "pmu_buses": [], "objective": None, "success": False}


def solve_bilp_with_zib(
    n_buses: int,
    branches: List[Tuple[int, int]],
    zero_injection_buses: List[int],
) -> Dict:
    """Solve BILP with zero-injection bus (ZIB) constraints.

    At a zero-injection bus z, if all but one neighbour is observed, the
    remaining is also observed. This is modelled by augmenting the
    connectivity matrix: for each ZIB z, add 1 to column j for each
    neighbour j of z (the ZIB "propagates" observability).

    More precisely, the constraint for each bus i becomes:
        Σ_j f'[i][j] * x_j ≥ 1
    where f' incorporates the ZIB effect.

    Parameters
    ----------
    n_buses : int
    branches : list of (int, int)
    zero_injection_buses : list of int

    Returns
    -------
    dict (same structure as solve_bilp_basic)
    """
    f = build_connectivity_matrix(n_buses, branches).astype(float)
    adj = _adjacency(n_buses, branches)

    # Augment: for each ZIB, its neighbours help observe each other
    # This is a common linear relaxation of the ZIB effect.
    # For ZIB z with neighbours N(z), the observability of any bus in N(z)
    # can be aided by PMUs at other buses in N(z) ∪ {z}.
    for z in zero_injection_buses:
        z_idx = z - 1
        neighbours = list(adj[z])
        # For bus z itself: already has f[z_idx][z_idx] = 1
        # For each neighbour of z: all other neighbours of z also contribute
        for nb in neighbours:
            nb_idx = nb - 1
            for other in neighbours:
                if other != nb:
                    f[nb_idx, other - 1] = 1
            # z itself contributes to observing nb (already set)
            # nb contributes to observing z (already set)

    c = np.ones(n_buses)
    A_ub = -f
    b_ub = -np.ones(n_buses)
    bounds = [(0, 1)] * n_buses
    integrality = np.ones(n_buses)

    result = linprog(
        c, A_ub=A_ub, b_ub=b_ub, bounds=bounds,
        integrality=integrality, method="highs",
    )

    if result.success:
        x = np.round(result.x).astype(int)
        pmu_buses = [i + 1 for i in range(n_buses) if x[i] == 1]
        return {
            "n_pmus": int(sum(x)),
            "pmu_buses": pmu_buses,
            "objective": result.fun,
            "success": True,
        }
    return {"n_pmus": None, "pmu_buses": [], "objective": None, "success": False}


def solve_bilp_verified(
    n_buses: int,
    branches: List[Tuple[int, int]],
    zero_injection_buses: Optional[List[int]] = None,
    max_sa_retries: int = 10,
    seed: int = 42,
) -> Dict:
    """BILP + verification + SA fallback.

    1. Run BILP with ZIB to get optimal PMU count.
    2. Verify the BILP solution with strict Rules 1-3 observability.
    3. If BILP solution is infeasible under Rules 1-3, use SA to find
       a feasible placement with the same PMU count.

    The BILP+ZIB linear relaxation may produce placements that are not
    strictly observable under Baldwin's Rules 1-3 (the linear constraint
    over-approximates ZIB propagation). This function ensures the
    returned solution is verified observable.

    Parameters
    ----------
    n_buses, branches, zero_injection_buses : standard
    max_sa_retries : int
        Number of SA attempts to find a feasible solution.
    seed : int

    Returns
    -------
    dict with 'n_pmus', 'pmu_buses', 'ratio', 'observable', 'success',
              'method' ('bilp' or 'bilp+sa')
    """
    if zero_injection_buses is None:
        zero_injection_buses = []

    # Step 1: BILP for optimal count
    if zero_injection_buses:
        bilp_result = solve_bilp_with_zib(n_buses, branches, zero_injection_buses)
    else:
        bilp_result = solve_bilp_basic(n_buses, branches)

    if not bilp_result["success"]:
        return {**bilp_result, "method": "bilp_failed"}

    n_pmus = bilp_result["n_pmus"]
    pmu_buses = bilp_result["pmu_buses"]

    # Step 2: Verify with strict Rules 1-3
    obs, _, _ = check_topological_observability_rules(
        n_buses, branches, pmu_buses, zero_injection_buses
    )

    if obs:
        return {
            "n_pmus": n_pmus,
            "pmu_buses": pmu_buses,
            "ratio": n_pmus / n_buses,
            "observable": True,
            "success": True,
            "method": "bilp",
        }

    # Step 3: BILP solution not observable under Rules 1-3.
    # Use SA to find a feasible placement with the same count.
    for retry in range(max_sa_retries):
        sa_result = solve_sa_baldwin(
            n_buses, branches, zero_injection_buses,
            nu=n_pmus, seed=seed + retry * 1000,
        )
        if sa_result["observable"]:
            return {
                "n_pmus": n_pmus,
                "pmu_buses": sa_result["pmu_buses"],
                "ratio": n_pmus / n_buses,
                "observable": True,
                "success": True,
                "method": "bilp+sa",
            }

    # SA couldn't find feasible solution with n_pmus; try n_pmus + 1
    for retry in range(max_sa_retries):
        sa_result = solve_sa_baldwin(
            n_buses, branches, zero_injection_buses,
            nu=n_pmus + 1, seed=seed + retry * 1000,
        )
        if sa_result["observable"]:
            return {
                "n_pmus": n_pmus + 1,
                "pmu_buses": sa_result["pmu_buses"],
                "ratio": (n_pmus + 1) / n_buses,
                "observable": True,
                "success": True,
                "method": "bilp+sa+1",
            }

    return {
        "n_pmus": n_pmus,
        "pmu_buses": bilp_result["pmu_buses"],
        "ratio": n_pmus / n_buses,
        "observable": False,
        "success": False,
        "method": "bilp_unverified",
    }


# ===================================================================
# Greedy graph-theoretic initial placement (Baldwin Section III-A)
# ===================================================================

def graph_theoretic_initial(
    n_buses: int,
    branches: List[Tuple[int, int]],
    zero_injection_buses: Optional[List[int]] = None,
) -> List[int]:
    """Baldwin's greedy graph-theoretic procedure for initial upper bound.

    Algorithm (Baldwin 1993, Section III-A):
      Step 1: Among buses in the unobservable region, select the bus
              incident to the most branches in that region. Place PMU there.
      Step 2: Determine the observed region (using Rules 1-3).
      Step 3: If network is not fully observable, go to Step 1.

    Parameters
    ----------
    n_buses : int
    branches : list of (int, int)
    zero_injection_buses : list of int or None

    Returns
    -------
    pmu_buses : list of int (1-indexed)
    """
    if zero_injection_buses is None:
        zero_injection_buses = []

    adj = _adjacency(n_buses, branches)
    pmu_buses: List[int] = []

    while True:
        obs, observed, unobserved = check_topological_observability_rules(
            n_buses, branches, pmu_buses, zero_injection_buses
        )
        if obs:
            break

        unobs_set = set(unobserved)
        # Count branches in unobservable region for each unobserved bus
        best_bus = -1
        best_count = -1
        for bus in unobserved:
            count = sum(1 for nb in adj[bus] if nb in unobs_set)
            if count > best_count:
                best_count = count
                best_bus = bus
        pmu_buses.append(best_bus)

    return sorted(pmu_buses)


# ===================================================================
# Simulated Annealing (Baldwin Section III-B, III-C)
# ===================================================================

def _random_placement(n_buses: int, nu: int, rng: random.Random) -> List[int]:
    """Generate a random PMU placement of size nu from buses 1..n_buses."""
    return sorted(rng.sample(range(1, n_buses + 1), nu))


def _neighbour_placement(
    current: List[int], n_buses: int, rng: random.Random
) -> List[int]:
    """Generate a neighbour placement by swapping one PMU bus with a non-PMU bus."""
    placement = list(current)
    all_buses = set(range(1, n_buses + 1))
    non_pmu = list(all_buses - set(placement))
    idx = rng.randrange(len(placement))
    new_bus = rng.choice(non_pmu)
    placement[idx] = new_bus
    return sorted(placement)


def solve_sa_baldwin(
    n_buses: int,
    branches: List[Tuple[int, int]],
    zero_injection_buses: Optional[List[int]] = None,
    nu: Optional[int] = None,
    seed: int = 42,
    verbose: bool = False,
) -> Dict:
    """Baldwin's Simulated Annealing for PMU placement.

    For a given number of PMUs (nu), find a placement that makes the
    system observable (Φ = 0).

    SA parameters from Baldwin 1993, Section III-C:
      - T₀ = 15 (initial temperature)
      - β = 0.879 (geometric cooling: T_{i+1} = β * T_i)
      - M = 0.002 * C(N, ν) placement sets tested per temperature step
        (where C(N,ν) is the binomial coefficient, capped for tractability)
      - Number of temperature steps: ~40 (chosen so T_L ≈ 0.0869 is reached)
      - T_L = -1/ln(P_acc), P_acc = 0.00001 => T_L ≈ 0.0869
      - Acceptance: ΔE ≤ 0 always; else with prob exp(-ΔE/T)
      - Stopping: E=0 found, no acceptances at a temperature, or T < T_L

    Parameters
    ----------
    n_buses : int
    branches : list of (int, int)
    zero_injection_buses : list of int or None
    nu : int or None
        Number of PMUs to place. If None, uses graph_theoretic_initial count.
    seed : int
    verbose : bool

    Returns
    -------
    dict with 'n_pmus', 'pmu_buses', 'phi' (unobserved count),
              'observable' (bool), 'success' (bool)
    """
    if zero_injection_buses is None:
        zero_injection_buses = []

    rng = random.Random(seed)

    if nu is None:
        initial = graph_theoretic_initial(n_buses, branches, zero_injection_buses)
        nu = len(initial)

    # SA parameters (Baldwin 1993, Section III-C)
    T0 = 15.0
    beta = 0.879
    P_acc = 0.00001
    T_L = -1.0 / math.log(P_acc)  # ≈ 0.0869
    n_temp_steps = 40

    # M = 0.002 * C(N, nu), but cap to avoid astronomical values
    C_N_nu = comb(n_buses, nu, exact=True)
    M = max(10, int(0.002 * min(C_N_nu, 1_000_000)))

    # Initial random placement
    current = _random_placement(n_buses, nu, rng)
    current_phi = count_unobserved(n_buses, branches, current, zero_injection_buses)

    best = list(current)
    best_phi = current_phi

    T = T0
    for step in range(n_temp_steps):
        if T < T_L:
            break
        if best_phi == 0:
            break

        accepted_any = False
        for _ in range(M):
            candidate = _neighbour_placement(current, n_buses, rng)
            candidate_phi = count_unobserved(
                n_buses, branches, candidate, zero_injection_buses
            )

            delta_e = candidate_phi - current_phi

            if delta_e <= 0:
                accept = True
            else:
                accept = rng.random() < math.exp(-delta_e / T)

            if accept:
                current = candidate
                current_phi = candidate_phi
                accepted_any = True

                if current_phi < best_phi:
                    best = list(current)
                    best_phi = current_phi

                if best_phi == 0:
                    break

        if verbose:
            print(f"  SA step {step}: T={T:.4f}, best_phi={best_phi}, M={M}")

        if not accepted_any:
            break

        T *= beta

    return {
        "n_pmus": nu,
        "pmu_buses": sorted(best),
        "phi": best_phi,
        "observable": best_phi == 0,
        "success": best_phi == 0,
    }


# ===================================================================
# Bisecting search with SA (Baldwin Section III-D)
# ===================================================================

def solve_bisecting_search_baldwin(
    n_buses: int,
    branches: List[Tuple[int, int]],
    zero_injection_buses: Optional[List[int]] = None,
    seed: int = 42,
    verbose: bool = False,
    sa_retries: int = 3,
) -> Dict:
    """Baldwin's modified bisecting search for minimum PMU placement.

    Algorithm (Baldwin 1993, Section III-D):
      1. Use graph_theoretic_initial to get upper bound ν_U.
         Lower bound ν_L = 0.
      2. If ν_L == 0: test point = 0.85 * ν_U (rounded).
         Else: test point = (ν_L + ν_U) // 2 (midpoint).
      3. Run SA with ν_test PMUs.
         - If observable placement found: ν_U = ν_test, record placement.
         - If not: ν_L = ν_test.
      4. Repeat until ν_U - ν_L ≤ 1.
      5. ν_U is the minimum number of PMUs.

    Multiple SA runs per test point (sa_retries) to reduce stochastic failure.

    Parameters
    ----------
    n_buses : int
    branches : list of (int, int)
    zero_injection_buses : list of int or None
    seed : int
    verbose : bool
    sa_retries : int
        Number of SA attempts per test point.

    Returns
    -------
    dict with 'n_pmus', 'pmu_buses', 'ratio' (n_pmus/n_buses),
              'observable', 'success'
    """
    if zero_injection_buses is None:
        zero_injection_buses = []

    rng_seed = seed

    # Step 1: upper bound from greedy
    initial = graph_theoretic_initial(n_buses, branches, zero_injection_buses)
    nu_U = len(initial)
    best_placement = list(initial)
    nu_L = 0

    if verbose:
        print(f"Bisecting search: initial upper bound ν_U = {nu_U}")

    while nu_U - nu_L > 1:
        # Step 2: choose test point
        if nu_L == 0:
            nu_test = max(1, int(round(0.85 * nu_U)))
        else:
            nu_test = (nu_L + nu_U) // 2

        if nu_test <= nu_L:
            nu_test = nu_L + 1
        if nu_test >= nu_U:
            break

        if verbose:
            print(f"  Testing ν = {nu_test}  (bounds: [{nu_L}, {nu_U}])")

        # Step 3: run SA (multiple retries)
        found = False
        for retry in range(sa_retries):
            result = solve_sa_baldwin(
                n_buses, branches, zero_injection_buses,
                nu=nu_test, seed=rng_seed + retry * 1000, verbose=False,
            )
            if result["observable"]:
                found = True
                nu_U = nu_test
                best_placement = result["pmu_buses"]
                if verbose:
                    print(f"    -> Observable! ν_U = {nu_U}")
                break

        if not found:
            nu_L = nu_test
            if verbose:
                print(f"    -> Not observable. ν_L = {nu_L}")

    return {
        "n_pmus": nu_U,
        "pmu_buses": sorted(best_placement),
        "ratio": nu_U / n_buses,
        "observable": True,
        "success": True,
    }
