# Chapter 4: Results and Discussion — Tracking Document

**Created:** 2026-03-27
**Last Updated:** 2026-03-27
**Status:** First complete draft
**File:** `Chapters/chapter4.tex`

---

## Final Outline

### Chapter Introduction (no section number)
Brief paragraph introducing the chapter scope and zigzag mapping to Chapter 3.

### 4.1 Baseline Results and Comparison
Corresponds to Section 3.2 (Baseline Implementation).

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 4.1 main | Table: mDPR vs BM25S on 4 metrics, reproduction accuracy (<0.1% for mDPR, 96% for BM25S) | `docs/experiments/exp_001_baseline_dense.md`, `docs/experiments/exp_002_baseline_bm25.md` |
| 4.1.1 Complementary Strengths | mDPR better NDCG/MRR, BM25 better Recall@100, confirmed test-separately decision | Same |

### 4.2 Error Analysis Findings
Corresponds to Section 3.3 (Error Analysis Methodology).

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 4.2.1 Overall Failure Rate | 39% failure (1,130 queries), 192 zero-recall, only 5.1% successful | `research_decisions/error_analysis_phase1_quantitative.md` |
| 4.2.2 Short Query Performance Gap | Short=0.240 vs Long=0.406 (41% gap), r=0.125 (p<0.001) | Same |
| 4.2.3 Retrieval Coverage Analysis | 99.4% at depth 100 vs 93.4% at depth 10 — ranking problem, not retrieval | Same |
| 4.2.4 Technique Selection Rationale | Vocabulary mismatch, named entity variations, diacritics → Query2Doc | `research_decisions/qe_technique_selection.md` |

### 4.3 Query2Doc Results
Corresponds to Section 3.4 (Query2Doc Implementation).

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 4.3.1 Dense Retrieval (exp_003) | +8.9% NDCG@10, +7.3% Recall@10, +7.8% MRR, 8.45x expansion, ~40 min runtime | `docs/experiments/exp_003_query2doc_dense.md` |
| 4.3.2 BM25 Retrieval (exp_004) | -11.5% NDCG@10 (all metrics degraded), term dilution analysis | `docs/experiments/exp_004_query2doc_bm25.md` |
| 4.3.3 Comparison with Original Paper | Zero-shot 3B Arabic > Few-shot 175B English on dense; BM25 failure due to missing repetition | Same |

### 4.4 Model Comparison Results
Corresponds to Section 3.5 (Model Comparison Methodology).

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 4.4.1 Dense Retrieval Leaderboard | Full table: Aya (+23.5%) > Jais-2 (+20.5%) > Qwen3-8B (+19.3%) > ... > SILMA (+3.7%) | `.claude/contexts/thesis-writing.md`, `OSMAN_MODEL_COMPARISON_RESULTS.md`, experiment docs |
| 4.4.2 BM25 Retrieval Results | Jais-2 (+10.8%) > Aya (+9.2%) > Qwen2.5-7B (+1.3%); 6/9 models degrade; Jais-2 Arabic vocab hypothesis | Same |
| 4.4.3 Dropped Models Analysis | ALLaM: -48.9% (tokenizer leak), GPT-OSS: 70x slower + hallucinations | exp_008, exp_009 docs, model research docs |

### 4.5 Key Findings and Analysis
Synthesis section (Chapter 4 only — no Chapter 3 counterpart).

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 4.5.1 Model Size vs Performance | 2-3B: +3.7-8.9%, 4B: +8-14%, 7-8B: +16.4-23.5% | Compiled from all experiments |
| 4.5.2 Generational Improvement | Qwen3 vs Qwen 2.5 at both scales (+4.7%, +2.5%) | exp_003, exp_007, Osman results |
| 4.5.3 Arabic Specialisation vs Multilingual | OALL ≠ QE quality; Jais-2 exception for BM25 due to vocab | Analysis |
| 4.5.4 Dense vs BM25 Behaviour | 9/9 improve dense, 3/9 improve BM25; term dilution explanation | Compiled |
| 4.5.5 Best Model Recommendations | Aya (overall), Jais-2 (BM25), Qwen3-4B (constrained), temp=0.1 | Compiled |
| 4.5.6 Summary of All Experiments | Consolidated table of all experiments | All experiment docs |

---

## How to Update This Chapter

### Adding Expanded Experiment Results (Phase 4)
1. Add new results section (e.g., 4.6 "Chunking-Aware QE Results")
2. Update Table 4.10 (full summary) with new experiments
3. If new models are added, update leaderboard tables
4. Update Section 4.5 key findings if new patterns emerge
5. Ensure corresponding Chapter 3 methodology section exists

