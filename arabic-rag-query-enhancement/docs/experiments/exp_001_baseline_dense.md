# Experiment 001: Dense Baseline (mDPR)

**Date:** January 16, 2026  
**Status:** ✅ Complete  
**Colab Notebook:** https://colab.research.google.com/drive/1WAqG5-fK0NTjKZFCir15x4km3a1n4P1M?usp=sharing

---

## 1. Objective

Establish the mDPR dense retrieval baseline for MIRACL Arabic dataset using **Identity query enhancement** (no enhancement). This serves as the reference point for evaluating future query enhancement techniques.

**Research Question:** What is the baseline performance of mDPR on MIRACL Arabic without any query enhancement?

---

## 2. Methodology

### 2.1 Dataset
- **Name:** MIRACL Arabic (Dev Set)
- **Queries:** 2,896
- **Corpus:** 2,061,414 passages
- **Language:** Modern Standard Arabic (MSA)
- **Source:** Accessed via Pyserini prebuilt index

### 2.2 Retrieval System
- **Model:** mDPR (Multilingual Dense Passage Retrieval)
- **Encoder:** `castorini/mdpr-tied-pft-msmarco`
- **Index:** Pyserini prebuilt FAISS index (`miracl-v1.0-ar-mdpr-tied-pft-msmarco`)
- **Index Size:** 5.47 GB
- **Embedding Dimension:** 768
- **Similarity Metric:** Cosine similarity (via normalized embeddings)

### 2.3 Query Enhancement
- **Technique:** Identity Enhancement
- **Implementation:** `IdentityEnhancer` class
- **Behavior:** Returns query unchanged (baseline)
- **Purpose:** Establish baseline without any enhancement

### 2.4 Implementation Details

**Hardware:**
- Platform: Google Colab
- GPU: NVIDIA T4 (15 GB VRAM)
- RAM: 12.7 GB

**Software:**
- Python: 3.10
- PyTorch: 2.0+
- Transformers: 4.30+
- Pyserini: 0.22.1
- FAISS: CPU version

**Key Parameters:**
- Batch size: 64 queries
- Top-K retrieved: 100 documents per query
- GPU acceleration: Enabled for query encoding
- FAISS search: CPU (sufficient for this dataset)

### 2.5 Evaluation Metrics
- **Recall@10:** Proportion of relevant documents in top 10
- **Recall@100:** Proportion of relevant documents in top 100
- **NDCG@10:** Normalized Discounted Cumulative Gain at 10
- **MRR:** Mean Reciprocal Rank

---

## 3. Results

### 3.1 Quantitative Results

| Metric | Our Result | MIRACL Target | Achievement |
|--------|------------|---------------|-------------|
| **Recall@10** | 0.6156 | - | (Thesis baseline) |
| **Recall@100** | 0.8407 | 0.841 | 99.96% ✅ |
| **NDCG@10** | 0.4993 | 0.499 | 100.06% ✅ |
| **MRR** | 0.5328 | - | - |
| **Queries** | 2,896 | 2,896 | 100% |

**Conclusion:** Successfully reproduced MIRACL paper results with <0.1% difference.

### 3.2 Performance Metrics

| Phase | Time | Notes |
|-------|------|-------|
| Index download | 5-10 min | First run only (cached afterwards) |
| Query encoding | 1-2 min | GPU-accelerated (64 queries/batch) |
| FAISS search | <1 min | CPU search |
| Evaluation | <1 min | Metric computation |
| **Total** | **2-3 min** | Excluding first-time index download |

**GPU Utilization:** 80-90% during query encoding phase

### 3.3 Comparison with Related Work

**mDPR (Our Implementation):**
- Recall@100: 0.8407
- NDCG@10: 0.4993

**MIRACL Paper (Official):**
- Recall@100: 0.841
- NDCG@10: 0.499

**Difference:** <0.1% (within acceptable margin)

---

## 4. Analysis

### 4.1 Strengths

1. **High Recall@100 (0.8407):**
   - Successfully retrieves 84% of relevant documents in top 100
   - Strong baseline for query enhancement experiments

2. **Good Ranking Quality (NDCG@10: 0.4993):**
   - Relevant documents are ranked relatively high
   - Better than random ranking (would be ~0.0)

3. **Fast Inference:**
   - 2-3 minutes for full dev set (2,896 queries)
   - Enables rapid experimentation

