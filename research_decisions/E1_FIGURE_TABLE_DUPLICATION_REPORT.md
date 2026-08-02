# E1 — Figure ↔ Table Duplication Analysis

**Task:** E1 (Phase E), `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`
**Owner:** Osman · **Run:** 2026-07-30 · **Status:** analysis only — no `.tex`, figure, or notebook was modified.
**Feeds:** D2 (appendix analysis), D5 (conciseness pass), E2 (figure regeneration), E3 (dead labels / Ch.4 table audit).

**Sources of truth used:** compiled `1-main.pdf` (122 pp, 2026-07-29 build), `1-main.lof` / `1-main.lot` / `1-main.toc`, `Chapters/chapter1–5.tex`, `thesis_figures/` (notebooks, `output/pdf/`, `system_diagrams/`, `data/`).

---

## 0. Headline findings

1. **The premise from the meeting is half right — and the wrong half matters.** Figure 4.1 is *not* a re-plot of Table 4.1: it is a genuine per-query distribution over 2,896 queries and Table 4.1 holds three rows of aggregate metrics. The duplication the team correctly sensed is real but lives **one section later**: **Figure 4.5 is a bar chart of Table 4.8's NDCG@10 column, printed on the same page directly beneath it** (p. 66), and **Figure 4.6 re-plots three more columns of the same table** on p. 67. Those are the textbook cases.
2. **6 of 15 Chapter 4 figures are pure re-plots** of an adjacent table and can be dropped with no information loss: **4.2, 4.5, 4.6, 4.13, 4.14, 4.15**.
3. **Chapters 2–3 are clean.** All 8 diagrams there (Fig 2.1, 3.1–3.7) are ORIGINAL system diagrams — zero duplication suspects, as expected.
4. **Page savings: ~3.2 pages** from high-confidence actions, **~4.5 pages** if the medium-confidence appendix moves are also taken.
5. **Context that changes the urgency:** the core manuscript (Ch. 1–5) is **pages 1–97 = 97 pages** (Bibliography starts p. 98). **We are already under the 100-page limit.** These cuts buy margin and answer the supervisor's tables-vs-figures directive; they are not rescuing a violation. *(This is a direct input to D1 — the number D1 is asked to compute is 97.)*
6. **Two live defects found in figures currently in the thesis** (details in §5): Figure 4.9's axis labels are mojibake (`Î"` instead of `Δ`) in the compiled PDF, and Figures 4.5/4.6 contain an `Aya 8B CSQE` bar that does not belong in a Query2Doc chart and is absent from the table they accompany.

---

## 1. Inventory

**Totals:** 23 numbered figures, 34 numbered tables. Chapters 1 and 5 contain **zero** floats.

*Size column = estimated fraction of the text block (452.97 × 700.51 pt), computed from each graphic's true aspect ratio × its `width=` fraction, plus caption lines. Verified against the compiled PDF for pp. 66–67 and 75 (estimates were accurate to a few percent).*

### 1.1 Figures