### Adding Osman's BM25 Full Metrics
- Currently only NDCG@10 for some models — add Recall@10, Recall@100, MRR when available
- Update Tables 4.6 and 4.10

### Updating After Query Repetition Experiments
- If BM25 experiments with n=5 repetition are run, add new section
- Compare with current simple-concatenation results
- Update term dilution analysis

---

## Cross-Reference Labels

| Label | Section | Usage |
|-------|---------|-------|
| `chap:results` | Chapter 4 | "As shown in Chapter~\ref{chap:results}" |
| `sec:res_baseline` | 4.1 | Baseline results |
| `tab:baseline_results` | 4.1 | Baseline comparison table |
| `sec:res_baseline_comparison` | 4.1.1 | Complementary strengths |
| `sec:res_error` | 4.2 | Error analysis findings |
| `sec:res_error_rate` | 4.2.1 | Failure rate |
| `tab:error_segmentation` | 4.2.1 | Performance segmentation table |
| `sec:res_error_length` | 4.2.2 | Short query gap |
| `tab:query_length` | 4.2.2 | Query length performance table |
| `sec:res_error_coverage` | 4.2.3 | Coverage analysis |
| `tab:coverage` | 4.2.3 | Coverage by depth table |
| `sec:res_error_rationale` | 4.2.4 | Technique selection rationale |
| `sec:res_query2doc` | 4.3 | Query2Doc results |
| `sec:res_q2d_dense` | 4.3.1 | Dense results (exp_003) |
| `tab:q2d_dense` | 4.3.1 | Dense results table |
| `sec:res_q2d_bm25` | 4.3.2 | BM25 results (exp_004) |
| `tab:q2d_bm25` | 4.3.2 | BM25 results table |
| `sec:res_term_dilution` | 4.3.2 | Term dilution analysis |
| `sec:res_q2d_comparison` | 4.3.3 | Comparison with original paper |
| `tab:q2d_paper_comparison` | 4.3.3 | Paper comparison table |
| `sec:res_model_comparison` | 4.4 | Model comparison results |
| `sec:res_mc_dense` | 4.4.1 | Dense leaderboard |
| `tab:dense_leaderboard` | 4.4.1 | Dense leaderboard table |
| `fig:dense_bar_chart` | 4.4.1 | Dense bar chart figure |
| `sec:res_mc_bm25` | 4.4.2 | BM25 results |
| `tab:bm25_leaderboard` | 4.4.2 | BM25 leaderboard table |
| `sec:res_dropped` | 4.4.3 | Dropped models analysis |
| `sec:res_allam` | 4.4.3 | ALLaM analysis |
| `sec:res_gptoss` | 4.4.3 | GPT-OSS analysis |
| `sec:res_key_findings` | 4.5 | Key findings synthesis |
| `sec:res_finding_size` | 4.5.1 | Size vs performance |
| `fig:size_vs_performance` | 4.5.1 | Size vs performance scatter plot |
| `sec:res_finding_generation` | 4.5.2 | Generational improvement |
| `tab:qwen_generations` | 4.5.2 | Qwen generational comparison table |
| `sec:res_finding_arabic` | 4.5.3 | Arabic vs multilingual |
| `sec:res_finding_retriever` | 4.5.4 | Dense vs BM25 behaviour |
| `tab:retriever_divergence` | 4.5.4 | Retriever divergence table |
| `sec:res_finding_best` | 4.5.5 | Best model recommendations |
| `sec:res_summary` | 4.5.6 | Full experiment summary |
| `tab:full_summary` | 4.5.6 | Consolidated experiment table |
| `sec:res_repetition` | 4.6 | BM25 repetition results |
| `tab:bm25_repetition` | 4.6 | BM25 repetition table |
| `tab:bm25_best_config` | 4.6 | BM25 best-config supplementary table |
| `fig:repetition_heatmap` | 4.6 | Repetition heatmap figure |
| `sec:res_hybrid` | 4.7 | Hybrid fusion results |
| `tab:hybrid_results` | 4.7 | Hybrid fusion table |
| `fig:hybrid_comparison` | 4.7 | Hybrid comparison figure |
| `sec:res_csqe` | 4.8 | CSQE results |
| `sec:res_csqe_main` | 4.8.1 | CSQE main results |
| `tab:csqe_main` | 4.8.1 | CSQE main results table |
| `sec:res_csqe_ablation` | 4.8.2 | CSQE component ablation |
| `tab:csqe_ablation` | 4.8.2 | CSQE ablation table |
| `tab:alpha_sweep` | 4.8.2 | Alpha sweep table |
| `sec:res_csqe_hybrid` | 4.9 | CSQE + hybrid fusion results |
| `sec:res_csqe_configs` | 4.9.1 | Config A/B/C comparison |
| `tab:csqe_hybrid_configs` | 4.9.1 | Config comparison table |
| `tab:config_a_ablation` | 4.9.1 | Config A ablation table |
| `tab:config_a_alpha` | 4.9.1 | Config A alpha sweep table |
| `tab:delta_analysis` | 4.9.1 | Delta analysis table |
| `sec:res_progression` | 4.9.2 | System progression |
| `tab:system_progression` | 4.9.2 | Progression table |
| `sec:res_error_csqe` | 4.10 | Per-query error analysis |
| `sec:res_win_loss` | 4.10.1 | Win/loss distribution |
| `tab:error_distribution` | 4.10.1 | Win/loss table |
| `fig:csqe_scatter` | 4.10.1 | CSQE scatter plot figure |
| `sec:res_firstpass` | 4.10.2 | First-pass quality analysis |
| `tab:error_patterns` | 4.10.2 | First-pass quality table |
| `tab:query_length_split` | 4.10.2 | Query length split table |
| `sec:res_bigwins` | 4.10.3 | Big wins / corpus grounding |
| `tab:bigwin_examples` | 4.10.3 | Big-win examples table |
| `sec:res_regressions` | 4.10.4 | Regression analysis |
| `tab:regression_causes` | 4.10.4 | Regression causes table |
| `fig:regression_pie` | 4.10.4 | Regression pie chart |

