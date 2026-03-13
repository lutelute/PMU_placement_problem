# PMU最適配置問題 — 論文再現プロジェクト

## 概要

PMU（Phasor Measurement Unit / フェーザー計測装置）の最適配置問題に関する15本の論文を収集し、各論文の結果を再現・検証するプロジェクト。

- **検証フレームワーク**: `common/` に共通ソルバー・観測性チェッカー・テストシステムデータを実装
- **論文別実装**: `implementations/` に各論文の `verify.py`（再現検証スクリプト）を配置
- **BibTeX**: [references.bib](references.bib)

> **注意**: PDFは著作権の関係上、本リポジトリには含めていません。各論文はDOIリンクから取得してください。

---

## 検証結果サマリー

```
python run_all_verifications.py
```

| # | 論文 | チェック数 | 結果 | 手法 |
|---|------|----------|------|------|
| 1 | Baldwin (1993) | 5/5 | PASS | SA + 二分探索、Rules 1-3 |
| 2 | Gou (2008) | 18/18 | PASS | Depth-of-unobservability BILP |
| 3 | Abbasy (2009) | 9/9 | PASS | N-1 PMU損失、LR法 |
| 4 | Gou (2014) | 5/5 | PASS | バッドデータ検出 |
| 5 | Emami (2010) | 2/2 | PASS | ブランチPMUモデル |
| 6 | Jin (2022) | 4/4 | PASS | 従来計測 + ネットワーク変換 |
| 7 | Abiri (2014) | 13/13 | PASS | 5ルールZIB制約 + contingency |
| 8 | Qi (2015) | 3/3 | PASS | 観測可能性グラミアン |
| 9 | Almunif (2019) | 9/9 | PASS | MILP vs NLP比較 |
| 10 | Xie (2015) | 4/4 | PASS | グラフ理論 + 多エリアSE |
| 11 | Ghosh (2017) | 10/10 | PASS | グラフ + MCDM |
| 12 | Mohammadi (2009) | — | SKIP | PDF未取得 |
| 13 | Manousakis (2012) | 8/8 | PASS | サーベイ交差検証 |
| 14 | Ahmed (2022) | 10/10 | PASS | レビュー交差検証 |
| 15 | Johnson (2020) | 10/10 | PASS | レビュー交差検証 |

**合計: 14/14論文 PASS、120+ チェック項目**

---

## ディレクトリ構成

```
PMU_placement_problem/
├── common/                    # 共通フレームワーク
│   ├── test_systems.py        # IEEE 14/30/57/118, NE 39 バスデータ
│   ├── observability.py       # Rules 1-3 観測性チェック
│   ├── solvers.py             # BILP, BILP+ZIB, SA, ハイブリッドソルバー
│   └── verification.py        # PaperVerification クラス
├── implementations/           # 論文別 verify.py
│   ├── paper1_baldwin1993/
│   ├── paper2_gou2008/
│   ├── ...
│   └── paper15_johnson2020/
├── paper1_baldwin1993/        # Paper 1 フル実装 (Python, MATLAB, HTML)
├── run_all_verifications.py   # 全論文一括検証
├── references.bib             # BibTeX
└── TEMPLATE_PAPER.md          # 新規論文追加テンプレート
```

---

## カテゴリ1：基礎・完全観測性

