# Phase 4 Quick Wins: Implementation Guide

**Date:** 2026-04-03
**Status:** Ready for Implementation
**Purpose:** Detailed implementation notes for Direction 1 experiments. Each section captures what to change, why, and what the current pipeline looks like so an implementation session can start without re-deriving context.

---

## Current Pipeline Architecture (What Exists)

**Generation notebook** (e.g., `Query_generator_aya_8b.ipynb`):
1. Loads model + tokenizer from HuggingFace
2. `Query2DocEnhancer` class with `enhance()` and `enhance_batch()` methods
3. System prompt: `"You are asked to write a passage that answers the given query. Do not ask the user for further clarification. Respond in Arabic only."`
4. Concatenation: `return f"{query} {pseudo_doc}"` (simple space-separated)
5. Output saved as `.pkl` to Google Drive: `enhanced_queries_{model}.pkl`

**Evaluation notebook** (`evaluate_enhanced_queries.ipynb`):
- Loads the `.pkl` file of enhanced queries
- Runs them through both mDPR (dense) and BM25S (sparse) retrievers
- Evaluates with pytrec-eval: nDCG@10, Recall@10, Recall@100, MRR

**Key file paths (Google Drive):**
- Enhanced queries: `/content/drive/MyDrive/enhanced_queries_{model}.pkl`
- BM25S index: loaded via symlinks in Colab
- mDPR index: Pyserini pre-built, loaded via faiss

**What we already have for ALL 9 models:**
- The `.pkl` files with enhanced queries (query + pseudo_doc concatenated)
- Dense retrieval results (run files with scores)
- BM25 retrieval results (run files with scores)
- Evaluation metrics computed

---

## Experiment 1.1: BM25 Query Repetition Fix

### The Problem
Our current concatenation is: `enhanced = query + " " + pseudo_doc`

BM25 scores terms by frequency. When a 5-token query is concatenated with a 200-token pseudo-doc, the original query terms become ~2.5% of the expanded query. BM25 treats the pseudo-doc terms as more important simply because they're longer. This is the root cause of 6/9 models degrading BM25.

The original Query2Doc paper (Wang et al., EMNLP 2023) addresses this by repeating the query n times: `enhanced = (query + " ") * n + pseudo_doc`. With n=5, the query terms represent ~11% of the expanded query — enough to maintain BM25's term frequency signal.

### What to Change

**Option A: Fixed Repetition (simplest)**
```
# CURRENT (line 763 and 814 in Aya notebook):
return f"{query} {pseudo_doc}"

# CHANGE TO:
n = 5  # repetition count
return f"{(query + ' ') * n}{pseudo_doc}"
```

**Option B: MuGI Adaptive Repetition (better)**
```
# From MuGI (Zhang et al., EMNLP 2024 Findings, arXiv:2401.06311):
beta = 4  # proportionality constant
lambda_n = max(1, int(len(pseudo_doc.split()) / (len(query.split()) * beta)))
return f"{(query + ' ') * lambda_n}{pseudo_doc}"
```
The adaptive formula automatically increases repetitions for longer pseudo-docs and shorter queries. MuGI found beta=4 works well, but we should test beta ∈ {2, 4, 6}.

### How to Run Without New LLM Inference

