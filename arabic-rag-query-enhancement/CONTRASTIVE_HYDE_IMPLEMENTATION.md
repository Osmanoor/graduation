# Contrastive HyDE Implementation Summary

## Overview

Implemented a novel **Contrastive HyDE Retrieval** experiment that extends Query2Doc/HyDE with negative hypothetical documents for improved ranking precision.

## What Was Implemented

### 1. Contrastive HyDE Enhancer (`src/enhancers/contrastive_hyde.py`)

Generates both positive and negative hypothetical documents:

**Features:**
- Dual document generation (positive + negative)
- Batch processing for efficiency
- Configurable prompts for each document type
- GPU-accelerated with Qwen 2.5 3B

**Positive Prompt:** "Write a passage that answers the given query"  
**Negative Prompt:** "Write a passage that is semantically related to the query but does NOT answer it"

### 2. Contrastive Dense Retriever (`src/retrievers/contrastive_dense.py`)

Performs contrastive scoring for document ranking:

**Scoring Formula:**
```
Score(D) = α · sim(Query, D) + β · sim(PosHyDE, D) - γ · sim(NegHyDE, D)
```

**Features:**
- Configurable weights (α, β, γ)
- Efficient candidate retrieval + re-ranking
- GPU-accelerated encoding
- Batch processing support

### 3. Experiment Notebook (`experiments/exp_005_contrastive_hyde_dense.ipynb`)

Complete end-to-end experiment:

**Sections:**
1. Setup and installation
2. Data loading (MIRACL Arabic)
3. Contrastive HyDE document generation
4. Contrastive retrieval
5. Evaluation and comparison
6. Ablation study (weight sensitivity)
7. Results analysis

### 4. Documentation

- **Experiment Guide:** `docs/experiments/exp_005_contrastive_hyde_dense.md`
- **Quick Start:** `experiments/CONTRASTIVE_HYDE_QUICKSTART.md`
- **This Summary:** `CONTRASTIVE_HYDE_IMPLEMENTATION.md`

## Key Innovation

**Problem:** Standard HyDE/Query2Doc can retrieve semantically related but irrelevant documents.

**Solution:** Generate negative hypothetical documents that represent what an irrelevant (but related) document looks like, then explicitly penalize similarity to these negative examples.

**Benefits:**
- Better precision through negative signal
- Improved ranking quality
- More robust to topic drift
- Better handling of ambiguous queries

## Configuration

```python
# Default weights (configurable)
alpha = 0.4   # Query-document similarity
beta = 0.4    # Positive HyDE-document similarity
gamma = 0.2   # Negative HyDE-document similarity (subtracted)

# LLM settings
model = "Qwen/Qwen2.5-3B-Instruct"
max_tokens = 128
temperature = 0.7
batch_size = 8
```

## Usage Example

```python
from src.enhancers.contrastive_hyde import ContrastiveHyDEEnhancer
from src.retrievers.contrastive_dense import ContrastiveDenseRetriever

# Initialize enhancer
enhancer = ContrastiveHyDEEnhancer()

# Generate documents
positive_docs, negative_docs = enhancer.enhance_batch(queries)

# Initialize retriever
retriever = ContrastiveDenseRetriever(
    index=faiss_index,
    docid_map=docid_map,
    alpha=0.4, beta=0.4, gamma=0.2
)

# Perform contrastive search
results = retriever.contrastive_search(
    queries=queries,
    positive_docs=positive_docs,
    negative_docs=negative_docs,
    k=100
)
```

## Running the Experiment

### Google Colab (Recommended)
1. Open `experiments/exp_005_contrastive_hyde_dense.ipynb`
2. Run all cells
3. Results saved to `results/contrastive_hyde_dense/`

**Expected Runtime:** ~45-60 minutes
- Document generation: ~30-40 min (2x Query2Doc)
- Retrieval: ~10-15 min
- Evaluation: ~1 min

## Comparison with Baselines

| Approach | Positive Docs | Negative Docs | Contrastive Scoring |
|----------|--------------|---------------|-------------------|
| Dense Baseline | ❌ | ❌ | ❌ |
| Query2Doc (Exp 003) | ✅ | ❌ | ❌ |
| Contrastive HyDE (Exp 005) | ✅ | ✅ | ✅ |

## Ablation Study

The notebook includes weight sensitivity analysis:

1. **No negative** (γ=0): Baseline equivalent to Query2Doc
2. **Balanced** (default): α=0.4, β=0.4, γ=0.2
3. **Strong negative**: α=0.3, β=0.4, γ=0.3
4. **Query-focused**: α=0.5, β=0.3, γ=0.2

## Files Created

```
arabic-rag-query-enhancement/
├── src/
│   ├── enhancers/
│   │   └── contrastive_hyde.py          # Dual document generator
│   └── retrievers/
│       └── contrastive_dense.py         # Contrastive retriever
├── experiments/
│   ├── exp_005_contrastive_hyde_dense.ipynb  # Main experiment
│   └── CONTRASTIVE_HYDE_QUICKSTART.md        # Quick start guide
├── docs/
│   └── experiments/
│       └── exp_005_contrastive_hyde_dense.md # Detailed documentation
└── CONTRASTIVE_HYDE_IMPLEMENTATION.md        # This file
```

## Next Steps

1. **Run Experiment:** Execute notebook on Google Colab
2. **Analyze Results:** Compare with Query2Doc baseline
3. **Document Findings:** Update experiment doc with actual metrics
4. **Optimize Weights:** Test different α, β, γ configurations
5. **Extend to BM25:** Test contrastive approach with BM25 retriever
6. **Error Analysis:** Identify which queries benefit most

## Technical Notes

### Memory Requirements
- **GPU:** 12GB+ recommended (T4 or better)
- **RAM:** 16GB+ for index loading
- **Storage:** ~10GB for models and indices

### Performance Optimizations
- Batch processing for document generation
- GPU-accelerated encoding
- Efficient candidate retrieval before re-ranking
- Left-padding for decoder-only models

### Limitations
- 2x generation time vs Query2Doc
- Requires careful weight tuning
- Negative document quality depends on LLM
- Re-ranking adds computational overhead

## References

- **HyDE:** Gao et al. (2022) "Precise Zero-Shot Dense Retrieval without Relevance Labels"
- **Query2Doc:** Wang et al. (2023) "Query2doc: Query Expansion with Large Language Models"
- **Contrastive Learning:** Chen et al. (2020) "A Simple Framework for Contrastive Learning"
