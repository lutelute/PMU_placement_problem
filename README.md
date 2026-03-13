# PMU最適配置に関する論文リスト

## 概要
PMU（Phasor Measurement Unit / フェーザー計測装置）をどこに導入すべきかを論じた論文のまとめ。
BibTeXデータは [references.bib](references.bib) を参照。

---

## カテゴリ1：基礎・完全観測性

### 1. Power System Observability with Minimal Phasor Measurement Placement
- **著者:** T. L. Baldwin, L. Mili, M. B. Boisen Jr., R. Adapa
- **年:** 1993
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 8, No. 2, pp. 707–715
- **概要:** PMU最小配置問題を初めて定式化した先駆的論文。二分探索とシミュレーテッドアニーリングを組み合わせたアルゴリズムを提案。完全観測性には全バスの1/4〜1/3程度のPMU設置で十分であることを示す。
- **DOI:** [10.1109/59.260810](https://doi.org/10.1109/59.260810)
- **BibTeX:** `Baldwin1993`
- **PDF:** [01_Baldwin1993_minimal_pmu_placement.pdf](pdf/01_Baldwin1993_minimal_pmu_placement.pdf)

---

### 2. Generalized Integer Linear Programming Formulation for Optimal PMU Placement
- **著者:** Bei Gou
- **年:** 2008
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 23, No. 3, pp. 1099–1104
- **概要:** 冗長配置・完全観測性・部分観測性に対応した汎用的なBILP（二値整数線形計画法）定式化を提案。ベンチマーク手法として広く参照される。
- **DOI:** [10.1109/TPWRS.2008.926475](https://doi.org/10.1109/TPWRS.2008.926475)
- **BibTeX:** `Gou2008`
- **PDF:** [02_Gou2008_generalized_ilp.pdf](pdf/02_Gou2008_generalized_ilp.pdf)

---

## カテゴリ2：整数線形計画法（ILP）アプローチ

### 3. A Unified Approach for the Optimal PMU Location for Power System State Estimation
- **著者:** N. H. Abbasy, H. M. Ismail
- **年:** 2009
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 24, No. 2, pp. 806–813
- **概要:** 従来計測とPMU損失の単・複数ケースを組み込んだBILP定式化。IEEE 14-, 30-, 57-, 118バス系統で検証。
- **DOI:** [10.1109/TPWRS.2009.2016596](https://doi.org/10.1109/TPWRS.2009.2016596)
- **BibTeX:** `Abbasy2009`
- **PDF:** [03_Abbasy2009_unified_approach.pdf](pdf/03_Abbasy2009_unified_approach.pdf)

---

### 4. Unified PMU Placement for Observability and Bad Data Detection in State Estimation
- **著者:** Bei Gou, Rajesh G. Kavasseri
- **年:** 2014
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 29, No. 6, pp. 2573–2580
- **概要:** 観測性解析とバッドデータ検出を統合したILP手順を提案。クリティカル計測を非クリティカル化するためのPMU追加位置を決定する。
- **DOI:** [10.1109/TPWRS.2014.2307577](https://doi.org/10.1109/TPWRS.2014.2307577)
- **BibTeX:** `Gou2014`
- **PDF:** [04_Gou2014_observability_bad_data.pdf](pdf/04_Gou2014_observability_bad_data.pdf)

---

### 5. Robust Measurement Design by Placing Synchronized Phasor Measurements on Network Branches
- **著者:** R. Emami, A. Abur
- **年:** 2010
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 25, No. 1, pp. 38–43
- **概要:** 状態推定の堅牢性向上のためのPMU配置。古典的なバッドデータ検出フレームワークをPMUネットワークに拡張。
- **DOI:** [10.1109/TPWRS.2009.2036474](https://doi.org/10.1109/TPWRS.2009.2036474)
- **BibTeX:** `Emami2010`
- **PDF:** [05_Emami2010_robust_measurement.pdf](pdf/05_Emami2010_robust_measurement.pdf)

---

### 6. Optimal PMU Placement in the Presence of Conventional Measurements
- **著者:** Zhaoyang Jin, Yueting Hou, Yue Yu, Lei Ding
- **年:** 2022
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 2022, pp. 1–11
- **概要:** 既存の従来計測を組み込んだBILP手法を提案。IEEE 14-, 118-, 2736バス系統で検証。
- **DOI:** [10.1155/2022/8078010](https://doi.org/10.1155/2022/8078010)
- **BibTeX:** `Jin2022`
- **PDF:** [06_Jin2022_conventional_measurements.pdf](pdf/06_Jin2022_conventional_measurements.pdf)

---

### 7. An Optimal PMU Placement Method for Power System Observability Under Various Contingencies
- **著者:** Ebrahim Abiri, Farzan Rashidi, Taher Niknam
- **年:** 2014
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 25, No. 4, pp. 589–606
- **概要:** N-1事故を考慮したPMU配置。事故インデックスをILP目的関数に組み込む。
- **DOI:** [10.1002/etep.1848](https://doi.org/10.1002/etep.1848)
- **BibTeX:** `Abiri2014`
- **PDF:** [07_Abiri2014_contingencies.pdf](pdf/07_Abiri2014_contingencies.pdf)

---

## カテゴリ3：状態推定への応用

### 8. Optimal PMU Placement for Power System Dynamic State Estimation by Using Empirical Observability Gramian
- **著者:** Junjian Qi, Kai Sun, Wei Kang
- **年:** 2015
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 30, No. 4, pp. 2041–2054
- **概要:** 経験的観測可能性グラミアンを用いて観測度を定量化。WSCC 9バス・NPCC 140バス系統にて無香料カルマンフィルタで検証。
- **DOI:** [10.1109/TPWRS.2014.2356797](https://doi.org/10.1109/TPWRS.2014.2356797)
- **BibTeX:** `Qi2015`
- **PDF:** [08_Qi2015_observability_gramian.pdf](pdf/08_Qi2015_observability_gramian.pdf)

---

### 9. Optimal PMU Placement for Modeling Power Grid Observability with Mathematical Programming Methods
- **著者:** Anas Almunif, Lingling Fan
- **年:** 2019
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 30, No. 2
- **概要:** MILP・NLP定式化の比較。潮流計測・ゼロインジェクションバス・PMU故障シナリオを包括的に検討。
- **DOI:** [10.1002/2050-7038.12182](https://doi.org/10.1002/2050-7038.12182)
- **BibTeX:** `Almunif2019`
- **PDF:** [09_Almunif2019_math_programming.pdf](pdf/09_Almunif2019_math_programming.pdf)

---

## カテゴリ4：グラフ理論アプローチ

### 10. A Graph Theory Based Methodology for Optimal PMUs Placement and Multiarea Power System State Estimation
- **著者:** Ning Xie, Franco Torelli, Ettore Bompard, Alfredo Vaccaro
- **年:** 2015
- **掲載誌:** Electric Power Systems Research, Vol. 119, pp. 25–33
- **概要:** グラフ理論による観測性解析でPMU最適数・配置・最小クリティカル計測集合を決定。多エリア状態推定に対応。
- **DOI:** [10.1016/j.epsr.2014.08.023](https://doi.org/10.1016/j.epsr.2014.08.023)
- **BibTeX:** `Xie2015`
- **PDF:** [10_Xie2015_graph_theory_multiarea.pdf](pdf/10_Xie2015_graph_theory_multiarea.pdf)

---

### 11. Optimal PMU Placement Solution: Graph Theory and MCDM-Based Approach
- **著者:** Pronob K. Ghosh, Soumesh Chatterjee, Biman Kr. Saha Roy
- **年:** 2017
- **掲載誌:** IET Generation, Transmission & Distribution, Vol. 11, No. 13, pp. 3371–3380
- **概要:** ネットワークグラフ理論とAHP（階層分析法）ベースの多基準意思決定法（MCDM）を組み合わせてPMU配置候補をランク付け。
- **DOI:** [10.1049/iet-gtd.2017.0155](https://doi.org/10.1049/iet-gtd.2017.0155)
- **BibTeX:** `Ghosh2017`
- **PDF:** [11_Ghosh2017_graph_mcdm.pdf](pdf/11_Ghosh2017_graph_mcdm.pdf)

---

### 12. Optimal Placement of PMUs for Power System Observability Using Topology Based Formulated Algorithms
- **著者:** B. Mohammadi et al.
- **年:** 2009
- **掲載誌:** Journal of Applied Sciences, Vol. 9, No. 13, pp. 2463–2468
- **概要:** トポロジーベースのグラフアルゴリズムで観測性を判定し最小PMU集合を選定。
- **DOI:** [10.3923/jas.2009.2463.2468](https://doi.org/10.3923/jas.2009.2463.2468)
- **BibTeX:** `Mohammadi2009`
- **PDF:** なし (未取得)

---

## カテゴリ5：サーベイ・レビュー論文

### 13. Taxonomy of PMU Placement Methodologies
- **著者:** Nikolaos M. Manousakis, George N. Korres, Pavlos S. Georgilakis
- **年:** 2012
- **掲載誌:** IEEE Transactions on Power Systems, Vol. 27, No. 2, pp. 1070–1077
- **概要:** PMU配置手法を数理計画法・ヒューリスティック・メタヒューリスティックに分類した最も広く引用されるサーベイ論文。
- **DOI:** [10.1109/TPWRS.2011.2179816](https://doi.org/10.1109/TPWRS.2011.2179816)
- **BibTeX:** `Manousakis2012`
- **PDF:** [13_Manousakis2012_taxonomy.pdf](pdf/13_Manousakis2012_taxonomy.pdf)

---

### 14. A Critical Review of State-of-the-Art Optimal PMU Placement Techniques
- **著者:** Muhammad Musadiq Ahmed, Muhammad Amjad, Muhammad Ali Qureshi, Kashif Imran, Zunaib Maqsood Haider, Muhammad Omer Khan
- **年:** 2022
- **掲載誌:** Energies (MDPI), Vol. 15, No. 6, Article 2125
- **概要:** 数理計画法・メタヒューリスティック・ハイブリッド手法を網羅した2022年の包括的レビュー。テスト系統やソルバー性能の比較表あり。
- **DOI:** [10.3390/en15062125](https://doi.org/10.3390/en15062125)
- **BibTeX:** `Ahmed2022`
- **PDF:** [14_Ahmed2022_critical_review.pdf](pdf/14_Ahmed2022_critical_review.pdf)

---

### 15. A Critical Review of Methods for Optimal Placement of Phasor Measurement Units
- **著者:** Teena Johnson, Tukaram Moger
- **年:** 2020
- **掲載誌:** International Transactions on Electrical Energy Systems, Vol. 31, No. 3
- **概要:** 2003〜2020年のハイブリッド手法論文を調査。収束挙動と解の品質に焦点を当てる。
- **DOI:** [10.1002/2050-7038.12698](https://doi.org/10.1002/2050-7038.12698)
- **BibTeX:** `Johnson2020`
- **PDF:** [15_Johnson2020_critical_review_methods.pdf](pdf/15_Johnson2020_critical_review_methods.pdf)

---

## 一覧表

| # | タイトル（略） | 著者 | 年 | 掲載誌 | DOI | PDF |
|---|---|---|---|---|---|---|
| 1 | Minimal PMU Placement for Observability | Baldwin et al. | 1993 | IEEE Trans. Power Syst. | [10.1109/59.260810](https://doi.org/10.1109/59.260810) | [PDF](pdf/01_Baldwin1993_minimal_pmu_placement.pdf) |
| 2 | Generalized ILP for Optimal PMU Placement | Gou | 2008 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2008.926475](https://doi.org/10.1109/TPWRS.2008.926475) | [PDF](pdf/02_Gou2008_generalized_ilp.pdf) |
| 3 | Unified Approach for Optimal PMU Location | Abbasy, Ismail | 2009 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2009.2016596](https://doi.org/10.1109/TPWRS.2009.2016596) | [PDF](pdf/03_Abbasy2009_unified_approach.pdf) |
| 4 | PMU Placement: Observability + Bad Data | Gou, Kavasseri | 2014 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2014.2307577](https://doi.org/10.1109/TPWRS.2014.2307577) | [PDF](pdf/04_Gou2014_observability_bad_data.pdf) |
| 5 | Robust Measurement Design with PMU | Emami, Abur | 2010 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2009.2036474](https://doi.org/10.1109/TPWRS.2009.2036474) | [PDF](pdf/05_Emami2010_robust_measurement.pdf) |
| 6 | PMU Placement with Conventional Measurements | Jin et al. | 2022 | Int. Trans. Elec. Energy Syst. | [10.1155/2022/8078010](https://doi.org/10.1155/2022/8078010) | [PDF](pdf/06_Jin2022_conventional_measurements.pdf) |
| 7 | PMU Placement Under Contingencies | Abiri et al. | 2014 | Int. Trans. Elec. Energy Syst. | [10.1002/etep.1848](https://doi.org/10.1002/etep.1848) | [PDF](pdf/07_Abiri2014_contingencies.pdf) |
| 8 | PMU Placement via Observability Gramian | Qi, Sun, Kang | 2015 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2014.2356797](https://doi.org/10.1109/TPWRS.2014.2356797) | [PDF](pdf/08_Qi2015_observability_gramian.pdf) |
| 9 | PMU Observability via Math Programming | Almunif, Fan | 2019 | Int. Trans. Elec. Energy Syst. | [10.1002/2050-7038.12182](https://doi.org/10.1002/2050-7038.12182) | [PDF](pdf/09_Almunif2019_math_programming.pdf) |
| 10 | Graph Theory for PMU + Multiarea SE | Xie et al. | 2015 | Elec. Power Syst. Research | [10.1016/j.epsr.2014.08.023](https://doi.org/10.1016/j.epsr.2014.08.023) | [PDF](pdf/10_Xie2015_graph_theory_multiarea.pdf) |
| 11 | Graph Theory + MCDM for PMU Placement | Ghosh et al. | 2017 | IET Gen. Trans. Distrib. | [10.1049/iet-gtd.2017.0155](https://doi.org/10.1049/iet-gtd.2017.0155) | [PDF](pdf/11_Ghosh2017_graph_mcdm.pdf) |
| 12 | Topology-Based PMU Placement Algorithms | Mohammadi et al. | 2009 | J. Applied Sciences | [10.3923/jas.2009.2463.2468](https://doi.org/10.3923/jas.2009.2463.2468) | なし |
| 13 | Taxonomy of PMU Placement Methodologies | Manousakis et al. | 2012 | IEEE Trans. Power Syst. | [10.1109/TPWRS.2011.2179816](https://doi.org/10.1109/TPWRS.2011.2179816) | [PDF](pdf/13_Manousakis2012_taxonomy.pdf) |
| 14 | Critical Review of PMU Placement Techniques | Ahmed et al. | 2022 | Energies (MDPI) | [10.3390/en15062125](https://doi.org/10.3390/en15062125) | [PDF](pdf/14_Ahmed2022_critical_review.pdf) |
| 15 | Critical Review of Methods for PMU Placement | Johnson, Moger | 2020 | Int. Trans. Elec. Energy Syst. | [10.1002/2050-7038.12698](https://doi.org/10.1002/2050-7038.12698) | [PDF](pdf/15_Johnson2020_critical_review_methods.pdf) |

---

## 無関係PDF（old/ に退避済み）

フォルダ内に以下の無関係なPDFが含まれていたため `old/` に退避した。

### Lightning Protection of a Smart Grid Sensor

- **著者:** Celio Fonseca Barbosa, Flavio Eduardo Nallin
- **年:** 2015
- **掲載誌:** Electric Power Systems Research, Vol. 118, pp. 83–88
- **概要:** スマートグリッドセンサーの雷保護手法に関する論文。配電線に設置されるセンサーのRF回路・電圧トランスデューサ・電流トランスデューサに対する雷サージ保護を論じる。PMU配置とは無関係。
- **DOI:** [10.1016/j.epsr.2014.05.017](https://doi.org/10.1016/j.epsr.2014.05.017)
- **ファイル名:** `1-s2.0-S0378779614002053-main.pdf`（および重複 `(1).pdf`）
- **混入経緯（推定）:** 元MDの論文10（Graph Theory + Multiarea SE）のDOIが誤って `10.1016/j.epsr.2014.05.017` と記載されていたため、このDOIに対応する別論文のPDFがダウンロードされたものと推測される。正しいDOIは `10.1016/j.epsr.2014.08.023`（Xie et al.）。

---

## 元MDからの修正履歴

Crossref APIで全DOIを検証した結果、以下の誤りを修正した。

| # | 項目 | 元MDの記載 | 修正後（Crossrefで確認） |
|---|---|---|---|
| 3 | 著者 | S. Chakrabarti, E. Kyriakides | N. H. Abbasy, H. M. Ismail |
| 4 | 著者 | Abur 研究グループ | Bei Gou, Rajesh G. Kavasseri |
| 4 | DOI | `10.1109/TPWRS.2014.2306014`（Crossref上に存在しない） | `10.1109/TPWRS.2014.2307577` |
| 7 | 年 | 2015 | 2014（オンライン公開年） |
| 9 | 年 | 2020 | 2019（オンライン公開年） |
| 10 | 著者 | Scala 研究グループ | Ning Xie, Franco Torelli, Ettore Bompard, Alfredo Vaccaro |
| 10 | DOI | `10.1016/j.epsr.2014.05.017`（別論文: Lightning Protection） | `10.1016/j.epsr.2014.08.023` |
| 10 | Vol/pp | Vol. 116, pp. 134–143 | Vol. 119, pp. 25–33 |
| 15 | 年 | 2021 | 2020（オンライン公開年） |

## PDF取得状況

- **取得済み:** 14本（論文1〜11, 13〜15）
- **未取得:** 1本（論文12: Mohammadi et al. 2009）
- **無関係（退避済み）:** 1本 + 重複2本
