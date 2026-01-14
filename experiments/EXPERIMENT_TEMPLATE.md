# Experiment: [EXP_ID] - [Short Title]
**Date:** [YYYY-MM-DD]  
**Owner:** [Name]  
**Status:** [Running / Complete / Failed]

---

## 1. Motivation
**Why are we running this experiment?**
- [What question are we trying to answer?]
- [What hypothesis are we testing?]
- [What previous result motivated this?]

**Related Experiments:** [Link to previous experiments if any]

---

## 2. Setup

### 2.1 Retriever Configuration
| Parameter | Value |
|-----------|-------|
| Retriever Type | [BM25 / mDPR / BGE-M3 / etc.] |
| Index | [Pyserini index name or custom] |
| Top-K | [10 / 100 / etc.] |

### 2.2 Query Enhancement (if applicable)
| Parameter | Value |
|-----------|-------|
| Technique | [None (baseline) / HyDE / Query Rewriting / etc.] |
| LLM Used | [Model name and version] |
| Prompt | [See Section 2.3 or "N/A"] |

### 2.3 Prompt Used (if applicable)
```
[Paste the exact prompt here, or write "N/A" for baseline]
```

### 2.4 Dataset
| Parameter | Value |
|-----------|-------|
| Dataset | MIRACL Arabic |
| Split | [dev / test / train] |
| Subset Size | [Full / N queries] |
| Subset Selection | [Random / First N / Stratified / etc.] |

### 2.5 Environment
| Parameter | Value |
|-----------|-------|
| Platform | [Colab Free / Colab Pro / Local] |
| GPU | [T4 / None / etc.] |
| Runtime | [Estimated or actual time] |

---

## 3. Results

### 3.1 Primary Metrics
| Metric | Value | Baseline | Δ (Change) |
|--------|-------|----------|------------|
| Recall@10 | [X.XXX] | [X.XXX] | [+/-X.X%] |
| Recall@100 | [X.XXX] | [X.XXX] | [+/-X.X%] |
| NDCG@10 | [X.XXX] | [X.XXX] | [+/-X.X%] |
| MRR | [X.XXX] | [X.XXX] | [+/-X.X%] |

### 3.2 Results File Location
```
[Path to saved results file, e.g., results/exp_001_results.json]
```

### 3.3 Score Distribution (Optional)
- Mean score of top-1 doc: [X.XX]
- Mean score gap (top-1 vs top-2): [X.XX]
- Queries with zero relevant in top-10: [N / total]

---

## 4. Analysis

### 4.1 Immediate Observations
- [What do the numbers tell us?]
- [Any surprising results?]

### 4.2 Error Analysis (if performed)
**Failed Queries (NDCG@10 < 0.1):** [N queries]

| Query ID | Query Text | Failure Hypothesis |
|----------|------------|-------------------|
| [ID] | [Text] | [Why did it fail?] |

**Improved Queries (vs baseline):** [N queries]
- [Any patterns in what improved?]

### 4.3 Query-Side Analysis (Optional)
| Query Feature | Correlation with Success |
|---------------|-------------------------|
| Query Length | [Positive / Negative / None] |
| Contains Named Entity | [Yes/No pattern] |
| Question Type (AAFAQ) | [Factoid better / etc.] |

---

## 5. Conclusions

### 5.1 Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### 5.2 Implications for Next Experiment
- [What should we try next based on these results?]
- [What hypothesis does this generate?]

### 5.3 Limitations
- [What can't we conclude from this experiment?]
- [What confounding factors exist?]

---

## 6. Artifacts

### 6.1 Code
- Notebook: `[path/to/notebook.ipynb]`
- Script: `[path/to/script.py]`

### 6.2 Data Files
- Results: `[path/to/results.json]`
- Logs: `[path/to/logs.txt]`

### 6.3 Visualizations (if any)
- [Link or embed charts/graphs]

---

## 7. Notes
[Any additional observations, ideas for future work, or context that doesn't fit above]

---

**Document Created:** [Date]  
**Last Updated:** [Date]
