Here is the updated Technical Report. It explicitly distinguishes between the successful **CLI approach (Attempt C)** and the currently failing **Python Code approach (Attempt D)**, highlighting this as a critical open issue for Phase 2.

---

# Technical Report: MIRACL Arabic BM25 Baseline Reproduction
**Date:** January 10, 2026  
**Updated:** January 12, 2026  
**Subject:** Discrepancy Between CLI and Python Code Execution in Reproducing SOTA Retrieval  
**Dataset:** MIRACL (Arabic Subset)  
**Method:** Sparse Retrieval (BM25)

---

## 1. Executive Summary
The objective was to reproduce the official BM25 baseline for the MIRACL Arabic dataset (**Recall@100 $\approx$ 0.889**).

While we successfully reproduced this result using the **Command Line Interface (CLI)** within a specific legacy environment, attempts to reproduce the same result using **Python Code** (required for future Query Enhancement experiments) consistently failed, yielding a significantly lower score (**Recall@100 $\approx$ 0.23**).

**Update (12/1/2026):** After documenting the Pyserini blocker, we implemented an alternative solution using **BM25S** (pure Python) that achieves **Recall@100 = 0.8603** (96.8% of target) and provides clean QE integration without Java dependencies.

This report documents the five distinct implementation attempts.

---

## 2. Methodology & Implementation Attempts

### Attempt A: Modern Environment (CLI & Code)
*   **Configuration:** Python 3.12, Java 21 (System Default).
*   **Result:** **Failure** (Recall@100 $\approx$ 0.23).
*   **Diagnosis:** The official index (built with Lucene 8/Java 11) is incompatible with the modern `ArabicAnalyzer` in Java 21. The stemmers produce different roots, causing a semantic mismatch.

### Attempt B: Local Index Reconstruction (CLI)
*   **Configuration:** Python 3.12, Java 21.
*   **Approach:** Rebuilt the index locally from raw data using Java 21.
*   **Result:** **Partial Success** (Recall@100 $\approx$ 0.79).
*   **Analysis:** While internally consistent, the modern Lucene implementation performs worse on this specific dataset than the legacy version. This establishes a "Modern Baseline" but fails to reproduce the paper's results.

### Attempt C: The "Time Machine" via CLI (Success) ✅
*   **Configuration:** Conda Environment (Python 3.8, OpenJDK 11, Pyserini 0.19.0).
*   **Execution:** Standard Pyserini CLI command (`python -m pyserini.search.lucene ...`).
*   **Result:** **Success** (Recall@100 = **0.889**).
*   **Conclusion:** The environment setup is correct. The binary dependencies (MKL, Faiss, Torch) and Java version are capable of reproducing the result.

### Attempt D: The "Time Machine" via Python Code (Open Issue) ❌
*   **Configuration:** Exact same Conda Environment as Attempt C.
*   **Execution:** Python script (`searcher = LuceneSearcher.from_prebuilt_index(...)`).
*   **Result:** **Failure** (Recall@100 = **0.235**).
*   **Observation:** Even inside the correct Conda environment, the Python script produces the *exact* low score associated with the Java Version Mismatch (see Attempt A).

---

## 3. Analysis of the Open Issue (Attempt C vs. D)

The critical finding is that **Attempt C (CLI)** and **Attempt D (Code)** behave differently despite running in the exact same shell environment.

| Feature | Attempt C (CLI) | Attempt D (Python Code) |
| :--- | :--- | :--- |
| **Command** | `python -m pyserini.search...` | `searcher = LuceneSearcher(...)` |
| **Java Version Used** | **Java 11** (Correct) | **Java 21** (Incorrect System Fallback) |
| **Mechanism** | Pyserini's `__main__` wrapper sets up JVM args before execution. | `pyjnius` initializes JVM implicitly on import. |
| **Recall@100** | **0.889** | **0.235** |

### Root Cause Hypothesis
The Python bindings (Pyjnius) are failing to detect the Conda environment's `JAVA_HOME` when run programmatically. Instead, they are "escaping" the environment and locking onto the System Java (Java 21) installed on the host machine. 

