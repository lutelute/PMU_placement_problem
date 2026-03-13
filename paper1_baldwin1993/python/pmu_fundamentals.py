"""
PMU配置問題の根本原理
=====================
Level 1: トポロジー的観測性（Baldwin 1993）
Level 2: 数値的観測性（状態推定 + 潮流計算）
Level 3: 推定電圧 vs 計測電圧の可視化

IEEE 14-bus系統で実演
"""

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

np.set_printoptions(precision=4, suppress=True)


# =============================================================================
# IEEE 14-bus系統データ（簡略化：DCモデル用）
# =============================================================================

def ieee14_system():
    """
    IEEE 14-bus system data.
    Returns bus data, branch data (reactance), and adjacency.
    """
    n_bus = 14
    # ブランチ: (from, to, reactance_pu)
    branches = [
        (1,  2,  0.05917), (1,  5,  0.22304), (2,  3,  0.19797),
        (2,  4,  0.17632), (2,  5,  0.17388), (3,  4,  0.17103),
        (4,  5,  0.04211), (4,  7,  0.20912), (4,  9,  0.55618),
        (5,  6,  0.25202), (6, 11,  0.19890), (6, 12,  0.25581),
        (6, 13,  0.13027), (7,  8,  0.17615), (7,  9,  0.11001),
        (9, 10,  0.08450), (9, 14,  0.27038), (10,11,  0.20640),
        (12,13,  0.19988), (13,14,  0.34802),
    ]

    # 各バスの有効電力注入 (pu) — 正=発電, 負=負荷
    # Bus 1 = slack (θ=0), Bus 2,3,6,8 = PV (generators)
    P_inject = np.array([
        2.324,   # Bus 1 (slack - will be computed)
        0.183,   # Bus 2
       -0.942,   # Bus 3
       -0.478,   # Bus 4
       -0.076,   # Bus 5
        0.112,   # Bus 6 (gen - load)
        0.000,   # Bus 7 (zero injection)
        0.000,   # Bus 8 (gen, no load assumed small)
       -0.295,   # Bus 9
       -0.090,   # Bus 10
       -0.035,   # Bus 11
       -0.061,   # Bus 12
       -0.135,   # Bus 13
       -0.149,   # Bus 14
    ])

    return {
        'n_bus': n_bus,
        'branches': branches,
        'P_inject': P_inject,
        'slack_bus': 0,  # 0-indexed
    }


# =============================================================================
# Level 0: DC潮流計算（真の状態を得る）
# =============================================================================

def dc_power_flow(sys):
    """
    DC潮流計算: B·θ = P を解いて各バスの位相角θを求める

    DC近似の仮定:
      - |V| ≈ 1.0 pu (全バス)
      - sin(θi - θj) ≈ θi - θj
      - 抵抗無視 (R << X)

    したがって: P_ij = (θi - θj) / x_ij
    行列形式:  P = B · θ
    """
    n = sys['n_bus']
    branches = sys['branches']
    slack = sys['slack_bus']

    # Bマトリクス（サセプタンス行列）の構築
    B = np.zeros((n, n))
    for (i, j, x) in branches:
        b = 1.0 / x  # サセプタンス = 1/リアクタンス
        i0, j0 = i-1, j-1
        B[i0, i0] += b
        B[j0, j0] += b
        B[i0, j0] -= b
        B[j0, i0] -= b

    # スラックバスを除外して解く
    non_slack = [i for i in range(n) if i != slack]
    B_red = B[np.ix_(non_slack, non_slack)]
    P_red = sys['P_inject'][non_slack]

    theta_red = np.linalg.solve(B_red, P_red)

    # 全バスの位相角
    theta = np.zeros(n)
    for idx, bus in enumerate(non_slack):
        theta[bus] = theta_red[idx]

    # 電圧フェーザー（DC近似: |V|=1, angle=θ）
    V_true = np.exp(1j * theta)  # V = 1.0 * e^(jθ)

    print("=" * 70)
    print("DC潮流計算結果（真の系統状態）")
    print("=" * 70)
    print(f"{'Bus':>4} {'|V| [pu]':>10} {'θ [deg]':>10} {'P [pu]':>10}")
    print("-" * 44)
    for i in range(n):
        print(f"{i+1:4d} {abs(V_true[i]):10.4f} {np.degrees(theta[i]):10.4f} {sys['P_inject'][i]:10.4f}")

    return theta, V_true, B


