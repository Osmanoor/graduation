# Literature Review: Query Expansion + Hybrid Retrieval Intersection

**Date:** 2026-03-28
**Status:** Research Complete
**Task:** Phase 4 literature review -- hybrid retrieval and QE interaction
**Context:** Our project shows dense retrieval benefits from QE (+3.7% to +23.5% NDCG@10) but BM25 often degrades (-6% to -15% for 6/9 models). This review investigates whether hybrid retrieval can resolve this asymmetry.

---

## Executive Summary

The literature reveals a rich and rapidly evolving research area at the intersection of query expansion and hybrid retrieval. Key findings:

1. **Hybrid retrieval without QE already outperforms your baselines significantly.** The MIRACL paper reports BM25+mDPR hybrid nDCG@10 = 0.673 for Arabic -- a +34.8% jump over your mDPR baseline (0.4993) and +45.6% over BM25 (0.4621). This is the single largest potential improvement available to you.

2. **QE + fusion is better than QE + single retriever.** Exp4Fuse (Liu et al., ACL 2025) shows that fusing original-query and expanded-query retrieval lists via modified RRF outperforms using expanded queries alone, with up to +8.7 absolute points improvement.

3. **Dense and sparse need DIFFERENT expansions.** LevelRAG (Zhang et al., 2025) and MuGI (Zhang et al., EMNLP 2024) demonstrate that retriever-specific query optimization substantially outperforms one-size-fits-all expansion.

4. **The reason BM25 degrades with QE is well-understood.** LLM-generated pseudo-documents inject off-topic terms, meta-text, and hallucinated content that pollute BM25's term-frequency matching. Solutions exist: term filtering, corpus grounding, and fusion with unexpanded results.

5. **Adaptive/selective QE is feasible but QPP is immature.** UniRAG (ACL 2025) and DMQR-RAG show adaptive strategy selection, but QPP-driven selective expansion offers only marginal gains per recent analysis.

6. **Convex Combination (CC) fusion outperforms RRF** in both in-domain and out-of-domain settings (Bruch et al., ACM TOIS 2023). CC is also more sample-efficient to tune.

---

## Table of Contents

