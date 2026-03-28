# Chapter 3: Methodology — Tracking Document

**Created:** 2026-03-27
**Last Updated:** 2026-03-27
**Status:** First complete draft
**File:** `Chapters/chapter3.tex`

---

## Final Outline

### Chapter Introduction (no section number)
Brief paragraph introducing the chapter scope and structure, with forward references to all sections and to Chapter 4.

### 3.1 Dataset and Experimental Setup
Shared setup for all experiments.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 3.1.1 Dataset: MIRACL Arabic | Corpus size (2.06M passages, 656K articles), dev set (2,896 queries, 29K judgements), MSA-only, HuggingFace access | `RESEARCH_CONTEXT_KERNEL.md.md`, `research_decisions/technical_specifications.md` |
| 3.1.2 Hardware and Software Environment | T4 vs A100, Colab, Python stack, bitsandbytes NF4 quantisation | `docs/experiments/exp_001_baseline_dense.md` |
| 3.1.3 Evaluation Metrics | NDCG@10, Recall@10, MRR, Recall@100, pytrec_eval | References to Chapter 2 equations |
| 3.1.4 Experimental Pipeline Overview | Two-phase architecture, query enhancement → retrieval → evaluation, two-notebook workflow | `research_decisions/model_comparison_guide.md` |

### 3.2 Baseline Implementation
Two baselines: Dense (mDPR) and Sparse (BM25S).

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 3.2.1 Dense Retrieval Baseline (mDPR) | mdpr-tied-pft-msmarco, FAISS index (5.47 GB), GPU batch encoding (64 queries), intentionally "weaker" baseline rationale | `docs/experiments/exp_001_baseline_dense.md`, `reports/mdpr_baseline_report.md` |
| 3.2.2 Sparse Retrieval Baseline (BM25S) | BM25S library, Pyserini blocker (Java conflict), PyStemmer + NLTK stopwords, k1=0.9 b=0.4, 96% of Pyserini performance | `docs/experiments/exp_002_baseline_bm25.md` |
| 3.2.3 Baseline Comparison Rationale | Test separately for insight into improvement origins | `RESEARCH_CONTEXT_KERNEL.md.md` |

### 3.3 Error Analysis Methodology
Phase 1 quantitative analysis on exp_001.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 3.3.1 Quantitative Analysis Framework | 3 performance categories (Failed/Mediocre/Successful), query features computed | `research_decisions/error_analysis_phase1_quantitative.md` |
| 3.3.2 Query Length Bucketing | Short/Medium/Long buckets, Pearson correlation | Same |
| 3.3.3 Failed Query Inspection | 20 worst queries, manual categorisation by question type, named entities, diacritics, spelling | Same |

### 3.4 Query2Doc Implementation
Query2Doc technique, modifications, and engineering.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 3.4.1 Query2Doc Technique | Pseudo-document generation, concatenation, difference from HyDE | `papers/2023_Query2doc.md`, `wang_2023_query2doc` citation |
| 3.4.2 Modifications from the Original Paper | Zero-shot, small open-source models, Arabic-only, retriever-specific concatenation | `research_decisions/qe_technique_selection.md` |
| 3.4.3 LLM Configuration | System prompt, generation params (temp, top_p, max_new_tokens, batch_size) | `docs/experiments/exp_003_query2doc_dense.md` |
| 3.4.4 Batch Processing Optimisation | Sequential → batch (8x), 256→128 tokens (2x), inference opts → 16x total speedup | Same |
| 3.4.5 Dense Retrieval with Query2Doc | q_enhanced = q + d_pseudo, mDPR encoding | Same |
| 3.4.6 BM25 Retrieval with Query2Doc | Same queries, no repetition in exp_004, paper's n=5 recommendation | `docs/experiments/exp_004_query2doc_bm25.md` |

### 3.5 Model Comparison Methodology
10 models, standardised protocol.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 3.5.1 Model Selection Criteria | Arabic support, 2-8B size, open-source, 3 categories (Arabic-specialised, multilingual, experimental) | `research_decisions/model_comparison_guide.md`, `research_decisions/llm_model_research.md` |
| 3.5.2 Standardised Evaluation Protocol | Sanity check → Full generation → Dense eval → BM25 eval, team split | Same |
| 3.5.3 Temperature Selection | Model-recommended vs empirical (SILMA 0.7 vs 0.1), 0.1 as default | `OSMAN_MODEL_COMPARISON_RESULTS.md` |
| 3.5.4 Model-Specific Technical Issues | Falcon batching bug, Jais BF16/token_type_ids, Qwen3 thinking mode, ALLaM tokenizer leak, GPT-OSS MoE slowness | Individual model research docs |
| 3.5.5 Quantisation Strategy | NF4 via bitsandbytes, double quantisation, applied to 7B+ models | `research_decisions/model_comparison_guide.md` |

