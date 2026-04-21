# Experiment 005: Contrastive HyDE + Dense Retrieval

**Date:** February 12, 2026  
**Status:** Ready to Run  
**Baseline:** Exp 003 (Query2Doc + Dense)

## Objective

Test a novel contrastive retrieval approach using both positive and negative hypothetical documents to improve ranking precision.

## Motivation

Standard HyDE/Query2Doc generates only positive hypothetical documents that answer the query. However, this can lead to:
- Retrieval of semantically related but irrelevant documents
- Topic drift in results
- Poor precision for ambiguous queries

**Key Insight:** By generating negative hypothetical documents (related but don't answer the query), we can explicitly penalize documents that are topically similar but not truly relevant.

## Method

### 1. Dual Document Generation

For each query, generate TWO hypothetical documents using Qwen 2.5 3B:

**Positive Document:**
- Prompt: "Write a passage that answers the given query"
- Purpose: Captures what a relevant document should look like

**Negative Document:**
- Prompt: "Write a passage that is semantically related to the query but does NOT answer it"
- Purpose: Captures what an irrelevant but related document looks like

### 2. Contrastive Scoring

Instead of standard dense retrieval scoring, use:

```
Score(D) = α · sim(Query, D) + β · sim(PosHyDE, D) - γ · sim(NegHyDE, D)
```

Where:
- `α = 0.4`: Weight for query-document similarity
- `β = 0.4`: Weight for positive HyDE-document similarity
- `γ = 0.2`: Weight for negative HyDE-document similarity (subtracted)

### 3. Retrieval Pipeline

1. Encode query, positive doc, negative doc using mDPR encoder
2. Retrieve candidate documents using query embedding (top 300)
3. Re-rank candidates using contrastive scoring formula
4. Return top 100 documents

## Configuration

```python
# LLM for document generation
model_name: "Qwen/Qwen2.5-3B-Instruct"
max_new_tokens: 128
temperature: 0.7
batch_size: 8

# Retriever
encoder: "castorini/mdpr-tied-pft-msmarco"
index: "miracl-v1.0-ar-mdpr-tied-pft-msmarco"

# Contrastive weights
alpha: 0.4  # Query weight
beta: 0.4   # Positive HyDE weight
gamma: 0.2  # Negative HyDE weight (subtracted)
```

## Expected Results

**Hypothesis:** Contrastive HyDE should improve:
- **Precision metrics** (NDCG@10, MRR) by penalizing related-but-irrelevant docs
- **Ranking quality** through explicit negative signal
- **Robustness** to ambiguous or broad queries

**Trade-offs:**
- 2x generation time (positive + negative docs)
- Slightly higher computational cost for re-ranking
- Requires careful weight tuning

## Comparison Points

| Metric | Dense Baseline | Query2Doc (Exp 003) | Contrastive HyDE (Exp 005) |
|--------|---------------|---------------------|---------------------------|
| Recall@100 | ~0.841 | TBD | TBD |
| NDCG@10 | ~0.499 | TBD | TBD |
| MRR | TBD | TBD | TBD |

## Implementation Files

- **Enhancer:** `src/enhancers/contrastive_hyde.py`
- **Retriever:** `src/retrievers/contrastive_dense.py`
- **Notebook:** `experiments/exp_005_contrastive_hyde_dense.ipynb`

## Ablation Studies

The notebook includes weight sensitivity analysis:

1. **No negative** (α=0.5, β=0.5, γ=0.0): Equivalent to Query2Doc
2. **Balanced** (α=0.4, β=0.4, γ=0.2): Default configuration
3. **Strong negative** (α=0.3, β=0.4, γ=0.3): Higher penalty for negative similarity
4. **Query-focused** (α=0.5, β=0.3, γ=0.2): Emphasize original query

## Next Steps

1. Run experiment on Google Colab
2. Compare results with Query2Doc baseline
3. Analyze per-query improvements
4. Test optimal weight configuration
5. Consider testing with BM25 retriever
6. Investigate failure cases

## References

- **HyDE:** Gao et al. (2022) "Precise Zero-Shot Dense Retrieval without Relevance Labels"
- **Query2Doc:** Wang et al. (2023) "Query2doc: Query Expansion with Large Language Models"
- **Contrastive Learning:** Chen et al. (2020) "A Simple Framework for Contrastive Learning of Visual Representations"