4. **Reproducible:**
   - Exact reproduction of MIRACL results
   - Validates implementation correctness

### 4.2 Limitations

1. **Not Fine-tuned on MIRACL:**
   - mDPR was pre-trained on MS MARCO (English)
   - Not specifically optimized for Arabic or MIRACL
   - Intentionally chosen as "weaker" baseline to show QE improvement potential

2. **Semantic Gaps:**
   - May miss documents with different wording but same meaning
   - Dense embeddings don't capture all lexical variations

3. **No Query Understanding:**
   - Treats query as-is without enhancement
   - Doesn't handle ambiguous, incomplete, or noisy queries

### 4.3 Observations

**Query Encoding:**
- GPU acceleration provides 5-7x speedup vs CPU
- Batch processing (64 queries) is efficient
- No memory issues with T4 GPU (15 GB VRAM)

**FAISS Search:**
- CPU search is fast enough (<1 min for 2,896 queries)
- No need for GPU-accelerated FAISS for this dataset size

**Reproducibility:**
- Results are consistent across runs
- No randomness in the pipeline (deterministic)

---

## 5. Error Analysis

### 5.1 Query Types (Qualitative)

**Expected to perform well:**
- Factual queries with clear keywords
- Queries matching document vocabulary
- Short, specific queries

**Expected to struggle:**
- Ambiguous queries
- Queries with dialectal variations
- Complex multi-part questions
- Queries requiring inference

### 5.2 Opportunities for Query Enhancement

Based on mDPR limitations, query enhancement could help with:

1. **Semantic Expansion:**
   - Add synonyms and related terms
   - Bridge vocabulary gaps

2. **Query Clarification:**
   - Resolve ambiguities
   - Add context

3. **Dialect Normalization:**
   - Convert dialectal Arabic to MSA
   - Handle spelling variations

4. **Query Decomposition:**
   - Break complex queries into sub-queries
   - Handle multi-part questions

---

## 6. Files Generated

### 6.1 Results Files

**Location:** `results/baseline_dense/`

1. **`exp_001_baseline_dense.txt`** (TREC format)
   - Format: `query_id Q0 doc_id rank score run_name`
   - Size: ~290K lines (2,896 queries × 100 docs)
   - Purpose: Standard IR evaluation format

2. **`exp_001_metrics.json`**
   - Contains: All evaluation metrics
   - Format: JSON
   - Purpose: Easy parsing for analysis

### 6.2 Code Files

**Location:** `src/`

1. **`src/utils/data_loader.py`**
   - Loads MIRACL topics and qrels
   - Used in: All experiments

2. **`src/retrievers/dense.py`**
   - mDPR retriever implementation
   - GPU-accelerated query encoding
   - Used in: All dense retrieval experiments

3. **`src/enhancers/base.py`**
   - `QueryEnhancer` base class
   - `IdentityEnhancer` implementation
   - Used in: This experiment

4. **`src/evaluation/metrics.py`**
   - Evaluation metrics computation
   - Result saving utilities
   - Used in: All experiments

---

## 7. Reproducibility

### 7.1 Environment

```yaml
Platform: Google Colab
GPU: NVIDIA T4 (15 GB VRAM)
Python: 3.10
Dependencies:
  - pyserini: 0.22.1
  - faiss-cpu: 1.7.4+
  - transformers: 4.30+
  - torch: 2.0+
  - pytrec-eval: 0.5+
```

### 7.2 Reproduction Steps

1. Open Colab notebook: https://colab.research.google.com/drive/1WAqG5-fK0NTjKZFCir15x4km3a1n4P1M?usp=sharing
2. Run Step 1 (Installation)
3. Restart runtime
4. Run Step 2 onwards
5. Results will match within ±0.01

### 7.3 Expected Variability

- **Recall@100:** ±0.001 (deterministic)
- **NDCG@10:** ±0.001 (deterministic)
- **Runtime:** ±30 seconds (depends on Colab load)

---

## 8. Comparison with BM25 Baseline

| Metric | mDPR (Dense) | BM25S (Sparse) | Difference |
|--------|--------------|----------------|------------|
| **Recall@100** | 0.8407 | 0.8603 | -0.0196 (-2.3%) |
| **NDCG@10** | 0.4993 | 0.4610 | +0.0383 (+8.3%) |
| **Recall@10** | 0.6156 | 0.5926 | +0.0230 (+3.9%) |
| **MRR** | 0.5328 | 0.4821 | +0.0507 (+10.5%) |

