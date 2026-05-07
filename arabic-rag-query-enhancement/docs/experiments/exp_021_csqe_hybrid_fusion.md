# Experiment 2.1: CSQE + Hybrid Fusion

**Date:** April 10, 2026  
**Owner:** Mohammed Elhaj  
**Status:** ✅ Complete  
**Notebook:** `experiments/phase4_quick_wins (1).ipynb` (Section 10)

---

## Motivation

Exp 013 (CSQE) showed that corpus-steered query expansion lifts BM25 nDCG@10 from 0.4621 to 0.6157 — a massive +33% gain — but still fell 0.011 points short of the hybrid baseline (0.6267). Meanwhile, Exp 1.2 showed that BM25+mDPR hybrid fusion is a very strong non-QE system.

The natural next question: **what happens when we combine CSQE-enhanced queries with hybrid fusion?** We test three configurations that cover the space of "which retriever gets the CSQE query":

- **Config A:** BM25+CSQE + Dense (original short query)
- **Config B:** BM25 (original) + Dense+CSQE
- **Config C:** BM25+CSQE + Dense+CSQE (all QE)

---

## Setup

| Parameter | Value |
|-----------|-------|
| CSQE pkl | `results/enhanced_queries/exp_013_csqe_aya_8b.pkl` (2,896 queries) |
| BM25 retriever | BM25S (Arabic stemmer + stopwords) |
| Dense retriever | mDPR (FAISS index) |
| Top-K per retriever | 100 |
| Fusion methods | Convex Combination (CC): α ∈ {0.1 … 0.9}; RRF: k ∈ {20, 60} |
| Dataset | MIRACL Arabic dev (2,896 queries) |
| GPU | A100 40GB (Dense encoding: 23 min) |

---

## Results

### Full Results Table — All Systems (for thesis)

| Method | nDCG@10 | Recall@10 | Recall@100 | MRR | Source |
|--------|---------|-----------|------------|-----|--------|
| BM25 alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 | exp_002 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 | exp_001 |
| Blind QE + Dense: Qwen 2.5 3B | 0.5435 | 0.6608 | 0.8594 | 0.5742 | exp_003 |
| Blind QE + Dense: Qwen3-4B | 0.5691 | 0.6824 | 0.8726 | 0.6015 | exp_007 |
| Blind QE + BM25: Aya 8B best (β=2) | 0.5855 | — | — | — | exp_011 |
| Blind QE + Dense: Jais-2-8B | 0.6018 | 0.7161 | 0.8981 | 0.6356 | exp_006 |
| Blind QE + Dense: Aya 8B (Osman) | 0.6164 | 0.7256 | 0.9001 | 0.6493 | Osman exp |
| BM25+CSQE alone | 0.6157 | 0.7447 | 0.9422 | 0.6380 | exp_013 |
| Dense+CSQE alone | 0.5915 | 0.7073 | 0.8816 | 0.6225 | exp_013 |
| Hybrid CC α=0.5 (no QE) | 0.6266 | 0.7478 | 0.9458 | 0.6577 | exp_012 |
| Hybrid RRF k=20 (no QE) | 0.6267 | 0.7597 | 0.9466 | 0.6517 | exp_012 |
| B: BM25 + Dense+CSQE RRF (k=20) | 0.6474 | 0.7928 | 0.9571 | 0.6578 | exp_021 |
| B: BM25 + Dense+CSQE CC (α=0.4) | 0.6588 | 0.7851 | 0.9569 | 0.6777 | exp_021 |
| C: BM25+CSQE + Dense+CSQE RRF (k=20) | 0.6936 | 0.8290 | 0.9660 | 0.7037 | exp_021 |
| C: BM25+CSQE + Dense+CSQE CC (α=0.5) | 0.6959 | 0.8249 | 0.9647 | 0.7079 | exp_021 |
| A: BM25+CSQE + Dense CC (α=0.6) | 0.7088 | 0.8302 | 0.9717 | 0.7268 | exp_021 |
| **A: BM25+CSQE + Dense RRF (k=20)** | **0.7137** | **0.8363** | **0.9734** | **0.7362** | exp_021 |

### Config A — Full CC Alpha Sweep

| α | nDCG@10 | Recall@10 | Recall@100 | MRR |
|---|---------|-----------|------------|-----|
| 0.1 | — | — | — | — |
| … | … | … | … | … |
| 0.6 | 0.7088 | 0.8302 | 0.9717 | 0.7268 |
| … | … | … | … | … |

*Full sweep values in `results/exp_21_csqe_hybrid/exp21_all_metrics.json`*

### Delta Analysis vs Key Benchmarks (nDCG@10)

