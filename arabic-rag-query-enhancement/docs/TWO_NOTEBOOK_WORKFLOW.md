# Two-Notebook Workflow for Query Enhancement Evaluation

## Overview

This workflow separates query enhancement from retrieval evaluation into two independent notebooks. This approach is efficient for testing multiple models or retrievers without re-running expensive LLM inference.

**Benefits:**
- ✅ Run enhancement once, evaluate multiple times
- ✅ Save time when testing different retrievers
- ✅ Save GPU memory by separating concerns
- ✅ Reusable enhanced queries for future experiments
- ✅ Easy to compare different LLM models

---

## Workflow Architecture

```
┌─────────────────────────────────────────┐
│  Notebook 1: Query Generator            │
│  (Query_generator_query2doc.ipynb)      │
│                                          │
│  Input:  Original queries (MIRACL)      │
│  Process: LLM enhancement (Qwen 2.5 3B) │
│  Output:  enhanced_queries.pkl          │
│  Time:    ~40 minutes                   │
└─────────────────────────────────────────┘
                    ↓
         enhanced_queries.pkl
                    ↓
┌─────────────────────────────────────────┐
│  Notebook 2: Evaluator                  │
│  (evaluate_enhanced_queries.ipynb)      │
│                                          │
│  Input:  enhanced_queries.pkl           │
│  Process: Dense + BM25 retrieval        │
│  Output:  Metrics for both retrievers   │
│  Time:    ~10 minutes                   │
└─────────────────────────────────────────┘
```

---

## Notebook 1: Query Generator

**File:** `experiments/Query_generator_query2doc.ipynb`

### Purpose
Generate enhanced queries using an LLM (Query2Doc technique) and save them to a pickle file.

### Steps

#### 1. Installation & Setup
```python
# Install dependencies
!pip install -q pyserini faiss-cpu pytrec-eval transformers torch datasets accelerate bitsandbytes

# Restart runtime after installation
```

#### 2. Load Data
```python
from src.utils.data_loader import MIRACLDataLoader

data_loader = MIRACLDataLoader(language="ar", split="dev")
topics, qrels = data_loader.load_all()

query_ids = list(topics.keys())
query_texts = [topics[qid]['title'] for qid in query_ids]
```

#### 3. Initialize Enhancer
```python
from src.enhancers.query2doc import Query2DocEnhancer

enhancer = Query2DocEnhancer(
    model_name="Qwen/Qwen2.5-3B-Instruct",
    max_new_tokens=128,
    temperature=0.7,
    batch_size=8
)
```

#### 4. Enhance Queries
```python
enhanced_queries = enhancer.enhance_batch(
    query_texts,
    query_ids,
    show_progress=True
)
```

#### 5. Save to File
```python
import pickle

with open('enhanced_queries_exp003.pkl', 'wb') as f:
    pickle.dump({
        'query_ids': query_ids,
        'original': query_texts,
        'enhanced': enhanced_queries
    }, f)

print("✓ Saved to: enhanced_queries_exp003.pkl")
```

### Output File Structure

```python
{
    'query_ids': ['query-1', 'query-2', ...],      # List of query IDs
    'original': ['original text 1', ...],           # Original queries
    'enhanced': ['enhanced text 1', ...]            # Enhanced queries
}
```

### Runtime
- **First run:** ~45 minutes (includes model download ~6GB)
- **Subsequent runs:** ~40 minutes

### Memory Usage
- **GPU:** ~8GB (Qwen 2.5 3B in float16)
- **RAM:** ~4GB

---

## Notebook 2: Evaluator

**File:** `experiments/evaluate_enhanced_queries.ipynb`

### Purpose
Load pre-enhanced queries and evaluate them with multiple retrievers (Dense + BM25).

### Steps

#### 1. Installation & Setup
```python
# Install dependencies
!pip install -q pyserini faiss-cpu pytrec-eval transformers torch datasets bm25s PyStemmer nltk requests

# Restart runtime after installation
```

#### 2. Link Indexes
```python
drive_base = '/content/drive/MyDrive/graduation project/colab_data'

!ln -sf {drive_base}/mdpr_faiss.index data/miracl_ar/mdpr_faiss.index
!ln -sf {drive_base}/docid_map.pkl data/miracl_ar/docid_map.pkl
!ln -sf {drive_base}/bm25s_index data/miracl_ar/bm25s_index
!ln -sf {drive_base}/corpus_ids.pkl data/miracl_ar/corpus_ids.pkl
```

