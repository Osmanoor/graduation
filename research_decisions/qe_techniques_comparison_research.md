# QE Techniques Comparison Research: Alternatives & Extensions to Query2Doc

**Date:** 2026-03-28
**Status:** Research Complete
**Task:** 6.1 (Literature review -- QE technique landscape)
**Purpose:** Map the space of LLM-based QE techniques that could be compared with or combined with our Query2Doc pipeline

---

## Executive Summary

This document surveys the major LLM-based query enhancement techniques beyond Query2Doc, organized by mechanism. Our project already has strong Query2Doc results (up to +23.5% NDCG@10 with Aya Expanse 8B on MIRACL Arabic). The question is: what else exists, how does it differ, and could any of these improve or complement our work?

**Key Finding:** The techniques fall into a clear taxonomy:

| Category | Technique | How it differs from Query2Doc |
|----------|-----------|-------------------------------|
| Embed pseudo-doc | **HyDE** | Embeds the pseudo-doc instead of concatenating |
| Multiple generations | **MuGI**, **GRF** | Generates multiple pseudo-docs, aggregates |
| Replace query | **Rewrite-Retrieve-Read**, **RaFe** | Rewrites query entirely instead of expanding |
| Multi-query | **RAG-Fusion**, **DMQR-RAG** | Generates multiple diverse queries |
| Iterative loop | **ITER-RETGEN**, **IRCoT** | Retrieve-generate-retrieve loops |
| CoT reasoning | **CoT-QE** (Jagerman et al.) | Uses chain-of-thought to decompose/expand |
| Corpus-grounded | **CSQE**, **ProQE** | Grounds expansion in retrieved documents |
| Learned (training-based) | **SoftQE**, **RQ-RAG** | Trains encoder/LLM to internalize expansion |

**Most promising for our project (AI Suggestion):**
1. **HyDE** -- direct comparison (same generation, different usage)
2. **GRF** -- multiple generation subtasks, strong results
3. **CSQE** -- corpus-grounded extension of Query2Doc (already in Phase 4 review)
4. **MuGI** -- multiple pseudo-documents, training-free

---

## 1. HyDE: Hypothetical Document Embeddings