---

## Figures and Tables

| ID | Type | Caption | Status |
|----|------|---------|--------|
| `tab:baseline_results` | Table | Baseline results | Complete |
| `tab:error_segmentation` | Table | Performance segmentation | Complete |
| `tab:query_length` | Table | Query length performance | Complete |
| `tab:coverage` | Table | Coverage by depth | Complete |
| `tab:q2d_dense` | Table | Dense Query2Doc results | Complete |
| `tab:q2d_bm25` | Table | BM25 Query2Doc results | Complete |
| `tab:q2d_paper_comparison` | Table | Original paper comparison | Complete |
| `tab:dense_leaderboard` | Table | Dense model leaderboard | Complete |
| `tab:bm25_leaderboard` | Table | BM25 model leaderboard | Complete |
| `tab:qwen_generations` | Table | Qwen generational comparison | Complete |
| `tab:retriever_divergence` | Table | Dense vs BM25 divergence | Complete |
| `tab:full_summary` | Table | All experiments summary | Complete |
| `fig:dense_bar_chart` | Figure | Dense NDCG@10 bar chart | Placeholder |
| `fig:size_vs_performance` | Figure | Size vs performance scatter | Placeholder |

---

## Exact Metric Values Source Reference

All metric values in this chapter come from documented experiment files:

| Experiment | Source Document |
|------------|----------------|
| exp_001 (Dense baseline) | `docs/experiments/exp_001_baseline_dense.md` |
| exp_002 (BM25 baseline) | `docs/experiments/exp_002_baseline_bm25.md` |
| exp_003 (Qwen 2.5 3B, Dense) | `docs/experiments/exp_003_query2doc_dense.md` |
| exp_004 (Qwen 2.5 3B, BM25) | `docs/experiments/exp_004_query2doc_bm25.md` |
| exp_005 (Falcon-H1, Dense+BM25) | `docs/experiments/exp_005_falcon_h1_3b_dense.md` |
| exp_006 (Jais-2, Dense+BM25) | `research_decisions/model_comparison_guide.md`, TASKS.md |
| exp_007 (Qwen3-4B, Dense+BM25) | `docs/experiments/exp_007_qwen3_4b_dense.md` |
| exp_008 (ALLaM, Dense) | TASKS.md, CLAUDE.md reference tables |
| exp_009 (GPT-OSS, Dropped) | TASKS.md, CLAUDE.md reference tables |
| Osman's 5 models | `docs/OSMAN_MODEL_COMPARISON_RESULTS.md` |

---

## Formatting Rules
- **Passive voice** throughout
- **Tables**: Caption ABOVE, `\label{tab:xxx}`
- **Figures**: Caption below, `\label{fig:xxx}`
- **No re-explanation** of models — use `\ref{sec:xxx}` to Chapter 2
- **No code** — analysis described in prose only
- **IEEE references**: `[1]` before full stop
- **Negative results** documented with full analysis (Dr. Tahani's instruction)