#### 3. Upload Enhanced Queries
```python
from google.colab import files

uploaded = files.upload()  # Upload enhanced_queries_exp003.pkl
```

#### 4. Load Enhanced Queries
```python
import pickle

with open('enhanced_queries_exp003.pkl', 'rb') as f:
    data = pickle.load(f)

query_ids = data['query_ids']
enhanced_queries = data['enhanced']
```

#### 5. Evaluate with Dense Retriever
```python
from src.retrievers.dense import mDPRRetriever

dense_retriever = mDPRRetriever(
    index_path='data/miracl_ar/mdpr_faiss.index',
    docid_map_path='data/miracl_ar/docid_map.pkl',
    device='cuda'
)

dense_results_list = dense_retriever.search(enhanced_queries, k=100)
dense_metrics = evaluator.evaluate(dense_results)
```

#### 6. Evaluate with BM25 Retriever
```python
from src.retrievers.bm25 import BM25SRetriever

bm25_retriever = BM25SRetriever(
    index_path='data/miracl_ar/bm25s_index',
    corpus_ids_path='data/miracl_ar/corpus_ids.pkl'
)

bm25_results_list = bm25_retriever.search(enhanced_queries, k=100)
bm25_metrics = evaluator.evaluate(bm25_results)
```

#### 7. Compare Results
```python
print(f'Dense: NDCG@10={dense_metrics["ndcg_cut_10"]:.4f}')
print(f'BM25:  NDCG@10={bm25_metrics["ndcg_cut_10"]:.4f}')
```

### Runtime
- **Dense evaluation:** ~5 minutes
- **BM25 evaluation:** ~5 minutes
- **Total:** ~10 minutes

### Memory Usage
- **GPU:** ~4GB (for Dense retriever)
- **RAM:** ~6GB (for BM25 index)

---

## Use Cases

### 1. Test Multiple LLM Models

Generate enhanced queries with different models:

```bash
# Run Query Generator with Qwen 2.5 3B
enhanced_queries_qwen25_3b.pkl

# Run Query Generator with Qwen 2.5 7B
enhanced_queries_qwen25_7b.pkl

# Run Query Generator with Gemma 3 4B
enhanced_queries_gemma3_4b.pkl
```

Then evaluate each with the same Evaluator notebook.

### 2. Test Different Enhancement Parameters

```python
# Temperature 0.1 (focused)
enhancer = Query2DocEnhancer(temperature=0.1)
# Save as: enhanced_queries_temp01.pkl

# Temperature 0.7 (balanced)
enhancer = Query2DocEnhancer(temperature=0.7)
# Save as: enhanced_queries_temp07.pkl

# Temperature 1.0 (diverse)
enhancer = Query2DocEnhancer(temperature=1.0)
# Save as: enhanced_queries_temp10.pkl
```

### 3. Test Additional Retrievers

Add new retriever to Evaluator notebook:

```python
# Hybrid retriever (RRF)
from src.retrievers.hybrid import HybridRetriever

hybrid_retriever = HybridRetriever(dense_retriever, bm25_retriever)
hybrid_results = hybrid_retriever.search(enhanced_queries, k=100)
hybrid_metrics = evaluator.evaluate(hybrid_results)
```

---

## File Naming Convention

Use descriptive names for enhanced query files:

```
enhanced_queries_{model}_{params}.pkl

Examples:
- enhanced_queries_qwen25_3b_temp07.pkl
- enhanced_queries_qwen25_7b_temp01.pkl
- enhanced_queries_gemma3_4b_temp05.pkl
- enhanced_queries_jais_8b_temp07.pkl
```

---

## Comparison Workflow

### Step 1: Generate Enhanced Queries (Multiple Models)

Run Query Generator notebook for each model:

1. Qwen 2.5 3B → `enhanced_queries_qwen25_3b.pkl`
2. Qwen 2.5 7B → `enhanced_queries_qwen25_7b.pkl`
3. Gemma 3 4B → `enhanced_queries_gemma3_4b.pkl`

**Time:** 40 min × 3 models = 2 hours

### Step 2: Evaluate All Models

Run Evaluator notebook for each pkl file:

1. Upload `enhanced_queries_qwen25_3b.pkl` → Get metrics
2. Upload `enhanced_queries_qwen25_7b.pkl` → Get metrics
3. Upload `enhanced_queries_gemma3_4b.pkl` → Get metrics

**Time:** 10 min × 3 models = 30 minutes