| Fig | Page | Caption (short) | Source file | Notebook / origin | Shows | Size |
|---|---|---|---|---|---|---|
| 2.1 | 9 | RAG system architecture | `fig_2_1_rag_arch.pdf` | TikZ `system_diagrams/` | Query → retriever → corpus → LLM flow | 27% |
| 3.1 | 36 | Experimental pipeline overview | `fig_3_1_pipeline.pdf` | TikZ | QE layer + BM25S/mDPR + fusion + eval | 35% |
| 3.2 | 37 | mDPR encoding flow | `fig_3_4_mdpr.pdf` | TikZ | Batch encode → 768-d → FAISS | **62%** |
| 3.3 | 38 | BM25S indexing flow | `fig_3_3_bm25s.pdf` | TikZ | Tokenise → stopwords → BM25S index | 21% |
| 3.4 | 42 | Query2Doc generation | `fig_3_5_query2doc.pdf` | TikZ | Prompt → pseudo-doc → concat | 55% |
| 3.5 | 51 | Hybrid fusion: CC and RRF | `fig_3_7_hybrid.pdf` | TikZ | Two fusion formulas side by side | 37% |
| 3.6 | 52 | CSQE pipeline | `fig_3_8_csqe_aigen_v4_boosted.png` | **AI-generated raster** (PaperBanana) | 3-stage CSQE flow | 45%\* |
| 3.7 | 55 | Best system architecture | `fig_3_9_best_system.pdf` | TikZ | Asymmetric BM25/mDPR + RRF | 22% |
| 4.1 | 59 | Per-query NDCG@10 distribution | `fig_4_1_ndcg_hist_v1.pdf` | `02_baseline_figures` | 20-bin histogram, both retrievers, 2,896 queries | 49% |
| 4.2 | 60 | Failure cliff on baseline NDCG@10 | `fig_4_2_failure_cliff_v1.pdf` | `02_baseline_figures` | CDF of mDPR per-query nDCG, annotated 33.9% | 46% |
| 4.3 | 61 | NDCG@10 by query length | `fig_4_3_length_box_v1.pdf` | `02_baseline_figures` | Box plot, 3 length buckets | 47% |
| 4.4 | 62 | Recall@k curve | `fig_4_4_recall_curve.pdf` | `02_baseline_figures` | Mean Recall@k, k=1–100, log x | 46% |
| 4.5 | 66 | Dense NDCG@10 across models | `fig_4_5_models_bar_v1.pdf` | `03_model_comparison` | 10 bars + baseline line | 51% |
| 4.6 | 67 | Dense grouped multi-metric | `fig_4_5_models_grouped_v3.pdf` | `03_model_comparison` | 10 models × 3 metrics | 43% |
| 4.7 | 69 | Model size vs Query2Doc gain | `fig_4_6_size_v2_labelled.pdf` | `03_model_comparison` | Scatter + linear fit (slope 0.0131) | 48% |
| 4.8 | 74 | BM25 repetition sweep, 9 models | `fig_4_7_repetition_v1.pdf` | `03_model_comparison` | 9 curves over n∈{1,3,5,7,10} | 51% |
| 4.9 | 75 | Dense vs BM25 gain per model | `fig_4_8_gains_v1.pdf` | `03_model_comparison` | Quadrant scatter of Δ pairs | 44% |
| 4.10 | 77 | Hybrid CC α sweep, all metrics | `fig_4_9_alpha_sweep_v2_all.pdf` | `04_csqe_figures` | 4 metric curves over α=0.1–0.9 | **53%** |
| 4.11 | 81 | System progression | `fig_4_11_progression_v2_annot.pdf` | `04_csqe_figures` | 6 annotated bars, baseline → 0.714 | 51% |
| 4.12 | 84 | Per-query Δ NDCG@10 histogram | `fig_4_12_delta_hist_v1.pdf` | `05_error_analysis` | 2,896 deltas, shaded win/regress bands | 52% |
| 4.13 | 85 | NDCG@10 by first-pass relevance | `fig_4_13_firstpass_v2_annot.pdf` | `05_error_analysis` | 2 groups × 2 systems | 48% |
| 4.14 | 86 | Per-bucket comparison by length | `fig_4_14_lengthgain_v2_grouped.pdf` | `05_error_analysis` | 3 buckets × 2 systems | 48% |
| 4.15 | 88 | Regression type breakdown | `fig_4_15_regtype_v2_donut.pdf` | `05_error_analysis` | 3-slice donut | 50% |

\* Fig 3.6's file is a **JPEG with a `.png` extension** (2752×1536) — see §5.3.

**Also present, not counted:** a dead `figure` environment (`fig:regression_pie_old`) wrapped in `\iffalse` at `chapter4.tex:922-933`, and the university logo on the title page (bare `\includegraphics`, no float). Together these reconcile the "24 figures" from the C7 audit with the 23 in the List of Figures.

