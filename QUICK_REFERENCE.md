# Quick Reference Guide — Arabic RAG Query Enhancement

**For:** Quick lookups, presentations, and thesis defense preparation  
**Last Updated:** May 9, 2026

---

## The One-Sentence Summary

We improved Arabic information retrieval by +54.5% using small open-source language models (2-8B parameters) to expand queries with corpus-grounded vocabulary, demonstrating that different retrievers benefit from different query representations.

---

## Key Numbers (Memorize These)

| Metric | Value | Context |
|--------|-------|---------|
| **Final NDCG@10** | **0.7137** | Best system (CSQE + Hybrid RRF) |
| **Improvement** | **+54.5%** | Over BM25 baseline (0.4621) |
| **Dataset Size** | 2.1M passages | MIRACL Arabic corpus |
| **Queries Tested** | 2,896 | Dev set, MSA only |
| **Models Tested** | 10 | 2B to 8B parameters |
| **Best Model** | Aya Expanse 8B | +23.5% on Dense alone |
| **Runtime** | ~50 minutes | Full pipeline on Colab |
| **Cost** | $0 | All open-source, free Colab |

---

## The Three-Stage Story

### Stage 1: Blind Query Enhancement (Query2Doc)
- **What:** LLM generates pseudo-document from parametric knowledge
- **Result:** +8.9% NDCG@10 on Dense (Qwen 2.5 3B)
- **Problem:** BM25 degraded (−11.5%) due to term dilution
- **Fix:** Query repetition (n=5-7) recovered all models

### Stage 2: Corpus-Steered Enhancement (CSQE)
- **What:** BM25 first-pass retrieval → LLM extracts from actual corpus docs
- **Result:** +33.2% NDCG@10 on BM25 (Aya 8B)
- **Advantage:** +5.2% over blind QE through vocabulary grounding
- **Gap:** Still 0.011 points short of hybrid baseline

### Stage 3: Hybrid Fusion + Asymmetric QE
- **What:** BM25+CSQE + Dense (original query) with RRF fusion
- **Result:** 0.7137 NDCG@10 (+54.5% over baseline)
- **Key Insight:** Different retrievers need different query representations
- **Achievement:** Beat hybrid baseline by +13.9%

---

## The Research Gap We Filled

| Gap | Before Our Work | Our Contribution |
|-----|----------------|------------------|
| **Language** | QE techniques only tested on English | First comprehensive Arabic QE study |
| **Model Size** | Required 175B+ proprietary models | Proved 2-8B open-source models work |
| **Corpus Grounding** | No CSQE evaluation on Arabic | First CSQE application to MIRACL Arabic |
| **Retriever Specificity** | Same query for all retrievers | Discovered asymmetric QE is optimal |

---

## Experiment Quick Reference

| Exp | Name | Key Result | Insight |
|-----|------|------------|---------|
| 001 | mDPR Baseline | 0.4993 NDCG@10 | Better ranking than BM25 |
| 002 | BM25 Baseline | 0.4621 NDCG@10 | Better recall than mDPR |
| 003 | Query2Doc + Dense | 0.5435 (+8.9%) | Zero-shot 3B > few-shot 175B |
| 004 | Query2Doc + BM25 | 0.4090 (−11.5%) | Term dilution without repetition |
| 005-010 | Model Comparison | 0.5178 to 0.6164 | Size correlates with performance |
| 011 | BM25 Repetition Fix | 0.5855 (Aya β=2) | Recovered all degraded models |
| 012 | Hybrid Baseline | 0.6267 (RRF k=20) | Strong non-QE baseline |
| 013 | CSQE | 0.6157 (BM25+CSQE) | Corpus grounding works |
| 021 | CSQE + Hybrid | **0.7137** | **Best system** |

---

## Model Leaderboard (Dense Retrieval)

| Rank | Model | NDCG@10 | Size | Type |
|------|-------|---------|------|------|
| 1 | Aya Expanse 8B | 0.6164 | 8B | Multilingual |
| 2 | Jais-2-8B | 0.6018 | 8B | Arabic-specialized |
| 3 | Qwen3-8B | 0.5966 | 8B | Multilingual |
| 4 | Qwen 2.5-7B | 0.5811 | 7B | Multilingual |
| 5 | Qwen3-4B | 0.5691 | 4B | Multilingual |
| 6 | Gemma 3 4B | 0.5397 | 4B | Multilingual |
| 7 | Falcon-H1-3B | 0.5359 | 3B | Arabic-specialized |
| 8 | Qwen 2.5-3B | 0.5435 | 3B | Multilingual |
| 9 | SILMA 2B | 0.5178 | 2B | Arabic RAG-specific |

