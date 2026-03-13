# PMU最適配置に関する論文リスト

## 概要
PMU（Phasor Measurement Unit / フェーザー計測装置）をどこに導入すべきかを論じた論文のまとめ。

---

## カテゴリ1：基礎・完全観測性

### 1. Power System Observability with Minimal Phasor Measurement Placement
- **著者:** T. L. Baldwin, L. Mili, M. B. Boisen Jr., R. Adapa
- **年:** 1993
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 8, No. 2, pp. 707–715
- **概要:** PMU最小配置問題を初めて定式化した先駆的論文。二分探索とシミュレーテッドアニーリングを組み合わせたアルゴリズムを提案。完全観測性には全バスの1/4〜1/3程度のPMU設置で十分であることを示す。
- **DOI:** [10.1109/59.260810](https://doi.org/10.1109/59.260810)
- **IEEE Xplore:** https://ieeexplore.ieee.org/document/260810/

---

### 2. Generalized Integer Linear Programming Formulation for Optimal PMU Placement
- **著者:** Bei Gou
- **年:** 2008
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 23, No. 3, pp. 1099–1104
- **概要:** 冗長配置・完全観測性・部分観測性に対応した汎用的なBILP（二値整数線形計画法）定式化を提案。ベンチマーク手法として広く参照される。
- **DOI:** [10.1109/TPWRS.2008.926475](https://doi.org/10.1109/TPWRS.2008.926475)
- **IEEE Xplore:** https://ieeexplore.ieee.org/document/4562140/

---

## カテゴリ2：整数線形計画法（ILP）アプローチ

### 3. A Unified Approach for the Optimal PMU Location for Power System State Estimation
- **著者:** S. Chakrabarti, E. Kyriakides
- **年:** 2009
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 24, No. 2, pp. 806–813
- **概要:** 従来計測とPMU損失の単・複数ケースを組み込んだBILP定式化。IEEE 14-, 30-, 57-, 118バス系統で検証。
- **DOI:** [10.1109/TPWRS.2009.2016596](https://doi.org/10.1109/TPWRS.2009.2016596)
- **IEEE Xplore:** https://ieeexplore.ieee.org/abstract/document/4839066

---

### 4. Unified PMU Placement for Observability and Bad Data Detection in State Estimation
- **著者:** Abur 研究グループ
- **年:** 2014
- **掲載誌:** IEEE Transactions on Power Systems
- **概要:** 観測性解析とバッドデータ検出を統合したILP手順を提案。クリティカル計測を非クリティカル化するためのPMU追加位置を決定する。
- **DOI:** [10.1109/TPWRS.2014.2306014](https://doi.org/10.1109/TPWRS.2014.2306014)
- **IEEE Xplore:** https://ieeexplore.ieee.org/document/6777591/

---

### 5. Robust Measurement Design by Placing Synchronized Phasor Measurements on Network Branches
- **著者:** R. Emami, A. Abur
- **年:** 2010
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 25, No. 1, pp. 38–43
- **概要:** 状態推定の堅牢性向上のためのPMU配置。古典的なバッドデータ検出フレームワークをPMUネットワークに拡張。
- **DOI:** [10.1109/TPWRS.2009.2036474](https://doi.org/10.1109/TPWRS.2009.2036474)

---

### 6. Optimal PMU Placement in the Presence of Conventional Measurements
- **著者:** Jin et al.
- **年:** 2022
- **掲載誌:** International Transactions on Electrical Energy Systems (Wiley/Hindawi)
- **概要:** 既存の従来計測を組み込んだBILP手法を提案。IEEE 14-, 118-, 2736バス系統で検証。
- **DOI:** [10.1155/2022/8078010](https://doi.org/10.1155/2022/8078010)
- **Wiley:** https://onlinelibrary.wiley.com/doi/10.1155/2022/8078010

---

### 7. An Optimal PMU Placement Method for Power System Observability Under Various Contingencies
- **著者:** E. Abiri et al.
- **年:** 2015
- **掲載誌:** International Transactions on Electrical Energy Systems, Wiley, Vol. 25
- **概要:** N-1事故を考慮したPMU配置。事故インデックスをILP目的関数に組み込む。
- **DOI:** [10.1002/etep.1848](https://doi.org/10.1002/etep.1848)
- **Wiley:** https://onlinelibrary.wiley.com/doi/abs/10.1002/etep.1848

---

## カテゴリ3：状態推定への応用

### 8. Optimal PMU Placement for Power System Dynamic State Estimation by Using Empirical Observability Gramian
- **著者:** J. Qi, K. Sun, W. Kang
- **年:** 2015
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 30, No. 4, pp. 2041–2054
- **概要:** 経験的観測可能性グラミアンを用いて観測度を定量化。WSCC 9バス・NPCC 140バス系統にて無香料カルマンフィルタで検証。
- **DOI:** [10.1109/TPWRS.2014.2356797](https://doi.org/10.1109/TPWRS.2014.2356797)
- **arXiv:** https://arxiv.org/pdf/1405.6412

---

### 9. Optimal PMU Placement for Modeling Power Grid Observability with Mathematical Programming Methods
- **著者:** A. Almunif, L. Fan
- **年:** 2020
- **掲載誌:** International Transactions on Electrical Energy Systems, Wiley
- **概要:** MILP・NLP定式化の比較。潮流計測・ゼロインジェクションバス・PMU故障シナリオを包括的に検討。
- **DOI:** [10.1002/2050-7038.12182](https://doi.org/10.1002/2050-7038.12182)
- **Wiley:** https://onlinelibrary.wiley.com/doi/abs/10.1002/2050-7038.12182

---

## カテゴリ4：グラフ理論アプローチ

### 10. A Graph Theory Based Methodology for Optimal PMUs Placement and Multiarea Power System State Estimation
- **著者:** Scala 研究グループ
- **年:** 2014
- **掲載誌:** Electric Power Systems Research, Elsevier, Vol. 116, pp. 134–143
- **概要:** グラフ理論による観測性解析でPMU最適数・配置・最小クリティカル計測集合を決定。多エリア状態推定に対応。
- **DOI:** [10.1016/j.epsr.2014.05.017](https://doi.org/10.1016/j.epsr.2014.05.017)
- **ScienceDirect:** https://www.sciencedirect.com/science/article/abs/pii/S0378779614003204

---

### 11. Optimal PMU Placement Solution: Graph Theory and MCDM-Based Approach
- **著者:** 複数著者
- **年:** 2017
- **掲載誌:** IET Generation, Transmission & Distribution, Vol. 11, No. 14
- **概要:** ネットワークグラフ理論とAHP（階層分析法）ベースの多基準意思決定法（MCDM）を組み合わせてPMU配置候補をランク付け。
- **DOI:** [10.1049/iet-gtd.2017.0155](https://doi.org/10.1049/iet-gtd.2017.0155)
- **IET Digital Library:** https://digital-library.theiet.org/doi/10.1049/iet-gtd.2017.0155

---

### 12. Optimal Placement of PMUs for Power System Observability Using Topology Based Formulated Algorithms
- **著者:** 複数著者
- **年:** 2009
- **掲載誌:** Journal of Applied Sciences, Vol. 9, No. 13, pp. 2463–2468
- **概要:** トポロジーベースのグラフアルゴリズムで観測性を判定し最小PMU集合を選定。
- **DOI:** [10.3923/jas.2009.2463.2468](https://doi.org/10.3923/jas.2009.2463.2468)
- **Full text:** https://scialert.net/fulltext/?doi=jas.2009.2463.2468

---

## カテゴリ5：サーベイ・レビュー論文

### 13. Taxonomy of PMU Placement Methodologies
- **著者:** N. M. Manousakis, G. N. Korres, P. S. Georgilakis
- **年:** 2012
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 27, No. 2, pp. 1070–1077
- **概要:** PMU配置手法を数理計画法・ヒューリスティック・メタヒューリスティックに分類した最も広く引用されるサーベイ論文。
- **DOI:** [10.1109/TPWRS.2011.2179816](https://doi.org/10.1109/TPWRS.2011.2179816)
- **ResearchGate:** https://www.researchgate.net/publication/260509656

---

### 14. A Critical Review of State-of-the-Art Optimal PMU Placement Techniques
- **著者:** M. M. Ahmed, M. Amjad, M. A. Qureshi et al.
- **年:** 2022
- **掲載誌:** Energies (MDPI), Vol. 15, No. 6, Article 2125
- **概要:** 数理計画法・メタヒューリスティック・ハイブリッド手法を網羅した2022年の包括的レビュー。テスト系統やソルバー性能の比較表あり。
- **DOI:** [10.3390/en15062125](https://doi.org/10.3390/en15062125)
- **MDPI:** https://www.mdpi.com/1996-1073/15/6/2125

---

### 15. A Critical Review of Methods for Optimal Placement of Phasor Measurement Units
- **著者:** T. Johnson et al.
- **年:** 2021
- **掲載誌:** International Transactions on Electrical Energy Systems, Wiley
- **概要:** 2003〜2020年のハイブリッド手法論文を調査。収束挙動と解の品質に焦点を当てる。
- **DOI:** [10.1002/2050-7038.12698](https://doi.org/10.1002/2050-7038.12698)
- **Wiley:** https://onlinelibrary.wiley.com/doi/full/10.1002/2050-7038.12698

---

## 一覧表

| # | タイトル（略） | 著者 | 年 | 掲載誌 | DOI |
|---|---|---|---|---|---|
| 1 | Minimal PMU Placement for Observability | Baldwin et al. | 1993 | IEEE Trans. Power Syst. | [10.1109/59.260810](https://doi.org/10.1109/59.260810) |
| 2 | Generalized ILP for Optimal PMU Placement | Gou | 2008 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2008.926475](https://doi.org/10.1109/TPWRS.2008.926475) |
| 3 | Unified Approach for Optimal PMU Location | Chakrabarti, Kyriakides | 2009 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2009.2016596](https://doi.org/10.1109/TPWRS.2009.2016596) |
| 4 | PMU Placement: Observability + Bad Data | Abur group | 2014 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2014.2306014](https://doi.org/10.1109/TPWRS.2014.2306014) |
| 5 | Robust Measurement Design with PMU | Emami, Abur | 2010 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2009.2036474](https://doi.org/10.1109/TPWRS.2009.2036474) |
| 6 | PMU Placement with Conventional Measurements | Jin et al. | 2022 | Int. Trans. Elec. Energy Syst. | [10.1155/2022/8078010](https://doi.org/10.1155/2022/8078010) |
| 7 | PMU Placement Under N-1 Contingencies | Abiri et al. | 2015 | Int. Trans. Elec. Energy Syst. | [10.1002/etep.1848](https://doi.org/10.1002/etep.1848) |
| 8 | PMU Placement via Observability Gramian | Qi, Sun, Kang | 2015 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2014.2356797](https://doi.org/10.1109/TPWRS.2014.2356797) |
| 9 | PMU Observability via Math Programming | Almunif, Fan | 2020 | Int. Trans. Elec. Energy Syst. | [10.1002/2050-7038.12182](https://doi.org/10.1002/2050-7038.12182) |
| 10 | Graph Theory for PMU + Multiarea SE | Scala group | 2014 | Elec. Power Syst. Research | [10.1016/j.epsr.2014.05.017](https://doi.org/10.1016/j.epsr.2014.05.017) |
| 11 | Graph Theory + MCDM for PMU Placement | 複数 | 2017 | IET Gen. Trans. Distrib. | [10.1049/iet-gtd.2017.0155](https://doi.org/10.1049/iet-gtd.2017.0155) |
| 12 | Topology-Based PMU Placement Algorithms | 複数 | 2009 | J. Applied Sciences | [10.3923/jas.2009.2463.2468](https://doi.org/10.3923/jas.2009.2463.2468) |
| 13 | Taxonomy of PMU Placement Methodologies | Manousakis et al. | 2012 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2011.2179816](https://doi.org/10.1109/TPWRS.2011.2179816) |
| 14 | Critical Review of PMU Placement Techniques | Ahmed et al. | 2022 | Energies (MDPI) | [10.3390/en15062125](https://doi.org/10.3390/en15062125) |
| 15 | Critical Review of Methods for PMU Placement | Johnson et al. | 2021 | Int. Trans. Elec. Energy Syst. | [10.1002/2050-7038.12698](https://doi.org/10.1002/2050-7038.12698) |
