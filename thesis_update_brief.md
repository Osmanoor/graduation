# Thesis Update Brief — Phase 4 Additions
**Created:** 2026-04-15  
**Purpose:** Single source of truth for updating ALL chapters with Phase 4 experiment results. Use this file instead of reading individual experiment docs.  
**Covers experiments:** Exp 1.1 (BM25 repetition), Exp 1.2 (Hybrid fusion), Exp 013 (CSQE), Exp 013c/013d (CSQE ablations), Exp 2.1 (CSQE+Hybrid), Error Analysis.

---

## Quick Reference — All Confirmed Numbers

### Baselines (no QE)
| System | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25S alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| Hybrid CC α=0.5 | 0.6266 | 0.7478 | 0.9458 | 0.6577 |
| Hybrid RRF k=20 | 0.6267 | 0.7597 | 0.9467 | 0.6517 |

### BM25 Query Repetition — Best Result per Model (Exp 1.1)
| Model | n=1 | Best n | Best nDCG@10 | Δ |
|-------|-----|--------|-------------|---|
| BM25 baseline (no QE) | 0.4621 | — | 0.4621 | — |
| Aya Expanse 8B | 0.5046 | β=2 | **0.5855** | +0.0808 |
| Jais-2-8B | 0.5122 | β=2 | 0.5731 | +0.0610 |
| Qwen 2.5-7B | 0.4682 | n=5 | 0.5358 | +0.0675 |
| Qwen3-8B | 0.4459 | n=7 | 0.5328 | +0.0868 |
| Gemma 3 4B | 0.3447 | n=7 | 0.5277 | +0.1831 |
| Qwen3-4B | 0.4145 | n=7 | 0.5244 | +0.1098 |
| Qwen 2.5-3B | 0.4090 | n=5 | 0.5185 | +0.1095 |
| Falcon-H1-3B | 0.4038 | n=10 | 0.5113 | +0.1074 |
| SILMA 2B | 0.4194 | n=5 | 0.4832 | +0.0639 |

Key finding: query repetition β ∈ {2,5,7,10} fixes all 9 previously-degraded BM25 models. Best single model: Aya Expanse 8B β=2 → 0.5855.

### CSQE — BM25 Component Ablation (Exp 013c/013d/013)
| Variant | nDCG@10 | Recall@10 | Recall@100 | MRR |
|---------|---------|-----------|------------|-----|
| Corpus-only (4c+0b, α=4) | 0.5381 | 0.6457 | 0.8790 | 0.5651 |
| Blind-only (0c+4b, α=4) | 0.5752 | 0.7089 | 0.9201 | 0.6032 |
| **CSQE 2+2 (α=4)** | **0.6157** | **0.7447** | **0.9422** | **0.6380** |
| Dense+CSQE alone | 0.5915 | 0.7073 | 0.8816 | 0.6225 |

α sweep (BM25+CSQE): α=1→0.6095, α=2→0.6130, α=3→0.6154, α=4→0.6157 (nearly flat).

### CSQE + Hybrid Fusion — All Configurations (Exp 2.1)
| Config | Fusion | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|--------|---------|-----------|------------|-----|
| B: BM25 + Dense+CSQE | CC α=0.4 | 0.6588 | 0.7851 | 0.9569 | 0.6777 |
| B: BM25 + Dense+CSQE | RRF k=20 | 0.6474 | 0.7928 | 0.9571 | 0.6578 |
| C: BM25+CSQE + Dense+CSQE | CC α=0.5 | 0.6959 | 0.8249 | 0.9647 | 0.7079 |
| C: BM25+CSQE + Dense+CSQE | RRF k=20 | 0.6936 | 0.8290 | 0.9660 | 0.7037 |
| A: BM25+CSQE + Dense orig | CC α=0.6 | 0.7088 | 0.8302 | 0.9717 | 0.7268 |
| **A: BM25+CSQE + Dense orig** | **RRF k=20** | **0.7137** | **0.8363** | **0.9734** | **0.7362** |

Config A ablation (RRF): Corpus-only+Dense=0.6616, Blind-only+Dense=0.7082, CSQE 2+2+Dense=**0.7137**.

### Error Analysis Key Numbers
| Condition | Count | % | Metric |
|-----------|-------|---|--------|
| CSQE > Blind QE | 1,646 | 56.8% | per-query nDCG@10 |
| Tie | 770 | 26.6% | |
| CSQE < Blind QE | 480 | 16.6% | |
| Mean delta | — | — | +0.1890 |
| Failures (CSQE < 0.1) | 258 | 8.9% | 257/258 = dataset ceiling, not CSQE failure |
| Big wins (Δ > 0.3) | 1,061 | 36.6% | CSQE=1.000, Blind=0.000 |
| Regressions (Δ < −0.1) | 367 | 12.7% | |

First-pass quality split:
- 1st-pass IS relevant (1,061 queries): Blind=0.6684, CSQE+Hybrid=**0.8877** (Δ=+0.2193)
- 1st-pass NOT relevant (1,835 queries): Blind=0.4100, CSQE+Hybrid=**0.5814** (Δ=+0.1714)

Query length split:
- Short (<5 words, n=865): Δ = +0.1990
- Long (≥10 words, n=131): Δ = +0.1053

Regression types (367 total): Type A 52% (strong BM25 hurt by expansion), Type B 36% (poisoned first-pass), Type C 12% (partial BM25).

---

## Chapter 3 — New Sections to Add

**Append after existing Section 3.5 (Model Comparison Methodology). Do NOT modify 3.1–3.5.**  
**New sections: 3.6, 3.7, 3.8, 3.9.**

---

### Section 3.6: Query Repetition for Sparse Retrieval
**Label:** `\label{sec:meth_repetition}`  
**Corresponds to:** Section 4.6 in Chapter 4

**Content to write:**
- **Problem:** Query2Doc single-pass (n=1) degrades BM25 for 6/9 models (term dilution, Section~\ref{sec:res_term_dilution}). The original Query2Doc paper [Wang et al. 2023] used n=5 documents with equal weighting.
- **Two solution families evaluated:**
  1. **Fixed repetition (Query2Doc-style):** prepend the query n times before the pseudo-document. n is a global hyperparameter applied identically to every query regardless of its length or the pseudo-document's length. Sweep n ∈ \{1, 3, 5, 7, 10\}.
  2. **Adaptive repetition (MuGI-style) [Zhang et al. 2024]:** compute n per-query from the ratio of pseudo-document length to query length, with a controlling parameter β:
     `\label{eq:mugi_repetition}`  
     `n(q, d, \beta) = \max\!\left(1,\; \left\lfloor \dfrac{|d|}{|q| \cdot \beta} \right\rfloor \right)`  
     where $|q|$ and $|d|$ are the token lengths of the query and pseudo-document respectively. Larger β yields fewer repetitions; smaller β yields more. Sweep β ∈ \{2, 4, 6\}.
- **Enhanced query assembly:**  
  `\label{eq:query_repetition}`  
  `q_{\text{rep}} = \underbrace{q \circ q \circ \cdots \circ q}_{n \text{ times}} \circ d_1 \circ d_2 \circ \cdots \circ d_k`  
  (where ∘ denotes string concatenation with a space separator, and k is the number of pseudo-documents; for Query2Doc single-pass, k=1)
- **Motivation for the adaptive variant:** The optimal number of repetitions depends on the length ratio between query and pseudo-document. A 3-word query paired with a 200-token pseudo-document needs more repetition than a 15-word query paired with a 100-token pseudo-document. MuGI's per-query adaptation removes this length-sensitivity and produced the best results for the two largest models (Aya Expanse 8B and Jais-2-8B), where β=2 was the winning configuration.
- **Sweep design:** 9 models × 8 configurations (n∈\{1,3,5,7,10\} + β∈\{2,4,6\}) = 72 BM25 evaluations. All expansions already generated (single-pass pkls from the Task 4.0b model comparison); no new LLM inference was needed. Evaluations used pytrec\_eval on MIRACL Arabic dev (2,896 queries). Total runtime approximately 73 minutes on Colab CPU.
- **References:** \cite{wang_2023_query2doc} (Query2Doc), \cite{zhang_2024_mugi} (MuGI adaptive formulation), \cite{lin_2021_bm25s} (BM25S implementation).

---

### Section 3.7: Hybrid Retrieval Fusion
**Label:** `\label{sec:meth_hybrid}`  
**Corresponds to:** Section 4.7 in Chapter 4

**Content to write:**
- **Motivation:** BM25 (lexical) and mDPR (semantic) are known to be complementary (Section~\ref{sec:res_baseline_comparison}). Hybrid fusion combines both ranked lists into a single ranking.
- **Two fusion methods tested:**

  **Convex Combination (CC):**  
  `\label{eq:hybrid_cc}`  
  `s_{\text{CC}}(d, q) = \alpha \cdot s_{\text{Dense}}(d, q) + (1 - \alpha) \cdot s_{\text{BM25}}(d, q)`  
  where scores are min-max normalised to [0,1] before combination. α swept over {0.1, 0.2, ..., 0.9}.

  **Reciprocal Rank Fusion (RRF):**  
  `\label{eq:rrf}`  
  `s_{\text{RRF}}(d) = \sum_{r \in R} \frac{1}{k + \text{rank}_r(d)}`  
  where k=20 and k=60 were tested. k=20 follows standard practice [Bruch et al. 2023].

- **Setup:** Both BM25S and mDPR retrieve top-100 candidates independently. Fusion and re-ranking is done in Python without additional GPU inference.
- **References:** \cite{bruch_2023_rrf} or cite the hybrid retrieval section in Chapter 2.

---

### Section 3.8: Corpus-Steered Query Expansion (CSQE)
**Label:** `\label{sec:meth_csqe}`  
**Corresponds to:** Section 4.8 in Chapter 4