---

## How to Update This Chapter

### Adding Expanded Experiments (Phase 4)
1. Add new subsection under 3.5 or create new section 3.6 (e.g., "Chunking-Aware QE Methodology")
2. If new hardware is used, update Section 3.1.2
3. If new metrics are added, update Section 3.1.3
4. Ensure corresponding Chapter 4 section is created (zigzag)

### Adding New Models
1. Ensure model is described in Chapter 2 (Section 2.3)
2. Add to Table 3.2 (model configurations)
3. If new technical issues arise, add to Section 3.5.4
4. Update model count in Section 3.5 intro text

### Adding New Techniques (e.g., HyDE, few-shot)
1. Create new section (e.g., 3.6 "HyDE Implementation")
2. Reference theoretical background from Chapter 2
3. Document modifications from original paper
4. Create corresponding Chapter 4 results section

---

## Cross-Reference Labels (for Chapter 4 and other chapters)

| Label | Section | Usage |
|-------|---------|-------|
| `chap:methodology` | Chapter 3 | "As described in Chapter~\ref{chap:methodology}" |
| `sec:meth_dataset` | 3.1 | Dataset and setup |
| `sec:meth_miracl` | 3.1.1 | MIRACL dataset specifics |
| `sec:meth_hardware` | 3.1.2 | Hardware/software environment |
| `sec:meth_metrics` | 3.1.3 | Evaluation metrics |
| `sec:meth_pipeline` | 3.1.4 | Pipeline overview |
| `fig:pipeline_overview` | 3.1.4 | Pipeline flowchart figure |
| `sec:meth_baseline` | 3.2 | Baseline implementation |
| `sec:meth_dense_baseline` | 3.2.1 | mDPR baseline |
| `sec:meth_bm25_baseline` | 3.2.2 | BM25S baseline |
| `sec:meth_baseline_rationale` | 3.2.3 | Why test separately |
| `sec:meth_error` | 3.3 | Error analysis methodology |
| `sec:meth_error_quant` | 3.3.1 | Quantitative analysis framework |
| `sec:meth_error_buckets` | 3.3.2 | Query length bucketing |
| `sec:meth_error_inspection` | 3.3.3 | Failed query inspection |
| `sec:meth_query2doc` | 3.4 | Query2Doc implementation |
| `sec:meth_q2d_technique` | 3.4.1 | Query2Doc technique |
| `sec:meth_q2d_modifications` | 3.4.2 | Modifications from original paper |
| `sec:meth_q2d_llm` | 3.4.3 | LLM configuration |
| `tab:q2d_params` | 3.4.3 | Generation parameters table |
| `sec:meth_q2d_batch` | 3.4.4 | Batch processing |
| `sec:meth_q2d_dense` | 3.4.5 | Dense + Query2Doc |
| `eq:q2d_dense` | 3.4.5 | Dense concatenation equation |
| `sec:meth_q2d_bm25` | 3.4.6 | BM25 + Query2Doc |
| `eq:q2d_bm25` | 3.4.6 | BM25 repetition equation |
| `sec:meth_model_comparison` | 3.5 | Model comparison methodology |
| `sec:meth_model_selection` | 3.5.1 | Model selection criteria |
| `tab:model_configs` | 3.5.1 | Model configurations table |
| `sec:meth_model_protocol` | 3.5.2 | Evaluation protocol |
| `sec:meth_temperature` | 3.5.3 | Temperature selection |
| `sec:meth_model_issues` | 3.5.4 | Technical issues |
| `sec:meth_quantisation` | 3.5.5 | Quantisation strategy |

---

## Figures and Tables

| ID | Type | Caption | Status |
|----|------|---------|--------|
| `fig:pipeline_overview` | Figure | Experimental pipeline flowchart | Placeholder — needs actual figure |
| `tab:q2d_params` | Table | LLM generation parameters (exp_003) | Complete |
| `tab:model_configs` | Table | Model configurations for comparison | Complete |

---

## Formatting Rules
- **Passive voice** throughout ("The experiment was conducted..." not "We conducted...")
- **No code** in thesis body — code referenced by description only
- **No re-explanation** of models or concepts defined in Chapter 2 — use `\ref{sec:xxx}` labels
- **IEEE references**: Numbered by order of appearance, `[1]` before full stop
- **Figures**: Figure 3.X, caption below, `\label{fig:xxx}`
- **Tables**: Table 3.X, caption ABOVE, `\label{tab:xxx}`
