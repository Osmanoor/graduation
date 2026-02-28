# Experiment Documentation

This directory contains detailed documentation for all experiments conducted in the Arabic RAG Query Enhancement project.

---

## Experiment Index

### Phase 1: Baseline Establishment

| ID | Name | Status | Date | Colab Link |
|----|------|--------|------|------------|
| 001 | Dense Baseline (mDPR) | ✅ Complete | 2026-01-16 | [Colab](https://colab.research.google.com/drive/1WAqG5-fK0NTjKZFCir15x4km3a1n4P1M?usp=sharing) |
| 002 | BM25 Baseline (BM25S) | ✅ Complete | 2026-01-26 | [Colab](https://colab.research.google.com/drive/1AJmPYlLrhY1kLbwTWF2Ga7AyXWNWYemh) |

### Phase 2: Query Enhancement

| ID | Name | Status | Date | Colab Link |
|----|------|--------|------|------------|
| 003 | Query2Doc + Dense (Qwen 2.5 3B) | ✅ Complete | 2026-02-11 | [Colab](https://colab.research.google.com/drive/1dfjqvgYbELPimgUvtnnFkTegZHPL5IQl) |
| 004 | Query2Doc + BM25 (Qwen 2.5 3B) | ✅ Complete | 2026-02-12 | [Generator](https://colab.research.google.com/drive/1BoKaHu-eqiAZUrpbPlReXpOkmvodQjhM) / [Evaluator](https://colab.research.google.com/drive/1goRXAokKf0MrTnzmVQLGaWbs34_zZLo8) |

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

## Experiment 002: BM25 Baseline (BM25S)

**Status:** ✅ Complete  
**Documentation:** [exp_002_baseline_bm25.md](exp_002_baseline_bm25.md)  
**Colab:** https://colab.research.google.com/drive/1AJmPYlLrhY1kLbwTWF2Ga7AyXWNWYemh

**Objective:** Establish BM25S baseline with Identity enhancement (no enhancement)

**Results:**
- Recall@10: 0.5964
- Recall@100: 0.8577 (Target: 0.889) ✅
- NDCG@10: 0.4621 (Target: 0.481) ✅
- MRR: 0.4836

**Key Findings:**
- Achieved 96%+ of Pyserini target (pure Python implementation)
- Higher Recall@100 than mDPR (+2.0%)
- Lower NDCG@10 than mDPR (-7.5%)
- Complementary strengths with Dense retrieval

---

## Experiment 003: Query2Doc + Dense (Qwen 2.5 3B)

**Status:** ✅ Complete  
**Documentation:** [exp_003_query2doc_dense.md](exp_003_query2doc_dense.md)  
**Colab:** https://colab.research.google.com/drive/1dfjqvgYbELPimgUvtnnFkTegZHPL5IQl

**Objective:** Test Query2Doc LLM-based query expansion with Dense retrieval (mDPR)

**Results:**
- Recall@10: 0.6608 (baseline: 0.6156) = +7.3%
- Recall@100: 0.8594 (baseline: 0.8407) = +2.2%
- NDCG@10: 0.5435 (baseline: 0.4993) = +8.9% ✅
- MRR: 0.5742 (baseline: 0.5328) = +7.8%

**Key Findings:**
- ALL metrics improved with Query2Doc enhancement
- +8.9% NDCG@10 exceeds original Query2Doc paper results
- Zero-shot 3B model outperforms few-shot 175B GPT-3 from paper
- Query expansion ratio: 9.73x (median: 8.45x)
- Runtime: ~40 minutes on Colab T4 (free tier)

---

## Experiment 004: Query2Doc + BM25 (Qwen 2.5 3B)

**Status:** ✅ Complete  
**Documentation:** [exp_004_query2doc_bm25.md](exp_004_query2doc_bm25.md)  
**Colab:** [Generator](https://colab.research.google.com/drive/1BoKaHu-eqiAZUrpbPlReXpOkmvodQjhM) / [Evaluator](https://colab.research.google.com/drive/1goRXAokKf0MrTnzmVQLGaWbs34_zZLo8)

**Objective:** Test Query2Doc LLM-based query expansion with BM25 sparse retrieval

**Results:**
- Recall@10: 0.5384 (baseline: 0.5964) = -9.7% ❌
- Recall@100: 0.8155 (baseline: 0.8577) = -4.9% ❌
- NDCG@10: 0.4090 (baseline: 0.4621) = -11.5% ❌
- MRR: 0.4342 (baseline: 0.4836) = -10.2% ❌

**Key Findings:**
- ALL metrics declined with Query2Doc enhancement
- Opposite effect vs Dense: +8.9% (Dense) vs -11.5% (BM25)
- Likely cause: Missing query repetition (paper recommends 5x for BM25)
- Term dilution hurts BM25 term weighting
- Two-notebook workflow: Generator (~40 min) + Evaluator (~5 min)

**Lesson:** Query enhancement techniques must be adapted to retriever type

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

### All Results Summary

| Experiment | Retriever | Enhancement | Recall@10 | Recall@100 | NDCG@10 | MRR |
|------------|-----------|-------------|-----------|------------|---------|-----|
| 001 | mDPR | Identity | 0.6156 | 0.8407 | 0.4993 | 0.5328 |
| 002 | BM25S | Identity | 0.5964 | 0.8577 | 0.4621 | 0.4836 |
| 003 | mDPR | Query2Doc (Qwen 2.5 3B) | 0.6608 | 0.8594 | 0.5435 | 0.5742 |
| 004 | BM25S | Query2Doc (Qwen 2.5 3B) | 0.5384 | 0.8155 | 0.4090 | 0.4342 |

### Baseline Performance Comparison

| Metric | mDPR (001) | BM25S (002) | Winner |
|--------|------|-------|--------|
| Recall@100 | 0.8407 | 0.8577 | BM25S (+2.0%) |
| NDCG@10 | 0.4993 | 0.4621 | mDPR (+8.0%) |
| Recall@10 | 0.6156 | 0.5964 | mDPR (+3.2%) |
| MRR | 0.5328 | 0.4836 | mDPR (+10.2%) |

**Insight:** Dense and sparse retrievers have complementary strengths.

### Query2Doc Enhancement Impact

| Metric | Dense (003 vs 001) | BM25 (004 vs 002) |
|--------|-------------------|-------------------|
| Recall@10 | +7.3% ✅ | -9.7% ❌ |
| Recall@100 | +2.2% ✅ | -4.9% ❌ |
| NDCG@10 | +8.9% ✅ | -11.5% ❌ |
| MRR | +7.8% ✅ | -10.2% ❌ |

**Insight:** Query2Doc helps semantic retrieval but hurts term-based retrieval (without query repetition).

---

## File Locations

### Experiment Notebooks
- `experiments/exp_001_baseline_dense.ipynb`
- `experiments/exp_003_query2doc_dense.ipynb`
- `experiments/Query_generator_query2doc.ipynb` (exp_004 generator)
- `experiments/evaluate_enhanced_queries.ipynb` (exp_004 evaluator)

### Results
- `results/baseline_dense/` - Dense baseline results (exp_001)
- `results/baseline_bm25/` - BM25 baseline results (exp_002)
- `results/exp_003_query2doc_dense/` - Query2Doc + Dense results
- `results/query2doc_bm25/` - Query2Doc + BM25 results (exp_004)

### Enhanced Queries
- `enhanced_queries_exp003.pkl` - Query2Doc enhanced queries (Qwen 2.5 3B)
- `enhanced_queries_exp004.pkl` - Same as exp_003 (reused for BM25)

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

**Last Updated:** February 12, 2026