**Critical insight:** We don't need to re-generate pseudo-documents. We need to:
1. Load each existing `.pkl` file
2. **Split** each enhanced query back into original query + pseudo_doc (they're separated by the first space after the original query text — or we can re-load the original MIRACL queries and strip them)
3. Re-concatenate with repetition: `(query + " ") * n + pseudo_doc`
4. Re-run BM25 evaluation only (not dense — dense results won't change much with repetition since mDPR uses semantic matching)

**Alternative approach:** If splitting the `.pkl` is tricky, we can load the original MIRACL dev queries alongside the `.pkl` and reconstruct. The original queries are in `miracl/miracl` HuggingFace dataset, `dev` split, `query` field.

### Configurations to Test

| Config | Repetition | Notes |
|--------|-----------|-------|
| n=1 | `query + pseudo_doc` | Current (baseline, already have results) |
| n=3 | `query*3 + pseudo_doc` | Light repetition |
| n=5 | `query*5 + pseudo_doc` | Original Query2Doc paper recommendation |
| n=7 | `query*7 + pseudo_doc` | Heavier |
| n=10 | `query*10 + pseudo_doc` | Maximum tested |
| adaptive (β=2) | MuGI formula | Aggressive adaptation |
| adaptive (β=4) | MuGI formula | MuGI default |
| adaptive (β=6) | MuGI formula | Conservative adaptation |

### Models to Test
ALL 9 viable models (we have all .pkl files):
- Aya Expanse 8B, Jais-2-8B, Qwen3-8B, Qwen 2.5-7B, Qwen3-4B, Gemma 3 4B, Qwen 2.5 3B, Falcon-H1-3B, SILMA Kashif-2B

### Expected Output

**New thesis table: "Effect of Query Repetition on BM25 Performance (nDCG@10)"**

| Model | n=1 (current) | n=3 | n=5 | n=7 | Adaptive (β=4) |
|-------|--------------|-----|-----|-----|----------------|
| Aya Expanse 8B | 0.5047 | ? | ? | ? | ? |
| Jais-2-8B | 0.5121 | ? | ? | ? | ? |
| ... | ... | ... | ... | ... | ... |

**Key question answered:** How many of the 6 degraded models flip to positive with repetition?

**Thesis location:** Chapter 4 (new results table), Chapter 5 (explains the degradation mechanism and fix)

### Effort: ~1 day
- Implementation: 1-2 hours (modify concatenation, loop over models)
- BM25 re-evaluation: 2-3 hours (2,896 queries × 9 models × ~5 repetition values, but BM25 is fast)
- Analysis: 1-2 hours

---

## Experiment 1.2: Hybrid Baseline (BM25 + mDPR)

### The Finding
The MIRACL paper (Zhang et al., TACL 2023, Table 2) reports:
- BM25 alone: 0.481 nDCG@10
- mDPR alone: 0.499 nDCG@10
- **BM25 + mDPR hybrid: 0.673 nDCG@10** (alpha=0.5, untuned)

This was **verified** from three sources: the MIRACL paper Table 2, Pyserini 2CR reproduction page, and ar5iv HTML rendering.

Our baselines are slightly different (BM25S=0.462, mDPR=0.499) because we use BM25S (Python-native) instead of Pyserini BM25. Our hybrid will likely be ~0.63-0.66 instead of 0.673.

### What to Implement

A new evaluation script (or notebook cell) that:
1. Loads the BM25 run file (per-query ranked list with scores)
2. Loads the mDPR run file (per-query ranked list with scores)
3. For each query:
   a. Collect all candidate documents from both lists (union)
   b. Min-max normalize BM25 scores to [0,1]: `s_norm = (s - s_min) / (s_max - s_min)` per query
   c. Min-max normalize mDPR scores to [0,1]: same formula per query
   d. For documents appearing in only one list: assign score 0 from the other
   e. Compute: `s_hybrid = α * s_BM25_norm + (1-α) * s_mDPR_norm`
4. Sort by hybrid score, take top-100
5. Evaluate with pytrec-eval

### Why Convex Combination (CC) Over RRF

Bruch et al. (ACM TOIS 2023, arXiv:2210.11934) showed CC outperforms RRF in both in-domain and out-of-domain settings. RRF discards useful score distribution information. CC needs only ~20 queries to tune alpha.

We should test BOTH, but CC should be primary.

### Configurations to Test

**Convex Combination (CC):** α ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}
**RRF (for comparison):** `score(d) = Σ 1/(k + rank_i(d))`, k ∈ {20, 60, 100}

### Input Files Needed
- BM25 baseline run file (from exp_002)
- mDPR baseline run file (from exp_001)
- Both should be in TREC run format or equivalent with scores

### Expected Output

**New thesis table: "Hybrid BM25+mDPR Baseline"**

| Method | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25 alone | 0.4621 | 0.5622 | 0.8577 | 0.4862 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| Hybrid CC (best α) | ~0.64? | ? | ? | ? |
| Hybrid RRF (best k) | ~0.62? | ? | ? | ? |

**New thesis figure:** α sensitivity curve (nDCG@10 vs α)

**Key finding:** Establishes the strongest non-QE baseline. All QE experiments should beat this.

**Thesis location:** Chapter 3 (new methodology subsection on hybrid retrieval), Chapter 4 (new baseline row in all comparison tables)

### Effort: ~0.5 days
- Implementation: 2-3 hours (score normalization + fusion)
- Evaluation: ~30 minutes (one sweep, lightweight computation)
- Analysis: 1 hour (generate α curve, compare CC vs RRF)

---

## Experiment 1.3: HyDE vs Query2Doc Comparison

### The Difference

Both HyDE and Query2Doc use an LLM to generate a pseudo-document. The difference is how it's used:

| | Query2Doc | HyDE |
|---|-----------|------|
| Input to retriever | `query + pseudo_doc` (text) | `embed(pseudo_doc)` (vector) |
| Original query | Preserved in retrieval input | Discarded (only in pseudo-doc implicitly) |
| Works with BM25 | Yes (text concatenation) | No (needs embeddings) |
| Works with dense | Yes (encode combined text) | Yes (encode pseudo-doc alone) |

**HyDE hypothesis:** The pseudo-document is semantically closer to relevant documents than the query is, so embedding it directly should give better dense retrieval.

**Query2Doc hypothesis:** Keeping the original query preserves important terms that the pseudo-doc may miss.

### What to Implement

For **dense retrieval only** (HyDE doesn't apply to BM25):
1. Load existing `.pkl` files for each model
2. Extract ONLY the pseudo-document part (strip the original query prefix)
3. Encode the pseudo-document alone through mDPR encoder
4. Use that embedding to search the mDPR index (same FAISS index already built)
5. Evaluate with pytrec-eval

**Key technical detail:** mDPR has separate query and passage encoders. For HyDE, we should encode the pseudo-document through the **query encoder** (since we're using it as a query replacement). The pseudo-doc is NOT a real passage, so the passage encoder may not be appropriate.

### Models to Test
Top 3 only (to keep scope manageable):
- Aya Expanse 8B (best overall)
- Jais-2-8B (best dense)
- Qwen3-4B (best mid-size)

### Expected Output

**New thesis table: "HyDE vs Query2Doc on MIRACL Arabic (Dense Retrieval)"**

| Model | No QE (baseline) | Query2Doc | HyDE | Δ (Q2D vs HyDE) |
|-------|-----------------|-----------|------|------------------|
| Aya Expanse 8B | 0.4993 | 0.6166 | ? | ? |
| Jais-2-8B | 0.4993 | 0.6018 | ? | ? |
| Qwen3-4B | 0.4993 | 0.5691 | ? | ? |

**Why this matters:** No paper compares HyDE vs Query2Doc on Arabic. This is a **novel contribution** to the literature. The result will either:
- Confirm Query2Doc > HyDE for Arabic (preserving original query terms matters for morphologically-rich languages)
- Or show HyDE > Query2Doc (semantic matching dominates even for Arabic)

Either outcome is publishable.

**Knowledge leakage angle:** Yoon et al. (arXiv:2504.14175) found that HyDE/Query2Doc gains on English may be inflated because LLMs memorize benchmark answers. Our Arabic evaluation is more rigorous because LLMs are less likely to have memorized MIRACL Arabic content. Worth mentioning in Chapter 5.

**Thesis location:** Chapter 2 (add HyDE to literature review), Chapter 3 (methodology for HyDE experiment), Chapter 4 (comparison table), Chapter 5 (analysis)

### Effort: ~1 day
- Implementation: 3-4 hours (extract pseudo-docs, encode through mDPR query encoder, search)
- Evaluation: 1-2 hours (3 models × mDPR search)
- Analysis: 1-2 hours

---

## Experiment 1.4: Prompt Variant Comparison

### The Rationale

Our current pipeline uses a single prompt strategy (pseudo-document generation). The literature shows different prompt strategies produce different types of expansion:

| Prompt Strategy | Output Type | Best For | Reference |
|----------------|------------|----------|-----------|
| **Pseudo-document** (current) | Long narrative passage | Dense retrieval (semantic matching) | Query2Doc (Wang et al., 2023) |
| **Chain-of-Thought** | Reasoning chain with related concepts | Capturing implicit relationships | Jagerman et al. (arXiv:2305.03653) |
| **Keywords** | Short keyword list | BM25 (direct term matching, less dilution) | GRF finding (Mackie et al., SIGIR 2023) |
| **Rewrite** | Refined/expanded query | Preserving query structure while adding context | Rewrite-Retrieve-Read (Ma et al., EMNLP 2023) |

### What to Implement

Same model (Aya Expanse 8B), same pipeline, only the system prompt changes:

**Prompt A — Pseudo-Document (current, already have results):**
```
System: "You are asked to write a passage that answers the given query. 
Do not ask the user for further clarification. Respond in Arabic only."
User: {query}
```

**Prompt B — Chain-of-Thought (CoT-QE):**
```
System: "You are a search expert. Think step by step about what this Arabic 
query is asking. Identify the key concepts, related terms, and important 
context that would help find relevant documents. Respond in Arabic only."
User: {query}
```

**Prompt C — Keywords:**
```
System: "You are a search expert. Given an Arabic query, list 10-15 important 
Arabic keywords, named entities, and specific phrases that would appear in 
relevant documents. Output ONLY the keywords separated by spaces, no 
explanations. Respond in Arabic only."
User: {query}
```

**Prompt D — Query Rewrite:**
```
System: "You are a search expert. Rewrite the following Arabic query to be 
more specific, detailed, and effective for document retrieval. Include relevant 
context and terminology. Output only the rewritten query. Respond in Arabic only."
User: {query}
```

### How to Run

1. Copy the Aya notebook 3 times (one per new prompt variant)
2. Change ONLY the `self.system_prompt` in each
3. Generate new `.pkl` files: `enhanced_queries_aya_prompt_B.pkl`, etc.
4. Evaluate each on both mDPR and BM25 (with optimal n from Exp 1.1 for BM25)

### Configurations

| Prompt | Model | Dense eval | BM25 eval (with repetition) |
|--------|-------|-----------|---------------------------|
| A (pseudo-doc) | Aya 8B | Already have | Re-run with n from 1.1 |
| B (CoT) | Aya 8B | New generation + eval | New generation + eval |
| C (keywords) | Aya 8B | New generation + eval | New generation + eval |
| D (rewrite) | Aya 8B | New generation + eval | New generation + eval |

### Expected Output

**New thesis table: "Effect of Prompt Strategy on Arabic QE"**

| Prompt | Dense nDCG@10 | Dense Recall@10 | BM25 nDCG@10 | BM25 Recall@10 |
|--------|--------------|-----------------|-------------|----------------|
| No QE (baseline) | 0.4993 | 0.6156 | 0.4621 | 0.5622 |
| A: Pseudo-doc | 0.6166 | 0.7231 | ? (with rep) | ? |
| B: CoT reasoning | ? | ? | ? | ? |
| C: Keywords only | ? | ? | ? | ? |
| D: Query rewrite | ? | ? | ? | ? |

**Hypotheses:**
- Keywords (C) should work best for BM25 (fewer noisy terms, direct term matching)
- Pseudo-doc (A) should work best for dense (semantic richness)
- CoT (B) may capture relationships that pseudo-doc misses
- If keywords beat pseudo-doc on BM25, this motivates retriever-specific prompts (Direction 2.2)

**Thesis location:** Chapter 3 (prompt design methodology), Chapter 4 (comparison table), Chapter 5 (which strategy works when and why)

### Effort: ~2-3 days
- Implementation: 1-2 hours (copy notebook, change prompts)
- Generation: 3× ~1 hour on A100 = ~3 hours (2,896 queries × 3 new prompts)
- Evaluation: 2-3 hours (3 prompts × 2 retrievers)
- Analysis: 2-3 hours

---

## Summary: What Stays the Same vs What's New

| Component | Exp 1.1 | Exp 1.2 | Exp 1.3 | Exp 1.4 |
|-----------|---------|---------|---------|---------|
| LLM model | Same (reuse) | N/A | Same (reuse) | Same Aya |
| Pseudo-documents | Reuse existing | N/A | Reuse existing | New generation |
| mDPR index | Same | Same | Same | Same |
| BM25 index | Same | Same | N/A | Same |
| Concatenation | **CHANGED** (add repetition) | N/A | **CHANGED** (pseudo-doc only) | Standard + repetition |
| Evaluation pipeline | Same | **NEW** (fusion script) | Same | Same |
| System prompt | Same | N/A | Same | **CHANGED** (3 variants) |
| GPU needed? | No (BM25 is CPU) | No (just math) | Yes (mDPR encoding) | Yes (Aya generation) |

---

## Dependencies and Parallel Execution

```
[1.1 BM25 Repetition] ─── can run on CPU, no Colab needed
[1.2 Hybrid Baseline]  ─── can run locally, no Colab needed
[1.3 HyDE Comparison]  ─── needs Colab GPU for mDPR encoding

All three above: FULLY INDEPENDENT, run in parallel

[1.4 Prompt Variants]  ─── needs Colab GPU for Aya generation
                            needs optimal n from 1.1 for BM25 eval
                            so START AFTER 1.1 is done
```

---

## Key Papers to Cite

| Paper | What we use from it | Citation |
|-------|-------------------|----------|
| Query2Doc | Query repetition for BM25 (n=5) | Wang et al., EMNLP 2023, arXiv:2303.07678 |
| MuGI | Adaptive repetition formula | Zhang et al., EMNLP 2024 Findings, arXiv:2401.06311 |
| MIRACL | Hybrid baseline numbers | Zhang et al., TACL 2023, arXiv:2210.09984 |
| Bruch et al. | CC > RRF for fusion | Bruch et al., ACM TOIS 2023, arXiv:2210.11934 |
| HyDE | Embed pseudo-doc approach | Gao et al., ACL 2023, arXiv:2212.10496 |
| GRF | Varied generation subtasks finding | Mackie et al., SIGIR 2023, arXiv:2304.13157 |
| CoT-QE | Chain-of-thought for QE | Jagerman et al., 2023, arXiv:2305.03653 |
| Knowledge leakage | Arabic eval is more rigorous | Yoon et al., 2025, arXiv:2504.14175 |
| Arabic QE validation | Aya for Arabic QE confirmed | Macmillan-Scott et al., 2025, arXiv:2511.19325 |
