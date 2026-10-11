# Robust Visual-Inertial Odometry with Linear Time-Varying Observer-Aided Constraints

First English manuscript draft in the Springer LNCS template.

- Author: **liuhe**
- Affiliation: **Huazhong University of Science and Technology**
- Email: **liuhe2024@hust.edu.cn**
- Main source: [main.tex](main.tex)
- Compiled draft: [output/manuscript.pdf](output/manuscript.pdf)
- Chinese reading version: [output/manuscript_zh.pdf](output/manuscript_zh.pdf)
- Chinese source: [main_zh.tex](main_zh.tex)
- Bibliography: [references.bib](references.bib)

## Structure

1. Introduction, ending with the contribution list.
2. Theoretical preliminaries: frames and bearing geometry, LTV Observer, ESKF/MSCKF.
3. LTV observer-aided ESKF fusion: G/V/L residuals, Jacobians, validity checks, and joint update.
4. Experiments: frozen OFF/G/V/L/GVL configurations on ten EuRoC sequences.
5. Conclusion.

A vector framework sketch is drawn directly in TikZ. Three textual figure placeholders mark the coordinate geometry, trajectory/error curves, and local-window plots. No synthetic trajectories or invented experimental results are inserted.

## Build

Requires Python 3, a LaTeX distribution with pdflatex, bibtex, latexmk, Latin Modern, AMS math, booktabs, TikZ/PGF, xurl, and hyperref.

```bash
make
```

This regenerates six tables from the frozen JSON files, compiles citations and cross-references, and writes output/manuscript.pdf.

For Overleaf, upload this repository and select main.tex as the main document. Generated tables/*.tex are committed, so Python is not required on Overleaf.

### 中文阅读版

中文版本逐段对应英文初稿，保留相同的公式、标签、实验数值和结论，并翻译表头、图注及图占位说明。参考文献保留原始文献题名。英文稿仍是投稿稿件的主版本。

中文编译需要 XeLaTeX、xeCJK 和 Fandol 字体（TeX Live 的 texlive-lang-chinese 提供这些依赖）：

```bash
make chinese
```

在 Overleaf 中选择 main_zh.tex 为主文件，并将编译器设为 XeLaTeX。中文表格可通过 scripts/generate_chinese_tables.py 从英文数值表自动生成。

## Evidence and formula provenance

The draft's experimental tables are generated from the checked-in snapshots in data/. These are archived result summaries, not newly executed VIO experiments.

- Source implementation revision: liuhestu/OPEN-VINS-LTV@5ce89b93c6ed3e37274d57e0900feb2b4e2e3185.
- Final experiment archive: [docs/euroc_final_results.md](https://github.com/liuhestu/OPEN-VINS-LTV/blob/231b9c36035b651ffa1a6346476892e1f5eb1623/docs/euroc_final_results.md), with its adjacent euroc_final_results_data directory.
- G/V formulas: ov_msckf/src/ltv/fusion/UpdaterLTV.cpp and docs/ltv/phase0/frame_and_jacobian_contract.md.
- L prediction, Jacobian, eligibility, and variance budget: ov_msckf/src/ltv/fusion/UpdaterLandmarkApprox.h.
- Main residual stacking and single update: ov_msckf/src/update/UpdaterMSCKF.cpp.
- LTV theory: Wang and Tayebi, arXiv:2407.18099.
- Filter exposition: Sun et al., arXiv:1712.00036, and the OpenVINS paper.

The manuscript uses a world-to-body rotation, with R_true = Exp(-[delta_theta]x) R_hat, matching the implementation's first-order JPL error convention. The landmark measurement uses the prediction captured before the current observer bearing correction; its stored anchor is a historical post-camera snapshot.

## Draft scope

- Fifty accuracy cases and fifty separate serial measurements are described by the archive.
- Native SLAM landmarks are disabled (max_slam: 0).
- MH_04 was excluded after a previous baseline divergence; it is not counted as a successful evaluated sequence.
- Scene/mode weights differ and the evaluated sequences participated in tuning. This is a frozen tuned-configuration comparison.
- The draft reports the recorded local error increases and measured overhead.
- V1_01 attitude-dependent RPE remains descriptive because the corrected GT orientation provenance is unverified.
- Independent dataset validation and the pending trajectory figures are not presented as completed.

Before submission, review the contribution wording, expand related work for the intended venue, add real trajectory figures, confirm author/affiliation formatting, and supply the exact performance-host hardware details.

## Template cleanup

Only the required, unmodified llncs.cls and splncs04.bst support files are retained. The original sample manuscript/PDF, example EPS, package documentation, description sample, and template history/readme are removed.
