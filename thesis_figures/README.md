# Thesis Figures — Master Registry

Single source of truth for every figure and table in the thesis. Each entry links: chapter section, claim, data source, the notebook that produces it, and the output file. The thesis `.tex` should `\includegraphics` from `output/pdf/` exclusively.

## Quickstart

```bash
# 1. Install deps (Python ≥ 3.10 recommended)
pip install pandas numpy matplotlib scipy pyyaml jupyter pytrec_eval gdown

# 2. Fetch any missing data (only large files; small CSVs are committed)
jupyter execute notebooks/00_pull_drive_data.ipynb

# 3. Compute per-query metrics from TREC runs
jupyter execute notebooks/01_compute_per_query.ipynb

# 4. Produce all figures
for nb in 02_baseline_figures 03_model_comparison 04_csqe_figures 05_error_analysis; do
  jupyter execute notebooks/$nb.ipynb
done

# 5. Compile TikZ system diagrams (Ch 3 flowcharts)
cd system_diagrams && for f in fig_3_*.tex; do xelatex "$f"; done
mv fig_3_*.pdf ../output/pdf/

# 6. Excalidraw diagrams (Ch 2 conceptual + a few Ch 3) — manual step
#    See system_diagrams/*.spec.md for instructions
```

## Folder layout

```
thesis_figures/
├── data_manifest.yaml      # Drive IDs + local paths for every input file
├── data/
│   ├── raw/                # pulled from Drive / copied from local repo
│   └── computed/           # derivatives (per-query NDCG, query lengths)
├── notebooks/
│   ├── _helpers.py         # shared style + savefig + TREC loaders
│   ├── 00_pull_drive_data.ipynb
│   ├── 01_compute_per_query.ipynb
│   ├── 02_baseline_figures.ipynb       # Figs 4.1-4.4 + Table 4.1
│   ├── 03_model_comparison.ipynb       # Figs 4.5-4.8 + Tables 4.2, 4.3
│   ├── 04_csqe_figures.ipynb           # Figs 4.9-4.11 + Tables 4.4, 4.5, 4.7
│   └── 05_error_analysis.ipynb         # Figs 4.12-4.15
├── system_diagrams/
│   ├── README.md           # workflow + tool mapping
│   ├── fig_2_1_rag_arch.excalidraw     # template
│   ├── fig_2_2_qe_taxonomy.spec.md
│   ├── fig_2_3_dense_vs_sparse.spec.md
│   ├── fig_3_1_pipeline.tex            # ready-to-compile TikZ
│   ├── fig_3_2_miracl.spec.md
│   ├── fig_3_3_bm25s.tex
│   ├── fig_3_4_mdpr.tex
│   ├── fig_3_5_query2doc.spec.md
│   ├── fig_3_6_repetition.tex
│   ├── fig_3_7_hybrid.tex
│   ├── fig_3_8_csqe.tex
│   └── fig_3_9_best_system.tex
├── styles/thesis_style.mplstyle        # locked matplotlib rcParams
└── output/
    ├── pdf/                # vector — what the thesis \includegraphics{}-es
    └── png/                # for review / Word fallback
```

## Naming convention

- Figures: `fig_<chap>_<num>_<slug>.pdf` (e.g., `fig_4_11_progression.pdf`)
- Plot variations: append `_v1`, `_v2`, `_alt`. Recommended variation ends with no suffix or `_v1` (and is marked ★ in the registry below).
- Tables: produced as LaTeX snippets in `output/pdf/table_<chap>_<num>.tex`. Do **not** export tables as images — `\input{}` them.

## Variations policy