### 1.2 Tables

| Tab | Page | Caption (short) | Data | Rows | Size |
|---|---|---|---|---|---|
| 2.1 | 12 | QE papers reviewed | `table_2_1_papers.csv` (13) | 13 | ~45% |
| 2.2 | 18 | Arabic datasets surveyed | inline | 6 | ~25% |
| 2.3 | 19 | Open-source LLMs evaluated | `table_2_2_models.csv` (10) | 10 | ~30% |
| 2.4 | 26 | Summary of language models | inline | 10 (+2 group rows) | ~35% |
| 3.1 | 43 | Q2D generation parameters | inline | 5 | ~20% |
| 3.2 | 46 | Model configs for comparison | inline | ~10 | ~30% |
| 4.1 | 57 | Baseline retrieval results | inline | 3 | ~22% |
| 4.2 | 59 | Performance segmentation | inline | 3 | ~17% |
| 4.3 | 60 | Performance by query length | inline | 3 | ~17% |
| 4.4 | 62 | Coverage at retrieval depth | inline | 4 | ~18% |
| 4.5 | 63 | Query2Doc, dense | inline | 4 | ~19% |
| 4.6 | 64 | Query2Doc, BM25 | inline | 4 | ~19% |
| 4.7 | 65 | Q2D vs original paper | inline | 6 | ~26% |
| 4.8 | 66 | Dense leaderboard | `model_comparison_dense.csv` | 11 | ~28% |
| 4.9 | 67 | BM25 leaderboard | `model_comparison_bm25.csv` | 10 | ~27% |
| 4.10 | 70 | Qwen generational comparison | inline | 2 | ~15% |
| 4.11 | 71 | Models improving by retriever | inline | 5 | ~21% |
| 4.12 | 73 | BM25 repetition, full 9×8 grid | `exp11_ndcg10.csv` | 10 | **~40%** |
| 4.13 | 73 | BM25 metrics at best config | `exp11_*.csv` | 9 | ~30% |
| 4.14 | 76 | Hybrid fusion results | `exp12_cc_sweep.csv` | 13 | **~40%** |
| 4.15 | 78 | CSQE main results | `exp21_summary.csv` | 5 | ~24% |
| 4.16 | 78 | CSQE component ablation | `csqe_ablation_table.csv` | 4 | ~22% |
| 4.17 | 79 | α sweep, CSQE BM25 | `csqe_alpha_ablation.csv` | 4 | ~17% |
| 4.18 | 80 | CSQE fusion strategies | `exp21_all_metrics.json` | 7 | ~33% |
| 4.19 | 80 | BM25-expanded RRF ablation | inline | 3 | ~17% |
| 4.20 | 81 | α sweep, best system | `csqe_alpha_ablation.csv` | 4 | ~19% |
| 4.21 | 82 | Δ vs prior systems | inline | 7 | ~25% |
| 4.22 | 82 | System progression | `exp21_summary.csv` | 7 | ~30% |
| 4.23 | 83 | Win/loss distribution | `csqe_vs_blind_per_query.csv` | 4 | ~33%† |
| 4.24 | 84 | Split by first-pass quality | `csqe_error_patterns.csv` | 3 | ~22% |
| 4.25 | 85 | Split by query length | `sec4_10_length_buckets*.csv` | 3 | ~22% |
| 4.26 | 87 | Big-win query examples | inline (Arabic) | 3 | **~38%** |
| 4.27 | 87 | Regression classification | `csqe_error_patterns.csv` | 3 | ~22% |
| 4.28 | 90 | Summary of all experiments | inline | 17 (+3 group rows) | **~55%** |

† Table 4.23's caption is 4 lines and larger than its 4-row body — flagged for D5.

---

## 2. Classification

