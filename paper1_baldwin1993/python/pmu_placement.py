"""
PMU Optimal Placement Problem - Baldwin et al. 1993
"Power System Observability with Minimal Phasor Measurement Placement"

Reproduced implementation:
  - Observability rules for PMU placement
  - Binary Integer Linear Programming (BILP) formulation
  - Simulated Annealing heuristic (original paper method)
  - IEEE test systems (7, 14, 30 bus)
"""

import numpy as np
from scipy.optimize import linprog
import random
import math
import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Tuple, Set, Dict, Optional


# =============================================================================
# IEEE Test Systems - Bus Connectivity Data
# =============================================================================

def ieee7_bus() -> Dict:
    """IEEE 7-bus test system."""
    n_bus = 7
    # Branches: (from, to) — 1-indexed
    branches = [
        (1, 2), (1, 3), (2, 3), (2, 5), (3, 4),
        (4, 5), (4, 7), (5, 6), (6, 7)
    ]
    name = "IEEE 7-bus"
    # Known optimal: 2 PMUs (buses 2, 5) or (3, 5) etc.
    return {"n_bus": n_bus, "branches": branches, "name": name}


def ieee14_bus() -> Dict:
    """IEEE 14-bus test system."""
    n_bus = 14
    branches = [
        (1, 2), (1, 5), (2, 3), (2, 4), (2, 5),
        (3, 4), (4, 5), (4, 7), (4, 9), (5, 6),
        (6, 11), (6, 12), (6, 13), (7, 8), (7, 9),
        (9, 10), (9, 14), (10, 11), (12, 13), (13, 14)
    ]
    # Zero injection buses (no generation, no load): 7
    zi_buses = [7]
    name = "IEEE 14-bus"
    return {"n_bus": n_bus, "branches": branches, "name": name, "zi_buses": zi_buses}


def ieee30_bus() -> Dict:
    """IEEE 30-bus test system."""
    n_bus = 30
    branches = [
        (1, 2), (1, 3), (2, 4), (2, 5), (2, 6),
        (3, 4), (4, 6), (4, 12), (5, 7), (6, 7),
        (6, 8), (6, 9), (6, 10), (6, 28), (8, 28),
        (9, 10), (9, 11), (10, 17), (10, 20), (10, 21),
        (10, 22), (12, 13), (12, 14), (12, 15), (12, 16),
        (14, 15), (15, 18), (15, 23), (16, 17), (18, 19),
        (19, 20), (21, 22), (22, 24), (23, 24), (24, 25),
        (25, 26), (25, 27), (27, 28), (27, 29), (27, 30),
        (29, 30)
    ]
    name = "IEEE 30-bus"
    return {"n_bus": n_bus, "branches": branches, "name": name}


# =============================================================================
# Observability Analysis
# =============================================================================

def build_adjacency_matrix(n_bus: int, branches: List[Tuple[int, int]]) -> np.ndarray:
    """Build binary adjacency matrix A where A[i][j] = 1 if bus i and j are connected."""
    A = np.zeros((n_bus, n_bus), dtype=int)
    for (i, j) in branches:
        A[i-1][j-1] = 1
        A[j-1][i-1] = 1
    return A


def build_connectivity_matrix(n_bus: int, branches: List[Tuple[int, int]]) -> np.ndarray:
    """
    Build connectivity matrix f for BILP formulation.
    f[i][j] = 1 if bus j can observe bus i (i.e., i==j or i and j are connected).
    This is A + I (adjacency + identity).
    """
    A = build_adjacency_matrix(n_bus, branches)
    return A + np.eye(n_bus, dtype=int)