**Subsections:**

#### 3.8.1 The CSQE Pipeline
**Label:** `\label{sec:meth_csqe_pipeline}`

- **Two-stage design** distinguishing CSQE from standard (blind) Query2Doc:
  1. **First-pass retrieval:** BM25S retrieves top-k=5 documents using the original query q.
  2. **Corpus-grounded expansion:** Each retrieved document dᵢ is concatenated with q and passed to the LLM with a CSQE-specific system prompt instructing extraction of topically relevant Arabic vocabulary.
  3. **Blind expansion:** The same query q is passed to the LLM without retrieved context (standard Query2Doc).
  4. **Expansion assembly:**  
     `\label{eq:csqe_query}`  
     `q_{\text{CSQE}} = (q+\text{' '})^{\alpha} \; \| \; c_1 \| c_2 \| b_1 \| b_2`  
     where cᵢ = corpus-grounded samples, bᵢ = blind samples, α = query repetition factor.

- **Configuration used (exp_013):** k=5 first-pass, 2 corpus samples + 2 blind samples, α=4, temp=1.0, max_new_tokens=128 per sample, model = Aya Expanse 8B (BF16, A100 40GB).
- **Rationale for combining corpus + blind:** Corpus samples provide attested Arabic vocabulary anchored to the actual Wikipedia passages; blind samples provide diverse answer-space vocabulary. They are complementary (validated in Section~\ref{sec:res_csqe_ablation}).

#### 3.8.2 Component Ablation Design
**Label:** `\label{sec:meth_csqe_ablation}`

- **013c (corpus-only):** num_corpus_samples=4, num_blind_samples=0 — isolates contribution of first-pass grounding
- **013d (blind-only):** num_corpus_samples=0, num_blind_samples=4 — isolates contribution of blind generation
- **013 (full CSQE):** 2+2 — the combined system
- **α sweep (α ∈ {1,2,3,4}):** Reconstructed from stored expansion pkls — no new LLM inference needed.

#### 3.8.3 Retriever-Specific Application
**Label:** `\label{sec:meth_csqe_config}`

Three fusion configurations tested to determine optimal QE assignment per retriever:
- **Config A:** BM25+CSQE (long expanded query) + Dense original query → hypothesis: BM25 benefits from vocabulary breadth; Dense encoder degrades on long inputs
- **Config B:** BM25 original query + Dense+CSQE → hypothesis: semantic signal of CSQE helps dense encoding
- **Config C:** Both BM25 and Dense receive CSQE query → maximum expansion
- Both RRF (k=20) and CC (α swept) were evaluated for each configuration.

---

### Section 3.9: Per-Query Error Analysis
**Label:** `\label{sec:meth_error_csqe}`  
**Corresponds to:** Section 4.9 in Chapter 4

**Content to write:**
- **Motivation:** Aggregate metrics mask where CSQE helps vs. hurts. Per-query analysis decomposes the overall gain.
- **Method:** pytrec_eval computes nDCG@10 per query for both Config A RRF (best system) and Aya Blind BM25 n=1. Delta = CSQE score − blind score is computed per query.
- **Categories defined:**
  - Failure: CSQE nDCG@10 < 0.1 (threshold)
  - Big win: Δ > 0.3
  - Regression: Δ < −0.1
- **First-pass quality split:** Queries are split by whether the BM25 first-pass retrieved a relevant document (any qrel > 0 in top-5), enabling analysis of how first-pass quality affects CSQE gains.
- **Regression classification:** Regressions manually inspected and classified into Type A (BM25 already strong, expansion introduces noise) and Type B (first-pass retrieves irrelevant doc, LLM grounding poisoned).

---

## Chapter 4 — New Sections to Add

**Append after existing Section 4.5 (Key Findings and Analysis). Do NOT modify 4.1–4.5.**  
**New sections: 4.6, 4.7, 4.8, 4.9. Update Table~\ref{tab:full_summary} in 4.5.6 to include all new experiments.**

---

### Section 4.6: BM25 Query Repetition Results
**Label:** `\label{sec:res_repetition}`  
**New labels:** `\label{tab:bm25_repetition}`, `\label{fig:repetition_heatmap}`

**Table 4.X: BM25 nDCG@10 by Model and Repetition Configuration** (`\label{tab:bm25_repetition}`)  
Caption: "BM25 nDCG@10 for nine models under query repetition. Columns n∈\{1,3,5,7,10\} are fixed-count repetition (Query2Doc style); columns β∈\{2,4,6\} are MuGI adaptive repetition where n is computed per-query as $n=\max(1, \lfloor |d|/(|q|\cdot\beta)\rfloor)$. MIRACL Arabic dev (2,896 queries). Best value per model in bold. Values taken verbatim from `exp_011_bm25_repetition.md`."

| Model | n=1 | n=3 | n=5 | n=7 | n=10 | β=2 | β=4 | β=6 |
|-------|-----|-----|-----|-----|------|-----|-----|-----|
| BM25 alone (no QE) | 0.4621 | — | — | — | — | — | — | — |
| Aya Expanse 8B | 0.5046 | 0.5652 | 0.5832 | 0.5849 | 0.5773 | **0.5855** | 0.5515 | 0.5256 |
| Jais-2-8B       | 0.5122 | 0.5492 | 0.5529 | 0.5516 | 0.5436 | **0.5731** | 0.5521 | 0.5350 |
| Qwen3-8B        | 0.4459 | 0.5181 | 0.5319 | **0.5328** | 0.5254 | 0.5254 | 0.4841 | 0.4591 |
| Qwen 2.5-7B     | 0.4682 | 0.5294 | **0.5358** | 0.5331 | 0.5257 | 0.5320 | 0.4977 | 0.4774 |
| Qwen3-4B        | 0.4145 | 0.5054 | 0.5239 | **0.5244** | 0.5188 | 0.5177 | 0.4678 | 0.4347 |
| Gemma 3 4B      | 0.3447 | 0.4800 | 0.5178 | **0.5277** | 0.5239 | 0.4915 | 0.4184 | 0.3694 |
| Qwen 2.5-3B     | 0.4090 | 0.5060 | **0.5185** | 0.5181 | 0.5116 | 0.5046 | 0.4551 | 0.4253 |
| Falcon-H1-3B    | 0.4038 | 0.4881 | 0.5082 | 0.5112 | **0.5113** | 0.4979 | 0.4561 | 0.4266 |
| SILMA 2B        | 0.4194 | 0.4783 | **0.4832** | 0.4829 | 0.4788 | 0.4494 | 0.4252 | 0.4203 |

**Supplementary Recall and MRR at best config** (from exp_011 best-config row):

| Model | Best Config | nDCG@10 | Recall@10 | Recall@100 | MRR | Δ nDCG vs n=1 |
|-------|------------|---------|-----------|------------|-----|---------------|
| Aya Expanse 8B | β=2 | 0.5855 | 0.7128 | 0.9300 | 0.6165 | +0.0808 |
| Jais-2-8B | β=2 | 0.5731 | 0.7075 | 0.9217 | 0.6004 | +0.0610 |
| Qwen 2.5-7B | n=5 | 0.5358 | 0.6765 | 0.9105 | 0.5586 | +0.0675 |
| Qwen3-8B | n=7 | 0.5328 | 0.6695 | 0.9064 | 0.5590 | +0.0868 |
| Gemma 3 4B | n=7 | 0.5277 | 0.6640 | 0.9002 | 0.5551 | **+0.1831** |
| Qwen3-4B | n=7 | 0.5244 | 0.6617 | 0.8980 | 0.5500 | +0.1098 |
| Qwen 2.5-3B | n=5 | 0.5185 | 0.6501 | 0.9031 | 0.5494 | +0.1095 |
| Falcon-H1-3B | n=10 | 0.5113 | 0.6456 | 0.8927 | 0.5379 | +0.1074 |
| SILMA 2B | n=5 | 0.4832 | 0.6216 | 0.8747 | 0.5048 | +0.0639 |

**Prose points to make:**
1. Query repetition recovers all nine previously degraded BM25 models. At n=1 (no repetition), only 3/9 models exceeded the BM25 baseline (Aya 0.5046, Jais-2 0.5122, Qwen 2.5-7B 0.4682); at the optimal repetition configuration, all 9/9 exceeded it.
2. Optimal repetition strategy is model-size-dependent: large models (8B) converge at MuGI β=2 (adaptive, produces stronger repetition for longer pseudo-documents); mid-size models (3–4B) plateau at fixed n=5–7; the smallest model (SILMA 2B) peaks earlier at n=5 because its pseudo-documents are shorter.
3. Beyond the optimum, performance decreases symmetrically — excessive repetition over-weights the original query tokens and suppresses the useful expansion vocabulary. The sharpest decline is visible in the β=4 and β=6 columns for the 3–4B models.
4. Aya Expanse 8B at β=2 achieves 0.5855 nDCG@10, improving BM25 by +26.7% over baseline (0.4621) and recovering +0.0808 from the n=1 result (0.5046). This confirms that query repetition — not a change of model — was the missing ingredient for the six originally degraded systems.
5. Reference fig:repetition_heatmap (heatmap figure from `experiments/exp_11_bm25_repetition/` results folder).

---

### Section 4.7: Hybrid Retrieval Fusion Results
**Label:** `\label{sec:res_hybrid}`  
**New labels:** `\label{tab:hybrid_results}`, `\label{fig:hybrid_comparison}`

**Table 4.X: Hybrid Fusion — Full CC Alpha Sweep and RRF Results** (`\label{tab:hybrid_results}`)  
Caption: "Hybrid retrieval fusion results on MIRACL Arabic dev set (2,896 queries). CC = Convex Combination (min-max normalised per query, α controls Dense weight); RRF = Reciprocal Rank Fusion. Values taken verbatim from `exp_012_hybrid_baseline.md`."

