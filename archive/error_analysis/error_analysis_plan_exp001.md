# Error Analysis Plan: Experiment 001 (Dense Baseline - mDPR)
**Date:** January 17, 2026  
**Experiment:** exp_001_baseline_dense  
**Baseline:** mDPR (Identity Enhancement - No QE)  
**Status:** Plan Ready for Execution

---

## Context & Background

### Experiment Results (from exp_001_metrics.json)
- **Recall@10:** 0.6156
- **Recall@100:** 0.8407
- **NDCG@10:** 0.4993
- **MRR:** 0.5328
- **Queries:** 2,896

### Comparison with BM25S Baseline
| Metric | mDPR (Dense) | BM25S (Sparse) | Winner |
|--------|--------------|----------------|--------|
| Recall@100 | 0.8407 | 0.8603 | BM25S (+2.3%) |
| NDCG@10 | 0.4993 | 0.4610 | mDPR (+8.3%) |
| Recall@10 | 0.6156 | 0.5926 | mDPR (+3.9%) |
| MRR | 0.5328 | 0.4821 | mDPR (+10.5%) |

**Key Insight:** BM25 retrieves more docs, mDPR ranks them better. Complementary strengths!

---

## Goals of Error Analysis

Per `research_decisions/miracal_metdata_refrence_reports/error analysis best practices.md`:

1. **Build Intuition** - Understand what types of queries succeed/fail
2. **Identify Weaknesses** - Find patterns in failures that QE can address
3. **Guide Iteration** - Select the right QE technique based on evidence

**End Goal:** Move from "The system failed" to "The system failed *because*..." to "Therefore, we fix it by..."

---

## Analysis Framework

Based on:
- `research_decisions/error_analysis_research.md` (4-provider synthesis)
- `research_decisions/miracal_metdata_refrence_reports/error analysis best practices.md`
- `research_decisions/evaluation_pipeline_spec.md`

### Phase 1: Quantitative Analysis (CPU-based, run locally)
| Analysis | What We Measure | Why It Matters |
|----------|-----------------|----------------|
| **Per-query metrics** | NDCG@10, Recall@10, MRR per query | Identify failed queries |
| **Query length** | Token count distribution | Short queries often ambiguous |
| **Score gaps** | Top-1 vs Top-2 score difference | Confidence/uncertainty indicator |
| **Rank distribution** | Where do relevant docs land? | Informs if re-ranking helps |
| **Failure thresholds** | Queries with NDCG@10 < 0.3 | Focus on worst performers |

### Phase 2: Qualitative Analysis (Manual + AI-assisted)
| Analysis | Sample Size | Method |
|----------|-------------|--------|
| **Failed queries** | 20 worst | Manual AAFAQ categorization |
| **Successful queries** | 20 best | Understand what works |
| **Linguistic forensics** | 10-15 samples | Arabic-specific issues |

### Phase 3: Synthesis
- Create failure taxonomy
- Map failures to QE techniques
- Recommend first technique
- Document in `research_decisions/error_analysis_results_exp001.md`

---

## Implementation Plan

### Step 1: Data Preparation (Local)
**Script:** `arabic-rag-query-enhancement/src/analysis/load_exp001_data.py`

Load from HuggingFace (no Java/Pyserini needed):
```python
# Topics (queries)
from datasets import load_dataset
miracl = load_dataset("miracl/miracl", "ar")
topics = miracl['dev']  # 2,896 queries

# Qrels (relevance judgments)
# Parse from HuggingFace or download TSV

# Results (already have)
# arabic-rag-query-enhancement/results/baseline_dense/exp_001_baseline_dense.txt
```

**Output:** JSON files for easy analysis
- `data/processed/exp001_topics.json`
- `data/processed/exp001_qrels.json`
- `data/processed/exp001_results.json` (parsed from TREC format)

---

### Step 2: Quantitative Analysis (Local)
**Script:** `arabic-rag-query-enhancement/src/analysis/analyze_exp001_quantitative.py`

**Analyses to perform:**

1. **Per-Query Metrics**
   - Compute NDCG@10, Recall@10, MRR for each query
   - Save to `results/baseline_dense/exp_001_per_query_metrics.json`

2. **Query Length Analysis**
   - Tokenize queries (simple whitespace split for Arabic)
   - Compute: min, max, mean, median length
   - Correlation: length vs NDCG@10
   - Plot: length distribution for failed vs successful queries

3. **Score Gap Analysis**
   - For each query: score_gap = top_1_score - top_2_score
   - Compute: mean, median, distribution
   - Correlation: score_gap vs NDCG@10
   - Identify "low confidence" queries (small gap)

4. **Rank Distribution**
   - For each query with relevant docs:
     - Find rank of first relevant doc
     - Find rank of all relevant docs
   - Plot: histogram of first relevant doc rank
   - Compute: % of queries with relevant in top-10, top-20, top-50, top-100

5. **Failure Segmentation**
   - Define thresholds:
     - Failed: NDCG@10 < 0.3
     - Mediocre: 0.3 ≤ NDCG@10 < 0.7
     - Successful: NDCG@10 ≥ 0.7
   - Count queries in each bucket
   - Export failed query IDs for qualitative analysis