| | Count | Figures |
|---|---|---|
| **ORIGINAL** | 12 | 2.1, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.1, 4.7, 4.9, 4.12 |
| **PARTIAL OVERLAP** | 5 | 4.3, 4.4, 4.8, 4.10, 4.11 |
| **DUPLICATE** | 6 | 4.2, 4.5, 4.6, 4.13, 4.14, 4.15 |

---

## 3. Per-pair verdicts

> **Placement note that makes the savings real:** every Chapter 4 figure uses `\begin{figure}[H]` — a hard inline placement, not a float. The figure occupies exactly its own box height in the text stream, so deleting one genuinely reclaims that vertical space and pulls the following text up. Savings below are close to 1:1, not optimistic.

### DUPLICATE — drop the figure

**D-1 · Figure 4.6 ↔ Table 4.8** (fig p. 67, table p. 66)
Fig 4.6 plots NDCG@10, Recall@10 and MRR — three columns of Table 4.8 — for the same ten models in the same order. All three series are monotone and parallel, so even the "shape" carries no argument. It also sits immediately after Fig 4.5, which already plots one of those three series.
→ **DROP the figure.** **Confidence: HIGH.** Saves **~0.43 page**.

**D-2 · Figure 4.15 ↔ Table 4.27** (fig p. 88, table p. 87)
A 3-slice donut for the three numbers 52% / 36% / 12%, occupying half a page. Table 4.27 carries the same percentages *plus* counts *plus* the Description column that actually explains what Types A/B/C are. The figure also has a rendering bug (§5.2).
→ **DROP the figure.** **Confidence: HIGH.** Saves **~0.50 page**.

**D-3 · Figure 4.5 ↔ Table 4.8** (both p. 66)
The canonical case, and the one the supervisor's directive is aimed at: a bar chart of the table's NDCG@10 column, printed directly below the table on the same page. The figure adds a baseline reference line; the table is already sorted by NDCG@10 and carries a ΔNDCG column, so ranking and gain-over-baseline are equally immediate there — while the table also carries Params, Recall@10 and MRR, which the figure drops.
In a defense reading the table wins: it answers "which model, by how much, on which metrics" in one glance; the figure answers only the first two. The figure additionally contains an error (§5.1).
→ **DROP the figure, keep Table 4.8.** **Confidence: HIGH.** Saves **~0.51 page**.

**D-4 · Figure 4.13 ↔ Table 4.24** (fig p. 85, table p. 84)
Four bars reproducing the four cells of a 2×2 table (0.668 / 0.888 / 0.410 / 0.581, n = 1,061 / 1,835). Table 4.24 additionally carries the Δ column and the "All queries" row.
→ **DROP the figure.** **Confidence: HIGH.** Saves **~0.48 page**.

**D-5 · Figure 4.14 ↔ Table 4.25** (fig p. 86, table p. 85)
Six bars reproducing the six cells of Table 4.25 (0.369/0.530, 0.506/0.703, 0.567/0.698). The table additionally carries Δ absolute and Δ relative — and the relative gain (+43.6% for short queries) is the actual claim §4.10.2 makes, which the figure cannot show. Fig 4.14 also repeats Fig 4.3's x-axis 25 pages later.
→ **DROP the figure.** **Confidence: HIGH.** Saves **~0.48 page**.

**D-6 · Figure 4.2 ↔ Table 4.2 (and ↔ Figure 4.1)** (fig p. 60, table p. 59)
Doubly redundant. Its single annotation — "33.9% of queries NDCG@10 < 0.3" — is row 1 of Table 4.2 verbatim, and it is the CDF of exactly the variable Figure 4.1 already histograms one page earlier. Two views of one distribution, plus a table of the same distribution, across two pages.
→ **DROP the figure, keep Fig 4.1 + Table 4.2.** **Confidence: HIGH.** Saves **~0.46 page**.

### PARTIAL OVERLAP — keep both, or trim the table

