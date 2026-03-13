"""
Observability checking functions for PMU placement.

Implements topological observability analysis following Baldwin et al. (1993):
  - Rule 1: A PMU measures the voltage at its bus and the current on all
            incident branches, making all adjacent buses observed.
  - Rule 2: If both end-bus voltages of a branch are known, the branch
            current can be computed (pseudo-measurement).
  - Rule 3: At any bus, if all but one incident branch current are known,
            KCL gives the remaining current, which yields the voltage at
            the far end of that branch.

Rules 2 and 3 propagate iteratively until no new buses are observed.

Reference:
    T. L. Baldwin, L. Mili, M. B. Boisen Jr., and R. Adapa,
    "Power System Observability With Minimal Phasor Measurement Placement,"
    IEEE Trans. Power Systems, vol. 8, no. 2, May 1993.
"""

from __future__ import annotations

from typing import List, Set, Tuple

import numpy as np


# ──────────────────────────────────────────────────────────────────────
# Connectivity matrix
# ──────────────────────────────────────────────────────────────────────

def build_connectivity_matrix(n_buses: int, branches: List[Tuple[int, int]]) -> np.ndarray:
    """Build the bus connectivity (adjacency + identity) matrix.

    The matrix f is defined as:
        f[i][j] = 1  if bus (i+1) and bus (j+1) are connected or i == j
        f[i][j] = 0  otherwise

    This is the *f* matrix used in the BILP formulation (Baldwin eq. 3).

    Parameters
    ----------
    n_buses : int
        Total number of buses (buses are numbered 1..n_buses).
    branches : list of (int, int)
        Branch list as 1-indexed (from_bus, to_bus) tuples.

    Returns
    -------
    np.ndarray
        n_buses x n_buses binary matrix.
    """
    f = np.eye(n_buses, dtype=int)
    for i, j in branches:
        f[i - 1, j - 1] = 1
        f[j - 1, i - 1] = 1
    return f


def _adjacency(n_buses: int, branches: List[Tuple[int, int]]) -> dict:
    """Return adjacency dict mapping bus -> set of neighbor buses (1-indexed)."""
    adj: dict[int, set] = {b: set() for b in range(1, n_buses + 1)}
    for i, j in branches:
        adj[i].add(j)
        adj[j].add(i)
    return adj


# ──────────────────────────────────────────────────────────────────────
# Basic topological observability (Rule 1 only)
# ──────────────────────────────────────────────────────────────────────

def check_topological_observability_basic(
    n_buses: int,
    branches: List[Tuple[int, int]],
    pmu_buses: List[int],
) -> Tuple[bool, Set[int], Set[int]]:
    """Check observability using Rule 1 only (direct adjacency).

    A bus is observed if:
      - A PMU is installed at the bus, OR
      - A PMU is installed at an adjacent bus.

    Parameters
    ----------
    n_buses : int
        Number of buses.
    branches : list of (int, int)
        Branch list (1-indexed).
    pmu_buses : list of int
        Buses where PMUs are placed (1-indexed).

    Returns
    -------
    is_observable : bool
        True if every bus is observed.
    observed : set of int
        Set of observed bus numbers.
    unobserved : set of int
        Set of unobserved bus numbers.
    """
    adj = _adjacency(n_buses, branches)
    observed: Set[int] = set()
    for p in pmu_buses:
        observed.add(p)
        observed.update(adj[p])
    all_buses = set(range(1, n_buses + 1))
    unobserved = all_buses - observed
    return len(unobserved) == 0, observed, unobserved


# ──────────────────────────────────────────────────────────────────────
# Full topological observability (Rules 1-3, iterative)
# ──────────────────────────────────────────────────────────────────────