**Best for BM25:** Jais-2-8B (0.5731 with β=2) — Arabic vocabulary advantage

---

## Key Findings (Defense Talking Points)

### 1. Model Size Matters
- **2-3B:** +3.7% to +8.9% improvement
- **4B:** +8% to +14% improvement
- **7-8B:** +16.4% to +23.5% improvement
- **Conclusion:** Larger models generate better expansions, but 4B offers best cost-benefit

### 2. Generational Improvement
- **Qwen3-4B vs Qwen 2.5-3B:** +4.7% NDCG@10 at similar size
- **Qwen3-8B vs Qwen 2.5-7B:** +2.5% NDCG@10
- **Conclusion:** Newer model generations improve QE quality

### 3. Arabic Specialization ≠ QE Quality
- **OALL benchmarks** (Arabic language understanding) don't predict QE effectiveness
- **Aya 8B** (multilingual) outperforms **Jais-2** (Arabic-specialized) on Dense
- **Exception:** Jais-2 best for BM25 due to Arabic-specialized vocabulary
- **Conclusion:** Training data diversity matters more than Arabic-only focus

### 4. Dense vs BM25 Divergence
- **Dense:** 9/9 models improve (semantic expansion helps embeddings)
- **BM25:** Only 3/9 improve without repetition (term dilution hurts)
- **Fix:** Query repetition (n=5-7) recovers all models
- **Conclusion:** Retriever-specific strategies are essential

### 5. Corpus Grounding Works
- **Blind QE (Query2Doc):** +8.9% Dense, −11.5% BM25 (n=1)
- **Corpus-Steered (CSQE):** +33.2% BM25, +18.5% Dense
- **Advantage:** +5.2% over blind QE on BM25
- **Conclusion:** Showing LLM actual corpus vocabulary improves alignment

### 6. Asymmetric QE is Optimal
- **Config A (BM25+CSQE + Dense original):** 0.7137 NDCG@10 ← **BEST**
- **Config C (both enhanced):** 0.6959 NDCG@10 (−0.018)
- **Reason:** BM25 needs vocabulary expansion, Dense needs semantic purity
- **Conclusion:** Different retrievers benefit from different query representations

---

## Error Analysis Highlights

### Baseline Failure Patterns
- **39% failure rate** (NDCG@10 < 0.3)
- **Short query gap:** 59% of long query performance
- **Correlation:** r=0.125 (p<0.001) between length and performance
- **Retrieval vs ranking:** 84% Recall@100 but 50% NDCG@10

### CSQE Improvements
- **First-pass quality:** 88.8% queries have relevant docs (vs 66.8% blind)
- **Win/loss:** 1,896 wins, 1,000 losses vs baseline
- **Big wins:** +0.5 to +1.0 NDCG@10 on specific queries
- **Regressions:** 52% Type A (strong BM25 hurt), 36% Type B (poisoned first-pass)

---

## Technical Optimizations

### Speed Improvements
1. **Batch processing:** 8x speedup (8 queries in parallel)
2. **Token reduction:** 2x speedup (256→128 tokens)
3. **Inference optimization:** FP16, eval mode, no_grad
4. **Combined:** 16x faster (8 hours → 40 minutes)