### Step 3: Compare Results

Create comparison table:

| Model | Dense NDCG@10 | Dense Recall@100 | BM25 NDCG@10 | BM25 Recall@100 |
|-------|---------------|------------------|--------------|-----------------|
| Qwen 2.5 3B | 0.5435 | 0.8594 | 0.4821 | 0.8677 |
| Qwen 2.5 7B | ? | ? | ? | ? |
| Gemma 3 4B | ? | ? | ? | ? |

---

## Advantages Over Single Notebook

### Traditional Approach (Single Notebook)
```
Enhancement + Dense + BM25 = 40 + 5 + 5 = 50 minutes per model
3 models = 150 minutes total
```

### Two-Notebook Approach
```
Enhancement (3 models) = 40 × 3 = 120 minutes
Evaluation (3 models) = 10 × 3 = 30 minutes
Total = 150 minutes (same time)

BUT: Can re-evaluate anytime without re-enhancement!
```

### Benefits
1. **Flexibility:** Test new retrievers without re-running LLM
2. **Debugging:** If evaluation fails, just re-run evaluator
3. **Sharing:** Share pkl files with team members
4. **Reproducibility:** Exact same enhanced queries for all tests
5. **Cost:** No repeated API calls for same queries

---

## Troubleshooting

### Issue: File Upload Fails

**Solution:** Use Google Drive instead:

```python
# In Query Generator: Save to Drive
with open('/content/drive/MyDrive/enhanced_queries.pkl', 'wb') as f:
    pickle.dump(data, f)

# In Evaluator: Load from Drive
with open('/content/drive/MyDrive/enhanced_queries.pkl', 'rb') as f:
    data = pickle.load(f)
```

### Issue: Out of Memory in Query Generator

**Solution:** Reduce batch size:

```python
enhancer = Query2DocEnhancer(
    batch_size=4  # Reduce from 8 to 4
)
```

### Issue: Slow Enhancement

**Solution:** Reduce max_new_tokens:

```python
enhancer = Query2DocEnhancer(
    max_new_tokens=64  # Reduce from 128
)
```

### Issue: Pillow Conflict Warning

**Solution:** Ignore it - doesn't affect functionality. Just restart runtime after installation.

---

## Best Practices

### 1. Always Save Metadata

Include model info in pkl file:

```python
with open('enhanced_queries.pkl', 'wb') as f:
    pickle.dump({
        'query_ids': query_ids,
        'original': query_texts,
        'enhanced': enhanced_queries,
        'metadata': {
            'model': 'Qwen/Qwen2.5-3B-Instruct',
            'temperature': 0.7,
            'max_new_tokens': 128,
            'date': '2026-02-12',
            'num_queries': len(query_ids)
        }
    }, f)
```

### 2. Verify Before Saving

```python
# Check enhancement quality
print(f"Original: {query_texts[0]}")
print(f"Enhanced: {enhanced_queries[0][:200]}")

# Check lengths
print(f"Avg expansion: {sum(len(e) for e in enhanced_queries) / sum(len(o) for o in query_texts):.2f}x")
```

### 3. Keep Organized

```
results/
├── enhanced_queries/
│   ├── qwen25_3b_temp07.pkl
│   ├── qwen25_7b_temp07.pkl
│   └── gemma3_4b_temp07.pkl
└── evaluations/
    ├── qwen25_3b_results.json
    ├── qwen25_7b_results.json
    └── gemma3_4b_results.json
```

---

## Next Steps

1. **Model Comparison:** Test 10 different LLM models (Task 4.0b in TASKS.md)
2. **Parameter Tuning:** Test different temperatures and token lengths
3. **Hybrid Retrieval:** Combine Dense + BM25 using RRF
4. **Error Analysis:** Analyze which queries benefit most from enhancement

---

## Summary

**Query Generator Notebook:**
- Purpose: Generate enhanced queries once
- Input: Original MIRACL queries
- Output: enhanced_queries.pkl
- Time: ~40 minutes
- Run: Once per model/configuration

**Evaluator Notebook:**
- Purpose: Evaluate enhanced queries with retrievers
- Input: enhanced_queries.pkl
- Output: Metrics for Dense + BM25
- Time: ~10 minutes
- Run: Multiple times with same pkl file

**Total Efficiency:** Generate once, evaluate many times!

---

**Created:** February 12, 2026  
**Team:** Mohammed Elhaj, Osman Bashir  
**Institution:** University of Khartoum