**P-1 · Figure 4.11 ↔ Table 4.22 + Table 4.21** (fig p. 81, tables p. 82)
Fig 4.11's six bars are Table 4.22's rows minus one, and its delta annotations overlap Table 4.21. But this is the thesis's headline figure — the single image that carries the whole contribution (0.462 → 0.714) and the one a committee will look at first. Meanwhile **Table 4.22 is triply redundant**: every one of its rows also appears in Table 4.28 (Summary of All Experiments, p. 90).
→ **KEEP the figure, DROP Table 4.22.** **Confidence: HIGH.** Saves **~0.30 page**.
→ Regeneration note for E2: add the missing **Best blind BM25 (Aya β=2, 0.5855)** bar so the figure fully covers what Table 4.22 was carrying.

**P-2 · Figure 4.8 ↔ Tables 4.12 + 4.13** (fig p. 74, tables p. 73)
The figure earns its place: the plateau-then-decline shape across nine models, and all nine crossing the BM25 baseline, is the argument of §4.6 and a 9×8 numeric grid conveys it poorly. Keep it.
The redundancy is on the table side. **Table 4.12 is the full 9×8 sweep (~40% of a page)** — reference data, not argument.
→ **KEEP both figure and Table 4.13; MOVE Table 4.12 to an appendix.** **Confidence: MEDIUM-HIGH.** Saves **~0.40 page** of main text. → **hand-off to D2.**
→ Caveat for E2: the figure plots only the `n` columns, so the top-3 models' actual optima (β=2) are **off-chart**; a figure-only reader concludes the optimum is n≈7. Either add the β points or annotate.

**P-3 · Figure 4.10 ↔ Table 4.14** (fig p. 77, table p. 76)
The figure plots all four metrics across the nine CC α values — i.e. the CC block of Table 4.14 — and adds the unimodal peak at α=0.5 and Recall@100's flatness, both of which §4.7 asserts in prose. The table adds the two RRF rows the figure omits.
→ **KEEP the figure; SHRINK Table 4.14** to baselines + best CC + both RRF rows, moving the full nine-point α sweep to an appendix. **Confidence: MEDIUM.** Saves **~0.20 page**. → **hand-off to D2.**

**P-4 · Figure 4.3 ↔ Table 4.3** (fig p. 61, table p. 60)
Same three buckets. The table gives mean + count + %; the box plot gives median + IQR + range. The spread is genuine extra information — but it works *against* the section's claim: the medians (0.30 / 0.51 / 0.47) make the short-query gap look mild, all three buckets span 0→1, and the figure carries no `n`, hiding that "Short" is only 147 of 2,896 queries. The text already states the non-monotonicity and r ≈ −0.01.
→ **DROP the figure, keep Table 4.3.** **Confidence: MEDIUM** — the counter-argument is that this is the only place showing that length explains almost nothing. If kept, it should be replaced by opportunity **G3** below, which makes that point properly. Saves **~0.47 page**.

**P-5 · Figure 4.4 ↔ Table 4.4** (both p. 62)
**These are not the same quantity** — and that is the problem. Table 4.4 reports *coverage* (fraction of queries with ≥1 relevant doc by depth k: 74.6 / 80.8 / 86.9 / 90.1%); Figure 4.4 plots *mean Recall@k*. Adjacent, both about "retrieval depth", easy to conflate — a committee member may read the figure as showing the table's numbers and find they disagree.
→ **KEEP the figure, FOLD Table 4.4 into prose.** All four of its numbers are already quoted in the surrounding text; the table is 4 rows × 2 columns. Also sharpen both captions to name the metric explicitly. **Confidence: MEDIUM.** Saves **~0.19 page**.

### ORIGINAL — keep, no action