| Comparison | Δ nDCG@10 | % change |
|------------|-----------|---------|
| Best (A RRF) vs BM25 alone | +0.2516 | +54.5% |
| Best (A RRF) vs mDPR alone | +0.2144 | +42.9% |
| Best (A RRF) vs best blind BM25 QE (Aya β=2) | +0.1282 | +21.9% |
| Best (A RRF) vs best blind Dense QE (Aya 8B, 0.6164) | +0.0973 | +15.8% |
| Best (A RRF) vs Hybrid RRF (no QE) | +0.0870 | +13.9% |
| Config C vs Config A | −0.0178 | Dense hurts with CSQE queries |
| Config B vs Hybrid RRF | +0.0207 | Weakest config still beats no-QE hybrid |
| ALL configs vs Hybrid RRF | **all positive** | Every fusion beats the non-QE hybrid |

### System Progression (thesis narrative table)

| Stage | nDCG@10 | Δ cumulative |
|-------|---------|-------------|
| BM25 alone (no QE) | 0.4621 | — |
| mDPR alone (no QE) | 0.4993 | — |
| Best blind QE + Dense (Jais-2) | 0.6018 | +0.1025 over mDPR |
| Best blind QE + BM25 (Aya β=2) | 0.5855 | +0.1234 over BM25 |
| Hybrid fusion (no QE) | 0.6267 | +0.1646 over BM25 |
| CSQE + BM25 alone | 0.6157 | +0.1536 over BM25 |
| **CSQE + Hybrid (Config A RRF)** | **0.7137** | **+0.2516 over BM25** |

---

## Analysis

1. **Config A is the winner: BM25+CSQE + Dense (original).** This is counterintuitive — why not expand both? The answer is that BM25 and Dense benefit from *different* query representations. BM25 uses exact term matching, so CSQE's corpus-grounded vocabulary expansion (more Arabic terms, extracted from relevant documents) directly increases recall. Dense (mDPR) uses semantic similarity between query and document vectors, and its encoder was trained on short natural-language queries. Feeding it 1,500-character CSQE expansions degrades the embedding quality.

2. **Dense+CSQE hurts in fusion (Config C < Config A by −0.018 nDCG@10).** Config C gives Dense the CSQE query (0.5915 individually) vs Config A which gives Dense the original query (0.4993 individually). Yet Config A fused is *better*. This confirms the encoder mismatch: the individual retrieval gains from Dense+CSQE are real but the embeddings are less discriminative, which hurts when fused with a strong BM25+CSQE signal.

3. **Config B is the weakest (+0.0321 over hybrid at best).** Applying CSQE only to Dense (Config B) gives the smallest gain. BM25 is the retriever that most benefits from CSQE's expanded vocabulary — without it, the BM25 side stays at baseline, capping the fusion ceiling.

4. **RRF outperforms CC for Config A (0.7137 vs 0.7088).** For Config C, CC slightly edges RRF (0.6959 vs 0.6936). This matches our Exp 1.2 finding where RRF and CC were nearly tied. RRF is more robust when the score distributions differ significantly between the two run files (CSQE-expanded BM25 vs original-query Dense scores are very different scale/shape).

5. **Recall@100 reaches 0.9734 — the ceiling for this dataset.** The combined system finds 97.3% of relevant documents in the top 100 candidates. The remaining 2.7% is likely irretrievable regardless of reranking. At k=10, Recall@10 = 0.8363 means 84% of relevant docs appear in the first 10 results — a strong upper bound for any downstream reranker.

6. **This is the main thesis result.** A system combining CSQE query expansion (grounded in corpus vocabulary) with hybrid retrieval (BM25 + Dense) achieves 0.7137 nDCG@10 — a +54.5% improvement over BM25 alone and a +42.9% improvement over Dense alone.

---

## Key Design Principle (Thesis Contribution)

> **Retriever-specific query representation:** BM25 benefits from long, vocabulary-rich CSQE expansions; Dense benefits from short, semantically pure original queries. Applying QE asymmetrically — only to BM25 — maximizes the gains from each retriever's inherent strength.

This is a novel finding that extends beyond the original CSQE paper (which only evaluates on BM25).

---

## References

- Lei, Y., et al. (2024). "CSQE: Corpus-Steered Query Expansion." arXiv:2402.18031.
- Zhang et al. (2023). "MIRACL: A Multilingual Retrieval Dataset." TACL. arXiv:2210.09984.
- Bruch et al. (2023). "An Analysis of Fusion Functions for Hybrid Retrieval." ACM TOIS. arXiv:2210.11934.

---

## Artifacts

| File | Description |
|------|-------------|
| `experiments/phase4_quick_wins (1).ipynb` | Notebook (Section 10) |
| `results/exp_21_csqe_hybrid/exp21_summary.csv` | Summary table |
| `results/exp_21_csqe_hybrid/exp21_all_metrics.json` | Full CC + RRF metrics |
| `results/exp_21_csqe_hybrid/bm25_csqe_run.txt` | TREC run — BM25+CSQE |
| `results/exp_21_csqe_hybrid/dense_csqe_run.txt` | TREC run — Dense+CSQE |
| `results/exp_21_csqe_hybrid/hybrid_csqe_rrf_k20.txt` | TREC run — best Config C (for ablation) |