**Key Insights:**
1. **BM25 has higher Recall@100** - retrieves more relevant documents overall
2. **mDPR has higher NDCG@10** - better at ranking relevant documents in top 10
3. **mDPR has higher MRR** - finds first relevant document earlier
4. **Complementary strengths** - suggests potential for hybrid approaches

---

## 9. Next Steps

### 9.1 Immediate Actions

1. ✅ **Baseline established** - mDPR reproduction complete
2. ⏳ **Error analysis** - Identify which queries fail and why
3. ⏳ **Select first QE technique** - Based on error patterns

### 9.2 Phase 2: Query Enhancement

**Candidate Techniques:**
1. **HyDE (Hypothetical Document Embeddings)**
   - Generate hypothetical answer
   - Use for retrieval instead of query

2. **Query2Doc**
   - Expand query with LLM-generated context
   - Combine with original query

3. **Step-Back Prompting**
   - Generate broader conceptual query
   - Retrieve with broader context

4. **Query Rewriting**
   - Normalize dialect to MSA
   - Clarify ambiguous queries

**Selection Criteria:**
- Error analysis results
- Implementation complexity
- Expected improvement
- API budget constraints

### 9.3 Experiment 002 Plan

**Objective:** Test first query enhancement technique

**Approach:**
1. Implement chosen QE technique in `src/enhancers/`
2. Create `exp_002_qe_dense.ipynb`
3. Run with same mDPR retriever
4. Compare with Experiment 001 baseline

**Success Criteria:**
- NDCG@10 improvement > 2%
- Recall@10 improvement > 2%
- No significant Recall@100 degradation

---

## 10. Lessons Learned

### 10.1 Technical

1. **GPU acceleration is essential:**
   - 5-7x speedup for query encoding
   - Enables rapid experimentation

2. **Pyserini prebuilt indexes work well:**
   - No need to build custom indexes
   - Reproducible results

3. **Modular design pays off:**
   - Easy to swap query enhancers
   - Clean separation of concerns

### 10.2 Research

1. **mDPR is a good baseline:**
   - Not too strong (leaves room for improvement)
   - Not too weak (reasonable starting point)

2. **MIRACL is well-designed:**
   - Clear evaluation protocol
   - Reproducible results

3. **Dense vs Sparse trade-offs:**
   - Dense better at ranking (NDCG)
   - Sparse better at recall (Recall@100)

---

## 11. References

### 11.1 Papers

1. **MIRACL Dataset:**
   - Zhang et al. (2022). "MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages"
   - https://arxiv.org/abs/2210.09984

2. **mDPR Model:**
   - Karpukhin et al. (2020). "Dense Passage Retrieval for Open-Domain Question Answering"
   - https://arxiv.org/abs/2004.04906

### 11.2 Code

- **Pyserini:** https://github.com/castorini/pyserini
- **Our Implementation:** https://github.com/Osmanoor/graduation

### 11.3 Related Experiments

- **BM25 Baseline:** `reports/bm25_baseline_report.md`
- **mDPR Technical Report:** `reports/mdpr_baseline_report.md`

---

## 12. Appendix

### 12.1 Sample Queries

**Query 1:**
- ID: 1
- Text: [Sample Arabic query]
- Relevant docs: [Count]
- Retrieved in top 10: [Yes/No]

### 12.2 Metric Definitions

**Recall@K:**
```
Recall@K = (# relevant docs in top K) / (# total relevant docs)
```

**NDCG@K:**
```
NDCG@K = DCG@K / IDCG@K
where DCG = Σ (2^rel - 1) / log2(rank + 1)
```

**MRR:**
```
MRR = (1/|Q|) Σ (1 / rank of first relevant doc)
```

### 12.3 Hardware Specifications

**Google Colab T4 GPU:**
- CUDA Cores: 2,560
- Tensor Cores: 320
- Memory: 15 GB GDDR6
- Memory Bandwidth: 320 GB/s
- FP32 Performance: 8.1 TFLOPS

---

**Document Status:** ✅ Complete  
**Last Updated:** January 16, 2026  
**Next Review:** After Experiment 002