| Fig | Why it is not derivable from any table |
|---|---|
| 2.1, 3.1–3.5, 3.7 | System diagrams. Nothing tabular about them. |
| 3.6 | CSQE pipeline diagram — the one figure that explains the thesis's own contribution. Keep (but see §5.3 on the file). |
| **4.1** | Full per-query distribution over 2,896 queries for **both** retrievers. Table 4.1 has 3 rows of aggregates; Table 4.2 has 3 coarse bins for one retriever. The bimodality — a large mass at 0 and another at 1 — is the visual argument for QE and appears in no table. **Keep both; this is the pair the meeting mis-identified.** |
| **4.7** | Scatter + fitted trend (slope 0.0131). The points are derivable by joining Table 4.8's Params and ΔNDCG columns, but the regression line and the visual basis for §4.5.1's deliberately cautious claim exist only here. |
| **4.9** | Quadrant scatter requiring a **join of Tables 4.8 and 4.9**. "Only Aya and Jais-2 are in the both-positive quadrant" is not readable from either table alone. **Keep — but must be regenerated, see §5.1.** |
| **4.12** | 2,896-point delta distribution with the tie spike at Δ=0, the big-win mass and the regression tail. Table 4.23 has 3 counts and a mean. Alongside 4.11, the most valuable figure in the thesis. |

---

## 4. Genuine figure opportunities

Concrete, buildable from data already in `thesis_figures/data/`. **Not created — proposals only.** Ranked by value per unit effort.

**G1 — Per-query win/loss scatter: blind QE vs CSQE+Hybrid** ⭐ *highest value*
Scatter of `ndcg10_aya_blind_bm25` (x) vs `ndcg10_csqe_hybrid` (y), 2,896 points, with the y=x diagonal. Makes visible in one image what §4.10.3 currently *tells* in prose plus three examples in Table 4.26: the dense cluster at (0, 1) — the 1,061 big wins where blind QE hallucinated and corpus grounding rescued the query — and the opposing Type-A cluster at high-x/low-y.
**Source:** `data/raw/csqe_vs_blind_per_query.csv` (2,896 rows, all columns present).
**Note:** Figure 4.12's label is already `fig:csqe_scatter` — a scatter appears to have been the original intent before a histogram was substituted. This would deliver it, and could either complement or replace Fig 4.12.

**G2 — Recall funnel through the pipeline** ⭐ *serves F1 (defense narrative) too*
Funnel/waterfall of Recall@100 by stage: BM25 alone 0.8577 → BM25+CSQE 0.9422 → BM25-expanded RRF 0.9734, annotated "97.3% ceiling for downstream reranking". §4.9 makes this argument in prose only. A funnel is a genuinely different form from any table and directly answers the "it reads as half a RAG" problem flagged in F1.
**Source:** `data/raw/exp21_summary.csv` + `data/raw/exp12_summary.csv`.

**G3 — Query-length distribution of MIRACL Arabic dev**
Histogram of `word_count` over 2,896 queries with the 1–3 / 4–8 / 9+ boundaries marked. Shows that 86.2% of queries fall in a single bucket — which is why every bucketed result in the thesis is dominated by the medium band, currently only implied by an `n` column. **Would properly replace Fig 4.3** (see P-4).
**Source:** `data/computed/query_lengths.csv`.

**G4 — Failure decomposition (no dataset ceiling)**
Small stacked bar: 258 failures → 199 "missed by all methods, relevant doc present in corpus" + 58 "retrievable by BM25 alone, lost by CSQE", over a 100%-corpus-presence band. §4.10.1 argues this in one dense paragraph; the "there is no indexing gap or dataset ceiling" claim is a strong defensive point that deserves to be instantly legible. Could take Fig 4.15's vacated slot.
**Source:** `data/computed/task_1_1_failure_corpus_check.csv` (258 rows, `verdict` column ready).

**G5 — Repetition sweep including the β configurations** *(a fix, not an addition)*
Redo Fig 4.8 with the MuGI β=2/4/6 points on-chart so the actual optima are visible. Resolves the P-2 caveat.
**Source:** `data/raw/exp11_ndcg10.csv` — already contains all eight columns.