# =============================================================================
# Level 1: トポロジー的観測性（Baldwin 1993）
# =============================================================================

def topological_observability(sys, pmu_buses):
    """
    トポロジー的観測性チェック

    ルール: PMUがバスiにあれば、バスiと隣接バスの電圧が「観測可能」
    → 接続行列 f を使って f·x ≥ 1 かチェック

    ★ ここでは潮流計算は一切不要 ★
    """
    n = sys['n_bus']
    branches = sys['branches']

    # 接続行列 f
    f = np.eye(n, dtype=int)
    for (i, j, _) in branches:
        f[i-1, j-1] = 1
        f[j-1, i-1] = 1

    x = np.zeros(n, dtype=int)
    for b in pmu_buses:
        x[b-1] = 1

    depth = f @ x  # 各バスの観測深度
    observable = depth >= 1

    print("\n" + "=" * 70)
    print(f"Level 1: トポロジー的観測性 (PMU at buses {pmu_buses})")
    print("=" * 70)
    print(f"{'Bus':>4} {'PMU?':>6} {'Depth':>6} {'Observable':>12}")
    print("-" * 32)
    for i in range(n):
        print(f"{i+1:4d} {'YES' if x[i] else '':>6} {depth[i]:6d} {'✓' if observable[i] else '✗':>12}")
    print(f"\n完全観測性: {'達成' if all(observable) else '未達成'}")
    return observable, depth


# =============================================================================
# Level 2: 計測モデルと状態推定（WLS: Weighted Least Squares）
# =============================================================================

def build_measurement_model(sys, pmu_buses, theta_true):
    """
    PMU計測モデルの構築

    PMUが計測するもの:
      1. 設置バスの電圧フェーザー → θ_i を直接計測
      2. 接続ブランチの電流フェーザー → (θ_i - θ_j)/x_ij を計測

    計測モデル: z = H·θ + e
      z: 計測ベクトル
      H: 計測ヤコビアン行列
      e: 計測誤差 (ガウスノイズ)
      θ: 状態ベクトル（各バスの位相角）

    ★ ここが潮流計算と繋がる核心部分 ★
    """
    n = sys['n_bus']
    branches = sys['branches']
    slack = sys['slack_bus']

    measurements = []  # (type, value, sigma, H_row)
    meas_labels = []

    for pmu_bus in pmu_buses:
        p = pmu_bus - 1  # 0-indexed

        # (A) 電圧位相角の直接計測: z = θ_p
        H_row = np.zeros(n)
        H_row[p] = 1.0
        sigma = 0.01  # PMUの精度: ~0.01 rad ≈ 0.57°
        noise = np.random.normal(0, sigma)
        z_val = theta_true[p] + noise
        measurements.append((z_val, sigma, H_row))
        meas_labels.append(f"θ_{pmu_bus} (電圧角)")

        # (B) 接続ブランチの電流計測: z = (θ_i - θ_j) / x_ij
        for (i, j, x_ij) in branches:
            i0, j0 = i-1, j-1
            if i0 == p or j0 == p:
                H_row = np.zeros(n)
                H_row[i0] = 1.0 / x_ij
                H_row[j0] = -1.0 / x_ij
                sigma_flow = 0.02
                noise = np.random.normal(0, sigma_flow)
                z_val = (theta_true[i0] - theta_true[j0]) / x_ij + noise
                measurements.append((z_val, sigma_flow, H_row))
                meas_labels.append(f"P_{i}-{j} (潮流)")

    # 計測ベクトル・行列の組立
    m = len(measurements)
    z = np.array([meas[0] for meas in measurements])
    R_diag = np.array([meas[1]**2 for meas in measurements])  # 分散
    H = np.array([meas[2] for meas in measurements])

    print("\n" + "=" * 70)
    print(f"Level 2: 計測モデル (PMU at buses {pmu_buses})")
    print("=" * 70)
    print(f"状態変数数: {n} (各バスの位相角 θ)")
    print(f"計測数:     {m}")
    print(f"冗長度:     {m/n:.2f} (m/n, ≥1で観測可能)")
    print(f"\n計測リスト:")
    for i, label in enumerate(meas_labels):
        print(f"  z[{i:2d}] = {z[i]:+8.4f}  ({label})")

    return z, H, R_diag, meas_labels


