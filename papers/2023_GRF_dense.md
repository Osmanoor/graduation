# Generative and Pseudo-Relevant Feedback for Sparse, Dense and Learned Sparse Retrieval
**Year:** 2023
**Authors:** Iain Mackie, Shubham Chatterjee, and Jeffrey Dalton
**Venue:** arXiv (Preprint)

## Short Description
This paper extends the authors' previous work on Generative Relevance Feedback (GRF) by applying LLM-based query expansion to **Dense** (vector-based) and **Learned Sparse** (SPLADE) retrieval models, rather than just standard sparse (BM25) models. Furthermore, it proposes a weighted fusion method to combine the benefits of GRF (external knowledge) with traditional Pseudo-Relevance Feedback (corpus-specific knowledge).

## Research Question
1. Can Generative Relevance Feedback (GRF) effectively improve Dense and Learned Sparse retrieval models?
2. Are the ranking signals from GRF and traditional Pseudo-Relevance Feedback (PRF) complementary, and can they be fused to improve recall?

## Main Methodology
1.  **Generation:** Identical to the previous paper, they use GPT-3 to generate diverse text (facts, essays, news) based on the query.
2.  **Dense GRF:** They use **TCT-ColBERT**. The generated documents are encoded into vectors. A Rocchio-style update is applied: the new query vector is a weighted combination of the original query vector and the mean of the generated document vectors ($GRF = \alpha \vec{Q} + \beta \vec{D_{LLM}}$).
3.  **Learned Sparse GRF:** They use **SPLADE**. The generated documents are processed to extract expansion terms and weights, which are then combined with the query's sparse representation.
4.  **Fusion (WRRF):** They use Weighted Reciprocal Rank Fusion to combine the result list from the GRF run with the result list from a standard PRF run.

## Dataset & Benchmark
*   **TREC Robust04:** News articles.
*   **CODEC:** Complex social science topics.
*   **TREC Deep Learning (DL) 19/20:** Web documents (MS MARCO).
*   **DL-HARD:** A subset of difficult queries requiring reasoning.
*   **Overlap with MIRACL:** No.

## Key Results
*   **GRF Effectiveness:** GRF improves over standard PRF baselines for Dense (TCT-ColBERT) and Learned Sparse (SPLADE) models by approximately **9-10%** on nDCG@20 and Recall.
*   **Fusion Wins:** Combining GRF and PRF (Fusion) achieved the best R@1000 in **17 out of 18** experiments.
*   **Complementarity:** Query analysis showed that GRF helps "hard" queries by providing external context (explaining *concepts* like "clear-cutting"), while PRF helps queries that require specific *corpus grounding* (finding specific events like "human stampede in Saudi Arabia" rather than general information about stampedes in India).

## Relevance to Our Project
- **Applicable to Arabic?** **Yes.** This is highly relevant if we plan to use Dense Retrievers (like mBERT or Arabic-ColBERT) or Learned Sparse models (like SPLADE-v2) for Arabic.
- **Uses MIRACL?** **No.**
- **Retrieval metrics reported?** MAP, nDCG@10, Recall@1000.
- **Feasible for us?** **Medium.** Implementing the fusion (GRF + PRF) doubles the retrieval inference cost because you must run two separate retrieval passes and then merge them. However, it offers a robust way to handle the "hallucination" risk of LLMs by grounding them with standard PRF.

## Notes
*   This paper provides the technical "how-to" for applying LLM expansion to vector search, which is a common modern retrieval setup.
*   The finding that "PRF and GRF are complementary" is crucial: it suggests we shouldn't replace standard feedback entirely with LLMs, but rather use both.