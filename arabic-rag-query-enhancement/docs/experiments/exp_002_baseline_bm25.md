# Experiment 002: BM25 Baseline (BM25S)

**Date:** January 26, 2026  
**Status:** ✅ Complete  
**Colab Notebook:** https://colab.research.google.com/drive/1AJmPYlLrhY1kLbwTWF2Ga7AyXWNWYemh

---

## 1. Objective

Establish the BM25S sparse retrieval baseline for MIRACL Arabic dataset using **Identity query enhancement** (no enhancement). This serves as the second baseline (alongside mDPR) for evaluating future query enhancement techniques.

**Research Question:** What is the baseline performance of BM25S on MIRACL Arabic without any query enhancement?

---

## 2. Methodology

### 2.1 Dataset
- **Name:** MIRACL Arabic (Dev Set)
- **Queries:** 2,896
- **Corpus:** 2,061,414 passages
- **Language:** Modern Standard Arabic (MSA)
- **Source:** Pre-built BM25S index stored in Google Drive

### 2.2 Retrieval System
- **Model:** BM25S (Pure Python implementation)
- **Library:** bm25s v0.2+
- **Index:** Pre-built from MIRACL corpus
- **Index Size:** ~ 0.5 GB (stored in Google Drive)
- **Tokenization:** Arabic stemming (PyStemmer)
- **Stopwords:** NLTK Arabic stopwords (245+ words)
- **BM25 Parameters:**
  - Method: Lucene-style BM25
  - k1: 0.9
  - b: 0.4

### 2.3 Query Enhancement
- **Technique:** Identity Enhancement
- **Implementation:** `IdentityEnhancer` class
- **Behavior:** Returns query unchanged (baseline)
- **Purpose:** Establish baseline without any enhancement

### 2.4 Implementation Details

**Hardware:**
- Platform: Google Colab
- CPU: Intel Xeon (2 cores)
- RAM: 12.7 GB
- GPU: Not used (BM25 is CPU-based)

**Software:**
- Python: 3.10
- bm25s: 0.2+
- PyStemmer: 2.2.0
- NLTK: 3.8+
- pytrec-eval: 0.5+

**Key Advantages:**
- No Java dependencies (unlike Pyserini)
- Pure Python implementation
- Easy integration with query enhancement
- Fast indexing and retrieval

### 2.5 Evaluation Metrics
- **Recall@10:** Proportion of relevant documents in top 10
- **Recall@100:** Proportion of relevant documents in top 100
- **NDCG@10:** Normalized Discounted Cumulative Gain at 10
- **MRR:** Mean Reciprocal Rank

---

## 3. Results

### 3.1 Quantitative Results

| Metric | Our Result | Pyserini Target | Achievement |
|--------|------------|-----------------|-------------|
| **Recall@10** | 0.5964 | - | (Thesis baseline) |
| **Recall@100** | 0.8577 | 0.889 | 96.48% ✅ |
| **NDCG@10** | 0.4621 | 0.481 | 96.07% ✅ |
| **MRR** | 0.4836 | - | - |
| **Queries** | 2,896 | 2,896 | 100% |

**Conclusion:** Achieved 96%+ of Pyserini target performance using pure Python implementation.

### 3.2 Performance Metrics

| Phase | Time | Notes |
|-------|------|-------|
| Index loading | <1 min | From Google Drive (cached) |
| Query tokenization | 1-2 min | Arabic stemming + stopwords |
| BM25 search | 2-3 min | CPU-based retrieval |
| Evaluation | <1 min | Metric computation |
| **Total** | **3-5 min** | Excluding first-time index download |

**CPU Utilization:** 80-90% during search phase

### 3.3 Comparison with Related Work

**BM25S (Our Implementation):**
- Recall@100: 0.8577
- NDCG@10: 0.4621

**Pyserini BM25 (Official):**
- Recall@100: 0.889
- NDCG@10: 0.481

**Difference:** ~4% lower (acceptable trade-off for pure Python implementation)

---

## 4. Analysis

### 4.1 Strengths

1. **Highest Recall@100 (0.8577):**
   - Retrieves 85.8% of relevant documents in top 100
   - Better than mDPR (0.8407) by 2%
   - Strong lexical matching capability

2. **No Java Dependencies:**
   - Pure Python implementation
   - Easier to integrate with LLM-based query enhancement
   - No JVM conflicts or version issues

3. **Fast Inference:**
   - 3-5 minutes for full dev set (2,896 queries)
   - Comparable to mDPR despite being CPU-only

4. **Reproducible:**
   - Deterministic results
   - Pre-built index ensures consistency

### 4.2 Limitations

1. **Lower Ranking Quality (vs mDPR):**
   - NDCG@10: 0.4621 vs 0.4993 (mDPR)
   - MRR: 0.4836 vs 0.5328 (mDPR)
   - Lexical matching doesn't capture semantic similarity