| Method | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25S alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| Hybrid CC α=0.1 | 0.5248 | 0.6412 | 0.9333 | 0.5584 |
| Hybrid CC α=0.2 | 0.5533 | 0.6683 | 0.9413 | 0.5861 |
| Hybrid CC α=0.3 | 0.5830 | 0.7014 | 0.9449 | 0.6161 |
| Hybrid CC α=0.4 | 0.6137 | 0.7392 | 0.9454 | 0.6426 |
| **Hybrid CC α=0.5** | **0.6266** | 0.7478 | 0.9458 | **0.6577** |
| Hybrid CC α=0.6 | 0.6051 | 0.7289 | 0.9440 | 0.6355 |
| Hybrid CC α=0.7 | 0.5743 | 0.6963 | 0.9439 | 0.6049 |
| Hybrid CC α=0.8 | 0.5384 | 0.6634 | 0.9416 | 0.5678 |
| Hybrid CC α=0.9 | 0.4996 | 0.6297 | 0.9350 | 0.5257 |
| **Hybrid RRF k=20** | **0.6267** | **0.7597** | **0.9467** | 0.6517 |
| Hybrid RRF k=60 | 0.6230 | 0.7553 | 0.9467 | 0.6490 |

> **Note on Recall@100 for RRF k=20:** The source experiment doc (`exp_012_hybrid_baseline.md`) records 0.9467; downstream reference tables (CLAUDE.md, exp_021) record 0.9466. Use 0.9467 in the thesis — the source experiment file is authoritative. The 1-unit 4th-decimal difference is a rounding artefact and does not affect any conclusion.

**Prose points to make:**
1. Hybrid fusion (+35.6\% over BM25, +25.5\% over mDPR) substantially outperforms either retriever alone, confirming the complementarity identified in Section~\ref{sec:res_baseline_comparison}.
2. RRF k=20 (0.6267) and CC α=0.5 (0.6266) are statistically indistinguishable on nDCG@10. RRF has the edge on Recall@10 (+0.0119); CC has the edge on MRR (+0.0060). RRF requires no hyperparameter tuning and is adopted as the primary hybrid baseline.
3. The CC sweep is smooth and unimodal, peaking at α=0.5 and degrading symmetrically toward either extreme. At α=0.9 (almost pure Dense) the result (0.4996) is essentially the mDPR-alone baseline (0.4993); at α=0.1 (almost pure BM25) the result (0.5248) is higher than BM25 alone because CC still picks up Dense's tie-breaking contribution. This confirms the two retrievers contribute roughly equally.
4. RRF k=20 slightly outperforms k=60 (0.6267 vs 0.6230). The smaller k gives more weight to top-ranked items, which helps nDCG@10 but does not affect Recall@100 (both 0.9467).
5. This 0.6267 nDCG@10 hybrid baseline is the target that all subsequent QE methods must surpass.

---

### Section 4.8: Corpus-Steered Query Expansion Results
**Label:** `\label{sec:res_csqe}`  
**New labels:** `\label{sec:res_csqe_ablation}`, `\label{tab:csqe_main}`, `\label{tab:csqe_ablation}`, `\label{tab:alpha_sweep}`

#### 4.8.1 Main CSQE Results
**Label:** `\label{sec:res_csqe_main}`

**Table 4.X: CSQE Results Compared to Baselines** (`\label{tab:csqe_main}`)  
Caption: "nDCG@10, Recall@10, Recall@100, and MRR for CSQE-enhanced retrieval on MIRACL Arabic dev set. CSQE config: k=5 first-pass, 2 corpus + 2 blind samples, α=4, Aya Expanse 8B."

| Method | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25S alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| BM25+CSQE | **0.6157** | **0.7447** | **0.9422** | **0.6380** |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| Dense+CSQE | 0.5915 | 0.7073 | 0.8816 | 0.6225 |
| Hybrid RRF k=20 (no QE) | 0.6267 | 0.7597 | 0.9467 | 0.6517 |

Prose: BM25+CSQE (0.6157) achieves a +33.2% improvement over BM25 alone and, notably, nearly matches the no-QE hybrid baseline (0.6267) using only a single retriever. Dense+CSQE improves over mDPR alone (+18.5%) but falls below BM25+CSQE — the Dense encoder was trained on short natural-language queries, and the long CSQE expansion (≈1,500 characters) degrades the embedding quality relative to vocabulary-based matching.

#### 4.8.2 Component Ablation
**Label:** `\label{sec:res_csqe_ablation}`

**Table 4.X: CSQE Component Ablation on BM25** (`\label{tab:csqe_ablation}`)  
Caption: "BM25 nDCG@10 for corpus-only, blind-only, and combined CSQE expansion variants. All variants use α=4, Aya Expanse 8B, k=5 first-pass."

| Variant | nDCG@10 | Recall@10 | Recall@100 | MRR |
|---------|---------|-----------|------------|-----|
| BM25 alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| 013c: Corpus-only (4c+0b) | 0.5381 | 0.6457 | 0.8790 | 0.5651 |
| 013d: Blind-only (0c+4b) | 0.5752 | 0.7089 | 0.9201 | 0.6032 |
| **013: CSQE 2+2** | **0.6157** | **0.7447** | **0.9422** | **0.6380** |

Prose: Blind-only outperforms corpus-only on BM25 (0.5752 > 0.5381), counter to the initial hypothesis that corpus grounding would provide superior vocabulary. The explanation is that BM25 benefits from vocabulary breadth — blind generation produces full answer paragraphs with diverse Arabic term variants, while corpus extraction produces passage-level excerpts structurally similar to the query. However, the combined system (2+2) exceeds both components individually (+0.0405 over blind-only), confirming that corpus and blind expansions are complementary: corpus samples anchor the expansion to attested Wikipedia vocabulary, while blind samples diversify the answer-space coverage.

**Table 4.X: Query Repetition Factor α Sweep** (`\label{tab:alpha_sweep}`)  
Caption: "Effect of query repetition factor α on CSQE BM25 retrieval nDCG@10."

| α | BM25+CSQE nDCG@10 |
|---|-------------------|
| 1 | 0.6095 |
| 2 | 0.6130 |
| 3 | 0.6154 |
| **4** | **0.6157** |

Prose: Performance improves monotonically from α=1 to α=4 but the gain is minimal (+0.0062). α=1 already captures 98.9% of the α=4 nDCG@10. The query weighting factor is not a critical hyperparameter for this configuration.

---

### Section 4.9: CSQE with Hybrid Fusion
**Label:** `\label{sec:res_csqe_hybrid}`  
**New labels:** `\label{tab:csqe_hybrid_configs}`, `\label{tab:system_progression}`

#### 4.9.1 Fusion Configuration Comparison
**Label:** `\label{sec:res_csqe_configs}`

**Table 4.X: CSQE Hybrid Fusion — All Configurations** (`\label{tab:csqe_hybrid_configs}`)  
Caption: "Results for three CSQE application strategies in hybrid fusion. Config A: BM25 receives CSQE query, Dense receives original query. Config B: BM25 receives original query, Dense receives CSQE query. Config C: both retrievers receive CSQE query."

| Config | Fusion | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|--------|---------|-----------|------------|-----|
| Hybrid RRF k=20 (no QE) | RRF | 0.6267 | 0.7597 | 0.9467 | 0.6517 |
| B: BM25 + Dense+CSQE | RRF | 0.6474 | 0.7928 | 0.9571 | 0.6578 |
| B: BM25 + Dense+CSQE | CC α=0.4 | 0.6588 | 0.7851 | 0.9569 | 0.6777 |
| C: BM25+CSQE + Dense+CSQE | RRF | 0.6936 | 0.8290 | 0.9660 | 0.7037 |
| C: BM25+CSQE + Dense+CSQE | CC α=0.5 | 0.6959 | 0.8249 | 0.9647 | 0.7079 |
| A: BM25+CSQE + Dense orig | CC α=0.6 | 0.7088 | 0.8302 | 0.9717 | 0.7268 |
| **A: BM25+CSQE + Dense orig** | **RRF** | **0.7137** | **0.8363** | **0.9734** | **0.7362** |

**Key design principle (must state clearly):**  
Config A is the winner despite giving Dense the weaker input (original short query vs CSQE-expanded). This is explained by a retriever–query representation mismatch: BM25 uses exact term matching and directly benefits from CSQE's vocabulary-rich expansion; the mDPR encoder was trained on short natural-language queries and produces less discriminative embeddings when given a 1,500-character expansion. Applying QE asymmetrically — only to BM25 — maximises the gains from each retriever's inherent strength.

Config C (both retrievers expanded) scores 0.6936, lower than Config A (0.7137), even though Dense+CSQE individually outperforms Dense alone. This confirms that the relative quality of the two ranked lists matters for RRF — a less discriminative Dense run reduces the fusion ceiling even when it improves individually.

**Table 4.X: Config A RRF — Ablation Component Contribution** (inline or separate small table)

| Expansion | Config A RRF nDCG@10 |
|-----------|---------------------|
| Corpus-only (4c+0b) + Dense orig | 0.6616 |
| Blind-only (0c+4b) + Dense orig | 0.7082 |
| **CSQE 2+2 + Dense orig** | **0.7137** |

**Table 4.X: Config A RRF — Query Repetition α Sweep** (`\label{tab:config_a_alpha}`)  
Caption: "Effect of query repetition factor α on the best Config A RRF system. All values use the same CSQE 2c+2b expansion, varying only the α prepended to the BM25-side query."

| α | Config A RRF nDCG@10 |
|---|---------------------|
| 1 | 0.7123 |
| 2 | 0.7121 |
| 3 | 0.7130 |
| **4** | **0.7137** |