def check_observability(pmu_placement: List[int], n_bus: int,
                        branches: List[Tuple[int, int]]) -> Tuple[bool, Set[int]]:
    """
    Check if given PMU placement achieves complete observability.

    PMU observability rules (Baldwin et al. 1993):
      Rule 1: A bus with a PMU installed is directly observable.
      Rule 2: If bus i has a PMU, all buses directly connected to bus i
              are observable (PMU measures voltage at bus i and current
              on all incident branches, so V at adjacent buses can be computed).

    Args:
        pmu_placement: list of bus indices (1-indexed) with PMU
        n_bus: total number of buses
        branches: list of (from, to) branch tuples (1-indexed)

    Returns:
        (is_observable, observed_buses): tuple of bool and set of observed bus indices
    """
    observed = set()
    adj = build_adjacency_matrix(n_bus, branches)

    for pmu_bus in pmu_placement:
        idx = pmu_bus - 1
        # Rule 1: PMU bus itself
        observed.add(pmu_bus)
        # Rule 2: all adjacent buses
        for j in range(n_bus):
            if adj[idx][j] == 1:
                observed.add(j + 1)

    all_buses = set(range(1, n_bus + 1))
    return (observed == all_buses, observed)


def observability_depth(pmu_placement: List[int], n_bus: int,
                        branches: List[Tuple[int, int]]) -> np.ndarray:
    """
    Compute observability depth for each bus.
    depth[i] = number of PMUs that can observe bus i.
    Higher depth means more redundant observability.
    """
    f = build_connectivity_matrix(n_bus, branches)
    x = np.zeros(n_bus, dtype=int)
    for bus in pmu_placement:
        x[bus - 1] = 1
    return f @ x


# =============================================================================
# BILP Formulation (Binary Integer Linear Programming)
# =============================================================================

def solve_bilp(system: Dict, verbose: bool = True) -> Tuple[List[int], int]:
    """
    Solve PMU placement using BILP (Binary Integer Linear Programming).

    Formulation (Gou 2008 generalized form, based on Baldwin 1993 concept):
        minimize:   sum(x_i) for i = 1..N
        subject to: f * x >= 1  (each bus must be observed by at least 1 PMU)
                    x_i in {0, 1}

    Where f is the connectivity matrix and x is the PMU placement vector.

    Uses LP relaxation with rounding (scipy doesn't have native ILP).
    For exact solutions, we use branch-and-bound.
    """
    n_bus = system["n_bus"]
    branches = system["branches"]
    f = build_connectivity_matrix(n_bus, branches)

    # Solve using branch and bound
    best_solution = branch_and_bound_bilp(n_bus, f)

    pmu_buses = [i + 1 for i in range(n_bus) if best_solution[i] == 1]
    n_pmu = len(pmu_buses)

    if verbose:
        print(f"\n{'='*60}")
        print(f"BILP Solution for {system['name']}")
        print(f"{'='*60}")
        print(f"Number of PMUs: {n_pmu}")
        print(f"PMU locations (bus): {pmu_buses}")
        is_obs, obs_set = check_observability(pmu_buses, n_bus, branches)
        print(f"Complete observability: {is_obs}")
        depth = observability_depth(pmu_buses, n_bus, branches)
        print(f"Observability depth: {depth.tolist()}")

    return pmu_buses, n_pmu


def branch_and_bound_bilp(n_bus: int, f: np.ndarray) -> np.ndarray:
    """Simple branch and bound for binary ILP."""
    best = {"solution": np.ones(n_bus, dtype=int), "cost": n_bus}

    def _solve_lp_relaxation(fixed: Dict[int, int]) -> Optional[Tuple[float, np.ndarray]]:
        """Solve LP relaxation with some variables fixed."""
        c = np.ones(n_bus)
        # Constraints: f @ x >= 1 => -f @ x <= -1
        A_ub = -f.astype(float)
        b_ub = -np.ones(n_bus)
        bounds = []
        for i in range(n_bus):
            if i in fixed:
                bounds.append((fixed[i], fixed[i]))
            else:
                bounds.append((0.0, 1.0))
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        if res.success:
            return res.fun, res.x
        return None

    def _branch(fixed: Dict[int, int], depth: int):
        result = _solve_lp_relaxation(fixed)
        if result is None:
            return
        lb, x_relax = result

        if lb >= best["cost"]:
            return  # Prune

        # Check if solution is integer
        is_integer = all(abs(x_relax[i] - round(x_relax[i])) < 1e-6 for i in range(n_bus))
        if is_integer:
            x_int = np.round(x_relax).astype(int)
            cost = np.sum(x_int)
            if cost < best["cost"]:
                # Verify feasibility
                if np.all(f @ x_int >= 1):
                    best["solution"] = x_int.copy()
                    best["cost"] = cost
            return

        # Find most fractional variable
        frac_vars = [(i, abs(x_relax[i] - 0.5)) for i in range(n_bus) if i not in fixed]
        if not frac_vars:
            return
        branch_var = min(frac_vars, key=lambda t: t[1])[0]

        # Branch: try x=1 first (more likely to be feasible)
        for val in [1, 0]:
            new_fixed = fixed.copy()
            new_fixed[branch_var] = val
            _branch(new_fixed, depth + 1)

    _branch({}, 0)
    return best["solution"]