def state_estimation_wls(sys, pmu_buses, theta_true, V_true):
    """
    重み付き最小二乗法 (WLS) による状態推定

    ★ 最適化の根本 ★

    目的関数:
        min J(θ) = [z - H·θ]^T · R^{-1} · [z - H·θ]

        z: PMU計測値（計測電圧 + ノイズ）
        H: 計測ヤコビアン
        θ: 推定する状態（各バスの位相角）
        R: 計測誤差の共分散行列

    正規方程式の解:
        θ_hat = (H^T R^{-1} H)^{-1} · H^T R^{-1} · z

    これは「計測電圧と推定電圧の重み付き二乗誤差を最小化」する
    """
    n = sys['n_bus']
    slack = sys['slack_bus']

    z, H, R_diag, meas_labels = build_measurement_model(sys, pmu_buses, theta_true)

    # R^{-1} (対角行列の逆)
    R_inv = np.diag(1.0 / R_diag)

    # ゲイン行列 G = H^T R^{-1} H
    G = H.T @ R_inv @ H

    print("\n" + "=" * 70)
    print("ゲイン行列 G = H^T R^{-1} H")
    print("=" * 70)
    print(f"ランク: {np.linalg.matrix_rank(G)} / {n}")

    rank = np.linalg.matrix_rank(G)
    if rank < n:
        print(f"⚠ ランク不足！ 観測性が不完全 → 状態推定不可能")
        print(f"  (必要ランク={n}, 実ランク={rank}, 不足={n-rank})")

        # 固有値を見る
        eigvals = np.linalg.eigvalsh(G)
        zero_eigs = np.sum(np.abs(eigvals) < 1e-8)
        print(f"  ゼロ固有値数: {zero_eigs}")
        print(f"  → {zero_eigs}個のバスが観測不能")

        return None, None

    # 正規方程式を解く: θ_hat = G^{-1} H^T R^{-1} z
    theta_hat = np.linalg.solve(G, H.T @ R_inv @ z)

    # 推定電圧フェーザー
    V_est = np.exp(1j * theta_hat)

    # 残差: 計測値 - 推定値
    z_est = H @ theta_hat
    residuals = z - z_est

    print("\n" + "=" * 70)
    print("★ 計測電圧 vs 推定電圧 ★")
    print("=" * 70)
    print(f"{'Bus':>4} {'θ_true[deg]':>12} {'θ_est[deg]':>12} {'誤差[deg]':>10} "
          f"{'|V|_true':>9} {'|V|_est':>9}")
    print("-" * 66)
    for i in range(n):
        err = np.degrees(theta_hat[i] - theta_true[i])
        print(f"{i+1:4d} {np.degrees(theta_true[i]):12.4f} {np.degrees(theta_hat[i]):12.4f} "
              f"{err:10.4f} {abs(V_true[i]):9.4f} {abs(V_est[i]):9.4f}")

    # 推定精度指標
    theta_err = theta_hat - theta_true
    rmse = np.sqrt(np.mean(theta_err**2))
    max_err = np.max(np.abs(theta_err))
    print(f"\nRMSE(θ): {np.degrees(rmse):.6f} deg")
    print(f"最大誤差: {np.degrees(max_err):.6f} deg")

    return theta_hat, V_est


