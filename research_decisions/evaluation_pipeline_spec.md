# Evaluation Pipeline Specification
**Task:** 1.5 - Implement Evaluation Pipeline + Research Analysis Framework  
**Date:** January 14, 2026  
**Status:** Specification Complete - Ready for Implementation  
**Owner:** Mohammed (Research/Spec), Osman (Implementation)

---

## 1. Overview

This document specifies the evaluation pipeline design based on:
- 9/1/2026 meeting decisions (see `meetings/9.1.2026_meeting_outcomes.md`)
- Error analysis research (see `research_decisions/error_analysis_research.md`)

### Pipeline Philosophy
**Two-Phase Approach (Decided 9/1/2026):**
1. **Experiment Phase:** Run search → Save results to file
2. **Evaluation Phase:** Calculate metrics from saved results

**Two Purposes:**
1. Documentation for thesis (show our work)
2. Context for incremental improvement (act as context for Kiro/team)

---

## 2. Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     EXPERIMENT PHASE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Queries (MIRACL)  ──►  [Query Enhancement]  ──►  Enhanced Query│
│        │                    (optional)                │         │
│        │                                              │         │
│        ▼                                              ▼         │
│  ┌─────────────┐                            ┌─────────────┐     │
│  │  Retriever  │                            │  Retriever  │     │
│  │ (BM25/mDPR) │                            │ (BM25/mDPR) │     │
│  └─────────────┘                            └─────────────┘     │
│        │                                              │         │
│        ▼                                              ▼         │
│  Top-100 Results                            Top-100 Results     │
│  (Query ID, Passage ID, Score, Rank)                            │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              RESULTS FILE (JSON/JSONL)                   │   │
│  │  - Query ID                                              │   │
│  │  - List of (Passage ID, Score, Rank) for top 100         │   │
│  │  - Experiment metadata                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     EVALUATION PHASE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Results File  ──►  [Metric Calculator]  ──►  Metrics Report    │
│       +                                                         │
│  Qrels (MIRACL)                                                 │
│                                                                 │
│  Outputs:                                                       │
│  - Recall@10, Recall@100                                        │
│  - NDCG@10                                                      │
│  - MRR                                                          │
│  - Per-query breakdown                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ANALYSIS PHASE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Results + Metrics  ──►  [Analysis Tools]  ──►  Insights        │
│                                                                 │
│  Tools:                                                         │
│  - Score gap analysis                                           │
│  - Query feature correlation                                    │
│  - Wikipedia category extraction                                │
│  - Failed query clustering                                      │
│  - NoMIRACL hard negative analysis                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Storage Format Specification

### 3.1 Results File Format (Per Experiment)

**File:** `results/exp_XXX_results.jsonl`

```jsonl
{"query_id": "q001", "results": [{"passage_id": "doc123#0", "score": 0.85, "rank": 1}, {"passage_id": "doc456#2", "score": 0.72, "rank": 2}, ...]}
{"query_id": "q002", "results": [{"passage_id": "doc789#1", "score": 0.91, "rank": 1}, ...]}
```

**Fields:**
- `query_id`: MIRACL query identifier
- `results`: Array of top-100 results
  - `passage_id`: MIRACL passage identifier (format: `article_id#passage_num`)
  - `score`: Retrieval score from the system
  - `rank`: Position in results (1-100)

**Why JSONL:** One line per query, easy to stream/process large files.

### 3.2 Experiment Metadata File

**File:** `results/exp_XXX_metadata.json`

```json
{
  "experiment_id": "exp_001",
  "name": "BM25 Baseline",
  "date": "2026-01-15",
  "retriever": {
    "type": "BM25",
    "index": "miracl-v1.0-ar",
    "tool": "Pyserini"
  },
  "query_enhancement": {
    "enabled": false,
    "technique": null,
    "llm": null
  },
  "dataset": {
    "name": "MIRACL Arabic",
    "split": "dev",
    "num_queries": 2896
  },
  "parameters": {
    "top_k": 100
  }
}
```

### 3.3 Metrics Output File

**File:** `results/exp_XXX_metrics.json`

```json
{
  "experiment_id": "exp_001",
  "aggregate": {
    "recall_at_10": 0.456,
    "recall_at_100": 0.789,
    "ndcg_at_10": 0.481,
    "mrr": 0.523
  },
  "per_query": {
    "q001": {"recall_at_10": 0.5, "ndcg_at_10": 0.62, "mrr": 1.0},
    "q002": {"recall_at_10": 0.0, "ndcg_at_10": 0.0, "mrr": 0.0}
  }
}
```

---