1. [Area 1: RRF + Query Expansion](#area-1)
2. [Area 2: Retriever-Specific Query Expansion](#area-2)
3. [Area 3: Hybrid Retrieval Baselines on MIRACL](#area-3)
4. [Area 4: Adaptive / Selective QE](#area-4)
5. [Area 5: Fusion Strategies Beyond RRF](#area-5)
6. [Area 6: Dense-Sparse Complementarity with QE](#area-6)
7. [Cross-Cutting Survey Papers](#surveys)
8. [Synthesis: Implications for Our Project](#synthesis)

---

<a name="area-1"></a>
## Area 1: RRF + Query Expansion

### Paper 1.1: Exp4Fuse -- A Rank Fusion Framework for Enhanced Sparse Retrieval using LLM-based Query Expansion

- **Authors:** Liu et al.
- **Year/Venue:** 2025, Findings of ACL 2025 (Vienna)
- **arXiv:** 2506.04760
- **Code:** https://github.com/liuliuyuan6/Exp4Fuse

**Key Mechanism:** Instead of replacing the original query with an LLM-expanded one, Exp4Fuse runs TWO retrieval routes simultaneously: one with the original query, one with the LLM-expanded query. Both use a sparse retriever. The two ranked lists are then fused using a modified RRF method. This "expansion-as-fusion" approach avoids the problem of bad expansions destroying results.

**Results:**
- Outperforms classical and dense rerankers on MS MARCO, BEIR, and 7 low-resource datasets
- Up to +8.7 absolute NDCG@10 improvement over base BM25
- Key insight: even when the expanded query is mediocre, fusing it with the original preserves quality

**Relevance to Our Project:**
- **Directly applicable.** You already have both BM25 and mDPR pipelines. You can run BM25(original) + BM25(expanded) + mDPR(original) + mDPR(expanded) and fuse all four lists.
- **Explains your BM25 degradation pattern:** When expansion is noisy, using it as the SOLE input to BM25 hurts. But fusing expanded and unexpanded BM25 lists should preserve gains while limiting damage.
- **Feasible for Colab:** YES. No training needed. Just run retrieval twice per retriever and apply RRF. You already have the infrastructure.

---

### Paper 1.2: RAG-Fusion -- A New Take on Retrieval-Augmented Generation

- **Authors:** Zackary Rackauckas
- **Year/Venue:** 2024, arXiv preprint
- **arXiv:** 2402.03367
- **Code:** https://github.com/Raudaschl/rag-fusion

**Key Mechanism:** Uses an LLM to generate multiple VARIATIONS of the user's original query (not pseudo-documents, but alternative phrasings). Each variation is retrieved separately, then all results are fused via RRF into a single ranked list.

**Results:**
- Provides more comprehensive answers due to multi-perspective query coverage
- Some topic drift when generated queries deviate too far from original intent
- No formal NDCG/MRR numbers reported on standard benchmarks

**Relevance to Our Project:**
- **Moderate.** The multi-query approach could complement your Query2Doc (which generates pseudo-documents). You could generate N query variations instead of (or in addition to) pseudo-documents.
- **Feasible for Colab:** YES. Lightweight -- just multiple LLM calls + RRF. But adds latency proportional to number of query variations.
- **Limitation:** No controlled experiments on IR benchmarks like BEIR or MIRACL.

---

### Paper 1.3: Scaling Retrieval Augmented Generation with RAG Fusion: Lessons from an Industry Deployment

- **Authors:** (Industry paper)
- **Year/Venue:** 2026, arXiv preprint
- **arXiv:** 2603.02153

**Key Mechanism:** Industry-scale deployment of RAG-Fusion. Reports practical lessons on scaling multi-query + RRF fusion in production.

**Relevance to Our Project:** LOW. Industry-focused, but confirms that multi-query + RRF is production-ready.

---

<a name="area-2"></a>
## Area 2: Retriever-Specific Query Expansion

### Paper 2.1: LevelRAG -- Enhancing RAG with Multi-hop Logic Planning over Rewriting Augmented Searchers

- **Authors:** Zhuocheng Zhang, Yang Feng, Min Zhang
- **Year/Venue:** 2025, arXiv preprint (under review)
- **arXiv:** 2502.18139
- **Code:** https://github.com/ictnlp/LevelRAG

**Key Mechanism:** Two-level architecture:
- **High-level searcher:** Decomposes complex queries into atomic sub-queries (retriever-agnostic)
- **Low-level searchers:** Each searcher (sparse, dense, web) independently REWRITES the sub-query to optimize it for their specific retriever. The sparse searcher uses Lucene syntax optimization; the dense searcher uses semantic reformulation.

**This is the closest paper to "retriever-specific expansion."** The key insight is that the query rewriting should be DECOUPLED from the retriever choice, and each retriever gets its own optimized version of the query.

**Results:**
- Surpasses all baselines across 3 single-hop QA tasks AND complex multi-hop QA
- Superior performance from letting each retriever optimize its own query form
- Sparse searcher benefits from structured keyword-style rewrites; dense searcher benefits from natural language semantic expansion

**Relevance to Our Project:**
- **HIGHLY RELEVANT.** This directly addresses your observation that dense and sparse respond differently to QE. You could implement a simplified version: generate keyword-focused expansion for BM25, semantic expansion for mDPR.
- **Feasible for Colab:** MEDIUM. The full LevelRAG system requires multiple LLM calls per query (high-level + low-level). But the PRINCIPLE of retriever-specific prompting is trivially implementable: use one prompt template for BM25 (asking for keywords/terms) and another for mDPR (asking for contextual description).
- **AI Suggestion:** A "LevelRAG-lite" experiment: same LLM, two prompts -- one generating keyword lists for BM25, one generating Query2Doc-style pseudo-documents for mDPR. Then fuse results. This would be a novel contribution.

---

### Paper 2.2: MuGI -- Multi-Text Generation Integration for Information Retrieval

- **Authors:** Le Zhang, Yihong Wu, Qian Yang, Jian-Yun Nie
- **Year/Venue:** 2024, Findings of EMNLP 2024
- **arXiv:** 2401.06311
- **Code:** https://github.com/lezhang7/Retrieval_MuGI

**Key Mechanism:** Training-free framework that:
1. Prompts LLMs to generate MULTIPLE pseudo-references (not just one)
2. Uses adaptive query-reference reweighting to control the balance between original query and generated content
3. Specifically handles the dense vs. sparse difference: for BM25, multiple samplings generate essential vocabularies; for dense, they provide semantic coverage

**Results:**
- BM25+MuGI: +18% on TREC DL, +7.5% on BEIR over base BM25
- BM25+MuGI outperformed most dense retrievers in out-of-domain contexts
- Average nDCG@10 of 51% across 9 low-resource BEIR benchmarks (+7.6% over base BM25)
- Sets new SOTA for training-free sparse retrieval enhancement

**Relevance to Our Project:**
- **VERY HIGH.** MuGI specifically addresses the BM25 degradation problem through multiple generations + reweighting. Instead of one pseudo-document (which may be noisy), multiple samples allow the signal to emerge while noise averages out.
- **Directly comparable to Query2Doc.** MuGI explicitly benchmarks against Query2Doc and HyDE and outperforms both.
- **Feasible for Colab:** YES. Training-free. Uses same LLMs you already have. Main cost: generating N pseudo-references instead of 1 (N=5 in their experiments). With your Aya/Jais-2 models, this means ~5x generation time but no new infrastructure.
- **Key lesson for your BM25 problem:** Multiple samples + reweighting prevents topic drift.

---

### Paper 2.3: MPQE -- Multi-Model Pseudo-Document Generation and Reconstruction for Hybrid Query Expansion

- **Authors:** (Not fully specified in search results)
- **Year/Venue:** December 2025, Information Processing & Management (ScienceDirect)
- **DOI:** 10.1016/j.ipm.2025 (S0306457325004844)

**Key Mechanism:**
1. Generate pseudo-documents from MULTIPLE different LLMs (not just one model)
2. Segment each pseudo-document into semantic units
3. Filter via semantic clustering to remove noise/drift
4. Reconstruct into a concise, clean pseudo-document
5. Combine with original query for expansion

**Results:**
- 3%-17% improvement in BM25 effectiveness on MS MARCO and TREC DL
- 3% average nDCG@10 gain across 5 out-of-domain datasets (DBpedia, NFCorpus, Scifact, Trec-Covid, Touche2020)
- No fine-tuning required

**Relevance to Our Project:**
- **INTERESTING VARIANT.** You have already tested 10 different LLMs. Instead of picking the "best" one, MPQE suggests combining outputs from multiple models and using semantic clustering to filter noise.
- **Feasible for Colab:** MEDIUM. Requires running multiple LLMs per query. But you could use your top 2-3 models (Aya, Jais-2, Qwen3-4B) and combine their outputs.
- **Novel angle:** This could be a Phase 4 experiment -- "multi-model ensemble QE" using your existing model comparison infrastructure.

---

<a name="area-3"></a>
## Area 3: Hybrid Retrieval Baselines on MIRACL

### Paper 3.1: MIRACL -- A Multilingual Retrieval Dataset Covering 18 Diverse Languages

- **Authors:** Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, et al.
- **Year/Venue:** 2023, TACL (Transactions of the ACL)
- **arXiv:** 2210.09984

**Hybrid Results for Arabic (from the official MIRACL paper):**

| Method | Arabic nDCG@10 |
|--------|---------------|
| BM25 | 0.481 |
| mDPR | 0.499 |
| **BM25 + mDPR Hybrid (alpha=0.5)** | **0.673** |

**Key Mechanism:** Simple convex combination: s_Hybrid = alpha * s_BM25 + (1-alpha) * s_mDPR, with alpha=0.5 (untuned), after normalizing both scores to [0,1].

**CRITICAL FINDING:** The hybrid BM25+mDPR baseline achieves nDCG@10 = 0.673 for Arabic. Compare this with your current results:
- Your mDPR baseline: 0.4993
- Your best QE result (Aya, Dense): 0.6166
- MIRACL hybrid (no QE): 0.673

**This means the official hybrid baseline WITHOUT any QE already outperforms your best QE-enhanced dense result by +9.1%.** The hybrid approach captures complementary signals that QE alone cannot provide.

**Relevance to Our Project:**
- **ESSENTIAL BASELINE.** You MUST implement this hybrid baseline before claiming QE improvements. The combination BM25+mDPR is trivial to compute and provides the strongest baseline.
- **Feasible for Colab:** YES. You already have both BM25 and mDPR results. You just need to normalize scores and combine them.
- **Note:** Your BM25 and mDPR numbers differ slightly from the MIRACL paper's baselines (likely due to BM25S vs. Anserini). But the relative hybrid improvement should be similar.

---

### Paper 3.2: BGE-M3 -- Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings

- **Authors:** Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, Zheng Liu
- **Year/Venue:** 2024, arXiv (presented at EMNLP 2024 Industry Track)
- **arXiv:** 2402.03216

**Key Mechanism:** A single model that supports three retrieval modes:
- Dense retrieval (embedding similarity)
- Learned sparse retrieval (SPLADE-like learned term weights -- outperforms BM25)
- Multi-vector retrieval (ColBERT-like late interaction)

**Results on MIRACL (average across 18 languages):**

| Mode | nDCG@10 (avg) |
|------|--------------|
| M3-Dense | 67.8 |
| M3-Sparse | (outperforms BM25 in all languages) |
| M3-Dense + Sparse + Multi-vector | 70.0 |

**Relevance to Our Project:**
- **REFERENCE POINT, NOT DIRECT COMPARISON.** BGE-M3 was trained on MIRACL data, so its high scores are "expected not achieved" (as noted in your project docs). Your mDPR baseline is intentionally weaker to create room for QE improvement.
- **But the principle matters:** A single model with built-in hybrid retrieval (dense+sparse+multi-vector) achieves SOTA. This validates that hybrid > single retriever.
- **Feasible for Colab:** MEDIUM for future work. BGE-M3 is available on HuggingFace but requires re-encoding all 2.1M MIRACL passages. Not feasible as a quick experiment.

---

<a name="area-4"></a>
## Area 4: Adaptive / Selective QE

### Paper 4.1: UniRAG -- Unified Query Understanding Method for Retrieval Augmented Generation

- **Authors:** Rui Li, Liyang He, Qi Liu, Zheng Zhang, Heng Yu, Yuyang Ye, Linbo Zhu, Yu Su
- **Year/Venue:** 2025, ACL 2025 (Main Conference, Vienna)

**Key Mechanism:** UniRAG unifies three query augmentation strategies into a single decoder-only LLM:
1. **Query paraphrasing** (reformulation)
2. **Query expansion** (adding terms)
3. **Query abstraction** (generalization)

The model LEARNS to select the optimal strategy per query based on retrieval and generation feedback. It jointly performs augmentation and encoding, eliminating the separation between "how to expand" and "how to encode."

**Results:**
- Significantly outperforms traditional query augmentation methods across 5 knowledge-intensive benchmarks
- Adaptive selection > always applying the same strategy

**Relevance to Our Project:**
- **CONCEPTUALLY RELEVANT.** The idea that different queries need different expansion strategies is directly applicable. Some of your queries might benefit from pseudo-document generation (Query2Doc), while others might benefit from simple keyword addition or reformulation.
- **Feasible for Colab:** LOW-MEDIUM. UniRAG requires training/fine-tuning a unified model. But the PRINCIPLE of query-level strategy selection could be approximated with a simpler heuristic (e.g., short queries get expansion, long queries get reformulation).

---

### Paper 4.2: Q-PRM -- Adaptive Query Rewriting for RAG via Step-level Process Supervision

- **Authors:** Xiaopeng Ye, Chen Xu, Chaoliang Zhang, Zhaocheng Du, Jun Xu, Gang Wang, Zhenhua Dong
- **Year/Venue:** 2025, Findings of EMNLP 2025

**Key Mechanism:**
1. Uses Monte Carlo Tree Search (MCTS) to generate step-level process supervision signals
2. Reinforced self-training for progressive refinement
3. PRM-guided decoding during inference -- adaptively decides HOW MUCH to rewrite based on query complexity

Addresses the "over-refinement" (simple queries get unnecessarily complex rewrites) and "under-refinement" (complex queries get insufficient rewrites) problems.

**Results:**
- Consistently outperforms baselines across different levels of query complexity
- Handles both simple and complex queries appropriately

**Relevance to Our Project:**
- **INTERESTING but HEAVY.** MCTS + RL training is beyond Colab scope. But the insight that query complexity should guide expansion aggressiveness is valuable.
- **Feasible for Colab:** LOW. Requires substantial training infrastructure.
- **Actionable insight:** Use query length (which you've already analyzed) as a simple proxy for complexity. Apply stronger expansion to short queries, lighter expansion to long ones.

---

### Paper 4.3: DMQR-RAG -- Diverse Multi-Query Rewriting for RAG

- **Authors:** (Multiple authors)
- **Year/Venue:** 2024, arXiv
- **arXiv:** 2411.13154

**Key Mechanism:** Presents FOUR rewriting strategies that operate at different information levels:
1. Information compression (simplify the query)
2. Information supplement (add context)
3. Information transformation (rephrase entirely)
4. Information decomposition (split into sub-queries)

An **adaptive strategy selection method** minimizes the number of rewrites while optimizing performance.

**Results:**
- Effective with small LLMs (Llama3-8B, Qwen2-7B)
- Validated on 15 million real user queries in industry
- Improves hit rate, precision, and response quality

**Relevance to Our Project:**
- **MODERATE.** The four-strategy taxonomy is useful for thinking about QE. Your current approach (Query2Doc = information supplement) is just one strategy. Adding decomposition or transformation might help different query types.
- **Feasible for Colab:** YES. The adaptive selection is lightweight and works with models you already have.

---

### Paper 4.4: QPP-Driven Selective Query Processing -- Limitations

- **Authors:** Various (QPP++ 2025 Workshop at ECIR 2025)
- **Year/Venue:** 2025, ECIR Workshop + ACM TOIS

**Key Finding:** Recent work on QPP (Query Performance Prediction) for selective query processing shows that QPP-driven selective expansion offers **only marginal gains**. The predictors don't generalize well across collections and don't align well with dense retrieval architectures.

**Relevance to Our Project:**
- **CAUTIONARY.** While adaptive QE is appealing, the QPP approach to "predict when to expand" is currently unreliable. Simpler heuristics (query length, query type) may be more practical.
- **Feasible for Colab:** N/A (the research suggests this direction is not yet mature enough to deploy).

---

<a name="area-5"></a>
## Area 5: Fusion Strategies Beyond RRF

### Paper 5.1: An Analysis of Fusion Functions for Hybrid Retrieval

- **Authors:** Sebastian Bruch, Siyu Gai, Amir Ingber
- **Year/Venue:** 2023, ACM Transactions on Information Systems (TOIS), 42(1):1-35
- **arXiv:** 2210.11934

**Key Mechanism:** Systematic comparison of two fusion approaches:
1. **Reciprocal Rank Fusion (RRF):** Merges ranked lists based on reciprocal ranks, ignoring scores
2. **Convex Combination (CC):** s_fused = alpha * s_sparse + (1-alpha) * s_dense, with alpha tuned on a small set

**Critical Findings:**
- **CC outperforms RRF** in both in-domain AND out-of-domain settings
- RRF is sensitive to its k parameter and discards useful score distribution information
- CC is sample-efficient: needs only ~20 queries with ~500 relevance judgments to tune alpha
- Learning CC is agnostic to score normalization choice

**Relevance to Our Project:**
- **DIRECTLY APPLICABLE.** This tells you that for your hybrid pipeline, CC (convex combination) should be your first choice, not RRF. Since you already have both BM25 and mDPR scores, you just need to tune alpha.
- **Feasible for Colab:** YES. Trivial to implement. You have 2,896 dev queries with relevance judgments -- far more than the ~20 queries needed to tune alpha.
- **Note:** The MIRACL paper itself uses CC (alpha=0.5 untuned). Tuning alpha on your data could improve further.

---

### Paper 5.2: HF-RAG -- Hierarchical Fusion-based RAG with Multiple Sources and Rankers

- **Authors:** Santra et al.
- **Year/Venue:** 2025, CIKM 2025 (Seoul)
- **arXiv:** 2509.02837

**Key Mechanism:** Two-stage hierarchical fusion:
1. **Intra-source fusion:** Within each data source, fuse ranked lists from multiple IR models using RRF
2. **Inter-source fusion:** Across sources, apply z-score normalization then merge top documents

**Results:**
- Consistent improvement over best individual ranker or source
- Better out-of-domain generalization than flat fusion

**Relevance to Our Project:**
- **MODERATE.** The hierarchical principle could apply if you have 4 lists: BM25(orig), BM25(expanded), mDPR(orig), mDPR(expanded). First fuse within-retriever (BM25 lists together, mDPR lists together), then fuse across retrievers.
- **Feasible for Colab:** YES. Pure post-processing -- no model training.

---

<a name="area-6"></a>
## Area 6: Dense-Sparse Complementarity with QE

### Paper 6.1: On Complementarity Objectives for Hybrid Retrieval

- **Authors:** Dohyeon Lee, Seung-won Hwang, Kyungjae Lee, Seungtaek Choi, Sunghyun Park
- **Year/Venue:** 2023, ACL 2023 (Main Conference)
- **URL:** https://aclanthology.org/2023.acl-long.746/

**Key Mechanism:** Introduces the **Ratio of Complementarity (RoC)** metric that quantifies how complementary sparse and dense models are to each other. Instead of training dense models to capture "residual" features neglected by sparse models, they propose a two-level orthogonality objective that maximizes RoC.

**Results:**
- Improved RoC directly correlates with improved hybrid retrieval performance
- Outperforms all SOTA methods on MSMARCO-Passage, Natural Questions, and TREC Robust04

**Relevance to Our Project:**
- **THEORETICAL FOUNDATION.** This paper explains WHY hybrid retrieval works: dense and sparse models capture genuinely different signals. Your observation that "BM25 retrieves more docs, mDPR ranks them better" (from your baseline comparison) is exactly this complementarity.
- **Implications for QE:** If QE makes the dense retriever's signal MORE similar to the sparse retriever's signal (by adding keywords), it REDUCES complementarity. This could explain why QE helps dense (adds missing keyword signals) but hurts sparse (adds noise that confuses exact matching without adding new signal).
- **Feasible for Colab:** The RoC metric itself is computable from your existing results. You could measure how complementary BM25 and mDPR are before/after QE.

---

### Paper 6.2: Generative Query Expansion with Multilingual LLMs for Cross-Lingual Information Retrieval

- **Authors:** (Not fully specified)
- **Year/Venue:** November 2025, arXiv
- **arXiv:** 2511.19325

**Key Mechanism:** Evaluates multiple generative expansion strategies (pseudo-document generation, CoT prompting, Rephrase-and-Respond) for cross-lingual retrieval. Tests on CLIRMatrix with Arabic, Chinese, English, Spanish.

**Critical Findings for Arabic:**
- **Query length determines which prompting technique is effective** -- more elaborate prompts do NOT yield further gains for short queries
- **Meta-text pollution:** For CoT prompting and RaR, the LLM generates meta-text like "To answer this query, I will provide information about..." which ADVERSELY affects BM25 retrieval
- Cross-lingual QE produces the LARGEST improvements for languages with the WEAKEST baselines
- **Script differences** between query and document language severely degrade retrieval

**Relevance to Our Project:**
- **DIRECTLY RELEVANT.** This paper explicitly studies Arabic QE and confirms that:
  - (a) BM25 is hurt by LLM meta-text (matches your observation)
  - (b) Arabic benefits MORE from QE than high-resource languages
  - (c) Simple pseudo-document generation often outperforms complex prompting for short queries
- **Feasible for Colab:** YES. No new infrastructure -- just different prompting strategies.

---

### Paper 6.3: Information Retrieval with Dense and Sparse Representations (MIT Thesis)

- **Authors:** Yung-Sung Chuang
- **Year/Venue:** 2024, MIT Master's Thesis
- **URL:** https://dspace.mit.edu/handle/1721.1/153774

**Key Analysis of Why Dense and Sparse Respond Differently:**

Dense methods capture conceptual/semantic similarity (embeddings map meaning), while sparse methods capture exact-term precision (BM25 matches literal tokens). When QE adds semantically related content:
- **Dense benefits:** The expanded text shifts the embedding toward the relevant semantic region, even if specific words differ
- **Sparse suffers:** The expanded text introduces many new terms, diluting the term-frequency signal of the original query terms, and potentially introducing high-IDF irrelevant terms that attract wrong documents

**Relevance to Our Project:**
- **EXPLAINS YOUR CORE OBSERVATION.** This is the theoretical foundation for why 6/9 models degraded BM25 but improved dense. The keyword terms in your pseudo-documents have high IDF (they're specific/rare), so BM25 weights them heavily, pulling results toward the pseudo-document's topic rather than the original query.

---

<a name="surveys"></a>
## Cross-Cutting Survey Papers

### Survey S1: Query Expansion in the Age of Pre-trained and Large Language Models: A Comprehensive Survey

- **Authors:** Minghan Li et al. (Soochow University)
- **Year/Venue:** 2025, arXiv
- **arXiv:** 2509.07794 (v2, October 2025)

**Key Taxonomy (4 dimensions):**
1. **Model architecture:** Encoder-only vs. encoder-decoder vs. decoder-only
2. **Grounding:** Zero-grounding (pure LLM) vs. corpus-grounded (PRF-based)
3. **Interaction:** Non-interactive (single-pass) vs. interactive (multi-turn with feedback)
4. **Training:** Training-free vs. fine-tuned

**Key Insights Relevant to Your Work:**
- Zero-grounding methods (like your Query2Doc) risk drift and hallucination
- Grounding methods (like CSQE from your Phase 4 review) curb hallucination by anchoring in corpus
- For sparse retrieval, pseudo-references need repeated copies of original query to balance BM25's TF sensitivity
- Decoder-only LLMs (like your Aya/Jais-2) unlock zero-shot expansion but need careful prompt design

---

<a name="synthesis"></a>
## Synthesis: Implications for Our Project

### The Opportunity Matrix

Based on this review, here are the most impactful experiments ranked by expected impact and feasibility:

| Priority | Experiment | Expected Impact | Feasibility | New Code Needed |
|----------|-----------|----------------|-------------|----------------|
| 1 | **Hybrid baseline (BM25+mDPR, CC fusion)** | VERY HIGH (+34.8% over mDPR) | Trivial | Score normalization + CC |
| 2 | **QE + Hybrid (expand, then fuse)** | HIGH | Easy | Run existing QE + fusion |
| 3 | **Exp4Fuse-style dual-list fusion** | HIGH | Easy | Run BM25 twice (orig + expanded), fuse |
| 4 | **Retriever-specific prompts (LevelRAG-lite)** | MEDIUM-HIGH | Easy | Two prompt templates |
| 5 | **MuGI-style multi-sample expansion** | MEDIUM | Moderate (5x gen time) | Multiple LLM calls + reweighting |
| 6 | **Multi-model ensemble (MPQE-lite)** | MEDIUM | Moderate | Run 2-3 models + cluster/filter |
| 7 | **Adaptive QE by query length** | LOW-MEDIUM | Easy | Simple heuristic |

### Recommended Experimental Plan

**Phase 4a: Establish Hybrid Baseline (1-2 days)**
1. Take your existing BM25 and mDPR result files
2. Normalize scores to [0,1]
3. Compute hybrid scores with CC: s = alpha * s_BM25 + (1-alpha) * s_mDPR
4. Sweep alpha in {0.3, 0.4, 0.5, 0.6, 0.7} on dev set
5. Report nDCG@10, Recall@10, MRR

Expected result: nDCG@10 around 0.60-0.67 (even with your slightly different baselines)

**Phase 4b: QE + Hybrid (2-3 days)**
1. Take your best QE model (Aya Expanse 8B) expanded queries
2. Run BM25 on expanded queries (you may already have this)
3. Run mDPR on expanded queries (you already have this)
4. Compute 4-way hybrid: BM25(orig) + BM25(expanded) + mDPR(orig) + mDPR(expanded)
5. Try both CC and RRF fusion

Expected result: This should be your BEST configuration, combining the complementarity of BM25+mDPR with the semantic enrichment of QE.

**Phase 4c: Retriever-Specific Prompts (2-3 days)**
1. Design a BM25-optimized prompt: "Generate Arabic keywords and terms related to: {query}"
2. Design an mDPR-optimized prompt: "Generate a detailed Arabic paragraph about: {query}" (your current Query2Doc prompt)
3. Run each retriever with its optimized expansion
4. Fuse with CC

Expected result: BM25 should improve (keyword expansion matches its term-matching nature), while mDPR maintains or improves its current gains.

### Key Insight for Your Thesis

**The central argument writes itself:** Dense and sparse retrievers have complementary failure modes. QE helps dense but hurts sparse because pseudo-documents shift retrieval from keyword-matching toward semantic matching. The solution is:
1. Use retriever-appropriate expansion strategies
2. Fuse results from both retrievers (hybrid retrieval)
3. Fuse results from both expanded and unexpanded queries (dual-list fusion)

This three-level fusion approach (retriever fusion + expansion fusion + retriever-specific expansion) is novel and directly builds on your existing Query2Doc infrastructure.

---

## Papers Not Yet Published / Under Review

Several promising papers were found at workshops or under review:
- QPP++ 2025 Workshop papers (ECIR 2025) on QPP in the LLM era
- ExpandSearch (arXiv 2510.10009) on RL-trained query expansion with selective distillation
- ThinkQE (arXiv 2506.09260) on evolving thinking processes for QE

These are tracked here for future reference but not recommended for immediate experiments.

---

## Full Citation List

1. Liu et al. (2025). "Exp4Fuse: A Rank Fusion Framework for Enhanced Sparse Retrieval using LLM-based Query Expansion." Findings of ACL 2025. arXiv:2506.04760.
2. Rackauckas (2024). "RAG-Fusion: A New Take on Retrieval-Augmented Generation." arXiv:2402.03367.
3. Zhang, Feng, Zhang (2025). "LevelRAG: Enhancing RAG with Multi-hop Logic Planning over Rewriting Augmented Searchers." arXiv:2502.18139.
4. Zhang, Wu, Yang, Nie (2024). "MuGI: Multi-Text Generation Integration for Information Retrieval." Findings of EMNLP 2024. arXiv:2401.06311.
5. (2025). "MPQE: Multi-Model Pseudo-Document Generation and Reconstruction for Hybrid Query Expansion." Information Processing & Management.
6. Zhang, Thakur, Ogundepo et al. (2023). "MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages." TACL. arXiv:2210.09984.
7. Chen, Xiao, Zhang et al. (2024). "BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings." arXiv:2402.03216.
8. Li, He, Liu et al. (2025). "UniRAG: Unified Query Understanding Method for RAG." ACL 2025.
9. Ye, Xu, Zhang et al. (2025). "Q-PRM: Adaptive Query Rewriting for RAG via Step-level Process Supervision." Findings of EMNLP 2025.
10. (2024). "DMQR-RAG: Diverse Multi-Query Rewriting for RAG." arXiv:2411.13154.
11. Bruch, Gai, Ingber (2023). "An Analysis of Fusion Functions for Hybrid Retrieval." ACM TOIS 42(1):1-35. arXiv:2210.11934.
12. Santra et al. (2025). "HF-RAG: Hierarchical Fusion-based RAG." CIKM 2025. arXiv:2509.02837.
13. Lee, Hwang, Lee et al. (2023). "On Complementarity Objectives for Hybrid Retrieval." ACL 2023.
14. (2025). "Generative Query Expansion with Multilingual LLMs for Cross-Lingual IR." arXiv:2511.19325.
15. Chuang (2024). "Information Retrieval with Dense and Sparse Representations." MIT Master's Thesis.
16. Li et al. (2025). "Query Expansion in the Age of Pre-trained and Large Language Models: A Comprehensive Survey." arXiv:2509.07794.
17. (2025). "Uncovering the Limitations of QPP: Failures, Insights, and Implications." ACM TOIS. arXiv:2504.01101.