# =============================================================================
# Simulated Annealing (Original Baldwin et al. 1993 method)
# =============================================================================

def solve_sa(system: Dict, n_trials: int = 10, verbose: bool = True) -> Tuple[List[int], int]:
    """
    Solve PMU placement using Simulated Annealing (Baldwin et al. 1993).

    The original paper used SA combined with binary search on the number of PMUs.
    1. Binary search on k (number of PMUs)
    2. For each k, use SA to find a feasible placement of k PMUs

    SA parameters follow typical settings from the paper era.
    """
    n_bus = system["n_bus"]
    branches = system["branches"]
    f = build_connectivity_matrix(n_bus, branches)

    def evaluate(x: np.ndarray) -> int:
        """Count unobserved buses (penalty)."""
        obs = f @ x
        return int(np.sum(obs < 1))

    def sa_feasibility(k: int, max_iter: int = 5000) -> Optional[np.ndarray]:
        """Try to find a feasible placement of k PMUs using SA."""
        # Initial random placement of k PMUs
        x = np.zeros(n_bus, dtype=int)
        indices = random.sample(range(n_bus), k)
        for idx in indices:
            x[idx] = 1

        current_cost = evaluate(x)
        if current_cost == 0:
            return x

        best_x = x.copy()
        best_cost = current_cost

        T = 10.0  # Initial temperature
        T_min = 0.01
        alpha = 0.995  # Cooling rate

        for iteration in range(max_iter):
            if T < T_min:
                break

            # Generate neighbor: swap one PMU with one non-PMU
            pmu_indices = [i for i in range(n_bus) if x[i] == 1]
            non_pmu_indices = [i for i in range(n_bus) if x[i] == 0]

            if not pmu_indices or not non_pmu_indices:
                break

            remove = random.choice(pmu_indices)
            add = random.choice(non_pmu_indices)

            x_new = x.copy()
            x_new[remove] = 0
            x_new[add] = 1

            new_cost = evaluate(x_new)
            delta = new_cost - current_cost

            if delta <= 0 or random.random() < math.exp(-delta / T):
                x = x_new
                current_cost = new_cost

                if current_cost < best_cost:
                    best_x = x.copy()
                    best_cost = current_cost

                if best_cost == 0:
                    return best_x

            T *= alpha

        return best_x if best_cost == 0 else None

    # Binary search on number of PMUs
    lo, hi = 1, n_bus
    best_placement = np.ones(n_bus, dtype=int)  # Worst case: all buses
    best_k = n_bus

    while lo <= hi:
        mid = (lo + hi) // 2
        found = False

        for trial in range(n_trials):
            result = sa_feasibility(mid)
            if result is not None:
                found = True
                if mid < best_k:
                    best_k = mid
                    best_placement = result.copy()
                break

        if found:
            hi = mid - 1
        else:
            lo = mid + 1

    pmu_buses = [i + 1 for i in range(n_bus) if best_placement[i] == 1]

    if verbose:
        print(f"\n{'='*60}")
        print(f"Simulated Annealing Solution for {system['name']}")
        print(f"{'='*60}")
        print(f"Number of PMUs: {best_k}")
        print(f"PMU locations (bus): {pmu_buses}")
        is_obs, _ = check_observability(pmu_buses, n_bus, branches)
        print(f"Complete observability: {is_obs}")
        depth = observability_depth(pmu_buses, n_bus, branches)
        print(f"Observability depth: {depth.tolist()}")

    return pmu_buses, best_k


