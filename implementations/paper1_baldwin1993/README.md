# Paper 1: Baldwin et al. 1993 — PMU Optimal Placement

> T.L. Baldwin, L. Mili, M.B. Boisen Jr., R. Adapa,
> "Power System Observability with Minimal Phasor Measurement Placement,"
> IEEE Trans. Power Systems, Vol. 8, No. 2, pp. 707-715, 1993.

## What's implemented

| File | Description |
|------|-------------|
| `python/pmu_placement.py` | BILP (Branch & Bound) + SA solver, IEEE 7/14/30 bus systems |
| `python/pmu_fundamentals.py` | DC power flow + WLS state estimation, measured vs estimated voltage comparison |
| `python/parse_ieej_east30.py` | Parser for IEEJ Y-method data format |
| `matlab/pmu_placement_main.m` | MATLAB implementation (intlinprog + SA) |
| `html/index.html` | Interactive HTML demo — IEEE 7/14/30 bus |
| `html/east30.html` | Interactive HTML demo — IEEJ EAST30 + IEEE systems |
| `data/ieej_east30p_s.txt` | IEEJ East 30-machine system data (Y-method format) |
| `data/ieej_east30_fig41.pdf` | IEEJ East 30 official single-line diagram (Fig.4.1) |

## Quick Start

### HTML Demo (no install required)

Open `html/east30.html` in a browser. Features:
- IEEE 7/14/30 + IEEJ EAST30 (107 bus) system selection
- Click buses to place/remove PMUs
- Greedy BILP / Simulated Annealing auto-solver
- Real-time observability visualization
- Bus layout matches IEEJ Fig.4.1

### Python

```bash
pip install numpy scipy matplotlib networkx
python python/pmu_placement.py          # BILP + SA on all test systems
python python/pmu_fundamentals.py       # Power flow + state estimation demo
```

### MATLAB

```matlab
pmu_placement_main   % Requires Optimization Toolbox for intlinprog
```

## Key Results

| System | Buses | Branches | Min PMUs | Rate |
|--------|-------|----------|----------|------|
| IEEE 7-bus | 7 | 9 | 2 | 28.6% |
| IEEE 14-bus | 14 | 20 | 4 | 28.6% |
| IEEE 30-bus | 30 | 41 | 10 | 33.3% |
| IEEJ EAST30 | 107 | 123 | ~30 | ~28% |

## Mathematical Formulation

**BILP (Binary Integer Linear Programming):**

```
minimize    Σ x_i           (number of PMUs)
subject to  f · x ≥ 1       (all buses observed)
            x_i ∈ {0, 1}
```

Where `f` is the connectivity matrix: `f[i][j] = 1` if bus i and j are connected or i == j.

**State Estimation (WLS):**

```
minimize    J(θ) = [z - H·θ]^T · R^{-1} · [z - H·θ]
solution    θ_hat = (H^T R^{-1} H)^{-1} · H^T R^{-1} · z
```

## Data Sources

- IEEE test systems: IEEE PES standard test cases
- IEEJ EAST30: [IEEJ Power System Standard Models](https://www.iee.or.jp/pes/model/english/)