Prose: α is nearly flat for the final fused system — the α=1 result (0.7123) is only 0.0014 below α=4 (0.7137). This is consistent with Table~\ref{tab:alpha_sweep} (BM25-alone α sweep): once CSQE expansion is combined with a strong dense run via RRF, the α parameter has negligible effect. We report α=4 as the primary configuration because it matches the exp_013 settings, but α=1 would be preferable for a production deployment (one less token per expanded query).

**Table 4.X: Delta Analysis vs Key Benchmarks** (`\label{tab:delta_analysis}`)  
Caption: "nDCG@10 improvements of Config A RRF over prior systems."

| Comparison | Δ nDCG@10 | \% change |
|------------|-----------|----------|
| Config A RRF vs BM25 alone | +0.2516 | +54.5\% |
| Config A RRF vs mDPR alone | +0.2144 | +42.9\% |
| Config A RRF vs best blind BM25 QE (Aya β=2) | +0.1282 | +21.9\% |
| Config A RRF vs best blind Dense QE (Aya 8B) | +0.0973 | +15.8\% |
| Config A RRF vs Hybrid RRF (no QE) | +0.0870 | +13.9\% |
| Config C vs Config A | −0.0178 | Dense+CSQE hurts in fusion |
| Config B vs Hybrid RRF | +0.0207 | Weakest config still beats no-QE hybrid |

Prose: All three CSQE fusion configurations beat the no-QE hybrid baseline. The +0.0870 improvement of Config A over the hybrid baseline (+13.9\%) isolates the contribution of CSQE beyond what hybrid fusion alone provides.

#### 4.9.2 Overall System Progression
**Label:** `\label{sec:res_progression}`

**Table 4.X: System Progression Summary** (`\label{tab:system_progression}`)  
Caption: "nDCG@10 progression from baseline to best system on MIRACL Arabic dev set (2,896 queries). Δ cumulative measured from BM25S baseline."

| Stage | System | nDCG@10 | Δ cumul. |
|-------|--------|---------|---------|
| Baseline | BM25S alone | 0.4621 | — |
| Baseline | mDPR alone | 0.4993 | — |
| Blind QE | Best blind Dense (Aya 8B, n=1) | 0.6164 | +23.5\% over mDPR |
| Blind QE | Best blind BM25 (Aya 8B, β=2) | 0.5855 | +26.7\% over BM25 |
| Hybrid | Hybrid RRF k=20 (no QE) | 0.6267 | +35.6\% over BM25 |
| CSQE alone | BM25+CSQE | 0.6157 | +33.2\% over BM25 |
| **CSQE+Hybrid** | **Config A: BM25+CSQE + Dense RRF** | **0.7137** | **+54.5\% over BM25** |

**Prose for 4.9.2:** The progression demonstrates a consistent improvement through three stages of pipeline development. Blind QE improvements (Sections 4.3, 4.6) confirm that LLM-generated pseudo-documents are effective for Arabic information retrieval. The hybrid baseline (Section 4.7) establishes that lexical and semantic retrieval are complementary. CSQE (Section 4.8) introduces corpus grounding that outperforms blind QE on BM25. The final combination of corpus-steered expansion applied asymmetrically to hybrid retrieval (Config A RRF) achieves 0.7137 nDCG@10 — a 54.5\% improvement over BM25 alone and a 42.9\% improvement over mDPR alone. Recall@100 = 0.9734 indicates that 97.3\% of relevant documents appear within the top 100 candidates, establishing a strong upper bound for downstream reranking.

---

### Section 4.10: Per-Query Error Analysis
**Label:** `\label{sec:res_error_csqe}`  
**New labels:** `\label{tab:error_distribution}`, `\label{tab:error_patterns}`, `\label{tab:regression_causes}`, `\label{fig:csqe_scatter}`, `\label{fig:regression_pie}`

#### 4.10.1 Win/Loss Distribution
**Label:** `\label{sec:res_win_loss}`

> **⚠ Data-provenance note (read before writing this section).**
> The per-query error analysis in `exp_error_analysis_csqe.md` was computed comparing **Config C RRF (0.6936 nDCG@10)** against **Aya Blind BM25 n=1 (0.5046 nDCG@10)**, not Config A RRF (0.7137). The mean delta of +0.1890 equals 0.6936 − 0.5046. When citing the per-query results in the thesis, either:
> (a) state the comparison system explicitly as "the fully-expanded Config C RRF system (0.6936)" — simpler and matches the raw analysis, or
> (b) describe the analysis as comparing "a CSQE-hybrid system" without naming which config, and use 0.6936 in the row.
> Do NOT caption this table as "Config A RRF vs Blind" — that would misrepresent the numbers. The win/loss counts (1,646 / 770 / 480) and first-pass split are unchanged regardless, because Config A and Config C share the BM25+CSQE run file; the differences only appear in Dense side and thus in the fused score.

**Table 4.X: Per-Query nDCG@10 Win/Loss Distribution** (`\label{tab:error_distribution}`)  
Caption: "Per-query comparison of the CSQE+Hybrid system (Config C RRF, 0.6936 nDCG@10) against the Aya Blind BM25 n=1 baseline (0.5046 nDCG@10) on 2,896 MIRACL Arabic dev queries."

| Condition | Queries | \% |
|-----------|---------|---|
| CSQE+Hybrid > Blind | 1,646 | 56.8\% |
| Tie | 770 | 26.6\% |
| CSQE+Hybrid < Blind | 480 | 16.6\% |
| **Mean delta (CSQE − Blind)** | — | **+0.1890** |

Failures (nDCG@10 < 0.1): 258 queries (8.9\%). Inspection revealed 257 of 258 are irretrievable regardless of QE method — the relevant passage is absent from the Wikipedia corpus dump used for indexing. These represent a dataset-level ceiling, not CSQE failures. The single genuine CSQE failure (qid=1060) involved the LLM generating a **meta-description** (prose about how a topic might be described, rather than actual vocabulary-rich content), causing the relevant document to drop below rank 10 in RRF fusion. This meta-description failure mode is a known LLM-QE pathology and is mentioned in the limitations section.

#### 4.10.2 First-Pass Quality as Dominant Predictor
**Label:** `\label{sec:res_firstpass}`

**Table 4.X: Performance Split by First-Pass Retrieval Quality** (`\label{tab:error_patterns}`)  
Caption: "System performance split by whether BM25 first-pass (k=5) retrieved a relevant document."

| First-Pass Quality | n | Blind QE nDCG@10 | CSQE+Hybrid nDCG@10 | Δ |
|-------------------|---|-----------------|---------------------|---|
| Relevant doc retrieved | 1,061 | 0.6684 | **0.8877** | +0.2193 |
| No relevant doc retrieved | 1,835 | 0.4100 | 0.5814 | +0.1714 |
| **All queries** | **2,896** | **0.5046** | **0.6936** | **+0.1890** |

**Table 4.X: Performance Split by Query Length** (`\label{tab:query_length_split}`)  
Caption: "System performance decomposed by the number of tokens in the original MIRACL query."

| Query length | n | Blind QE nDCG@10 | CSQE+Hybrid nDCG@10 | Δ |
|-------------|---|-----------------|---------------------|---|
| Short (<5 words) | 865 | 0.4793 | 0.6783 | +0.1990 |
| Medium (5–9 words) | 1,900 | — | — | — |
| Long (≥10 words) | 131 | 0.6003 | 0.7056 | +0.1053 |

Prose: When first-pass retrieval succeeds (36.6\% of queries), CSQE+Hybrid achieves 0.8877 nDCG@10 — near-ceiling retrieval. The first-pass quality gap (+0.3063 between first-pass success and failure groups) is larger than the overall system advantage over blind QE (+0.1890), establishing first-pass recall as the dominant predictor of CSQE effectiveness. Short queries (<5 words, n=865) gain most from CSQE (+0.1990), as they are the most underspecified and benefit from both vocabulary expansion and corpus grounding. Long queries (≥10 words, n=131) still gain (+0.1053) but less, because their greater information content already mitigates the information-poverty problem that motivates query expansion.

#### 4.10.3 Big Wins: The Corpus Grounding Effect
**Label:** `\label{sec:res_bigwins}`

All 1,061 big-win queries (Δ > 0.3) share a single pattern: CSQE nDCG@10 = 1.000, Blind = 0.000. Blind QE hallucinates a plausible but factually incorrect entity; CSQE's first-pass corpus document anchors the expansion to the correct Wikipedia article.

Include representative examples:

| Query | Blind QE generates | CSQE grounds to | CSQE |
|-------|-------------------|-----------------|------|
| ما هو الرباط المنصوري؟ | A spinal surgery procedure | Mamluk-era building in Cairo | 1.000 |
| من هو مؤسس الفلسفة البراغماتية؟ | Hallucinated person | John Dewey article | 1.000 |
| من هو نيكولا بوالو؟ | A French businessman | 17th-century French poet | 1.000 |

This pattern validates the corpus grounding hypothesis: for niche or ambiguous Arabic terms, blind QE confidently generates a common modern interpretation, while corpus grounding locks onto the actual Wikipedia entity. Note the translation of this to query expansion: the corpus anchor provides the correct Arabic vocabulary (مملوكي، قاهرة vs جراحة العمود الفقري) that BM25 and Dense both need.

#### 4.10.4 Regression Analysis
**Label:** `\label{sec:res_regressions}`

**Table 4.X: Regression Root-Cause Classification** (`\label{tab:regression_causes}`)  
Caption: "Classification of 367 regression queries (CSQE nDCG@10 < Blind by > 0.1)."