# =============================================================================
# Level 3: 可視化 — 推定 vs 真値 vs 計測
# =============================================================================

def visualize_estimation(sys, pmu_buses, theta_true, V_true, theta_hat, V_est):
    """推定電圧と真の電圧の比較を可視化"""
    n = sys['n_bus']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'PMU State Estimation — PMU at buses {pmu_buses}', fontsize=14, fontweight='bold')

    buses = np.arange(1, n+1)
    pmu_mask = np.array([b in pmu_buses for b in buses])

    # (1) 位相角の比較
    ax = axes[0, 0]
    ax.bar(buses - 0.2, np.degrees(theta_true), 0.35, label='真値 (潮流計算)', color='#3498db', alpha=0.8)
    ax.bar(buses + 0.2, np.degrees(theta_hat), 0.35, label='推定値 (WLS)', color='#e74c3c', alpha=0.8)
    # PMU設置バスをマーク
    for b in pmu_buses:
        ax.axvline(b, color='gold', alpha=0.3, linewidth=8)
    ax.set_xlabel('Bus')
    ax.set_ylabel('位相角 θ [deg]')
    ax.set_title('位相角: 真値 vs 推定値')
    ax.legend()
    ax.set_xticks(buses)
    ax.grid(True, alpha=0.3)

    # (2) 推定誤差
    ax = axes[0, 1]
    errors = np.degrees(theta_hat - theta_true)
    colors = ['#e74c3c' if pmu_mask[i] else '#3498db' for i in range(n)]
    ax.bar(buses, errors, color=colors, alpha=0.8)
    ax.axhline(0, color='white', linewidth=0.5)
    ax.set_xlabel('Bus')
    ax.set_ylabel('誤差 [deg]')
    ax.set_title('推定誤差 (赤=PMU設置バス, 青=非設置バス)')
    ax.set_xticks(buses)
    ax.grid(True, alpha=0.3)

    # (3) フェーザー図（複素平面）
    ax = axes[1, 0]
    for i in range(n):
        # 真値
        ax.plot([0, V_true[i].real], [0, V_true[i].imag], '-', color='#3498db', alpha=0.3, linewidth=1)
        ax.plot(V_true[i].real, V_true[i].imag, 'o', color='#3498db', markersize=6)
        # 推定値
        ax.plot(V_est[i].real, V_est[i].imag, 'x', color='#e74c3c', markersize=8, markeredgewidth=2)
        ax.annotate(str(i+1), (V_true[i].real, V_true[i].imag), fontsize=7,
                    textcoords="offset points", xytext=(5, 5))

    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('電圧フェーザー図 (○真値, ×推定値)')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    # 単位円
    circle = plt.Circle((0, 0), 1.0, fill=False, color='gray', linestyle='--', alpha=0.5)
    ax.add_patch(circle)
    ax.set_xlim(0.85, 1.05)
    ax.set_ylim(-0.15, 0.05)

    # (4) 観測深度と推定精度の関係
    ax = axes[1, 1]
    # 接続行列による観測深度
    f_mat = np.eye(n, dtype=int)
    for (i, j, _) in sys['branches']:
        f_mat[i-1, j-1] = 1
        f_mat[j-1, i-1] = 1
    x_vec = np.zeros(n, dtype=int)
    for b in pmu_buses:
        x_vec[b-1] = 1
    depth = f_mat @ x_vec

    abs_errors = np.abs(errors)
    scatter = ax.scatter(depth, abs_errors, c=colors, s=100, edgecolors='white', zorder=3)
    for i in range(n):
        ax.annotate(str(i+1), (depth[i], abs_errors[i]), fontsize=8,
                    textcoords="offset points", xytext=(5, 3))
    ax.set_xlabel('観測深度 d (観測可能なPMU数)')
    ax.set_ylabel('|推定誤差| [deg]')
    ax.set_title('観測深度 vs 推定精度')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('estimation_comparison.png', dpi=150, bbox_inches='tight')
    print("\nSaved: estimation_comparison.png")
    plt.show()