2. **Vocabulary Mismatch:**
   - Struggles when query and document use different words
   - No understanding of synonyms or paraphrases

3. **No Semantic Understanding:**
   - Pure term-based matching
   - Doesn't capture meaning or context

4. **Slightly Lower than Pyserini:**
   - 96% achievement vs official Pyserini
   - Trade-off for pure Python implementation

### 4.3 Observations

**Tokenization:**
- Arabic stemming reduces vocabulary size
- NLTK stopwords (245+ words) improve precision
- Preprocessing takes 1-2 minutes

**BM25 Search:**
- CPU-based search is efficient for this dataset size
- No need for GPU acceleration
- Lucene-style BM25 parameters (k1=0.9, b=0.4) work well

**Index Storage:**
- Google Drive integration works smoothly
- Symbolic links avoid data duplication
- Index loads quickly (<1 min)

---

## 5. Error Analysis

### 5.1 Query Types (Qualitative)

**Expected to perform well:**
- Queries with exact keyword matches
- Factual queries with specific terms
- Queries using common vocabulary

**Expected to struggle:**
- Queries with synonyms or paraphrases
- Semantic queries without keyword overlap
- Queries requiring inference
- Dialectal variations

### 5.2 Opportunities for Query Enhancement

Based on BM25 limitations, query enhancement could help with:

1. **Lexical Expansion:**
   - Add synonyms and related terms
   - Increase keyword overlap with documents

2. **Query Normalization:**
   - Standardize spelling variations
   - Remove diacritics
   - Handle dialectal Arabic

3. **Semantic Enrichment:**
   - Add context to short queries
   - Clarify ambiguous terms

4. **Term Weighting:**
   - Emphasize important query terms
   - De-emphasize stopwords

---

## 6. Files Generated

### 6.1 Results Files

**Location:** `results/baseline_bm25/`

1. **`exp_002_baseline_bm25.txt`** (TREC format)
   - Format: `query_id Q0 doc_id rank score run_name`
   - Size: ~290K lines (2,896 queries × 100 docs)
   - Purpose: Standard IR evaluation format

2. **`exp_002_metrics.json`**
   - Contains: All evaluation metrics
   - Format: JSON
   - Purpose: Easy parsing for analysis

### 6.2 Code Files

**Location:** `src/`

1. **`src/utils/data_loader_hf.py`**
   - Loads MIRACL topics and qrels from HuggingFace
   - No pyserini dependency
   - Used in: BM25 experiments

2. **`src/retrievers/bm25.py`**
   - BM25S retriever implementation
   - Loads pre-built index from Google Drive
   - Pure Python (no Java)
   - Used in: All BM25 experiments

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
CPU: Intel Xeon (2 cores)
RAM: 12.7 GB
Python: 3.10
Dependencies:
  - bm25s: 0.2+
  - PyStemmer: 2.2.0
  - nltk: 3.8+
  - pytrec-eval: 0.5+
  - requests: 2.31+
