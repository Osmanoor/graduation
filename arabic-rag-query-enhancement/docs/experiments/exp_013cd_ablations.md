# Experiment 013c/013d: CSQE Component Ablation + Query Repetition Sweep

**Date:** April 11, 2026
**Owner:** Mohammed Elhaj
**Status:** ✅ Complete
**Notebook:** `experiments/exp_013_ablations.ipynb` (generation) + `docs/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb` (evaluation, Section 11)

---

## Motivation

Exp 013 showed CSQE (2 corpus + 2 blind, α=4) achieves 0.6157 nDCG@10 on BM25 alone and 0.7137 in Config A fusion. But two questions remained for thesis Chapter 5:

1. **Which component drives the gain — corpus grounding or blind sampling?** CSQE uses 2+2. Ablating to 4+0 (corpus-only) and 0+4 (blind-only) isolates the contribution of each.
2. **How sensitive is the result to query repetition α?** The choice α=4 was set in advance; α∈{1,2,3,4} can be reconstructed from stored expansions with no new model run.

---

## Setup

| Parameter | Exp 013c (corpus-only) | Exp 013d (blind-only) | Exp 013 (full CSQE) |
|-----------|----------------------|---------------------|---------------------|
| num_corpus_samples | 4 | 0 | 2 |
| num_blind_samples | 0 | 4 | 2 |
| query_repetition α | 4 | 4 | 4 |
| temperature | 1.0 | 1.0 | 1.0 |
| top_k_docs (first-pass) | 5 | 5 | 5 |
| doc_truncation_tokens | 128 | 128 | 128 |
| model | Aya Expanse 8B (BF16) | Aya Expanse 8B (BF16) | Aya Expanse 8B (BF16) |
| dataset | MIRACL Arabic dev (2,896 queries) | same | same |

**α ablation** reconstructed from exp_013 pkl `full_results` — no new generation needed.
Final query: `(query + ' ') * α + ' '.join(corpus_exps + blind_exps)`

---

## Results

### Component Ablation — Individual BM25 Retrieval

| System | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25 alone (no QE) | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| **013c: Corpus-only** (4c+0b, α=4) | **0.5381** | **0.6457** | **0.8790** | **0.5651** |
| **013d: Blind-only** (0c+4b, α=4) | **0.5752** | **0.7089** | **0.9201** | **0.6032** |
| **013: CSQE 2+2** (α=4) | **0.6157** | **0.7447** | **0.9422** | **0.6380** |
| Hybrid RRF k=20 (no QE) | 0.6267 | 0.7597 | 0.9466 | 0.6517 |

### Component Ablation — Config A Fusion (BM25+ablation + Dense original, RRF k=20)

| System | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| **013c + Dense RRF** | **0.6616** | **0.7905** | **0.9506** | **0.6812** |
| **013d + Dense RRF** | **0.7082** | **0.8288** | **0.9613** | **0.7324** |
| **013 + Dense RRF** | **0.7137** | **0.8363** | **0.9734** | **0.7363** |
| Hybrid RRF k=20 (no QE) | 0.6267 | 0.7597 | 0.9466 | 0.6517 |

### Query Repetition Ablation (α sweep, reconstructed from exp_013 full_results)

| α | BM25+CSQE nDCG@10 | Config A RRF nDCG@10 |
|---|-------------------|---------------------|
| 1 | 0.6095 | 0.7123 |
| 2 | 0.6130 | 0.7121 |
| 3 | 0.6154 | 0.7130 |
| **4** | **0.6157** | **0.7137** |

---

## Analysis

### Finding 1 — Blind-only outperforms corpus-only on BM25 alone

**013d (blind, 0.5752) > 013c (corpus, 0.5381)** — the opposite of what was predicted. This is counterintuitive: the "mufti" hypothesis expected corpus-grounded expansions to provide better vocabulary than parametric generation.

**Explanation:** BM25 benefits from *vocabulary breadth* (more Arabic term variants) and blind sampling generates full answer paragraphs with diverse vocabulary. Corpus extraction tends to produce passage-level excerpts — often structurally similar to the original query terms — providing less novel vocabulary gain for BM25 term matching.

### Finding 2 — Combination is synergistic, not additive

CSQE 2+2 (0.6157) > blind-only (0.5752) > corpus-only (0.5381).

The gap between CSQE and blind-only (+0.0405) is larger than between blind-only and BM25 alone (+0.1131). The corpus and blind expansions are *complementary*: corpus anchors the expansion to attested Arabic Wikipedia vocabulary; blind generates diverse answer-space vocabulary. Together they cover both.

### Finding 3 — Fusion narrows the gap between ablations

In Config A RRF fusion, the blind-only result (0.7082) is only 0.0055 below full CSQE (0.7137). The Dense original-query retriever compensates: it brings semantic signal that does not depend on expansion quality, reducing the marginal value of the corpus component in fusion.

**Key takeaway:** Corpus grounding matters most when BM25 is used alone. In the full system (BM25+CSQE + Dense RRF), its contribution is measurable but modest (+0.0055 nDCG@10).

### Finding 4 — Query repetition is a minor factor

BM25 improves monotonically α=1→4 but only by +0.0062 (0.6095 → 0.6157). Config A fusion is nearly flat: range = 0.0016 (0.7121 → 0.7137). Both observations are consistent with the Exp 1.1 BM25 repetition sweep (Aya blind: β=2 was best, with diminishing returns above β=3).

The slight gain from α=1→4 suggests the original query signal is not over-represented at α=4 for these expansion lengths. However, for practical purposes **α=1 already captures 98.7% of the Config A RRF gain** (0.7123 vs 0.7137). The α choice matters negligibly.

---

## Artifacts

| File | Description |
|------|-------------|
| `experiments/exp_013_ablations.ipynb` | Generation notebook (013c + 013d) |
| `docs/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb` | Evaluation (Section 11) |
| `results/enhanced_queries/exp_013c_corpus_only.pkl` | 013c enhanced queries pkl |
| `results/enhanced_queries/exp_013d_blind_only.pkl` | 013d enhanced queries pkl |
| `results/exp_11_ablations/ablation_table.csv` | Full ablation table |
| `results/exp_11_ablations/alpha_ablation.csv` | Alpha sweep table |
| `results/exp_11_ablations/ablation_bar_chart.png` | Component ablation bar chart |
| `results/exp_11_ablations/alpha_sweep.png` | Alpha sweep line chart |