# =============================================================================
# Level 4: PMU数による推定精度の変化
# =============================================================================

def compare_pmu_counts(sys, theta_true, V_true, B):
    """PMU配置パターンごとの推定精度を比較"""

    scenarios = [
        ("2 PMUs (不足)", [2, 9]),
        ("4 PMUs (最適)", [2, 7, 10, 13]),
        ("6 PMUs (冗長)", [2, 4, 7, 9, 10, 13]),
        ("8 PMUs (高冗長)", [1, 2, 4, 6, 7, 9, 10, 13]),
    ]

    print("\n" + "=" * 70)
    print("PMU配置パターン別の推定精度比較")
    print("=" * 70)

    results = []
    for label, pmu_buses in scenarios:
        print(f"\n{'─'*70}")
        print(f"シナリオ: {label} → buses {pmu_buses}")
        print(f"{'─'*70}")

        # 観測性チェック
        topological_observability(sys, pmu_buses)

        # 状態推定
        np.random.seed(42)  # 再現性のため
        theta_hat, V_est = state_estimation_wls(sys, pmu_buses, theta_true, V_true)

        if theta_hat is not None:
            rmse = np.degrees(np.sqrt(np.mean((theta_hat - theta_true)**2)))
            results.append((label, pmu_buses, rmse, theta_hat, V_est))
        else:
            results.append((label, pmu_buses, None, None, None))

    # サマリー表
    print("\n" + "=" * 70)
    print("サマリー: PMU数と推定精度")
    print("=" * 70)
    print(f"{'シナリオ':>20} {'PMU数':>6} {'RMSE[deg]':>12} {'状態推定':>10}")
    print("-" * 54)
    for label, pmu_buses, rmse, _, _ in results:
        if rmse is not None:
            print(f"{label:>20} {len(pmu_buses):6d} {rmse:12.6f} {'成功':>10}")
        else:
            print(f"{label:>20} {len(pmu_buses):6d} {'---':>12} {'不可能':>10}")

    return results


# =============================================================================
# メイン実行
# =============================================================================

def main():
    print("╔" + "═"*68 + "╗")
    print("║  PMU配置問題の根本原理 — 潮流計算から状態推定まで              ║")
    print("╚" + "═"*68 + "╝")

    sys = ieee14_system()

    # Step 1: 潮流計算で「真の系統状態」を得る
    print("\n\n" + "▓"*70)
    print("  STEP 1: DC潮流計算 → 真の電圧・位相角を計算")
    print("▓"*70)
    theta_true, V_true, B = dc_power_flow(sys)

    # Step 2: 最適PMU配置でトポロジー的観測性を確認
    print("\n\n" + "▓"*70)
    print("  STEP 2: トポロジー的観測性チェック")
    print("▓"*70)
    pmu_optimal = [2, 7, 10, 13]  # BILP最適解
    topological_observability(sys, pmu_optimal)

    # Step 3: PMU計測 → 状態推定 → 推定電圧 vs 計測電圧
    print("\n\n" + "▓"*70)
    print("  STEP 3: 状態推定 (WLS) — 計測電圧 vs 推定電圧")
    print("▓"*70)
    np.random.seed(42)
    theta_hat, V_est = state_estimation_wls(sys, pmu_optimal, theta_true, V_true)

    # Step 4: 可視化
    if theta_hat is not None:
        print("\n\n" + "▓"*70)
        print("  STEP 4: 可視化")
        print("▓"*70)
        visualize_estimation(sys, pmu_optimal, theta_true, V_true, theta_hat, V_est)

    # Step 5: PMU数による精度比較
    print("\n\n" + "▓"*70)
    print("  STEP 5: PMU配置パターン別の精度比較")
    print("▓"*70)
    compare_pmu_counts(sys, theta_true, V_true, B)


if __name__ == "__main__":
    main()