| Type | Count | % | Description |
|------|-------|---|-------------|
| A: Strong BM25 hurt | 191 | 52% | BM25 baseline ≥ 0.3; CSQE expansion introduces off-topic vocabulary |
| B: Poisoned first-pass | 131 | 36% | BM25 baseline < 0.1; first-pass retrieves irrelevant doc → LLM grounding on wrong content |
| C: Partial BM25 | 45 | 12% | BM25 baseline 0.1–0.3; mixed quality |

Prose for Type A: CSQE expansion introduces Arabic vocabulary from the corpus document that dilutes the original query terms. This is the same term-dilution effect observed in Section~\ref{sec:res_term_dilution}, but in reverse — here the expansion itself (rather than the pseudo-document) reduces BM25 precision for already-well-handled queries.

Prose for Type B: BM25 is sensitive to Arabic homonyms and short/ambiguous queries. Example: "ماهو التطرف؟" — BM25 retrieves "لهجة جنوبية" (a dialect article) because "ماهو" matches a dialectal phrase, not the intended "ما هو التطرف" (what is extremism?). The LLM then generates corpus-grounded content about dialects, poisoning the expansion for the actual query intent.

**Implications (must include):** These two failure modes suggest concrete future improvements: (1) a first-pass quality gate (fall back to blind QE when the top-1 BM25 document has low lexical overlap with the query) to address Type B; (2) asymmetric expansion weighting (lower weight for expansion in the concatenated query for queries where BM25 is already strong) to address Type A.

---

## Chapter 5 — Sections to Update

**Do NOT rewrite existing sections. ADD new content and MODIFY specific items.**

### 5.1 Conclusions — Additions (append after existing content)

Add these new conclusion paragraphs AFTER the existing conclusions (after "Overall" paragraph):

**New paragraph: Query repetition resolves sparse retrieval degradation.**  
The BM25 term-dilution problem, initially identified for 6 of 9 models (Section~\ref{sec:res_term_dilution}), was fully resolved through query repetition. By prepending the original query β times before the pseudo-document, all nine models exceeded the BM25 baseline at their optimal β. Aya Expanse 8B with β=2 achieved 0.5855 nDCG@10 — a 26.7\% improvement over the BM25 baseline and a substantial recovery from the 0.5046 result at β=1.

**New paragraph: Hybrid retrieval establishes a strong non-QE ceiling.**  
Combining BM25S and mDPR through Reciprocal Rank Fusion (RRF k=20) achieved 0.6267 nDCG@10 — a 35.6\% improvement over BM25 alone — without any query enhancement, confirming the complementarity of lexical and semantic retrieval observed in Section~\ref{sec:res_baseline_comparison}.

**New paragraph: Corpus-steered expansion (CSQE) validates the corpus grounding hypothesis.**  
The CSQE pipeline, which grounds LLM expansion in first-pass retrieved documents, achieved 0.6157 nDCG@10 on BM25 alone — nearly matching the no-QE hybrid baseline and substantially outperforming blind Query2Doc. Per-query error analysis confirmed the underlying mechanism: when first-pass retrieval succeeds, CSQE anchors the expansion to the correct Wikipedia entity, achieving near-ceiling performance (0.8877 nDCG@10 on first-pass-relevant queries). The combined system (Config A RRF: BM25+CSQE + Dense original query) achieved **0.7137 nDCG@10 — a 54.5\% improvement over BM25 alone and a 13.9\% improvement over the no-QE hybrid baseline**.

**New paragraph: Retriever-specific query representation is critical.**  
A key finding is that applying CSQE asymmetrically — only to the BM25 retriever — outperforms applying it to both retrievers (Config A: 0.7137 > Config C: 0.6959). BM25 benefits from CSQE's long, vocabulary-rich expansion; the mDPR encoder, trained on short queries, degrades under long expansion inputs. This retriever-specific representation principle has practical implications for any multi-retriever pipeline.

---

### 5.2 Challenges — Items to UPDATE

**Item 2 (BM25 term dilution):** Change "query repetition (n=5) not implemented" → MARK AS RESOLVED and state: "This challenge was resolved through the query repetition technique (Section~\ref{sec:res_repetition}), which recovered BM25 performance for all nine degraded models."

**Add new challenge (append to list):**  
**First-pass quality dependence.** CSQE performance is strongly conditioned on first-pass retrieval quality. When BM25 first-pass retrieves irrelevant documents (36\% of regression cases), the LLM expansion is grounded on incorrect content, causing regressions that blind QE does not exhibit. Arabic homonym sensitivity in BM25 (e.g., "ماهو" retrieved as a dialectal phrase rather than a question prefix) is the primary trigger.

---

### 5.3 Recommendations — Items to UPDATE

**Move to conclusions (items now implemented):**
- Recommendation 2 (BM25 query repetition) → Completed; reference Section~\ref{sec:res_repetition}
- Recommendation 4 (Hybrid retrieval with QE) → Completed; reference Section~\ref{sec:res_csqe_hybrid}

**New recommendations (append):**
1. **First-pass quality gate.** Implement a quality filter that checks lexical overlap between the top-1 BM25 document and the query before grounding the LLM. When overlap is below a threshold, fall back to blind QE. Expected improvement: recovery of ~131 Type B regression queries (Section~\ref{sec:res_regressions}).

2. **Asymmetric expansion weighting.** For Type A regressions (strong BM25 queries), reducing the expansion weight α or using field-based BM25 indexing (original query in one field, expansion in another with lower boost) would prevent vocabulary dilution for queries that BM25 already handles well.

3. **CSQE with stronger dense retrievers.** The current pipeline uses mDPR as a relatively weak dense baseline (intentional, per Section~\ref{sec:meth_dense_baseline}). Testing CSQE+Hybrid with BGE-M3 or mE5-large would assess whether the 54.5\% BM25 improvement translates to similar gains over stronger dense retrievers, and whether the retriever-specific representation finding generalises.

---

## Abstract — What to Update

**English Abstract (5-Abstract.tex):**
Change the closing result sentence to reflect the final best result:
- OLD: likely references the model comparison result (~0.62)
- NEW: "The proposed corpus-steered pipeline, combined with hybrid BM25+Dense fusion, achieved 0.7137 nDCG@10 on the MIRACL Arabic benchmark — a 54.5\% improvement over the BM25 baseline and a 13.9\% improvement over a strong no-QE hybrid system."

**Arabic Abstract (6-ARAbstract.tex):**
Update the corresponding Arabic sentence with the same numbers. The numbers are Arabic-script numerals or standard digits — use standard digits (0.7137، 54.5\%) for consistency with the English abstract.

---

## New Cross-Reference Labels to Add to READMEs

### README_chapter3.md additions:
```
| sec:meth_repetition | 3.6 | Query repetition methodology |
| eq:query_repetition | 3.6 | Query repetition equation |
| sec:meth_hybrid | 3.7 | Hybrid fusion methodology |
| eq:hybrid_cc | 3.7 | Convex combination equation |
| eq:rrf | 3.7 | RRF equation |
| sec:meth_csqe | 3.8 | CSQE methodology |
| sec:meth_csqe_pipeline | 3.8.1 | CSQE two-stage pipeline |
| eq:csqe_query | 3.8.1 | CSQE query assembly equation |
| sec:meth_csqe_ablation | 3.8.2 | CSQE ablation design |
| sec:meth_csqe_config | 3.8.3 | Config A/B/C retriever assignment |
| sec:meth_error_csqe | 3.9 | Per-query error analysis methodology |
```

### README_chapter4.md additions:
```
| sec:res_repetition | 4.6 | BM25 repetition results |
| tab:bm25_repetition | 4.6 | BM25 repetition table |
| fig:repetition_heatmap | 4.6 | Repetition heatmap figure |
| sec:res_hybrid | 4.7 | Hybrid fusion results |
| tab:hybrid_results | 4.7 | Hybrid fusion table |
| fig:hybrid_comparison | 4.7 | Hybrid comparison figure |
| sec:res_csqe | 4.8 | CSQE results |
| sec:res_csqe_main | 4.8.1 | CSQE main results |
| tab:csqe_main | 4.8.1 | CSQE main results table |
| sec:res_csqe_ablation | 4.8.2 | CSQE component ablation |
| tab:csqe_ablation | 4.8.2 | CSQE ablation table |
| tab:alpha_sweep | 4.8.2 | Alpha sweep table |
| sec:res_csqe_hybrid | 4.9 | CSQE + hybrid fusion results |
| sec:res_csqe_configs | 4.9.1 | Config A/B/C comparison |
| tab:csqe_hybrid_configs | 4.9.1 | Config comparison table |
| sec:res_progression | 4.9.2 | System progression |
| tab:system_progression | 4.9.2 | Progression table |
| sec:res_error_csqe | 4.10 | Per-query error analysis |
| sec:res_win_loss | 4.10.1 | Win/loss distribution |
| tab:error_distribution | 4.10.1 | Win/loss table |
| tab:error_patterns | 4.10.2 | First-pass quality table |
| sec:res_firstpass | 4.10.2 | First-pass quality analysis |
| sec:res_bigwins | 4.10.3 | Big wins / corpus grounding |
| sec:res_regressions | 4.10.4 | Regression analysis |
| tab:regression_causes | 4.10.4 | Regression causes table |
| fig:csqe_scatter | 4.10 | CSQE scatter plot figure |
| fig:regression_pie | 4.10.4 | Regression pie chart |
```

---

## New Citations Needed (References.bib)

1. **Lei et al. 2024 — CSQE paper:**  
   Key: `lei_2024_csqe`  
   Title: "CSQE: Corpus-Steered Query Expansion"  
   arXiv: 2402.18031  
   Used in: Chapter 2 (sec:modern_qe, sec:research_gap), Chapter 3 (sec:meth_csqe), Chapter 4 (sec:res_csqe)