**G6 — Rank-displacement plot for the 367 regressions** *(optional, higher effort)*
For regression queries, where did the previously-retrieved relevant document move to? Would make the Type-A/Type-B mechanism visible rather than asserted.
**Source:** TREC run files `bm25_csqe_run.txt` + `hybrid_csqe_rrf_k20.txt` — **on Drive, gitignored locally** (`data_manifest.yaml`); requires running `00_pull_drive_data.ipynb` first. Flagged as optional for that reason.

---

## 5. Defects found (hand-off to E2 / E3)

**5.1 · Figure 4.9 axis labels are mojibake — live in the compiled PDF.**
Both axes read `Î" NDCG@10 …` instead of `Δ NDCG@10 …` (verified on p. 75 of `1-main.pdf`). The notebook source is **correct** — `03_model_comparison.ipynb` cell 14 holds a proper U+0394 — so the committed render was produced from a mis-encoded run. Figure 4.12 (notebook 05) renders `Δ` correctly, which confirms the font is fine and this is specific to the notebook-03 run. **Re-running `03_model_comparison.ipynb` should fix it.** This also affects `fig_4_8_gains_v2_slope.pdf`.

**5.2 · Figure 4.15's percentage labels are clipped** by the donut ring — "12%" renders as "%". Moot if D-2 is accepted.

**5.3 · Figures 4.5 and 4.6 contain an `Aya 8B CSQE` bar** (0.5915) that is **absent from Table 4.8** and does not belong in a chart captioned "on the Query2Doc pipeline". Both figures also **omit ALLaM-7B**, which the table includes. Moot if D-1/D-3 are accepted; otherwise must be fixed.

**5.4 · Figure 3.6's file is a JPEG with a `.png` extension** (`fig_3_8_csqe_aigen_v4_boosted.png`, 2752×1536), and it is an **AI-generated raster** in an otherwise all-vector thesis. A TikZ version exists (`system_diagrams/fig_3_8_csqe.tex` → `.pdf`). Worth a deliberate decision rather than an accident — the CSQE diagram is the thesis's own contribution and a hand-drawn TikZ version is more defensible under questioning. **Team/supervisor decision.**

**5.5 · Dead figure environment** `fig:regression_pie_old` inside `\iffalse` at `chapter4.tex:922-933` — delete during E3.

