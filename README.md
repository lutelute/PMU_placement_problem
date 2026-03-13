# PMU最適配置問題 — 論文再現シミュレーション

> **[インタラクティブデモ（GitHub Pages）](https://lutelute.github.io/PMU_placement_problem/)**

15本の論文のアルゴリズムを再現実装し、各論文の結果テーブルと照合検証。14本のインタラクティブデモでPMU配置を直感的に体験できます。

---

## デモ一覧

| # | 論文 | 手法 | デモ |
|---|------|------|------|
| 1 | Baldwin (1993) | SA + 二分探索 / Rules 1-3 | [DEMO](https://lutelute.github.io/PMU_placement_problem/paper1_baldwin1993/html/) |
| 2 | Gou (2008) | Depth-of-unobservability BILP | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper2_gou2008/html/) |
| 3 | Abbasy (2009) | N-1 PMU損失 / LR法 | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper3_abbasy2009/html/) |
| 4 | Gou (2014) | 観測性 + 不良データ検出 | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper4_gou2014/html/) |
| 5 | Emami (2010) | ブランチPMUモデル | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper5_emami2010/html/) |
| 6 | Jin (2022) | 従来計測 + ネットワーク変換 | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper6_jin2022/html/) |
| 7 | Abiri (2014) | 5ルールZIB + contingency | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper7_abiri2014/html/) |
| 8 | Qi (2015) | 観測可能性グラミアン | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper8_qi2015/html/) |
| 9 | Almunif (2019) | MILP vs NLP比較 | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper9_almunif2019/html/) |
| 10 | Xie (2015) | グラフ理論 / 貪欲法 | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper10_xie2015/html/) |
| 11 | Ghosh (2017) | グラフ + MCDM (AHP) | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper11_ghosh2017/html/) |
| 12 | Mohammadi (2009) | トポロジーベース | PDF未取得のためSKIP |
| 13 | Manousakis (2012) | サーベイ（44文献分類） | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper13_manousakis2012/html/) |
| 14 | Ahmed (2022) | レビュー（LP/GA/PSO比較） | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper14_ahmed2022/html/) |
| 15 | Johnson (2020) | レビュー（ハイブリッド手法） | [DEMO](https://lutelute.github.io/PMU_placement_problem/implementations/paper15_johnson2020/html/) |

---

## 検証結果

```
python run_all_verifications.py
```

**14/14論文 PASS — 120+ チェック項目**

---

## PMU最適配置の基準値（文献コンセンサス）

| テスト系統 | バス数 | ZIBなし | ZIBあり | N-1 PMU損失 |
|-----------|--------|---------|---------|------------|
| IEEE 14 | 14 | 4 | 3 | 9 |
| IEEE 30 | 30 | 10 | 7 | — |
| New England 39 | 39 | 13 | 8 | — |
| IEEE 57 | 57 | 17 | 11 | 35 |
| IEEE 118 | 118 | 32 | 28 | 75 |

---

## ディレクトリ構成

```
PMU_placement_problem/
├── index.html                 # トップページ（GitHub Pages）
├── common/                    # 共通フレームワーク
│   ├── test_systems.py        #   IEEE 14/30/57/118, NE 39 バスデータ
│   ├── observability.py       #   Rules 1-3 観測性チェック
│   ├── solvers.py             #   BILP, BILP+ZIB, SA, ハイブリッドソルバー
│   └── verification.py        #   PaperVerification クラス
├── implementations/           # 論文別実装
│   ├── paper1_baldwin1993/    #   各論文ごとに:
│   │   ├── verify.py          #     再現検証スクリプト
│   │   └── html/index.html    #     インタラクティブデモ
│   ├── paper2_gou2008/
│   ├── ...
│   └── paper15_johnson2020/
├── run_all_verifications.py   # 全論文一括検証
├── references.bib             # BibTeX
└── .github/workflows/         # GitHub Pages 自動デプロイ
```

---

## 論文詳細

### カテゴリ1：基礎・完全観測性

**1. Power System Observability with Minimal Phasor Measurement Placement**
Baldwin et al. (1993) — IEEE Trans. Power Systems — [DOI](https://doi.org/10.1109/59.260810)

PMU最小配置問題（OPP）を初めて体系的に定式化した先駆的論文。観測性の3ルール（直接観測・隣接観測・KCL伝搬）を定義し、二分探索とシミュレーテッドアニーリング（SA）を組み合わせた解法を提案。IEEE 14/30/57/118-busで検証し、全バスの1/4〜1/3程度のPMUで完全観測性が達成できることを実証した。

---

**2. Generalized Integer Linear Programming Formulation for Optimal PMU Placement**
Gou (2008) — IEEE Trans. Power Systems — [DOI](https://doi.org/10.1109/TPWRS.2008.926475)

「非観測深度（Depth-of-Unobservability）」の概念を導入し、完全観測性（Depth-0）を一般化。接続行列のべき乗 f^(d+1)·x ≥ 1 による定式化で、Depth-1に緩和するだけでPMU数が約50%削減されることを示した。BILPとして厳密解が得られる点が強み。

---

### カテゴリ2：整数線形計画法（ILP）アプローチ

**3. A Unified Approach for the Optimal PMU Location for Power System State Estimation**
Abbasy, Ismail (2009) — IEEE Trans. Power Systems — [DOI](https://doi.org/10.1109/TPWRS.2009.2016596)

従来計測（SCADA）の存在、PMU単一損失（N-1）、複数PMU同時損失を統一的に扱うBILP定式化を提案。ラグランジュ緩和（LR）法により大規模系統でも効率的に求解可能。IEEE 14-busでN-1 PMU損失時に9台が必要であることを示した。

---

**4. Unified PMU Placement for Observability and Bad Data Detection in State Estimation**
Gou, Kavasseri (2014) — IEEE Trans. Power Systems — [DOI](https://doi.org/10.1109/TPWRS.2014.2307577)

観測性確保とバッドデータ検出（BDD）能力を同時に最適化する統合定式化。ヤコビアンのLDL^T分解により問題サイズを縮小。従来計測が十分にある場合、IEEE 14-busでわずか1台のPMUで観測可能になることを示した。

---

**5. Robust Measurement Design by Placing Synchronized Phasor Measurements on Network Branches**
Emami, Abur (2010) — IEEE Trans. Power Systems — [DOI](https://doi.org/10.1109/TPWRS.2009.2036474)

従来のバス設置型ではなく、ブランチ（送電線）にPMUを配置するモデルを提案。線路の両端電圧・電流を同時計測することで、状態推定の数値的堅牢性（条件数）を大幅に改善。測定冗長性の向上にも寄与する。

---

**6. Optimal PMU Placement in the Presence of Conventional Measurements**
Jin et al. (2022) — Int. Trans. Elec. Energy Syst. — [DOI](https://doi.org/10.1155/2022/8078010)

既存のSCADA計測を活用してPMU必要数を削減するBILP手法。ネットワーク変換（観測島のマージ）により従来計測をPMU等価に変換し、追加PMUの最小化を図る。実運用への移行を意識した実用的アプローチ。

---

**7. An Optimal PMU Placement Method for Power System Observability Under Various Contingencies**
Abiri et al. (2014) — Int. Trans. Elec. Energy Syst. — [DOI](https://doi.org/10.1002/etep.1848)

N-1送電線事故とN-1 PMU損失の両方を考慮した包括的な定式化。5つのZIBルール（KCL伝搬の拡張）による制約削減でPMU数を最小化。IEEE 14-busでZIBありの場合3台で完全観測性を達成。

---

### カテゴリ3：状態推定への応用

**8. Optimal PMU Placement for Power System Dynamic State Estimation by Using Empirical Observability Gramian**
Qi, Sun, Kang (2015) — IEEE Trans. Power Systems — [DOI](https://doi.org/10.1109/TPWRS.2014.2356797)

経験的観測可能性グラミアン（EOG）により系統の観測度を定量的に評価。グラミアン行列式の最大化を目的関数とし、動的状態推定（UKF: Unscented Kalman Filter）における最適なPMU配置を決定する。静的観測性だけでなく動的応答の推定精度も考慮した点が特徴。

---

**9. Optimal PMU Placement for Modeling Power Grid Observability with Mathematical Programming Methods**
Almunif, Fan (2019) — Int. Trans. Elec. Energy Syst. — [DOI](https://doi.org/10.1002/2050-7038.12182)

MILP（混合整数線形計画）とNLP（非線形計画）の定式化を体系的に比較。基本観測性・ZIB・潮流計測・PMU故障・チャネル制限の5シナリオで検証し、各手法の適用範囲と計算コストのトレードオフを明らかにした。

---

### カテゴリ4：グラフ理論アプローチ

**10. A Graph Theory Based Methodology for Optimal PMUs Placement and Multiarea Power System State Estimation**
Xie et al. (2015) — Electric Power Systems Research — [DOI](https://doi.org/10.1016/j.epsr.2014.08.023)

隣接行列から構成されるQ = A^T·A行列を用いたグラフ理論的アプローチ。貪欲法による近似解法で大規模系統にもスケール可能。多エリア分割での分散状態推定にも対応し、エリア間の境界バス処理を定式化。

---

**11. Optimal PMU Placement Solution: Graph Theory and MCDM-Based Approach**
Ghosh et al. (2017) — IET GTD — [DOI](https://doi.org/10.1049/iet-gtd.2017.0155)

グラフ理論で候補を絞り込み、AHP（階層分析法）ベースの多基準意思決定法（MCDM）で最終配置をランク付け。接続度・観測冗長性・経済性など複数の評価基準を統合的に扱う点が特徴。

---

**12. Optimal Placement of PMUs Using Topology Based Formulated Algorithms**
Mohammadi et al. (2009) — J. Applied Sciences — [DOI](https://doi.org/10.3923/jas.2009.2463.2468)

トポロジーベースのグラフアルゴリズムによるPMU配置手法。**PDF未取得のため検証スキップ。**

---

### カテゴリ5：サーベイ・レビュー

**13. Taxonomy of PMU Placement Methodologies**
Manousakis et al. (2012) — IEEE Trans. Power Systems — [DOI](https://doi.org/10.1109/TPWRS.2011.2179816)

PMU配置手法を数理計画法（LP/ILP）・ヒューリスティック（貪欲法・探索木）・メタヒューリスティック（GA/SA/PSO）に体系的に分類した、この分野で最も広く引用されるサーベイ。44文献をカバーし、各手法の長所・短所を比較。

---

**14. A Critical Review of State-of-the-Art Optimal PMU Placement Techniques**
Ahmed et al. (2022) — Energies (MDPI) — [DOI](https://doi.org/10.3390/en15062125)

LP・GA・PSO各手法カテゴリを網羅した2022年時点の包括的レビュー。SCADA計測とPMU計測の特性比較、ZIB・N-1制約の扱い方の違いなど、実装上の論点も整理。

---

**15. A Critical Review of Methods for Optimal Placement of Phasor Measurement Units**
Johnson, Moger (2020) — Int. Trans. Elec. Energy Syst. — [DOI](https://doi.org/10.1002/2050-7038.12698)

2003〜2020年の文献を対象に、単一手法からハイブリッド手法（GA+SA、PSO+ILPなど）への発展の潮流を分析。各ハイブリッド手法の組み合わせパターンと性能向上の傾向を整理した。

---

> **注意**: PDFは著作権の関係上、本リポジトリには含めていません。各論文はDOIリンクから取得してください。