Several data figures have 2–3 plot variations. **All variations are rendered** so Mohammed and Osman can pick after seeing them. Our recommendation is marked with ★ in the **Rec.** column. After picking a winner, delete losers from `output/` (or just don't reference them in the thesis).

---

## Figure Registry

### Chapter 2 — Literature Review & Background

All system diagrams are now **TikZ standalones**. PDFs already compiled and in `output/pdf/`.

| ID | Title | Type | Source / Notebook | Output | Rec. | Status |
|----|-------|------|-------------------|--------|------|--------|
| Fig 2.1 | RAG system architecture | TikZ | `system_diagrams/fig_2_1_rag_arch.tex` | `fig_2_1_rag_arch.pdf` | only | ✅ rendered |
| Fig 2.2 | Query Enhancement taxonomy | TikZ | `system_diagrams/fig_2_2_qe_taxonomy.tex` | `fig_2_2_qe_taxonomy.pdf` | only | ✅ rendered |
| Fig 2.3 | Dense vs Sparse retrieval | TikZ | `system_diagrams/fig_2_3_dense_vs_sparse.tex` | `fig_2_3_dense_vs_sparse.pdf` | only | ✅ rendered |
| Table 2.1 | Reviewed QE papers | LaTeX | hand-compile from `papers/` | `table_2_1.tex` | only | ⏳ TODO |
| Table 2.2 | LLM models used | LaTeX | hand-compile from `research_decisions/llm_model_research.md` | `table_2_2.tex` | only | ⏳ TODO |

### Chapter 3 — Methodology

| ID | Title | Type | Source / Notebook | Output | Rec. | Status |
|----|-------|------|-------------------|--------|------|--------|
| Fig 3.1 | End-to-end pipeline | TikZ | `system_diagrams/fig_3_1_pipeline.tex` | `fig_3_1_pipeline.pdf` | only | ✅ rendered |
| Fig 3.2 | MIRACL dataset structure | TikZ | `system_diagrams/fig_3_2_miracl.tex` | `fig_3_2_miracl.pdf` | only | ✅ rendered |
| Fig 3.3 | BM25S indexing flow | TikZ | `system_diagrams/fig_3_3_bm25s.tex` | `fig_3_3_bm25s.pdf` | only | ✅ rendered |
| Fig 3.4 | mDPR encoding flow | TikZ | `system_diagrams/fig_3_4_mdpr.tex` | `fig_3_4_mdpr.pdf` | only | ✅ rendered |
| Fig 3.5 | Query2Doc generation | TikZ | `system_diagrams/fig_3_5_query2doc.tex` | `fig_3_5_query2doc.pdf` | only | ✅ rendered |
| Fig 3.6 | BM25 query repetition | TikZ | `system_diagrams/fig_3_6_repetition.tex` | `fig_3_6_repetition.pdf` | only | ✅ rendered |
| Fig 3.7 | Hybrid fusion (CC + RRF) | TikZ | `system_diagrams/fig_3_7_hybrid.tex` | `fig_3_7_hybrid.pdf` | only | ✅ rendered |
| Fig 3.8 | CSQE pipeline | TikZ | `system_diagrams/fig_3_8_csqe.tex` | `fig_3_8_csqe.pdf` | only | ✅ rendered |
| Fig 3.9 | Best system (BM25-only-expanded) | TikZ | `system_diagrams/fig_3_9_best_system.tex` | `fig_3_9_best_system.pdf` | only | ✅ rendered |
| Table 3.1 | Per-model hardware config | LaTeX | hand-compile from individual exp docs | `table_3_1.tex` | only | ⏳ TODO |
| Table 3.2 | Per-model generation hyperparams | LaTeX | hand-compile from individual exp docs | `table_3_2.tex` | only | ⏳ TODO |

### Chapter 4 — Results & Discussion

#### 4.1 Baselines

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Table 4.1 | mDPR vs BM25 | 02 | `table_4_1.tex` | only | |
| Fig 4.1 v1 | NDCG histograms overlaid | 02 | `fig_4_1_ndcg_hist_v1.pdf` | ★ | Reader sees the bimodality directly. |
| Fig 4.1 v2 | NDCG CDF overlaid | 02 | `fig_4_1_ndcg_cdf_v2.pdf` | | Better for citing the 39% number, but harder to skim. |

#### 4.2 Error Analysis

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Fig 4.2 v1 | Failure cliff (CDF + annotation) | 02 | `fig_4_2_failure_cliff_v1.pdf` | ★ | The 39% number is annotated on the chart. |
| Fig 4.2 v2 | Failure rate per NDCG bucket | 02 | `fig_4_2_failure_buckets_v2.pdf` | | Less story, more inventory. |
| Fig 4.3 v1 | NDCG by length — boxplot | 02 | `fig_4_3_length_box_v1.pdf` | ★ | Standard, examiner-friendly. |
| Fig 4.3 v2 | NDCG by length — violin | 02 | `fig_4_3_length_violin_v2.pdf` | | Shows density shape; busier. |
| Fig 4.3 v3 | Scatter with binned mean line | 02 | `fig_4_3_length_scatter_v3.pdf` | | Most accurate but noisy at low N. |
| Fig 4.4 | Recall@k curve | 02 | `fig_4_4_recall_curve.pdf` | only | Log-x. |

#### 4.3 Model Comparison — Dense

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Table 4.2 | 10 models Dense metrics | 03 | `table_4_2.tex` | only | |
| Fig 4.5 v1 | Vertical sorted bar | 03 | `fig_4_5_models_bar_v1.pdf` | ★ | Best at thesis text width. |
| Fig 4.5 v2 | Horizontal sorted bar | 03 | `fig_4_5_models_bar_v2_h.pdf` | | Use if model names overflow. |
| Fig 4.5 v3 | Grouped bar across metrics | 03 | `fig_4_5_models_grouped_v3.pdf` | | Useful but dense; consider only if reviewer asks. |
| Fig 4.6 v1 | Size vs Δ NDCG scatter | 03 | `fig_4_6_size_v1.pdf` | | Clean but no story without labels. |
| Fig 4.6 v2 | Same with labels + trendline | 03 | `fig_4_6_size_v2_labelled.pdf` | ★ | Labels make the size→quality correlation legible. |

#### 4.4 Model Comparison — BM25 + Repetition

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Table 4.3 | BM25 best configs per model | 03 | `table_4_3.tex` | only | |
| Fig 4.7 v1 | n-sweep multi-line | 03 | `fig_4_7_repetition_v1.pdf` | ★ | The "repetition heals BM25" story is clearest here. |
| Fig 4.7 v2 | n-sweep + β markers | 03 | `fig_4_7_repetition_v2.pdf` | | Includes β configs but the x-axis is awkward. |
| Fig 4.7 v3 | Heatmap (model × config) | 03 | `fig_4_7_repetition_v3_heat.pdf` | | Best for browsing all values at once. |
| Fig 4.8 v1 | Dense Δ vs BM25 Δ scatter | 03 | `fig_4_8_gains_v1.pdf` | ★ | Shows that only Aya/Jais-2 improve both. |
| Fig 4.8 v2 | Slope chart | 03 | `fig_4_8_gains_v2_slope.pdf` | | Same message, different angle. |

#### 4.5 Hybrid (no QE)

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Table 4.4 | BM25 / mDPR / Hybrid CC / RRF | 04 | `table_4_4.tex` | only | |
| Fig 4.9 v1 | α-sweep — NDCG only | 04 | `fig_4_9_alpha_sweep_v1.pdf` | ★ | Single-metric focus. |
| Fig 4.9 v2 | α-sweep — all 4 metrics | 04 | `fig_4_9_alpha_sweep_v2_all.pdf` | | Use if reviewer wants full picture. |

#### 4.6 CSQE

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Table 4.5 | CSQE corpus / blind / 2+2 ablation | 04 | `table_4_5.tex` | only | |
| Fig 4.10 v1 | α sweep | 04 | `fig_4_10_csqe_alpha_v1.pdf` | | **Recommend NOT including** — flat curve. Fold into one prose sentence: "varying α from 1 to 4 changed NDCG@10 by less than 0.002, so we fix α=4." |
| Table 4.6 | CSQE vs blind QE (Aya) | hand-compile | `table_4_6.tex` | only | TODO; numbers in `exp_013_csqe_aya_8b.md`. |

#### 4.7 Best System (CSQE + Hybrid)

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Table 4.7 | Configs A/B/C all metrics | 04 | `table_4_7.tex` | only | |
| Fig 4.11 v1 | Plain progression bar | 04 | `fig_4_11_progression_v1.pdf` | | Cleanest. |
| Fig 4.11 v2 | Bar with Δ annotations | 04 | `fig_4_11_progression_v2_annot.pdf` | ★ | The Δ annotations make this the strongest headline. |
| Fig 4.11 v3 | Grouped bar across metrics | 04 | `fig_4_11_progression_v3_grouped.pdf` | | Use only if a single headline doesn't suit. Labels use BM25-only-expanded (post-D3). |

#### 4.8 Error Analysis of CSQE

| ID | Title | Notebook | Output | Rec. | Notes |
|----|-------|----------|--------|------|-------|
| Fig 4.12 v1 | Per-query Δ histogram | 05 | `fig_4_12_delta_hist_v1.pdf` | ★ | **Unblocked 2026-05-31** — `csqe_vs_blind_per_query.csv` validated; every aggregate reproduces. |
| Fig 4.12 v2 | KDE with mean line | 05 | `fig_4_12_delta_kde_v2.pdf` | | Smoother, but harder to read counts. |
| Fig 4.13 v1 | 1st-pass relevant — plain bar | 05 | `fig_4_13_firstpass_v1.pdf` | | |
| Fig 4.13 v2 | Same with sample sizes annotated | 05 | `fig_4_13_firstpass_v2_annot.pdf` | ★ | Sample sizes are crucial — relevant=1061 vs not=1835. |
| Fig 4.14 v1 | Δ gain by length — single bar | 05 | `fig_4_14_lengthgain_v1.pdf` | | |
| Fig 4.14 v2 | Grouped blind vs CSQE per bin | 05 | `fig_4_14_lengthgain_v2_grouped.pdf` | ★ | Shows both absolute values and the gap. |
| Fig 4.15 v1 | Regression types stacked bar | 05 | `fig_4_15_regtype_v1.pdf` | | |
| Fig 4.15 v2 | Donut chart | 05 | `fig_4_15_regtype_v2_donut.pdf` | ★ | Pie/donut is conventional for type breakdowns. |

---

## Status legend
- ⏳ Pending — no source produced yet
- 🟡 Skeleton ready — structure exists, needs polish
- ✅ Ready — source produced, run notebook / xelatex to render
- ❌ Cut — decided against inclusion

## Notes for the thesis
- Tables produced as LaTeX snippets (`booktabs`-friendly) and `\input{}` from the thesis. Do not export tables as images.
- Captions go in the thesis `.tex`, **not** inside the figure (Dr. Tahani's rule).
- Capital "F"/"T" in text references: "As shown in Figure 4.11", "Table 4.7 presents…"
- After picking variation winners, you can drop the losers from `output/` — the registry above tracks which ones the thesis references.
- The notebook scripts are deterministic: re-running produces identical PDF bytes (no random seeds involved). Safe to regenerate before submission.

## Visual feedback (Mohammed, 2026-05-31)

First-look review of `REVIEW.html` flagged that the current renders feel **too utilitarian**:
- **Black-and-white grayscale palette is too plain** — needs color (or at least a more deliberate accent).
- **TikZ system diagrams feel basic** — boxes-and-arrows reads as a generated artefact rather than a designed figure. Likely want helper icons, illustrative imagery, or richer visual metaphors.
- **Open question:** consider AI image generators for the conceptual diagrams (Ch 2 RAG architecture, QE taxonomy, Dense vs Sparse) — they're conceptual, not data-driven, so a stylised illustration might communicate better than mechanical TikZ.

This is not blocking the commit. Current renders are mathematically correct and submission-eligible if needed in a pinch. Visual upgrade is a separate iteration.

### Direction for the next figure-polish pass (not started)
1. Pick an accent color (one), add to `styles/thesis_style.mplstyle`. Suggest a single muted color (avoid bright primaries — keep examiner-friendly).
2. Decide which Ch 2/3 diagrams to upgrade visually. Candidates ranked by visual return:
   - Fig 2.1 RAG architecture — strongest candidate for icon-based redesign.
   - Fig 3.5 Query2Doc generation — natural fit for a stylised illustration of prompt → LLM → pseudo-doc.
   - Fig 3.8 CSQE pipeline — would benefit from icons distinguishing the 3 stages.
3. Evaluate AI image generators (DALL-E, SDXL) for the highest-conceptual diagrams (2.1, 2.2, 2.3). For methodology diagrams (3.3, 3.4, 3.6, 3.7), keep TikZ — they need precision over aesthetic.
4. Data figures (4.1–4.15): smaller upgrade — accent color on the primary data series + secondary tone for comparisons. Don't overhaul; just enrich the existing palette.

## Outstanding work (updated 2026-05-31)

### Done since the snapshot
- ✅ All 12 system diagrams rendered as TikZ PDFs in `output/pdf/` (Excalidraw track abandoned in favour of TikZ).
- ✅ Per-query CSQE-vs-blind data committed (`data/raw/csqe_vs_blind_per_query.csv`) — Fig 4.12 unblocked.
- ✅ Length-bin scheme locked: **Scheme A (Short 1–3 / Medium 4–8 / Long 9+ words)**. Applied in `_helpers.py`, notebook 02 (Fig 4.3) and notebook 05 (Fig 4.14).
- ✅ Config A/B/C → BM25-only-expanded / Dense-only-expanded / Both-expanded renaming applied in notebook 04.
- ✅ Numeric rounding to 3 decimals applied in Tables 4.1, 4.4, 4.5, 4.7.
- ✅ Notebook 02 switched from buggy `baseline_dense_per_query.json` to canonical `data/computed/baseline_dense_per_query_with_length.csv` — Fig 4.2 failure rate auto-corrects to ~34%.

### Done this session (also)
- ✅ All 5 data-figure notebooks executed; 32 PNG + 32 PDF variations in `output/`.
- ✅ Numbers verified against canonical post-WS1 data (34% failure, 0.499 mDPR, Scheme-A bucket means 0.345/0.511/0.476).
- ✅ `REVIEW.html` produced for joint Mohammed+Osman review with all 44 figures grouped and rated.
- ✅ `PROGRESS_SNAPSHOT.html` produced (status dashboard).

### Remaining
1. **Visual upgrade** of the figures (see "Visual feedback" section above) — not blocking submission but desired for polish.
2. **Hand-compile**: `model_comparison_dense.csv` — fill the blank `recall_10`, `recall_100`, `mrr` columns from Osman's experiment docs (currently only `ndcg_10` is populated for his 5 models).
3. **Hand-compile**: Table 4.6 — CSQE vs blind QE on BM25 and Dense (numbers in `exp_013_csqe_aya_8b.md`).
4. **Hand-compile**: Tables 2.1, 2.2, 3.1, 3.2 — pure literature/metadata, no plots.
5. **Thesis text edits** for Workstream 1 outcomes — see `research_decisions/STREAM_1_COMPLETION_REPORT.md` section 3. **Track A in `THESIS_NEXT_STEPS_TASKS.md` Progress Log — not started yet.**