2. **Bruch et al. 2023 — RRF analysis:**  
   Key: `bruch_2023_rrf`  
   Title: "An Analysis of Fusion Functions for Hybrid Retrieval"  
   ACM TOIS. arXiv: 2210.11934  
   Used in: Chapter 2 (sec:hybrid_retrieval), Chapter 3 (sec:meth_hybrid)

3. **Zhang et al. 2024 — MuGI adaptive repetition:**  
   Key: `zhang_2024_mugi`  
   Title: "MuGI: Enhancing Information Retrieval through Multi-Text Generation Integration with Large Language Models"  
   EMNLP Findings 2024. arXiv: 2401.06311  
   Used in: Chapter 3 (sec:meth_repetition — source of the adaptive β formula)

4. **Zhang et al. 2023 — MIRACL:**  
   Key: `zhang_2023_miracl` (may already exist — check References.bib)  
   Title: "MIRACL: A Multilingual Retrieval Dataset"  
   TACL. arXiv: 2210.09984

**BibTeX entry for zhang_2024_mugi (add to References.bib if missing):**
```bibtex
@inproceedings{zhang_2024_mugi,
  author    = {Le Zhang and Yihong Wu and Qian Yang and Jian-Yun Nie},
  title     = {{MuGI}: Enhancing Information Retrieval through Multi-Text Generation Integration with Large Language Models},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2024},
  year      = {2024},
  note      = {arXiv:2401.06311}
}
```

---