### Engineering Solutions
1. **BM25S:** Pure Python, no Java dependencies
2. **GPU-accelerated mDPR:** Manual batch encoding, 5-7x speedup
3. **Two-notebook workflow:** Separate generation and evaluation
4. **Cross-query batching:** Efficient A100 utilization for CSQE

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| BM25 term dilution | Query repetition (n=5-7, MuGI β=2) |
| Slow LLM inference | Batch processing + token reduction (16x speedup) |
| ALLaM tokenizer bug | Dropped model, documented failure |
| GPT-OSS 70x slower | Dropped model, MoE impractical for batch QE |
| MIRACL no metadata | Used docid structure (X#Y) for article grouping |
| Dense+CSQE degradation | Asymmetric QE (only to BM25) |

---

## Recommendations for Future Work

### High Priority
1. **Stronger embedding models** (BGE-M3, mE5-large)
2. **Dialectal Arabic** evaluation
3. **Reranking integration** (cross-encoder)

### Medium Priority
4. **Few-shot prompting** comparison
5. **HyDE vs Query2Doc** head-to-head
6. **Multi-stage QE** / iterative refinement

### Low Priority
7. **Production optimization** (distillation, quantization)
8. **Publication** (EACL/ACL/NAACL)

---

## Defense Preparation

### Expected Questions & Answers

**Q: Why small models instead of GPT-4?**  
A: (1) Resource constraints (free Colab), (2) Open-source reproducibility, (3) Proved 3B zero-shot can beat 175B few-shot, (4) Practical for deployment

**Q: Why did BM25 degrade initially?**  
A: Term dilution — adding 128 tokens of expansion without repetition dilutes original query terms' TF-IDF weights. Fixed with n=5-7 repetition.

**Q: What's novel about CSQE for Arabic?**  
A: (1) First application to MIRACL Arabic, (2) First comparison of blind vs corpus-aware for Arabic, (3) Discovered asymmetric QE principle, (4) Validated "mufti analogy"

**Q: Why not use GPT-4 or Claude?**  
A: (1) Cost ($0.50-$1.50 per 1K queries), (2) API rate limits, (3) Not reproducible, (4) Proved open-source models sufficient

**Q: How does this compare to MIRACL paper results?**  
A: MIRACL best hybrid (BM25+mDPR, α=0.5) = 0.673 NDCG@10. Our system (CSQE+Hybrid) = 0.7137 (+6.0% improvement).

**Q: What's the practical deployment cost?**  
A: ~$0 for research (free Colab). Production: ~$0.01-0.05 per 1K queries (Groq/Together API) or self-hosted GPU (~$1/hour A100).

**Q: Why Aya 8B instead of Jais-2?**  
A: Aya best overall Dense (+23.5%), Jais-2 best BM25 (+10.8%). For hybrid system, Aya's Dense advantage outweighs Jais-2's BM25 advantage.

**Q: Can this work for other languages?**  
A: Yes — CSQE is language-agnostic. MIRACL has 18 languages. Our approach should transfer with language-appropriate LLMs.

---

## File Locations (Quick Access)

### Thesis
- `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter*.tex`
- `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/README_chapter*.md`

### Key Experiments
- `arabic-rag-query-enhancement/docs/experiments/exp_001_baseline_dense.md`
- `arabic-rag-query-enhancement/docs/experiments/exp_013_csqe_aya_8b.md`
- `arabic-rag-query-enhancement/docs/experiments/exp_021_csqe_hybrid_fusion.md`

### Research Decisions
- `research_decisions/phase4_literature_review.md` (50+ papers)
- `research_decisions/mufti_approach_deep_research.md` (CSQE research)
- `research_decisions/llm_model_research.md` (10 models)

### Code
- `src/enhancers/query2doc.py` (Query2Doc implementation)
- `src/retrievers/dense.py` (mDPR retriever)
- `src/retrievers/bm25.py` (BM25S retriever)

### Notebooks
- `experiments/exp_013_csqe_aya_8b.ipynb` (CSQE)
- `experiments/phase4_quick_wins (1).ipynb` (Exp 011, 012, 021)

---

## Citation Information

**Title:** Query Enhancement for Arabic Retrieval-Augmented Generation Using Small Open-Source Language Models

**Authors:** Mohammed Elhaj, Osman Bashir

**Institution:** University of Khartoum, Faculty of Engineering

**Year:** 2026

**Dataset:** MIRACL Arabic (Zhang et al., 2023)

**Key Techniques:** Query2Doc (Wang et al., 2023), CSQE (Lei et al., 2024)

---

## Contact Information

**Mohammed Elhaj:** [email]  
**Osman Bashir:** [email]  
**Supervisor:** Dr. Tahani [title]  
**Institution:** University of Khartoum, Faculty of Engineering

---

**Document Created:** May 9, 2026  
**Purpose:** Quick reference for presentations, defense, and future work  
**Status:** Complete and ready for use
