# Strategies for Making LLM-Based Query Expansion Work with BM25/Sparse Retrieval

**Date:** 2026-03-28
**Status:** Research Complete
**Task:** Phase 4 research -- addressing the "term dilution" problem
**Context:** 6/9 tested LLMs DEGRADED BM25 performance in our Query2Doc pipeline. Only Jais-2 (+10.8%), Aya (+9.2%), and Qwen 2.5-7B (+1.3%) improved BM25.

---

## The Problem: Term Dilution in BM25

When a pseudo-document (typically 100-300 tokens) is concatenated with a short query (3-8 tokens), BM25's term-frequency-based scoring is overwhelmed by the expansion terms. The original query terms become a tiny fraction of the expanded query, causing:
- **Loss of original query signal**: BM25 weights the original query terms proportionally less
- **Introduction of noisy terms**: The pseudo-document adds many terms irrelevant to the information need
- **Length normalization distortion**: BM25's document-length normalization penalizes the much longer expanded query

This is exactly what we observed: models that produced longer, more elaborate pseudo-documents (like ALLaM) performed worst on BM25, while models with Arabic-native vocabulary (Jais-2) performed best because their generated terms more closely matched the BM25 index vocabulary.

---

## Table of Contents

1. [Strategy 1: Query Repetition / Weighting](#strategy-1)
2. [Strategy 2: Rank Fusion (Separate Retrieval Routes)](#strategy-2)
3. [Strategy 3: Term Selection / Filtering from Pseudo-Documents](#strategy-3)
4. [Strategy 4: Controlled Generation for Sparse Retrieval](#strategy-4)
5. [Strategy 5: Term Weighting in Expanded Queries](#strategy-5)
6. [Strategy 6: Document Expansion (doc2query family)](#strategy-6)
7. [Strategy 7: Iterative / Progressive Expansion](#strategy-7)
8. [Strategy 8: Multi-Document Generation](#strategy-8)
9. [Meta-Analysis: When Does Expansion Help vs. Hurt?](#meta-analysis)
10. [Feasibility Ranking for Our Project](#feasibility-ranking)
11. [Recommended Implementation Order](#recommendations)

---

<a name="strategy-1"></a>
## Strategy 1: Query Repetition / Weighting

### The Core Idea
Repeat the original query multiple times before concatenating with the pseudo-document, artificially boosting the term frequency of original query terms to preserve their importance in BM25 scoring.

### Paper 1.1: Query2Doc (Original Paper)
- **Authors:** Liang Wang, Nan Yang, Furu Wei
- **Year/Venue:** EMNLP 2023
- **arXiv:** 2303.07678
- **Key Mechanism:** Generate a pseudo-document via few-shot LLM prompting, then concatenate with the original query. For BM25, the original query is repeated before the pseudo-document to preserve term importance. The expanded query becomes: `q_expanded = [q repeated n times] + [pseudo-document]`
- **Results on BM25:** +3% to +15% on MS-MARCO and TREC DL. The repetition is critical for BM25 -- without it, the pseudo-document's terms dominate.
- **Value of n:** The paper uses a fixed repetition count. The exact value is not prominently stated in abstracts but the standard implementation uses n=5.
- **Limitation:** A fixed repetition count doesn't account for variable pseudo-document lengths. Longer pseudo-documents need more repetitions to maintain balance.
- **Feasibility:** TRIVIAL to implement. We already have Query2Doc -- just add `query * 5 + pseudo_doc` instead of `query + pseudo_doc`. This is the single highest-priority experiment.
- **Connection to our pipeline:** Direct modification of existing concatenation step.

### Paper 1.2: MuGI (Adaptive Query Repetition)
- **Authors:** Le Zhang et al.
- **Year/Venue:** EMNLP 2024 Findings
- **arXiv:** 2401.06311
- **Code:** https://github.com/lezhang7/Retrieval_MuGI
- **Key Mechanism:** Generates MULTIPLE pseudo-references (n=5 documents) and uses an ADAPTIVE repetition formula instead of fixed repetition:

  ```
  lambda = floor( sum(len(r_i)) / (len(q) * beta) )
  q_sparse = concat(q * lambda, r1, r2, ..., rn)
  ```

  Where `lambda` = repetition count, `len(r_i)` = length of each pseudo-reference, `len(q)` = query length, `beta` = proportionality constant (default beta=4).

- **Why adaptive:** "The variability in the length of queries and generated passages renders a static rate of repetition ineffective." The formula automatically increases repetitions for longer pseudo-documents and shorter queries.
- **Results on BM25:** +18% on TREC DL19, +16.4% on TREC DL20, +7.5% on BEIR (using ChatGPT-4). With open-source models, gains are smaller but still significant.
- **Key insight:** Gains plateau at 5 pseudo-references. More than 5 shows diminishing returns.
- **Feasibility:** MODERATE. We can implement this with our existing LLMs. Generating 5 pseudo-documents per query increases inference time 5x, but the adaptive repetition formula is trivial. Can use smaller models (even 3B) for the multiple generations.
- **Connection to our pipeline:** Direct extension of Query2Doc. Generate multiple pseudo-docs instead of one, use adaptive repetition.

---

<a name="strategy-2"></a>
## Strategy 2: Rank Fusion (Separate Retrieval Routes)

### The Core Idea
Instead of concatenating the expanded query (which risks term dilution), run TWO separate retrievals -- one with the original query, one with the expanded query -- and FUSE the results. This completely avoids the term dilution problem.

### Paper 2.1: Exp4Fuse
- **Authors:** Liu et al.
- **Year/Venue:** ACL 2025 Findings
- **arXiv:** 2506.04760
- **Code:** https://github.com/liuliuyuan6/Exp4Fuse
- **Key Mechanism:** Two retrieval routes through the SAME sparse retriever:
  1. **Original route:** Query -> BM25 -> Ranked list I_oq
  2. **Expansion route:** Query -> LLM generates pseudo-doc -> Expanded query (with repetition) -> BM25 -> Ranked list I_eq
  3. **Fusion:** Modified Reciprocal Rank Fusion: `FR_score = (w_i + n/10) * sum(1/(k + r_i))` where k=60

- **Key insight:** "Direct LLM-based query expansion on learned sparse retrievers can negatively impact performance because these models train on original queries." Fusion keeps both signals separate, avoiding degradation.
- **Results:** Outperforms Query2Doc, HyDE, and MUGI on BM25 across MS-MARCO and 7 low-resource BEIR datasets. Achieves SOTA on Touche-2020 with BM25.
- **LLMs used:** GPT-4-mini (primary), LLaMA3-8B-Instruct (generalizability test)
- **Feasibility:** EASY. We already have BM25 retrieval working. Just run it twice (once with original query, once with expanded) and fuse results. No new model needed -- uses existing Query2Doc pipeline. The computational cost is 2x retrieval (cheap) + 1x LLM generation (already done).
- **Connection to our pipeline:** This is the most natural fix for our BM25 degradation problem. We keep our existing Query2Doc output and just add the fusion step.

---

<a name="strategy-3"></a>
## Strategy 3: Term Selection / Filtering from Pseudo-Documents

### The Core Idea
Instead of concatenating the FULL pseudo-document with the query, EXTRACT only the most relevant terms/keywords from it. This reduces noise while preserving the beneficial expansion terms.

### Paper 3.1: CTQE (Candidate Token Query Expansion)
- **Authors:** Not specified in search results
- **Year/Venue:** CIKM 2025
- **arXiv:** 2509.02377
- **Code:** https://github.com/bluejeans8/CTQE
- **Key Mechanism:** Instead of generating a full pseudo-document and extracting terms from it, CTQE extracts diverse expansion terms directly from the LLM's output probability distribution (logits) during a SINGLE decoding pass. The unselected candidate tokens at each generation step are also conditioned on the query and capture useful expansion signals.
- **Results on BM25:** "Even with a single token, CTQE outperforms BM25 by more than 2 points in NDCG@10." Outperforms RM3, Query2Doc, and MUGI on some benchmarks.
- **Key advantage:** Achieves both relevance AND diversity without extra inference passes. Significantly lower latency than generating full pseudo-documents.
- **Feasibility:** MODERATE. Requires access to LLM logits during inference, which is available in HuggingFace transformers. Implementation is more complex than simple concatenation but uses only ONE forward pass per query.
- **Connection to our pipeline:** Could replace the Query2Doc generation step with a more targeted term extraction approach.

### Paper 3.2: GRF (Generative Relevance Feedback)
- **Authors:** Iain Mackie, Shubham Chatterjee et al.
- **Year/Venue:** SIGIR 2023
- **arXiv:** 2304.13157
- **Key Mechanism:** Builds probabilistic feedback models from LLM-generated text. Studies different generation subtasks: queries, entities, facts, news articles, documents, essays. The generated text is used to build an RM3-style term expansion model rather than being concatenated directly.
- **Results on BM25/Sparse:** Improves MAP 5-19% and NDCG@10 17-24% over RM3 expansion. On the hardest 20% of Robust04 topics, GRF improves NDCG@10 by +0.145 while RM3 only gains +0.006.
- **Key insight:** GRF and PRF are complementary. GRF provides external context not in the corpus; PRF grounds the query in the corpus. Combining both increases recall on 95% of experiments.
- **Feasibility:** MODERATE. Requires implementing RM3-style term selection on top of LLM output. The term extraction is more principled than raw concatenation.
- **Connection to our pipeline:** Instead of concatenating the pseudo-document, extract top terms using TF-IDF or similar and add only those to the query.

### Paper 3.3: Doc2Query-- (Filtering for Document Expansion)
- **Authors:** Watheq Mansour, Shengyao Zhuang, Guido Zuccon, Joel Mackenzie
- **Year/Venue:** SIGIR 2024
- **arXiv:** (SIGIR proceedings)
- **Key Mechanism:** Scores each document/expansion pair using a cross-encoder or bi-encoder and filters out low-scoring expansions. Applied to document expansion but the filtering principle applies to query expansion too.
- **Critical finding:** "Filtering actually harms recall-based metrics on various test collections." Removing noisy expansions also removes some beneficial ones.
- **Implication for our project:** Simple filtering may not work well. Term WEIGHTING (keeping all terms but with different importance) may be better than binary keep/discard filtering.
- **Feasibility:** EASY to test but may not help.

---

<a name="strategy-4"></a>
## Strategy 4: Controlled Generation for Sparse Retrieval

### The Core Idea
Instead of generating free-form pseudo-documents, CONSTRAIN the LLM to generate outputs specifically optimized for term-matching: keywords, entities, controlled vocabulary terms.

### Paper 4.1: BMQExpander (Ontology-Guided Query Expansion)
- **Authors:** Not specified in search results
- **Year/Venue:** arXiv 2025
- **arXiv:** 2508.11784
- **Key Mechanism:** Extracts key medical terms from query using an LLM, maps them to UMLS ontology concepts, retrieves definitions and semantic relationships, then prompts an LLM to generate a medically grounded pseudo-document using controlled vocabulary.
- **Results:** Up to +22.1% NDCG@10 over sparse baselines on biomedical benchmarks, +6.5% over strongest baseline. Fewer hallucinations than other LLM-based QE.
- **Key insight:** Grounding generation in controlled vocabulary (ontology) produces more relevant expansion terms and fewer hallucinations.
- **Feasibility for Arabic:** LOW-MODERATE. No Arabic biomedical ontology readily available, but the PRINCIPLE of constraining generation to corpus vocabulary is applicable. Could use a simple approach: extract the most frequent/important terms from the BM25 index and bias generation toward those terms.
- **Connection to our pipeline:** Could add a "generate keywords only" prompt instead of "generate a pseudo-document."

### Paper 4.2: TCDE (Topic-Centric Dual Expansion)
- **Authors:** Not specified in search results
- **Year/Venue:** arXiv December 2025
- **arXiv:** 2512.17164
- **Key Mechanism:** DUAL expansion of both queries AND documents:
  - **Query side:** LLM identifies distinct sub-topics within each query, generates a focused pseudo-document for EACH sub-topic. Original query repeated 5 times before concatenation.
  - **Document side:** LLM distills each document into 5 core topic sentences, appended to original document.
- **Results on BM25:** NDCG@10 improved from 0.2256 to 0.2549 on MS MARCO Dev. Achieves SOTA on TREC DL'19 for sparse retrieval (0.6657 NDCG@10).
- **LLM used:** Qwen-turbo (Alibaba Cloud) -- selected for speed and low cost
- **Feasibility:** LOW for document-side (requires re-indexing 2.1M documents). HIGH for query-side only (sub-topic decomposition is a prompt change).
- **Connection to our pipeline:** The query-side sub-topic decomposition could improve our pseudo-document quality. Instead of one generic pseudo-doc, generate one per sub-topic.

### Paper 4.3: EAR (Expand, Rerank, and Retrieve)
- **Authors:** Yung-Sung Chuang, Wei Fang, Shang-Wen Li, Wen-tau Yih, James R. Glass
- **Year/Venue:** ACL 2023 Findings
- **arXiv:** 2305.17080
- **Code:** https://github.com/voidism/EAR
- **Key Mechanism:** Generate DIVERSE query expansions (not just one), then train a RERANKER to select which expansion would lead to the best retrieval results. The reranker is trained to predict the rank of gold passages.
- **Key insight:** "The best query expansion often is not picked by greedy decoding." Generating multiple expansions and selecting the best one significantly outperforms single-expansion approaches.
- **Results:** Improves top-5/20 accuracy by 3-8 points in-domain and 5-10 points out-of-domain over vanilla query expansion with BM25.
- **Feasibility:** MODERATE. Requires training a small reranker (can be a lightweight cross-encoder), but the idea of generating multiple expansions and selecting is powerful.
- **Connection to our pipeline:** Generate 5-10 different query expansions, use a reranker to pick the best one for BM25 retrieval.

---

<a name="strategy-5"></a>
## Strategy 5: Term Weighting in Expanded Queries

### The Core Idea
Instead of treating all expansion terms equally (as BM25 does with raw concatenation), assign different weights to original query terms vs. expansion terms.

### Paper 5.1: BM25 Query Augmentation Learned End-to-End
- **Authors:** Xiaoyin Chen, Sam Wiseman
- **Year/Venue:** arXiv 2023
- **arXiv:** 2305.14087
- **Key Mechanism:** Learns a continuous augmentation vector and term reweighting end-to-end using contrastive loss. The learned augmentation adds new terms while reweighting controls their importance relative to original query terms.
- **Results:** +12 percentage points on top-5 accuracy on Natural Questions vs vanilla BM25. Transfers well to unseen datasets (+2-3 points on TriviaQA, EntityQuestions).
- **Feasibility:** LOW. Requires training a neural model, which contradicts our zero-shot/few-shot approach.
- **Connection to our pipeline:** The principle is important: expansion terms should have lower weight than original query terms. Even a simple heuristic (multiply original term frequencies by a factor) could help.

### Paper 5.2: SPLADE (Learned Sparse Retrieval)
- **Authors:** Formal, Piwowarski, Clinchant et al.
- **Year/Venue:** SIGIR 2021, with extensions through SPLADE-v3 (2024)
- **arXiv:** 2107.05720
- **Key Mechanism:** Learns sparse vector representations that unify term weighting and expansion in a supervised setting. A BERT-based model produces sparse outputs compatible with inverted index structures, with learned importance weights per term.
- **Recent extensions:** SPLADE-v3 (2024) achieves higher metrics via distillation, multi-hard-negative mining. Echo-Mistral-SPLADE (2024) uses a decoder-only LLM backbone.
- **Feasibility:** LOW for full implementation (requires training). But the CONCEPT of term-level importance weighting is applicable to our approach.
- **Connection to our pipeline:** Could use a pre-trained SPLADE model as an alternative sparse retriever that handles expansion terms more gracefully than BM25.

### Practical Heuristic (No Paper -- AI Suggestion)
**AI Suggestion:** A simple heuristic approach that doesn't require any training:
1. Take the original query terms
2. Take the pseudo-document terms
3. For BM25, construct expanded query as: `original_query * N + pseudo_document * 1`
4. Tune N on a small validation set (try N = 3, 5, 7, 10)

This is essentially what Query2Doc and MuGI do with their repetition strategies, but framed as a weighting problem.

---

<a name="strategy-6"></a>
## Strategy 6: Document Expansion (doc2query Family)

### The Core Idea
Instead of expanding the QUERY, expand the DOCUMENTS at indexing time. For each document in the corpus, generate potential queries it could answer and append them. This way, the BM25 index already contains the "expanded" vocabulary, and the original query can match more documents without any query-side modification.

### Paper 6.1: docTTTTTquery / doc2query-T5
- **Authors:** Rodrigo Nogueira, Jimmy Lin
- **Year/Venue:** 2019 (original), widely adopted since
- **Key Mechanism:** Train a T5 model to generate questions from documents. At indexing time, generate N questions per document and append to the document text. At query time, use standard BM25 on the expanded index.
- **Key advantage:** Expensive neural inference happens ONCE at indexing time. Query-time retrieval is as fast as standard BM25.
- **Feasibility:** LOW for our project. Would require generating queries for 2.1M Arabic documents -- extremely expensive. Also requires an Arabic question generation model.
- **Connection to our pipeline:** Complementary to Query2Doc. Query2Doc expands queries; doc2query expands documents. Together they could bridge the vocabulary gap from both sides.

### Paper 6.2: Doc2Query-- (Filtering)
- **Authors:** Gospodinov et al. (2023), Mansour et al. (SIGIR 2024 reproduction)
- **Key Mechanism:** Filter generated queries using cross-encoder scoring. Remove low-quality or hallucinated expansions.
- **Critical finding:** Filtering harms recall. The noise removed also contained some beneficial signal.
- **Feasibility:** Same as 6.1 -- requires document-side processing.

### Paper 6.3: Doc2Query++ (Topic-Coverage Based)
- **Authors:** Not specified
- **Year/Venue:** arXiv October 2025
- **arXiv:** 2510.09557
- **Key Mechanism:** Infers latent topics via BERTopic, extracts topic- and document-level keywords, uses them to GUIDE LLM-based query generation. Ensures diverse and relevant query generation with controlled topic coverage.
- **For dense retrieval:** Proposes Dual-Index Fusion to isolate text and query signals, preventing noise from query appending.
- **Results:** "Consistently achieves superior retrieval performance, robustly outperforming all baselines across datasets and both sparse and dense retrieval settings."
- **Feasibility:** LOW for our project (document-side). But the TOPIC-COVERAGE principle is applicable to query-side expansion.

### Relationship to Query2Doc
Query2Doc and doc2query are mirror images:
- **doc2query:** Document -> Generated queries (document expansion)
- **Query2Doc:** Query -> Generated document (query expansion)

For BM25, document expansion is generally more effective because:
1. The expansion happens at indexing time, not query time
2. Each document gets targeted expansions
3. No term dilution problem at query time

However, document expansion is impractical for our project due to the 2.1M document corpus size. Query-side expansion is the only feasible path.

---

<a name="strategy-7"></a>
## Strategy 7: Iterative / Progressive Expansion

### The Core Idea
Instead of generating one expansion in a single shot, use iterative retrieval-generation loops to progressively refine the query expansion, grounding each iteration in actual retrieved documents.

### Paper 7.1: ProQE (Progressive Query Expansion)
- **Authors:** Rashid et al.
- **Year/Venue:** arXiv June 2024
- **arXiv:** 2406.07136
- **Key Mechanism:** Iterative loop:
  1. Retrieve ONE document per iteration
  2. LLM judges relevance and extracts key terms
  3. Update query with extracted terms
  4. Repeat until budget is met
  5. Final chain-of-thought expansion before a single high-recall sweep
- **Results:** +37% over baselines on MRR and R@1. Most cost-effective approach tested.
- **Key advantage:** Works for both sparse and dense retrieval. Plug-and-play module.
- **Feasibility:** MODERATE. Multiple LLM calls per query (budget-dependent). But each call is small (term extraction, not full document generation). For 2,896 queries, could be expensive.
- **Connection to our pipeline:** Could replace single-shot Query2Doc with iterative expansion. Each iteration extracts more targeted terms.

### Paper 7.2: ThinkQE (Thinking-Based Expansion)
- **Authors:** Not specified
- **Year/Venue:** arXiv June 2025
- **arXiv:** 2506.09260
- **Key Mechanism:** Two components:
  1. **Thinking-based expansion:** LLM does chain-of-thought reasoning about the query before generating expansion terms
  2. **Corpus-interaction:** Iteratively refines expansions using retrieval feedback from the corpus
- **Results:** Outperforms training-intensive dense retrievers AND rerankers (including RankGPT4 and Rank1-14B). Training-free.
- **LLM used:** Qwen-R1-Distill-14B (temperature 0.7)
- **Feasibility:** LOW-MODERATE. Uses a 14B model (too large for Colab T4 in FP16). Could potentially work with a smaller reasoning model (Qwen3-4B with thinking mode).
- **Connection to our pipeline:** The "thinking before expanding" principle could be added to our prompt template.

### Paper 7.3: RFG Framework (Retrieval-Feedback-Grounded Multi-Query Expansion)
- **Authors:** Not specified
- **Year/Venue:** IC3K 2025
- **Key Mechanism:** Three-stage process:
  1. Generate diverse pseudo-queries using LLM grounded in initial BM25 retrieval results
  2. Each pseudo-query retrieves its own document set
  3. Rank fusion aggregates all retrieved lists
- **Key advantage:** Initial retrieval grounds the LLM generation, reducing hallucinations. Multiple queries capture different aspects.
- **Feasibility:** MODERATE. Requires initial BM25 retrieval + LLM generation + multiple BM25 retrievals + fusion. Multiple retrieval passes are cheap; LLM generation is the bottleneck.
- **Connection to our pipeline:** Combines Strategies 2 (fusion) and 7 (iterative) with grounded generation.

---

<a name="strategy-8"></a>
## Strategy 8: Multi-Document Generation

### Paper 8.1: MuGI (covered in Strategy 1.2)
Generate multiple pseudo-references instead of one. Key formula and results covered above.

### Paper 8.2: Multi-Model Pseudo-Document Generation (MPQE)
- **Year/Venue:** 2025 (Information Processing & Management)
- **Key Mechanism:** Uses MULTIPLE different LLMs to generate pseudo-documents, then reconstructs a hybrid expansion. Addresses "limited semantic coverage" of single-model approaches.
- **Feasibility:** HIGH conceptually -- we already have 9 tested LLMs. Could ensemble pseudo-documents from Jais-2 + Aya + Qwen3-4B.
- **Connection to our pipeline:** Direct extension. Use our best 2-3 models to each generate a pseudo-document, combine with adaptive repetition.

---

<a name="meta-analysis"></a>
## Meta-Analysis: When Does Expansion Help vs. Hurt?

### Paper M1: "When do Generative Query and Document Expansions Fail?"
- **Authors:** Orion Weller, Kyle Lo et al.
- **Year/Venue:** EACL 2024 Findings
- **arXiv:** 2309.08541
- **Key Findings:**
  1. **Strong negative correlation** between retriever baseline performance and expansion gains: expansion helps weak models but can hurt strong models.
  2. Expansions improve recall but add noise that makes it "difficult to discern between the top relevant documents" (introducing false positives).
  3. **Practical recipe:** Use expansions for weaker models OR when target dataset differs significantly from training corpus.
- **Implication for our project:** Our BM25 baseline (NDCG@10=0.4621) is relatively weak, which is EXACTLY where expansion should help most. The fact that 6/9 models hurt BM25 suggests the problem is implementation (term dilution), not the expansion approach itself.

### Paper M2: "A Case Study of Enhancing Sparse Retrieval using LLMs"
- **Authors:** Jagerman et al.
- **Year/Venue:** ACM Web Conference 2024
- **Key Findings:**
  1. LLMs can "diminish the discrepancy between the term frequencies of the important terms in a query and the relevant document."
  2. Query rewriting and query expansion are both beneficial for sparse retrieval, but effectiveness varies by domain.
  3. In certain domains, LLM effectiveness is constrained.
- **Implication for our project:** The Arabic domain with morphological complexity may benefit particularly from LLM expansion, since the vocabulary mismatch is more severe.

### Paper M3: Query Expansion Survey (Comprehensive)
- **Authors:** Not specified
- **Year/Venue:** arXiv September 2025
- **arXiv:** 2509.07794
- **Key taxonomy:** Organizes QE along four dimensions:
  1. **Point of injection:** implicit/embedding vs. selection-based explicit
  2. **Grounding and interaction:** zero-grounding prompts to multi-round retrieve-expand loops
  3. **Learning and alignment:** SFT/PEFT/DPO
  4. **Knowledge-graph integration**
- **Key finding for sparse retrieval:** "For sparse retrieval (BM25), pseudo-references are concatenated with repeated copies of the original query to balance their influence, given BM25's sensitivity to term frequency and document length."

---

<a name="feasibility-ranking"></a>
## Feasibility Ranking for Our Project

Criteria: Google Colab (T4/A100), 2-8B models, zero-shot, builds on existing Query2Doc pipeline, implementable in 1-2 weeks.

| Rank | Strategy | Effort | Expected BM25 Gain | Implementation |
|------|----------|--------|-------------------|----------------|
| 1 | **Query Repetition (n=5)** | 1 hour | +5-15% | Change 1 line of code |
| 2 | **Adaptive Repetition (MuGI formula)** | 2-3 hours | +7-18% | Add length-based lambda calculation |
| 3 | **Rank Fusion (Exp4Fuse)** | 1 day | +8-15% | Run BM25 twice, add RRF fusion |
| 4 | **Multi-model ensemble** | 1 day | Unknown | Combine pseudo-docs from Jais-2 + Aya |
| 5 | **Keyword-only prompt** | 2-3 hours | Unknown | Change prompt to "generate keywords" |
| 6 | **Sub-topic decomposition** | 1 day | Unknown | TCDE query-side only |
| 7 | **CTQE (logit-based)** | 2-3 days | +2-5% over BM25 | Extract candidate tokens from logits |
| 8 | **ProQE (iterative)** | 3-5 days | +10-37% (varies) | Iterative retrieval-generation loop |
| 9 | **GRF (term extraction model)** | 3-5 days | +5-24% over RM3 | RM3-style term selection from LLM output |
| 10 | **EAR (expansion reranking)** | 1 week | +3-10% | Requires training a reranker |
| -- | ~~Doc2query (document expansion)~~ | ~~Weeks~~ | ~~N/A~~ | ~~Requires processing 2.1M docs~~ |
| -- | ~~SPLADE (learned sparse)~~ | ~~Weeks~~ | ~~N/A~~ | ~~Requires training~~ |
| -- | ~~BM25 learned augmentation~~ | ~~Weeks~~ | ~~N/A~~ | ~~Requires training~~ |

---

<a name="recommendations"></a>
## Recommended Implementation Order

### Phase A: Quick Wins (1-2 days total)

**A1. Query Repetition (n=5) -- HIGHEST PRIORITY**
- Modify existing Query2Doc BM25 evaluation to use `query * 5 + pseudo_doc`
- Test with ALL existing model outputs (no new LLM inference needed)
- Expected to fix most of the 6/9 degradation cases
- Compare n = {1, 3, 5, 7, 10} to find optimal for Arabic

**A2. Adaptive Repetition (MuGI formula)**
- Implement `lambda = floor(sum(len(pseudo_docs)) / (len(query) * beta))`
- Test beta = {2, 4, 6, 8}
- Compare with fixed n=5

**A3. Keyword-Only Prompt Variant**
- Instead of "Write a passage that answers this query," use:
  "List 10 Arabic keywords and phrases related to this query: [query]"
- This produces shorter, more targeted expansions that may work better with BM25
- Test with Jais-2 and Aya (our best BM25 models)

### Phase B: Rank Fusion (1-2 days)

**B1. Implement Exp4Fuse-style fusion**
- Run BM25 with original query -> ranked list 1
- Run BM25 with expanded query (using repetition from Phase A) -> ranked list 2
- Fuse with Reciprocal Rank Fusion (k=60)
- This should be strictly better than either query alone

### Phase C: Advanced Strategies (if time permits, 3-5 days)

**C1. Multi-model ensemble**
- Use pseudo-documents from Jais-2, Aya, and Qwen3-4B
- Combine with adaptive repetition
- Test if ensemble > best single model

**C2. Sub-topic decomposition (TCDE query-side)**
- Prompt: "Identify 3 sub-topics in this query and generate a focused passage for each"
- Combine sub-topic pseudo-docs with original query using adaptive repetition

**C3. CTQE-style logit extraction**
- During LLM inference, collect top-k candidate tokens at each step
- Use these as expansion terms instead of/in addition to the generated text
- Requires more engineering but potentially better term diversity

---

## Key Citations Summary

| Paper | Year | Venue | arXiv | Most Relevant Strategy |
|-------|------|-------|-------|----------------------|
| Query2Doc (Wang et al.) | 2023 | EMNLP | 2303.07678 | Query repetition |
| MuGI (Zhang et al.) | 2024 | EMNLP Findings | 2401.06311 | Adaptive repetition |
| Exp4Fuse (Liu et al.) | 2025 | ACL Findings | 2506.04760 | Rank fusion |
| CTQE | 2025 | CIKM | 2509.02377 | Logit-based term selection |
| GRF (Mackie et al.) | 2023 | SIGIR | 2304.13157 | Term extraction from LLM output |
| EAR (Chuang et al.) | 2023 | ACL Findings | 2305.17080 | Expansion reranking |
| TCDE | 2025 | arXiv | 2512.17164 | Topic-centric dual expansion |
| Doc2Query++ | 2025 | arXiv | 2510.09557 | Document expansion + topic coverage |
| ProQE (Rashid et al.) | 2024 | arXiv | 2406.07136 | Progressive iterative expansion |
| ThinkQE | 2025 | arXiv | 2506.09260 | Reasoning-based expansion |
| Weller et al. | 2024 | EACL Findings | 2309.08541 | When expansion fails |
| Jagerman et al. | 2024 | WWW | (proceedings) | Case study: LLMs + sparse |
| QE Survey | 2025 | arXiv | 2509.07794 | Comprehensive taxonomy |
| BM25 Learned Aug. | 2023 | arXiv | 2305.14087 | Learned term reweighting |
| BMQExpander | 2025 | arXiv | 2508.11784 | Ontology-guided controlled generation |
| RFG Framework | 2025 | IC3K | (proceedings) | Retrieval-feedback grounded multi-query |
| FGQE | 2025 | ECIR | (proceedings) | Fair generative query expansion |
| docTTTTTquery (Nogueira & Lin) | 2019 | arXiv | (preprint) | Document expansion baseline |
| Doc2Query-- (Gospodinov et al.) | 2023 | ECIR | 2301.03266 | Filtering document expansions |
| SPLADE (Formal et al.) | 2021+ | SIGIR | 2107.05720 | Learned sparse representations |

---

## Bottom Line for Our Project

The core problem (6/9 models degrading BM25) is almost certainly solvable with **query repetition** (Strategy 1). This is the single most impactful change we can make, and it requires minimal implementation effort.

The original Query2Doc paper, MuGI, TCDE, and the comprehensive QE survey ALL agree: **for BM25, the original query must be repeated multiple times before concatenation with the pseudo-document**. Our current implementation concatenates `query + pseudo_doc` without repetition, which is the known-bad configuration.

After implementing repetition, **rank fusion** (Strategy 2) provides a further guaranteed improvement by preserving the original query's retrieval signal alongside the expanded query's signal.

These two strategies together should turn most of our BM25 degradation cases into improvements, and they require at most 2 days of implementation work.