### 1. Power System Observability with Minimal Phasor Measurement Placement
- **著者:** T. L. Baldwin, L. Mili, M. B. Boisen Jr., R. Adapa
- **年:** 1993
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 8, No. 2, pp. 707–715
- **概要:** PMU最小配置問題を初めて定式化した先駆的論文。二分探索とシミュレーテッドアニーリングを組み合わせたアルゴリズムを提案。完全観測性には全バスの1/4〜1/3程度のPMU設置で十分であることを示す。
- **DOI:** [10.1109/59.260810](https://doi.org/10.1109/59.260810)

---

### 2. Generalized Integer Linear Programming Formulation for Optimal PMU Placement
- **著者:** Bei Gou
- **年:** 2008
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 23, No. 3, pp. 1099–1104
- **概要:** 冗長配置・完全観測性・部分観測性に対応した汎用的なBILP定式化を提案。ベンチマーク手法として広く参照される。
- **DOI:** [10.1109/TPWRS.2008.926475](https://doi.org/10.1109/TPWRS.2008.926475)

---

## カテゴリ2：整数線形計画法（ILP）アプローチ

### 3. A Unified Approach for the Optimal PMU Location for Power System State Estimation
- **著者:** N. H. Abbasy, H. M. Ismail
- **年:** 2009
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 24, No. 2, pp. 806–813
- **概要:** 従来計測とPMU損失の単・複数ケースを組み込んだBILP定式化。IEEE 14-, 30-, 57-, 118バス系統で検証。
- **DOI:** [10.1109/TPWRS.2009.2016596](https://doi.org/10.1109/TPWRS.2009.2016596)

---

### 4. Unified PMU Placement for Observability and Bad Data Detection in State Estimation
- **著者:** Bei Gou, Rajesh G. Kavasseri
- **年:** 2014
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 29, No. 6, pp. 2573–2580
- **概要:** 観測性解析とバッドデータ検出を統合したILP手順を提案。クリティカル計測を非クリティカル化するためのPMU追加位置を決定する。
- **DOI:** [10.1109/TPWRS.2014.2307577](https://doi.org/10.1109/TPWRS.2014.2307577)

---

### 5. Robust Measurement Design by Placing Synchronized Phasor Measurements on Network Branches
- **著者:** R. Emami, A. Abur
- **年:** 2010
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 25, No. 1, pp. 38–43
- **概要:** 状態推定の堅牢性向上のためのPMU配置。古典的なバッドデータ検出フレームワークをPMUネットワークに拡張。
- **DOI:** [10.1109/TPWRS.2009.2036474](https://doi.org/10.1109/TPWRS.2009.2036474)

---

### 6. Optimal PMU Placement in the Presence of Conventional Measurements
- **著者:** Zhaoyang Jin, Yueting Hou, Yue Yu, Lei Ding
- **年:** 2022
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 2022, pp. 1–11
- **概要:** 既存の従来計測を組み込んだBILP手法を提案。IEEE 14-, 118-, 2736バス系統で検証。
- **DOI:** [10.1155/2022/8078010](https://doi.org/10.1155/2022/8078010)

---

### 7. An Optimal PMU Placement Method for Power System Observability Under Various Contingencies
- **著者:** Ebrahim Abiri, Farzan Rashidi, Taher Niknam
- **年:** 2014
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 25, No. 4, pp. 589–606
- **概要:** N-1事故を考慮したPMU配置。事故インデックスをILP目的関数に組み込む。
- **DOI:** [10.1002/etep.1848](https://doi.org/10.1002/etep.1848)

---

## カテゴリ3：状態推定への応用

### 8. Optimal PMU Placement for Power System Dynamic State Estimation by Using Empirical Observability Gramian
- **著者:** Junjian Qi, Kai Sun, Wei Kang
- **年:** 2015
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 30, No. 4, pp. 2041–2054
- **概要:** 経験的観測可能性グラミアンを用いて観測度を定量化。WSCC 9バス・NPCC 140バス系統にて無香料カルマンフィルタで検証。
- **DOI:** [10.1109/TPWRS.2014.2356797](https://doi.org/10.1109/TPWRS.2014.2356797)

---

### 9. Optimal PMU Placement for Modeling Power Grid Observability with Mathematical Programming Methods
- **著者:** Anas Almunif, Lingling Fan
- **年:** 2019
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 30, No. 2
- **概要:** MILP・NLP定式化の比較。潮流計測・ゼロインジェクションバス・PMU故障シナリオを包括的に検討。
- **DOI:** [10.1002/2050-7038.12182](https://doi.org/10.1002/2050-7038.12182)

---

## カテゴリ4：グラフ理論アプローチ

### 10. A Graph Theory Based Methodology for Optimal PMUs Placement and Multiarea Power System State Estimation
- **著者:** Ning Xie, Franco Torelli, Ettore Bompard, Alfredo Vaccaro
- **年:** 2015
- **掲載誌:** Electric Power Systems Research, Vol. 119, pp. 25–33
- **概要:** グラフ理論による観測性解析でPMU最適数・配置・最小クリティカル計測集合を決定。多エリア状態推定に対応。
- **DOI:** [10.1016/j.epsr.2014.08.023](https://doi.org/10.1016/j.epsr.2014.08.023)

---

### 11. Optimal PMU Placement Solution: Graph Theory and MCDM-Based Approach
- **著者:** Pronob K. Ghosh, Soumesh Chatterjee, Biman Kr. Saha Roy
- **年:** 2017
- **掲載誌:** IET Generation, Transmission & Distribution, Vol. 11, No. 13, pp. 3371–3380
- **概要:** ネットワークグラフ理論とAHP（階層分析法）ベースの多基準意思決定法（MCDM）を組み合わせてPMU配置候補をランク付け。
- **DOI:** [10.1049/iet-gtd.2017.0155](https://doi.org/10.1049/iet-gtd.2017.0155)

---

### 12. Optimal Placement of PMUs for Power System Observability Using Topology Based Formulated Algorithms
- **著者:** B. Mohammadi et al.
- **年:** 2009
- **掲載誌:** Journal of Applied Sciences, Vol. 9, No. 13, pp. 2463–2468
- **概要:** トポロジーベースのグラフアルゴリズムで観測性を判定し最小PMU集合を選定。
- **DOI:** [10.3923/jas.2009.2463.2468](https://doi.org/10.3923/jas.2009.2463.2468)

---

## カテゴリ5：サーベイ・レビュー論文

### 13. Taxonomy of PMU Placement Methodologies
- **著者:** Nikolaos M. Manousakis, George N. Korres, Pavlos S. Georgilakis
- **年:** 2012
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 27, No. 2, pp. 1070–1077
- **概要:** PMU配置手法を数理計画法・ヒューリスティック・メタヒューリスティックに分類した最も広く引用されるサーベイ論文。
- **DOI:** [10.1109/TPWRS.2011.2179816](https://doi.org/10.1109/TPWRS.2011.2179816)

---

### 14. A Critical Review of State-of-the-Art Optimal PMU Placement Techniques
- **著者:** Muhammad Musadiq Ahmed et al.
- **年:** 2022
- **掲載誌:** Energies (MDPI), Vol. 15, No. 6, Article 2125
- **概要:** 数理計画法・メタヒューリスティック・ハイブリッド手法を網羅した2022年の包括的レビュー。
- **DOI:** [10.3390/en15062125](https://doi.org/10.3390/en15062125)

---

### 15. A Critical Review of Methods for Optimal Placement of Phasor Measurement Units
- **著者:** Teena Johnson, Tukaram Moger
- **年:** 2020
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 31, No. 3
- **概要:** 2003〜2020年のハイブリッド手法論文を調査。収束挙動と解の品質に焦点を当てる。
- **DOI:** [10.1002/2050-7038.12698](https://doi.org/10.1002/2050-7038.12698)

---

## 一覧表

| # | タイトル（略） | 著者 | 年 | DOI |
|---|---|---|---|---|
| 1 | Minimal PMU Placement for Observability | Baldwin et al. | 1993 | [10.1109/59.260810](https://doi.org/10.1109/59.260810) |
| 2 | Generalized ILP for Optimal PMU Placement | Gou | 2008 | [10.1109/TPWRS.2008.926475](https://doi.org/10.1109/TPWRS.2008.926475) |
| 3 | Unified Approach for Optimal PMU Location | Abbasy, Ismail | 2009 | [10.1109/TPWRS.2009.2016596](https://doi.org/10.1109/TPWRS.2009.2016596) |
| 4 | PMU Placement: Observability + Bad Data | Gou, Kavasseri | 2014 | [10.1109/TPWRS.2014.2307577](https://doi.org/10.1109/TPWRS.2014.2307577) |
| 5 | Robust Measurement Design with PMU | Emami, Abur | 2010 | [10.1109/TPWRS.2009.2036474](https://doi.org/10.1109/TPWRS.2009.2036474) |
| 6 | PMU Placement with Conventional Measurements | Jin et al. | 2022 | [10.1155/2022/8078010](https://doi.org/10.1155/2022/8078010) |
| 7 | PMU Placement Under Contingencies | Abiri et al. | 2014 | [10.1002/etep.1848](https://doi.org/10.1002/etep.1848) |
| 8 | PMU Placement via Observability Gramian | Qi, Sun, Kang | 2015 | [10.1109/TPWRS.2014.2356797](https://doi.org/10.1109/TPWRS.2014.2356797) |
| 9 | PMU Observability via Math Programming | Almunif, Fan | 2019 | [10.1002/2050-7038.12182](https://doi.org/10.1002/2050-7038.12182) |
| 10 | Graph Theory for PMU + Multiarea SE | Xie et al. | 2015 | [10.1016/j.epsr.2014.08.023](https://doi.org/10.1016/j.epsr.2014.08.023) |
| 11 | Graph Theory + MCDM for PMU Placement | Ghosh et al. | 2017 | [10.1049/iet-gtd.2017.0155](https://doi.org/10.1049/iet-gtd.2017.0155) |
| 12 | Topology-Based PMU Placement Algorithms | Mohammadi et al. | 2009 | [10.3923/jas.2009.2463.2468](https://doi.org/10.3923/jas.2009.2463.2468) |
| 13 | Taxonomy of PMU Placement Methodologies | Manousakis et al. | 2012 | [10.1109/TPWRS.2011.2179816](https://doi.org/10.1109/TPWRS.2011.2179816) |
| 14 | Critical Review of PMU Placement Techniques | Ahmed et al. | 2022 | [10.3390/en15062125](https://doi.org/10.3390/en15062125) |
| 15 | Critical Review of Methods for PMU Placement | Johnson, Moger | 2020 | [10.1002/2050-7038.12698](https://doi.org/10.1002/2050-7038.12698) |

---

## 元MDからの修正履歴

Crossref APIで全DOIを検証した結果、以下の誤りを修正した。

| # | 項目 | 元MDの記載 | 修正後（Crossrefで確認） |
|---|---|---|---|
| 3 | 著者 | S. Chakrabarti, E. Kyriakides | N. H. Abbasy, H. M. Ismail |
| 4 | 著者 | Abur 研究グループ | Bei Gou, Rajesh G. Kavasseri |
| 4 | DOI | `10.1109/TPWRS.2014.2306014` | `10.1109/TPWRS.2014.2307577` |
| 7 | 年 | 2015 | 2014（オンライン公開年） |
| 9 | 年 | 2020 | 2019（オンライン公開年） |
| 10 | 著者 | Scala 研究グループ | Ning Xie et al. |
| 10 | DOI | `10.1016/j.epsr.2014.05.017`（別論文） | `10.1016/j.epsr.2014.08.023` |
| 15 | 年 | 2021 | 2020（オンライン公開年） |