```

### 7.2 Reproduction Steps

1. Open Colab notebook: https://colab.research.google.com/drive/1AJmPYlLrhY1kLbwTWF2Ga7AyXWNWYemh
2. Run Step 1 (Installation)
3. Restart runtime
4. Run Step 2 (Mount Google Drive)
5. Update `drive_base` path in Step 3 (Updated)
6. Run remaining cells
7. Results will match within ±0.01

### 7.3 Expected Variability

- **Recall@100:** ±0.001 (deterministic)
- **NDCG@10:** ±0.001 (deterministic)
- **Runtime:** ±1 minute (depends on Colab load)

### 7.4 Google Drive Setup

**Required Files:**
- `bm25s_index/` - Pre-built BM25S index directory
- `corpus_ids.pkl` - Pickled corpus document IDs

**Path Structure:**
```
/content/drive/MyDrive/graduation_project/colab_data/
├── bm25s_index/
│   ├── indices.npz
│   ├── params.json
│   └── vocab.npz
└── corpus_ids.pkl
```

---

## 8. Comparison with Dense Baseline (Exp 001)

| Metric | BM25S (Sparse) | mDPR (Dense) | Difference |
|--------|----------------|--------------|------------|
| **Recall@100** | 0.8577 | 0.8407 | +0.0170 (+2.0%) ✅ |
| **NDCG@10** | 0.4621 | 0.4993 | -0.0372 (-7.5%) |
| **Recall@10** | 0.5964 | 0.6156 | -0.0192 (-3.1%) |
| **MRR** | 0.4836 | 0.5328 | -0.0492 (-9.2%) |

**Key Insights:**

1. **BM25 has higher Recall@100** ✅
   - Retrieves more relevant documents overall
   - Better lexical coverage
   - Advantage: +2.0%

2. **mDPR has higher NDCG@10** ✅
   - Better at ranking relevant documents in top 10
   - Superior semantic understanding
   - Advantage: +7.5%

3. **mDPR has higher MRR** ✅
   - Finds first relevant document earlier
   - Better for single-answer queries
   - Advantage: +9.2%

4. **Complementary Strengths:**
   - BM25: Better recall (retrieves more)
   - mDPR: Better precision (ranks better)
   - Suggests potential for hybrid approaches

---

## 9. Next Steps

### 9.1 Immediate Actions

1. ✅ **BM25 baseline established** - Reproduction complete
2. ✅ **Comparison with mDPR** - Complementary strengths identified
3. ⏳ **Select first QE technique** - Based on error analysis (Task 3.4)

### 9.2 Phase 2: Query Enhancement

**Candidate Techniques (from Task 3.4):**

1. **Query Expansion with Normalization** ✅ Selected
   - Primary: Address short query information poverty
   - Secondary: Normalize spelling/diacritics
   - Implementation: Gemini 1.5 Flash for expansion

2. **Alternative: HyDE**
   - If expansion shows <15% improvement
   - Generate hypothetical documents

**Selection Rationale:**
- Error analysis (Task 3.3) showed short queries achieve 59% of long query performance
- Query expansion directly addresses information poverty
- BM25 benefits from lexical expansion (more keywords)

### 9.3 Experiment 003 Plan

**Objective:** Test Query Expansion + Normalization on BM25

**Approach:**
1. Implement Query Expansion in `src/enhancers/expansion.py`
2. Create `exp_003_qe_bm25.ipynb`
3. Run with same BM25S retriever
4. Compare with Experiment 002 baseline

**Success Criteria:**
- NDCG@10 improvement > 2%
- Recall@10 improvement > 2%
- No significant Recall@100 degradation

---

## 10. Lessons Learned

### 10.1 Technical

1. **Pure Python BM25 is viable:**
   - No Java dependencies simplifies deployment
   - Performance is acceptable (96% of Pyserini)
   - Easier integration with LLM-based QE

2. **Google Drive integration works well:**
   - Symbolic links avoid data duplication
   - Index loads quickly
   - Enables sharing across experiments

3. **HuggingFace data loading is simple:**
   - Direct URL access to topics/qrels
   - No need for pyserini for data loading
   - Reduces dependencies

### 10.2 Research

1. **BM25 vs Dense trade-offs confirmed:**
   - BM25 better at recall (retrieves more)
   - Dense better at ranking (orders better)
   - Validates literature findings

2. **Lexical matching has limits:**
   - Vocabulary mismatch is a real problem
   - Query enhancement can help bridge gaps

3. **Baseline quality matters:**
   - 96% achievement is acceptable
   - Pure Python benefits outweigh 4% performance loss

---

## 11. References

### 11.1 Papers

1. **MIRACL Dataset:**
   - Zhang et al. (2022). "MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages"
   - https://arxiv.org/abs/2210.09984

2. **BM25 Algorithm:**
   - Robertson & Zaragoza (2009). "The Probabilistic Relevance Framework: BM25 and Beyond"

### 11.2 Code

- **BM25S Library:** https://github.com/xhluca/bm25s
- **Our Implementation:** https://github.com/Osmanoor/graduation

### 11.3 Related Experiments

- **Dense Baseline:** `docs/experiments/exp_001_baseline_dense.md`
- **BM25 Technical Report:** `reports/bm25_baseline_report.md`

---

## 12. Appendix

### 12.1 BM25 Parameters

**Lucene-style BM25:**
```python
k1 = 0.9   # Term frequency saturation
b = 0.4    # Length normalization
```

**Scoring Formula:**
```
score(D,Q) = Σ IDF(qi) × (f(qi,D) × (k1 + 1)) / (f(qi,D) + k1 × (1 - b + b × |D|/avgdl))
```

Where:
- `f(qi,D)` = frequency of term qi in document D
- `|D|` = length of document D
- `avgdl` = average document length
- `IDF(qi)` = inverse document frequency of qi

### 12.2 Tokenization Details

**Arabic Stemming:**
- Library: PyStemmer (Snowball stemmer)
- Language: Arabic
- Effect: Reduces inflected words to root forms

**Stopwords:**
- Source: NLTK Arabic stopwords
- Count: 245+ words
- Examples: في، من، إلى، على، etc.

### 12.3 Metric Definitions

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

### 12.4 Index Statistics

**Corpus:**
- Documents: 2,061,414
- Vocabulary size: ~500K unique terms (after stemming)
- Average document length: ~150 tokens
- Index size: ~0.5 GB

---

**Document Status:** ✅ Complete  
**Last Updated:** January 26, 2026  
**Next Review:** After Experiment 003