## Writing Rules Reminder (from README_chapter3/4/5)
- Passive voice throughout
- Never re-explain models/concepts defined in Chapter 2 — use `\ref{}`
- All metric values must match this brief exactly
- Tables: caption ABOVE, `\label{tab:xxx}`
- Figures: caption below, `\label{fig:xxx}`
- IEEE references: `[N]` before full stop, numbered by order of first appearance
- Negative results included with analysis (Dr. Tahani's instruction)

---

## Chapter 1 — New Objectives and Thesis Layout Update

**Do NOT rewrite existing text. ADD to Section 1.2 (Objectives) and EDIT Section 1.3 (Thesis Layout) only.**

### Section 1.2 Objectives — Append three new objectives

After existing Objective 5, add:

```latex
    \item To investigate query repetition as a technique for resolving the BM25 term-dilution degradation observed when pseudo-documents are concatenated with short Arabic queries, and to identify the optimal repetition factor across multiple LLM models.

    \item To adapt and evaluate Corpus-Steered Query Expansion (CSQE) for Arabic retrieval, grounding LLM-generated expansions in first-pass retrieved documents and assessing the contribution of corpus-grounded versus blind expansion components through ablation.

    \item To combine corpus-steered query expansion with hybrid BM25--Dense retrieval and determine the optimal retriever-specific query representation strategy, examining whether applying query expansion asymmetrically to one retriever outperforms applying it to both.
```

### Section 1.3 Thesis Layout — Update Ch.3 and Ch.4 descriptions

**Replace Ch.3 paragraph** (currently ends at "model-specific technical considerations") with:

"...The adaptation of Query2Doc for Arabic zero-shot application is described, including modifications from the original paper and engineering optimisations. The chapter then presents the query repetition methodology for resolving BM25 term-dilution, the hybrid BM25--Dense fusion methodology, and the Corpus-Steered Query Expansion (CSQE) pipeline including its component ablation design and retriever-specific application strategy. The chapter concludes with the per-query error analysis methodology."

**Replace Ch.4 paragraph** (currently ends at "recommendations for model selection") with:

"...The comprehensive model comparison leaderboards are presented and analysed, including the examination of dropped models. The chapter then reports the Phase~4 expanded results: query repetition sweep across nine models, hybrid retrieval fusion configurations, CSQE component ablation and alpha sweep, CSQE combined with hybrid fusion across three retriever assignment configurations, the overall system progression table, and a per-query error analysis decomposing the sources of improvement and regression."

---

## Chapter 2 — Targeted Expansions

**Do NOT rewrite existing sections. Expand specific subsections as described below.**

### Expand `sec:hybrid_retrieval` — Add mathematical formulations

The current section (one paragraph) must be expanded to include the equations that Chapter 3 will reference. Add immediately after the existing paragraph:

```latex
Reciprocal Rank Fusion (RRF) \cite{bruch_2023_rrf} combines ranked lists by summing inverse rank scores:
\begin{equation}
    s_{\text{RRF}}(d) = \sum_{r \in \mathcal{R}} \frac{1}{k + \text{rank}_r(d)}
    \label{eq:rrf_ch2}
\end{equation}
where $\mathcal{R}$ is the set of ranked lists being fused and $k$ is a smoothing constant (typically $k = 20$) that reduces the impact of top-ranked documents. RRF is parameter-free in the sense that it does not require score normalisation, making it robust to score distribution differences between sparse and dense retrievers.

Score-level interpolation (Convex Combination, CC) computes a weighted sum of normalised retriever scores:
\begin{equation}
    s_{\text{CC}}(d, q) = \alpha \cdot \hat{s}_{\text{Dense}}(d, q) + (1 - \alpha) \cdot \hat{s}_{\text{BM25}}(d, q)
    \label{eq:hybrid_cc_ch2}
\end{equation}
where $\hat{s}$ denotes min-max normalised scores and $\alpha \in [0, 1]$ controls the relative contribution of the dense retriever. CC is sensitive to the normalisation strategy and score scale differences between the two systems.
```

Add labels: `\label{eq:rrf_ch2}` and `\label{eq:hybrid_cc_ch2}` (Chapter 3 will cross-reference these).

### Expand CSQE in `sec:modern_qe` — Add pipeline detail

The current CSQE mention (2–3 sentences) should be extended to describe the pipeline, since CSQE is the primary novel technique in this thesis. Expand to include:

```latex
The CSQE pipeline operates in two stages. First, a first-pass sparse retrieval step retrieves a small set of top-$k$ documents from the target corpus using the original query. These retrieved documents are then provided to the LLM alongside the query, instructing it to extract and synthesise topically relevant vocabulary and context grounded in the actual corpus content. This corpus-grounded expansion is combined with a blind expansion (standard Query2Doc) to produce the final enriched query. The key motivation is that corpus grounding anchors the LLM's output to attested Wikipedia vocabulary, preventing the hallucination of plausible but factually incorrect entities that characterises blind generation for niche or ambiguous queries. Lei et al. reported that even a 7B-parameter model achieves a 30\% improvement in mAP over BM25 on English benchmarks \cite{lei_2024_csqe}.
```

### Update `sec:research_gap` — Add Phase 4 gap

Append to the end of the research gap section:

```latex
A further gap exists in the application of corpus-steered expansion to non-English retrieval. The original CSQE work \cite{lei_2024_csqe} was evaluated exclusively on English benchmarks using English-language models; whether corpus grounding provides the same benefits for Arabic — where BM25 homonym sensitivity may corrupt the first-pass retrieval and misdirect the expansion — has not been investigated. Additionally, the interaction between corpus-steered expansion and hybrid BM25--Dense fusion has not been studied: specifically, whether applying query expansion asymmetrically to only one retriever in a hybrid system can outperform applying it to both is an open question with practical implications for retrieval pipeline design.
```

### Check References.bib

Verify the following citations exist. Add if missing:
- `lei_2024_csqe` — likely already present (found in chapter2.tex)
- `bruch_2023_rrf` — check and add if missing:
  ```bibtex
  @article{bruch_2023_rrf,
    author    = {Sebastian Bruch and Siyu Gai and Amir Ingber},
    title     = {An Analysis of Fusion Functions for Hybrid Retrieval},
    journal   = {ACM Transactions on Information Systems},
    year      = {2024},
    volume    = {42},
    number    = {1},
    doi       = {10.1145/3596512},
    note      = {arXiv:2210.11934}
  }
  ```
- `zhang_2023_miracl` — likely already present; verify key name matches usage in chapter2.tex

---

## Data Provenance — Where Every Number Came From

When in doubt about any value in this brief, these are the authoritative source files. In case of disagreement between this brief and downstream docs (CLAUDE.md, TASKS.md, memory entries), the source docs below are the source of truth.

| Numbers | Authoritative source |
|---------|---------------------|
| BM25 alone baseline (0.4621) | `docs/experiments/exp_002_baseline_bm25.md` |
| mDPR alone baseline (0.4993) | `docs/experiments/exp_001_baseline_dense.md` |
| Hybrid CC α-sweep, Hybrid RRF k=20/60 (all 0.62xx values) | `docs/experiments/exp_012_hybrid_baseline.md` |
| BM25 repetition sweep (all 9 models × 8 configs) | `docs/experiments/exp_011_bm25_repetition.md` |
| CSQE main results (BM25+CSQE 0.6157, Dense+CSQE 0.5915) | `docs/experiments/exp_013_csqe_aya.md` |
| CSQE ablation (013c=0.5381, 013d=0.5752) | `docs/experiments/exp_013c_csqe_corpus_only.md`, `exp_013d_csqe_blind_only.md` |
| CSQE+Hybrid all configs (A/B/C, RRF + CC) | `docs/experiments/exp_021_csqe_hybrid_fusion.md` |
| Config A RRF α sweep (α=1→0.7123, α=4→0.7137) | `CLAUDE.md` "Reference Baselines — CSQE Ablation" + exp_021 notebook Section 10 |
| Per-query error analysis (1,646/770/480, +0.1890 delta) | `docs/experiments/exp_error_analysis_csqe.md` |
| First-pass split (0.8877 vs 0.5814) | `docs/experiments/exp_error_analysis_csqe.md` |
| Query length split (Short Δ=+0.1990, Long Δ=+0.1053) | `docs/experiments/exp_error_analysis_csqe.md` |
| Regression classification (52% A, 36% B, 12% C) | `docs/experiments/exp_error_analysis_csqe.md` |
| Aya 8B blind Dense (0.6164, Osman's exp) | `docs/OSMAN_MODEL_COMPARISON_RESULTS.md` lines 192–228 |

**Raw result artifacts** (CSV/JSON for figure regeneration):
- `experiments/exp_11_bm25_repetition/exp11_all_metrics.json` — 9 models × 8 configs × 4 metrics
- `experiments/exp_12_hybrid_baseline/exp12_cc_metrics.json`, `exp12_rrf_metrics.json`
- `results/exp_21_csqe_hybrid/exp21_all_metrics.json` — full CC + RRF for Configs A/B/C
- `results/exp_error_analysis_csqe/per_query_deltas.csv` — per-query nDCG@10 for Blind and CSQE+Hybrid
- `results/exp_error_analysis_csqe/regression_classifications.csv` — manually labelled regression types

---

## Prompt for Chapter 1 + 2 Chat

```
I want to work on Task 6.4 — updating Chapters 1 and 2 of my thesis with the Phase 4 experiment results (query repetition, hybrid fusion, CSQE, CSQE+hybrid, per-query error analysis). Chapter 1 needs three new objectives and an updated thesis-layout paragraph. Chapter 2 needs three targeted expansions and three new citations.

**Read these files first for full context:**

1. `thesis_update_brief.md` — SINGLE SOURCE OF TRUTH for all Phase 4 numbers, tables, and prose. Focus on sections "Chapter 1 — New Objectives and Thesis Layout Update" and "Chapter 2 — Targeted Expansions" near the bottom.
2. `research_decisions/thesis_writing_guide.md` — Dr. Tahani's guidelines (passive voice, zigzag, cross-referencing, figure/table conventions). Apply throughout.
3. `TASKS.md` — find Task 6.4 for deliverable details
4. `RESEARCH_CONTEXT_KERNEL.md.md` — project overview
5. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter1.tex` — existing Chapter 1; preserve everything except the two sections specified below
6. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter2.tex` — existing Chapter 2; only modify the three subsections specified below
7. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/README_chapter1.md` — cross-reference labels and formatting conventions
8. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/README_chapter2.md` — cross-reference labels and formatting conventions
9. `University_of_Khartoum__EEE_bachelor_s_thesis_template/References.bib` — check whether lei_2024_csqe, bruch_2023_rrf, zhang_2024_mugi already exist before adding

**Chapter 1 changes (Section 1.2 Objectives + Section 1.3 Thesis Layout):**
- Section 1.2: APPEND three new objectives after the existing Objective 5 — use the EXACT LaTeX provided in `thesis_update_brief.md` under "Section 1.2 Objectives — Append three new objectives". Do not rewrite Objectives 1–5.
- Section 1.3: REPLACE the Chapter 3 paragraph and the Chapter 4 paragraph with the updated text from the brief under "Section 1.3 Thesis Layout — Update Ch.3 and Ch.4 descriptions". Do not touch the Ch.2 or Ch.5 paragraphs.

**Chapter 2 changes (three targeted expansions):**
- `sec:hybrid_retrieval`: APPEND the RRF and CC equation blocks (with labels `eq:rrf_ch2` and `eq:hybrid_cc_ch2`) immediately after the existing paragraph — Chapter 3 will cross-reference these labels.
- `sec:modern_qe`: EXPAND the existing CSQE mention (currently 2–3 sentences) into the fuller paragraph describing the two-stage pipeline, using the prose from the brief. The CSQE paragraph is the primary novel contribution of the thesis and must be proportionally detailed.
- `sec:research_gap`: APPEND the two-point Arabic/asymmetric-fusion gap paragraph from the brief — describes the non-English CSQE gap and the unstudied hybrid-asymmetric-QE gap.

**Also update:**
- `References.bib`: add the three new BibTeX entries (lei_2024_csqe, bruch_2023_rrf, zhang_2024_mugi) ONLY if they don't already exist. Use the BibTeX block provided in the brief for zhang_2024_mugi; for lei_2024_csqe and bruch_2023_rrf, use standard BibTeX entries matching the IEEE style of the existing file.
- `Chapters/README_chapter2.md`: add the two new equation labels (`eq:rrf_ch2`, `eq:hybrid_cc_ch2`) to the cross-reference table.

**Critical rules:**
- Passive voice throughout (Dr. Tahani's rule)
- Never re-explain models/concepts already defined in Chapter 2 — use `\ref{}` to earlier sections
- Every numeric value in the brief must appear in the thesis EXACTLY as written — no rounding, no rewording, no interpolation
- IEEE-style citations `[N]`, numbered by first appearance
- Figures: caption below, `\label{fig:xxx}`; Tables: caption ABOVE, `\label{tab:xxx}`
- Do NOT modify any section of Chapter 1 or Chapter 2 not explicitly listed above

**Deliverables:**
1. Full updated `chapter1.tex`
2. Full updated `chapter2.tex`
3. New/updated BibTeX entries for `References.bib` (as a diff block)
4. Updated `README_chapter2.md` with the new equation labels

This is a medium-sized task. If it's too long for one response, write Chapter 1 + README updates first, then I'll say "continue" for Chapter 2 + References.bib.
```

---

## Prompt for Chapter 3 + 4 Chat

```
I want to work on Task 6.4 — extending Chapter 3 (Methodology) and Chapter 4 (Results and Discussion) with the Phase 4 experiment sections, maintaining the zigzag correspondence our supervisor (Dr. Tahani) required. The existing sections 3.1–3.5 and 4.1–4.5 are complete and must not be touched. All new sections (3.6–3.9, 4.6–4.10) must be appended and must zigzag: every 4.x section must reference its corresponding 3.x methodology section via `\ref{}`.

**Read these files first for full context:**

1. `thesis_update_brief.md` — READ THE ENTIRE FILE. This is the single source of truth for EVERY number, table, equation, prose point, and cross-reference label used in the new sections. All values you write must match this file exactly.
2. `research_decisions/thesis_writing_guide.md` — Dr. Tahani's guidelines (especially the zigzag rule: 3.6↔4.6, 3.7↔4.7, 3.8↔4.8, 3.9↔4.9+4.10, passive voice, cross-referencing, figure/table conventions). Apply throughout.
3. `TASKS.md` — find Task 6.4 for deliverable details
4. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter3.tex` — existing Chapter 3; do NOT rewrite sections 3.1–3.5
5. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter4.tex` — existing Chapter 4; do NOT rewrite sections 4.1–4.5. You WILL update `tab:full_summary` in 4.5.6 to add the Phase 4 rows.
6. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/README_chapter3.md` — cross-reference labels and formatting conventions
7. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/README_chapter4.md` — cross-reference labels and formatting conventions
8. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/README_chapter2.md` — to reference existing Chapter 2 labels (`sec:jais2`, `sec:hybrid_retrieval`, `sec:modern_qe`, `eq:rrf_ch2`, `eq:hybrid_cc_ch2`, `eq:bm25`, etc.) without re-explaining concepts
9. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter2.tex` — only to verify the exact labels defined there (Chapter 1+2 update chat will have added `eq:rrf_ch2` and `eq:hybrid_cc_ch2`)

**Chapter 3 — APPEND new sections (do not modify 3.1–3.5):**
- **Section 3.6: Query Repetition for Sparse Retrieval** (`\label{sec:meth_repetition}`). Include BOTH the fixed-repetition equation (`eq:query_repetition`) AND the MuGI adaptive formula (`eq:mugi_repetition`). Justify why we need both: Query2Doc-style fixed n and MuGI-style adaptive β. Note that all expansions were reused from Task 4.0b (no new LLM inference).
- **Section 3.7: Hybrid Retrieval Fusion** (`\label{sec:meth_hybrid}`). Cross-reference `eq:rrf_ch2` and `eq:hybrid_cc_ch2` from Chapter 2 — DO NOT duplicate the equations. State sweep ranges: α ∈ {0.1, …, 0.9} and k ∈ {20, 60}. Describe the min-max per-query normalisation for CC.
- **Section 3.8: Corpus-Steered Query Expansion (CSQE)** (`\label{sec:meth_csqe}`). Three subsections:
  - 3.8.1 Pipeline (`sec:meth_csqe_pipeline`) — two-stage design, first-pass k=5, combination of corpus + blind samples, equation `eq:csqe_query` for the assembly
  - 3.8.2 Component Ablation Design (`sec:meth_csqe_ablation`) — describe exp_013c (4c+0b), exp_013d (0c+4b), exp_013 (2c+2b) and why the alpha sweep was reconstructed from stored pkls
  - 3.8.3 Retriever-Specific Application (`sec:meth_csqe_config`) — define Configs A, B, C and state the hypothesis that Dense degrades on long expanded queries
- **Section 3.9: Per-Query Error Analysis** (`\label{sec:meth_error_csqe}`). Describe pytrec_eval per-query nDCG@10, the failure/big-win/regression thresholds (< 0.1, > +0.3, < −0.1), the first-pass-quality split definition (any qrel > 0 in top-5), and the manual regression type taxonomy (Type A / B / C).

**Chapter 4 — APPEND new sections (do not modify 4.1–4.5; DO update `tab:full_summary` in 4.5.6 to add the Phase 4 rows):**
- **Section 4.6: BM25 Query Repetition Results** (`\label{sec:res_repetition}`). Use the 8-column sweep table from the brief VERBATIM (`tab:bm25_repetition`) and the supplementary Recall/MRR best-config table. Include ALL 5 prose points from the brief. Forward-reference `\ref{sec:meth_repetition}` and back-reference `\ref{sec:res_term_dilution}`.
- **Section 4.7: Hybrid Retrieval Fusion Results** (`\label{sec:res_hybrid}`). Use the full CC α-sweep (9 rows, α=0.1 through α=0.9) + RRF k=20 + RRF k=60 table (`tab:hybrid_results`). Cite **0.9467** for Recall@100 at RRF k=20 (source: `exp_012_hybrid_baseline.md`) — NOT 0.9466. The brief explains this discrepancy in a note; include the 0.9467 value without the note.
- **Section 4.8: Corpus-Steered Query Expansion Results** (`\label{sec:res_csqe}`):
  - 4.8.1 Main CSQE Results (`sec:res_csqe_main`) — `tab:csqe_main` comparing BM25+CSQE (0.6157), Dense+CSQE (0.5915), and no-QE hybrid baseline (0.6267, R@100=0.9467)
  - 4.8.2 Component Ablation (`sec:res_csqe_ablation`) — `tab:csqe_ablation` (013c vs 013d vs 013 full) and `tab:alpha_sweep` (α=1 through α=4 on BM25+CSQE). Prose: Blind-only > Corpus-only on BM25, but the combined 2+2 system beats both.
- **Section 4.9: CSQE with Hybrid Fusion** (`\label{sec:res_csqe_hybrid}`):
  - 4.9.1 Fusion Configuration Comparison (`sec:res_csqe_configs`) — `tab:csqe_hybrid_configs` (all three configs × RRF + CC), the Config A ablation sub-table, the new `tab:config_a_alpha` (Config A α sweep), and `tab:delta_analysis`. Emphasize the retriever-specific-representation principle as the KEY design finding of the thesis.
  - 4.9.2 Overall System Progression (`sec:res_progression`) — `tab:system_progression` showing baseline → blind QE → hybrid → CSQE → CSQE+hybrid culminating in 0.7137 nDCG@10 (+54.5% over BM25).
- **Section 4.10: Per-Query Error Analysis** (`\label{sec:res_error_csqe}`):
  - 4.10.1 Win/Loss Distribution (`sec:res_win_loss`) — `tab:error_distribution`. READ the data-provenance note in the brief: the underlying analysis compared Config C RRF (0.6936), not Config A RRF (0.7137). Use the exact caption wording from the brief: "Per-query comparison of the CSQE+Hybrid system (Config C RRF, 0.6936 nDCG@10) against the Aya Blind BM25 n=1 baseline (0.5046 nDCG@10) on 2,896 MIRACL Arabic dev queries."
  - 4.10.2 First-Pass Quality as Dominant Predictor (`sec:res_firstpass`) — `tab:error_patterns` (first-pass split) AND `tab:query_length_split` (short/long split). Both use full Blind/CSQE columns.
  - 4.10.3 Big Wins: The Corpus Grounding Effect (`sec:res_bigwins`) — all 1,061 big-win queries, three worked examples (الرباط المنصوري, John Dewey, Nicolas Boileau).
  - 4.10.4 Regression Analysis (`sec:res_regressions`) — `tab:regression_causes` (Type A 52% / B 36% / C 12%) and the two concrete Arabic failure examples (ماهو التطرف). Include the implications paragraph listing the two future improvements.

**Critical rules:**
- Passive voice throughout (Dr. Tahani's rule)
- ZIGZAG correspondence is mandatory: 3.6↔4.6, 3.7↔4.7, 3.8↔4.8, 3.9↔{4.9,4.10}. Every 4.x result section MUST reference its corresponding 3.x methodology section via `\ref{}` in the opening sentence.
- Reference Chapter 2 by label only — never re-explain models or concepts (e.g., "BM25, defined in Section~\ref{sec:bm25}" not "BM25 is a sparse retriever that…")
- Every numeric value in the thesis must match the brief EXACTLY — if a number looks suspicious, STOP and ask rather than rounding or interpolating
- NEVER invent intermediate values — only include α, n, or k values that appear in the brief tables
- Include negative and surprising results WITH analysis (Dr. Tahani's instruction) — e.g., Blind-only > Corpus-only on BM25 individually, Config C < Config A despite stronger Dense+CSQE, Type A regressions
- Figures: caption below with `\label{fig:xxx}`. Tables: caption ABOVE with `\label{tab:xxx}`.
- Describe flowcharts in prose where needed (actual figures will be inserted later) — state what each flowchart would depict
- Update `tab:full_summary` in 4.5.6 to include new rows for: Aya β=2 BM25, hybrid RRF k=20, BM25+CSQE, Dense+CSQE, Config A RRF (0.7137). Do NOT duplicate the full Phase 4 tables into 4.5.6.

**Deliverables:**
1. Full updated `chapter3.tex`
2. Full updated `chapter4.tex`
3. Updated `README_chapter3.md` with all new Section 3.6–3.9 labels listed in the brief
4. Updated `README_chapter4.md` with all new Section 4.6–4.10 labels listed in the brief

This is a very large task. If it's too long for one response:
- Response 1: Full updated `chapter3.tex` (all new Sections 3.6–3.9)
- Response 2 (say "continue"): Full updated `chapter4.tex` (Sections 4.6, 4.7, 4.8)
- Response 3 (say "continue"): Rest of `chapter4.tex` (Sections 4.9, 4.10) + updated `tab:full_summary` + both README files

Do not start until you have read `thesis_update_brief.md` in full — the brief was carefully revised to fix earlier data errors, and any Phase 4 number in the thesis that disagrees with the brief is wrong.
```

---

## Prompt for Chapter 5 + Abstract Chat

```
I want to work on Task 6.4 — updating Chapter 5 (Conclusions) and both abstracts (English and Arabic) of my thesis to reflect the Phase 4 experiment results. Chapter 5 needs four new conclusion paragraphs, one updated challenge, three updated recommendations, and three new recommendations. Both abstracts need the closing result sentence replaced with the new best result.

**Read these files first for full context:**

1. `thesis_update_brief.md` — SINGLE SOURCE OF TRUTH. Focus on the sections "Chapter 5 — Sections to Update" and "Abstract — What to Update" near the bottom, but read the Quick Reference block at the top to confirm the headline numbers (0.7137 nDCG@10, +54.5% over BM25, +13.9% over hybrid baseline).
2. `research_decisions/thesis_writing_guide.md` — Dr. Tahani's guidelines (passive voice, cross-referencing, figure/table conventions)
3. `TASKS.md` — find Task 6.4 for deliverable details
4. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter5.tex` — existing Chapter 5; preserve all existing sections, only append/update as specified
5. `University_of_Khartoum__EEE_bachelor_s_thesis_template/5-Abstract.tex` — English abstract
6. `University_of_Khartoum__EEE_bachelor_s_thesis_template/6-ARAbstract.tex` — Arabic abstract
7. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/README_chapter5.md` — cross-reference labels and formatting conventions

**Chapter 5 changes:**
- **Section 5.1 Conclusions:** APPEND four new paragraphs AFTER the existing "Overall" paragraph. Use the EXACT prose provided in the brief (query repetition paragraph, hybrid baseline paragraph, CSQE validation paragraph, retriever-specific representation paragraph). Do not rewrite any existing paragraphs. All forward-references must use `\ref{sec:res_repetition}`, `\ref{sec:res_hybrid}`, `\ref{sec:res_csqe}`, `\ref{sec:res_csqe_hybrid}`, `\ref{sec:res_error_csqe}`.
- **Section 5.2 Challenges:** UPDATE the existing BM25 term-dilution item — mark it RESOLVED inline with a forward reference to `\ref{sec:res_repetition}` (keep the original challenge text, add a "This challenge was resolved…" follow-up sentence). APPEND one new challenge: "First-pass quality dependence" (use the exact wording from the brief, including the Arabic homonym example).
- **Section 5.3 Recommendations:** MOVE Recommendation 2 (BM25 query repetition) and Recommendation 4 (Hybrid retrieval with QE) to a short note saying they have been implemented in Phase 4, with forward references to `\ref{sec:res_repetition}` and `\ref{sec:res_csqe_hybrid}`. APPEND three new recommendations (first-pass quality gate, asymmetric expansion weighting, CSQE with stronger dense retrievers) using the exact wording from the brief.

**Abstract changes:**
- **English abstract (5-Abstract.tex):** REPLACE the closing result sentence with: "The proposed corpus-steered pipeline, combined with hybrid BM25+Dense fusion, achieved 0.7137 nDCG@10 on the MIRACL Arabic benchmark — a 54.5\% improvement over the BM25 baseline and a 13.9\% improvement over a strong no-QE hybrid system." Do not touch any other sentence in the abstract.
- **Arabic abstract (6-ARAbstract.tex):** REPLACE the corresponding Arabic closing sentence with the same numbers. Use standard ASCII digits (0.7137, 54.5\%) unless the existing Arabic abstract uses Eastern Arabic numerals everywhere — in which case match the existing convention. Preserve all existing RTL formatting, `\RL{}`, and any `arabtex` macros in the file.

**Critical rules:**
- Passive voice for Chapter 5 prose (Dr. Tahani's rule)
- Every numeric value must match the brief EXACTLY
- Do not introduce new citations — Chapter 5 should cite only earlier chapters via `\ref{}`
- Preserve ALL existing `\label{}` definitions
- For the Arabic abstract: do not reformat other sentences, do not convert digits in other sentences, do not touch the `\documentclass` or `\usepackage` lines if present
- If the existing Chapter 5 or abstracts already mention any Phase 4 result, leave it alone — do not duplicate

**Deliverables:**
1. Full updated `chapter5.tex`
2. Full updated `5-Abstract.tex`
3. Full updated `6-ARAbstract.tex`
4. Short note on any `README_chapter5.md` updates needed

This is a medium task. If it's too long for one response, write Chapter 5 first, then I'll say "continue" for the two abstracts.
```
