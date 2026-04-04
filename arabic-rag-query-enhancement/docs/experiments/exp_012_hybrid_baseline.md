# Experiment 012: Hybrid Baseline (BM25 + mDPR)

**Date:** April 4, 2026  
**Owner:** Mohammed Elhaj  
**Status:** ✅ Complete  
**Notebook:** `experiments/phase4_quick_wins.ipynb`

---

## Motivation

BM25 and mDPR retrieve different relevant documents — BM25 via exact term matching, mDPR via semantic similarity. Fusing their scores should yield a stronger baseline than either alone.

The MIRACL paper (Zhang et al., TACL 2023) reports a hybrid BM25+mDPR = 0.673 nDCG@10. Our BM25S-based hybrid will be slightly lower since BM25S differs from Pyserini BM25.

This establishes the **strongest non-QE baseline** — all QE experiments must beat it to demonstrate value.

---

## Setup

| Parameter | Value |
|-----------|-------|
| BM25 source | `results/baseline_bm25/exp_002_baseline_bm25.txt` (TREC format) |
| mDPR source | `results/baseline_dense/exp_001_baseline_dense.txt` (TREC format) |
| Normalization | Min-max per query to [0, 1] |
| Missing docs | Score = 0 from the absent retriever |
| GPU needed | No — pure score arithmetic on existing run files |
| Dataset | MIRACL Arabic dev (2,896 queries) |

**Fusion methods tested:**
- **Convex Combination (CC):** `s = α · BM25_norm + (1−α) · mDPR_norm`, α ∈ {0.1 … 0.9}
- **Reciprocal Rank Fusion (RRF):** `s(d) = Σ 1/(k + rank_i(d))`, k ∈ {20, 60}

---

## Results

### Summary Table

| Method | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25 alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| **Hybrid CC (α=0.5)** | **0.6266** | 0.7478 | 0.9458 | **0.6577** |
| **Hybrid RRF (k=20)** | **0.6267** | **0.7597** | **0.9467** | 0.6517 |

**New strongest non-QE baseline: 0.6267 nDCG@10** (+0.1274 vs mDPR, +0.1646 vs BM25).

### CC Alpha Sweep (All Metrics)

| α | nDCG@10 | Recall@10 | Recall@100 | MRR |
|---|---------|-----------|------------|-----|
| 0.1 | 0.5248 | 0.6412 | 0.9333 | 0.5584 |
| 0.2 | 0.5533 | 0.6683 | 0.9413 | 0.5861 |
| 0.3 | 0.5830 | 0.7014 | 0.9449 | 0.6161 |
| 0.4 | 0.6137 | 0.7392 | 0.9454 | 0.6426 |
| **0.5** | **0.6266** | **0.7478** | **0.9458** | **0.6577** |
| 0.6 | 0.6051 | 0.7289 | 0.9440 | 0.6355 |
| 0.7 | 0.5743 | 0.6963 | 0.9439 | 0.6049 |
| 0.8 | 0.5384 | 0.6634 | 0.9416 | 0.5678 |
| 0.9 | 0.4996 | 0.6297 | 0.9350 | 0.5257 |

### RRF Results

| k | nDCG@10 | Recall@10 | Recall@100 | MRR |
|---|---------|-----------|------------|-----|
| **20** | **0.6267** | **0.7597** | **0.9467** | 0.6517 |
| 60 | 0.6230 | 0.7553 | 0.9467 | 0.6490 |

---

## Analysis

1. **CC vs RRF essentially tied on nDCG@10** (0.6266 vs 0.6267). RRF has slightly better Recall@10 (+0.0119); CC has better MRR (+0.0060).

2. **α=0.5 is optimal** — equal weighting of BM25 and mDPR. Slight BM25 bias (α=0.4–0.6) all perform well. The curve is smooth and peaked, confirming CC is robust.

3. **Recall@100 jumps to ~0.946** from 0.858 (BM25) / 0.841 (mDPR) — the union of candidate sets covers far more relevant documents.

4. **vs MIRACL paper:** Their hybrid = 0.673; ours = 0.627. The gap is expected — they use Pyserini BM25 (0.481) vs our BM25S (0.462).

5. **Implication for QE:** Jais-2-8B dense (0.6018 nDCG@10) and Aya BM25-with-repetition (0.5855) both fall below this hybrid baseline. Only QE approaches that improve *both* retrievers or achieve >0.627 on one will add value beyond simple fusion.

---

## References

- Zhang et al. (2023). "MIRACL: A Multilingual Retrieval Dataset." TACL. arXiv:2210.09984
- Bruch et al. (2023). "An Analysis of Fusion Functions for Hybrid Retrieval." ACM TOIS. arXiv:2210.11934

---

## Artifacts

| File | Description |
|------|-------------|
| `experiments/phase4_quick_wins.ipynb` | Notebook (Exp 1.1 + 1.2) |
| `experiments/exp_12_hybrid_baseline/exp12_cc_metrics.json` | CC metrics for all 9 α values |
| `experiments/exp_12_hybrid_baseline/exp12_rrf_metrics.json` | RRF metrics for k=20, k=60 |
| `experiments/exp_12_hybrid_baseline/exp12_summary.csv` | Summary comparison table |
| `experiments/exp_12_hybrid_baseline/exp12_cc_sweep.csv` | Full CC sweep table |
| `experiments/exp_12_hybrid_baseline/hybrid_cc_alpha0.5.txt` | TREC run file — best CC (for Task 6.3c) |
| `experiments/exp_12_hybrid_baseline/hybrid_rrf_k20.txt` | TREC run file — best RRF (for Task 6.3c) |
| `experiments/exp_12_hybrid_baseline/alpha_sensitivity.png` | α sensitivity plot |