# =============================================================================
# Visualization
# =============================================================================

def get_bus_positions(system_name: str, n_bus: int) -> Optional[Dict[int, Tuple[float, float]]]:
    """Get predefined bus positions for standard IEEE systems."""
    if "14" in system_name:
        return {
            1: (0, 4), 2: (2, 4), 3: (4, 3), 4: (3, 2),
            5: (1, 2), 6: (4, 1), 7: (5, 2), 8: (6, 2.5),
            9: (5, 0.5), 10: (5, -0.5), 11: (4.5, -0.5),
            12: (3.5, 0), 13: (4, -0.5), 14: (5.5, -0.5)
        }
    if "7" in system_name:
        return {
            1: (0, 2), 2: (1, 3), 3: (1, 1),
            4: (2, 1), 5: (2, 3), 6: (3, 2), 7: (3, 0.5)
        }
    return None


def visualize_placement(system: Dict, pmu_buses: List[int],
                        title: str = "", save_path: str = None):
    """Visualize PMU placement on the network graph."""
    n_bus = system["n_bus"]
    branches = system["branches"]

    G = nx.Graph()
    G.add_nodes_from(range(1, n_bus + 1))
    G.add_edges_from(branches)

    pos = get_bus_positions(system["name"], n_bus)
    if pos is None:
        pos = nx.spring_layout(G, seed=42)

    _, observed = check_observability(pmu_buses, n_bus, branches)
    depth = observability_depth(pmu_buses, n_bus, branches)

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # Color nodes
    colors = []
    for bus in range(1, n_bus + 1):
        if bus in pmu_buses:
            colors.append('#e74c3c')  # Red: PMU installed
        elif bus in observed:
            colors.append('#2ecc71')  # Green: observed
        else:
            colors.append('#95a5a6')  # Grey: unobserved

    # Draw
    nx.draw_edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#7f8c8d',
                                            width=2, alpha=0.7)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors,
                           node_size=700, edgecolors='black', linewidths=2)

    # Labels with depth
    labels = {bus: f"{bus}\n(d={int(depth[bus-1])})" for bus in range(1, n_bus + 1)}
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=9, font_weight='bold')

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#e74c3c', edgecolor='black', label='PMU installed'),
        Patch(facecolor='#2ecc71', edgecolor='black', label='Observed (no PMU)'),
        Patch(facecolor='#95a5a6', edgecolor='black', label='Unobserved'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11)

    if not title:
        title = f"{system['name']} - PMU Placement ({len(pmu_buses)} PMUs)"
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('off')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    plt.show()


# =============================================================================
# Main - Run all methods on all test systems
# =============================================================================

def main():
    systems = [ieee7_bus(), ieee14_bus(), ieee30_bus()]

    print("=" * 60)
    print("PMU Optimal Placement Problem")
    print("Baldwin et al. 1993 - Reproduction")
    print("=" * 60)

    for system in systems:
        print(f"\n\n{'#'*60}")
        print(f"# System: {system['name']}")
        print(f"# Buses: {system['n_bus']}, Branches: {len(system['branches'])}")
        print(f"{'#'*60}")

        # Show connectivity matrix
        f = build_connectivity_matrix(system["n_bus"], system["branches"])
        print(f"\nConnectivity matrix f (first 10 rows/cols):")
        print(f[:min(10, system["n_bus"]), :min(10, system["n_bus"])])

        # BILP solution
        pmu_bilp, n_bilp = solve_bilp(system)

        # SA solution
        pmu_sa, n_sa = solve_sa(system)

        # Visualize BILP result
        visualize_placement(
            system, pmu_bilp,
            title=f"{system['name']} - BILP ({n_bilp} PMUs)",
            save_path=f"result_{system['name'].replace(' ', '_').lower()}_bilp.png"
        )

        # Visualize SA result
        visualize_placement(
            system, pmu_sa,
            title=f"{system['name']} - SA ({n_sa} PMUs)",
            save_path=f"result_{system['name'].replace(' ', '_').lower()}_sa.png"
        )


if __name__ == "__main__":
    main()
