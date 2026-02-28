# Experiment 004: Query2Doc + BM25 Retrieval

**Date:** February 12, 2026  
**Status:** ✅ Complete  
**Baseline:** Experiment 002 (BM25, Identity Enhancement)

---

## Objective

Test Query2Doc query expansion with BM25S sparse retrieval to evaluate LLM-based enhancement on term-matching retrieval.

---

## Methodology

### Query Enhancement: Query2Doc

**Approach:** LLM-based pseudo-document generation (same as Exp 003)  
**Reference:** Wang et al. (2023) "Query2doc: Query Expansion with Large Language Models"

### LLM Configuration

**Model:** Qwen 2.5 3B Instruct
- **Size:** ~6GB in float16
- **Context:** 32K tokens
- **Language:** Multilingual with strong Arabic support

**System Prompt:**
```
You are asked to write a passage that answers the given query. 
Do not ask the user for further clarification. 
Respond in Arabic only.
```

**Generation Parameters:**
```python
max_new_tokens = 128
temperature = 0.7
top_p = 0.9
batch_size = 8
```

---

## Two-Notebook Workflow

### Notebook 1: Query Generator
**Colab:** https://colab.research.google.com/drive/1BoKaHu-eqiAZUrpbPlReXpOkmvodQjhM

**Process:**
1. Load MIRACL Arabic dev set (2,896 queries)
2. Initialize Query2DocEnhancer with Qwen 2.5 3B
3. Enhance all queries (~40 minutes)
4. Save to `enhanced_queries_exp004.pkl`

**Output:** Enhanced queries file for reuse

### Notebook 2: Evaluator
**Colab:** https://colab.research.google.com/drive/1goRXAokKf0MrTnzmVQLGaWbs34_zZLo8

**Process:**
1. Upload `enhanced_queries_exp004.pkl`
2. Load BM25S retriever
3. Search with enhanced queries (~5 minutes)
4. Evaluate and print metrics

**Output:** BM25 retrieval metrics

---

## Experimental Setup

### Dataset
- **Corpus:** MIRACL Arabic (2,061,414 passages)
- **Queries:** 2,896 (dev set)
- **Language:** Modern Standard Arabic (MSA)

### Retrieval Configuration
- **Model:** BM25S (pure Python implementation)
- **Index:** Pre-built from Google Drive
- **k:** 100 documents retrieved per query
- **Parameters:** k1=0.9, b=0.4

### Evaluation Metrics
- Recall@10
- Recall@100
- NDCG@10
- MRR (Mean Reciprocal Rank)

---

## Results

### Performance Metrics

| Metric | Baseline (Exp 002) | Query2Doc (Exp 004) | Change |
|--------|-------------------|---------------------|--------|
| **Recall@10** | 0.5964 | 0.5384 | -9.7% |
| **Recall@100** | 0.8577 | 0.8155 | -4.9% |
| **NDCG@10** | 0.4621 | 0.4090 | -11.5% |
| **MRR** | 0.4836 | 0.4342 | -10.2% |

### Key Findings

**❌ Query2Doc DECREASED performance with BM25**

1. **All metrics declined:**
   - NDCG@10: -11.5% (most significant drop)
   - Recall@10: -9.7%
   - MRR: -10.2%
   - Recall@100: -4.9% (smallest drop)

2. **Contrast with Dense (Exp 003):**
   - Dense + Query2Doc: +8.93% NDCG@10 ✅
   - BM25 + Query2Doc: -11.5% NDCG@10 ❌
   - **Opposite effects on different retrievers**

3. **Possible Explanations:**
   - **Term dilution:** Added pseudo-document dilutes original query terms
   - **BM25 term weighting:** Long documents reduce term importance
   - **Vocabulary mismatch:** LLM-generated terms don't match corpus vocabulary
   - **Missing query repetition:** Query2Doc paper repeats query 5x for BM25

---

## Analysis

### Why Query2Doc Failed with BM25

#### 1. Term Dilution Effect

**Original query (short):**
```
"ما هي عاصمة السودان"  (What is the capital of Sudan)
```

**Enhanced query (long):**
```
"ما هي عاصمة السودان الخرطوم هي عاصمة جمهورية السودان..." (200+ words)
```

**BM25 behavior:**
- Original: High weight on "عاصمة" (capital), "السودان" (Sudan)
- Enhanced: Weight distributed across 200+ words
- Result: Important terms lose prominence

#### 2. Query2Doc Paper Recommendation

From Wang et al. (2023):

> "For sparse retrieval (BM25), we repeat the original query n=5 times before concatenating with pseudo-document to maintain term importance."

**We did NOT implement this:**
```python
# What we did:
enhanced = f"{query} {pseudo_doc}"

# What paper recommends:
enhanced = f"{query} {query} {query} {query} {query} {pseudo_doc}"
```

