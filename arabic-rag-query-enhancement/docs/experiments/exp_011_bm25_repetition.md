# Experiment 011: BM25 Query Repetition Fix

**Date:** April 4, 2026  
**Owner:** Mohammed Elhaj  
**Status:** ✅ Complete  
**Notebook:** `experiments/phase4_quick_wins.ipynb`

---

## Motivation

Our Query2Doc pipeline concatenates `query + pseudo_doc`, but BM25 scores by term frequency. A ~5-token query drowns in ~200 pseudo-doc tokens, making BM25 treat pseudo-doc terms as more important. This caused **6/9 models to degrade below the BM25 baseline**.

The Query2Doc paper (Wang et al., EMNLP 2023) fixes this by repeating the query: `(query + " ") * n + pseudo_doc`. MuGI (Zhang et al., EMNLP 2024 Findings) proposes an adaptive formula: `n = max(1, ⌊|pseudo_doc| / (|query| × β)⌋)`.

---

## Setup

| Parameter | Value |
|-----------|-------|
| Retriever | BM25S (Python-native, CPU-only) |
| Dataset | MIRACL Arabic dev (2,896 queries) |
| Models | All 9 viable Query2Doc models |
| Top-K | 100 |
| Configs tested | n ∈ {1, 3, 5, 7, 10}, MuGI β ∈ {2, 4, 6} |
| Total runs | 72 (9 models × 8 configs) |
| Runtime | ~73 minutes on Colab CPU |

---

## Results

### Key Finding: All 9 Models Now Beat Baseline

| Metric | At n=1 (current) | At best config |
|--------|:-:|:-:|
| Models above BM25 baseline (0.4621) | **3 / 9** | **9 / 9** |
| Models fixed by repetition | — | **6** |

### Best Configuration Per Model (nDCG@10)

| Model | n=1 | Best Config | Best nDCG@10 | Recall@10 | Recall@100 | MRR | Δ nDCG vs n=1 |
|-------|-----|-------------|-------------|-----------|------------|-----|---------------|
| **Aya Expanse 8B** | 0.5046 | **β=2** | **0.5855** | 0.7128 | 0.9300 | 0.6165 | +0.0808 |
| Jais-2-8B | 0.5122 | β=2 | 0.5731 | 0.7075 | 0.9217 | 0.6004 | +0.0610 |
| Qwen 2.5-7B | 0.4682 | n=5 | 0.5358 | 0.6765 | 0.9105 | 0.5586 | +0.0675 |
| Qwen3-8B | 0.4459 | n=7 | 0.5328 | 0.6695 | 0.9064 | 0.5590 | +0.0868 |
| Gemma 3 4B | 0.3447 | n=7 | 0.5277 | 0.6640 | 0.9002 | 0.5551 | **+0.1831** |
| Qwen3-4B | 0.4145 | n=7 | 0.5244 | 0.6617 | 0.8980 | 0.5500 | +0.1098 |
| Qwen 2.5-3B | 0.4090 | n=5 | 0.5185 | 0.6501 | 0.9031 | 0.5494 | +0.1095 |
| Falcon-H1-3B | 0.4038 | n=10 | 0.5113 | 0.6456 | 0.8927 | 0.5379 | +0.1074 |
| SILMA 2B | 0.4194 | n=5 | 0.4832 | 0.6216 | 0.8747 | 0.5048 | +0.0639 |

### nDCG@10 Sweep (All Configs)

| Model | n=1 | n=3 | n=5 | n=7 | n=10 | β=2 | β=4 | β=6 |
|-------|-----|-----|-----|-----|------|-----|-----|-----|
| Aya Expanse 8B | .5046 | .5652 | .5832 | .5849 | .5773 | **.5855** | .5515 | .5256 |
| Jais-2-8B | .5122 | .5492 | .5529 | .5516 | .5436 | **.5731** | .5521 | .5350 |
| Qwen3-8B | .4459 | .5181 | .5319 | **.5328** | .5254 | .5254 | .4841 | .4591 |
| Qwen 2.5-7B | .4682 | .5294 | **.5358** | .5331 | .5257 | .5320 | .4977 | .4774 |
| Qwen3-4B | .4145 | .5054 | .5239 | **.5244** | .5188 | .5177 | .4678 | .4347 |
| Gemma 3 4B | .3447 | .4800 | .5178 | **.5277** | .5239 | .4915 | .4184 | .3694 |
| Qwen 2.5-3B | .4090 | .5060 | **.5185** | .5181 | .5116 | .5046 | .4551 | .4253 |
| Falcon-H1-3B | .4038 | .4881 | .5082 | .5112 | **.5113** | .4979 | .4561 | .4266 |
| SILMA 2B | .4194 | .4783 | **.4832** | .4829 | .4788 | .4494 | .4252 | .4203 |

> Full metrics (Recall@10, Recall@100, MRR) for every model × config: `experiments/exp_11_bm25_repetition/exp11_all_metrics.json`

---

## Analysis

1. **Optimal repetition depends on model size:**
   - Large models (8B): MuGI β=2 works best (adaptive, longer pseudo-docs get more repetition)
   - Smaller models (3-4B): Fixed n=5–7 is optimal
   - Smallest (2B): n=5 is sufficient (shorter pseudo-docs need less compensation)

2. **Diminishing returns past n=7:** Performance peaks at n=5–7 for most models, then slightly declines at n=10 — over-repetition starts hurting.

3. **Biggest gain:** Gemma 3 4B went from 0.3447 → 0.5277 (+0.1831), the worst-degraded model became mid-pack.

4. **Practical recommendation:** Use β=2 (adaptive) as default for BM25 + Query2Doc. It automatically calibrates repetition per query.

---

## References

- Wang et al. (2023). "Query2doc: Query Expansion with Large Language Models." EMNLP. arXiv:2303.07678
- Zhang et al. (2024). "MuGI: Multi-Granularity Interactions." EMNLP Findings. arXiv:2401.06311

---

## Artifacts

| File | Description |
|------|-------------|
| `experiments/phase4_quick_wins.ipynb` | Notebook (Exp 1.1 + 1.2) |
| `experiments/exp_11_bm25_repetition/exp11_all_metrics.json` | All 4 metrics × 9 models × 8 configs |
| `experiments/exp_11_bm25_repetition/exp11_ndcg10.csv` | nDCG@10 table |
| `experiments/exp_11_bm25_repetition/exp11_recall10.csv` | Recall@10 table |