def check_topological_observability_rules(
    n_buses: int,
    branches: List[Tuple[int, int]],
    pmu_buses: List[int],
    zero_injection_buses: List[int] | None = None,
) -> Tuple[bool, Set[int], Set[int]]:
    """Check observability using Baldwin's Rules 1-3 with iterative propagation.

    Rule 1 (PMU placement):
        A PMU at bus *k* measures V_k and all incident branch currents.
        All buses adjacent to *k* become voltage-observed.

    Rule 2 (pseudo-measurement):
        If both voltages at the ends of a branch are known, the branch
        current is computable.  Mark that branch current as known.

    Rule 3 (KCL extension):
        At any bus where all but one incident branch current are known,
        KCL gives the remaining branch current.  The voltage at the far
        end of that branch then becomes known.

    Zero-injection bus (ZIB) enhancement:
        At a ZIB, the net injection is zero, so if all but one neighbor
        voltage are known, KCL directly gives the unknown neighbor
        voltage (equivalent to Rule 3 with zero injection constraint).
        This is applied as part of the Rule 3 propagation.

    The algorithm iterates Rules 2-3 until no further buses are observed.

    Parameters
    ----------
    n_buses : int
        Number of buses.
    branches : list of (int, int)
        Branch list (1-indexed).
    pmu_buses : list of int
        PMU bus locations (1-indexed).
    zero_injection_buses : list of int or None
        Buses with zero net injection (1-indexed).

    Returns
    -------
    is_observable : bool
    observed : set of int
    unobserved : set of int
    """
    if zero_injection_buses is None:
        zero_injection_buses = []

    adj = _adjacency(n_buses, branches)
    zib_set = set(zero_injection_buses)

    # Track which buses have known voltages
    observed: Set[int] = set()

    # Track which branch currents are known.
    # A branch is stored as a frozenset({i, j}) for undirected lookup.
    known_currents: Set[frozenset] = set()

    # ── Rule 1: PMU placement ──
    for p in pmu_buses:
        observed.add(p)
        for neighbor in adj[p]:
            observed.add(neighbor)
            known_currents.add(frozenset((p, neighbor)))

    # ── Iterative propagation of Rules 2, 3, and ZIB ──
    changed = True
    while changed:
        changed = False

        # Rule 2: branch between two observed buses => current known
        for i, j in branches:
            br = frozenset((i, j))
            if br not in known_currents and i in observed and j in observed:
                known_currents.add(br)
                changed = True

        # Rule 3 (KCL): At a zero-injection bus (ZIB), if all but one
        # incident branch current are known, KCL gives the remaining
        # current (since injection = 0), yielding the far-end voltage.
        #
        # IMPORTANT: Rule 3 only applies at ZIBs (Baldwin 1993, Section
        # 2.2.4 explicitly uses "zero injection at bus 7" to justify
        # KCL inference).  At non-ZIB buses, the unknown injection
        # prevents KCL from determining the remaining branch current.
        #
        # At PMU buses, Rule 1 already gives all branch currents.
        for zb in zib_set:
            if zb not in observed:
                continue  # ZIB must be observed for KCL to apply
            incident = [frozenset((zb, nb)) for nb in adj[zb]]
            unknown_branches = [br for br in incident if br not in known_currents]
            if len(unknown_branches) == 1:
                br = unknown_branches[0]
                far_end = list(br - frozenset({zb}))[0]
                known_currents.add(br)
                if far_end not in observed:
                    observed.add(far_end)
                    changed = True

    all_buses = set(range(1, n_buses + 1))
    unobserved = all_buses - observed
    return len(unobserved) == 0, observed, unobserved


# ──────────────────────────────────────────────────────────────────────
# Phi(S): number of unobserved buses  (Baldwin eq. 5)
# ──────────────────────────────────────────────────────────────────────

def count_unobserved(
    n_buses: int,
    branches: List[Tuple[int, int]],
    pmu_buses: List[int],
    zero_injection_buses: List[int] | None = None,
) -> int:
    """Return Phi(S) = number of unobserved buses (Baldwin eq. 5).

    Uses the full Rule 1-3 observability check with ZIB enhancement.

    Parameters
    ----------
    n_buses : int
        Number of buses.
    branches : list of (int, int)
        Branch list (1-indexed).
    pmu_buses : list of int
        PMU bus locations (1-indexed).
    zero_injection_buses : list of int or None
        Zero-injection buses.

    Returns
    -------
    int
        Number of unobserved buses.
    """
    _, _, unobserved = check_topological_observability_rules(
        n_buses, branches, pmu_buses, zero_injection_buses
    )
    return len(unobserved)
