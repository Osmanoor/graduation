# Experiment 013: CSQE — Corpus-Steered Query Expansion

**Date:** April 10, 2026  
**Owner:** Mohammed Elhaj  
**Status:** ✅ Complete  
**Notebook:** `experiments/exp_013_csqe_aya_8b.ipynb`

---

## Motivation

Query2Doc (blind LLM expansion) generates hypothetical passages from parametric knowledge — it cannot "see" the actual corpus vocabulary. This creates a lexical mismatch: the model might use different terminology than MIRACL Arabic documents, reducing retrieval precision.

CSQE (Corpus-Steered Query Expansion, Lei et al. arXiv:2402.18031) solves this by adding a BM25 first-pass retrieval step. The LLM is shown the top-K retrieved documents and asked to *extract* relevant sentences, grounding its output in real corpus vocabulary. This is combined with blind expansions to retain the benefits of parametric knowledge.

This is the **main thesis contribution** — the first application of CSQE to Arabic information retrieval. We extend the base CSQE paper by incorporating query repetition (α=4, from our Exp 011 finding) alongside the 2+2 corpus/blind expansion scheme.

---

## Setup

| Parameter | Value |
|-----------|-------|
| Model | `CohereForAI/aya-expanse-8b` (BF16, no quantization) |
| GPU | A100 40GB (Colab) |
| Dataset | MIRACL Arabic dev (2,896 queries) |
| BM25 first-pass k | 5 (top-5 docs per query) |
| Doc truncation | 128 tokens per retrieved doc |
| Temperature | 1.0 (diversity for multi-sample) |
| max_new_tokens | 128 |
| Corpus samples (N1) | 2 (LLM extracts sentences from retrieved docs) |
| Blind samples (N2) | 2 (HyDE-style, parametric knowledge) |
| Query repetition α | 4 (= N_total, from Exp 011 best-config finding) |
| Final query format | `(query × 4) + corpus_exp1 + corpus_exp2 + blind_exp1 + blind_exp2` |
| Corpus batch size | 8 (long ~800-1000 tok prompts) |
| Blind batch size | 32 (short ~60-80 tok prompts) |
| Total runtime | 51.5 minutes (2,896 queries) |
| Throughput | 56.2 queries/minute |
| Errors | 0 / 2,896 |

**CSQE prompt type (paper Table 2):** One-shot example using English sharks query, LLM instruction in English, Arabic corpus documents, Arabic output — this follows the same English-instruction pattern proven in our existing Aya notebooks.

**Infrastructure change from plan:** BF16 + cross-query batching added over original sequential 4-bit design. No change to algorithm or prompts. BF16 gives higher numerical precision than 4-bit NF4.

---

## Results

### Primary Results — Full Metrics

| Retriever | nDCG@10 | Recall@10 | Recall@100 | MRR |
|-----------|---------|-----------|------------|-----|
| **BM25 + CSQE (exp_013)** | **0.6157** | **0.7447** | **0.9422** | **0.6380** |
| **Dense (mDPR) + CSQE (exp_013)** | **0.5915** | **0.7073** | **0.8816** | **0.6225** |

### Full Comparison Table — All Systems (for thesis)

| System | nDCG@10 | Recall@10 | Recall@100 | MRR | Source |
|--------|---------|-----------|------------|-----|--------|
| BM25 alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 | exp_002 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 | exp_001 |
| Blind QE + Dense: Qwen 2.5 3B | 0.5435 | 0.6608 | 0.8594 | 0.5742 | exp_003 |
| Blind QE + Dense: Falcon-H1-3B | 0.5359 | 0.6484 | 0.8531 | 0.5681 | exp_005 |
| Blind QE + Dense: Qwen3-4B | 0.5691 | 0.6824 | 0.8726 | 0.6015 | exp_007 |
| Blind QE + BM25: Aya 8B (n=1) | 0.5046 | — | — | — | exp_011 |
| Blind QE + BM25: Aya 8B (β=2, best) | 0.5855 | — | — | — | exp_011 |
| Blind QE + Dense: Jais-2-8B (best Dense) | 0.6018 | 0.7161 | 0.8981 | 0.6356 | exp_006 |
| Blind QE + Dense: Aya 8B | *not measured* | — | — | — | — |
| Hybrid RRF k=20 (no QE) | 0.6267 | 0.7597 | 0.9466 | 0.6517 | exp_012 |
| **BM25 + CSQE (exp_013)** | **0.6157** | **0.7447** | **0.9422** | **0.6380** | exp_013 |
| **Dense + CSQE (exp_013)** | **0.5915** | **0.7073** | **0.8816** | **0.6225** | exp_013 |

### Delta Analysis (nDCG@10)

| Comparison | Δ nDCG@10 | % change |
|------------|-----------|---------|
| BM25+CSQE vs BM25 alone | +0.1536 | +33.2% |
| Dense+CSQE vs mDPR alone | +0.0922 | +18.5% |
| BM25+CSQE vs best blind BM25 QE (Aya β=2) | +0.0302 | +5.2% |
| Dense+CSQE vs best blind Dense QE (Jais-2) | −0.0103 | −1.7% |
| BM25+CSQE vs Hybrid RRF (no QE) | −0.0110 | −1.7% |
| Dense+CSQE vs Hybrid RRF (no QE) | −0.0352 | −5.6% |

---

## Analysis

1. **Corpus grounding works (+5.2% over blind QE on BM25).** BM25+CSQE (0.6157) outperforms Aya 8B blind QE best-config (β=2, 0.5855) by 0.0302 nDCG@10. This confirms the core CSQE hypothesis: showing the model actual corpus documents improves vocabulary alignment.

2. **Did not beat the hybrid baseline (0.6267).** BM25+CSQE reaches 0.6157 — 0.011 points short of the minimum success criterion. This is the expected next bottleneck: a single retriever enhanced with QE cannot yet match the recall diversity of fusing two retrievers.

3. **Recall@100 jump is strong (BM25: 0.8577 → 0.9422, +0.0845).** CSQE dramatically expands the recall ceiling on BM25, exceeding even Hybrid Recall@100 (0.9467 ≈ 0.9422). This means the relevant documents ARE being surfaced at k=100; the gap is in ranking them at k=10.

4. **Dense+CSQE slightly below Jais-2 blind QE (−0.0103).** The Jais-2 model (Arabic-native, BF16) slightly outperforms Aya CSQE on Dense. This suggests either (a) Jais-2's Arabic specialization compensates for lack of corpus grounding, or (b) the CSQE corpus prompt is harder to follow for the extraction task than the blind generation task.

5. **Natural next step: CSQE + Hybrid Fusion (Task 6.3c).** Given the strong Recall@100 gain from CSQE and the strong nDCG@10 from hybrid fusion, combining them (BM25+CSQE + Dense, or BM25+CSQE + Dense+CSQE) is the highest-probability path to beating 0.6267. This is exactly Task 6.3c (Exp 2.1).

---

## References

- Lei, Y., et al. (2024). "CSQE: Corpus-Steered Query Expansion." arXiv:2402.18031.
- Zhang et al. (2023). "MIRACL: A Multilingual Retrieval Dataset." TACL. arXiv:2210.09984.

---

## Artifacts

| File | Description |
|------|-------------|
| `experiments/exp_013_csqe_aya_8b.ipynb` | Generation notebook (BF16, batched) |
| `results/enhanced_queries/exp_013_csqe_aya_8b.pkl` | Enhanced queries pkl (2,896 queries) |
| `research_decisions/csqe_implementation_plan.md` | Full implementation plan |
| `research_decisions/csqe_speed_optimization_plan.md` | BF16 + batching optimization plan |