## 4. Metrics Specification

### 4.1 Primary Metrics (Confirmed in meetings)

| Metric | Formula | What it Measures |
|--------|---------|------------------|
| **Recall@K** | (relevant in top-K) / (total relevant) | Coverage - did we find the relevant docs? |
| **NDCG@K** | Normalized DCG | Ranking quality - are relevant docs ranked higher? |
| **MRR** | 1 / (rank of first relevant) | Speed - how quickly do we find a relevant doc? |

### 4.2 K Values
- **Primary:** K=10 (main evaluation)
- **Secondary:** K=100 (for analysis, already saved)

### 4.3 Implementation Notes
- Use `pytrec_eval` or `ranx` library for standard implementations
- Ensure consistency with MIRACL leaderboard calculations
- Handle edge cases: queries with no relevant docs, ties in ranking

---

## 5. Analysis Framework (From Error Analysis Research)

Based on `research_decisions/error_analysis_research.md`, here's the analysis framework:

### 5.1 Immediate Analysis (Every Experiment)

| Analysis | Tool | Difficulty | Purpose |
|----------|------|------------|---------|
| **Score Gap** | Custom Python | Easy | Identify low-confidence retrievals |
| **Query Length Correlation** | Custom Python | Easy | Check if short queries fail more |
| **Rank Distribution** | ranx | Easy | See where relevant docs land |

**Score Gap Calculation:**
```python
score_gap = top_1_score - top_2_score
# Small gap = retriever is uncertain
# Large gap = retriever is confident
```

### 5.2 Short-term Analysis (After Baseline)

| Analysis | Tool | Difficulty | Purpose |
|----------|------|------------|---------|
| **Wikipedia Categories** | wikipedia-api | Easy | Domain-based error analysis |
| **NoMIRACL Hard Negatives** | HuggingFace dataset | Easy | Identify confusion patterns |
| **AAFAQ Query Classification** | Manual/Heuristic | Medium | Arabic-specific query types |

### 5.3 Advanced Analysis (If Time Permits)

| Analysis | Tool | Difficulty | Purpose |
|----------|------|------------|---------|
| **Failed Query Clustering** | E5-small + UMAP | Medium | Find thematic failure patterns |
| **LLM Topic Labeling** | Qwen/Llama API | Hard | Automated passage categorization |

---

## 6. Implementation Checklist

### Phase 1: Core Pipeline (Osman)
- [ ] Results saving function (JSONL format)
- [ ] Metadata saving function (JSON format)
- [ ] Metric calculation function (Recall, NDCG, MRR)
- [ ] Per-query metric breakdown
- [ ] Integration with Pyserini retrieval

### Phase 2: Analysis Tools (Mohammed)
- [ ] Score gap calculator
- [ ] Query length analyzer
- [ ] Wikipedia category fetcher script
- [ ] NoMIRACL dataset loader
- [ ] Basic visualization (rank distribution)

### Phase 3: Documentation
- [ ] Experiment template (✅ Created: `experiments/EXPERIMENT_TEMPLATE.md`)
- [ ] Example experiment doc after first baseline run

---

## 7. File Organization

```
results/
├── exp_001_bm25_baseline/
│   ├── exp_001_results.jsonl      # Raw retrieval results
│   ├── exp_001_metadata.json      # Experiment configuration
│   ├── exp_001_metrics.json       # Computed metrics
│   └── exp_001_analysis.json      # Analysis outputs (optional)
├── exp_002_mdpr_baseline/
│   └── ...
└── comparisons/
    └── baseline_comparison.json   # Cross-experiment comparisons

experiments/
├── EXPERIMENT_TEMPLATE.md         # Template for documentation
├── exp_001_bm25_baseline.md       # Human-readable experiment doc
├── exp_002_mdpr_baseline.md
└── ...
```

---

## 8. Dependencies

### Required Libraries
```
pyserini          # Retrieval (already using)
pytrec_eval       # Standard IR evaluation
ranx              # Ranking evaluation & visualization
wikipedia-api     # Category extraction
datasets          # HuggingFace (for NoMIRACL)
```

### Optional Libraries
```
sentence-transformers  # For clustering analysis
umap-learn            # For visualization
```

---

## 9. References

- Meeting decisions: `meetings/9.1.2026_meeting_outcomes.md`
- Error analysis research: `research_decisions/error_analysis_research.md`
- NoMIRACL paper: arXiv:2312.11361
- ranx library: https://github.com/AmenRa/ranx

---

**Document Status:** ✅ Specification Complete  
**Next Step:** Implementation by Osman  
**Review Date:** [After first baseline experiment]
