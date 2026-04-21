# Contrastive HyDE Quick Start Guide

## What is Contrastive HyDE?

An extension of Query2Doc/HyDE that generates BOTH:
1. **Positive hypothetical document** - answers the query
2. **Negative hypothetical document** - related but doesn't answer

Then uses contrastive scoring to rank documents:
```
Score(D) = 0.4·sim(Query,D) + 0.4·sim(Positive,D) - 0.2·sim(Negative,D)
```

## Running the Experiment

### Option 1: Google Colab (Recommended)

1. Open `experiments/exp_005_contrastive_hyde_dense.ipynb` in Colab
2. Run all cells in order
3. Results saved to `results/contrastive_hyde_dense/`

**Runtime:** ~45-60 minutes total
- Document generation: ~30-40 minutes
- Retrieval: ~10-15 minutes
- Evaluation: ~1 minute

### Option 2: Local (Requires GPU)

```bash
# Install dependencies
pip install -r requirements.txt

# Run notebook
jupyter notebook experiments/exp_005_contrastive_hyde_dense.ipynb
```

## Key Components

### 1. Contrastive HyDE Enhancer
```python
from src.enhancers.contrastive_hyde import ContrastiveHyDEEnhancer

enhancer = ContrastiveHyDEEnhancer(
    model_name="Qwen/Qwen2.5-3B-Instruct",
    max_new_tokens=128,
    temperature=0.7
)

# Generate both positive and negative docs
positive_docs, negative_docs = enhancer.enhance_batch(queries)
```

### 2. Contrastive Dense Retriever
```python
from src.retrievers.contrastive_dense import ContrastiveDenseRetriever

retriever = ContrastiveDenseRetriever(
    index=faiss_index,
    docid_map=docid_map,
    alpha=0.4,  # Query weight
    beta=0.4,   # Positive weight
    gamma=0.2   # Negative weight (subtracted)
)

# Perform contrastive search
results = retriever.contrastive_search(
    queries=queries,
    positive_docs=positive_docs,
    negative_docs=negative_docs,
    k=100
)
```

## Expected Outputs

1. **Generated Documents:**
   - `contrastive_hyde_docs_exp005.pkl` - All positive/negative docs

2. **Retrieval Results:**
   - `results/contrastive_hyde_dense/exp_005_contrastive_hyde_dense.txt` - TREC format
   - `results/contrastive_hyde_dense/exp_005_metrics.json` - Evaluation metrics

3. **Metrics:**
   - Recall@10, Recall@100
   - NDCG@10
   - MRR

## Troubleshooting

### Out of Memory
- Reduce `batch_size` in enhancer (default: 8)
- Reduce `max_new_tokens` (default: 128)

### Slow Generation
- Use smaller model: `Qwen/Qwen2.5-1.5B-Instruct`
- Increase `batch_size` if you have more GPU memory

### Index Not Found
- Update `drive_base` path in notebook
- Ensure FAISS index is downloaded/linked

## Comparing with Baselines

After running, compare with:
- **Exp 001:** Dense baseline (no enhancement)
- **Exp 003:** Query2Doc + Dense

Key metrics to watch:
- **NDCG@10:** Should improve due to better precision
- **Recall@100:** May be similar to Query2Doc
- **MRR:** Should improve if negative docs help ranking

## Ablation Study

The notebook includes weight sensitivity tests:
- No negative (γ=0): Equivalent to Query2Doc
- Balanced (default): α=0.4, β=0.4, γ=0.2
- Strong negative: α=0.3, β=0.4, γ=0.3
- Query-focused: α=0.5, β=0.3, γ=0.2

## Next Steps

1. Run experiment and document results
2. Compare with Query2Doc baseline
3. Analyze which queries benefit most
4. Test with BM25 retriever
5. Experiment with different weight configurations