**Output:**
- `results/baseline_dense/exp_001_quantitative_analysis.json` (all stats)
- `results/baseline_dense/exp_001_failed_queries.json` (for Phase 2)
- Console report with key findings

---

### Step 3: Qualitative Analysis (Separate Chat + Subagents)
**Location:** New chat session (when context full here)

**Input Files:**
- `results/baseline_dense/exp_001_failed_queries.json` (from Step 2)
- `data/processed/exp001_topics.json` (query text)
- `data/processed/exp001_qrels.json` (ground truth)
- `results/baseline_dense/exp_001_baseline_dense.txt` (retrieved docs)

**Tasks:**
1. **Sample Selection**
   - 20 worst queries (lowest NDCG@10)
   - 20 best queries (highest NDCG@10)
   - 10 random mediocre queries

2. **Manual Categorization** (using AAFAQ framework)
   - Question type: Factoid, List, Definition, Why, How, etc.
   - Complexity: Simple, Medium, Complex
   - Named entities: Yes/No
   - Temporal: Yes/No

3. **Linguistic Forensics** (Arabic-specific)
   - Morphology issues: Missing prefixes/suffixes
   - Root mismatch: Query root ≠ doc root
   - Spelling variations: Hamza, Ta marbuta, Alif maqsura
   - Dialect: MSA vs dialectal terms
   - Diacritics: Ambiguity from missing diacritics

4. **Failure Hypothesis Generation**
   - For each failed query, hypothesize why it failed
   - Group hypotheses into categories

**Output:**
- `research_decisions/error_analysis_results_exp001.md` (full report)

---

### Step 4: Synthesis & Recommendation
**Location:** Continuation of qualitative analysis chat

**Tasks:**
1. **Create Failure Taxonomy**
   - Categorize failures by root cause
   - Quantify: X% due to vocabulary gap, Y% due to ambiguity, etc.

2. **Map to QE Techniques**
   | Failure Pattern | Recommended QE Technique |
   |-----------------|--------------------------|
   | Short ambiguous queries | HyDE (generate context) |
   | Vocabulary mismatch | Query Expansion (synonyms) |
   | Morphology issues | Query Rewriting (normalize) |
   | Complex multi-part | Query Decomposition |

3. **Select First Technique**
   - Based on most common failure pattern
   - Consider: implementation complexity, API costs, expected impact

4. **Document Decision**
   - Update `research_decisions/open_questions.md` (Task 3.4)
   - Update `RESEARCH_CONTEXT_KERNEL.md.md`
   - Update `TASKS.md` with outcomes

**Output:**
- `research_decisions/qe_technique_selection.md` (decision rationale)

---

## Reference Files

### For Context
- `RESEARCH_CONTEXT_KERNEL.md.md` - Project state
- `TASKS.md` - Task 3.3 (this analysis)
- `research_decisions/error_analysis_research.md` - Research synthesis
- `research_decisions/miracal_metdata_refrence_reports/error analysis best practices.md` - Best practices

### For Implementation
- `arabic-rag-query-enhancement/src/evaluation/metrics.py` - Existing metrics code
- `arabic-rag-query-enhancement/experiments/bm25s_baseline.ipynb` - Data loading pattern
- `arabic-rag-query-enhancement/results/baseline_dense/exp_001_baseline_dense.txt` - Results
- `arabic-rag-query-enhancement/results/baseline_dense/exp_001_metrics.json` - Aggregate metrics

### For Documentation
- `arabic-rag-query-enhancement/docs/experiments/exp_001_baseline_dense.md` - Experiment doc
- `reports/mdpr_baseline_report.md` - Technical report

---

## Execution Timeline

| Phase | Duration | Location | Owner |
|-------|----------|----------|-------|
| **Step 1: Data Prep** | 30 min | This chat | Kiro |
| **Step 2: Quantitative** | 1-2 hours | This chat | Kiro + Mohammed |
| **Step 3: Qualitative** | 2-3 hours | New chat | Kiro + Subagents |
| **Step 4: Synthesis** | 1 hour | New chat | Mohammed + Kiro |

**Total:** ~5-7 hours of work

---

## Success Criteria

We succeed when we can say:

> "Our mDPR baseline failed on [X% of queries with pattern Y]. By analyzing the failed queries, we found that [specific issue Z]. Our recommended Query Enhancement technique is [technique name] because [evidence-based rationale]."

---

## Next Steps (Immediate)

1. ✅ **This document created** - Plan is ready
2. ⏳ **Create data loading script** - `src/analysis/load_exp001_data.py`
3. ⏳ **Create quantitative analysis script** - `src/analysis/analyze_exp001_quantitative.py`
4. ⏳ **Run quantitative analysis** - Execute locally
5. ⏳ **Review findings** - Discuss in this chat
6. ⏳ **Prepare for qualitative** - Export data for new chat session

---

**Document Status:** ✅ Plan Complete  
**Ready to Execute:** Yes  
**Next Action:** Create analysis scripts