Once the JVM is started by Pyjnius with the wrong version, it cannot be restarted or switched within the same Python process, leading to the tokenizer mismatch.

---

## 4. Current Status & Blockers

**Status:**
1.  **Environment:** ✅ Validated (via Attempt C).
2.  **Binary Dependencies:** ✅ Fixed (MKL/Faiss linking issues resolved).
3.  **Code Execution:** ⚠️ **Critical Blocker.**

**The Problem:**
Phase 2 (Query Enhancement) requires us to intercept the query inside a Python loop to apply LLM expansions. We cannot do this using the CLI (Attempt C). We *must* use the Python Code (Attempt D).

**Required Resolution:**
We must force the Python script to ignore the System Java and strictly utilize the Conda OpenJDK 11 binaries. Standard `os.environ` setting inside the script has proven insufficient; the fix likely requires shell-level injection or aggressive removal of the System Java.

---

## 5. Alternative Solution: BM25S Implementation (Attempt E)

**Date:** January 12, 2026

Given the Pyserini blocker documented above, we implemented an alternative approach using BM25S, a pure-Python BM25 library.

### Configuration
*   **Library:** BM25S v0.2+ (https://github.com/xhluca/bm25s)
*   **Environment:** Python 3.10+, Google Colab
*   **Stemmer:** PyStemmer (Arabic)
*   **Stopwords:** Manual list (20 words), testing NLTK (245 words)
*   **BM25 Parameters:** k1=0.9, b=0.4 (matching Lucene-style)

### Results

| Metric | BM25S Result | MIRACL Target | Achievement |
|--------|--------------|---------------|-------------|
| **Recall@100** | 0.8603 | 0.889 | 96.8% |
| **NDCG@10** | 0.4610 | 0.481 | 95.8% |
| **Recall@10** | 0.5926 | - | (Thesis metric) |
| **MRR** | 0.4821 | - | - |

### Gap Analysis
The 3.2% gap in Recall@100 is attributed to:
1. **Tokenization:** Whitespace-based vs Lucene's advanced Arabic analyzer
2. **Stemmer:** PyStemmer vs Lucene's ISRI implementation  
3. **Stopwords:** Currently 20 manual words vs Lucene's proprietary list (testing NLTK's 245 words)

### Advantages for Phase 2
1. ✅ **No Java dependencies** - eliminates all JVM configuration issues
2. ✅ **Clean Python API** - easy QE integration in loops
3. ✅ **Fast performance** - 500x faster than rank-bm25
4. ✅ **Index persistence** - save/load for reuse across experiments
5. ✅ **Reproducible** - works consistently in Colab

### Code Example (QE Integration)
```python
# Load saved index
retriever = bm25s.BM25.load("data/miracl_ar/bm25s_index")

# Apply query enhancement
enhanced_query = llm_enhance(original_query)

# Retrieve
query_tokens = bm25s.tokenize([enhanced_query], 
                               stopwords=arabic_stopwords,
                               stemmer=stemmer)
results, scores = retriever.retrieve(query_tokens, k=100)
```

### Resources
- **Colab Notebook:** https://colab.research.google.com/drive/1KJ5bWrrJnSqQ8NYI7gd0uAT1db4F69T_?usp=sharing
- **Local Code:** `experiments/bm25s_baseline.ipynb`

---

## 6. Next Steps

### For Pyserini (if needed in future)
1.  **Investigate JVM Injection:** Determine how to pass `-Djava.home` arguments explicitly to the `LuceneSearcher` constructor or `pyjnius` backend.
2.  **System Java Removal:** Attempt the "Scorched Earth" strategy: uninstall Java 21 from the host OS entirely so Python has no incorrect option to fall back on.
3.  **Manual Binding:** Verify if we can manually point `pyjnius` to the specific `libjvm.so` file inside the Conda directory before importing Pyserini.

### For BM25S (current path)
1. ✅ **Baseline established** - 0.8603 Recall@100
2. ⏳ **Validate NLTK stopwords** - may improve to ~0.87-0.88
3. ⏳ **Optional: Test Farasa stemmer** - potential 1-2% additional improvement