### Paper Details
- **Title:** Precise Zero-Shot Dense Retrieval without Relevance Labels
- **Authors:** Luyu Gao, Xueguang Ma, Jimmy Lin, Jamie Callan
- **Year/Venue:** 2022, ACL 2023 (Long Paper)
- **arXiv:** [2212.10496](https://arxiv.org/abs/2212.10496)
- **Code:** Available (Contriever-based)

### Key Mechanism
1. Given a query, prompt an LLM (InstructGPT) to generate a hypothetical document that would answer the query
2. **Encode the hypothetical document** (not the query) using an unsupervised dense encoder (Contriever)
3. Use the resulting embedding to retrieve real documents via vector similarity

**Critical difference from Query2Doc:** HyDE **replaces the query embedding** with the pseudo-document embedding. Query2Doc **concatenates** the pseudo-document text with the original query, then encodes the combined text. This means:
- HyDE: query information is *implicit* in the pseudo-doc embedding (original query is discarded for retrieval)
- Query2Doc: query information is *preserved* alongside the expansion (original query is kept)

### Results on Standard Benchmarks
- Outperforms Contriever (unsupervised SOTA) across web search, QA, fact verification
- Competitive with fine-tuned retrievers (DPR, ANCE) in zero-shot setting
- Tested on: MS-MARCO, Natural Questions, TriviaQA, FEVER, TREC DL
- Multilingual: Tested on Swahili, Korean, Japanese, Bengali (Mr.TyDi) -- **no Arabic results reported**

### Arabic / Multilingual Status
- Original paper tests non-English via Mr.TyDi (Swahili, Korean, Japanese, Bengali)
- **No direct Arabic evaluation in original paper**
- Relies on multilingual encoder (Contriever/mContriever) -- should work for Arabic in principle
- The 2025 paper by Macmillan-Scott et al. (arXiv:2511.19325) evaluates HyDE-style expansion for Arabic with Aya Expanse (see Section 8 below)

### Feasibility on Colab
- **HIGH.** Same generation step as Query2Doc (we already have this). The only change is *how* the pseudo-document is used for retrieval (embedding vs concatenation)
- Requires: a multilingual dense encoder (we already use mDPR)
- Additional cost: re-encoding pseudo-documents through mDPR (but mDPR is fast)
- **Implementation note:** For dense retrieval, HyDE embeds ONLY the pseudo-doc. For sparse (BM25), HyDE is not directly applicable without concatenation (which is just Query2Doc)

### Relevance Assessment
- **Directly comparable to Query2Doc** -- same input (LLM-generated pseudo-document), different usage
- We could run HyDE using the same pseudo-documents we already generated for Query2Doc experiments
- **Key experiment:** Compare HyDE vs Query2Doc using identical pseudo-documents from Aya/Jais-2
- HyDE assumes pseudo-doc and real doc share semantic space -- may break for Arabic if encoder is weak on Arabic

---

## 2. GRF: Generative Relevance Feedback

### Paper Details
- **Title:** Generative Relevance Feedback with Large Language Models
- **Authors:** Iain Mackie, Shubham Chatterjee, Jeffrey Dalton
- **Year/Venue:** 2023, SIGIR 2023 (Taipei, Taiwan)
- **arXiv:** [2304.13157](https://arxiv.org/abs/2304.13157)
- **Affiliation:** University of Glasgow

### Key Mechanism
1. Prompt an LLM (GPT-3/text-davinci-002) to generate long-form text about the query
2. **Vary the generation subtask:** queries, entities, facts, news articles, documents, essays
3. Build a **probabilistic feedback model** (like RM3/RM1) from the generated text
4. Use the feedback model for expansion (not simple concatenation)

**Critical difference from Query2Doc:** GRF treats the LLM output as a *pseudo-relevant document set* and applies classical relevance feedback (RM3) on it. Query2Doc simply concatenates. GRF also systematically varies the *type* of generation (essays vs entities vs facts).

### Results on Standard Benchmarks
- MAP: +5-19% over RM3 expansion
- NDCG@10: +17-24% over RM3 expansion
- Best R@1k on all tested datasets vs sparse, dense, and expansion baselines
- Long-form generation (essays, documents) is 7-14% more effective than short-form (entities, keywords)
- Tested on: TREC Robust04, TREC DL 2019/2020

### Arabic / Multilingual Status
- **Not tested on Arabic or multilingual settings**
- Uses English-only datasets and GPT-3
- The probabilistic feedback model (RM3) is language-agnostic in principle
- Would need Arabic LLM generation + Arabic RM3 implementation

### Feasibility on Colab
- **MEDIUM.** The generation step is the same as Query2Doc. The RM3 feedback model adds complexity but is computationally light. The main challenge is implementing RM3 in Python for Arabic (tokenization, stemming). BM25S could potentially be adapted.
- **Alternative:** Skip RM3, just test whether generating different text types (essays vs documents vs facts) affects Query2Doc performance. This is very easy to implement.

### Relevance Assessment
- **The "vary generation subtask" finding is highly actionable** -- we could test different prompt types with our existing models
- We already generate "pseudo-documents"; we could also generate "pseudo-facts", "pseudo-essays", etc.
- The RM3 feedback model is more complex but could be a Phase 4 extension

---

## 3. MuGI: Multi-Text Generation Integration

### Paper Details
- **Title:** Exploring the Best Practices of Query Expansion with Large Language Models (MuGI)
- **Authors:** Le Zhang, Yihong Wu
- **Year/Venue:** 2024, arXiv (SIGIR 2024 submission)
- **arXiv:** [2401.06311](https://arxiv.org/abs/2401.06311)

### Key Mechanism
1. Prompt an LLM **multiple times** (N samples) to generate pseudo-references
2. **Integrate** multiple pseudo-documents with the original query at a specified ratio
3. Use the expanded query for retrieval (both sparse and dense)

**Critical difference from Query2Doc:** Query2Doc generates ONE pseudo-document. MuGI generates MULTIPLE (typically 5-10) and aggregates them. This reduces noise from any single hallucinated generation.

### Results on Standard Benchmarks
- BM25 + MuGI: +18% on TREC DL, +7.5% on BEIR
- Outperforms HyDE and Query2Doc on BM25
- Enables BM25 to outperform dense retrievers (ANCE, DPR)
- A 110M retriever + MuGI outperforms a 7B model baseline
- Training-free

### Arabic / Multilingual Status
- **Not tested on Arabic** -- evaluated on English benchmarks (TREC DL, BEIR, MS-MARCO)

### Feasibility on Colab
- **HIGH but with cost tradeoff.** Same pipeline as Query2Doc but run N times. For 2,896 queries x 5 generations = ~14,480 generations. On A100 with Aya/Jais-2, this could take 5x longer (from ~1hr to ~5hrs). On T4 it may be prohibitive.
- **Easy experiment:** Generate 3-5 pseudo-docs per query with temperature>0, average or concatenate them

### Relevance Assessment
- **Directly extends Query2Doc** -- same mechanism, multiple samples
- Could use existing infrastructure with minimal code changes (just loop generation)
- Addresses a known weakness: single pseudo-document may hallucinate or miss key terms
- **Key question:** Does Arabic benefit more from multiple generations? (morphological richness could mean more variation)

---

## 4. Query Rewriting (Replace vs Expand)

### 4a. Rewrite-Retrieve-Read

#### Paper Details
- **Title:** Query Rewriting for Retrieval-Augmented Large Language Models
- **Authors:** Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, Nan Duan
- **Year/Venue:** 2023, EMNLP 2023
- **arXiv:** [2305.14283](https://arxiv.org/abs/2305.14283)

#### Key Mechanism
1. An LLM **rewrites** the query (not expands -- the original query is replaced)
2. The rewritten query is used for retrieval (web search or dense)
3. Retrieved documents are read by the LLM for final answer
4. **Trainable variant:** A small LM is trained as a rewriter using RL from LLM reader feedback

**Critical difference from Query2Doc:** Query2Doc ADDS information to the query. Rewriting REPLACES the query. Rewriting risks losing information from the original query; expansion risks adding noise.

#### Results
- Consistent improvement on open-domain QA and multiple-choice QA
- The trainable rewriter outperforms zero-shot prompting

#### Feasibility on Colab
- **HIGH for zero-shot variant.** Just change the prompt from "generate a document about this query" to "rewrite this query to be more search-friendly"
- **LOW for trainable variant.** Requires RL training loop, which is complex and compute-heavy

---

### 4b. RaFe: Ranking Feedback Improves Query Rewriting

#### Paper Details
- **Title:** RaFe: Ranking Feedback Improves Query Rewriting for RAG
- **Authors:** Shengyu Mao, Yong Jiang, Boli Chen, Xiao Li, Peng Wang, et al.
- **Year/Venue:** 2024, EMNLP 2024 Findings
- **arXiv:** [2405.14431](https://arxiv.org/abs/2405.14431)

#### Key Mechanism
1. Train a query rewriting model via supervised fine-tuning
2. Use a **reranker's scores** as feedback to further train the rewriter
3. Two-stage: SFT first, then ranking-feedback training

**Critical difference from Query2Doc:** Requires training. Uses feedback from a reranker to optimize rewrites.

#### Feasibility on Colab
- **LOW.** Requires SFT + feedback training of a rewriter model. Not feasible for comparison experiments.

---

### 4c. DMQR-RAG: Diverse Multi-Query Rewriting

#### Paper Details
- **Title:** DMQR-RAG: Diverse Multi-Query Rewriting for RAG
- **Authors:** Hangyu Mao et al. (Renmin University, Kuaishou Technology)
- **Year/Venue:** 2024, arXiv (ICLR 2025 submission, withdrawn)
- **arXiv:** [2411.13154](https://arxiv.org/abs/2411.13154)

#### Key Mechanism
1. Generate **multiple rewritten queries** using four different strategies:
   - GQR: Remove noise, clarify intent
   - KWR: Extract keywords for search engines
   - PAR: Generate pseudo-answer to broaden the query
   - CCE: Extract key contextual information
2. **Adaptive strategy selection** minimizes rewrites while optimizing performance
3. Uses reciprocal rank fusion to combine results

**Critical difference from Query2Doc:** Multiple diverse rewrites vs single expansion. Each rewrite targets a different aspect of query quality.

#### Results
- P@5 improved by up to 14.46% on FreshQA
- Surpasses RAG-Fusion in most metrics
- Tested on AmbigNQ, HotpotQA, FreshQA

#### Feasibility on Colab
- **MEDIUM.** The zero-shot variant (just prompting for different rewrite types) is easy. The adaptive selection requires more engineering. Could prototype with 2-3 rewrite strategies.

---

## 5. Chain-of-Thought Query Expansion

### 5a. CoT-QE (Jagerman et al.)

#### Paper Details
- **Title:** Query Expansion by Prompting Large Language Models
- **Authors:** Rolf Jagerman, Honglei Zhuang, Zhen Qin, Xuanhui Wang, Michael Bendersky
- **Year/Venue:** 2023, arXiv
- **arXiv:** [2305.03653](https://arxiv.org/abs/2305.03653)
- **Affiliation:** Google

#### Key Mechanism
1. Prompt an LLM with zero-shot, few-shot, or **Chain-of-Thought (CoT)** prompts
2. CoT prompts instruct the model to break down the query step-by-step
3. The CoT reasoning produces related terms and context
4. These terms are used for query expansion

**Critical difference from Query2Doc:** Query2Doc generates a pseudo-document. CoT-QE generates a *reasoning chain* that decomposes the query, then extracts expansion terms from that chain. CoT-QE is more structured/analytical; Query2Doc is more generative/creative.

#### Results
- CoT prompts outperform zero-shot and few-shot for expansion on MS-MARCO and BEIR
- LLM-generated expansions outperform traditional QE methods (RM3, Bo1)
- CoT is "especially useful" because it provides many related terms

#### Arabic / Multilingual Status
- **Not tested on Arabic.** English-only evaluation.

#### Feasibility on Colab
- **HIGH.** Just a different prompt. Instead of "Write a passage about [query]", use "Think step by step about what [query] is asking. What are the key concepts? What related terms would help find relevant documents?"
- Could test with existing Aya/Jais-2 models immediately

---

### 5b. IRCoT: Interleaving Retrieval with Chain-of-Thought

#### Paper Details
- **Title:** Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions
- **Authors:** Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, Ashish Sabharwal
- **Year/Venue:** 2022/2023, ACL 2023
- **arXiv:** [2212.10509](https://arxiv.org/abs/2212.10509)
- **Code:** [github.com/StonyBrookNLP/ircot](https://github.com/StonyBrookNLP/ircot)

#### Key Mechanism
1. Generate a CoT reasoning step
2. Use that step to retrieve relevant documents
3. Use retrieved documents to inform the next CoT step
4. Repeat: interleave retrieval and reasoning

**Critical difference from Query2Doc:** Query2Doc is a single-shot generate-then-retrieve. IRCoT is multi-step: reason-retrieve-reason-retrieve in a loop. Designed for multi-hop questions.

#### Results
- Retrieval: up to +21 points improvement
- QA: up to +15 points improvement
- Tested on: HotpotQA, 2WikiMultihopQA, MuSiQue, IIRC

#### Feasibility on Colab
- **LOW-MEDIUM.** Multi-step retrieval requires multiple LLM calls AND multiple retrieval calls per query. For 2,896 queries with 3-5 steps each, this is 9K-15K LLM calls + retrieval calls. Feasible on A100 but slow. Not designed for single-hop factoid queries (which most MIRACL queries are).

### Relevance Assessment
- Less relevant to our setting (MIRACL is mostly single-hop factoid retrieval)
- Could be relevant for the subset of complex/ambiguous queries in our error analysis

---

## 6. Iterative Retrieval-Generation

### ITER-RETGEN

#### Paper Details
- **Title:** Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy
- **Authors:** Zhihong Shao, Yeyun Gong, Yelong Shen, Minlie Huang, Nan Duan, Weizhu Chen
- **Year/Venue:** 2023, EMNLP 2023 Findings
- **arXiv:** [2305.15294](https://arxiv.org/abs/2305.15294)

#### Key Mechanism
1. Generate an initial response to the query
2. Use the response as additional context for retrieval
3. Retrieve better documents using the enriched query
4. Generate a better response using the new documents
5. Repeat for T iterations

**Critical difference from Query2Doc:** Query2Doc does step 1 only (generate pseudo-doc, retrieve once). ITER-RETGEN loops: the retrieved documents inform a better generation, which informs better retrieval. It is essentially "Query2Doc applied iteratively."

#### Results
- Superior to or competitive with SOTA on multi-hop QA, fact verification, commonsense reasoning
- Fewer retrieval/generation overheads compared to IRCoT (processes all retrieved knowledge as a whole)

#### Feasibility on Colab
- **MEDIUM.** 2-3 iterations would be feasible. Each iteration requires one LLM generation + one retrieval pass. For 2,896 queries x 2 iterations = ~6K LLM calls + 6K retrieval calls. On A100 this is ~2-3 hours.
- **Simplified version:** Just do TWO passes: (1) Query2Doc as normal, (2) use retrieved documents to generate a better pseudo-document, then retrieve again. This is very similar to CSQE from Phase 4 review.

---

## 7. Multi-Stage Retrieval Pipelines

### 7a. RAG-Fusion

#### Paper Details
- **Title:** RAG-Fusion: A New Take on Retrieval-Augmented Generation
- **Authors:** Zackary Rackauckas (Infineon Technologies)
- **Year/Venue:** 2024, arXiv
- **arXiv:** [2402.03367](https://arxiv.org/abs/2402.03367)

#### Key Mechanism
1. Generate **multiple query variations** from the original query
2. Retrieve documents for EACH query variation
3. Fuse results using **Reciprocal Rank Fusion (RRF)**
4. Feed the fused, reranked documents to the LLM

**Critical difference from Query2Doc:** Query2Doc generates one pseudo-document and retrieves once. RAG-Fusion generates multiple queries and retrieves multiple times, then fuses. Query2Doc expands the query; RAG-Fusion diversifies it.

#### Feasibility on Colab
- **MEDIUM.** Generating 3-5 query variants is easy. Running retrieval for each is more work (3-5x retrieval time). RRF is trivially implementable. Total: ~5x cost of baseline.

---

### 7b. FlashRank Two-Stage Pipeline

#### Paper Details
- **Title:** Enhancing Retrieval-Augmented Generation with Two-Stage Retrieval: FlashRank Reranking and Query Expansion
- **Year/Venue:** 2025, arXiv
- **arXiv:** [2601.03258](https://arxiv.org/abs/2601.03258)

#### Key Mechanism
1. Expand query with LLM-generated synonyms and context terms
2. Retrieve candidate documents (broad recall)
3. Rerank using FlashRank (marginal-utility reranker under token budget)
4. Select optimal evidence subset

#### Results
- NDCG@10: up to +5.4% on MS-MARCO, BEIR
- Generation accuracy: +6-8%
- Context tokens reduced by 35%
- Execution: <60ms for 100 candidates

#### Feasibility on Colab
- **HIGH.** Two-stage (expand + rerank) is straightforward. FlashRank is a lightweight reranker. We already have expansion; adding a cross-encoder reranker is the main addition.

---

## 8. Direct Comparisons: HyDE vs Query2Doc

### Paper: "Hypothetical Documents or Knowledge Leakage?"
- **Title:** Hypothetical Documents or Knowledge Leakage? Rethinking LLM-based Query Expansion
- **Authors:** Yejun Yoon, Jaeyoon Jung, Seunghyun Yoon, Kunwoo Park
- **Year/Venue:** 2025, arXiv
- **arXiv:** [2504.14175](https://arxiv.org/abs/2504.14175)

**Key Findings:**
- Directly compares HyDE and Query2Doc across multiple datasets and LLM backbones
- Questions whether performance gains come from "hypothetical document" quality or **knowledge leakage** (LLM memorizing benchmark answers)
- Performance improvements **consistently occur for claims whose generated documents contain information entailed by gold evidence**
- Implication: LLM-based QE (both HyDE and Query2Doc) benefits most when the LLM already "knows" the answer -- raises concerns about evaluation on benchmark datasets

**Relevance to our work:** This is a critical methodological concern. MIRACL Arabic is less likely to be memorized by English-centric LLMs, so our results may be *more genuine* than English-benchmark results. This is actually a strength of evaluating on Arabic.

---

## 9. Survey Papers on LLM-Based Query Expansion

### Survey 1: Query Expansion in the Age of PLMs and LLMs
- **Title:** Query Expansion in the Age of Pre-trained and Large Language Models: A Comprehensive Survey
- **Authors:** Minghan Li, Xinxuan Lv, Junjie Zou, Tongna Chen, Chao Zhang, et al.
- **Year/Venue:** 2025, arXiv
- **arXiv:** [2509.07794](https://arxiv.org/abs/2509.07794)
- **Taxonomy dimensions:** (1) injection point (implicit/embedding vs explicit/selection), (2) grounding (zero-grounding to multi-round loops), (3) learning (SFT/PEFT/DPO)
- **Covers:** HyDE, Query2Doc, GRF, MuGI, CSQE, CoT-QE, and more

### Survey 2: A Survey of Query Optimization in LLMs
- **Title:** A Survey of Query Optimization in Large Language Models
- **Year/Venue:** 2024, arXiv
- **arXiv:** [2412.17558](https://arxiv.org/abs/2412.17558)
- **Evolutionary stages:** Foundation Era (2020-2022) -> Expansion Era (2022-2024) -> Sophistication Era (2024-2025) -> Agentic Era (2025-2026)

### Survey 3: LLMs for Information Retrieval
- **Title:** Large Language Models for Information Retrieval: A Survey
- **Year/Venue:** 2023-2025, ACM TOIS
- **arXiv:** [2308.07107](https://arxiv.org/abs/2308.07107)
- **Covers:** Query rewriters, retrievers, rerankers, readers

---

## 10. Arabic / Multilingual QE with LLMs

### Paper: Generative QE with Multilingual LLMs for CLIR
- **Title:** Generative Query Expansion with Multilingual LLMs for Cross-Lingual Information Retrieval
- **Authors:** Olivia Macmillan-Scott, Roksana Goworek, Eda B. Ozyigit
- **Year/Venue:** November 2025, arXiv
- **arXiv:** [2511.19325](https://arxiv.org/abs/2511.19325)

**Key Findings:**
- Evaluates HyDE-style and Query2Doc-style expansion with multilingual LLMs
- Tests across Arabic, Chinese, English, Spanish using CLIRMatrix
- Uses **Aya Expanse 8B** (same model as our best performer) and fine-tuned variants
- **Query length determines which prompting technique works:** zero-shot best for short queries, few-shot best for longer queries
- More elaborate prompts often do NOT yield further gains
- LLM-based QE consistently improves over original queries

**CRITICAL relevance to our project:** This paper directly validates our approach (LLM-based QE for Arabic with Aya Expanse). It also provides insights on prompt design for Arabic that we should incorporate.

### Paper: Improved Arabic Query Expansion Using Word Embedding
- **Year/Venue:** 2025, Scientific Reports (Nature)
- **Key Finding:** Arabic morphology requires special processing; subset training of embeddings reduces time by 90% while preserving retrieval quality

### Paper: LLM-based QE Fails for Unfamiliar and Ambiguous Queries
- **Title:** LLM-based Query Expansion Fails for Unfamiliar and Ambiguous Queries
- **Authors:** (not specified)
- **Year/Venue:** 2025, SIGIR 2025
- **arXiv:** [2505.12694](https://arxiv.org/abs/2505.12694)

**Key Findings:**
- QE effectiveness **degrades when LLM is unfamiliar with the query topic**
- LLMs privilege popular entities -> QE is less effective for ambiguous queries
- This is especially relevant for Arabic: many Arabic-specific topics may be underrepresented in LLM training data

---

## 11. Additional Notable Techniques

### RQ-RAG: Learning to Refine Queries
- **arXiv:** [2404.00610](https://arxiv.org/abs/2404.00610) (2024)
- **Mechanism:** Trains a 7B model to dynamically refine queries via rewriting, decomposing, and disambiguating
- **Results:** +1.9% avg over SOTA on 3 single-hop QA datasets
- **Feasibility:** LOW (requires training)

### SoftQE: Learned Representations of Queries Expanded by LLMs
- **arXiv:** [2402.12663](https://arxiv.org/abs/2402.12663) (2024, Amazon)
- **Mechanism:** Trains query encoder to produce embeddings similar to LLM-expanded query embeddings. No LLM needed at inference.
- **Results:** +2.83% avg on BEIR out-of-domain tasks
- **Feasibility:** LOW (requires training query encoder)

### ProQE: Progressive Query Expansion
- **arXiv:** [2406.07136](https://arxiv.org/abs/2406.07136) (2024)
- **Mechanism:** Iteratively expands query by extracting key terms from each retrieved document, one document at a time
- **Results:** +37% over baselines; most cost-effective
- **Feasibility:** MEDIUM (iterative but lightweight per step)

---

## 12. Feasibility Matrix for Our Project

Rated for: Google Colab (T4 15GB / A100 40GB), 2-8B models, MIRACL Arabic (2,896 queries)

| Technique | Training Required? | Compute Cost (vs Query2Doc) | Implementation Difficulty | Arabic Tested? | Feasibility |
|-----------|-------------------|---------------------------|--------------------------|----------------|-------------|
| **HyDE** | No | ~1x (same generation) | LOW (change how pseudo-doc is used) | Indirect (Mr.TyDi) | **HIGH** |
| **GRF (varied prompts)** | No | ~1x per prompt type | LOW (different prompts) | No | **HIGH** |
| **MuGI (multi-gen)** | No | ~5x (N generations) | LOW (loop generation) | No | **MEDIUM-HIGH** |
| **CoT-QE** | No | ~1x (different prompt) | LOW (different prompt) | No | **HIGH** |
| **RAG-Fusion** | No | ~3-5x (multi-query retrieval) | MEDIUM (RRF implementation) | No | **MEDIUM** |
| **DMQR-RAG (zero-shot)** | No | ~4x (4 rewrite strategies) | MEDIUM (4 prompt types + fusion) | No | **MEDIUM** |
| **ITER-RETGEN (2 iter)** | No | ~2x (2 passes) | MEDIUM (retrieval loop) | No | **MEDIUM** |
| **Rewrite-Retrieve-Read** | No (zero-shot) | ~1x | LOW (different prompt) | No | **HIGH** |
| **CSQE** | No | ~2x (first-pass retrieval) | MEDIUM (retrieve + re-prompt) | No | **MEDIUM-HIGH** |
| **FlashRank (2-stage)** | No | ~1.5x (+ reranker) | MEDIUM (add reranker) | No | **MEDIUM-HIGH** |
| **ProQE** | No | ~3-5x (iterative) | MEDIUM-HIGH (iterative loop) | No | **MEDIUM** |
| **RQ-RAG** | Yes (SFT) | High | HIGH | No | **LOW** |
| **SoftQE** | Yes (encoder) | High | HIGH | No | **LOW** |
| **RaFe** | Yes (SFT+RL) | High | HIGH | No | **LOW** |
| **IRCoT** | No | ~5-10x (multi-hop) | HIGH (interleaved loop) | No | **LOW** |

---

## 13. Recommended Experiments (AI Suggestion)

Based on feasibility, scientific value, and complementarity with our existing Query2Doc results:

### Tier 1: Immediate (same generation, different usage -- minimal effort)

1. **HyDE comparison** -- Use existing pseudo-documents from Aya/Jais-2, embed them with mDPR, compare vs Query2Doc concatenation. Tests whether embedding or concatenation is better for Arabic.
   - *Effort:* ~2 hours implementation, ~1 hour runtime
   - *Scientific value:* Very high (direct HyDE vs Query2Doc comparison on Arabic -- novel)

2. **CoT-QE prompt** -- Replace Query2Doc prompt with a CoT prompt ("Think step by step about what this query needs"). Same model (Aya or Jais-2), same pipeline.
   - *Effort:* ~1 hour (prompt change only)
   - *Scientific value:* High (tests whether reasoning-based expansion beats document-style expansion for Arabic)

3. **Query Rewriting** -- Instead of "generate a document about [query]", prompt "rewrite [query] to be more specific and detailed for search". Compare expansion vs replacement.
   - *Effort:* ~1 hour (prompt change only)
   - *Scientific value:* High (expansion vs rewriting is a fundamental QE question)

### Tier 2: Moderate effort (extend pipeline)

4. **MuGI (multi-generation)** -- Generate 3-5 pseudo-documents per query (temperature=0.7), concatenate all with query. Tests whether multiple generations reduce noise.
   - *Effort:* ~4 hours (modify generation loop + longer runtime)
   - *Scientific value:* High (multiple generations could help Arabic's morphological richness)

5. **Varied generation subtasks (GRF-lite)** -- Generate facts, keywords, and pseudo-documents separately. Test which works best for Arabic.
   - *Effort:* ~3 hours (3 prompt variants)
   - *Scientific value:* Medium-high (which generation type works best is an open question for Arabic)

### Tier 3: Extended (requires new infrastructure)

6. **Two-pass (ITER-RETGEN simplified)** -- Query2Doc -> retrieve -> use top-3 documents to generate better pseudo-document -> retrieve again
   - *Effort:* ~1 day
   - *Scientific value:* High (tests whether corpus grounding helps Arabic QE)

7. **RAG-Fusion** -- Generate 3-5 query variations, retrieve for each, fuse with RRF
   - *Effort:* ~1 day
   - *Scientific value:* Medium (more about retrieval diversity than QE quality)

### NOT recommended for Phase 4:
- Training-based methods (RQ-RAG, SoftQE, RaFe) -- too expensive, too far from Query2Doc
- IRCoT -- designed for multi-hop, MIRACL is mostly single-hop
- Complex iterative loops with >3 iterations -- diminishing returns on Colab

---

## 14. Key Takeaways for Thesis

1. **Query2Doc is positioned between HyDE (embed-only) and GRF (feedback model)** in the QE technique spectrum. A comparison with HyDE is the most natural and impactful experiment.

2. **No existing paper compares HyDE vs Query2Doc on Arabic.** This is a gap we can fill.

3. **The knowledge leakage concern (Yoon et al., 2025) is less relevant for Arabic** since LLMs are less likely to have memorized MIRACL Arabic answers. This makes our evaluation more rigorous.

4. **Macmillan-Scott et al. (2025) validates our approach** -- LLM-based QE with Aya Expanse for Arabic works. They also find query length is a key factor, which aligns with our error analysis (short query gap).

5. **Multiple generation (MuGI) and varied prompts (GRF) are the lowest-hanging extensions** -- they require no new infrastructure, just different prompting strategies.

---

## References

1. Gao, L., Ma, X., Lin, J., & Callan, J. (2022). Precise Zero-Shot Dense Retrieval without Relevance Labels. arXiv:2212.10496. ACL 2023.
2. Wang, L., Yang, N., & Wei, F. (2023). Query2doc: Query Expansion with Large Language Models. arXiv:2303.07678. EMNLP 2023.
3. Mackie, I., Chatterjee, S., & Dalton, J. (2023). Generative Relevance Feedback with Large Language Models. arXiv:2304.13157. SIGIR 2023.
4. Zhang, L. & Wu, Y. (2024). MuGI: Exploring the Best Practices of Query Expansion with Large Language Models. arXiv:2401.06311.
5. Ma, X., Gong, Y., He, P., Zhao, H., & Duan, N. (2023). Query Rewriting for Retrieval-Augmented Large Language Models. arXiv:2305.14283. EMNLP 2023.
6. Mao, S., Jiang, Y., Chen, B., et al. (2024). RaFe: Ranking Feedback Improves Query Rewriting for RAG. arXiv:2405.14431. EMNLP 2024 Findings.
7. Mao, H. et al. (2024). DMQR-RAG: Diverse Multi-Query Rewriting for RAG. arXiv:2411.13154.
8. Jagerman, R., Zhuang, H., Qin, Z., Wang, X., & Bendersky, M. (2023). Query Expansion by Prompting Large Language Models. arXiv:2305.03653.
9. Trivedi, H., Balasubramanian, N., Khot, T., & Sabharwal, A. (2022). Interleaving Retrieval with Chain-of-Thought Reasoning. arXiv:2212.10509. ACL 2023.
10. Shao, Z., Gong, Y., Shen, Y., et al. (2023). Enhancing Retrieval-Augmented LLMs with Iterative Retrieval-Generation Synergy. arXiv:2305.15294. EMNLP 2023 Findings.
11. Rackauckas, Z. (2024). RAG-Fusion: A New Take on Retrieval-Augmented Generation. arXiv:2402.03367.
12. Yoon, Y., Jung, J., Yoon, S., & Park, K. (2025). Hypothetical Documents or Knowledge Leakage? Rethinking LLM-based Query Expansion. arXiv:2504.14175.
13. Li, M., Lv, X., Zou, J., et al. (2025). Query Expansion in the Age of Pre-trained and Large Language Models: A Comprehensive Survey. arXiv:2509.07794.
14. Macmillan-Scott, O., Goworek, R., & Ozyigit, E. B. (2025). Generative Query Expansion with Multilingual LLMs for Cross-Lingual Information Retrieval. arXiv:2511.19325.
15. (2025). LLM-based Query Expansion Fails for Unfamiliar and Ambiguous Queries. arXiv:2505.12694. SIGIR 2025.
16. Chan, C.-M. et al. (2024). RQ-RAG: Learning to Refine Queries for Retrieval Augmented Generation. arXiv:2404.00610.
17. (2024). SoftQE: Learned Representations of Queries Expanded by LLMs. arXiv:2402.12663.
18. Rashid et al. (2024). Progressive Query Expansion for Retrieval Over Cost-constrained Data Sources. arXiv:2406.07136.
19. (2025). Enhancing RAG with Two-Stage Retrieval: FlashRank Reranking and Query Expansion. arXiv:2601.03258.
20. (2024). A Survey of Query Optimization in Large Language Models. arXiv:2412.17558.
