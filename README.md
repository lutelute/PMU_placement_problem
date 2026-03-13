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

## 論文リスト（DOI）

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

> **注意**: PDFは著作権の関係上、本リポジトリには含めていません。各論文はDOIリンクから取得してください。
