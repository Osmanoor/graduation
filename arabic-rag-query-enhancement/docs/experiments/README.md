# Experiment Documentation

This directory contains detailed documentation for all experiments conducted in the Arabic RAG Query Enhancement project.

---

## Experiment Index

### Phase 1: Baseline Establishment

| ID | Name | Status | Date | Colab Link |
|----|------|--------|------|------------|
| 001 | Dense Baseline (mDPR) | ✅ Complete | 2026-01-16 | [Colab](https://colab.research.google.com/drive/1WAqG5-fK0NTjKZFCir15x4km3a1n4P1M?usp=sharing) |
| 002 | BM25 Baseline | ⏳ Pending | - | - |

### Phase 2: Query Enhancement

| ID | Name | Status | Date | Colab Link |
|----|------|--------|------|------------|
| 003 | QE + Dense (TBD) | ⏳ Pending | - | - |
| 004 | QE + BM25 (TBD) | ⏳ Pending | - | - |

---

## Experiment 001: Dense Baseline (mDPR)

**Status:** ✅ Complete  
**Documentation:** [exp_001_baseline_dense.md](exp_001_baseline_dense.md)  
**Colab:** https://colab.research.google.com/drive/1WAqG5-fK0NTjKZFCir15x4km3a1n4P1M?usp=sharing

**Objective:** Establish mDPR baseline with Identity enhancement (no enhancement)

**Results:**
- Recall@10: 0.6156
- Recall@100: 0.8407 (Target: 0.841) ✅
- NDCG@10: 0.4993 (Target: 0.499) ✅
- MRR: 0.5328

**Key Findings:**
- Successfully reproduced MIRACL results (99.96% accuracy)
- GPU acceleration provides 5-7x speedup
- mDPR better at ranking (NDCG) than recall (vs BM25)

---

## Experiment 002: BM25 Baseline

**Status:** ⏳ Pending  
**Planned Date:** TBD

**Objective:** Establish BM25 sparse retrieval baseline

**Expected Results:**
- Recall@100: ~0.860
- NDCG@10: ~0.461

---

## Documentation Template

Each experiment document should include:

1. **Objective** - Research question and goals
2. **Methodology** - Dataset, model, parameters
3. **Results** - Quantitative metrics and performance
4. **Analysis** - Strengths, limitations, observations
5. **Error Analysis** - What worked, what didn't
6. **Files Generated** - Results and code
7. **Reproducibility** - Environment and steps
8. **Comparison** - With other experiments
9. **Next Steps** - Future work
10. **Lessons Learned** - Technical and research insights
11. **References** - Papers and code
12. **Appendix** - Additional details

---

## Quick Reference

### Baseline Results Summary

| Experiment | Retriever | Enhancement | Recall@10 | Recall@100 | NDCG@10 | MRR |
|------------|-----------|-------------|-----------|------------|---------|-----|
| 001 | mDPR | Identity | 0.6156 | 0.8407 | 0.4993 | 0.5328 |
| 002 | BM25 | Identity | - | - | - | - |

### Performance Comparison

| Metric | mDPR | BM25 | Winner |
|--------|------|------|--------|
| Recall@100 | 0.8407 | 0.8603 | BM25 (+2.3%) |
| NDCG@10 | 0.4993 | 0.4610 | mDPR (+8.3%) |
| Recall@10 | 0.6156 | 0.5926 | mDPR (+3.9%) |
| MRR | 0.5328 | 0.4821 | mDPR (+10.5%) |

**Insight:** Dense and sparse retrievers have complementary strengths.

---

## File Locations

### Experiment Notebooks
- `experiments/exp_001_baseline_dense.ipynb`
- `experiments/exp_002_baseline_bm25.ipynb` (future)

### Results
- `results/baseline_dense/` - Dense baseline results
- `results/baseline_bm25/` - BM25 baseline results (future)
- `results/enhanced/` - Enhanced results (future)

### Documentation
- `docs/experiments/` - This directory
- `reports/` - Technical reports

---

## Naming Convention

**Experiment IDs:**
- Format: `exp_XXX_description`
- Example: `exp_001_baseline_dense`

**Files:**
- Notebook: `experiments/exp_XXX_description.ipynb`
- Documentation: `docs/experiments/exp_XXX_description.md`
- Results: `results/category/exp_XXX_*.txt`

---

## Status Legend

- ✅ **Complete** - Experiment finished and documented
- 🔄 **In Progress** - Currently running
- ⏳ **Pending** - Planned but not started
- ❌ **Failed** - Encountered issues
- 🔁 **Rerun** - Needs to be rerun

---

## Contact

For questions about experiments:
- Mohammed Elhaj: [email]
- Osman Bashir: [email]

---

**Last Updated:** January 16, 2026