#### 3. Dense vs Sparse Behavior

| Aspect | Dense (mDPR) | BM25 |
|--------|-------------|------|
| **Matching** | Semantic similarity | Exact term matching |
| **Query length** | Flexible | Sensitive to length |
| **Expansion benefit** | Adds semantic context ✅ | Dilutes term weights ❌ |
| **Query2Doc effect** | +8.93% NDCG@10 | -11.5% NDCG@10 |

---

## Comparison with Query2Doc Paper

### Original Paper (MS-MARCO English)

**Sparse Retrieval (BM25):**
- Approach: Repeat query 5x + pseudo-document
- Results: +3-7% NDCG@10 improvement
- Model: GPT-3 text-davinci-003 (175B)

**Our Implementation (MIRACL Arabic):**
- Approach: Query 1x + pseudo-document (missing repetition)
- Results: -11.5% NDCG@10 decline
- Model: Qwen 2.5 3B

**Key Difference:** We did not implement query repetition for BM25!

---

## Comparison: Dense vs BM25 with Query2Doc

### Dense Retrieval (Exp 003)
```
Baseline:  NDCG@10 = 0.4993
Query2Doc: NDCG@10 = 0.5435
Change:    +8.93% ✅
```

### BM25 Retrieval (Exp 004)
```
Baseline:  NDCG@10 = 0.4621
Query2Doc: NDCG@10 = 0.4090
Change:    -11.5% ❌
```

### Interpretation

**Query2Doc is retriever-dependent:**
- ✅ Works well with semantic/dense retrieval
- ❌ Hurts term-based/sparse retrieval (without query repetition)
- 📝 Requires different implementation strategies per retriever type

---

## Runtime Performance

### Hardware
- **Platform:** Google Colab Free Tier
- **GPU:** T4 (15GB VRAM)

### Timing Breakdown
1. **Query Enhancement:** ~40 minutes (Notebook 1)
2. **BM25 Retrieval:** ~5 minutes (Notebook 2)
3. **Evaluation:** <1 minute
4. **Total:** ~45 minutes

### Efficiency
- **Queries per minute:** ~72 (enhancement)
- **Reusable:** Enhanced queries saved for future tests
- **Cost:** $0 (free Colab)

---

## Files Generated

### Enhanced Queries
```
enhanced_queries_exp004.pkl
```

### Results
```
results/query2doc_bm25/
└── exp_004_metrics.json
```

### Metrics JSON
```json
{
  "recall_10": 0.5384,
  "recall_100": 0.8155,
  "ndcg_cut_10": 0.4090,
  "recip_rank": 0.4342,
  "num_queries": 2896
}
```

---

## Lessons Learned

### 1. Retriever-Specific Implementation Required

Query enhancement techniques are NOT retriever-agnostic:
- Dense retrieval: Simple concatenation works
- Sparse retrieval: Needs query repetition or term weighting

### 2. Follow Paper Recommendations

The Query2Doc paper explicitly recommends:
- Dense: `query + pseudo_doc`
- Sparse: `query × 5 + pseudo_doc`

We only implemented the dense version for both retrievers.

### 3. Term-Based vs Semantic Matching

**Term-based (BM25):**
- Sensitive to term frequency
- Long queries dilute important terms
- Needs careful term weighting

**Semantic (Dense):**
- Captures meaning, not just terms
- Benefits from additional context
- More robust to query length

---

## Next Steps

### Immediate: Fix BM25 Implementation

Implement query repetition as per paper:

```python
# For BM25 retrieval
enhanced_query_bm25 = f"{query} {query} {query} {query} {query} {pseudo_doc}"

# For Dense retrieval (keep as is)
enhanced_query_dense = f"{query} {pseudo_doc}"
```

Expected: +3-7% improvement (matching paper's results)

---

## Conclusion

Query2Doc with Qwen 2.5 3B shows **opposite effects** on different retrievers:
- **Dense (mDPR):** +8.93% NDCG@10 ✅ Strong improvement
- **BM25:** -11.5% NDCG@10 ❌ Significant decline

The decline with BM25 is likely due to:
1. Missing query repetition (paper's recommendation)
2. Term dilution in long enhanced queries
3. Vocabulary mismatch between LLM and corpus

**Key Insight:** Query enhancement techniques must be adapted to retriever characteristics. What works for semantic matching may hurt term matching.

**Recommendation:** Implement retriever-specific enhancement strategies rather than one-size-fits-all approach.

---

## References

1. Wang, L., Yang, N., & Wei, F. (2023). Query2doc: Query Expansion with Large Language Models. arXiv preprint arXiv:2303.07678.

2. Zhang, X., et al. (2023). MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages. TACL.

---

**Experiment conducted by:** Mohammed Elhaj, Osman Bashir  
**Institution:** University of Khartoum  
**Date:** February 12, 2026