**5.6 · Bonus, table↔table duplication** (outside E1's remit, but found en route — hand to D2/D5):
- **Table 2.3 (p. 19) ↔ Table 2.4 (p. 26)** — both list the same 10 models with overlapping columns (params, Arabic focus, multilingual), 7 pages apart in the same chapter. One should go.
- **Table 4.22 ↔ Table 4.28** — every row of 4.22 recurs in 4.28. Already covered by P-1.
- **Table 4.1's hybrid row ↔ Table 4.14** — deliberate forward reference, correctly cross-referenced. No action.

---

## 6. Page-savings summary

### High confidence — apply in D5

| Action | Item | Saving |
|---|---|---|
| Drop figure | Fig 4.5 (↔ Table 4.8) | 0.51 |
| Drop figure | Fig 4.15 (↔ Table 4.27) | 0.50 |
| Drop figure | Fig 4.14 (↔ Table 4.25) | 0.48 |
| Drop figure | Fig 4.13 (↔ Table 4.24) | 0.48 |
| Drop figure | Fig 4.2 (↔ Table 4.2 + Fig 4.1) | 0.46 |
| Drop figure | Fig 4.6 (↔ Table 4.8) | 0.43 |
| Drop table | Table 4.22 (↔ Fig 4.11 + Table 4.28) | 0.30 |
| | **Subtotal** | **≈ 3.2 pages** |

### Medium confidence — decide together

| Action | Item | Saving |
|---|---|---|
| Drop figure | Fig 4.3 (↔ Table 4.3) — or replace with G3 | 0.47 |
| Move to appendix | Table 4.12 (full 9×8 sweep) → D2 | 0.40 |
| Shrink table | Table 4.14 → 4 rows, sweep to appendix → D2 | 0.20 |
| Fold into prose | Table 4.4 (4 rows, all numbers already in text) | 0.19 |
| | **Subtotal** | **≈ 1.3 pages** |

**Combined: ≈ 4.5 pages.**

**Effect on the page budget.** Core manuscript is currently **97 pages** (Ch. 1 p. 1 → Ch. 5 ends p. 97). High-confidence actions alone take it to **≈ 94**; everything to **≈ 92-93**. Chapter 4 drops from 34 pages to ≈ 30. Figure count falls 23 → 17 (16 if Fig 4.3 goes), table count 34 → 32 — which moves the figure:table ratio toward the balance the supervisor asked for, without losing a single result.

---

## 7. Copy-paste action list

**For D5 (conciseness pass) — high confidence, batch-approvable**
```
DELETE  chapter4.tex  figure env  fig:dense_bar_chart      (Fig 4.5,  ~line 277-282)
DELETE  chapter4.tex  figure env  fig:dense_grouped        (Fig 4.6,  ~line 284-289)
DELETE  chapter4.tex  figure env  fig:failure_cliff        (Fig 4.2,  ~line 75-80)
DELETE  chapter4.tex  figure env  fig:first_pass_split     (Fig 4.13, ~line 859-864)
DELETE  chapter4.tex  figure env  fig:length_gain          (Fig 4.14, ~line 866-871)
DELETE  chapter4.tex  figure env  fig:regression_pie       (Fig 4.15, ~line 915-920)
DELETE  chapter4.tex  table  env  tab:system_progression   (Tab 4.22, ~line 758-775)
DELETE  chapter4.tex  dead \iffalse block fig:regression_pie_old  (~line 922-933)
```
Each deletion requires removing or rewording the sentence that cross-references it (E3 will catch any missed `\ref`).

**For D2 (appendix analysis) — inputs**
```
APPENDIX-CANDIDATE  Table 4.12  full 9x8 repetition sweep   (~0.40 page)
APPENDIX-CANDIDATE  Table 4.14  9-point CC alpha sweep rows (~0.20 page)
CONSIDER            Table 2.3 vs Table 2.4 — near-duplicate model tables, merge or drop one
NOTE                Table 4.26 (Arabic big-win examples, ~38%) — analysed as ORIGINAL content,
                    NOT a duplication candidate. D2 should judge it on page-budget grounds alone.
```

**For E2 (figure regeneration) — required fixes**
```
REGENERATE  03_model_comparison.ipynb  -> fixes Fig 4.9 mojibake (Δ), also v2_slope
FIX         Fig 4.11  add missing "Best blind BM25 (Aya β=2, 0.5855)" bar
FIX         Fig 4.8   add β=2/4/6 points, or annotate that optima are off-chart
DECIDE      Fig 3.6   AI-generated JPEG vs the existing TikZ fig_3_8_csqe.pdf
```
*Checked in passing:* the E2 carry-over concerns for Fig 4.2/4.3 appear **already resolved** in the committed renders — Fig 4.2 annotates 33.9% (matching the canonical 34%) and Fig 4.3 uses the 1–3 / 4–8 / 9+ buckets (matching Table 4.3). Fig 4.4 is a different quantity from Table 4.4 rather than a stale version (see P-5). E2 should still confirm independently.

---

## ⚠️ Needs a team or supervisor decision

1. **Fig 4.3 — drop or replace?** Dropping it removes the only view of within-bucket spread. Replacing it with **G3** (query-length histogram) makes the point better. Medium confidence either way; Osman + Elhaj call.
2. **Fig 3.6 — AI-generated raster for our own contribution's diagram.** A TikZ alternative already exists. Recommend raising with Dr. Tahani, since a committee may ask how the figure was made.
3. **Build any of G1/G2?** They cost time but G1 and G2 are the two figures that would most strengthen the results chapter and the defense — and they are genuine, not re-plots, which is exactly what the supervisor asked for. Recommend at least **G2** (cheap, and it doubles as F1 material).
