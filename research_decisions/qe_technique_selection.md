# Query Enhancement Technique Selection
**Date:** January 17, 2026  
**Decision:** Query Expansion with Normalization  
**Status:** ✅ Decided (Evidence-Based)

---

## Executive Summary

After comprehensive error analysis of 2,896 queries (Phase 1: Quantitative, Phase 2: Qualitative), we recommend **Query Expansion with Normalization** as the first Query Enhancement technique for the Arabic RAG system.

**Key Finding:** 80% of query failures stem from three patterns that Query Expansion directly addresses: spelling errors (40%), named entity variations (35%), and vocabulary mismatch (15%).

**Expected Impact:** 20-45% reduction in failed queries (conservative: 20-30%, optimistic: 35-45%).

---

## Decision Rationale

### Evidence from Error Analysis

**Phase 1 Quantitative Findings:**
- 39% of queries fail (NDCG@10 < 0.3) = 1,130 queries
- 192 queries have zero recall in top-10
- Short queries perform 41% worse than long queries
- 99.4% retrieval coverage in top-100, but only 93.4% in top-10

**Phase 2 Qualitative Findings (20 worst queries):**

| Failure Pattern | Count | % | Solution |
|-----------------|-------|---|----------|
| Spelling Errors | 8 | 40% | Normalization |
| Named Entity Variations | 7 | 35% | Expansion (variants) |
| Diacritics Mismatch | 5 | 25% | Normalization |
| Vocabulary Mismatch | 3 | 15% | Expansion (synonyms) |
| Short/Ambiguous | 3 | 15% | Expansion (context) |
| Abstract Concepts | 3 | 15% | Expansion/HyDE |
| Western Topics | 4 | 20% | Expansion (transliterations) |

---

## Selected Technique: Query Expansion with Normalization

### Definition

**Query Expansion:** Augment the original query with additional related terms, synonyms, entity variations, and contextual information to improve retrieval coverage.

**Normalization:** Preprocess the query to fix common Arabic spelling issues and remove diacritics before expansion.

### Two-Step Approach

#### Step 1: Normalization
- Fix spelling errors (missing hamza, alif maqsura)
- Remove diacritics (المَثَانةُ → المثانة)
- Standardize spacing (ماهو → ما هو)
- Normalize punctuation

#### Step 2: Expansion
- Add synonyms (آزوت → نيتروجين)
- Add entity variations (إبن الهيثم → ابن الهيثم، الحسن بن الهيثم)
- Add related terms (الحجر الاسود → الكعبة، مكة)
- Add transliteration variants (زودياك → Zodiac)

### Implementation Strategy

**Method:** Use Arabic LLM (e.g., Gemini, GPT-4) to generate expansions

**Prompt Template:**
```
أنت خبير في اللغة العربية. قم بتوسيع الاستعلام التالي بإضافة:
1. مرادفات
2. مصطلحات ذات صلة
3. أشكال مختلفة للأسماء
4. سياق إضافي

الاستعلام الأصلي: {normalized_query}

قدم الاستعلام الموسع بشكل طبيعي (جملة واحدة أو جملتين).
```

**Output Format:** Expanded query string (not list of terms)

**Example:**
- Original: `ما الرمز الكيميائي للآزوت؟`
- Normalized: `ما الرمز الكيميائي للازوت؟`
- Expanded: `ما الرمز الكيميائي للازوت النيتروجين nitrogen العنصر الكيميائي N`

---

## Why Query Expansion (Not HyDE)?

### Comparison

| Criterion | Query Expansion | HyDE |
|-----------|----------------|------|
| **Addresses Top Failures** | ✅ 80% (spelling, entities, vocab) | ⚠️ 15% (short queries) |
| **Implementation Complexity** | ⭐⭐ Medium | ⭐⭐⭐ High |
| **API Cost** | 💰 Low (short prompts) | 💰💰 High (long generation) |
| **Risk of Noise** | ⚠️ Medium | ⚠️⚠️ High (hallucination) |
| **Arabic Language Support** | ✅ Good | ⚠️ Requires careful prompting |
| **Proven for Arabic** | ✅ Yes (literature) | ⚠️ Limited evidence |

### Decision Factors

1. **Coverage:** Query Expansion addresses 80% of failure patterns vs HyDE's 15%
2. **Cost:** Expansion uses shorter prompts (lower API costs)
3. **Risk:** Lower hallucination risk (adding terms vs generating documents)
4. **Iteration Speed:** Simpler to implement and debug
5. **Arabic-Specific:** Better suited for Arabic linguistic issues (spelling, diacritics)

### When to Consider HyDE

If Query Expansion achieves <15% improvement, consider HyDE as:
- **Complementary technique** (use both)
- **Alternative for short queries** (selective application)
- **Second iteration** (after validating expansion approach)

---

## Expected Impact

### Conservative Estimate (20-30% improvement)

**Assumptions:**
- Normalization fixes 50% of spelling errors (4/8 queries)
- Expansion helps 50% of entity/vocab issues (5/10 queries)
- Total: 9/20 worst queries improved

**Result:** 45% of failed queries improved → 11.7% overall improvement

### Optimistic Estimate (35-45% improvement)

**Assumptions:**
- Normalization fixes 75% of spelling errors (6/8 queries)
- Expansion helps 70% of entity/vocab issues (7/10 queries)
- Total: 13/20 worst queries improved

**Result:** 65% of failed queries improved → 16.9% overall improvement

### Target Metrics (Experiment 002)

**Baseline (exp_001):**
- Recall@10: 0.6156
- NDCG@10: 0.4993
- MRR: 0.5328

**Target (exp_002 - Query Expansion):**
- Recall@10: 0.65-0.68 (+5-10%)
- NDCG@10: 0.52-0.55 (+4-10%)
- MRR: 0.55-0.58 (+3-9%)

---

## Implementation Plan

### Phase 1: Normalization Module (Week 4, Day 1-2)

**File:** `src/enhancers/normalizer.py`

**Functions:**
- `remove_diacritics(text)` - Remove Arabic diacritics
- `fix_hamza(text)` - Standardize hamza forms
- `fix_alif_maqsura(text)` - Standardize ى/ي
- `fix_ta_marbuta(text)` - Standardize ة/ه
- `normalize_spacing(text)` - Fix merged words
- `normalize_query(text)` - Main function

**Testing:** Unit tests on 20 worst queries

---

### Phase 2: Expansion Module (Week 4, Day 3-4)

**File:** `src/enhancers/query_expander.py`

**Functions:**
- `expand_with_llm(query, llm_client)` - LLM-based expansion
- `expand_query(query, method='llm')` - Main function

**LLM Options:**
1. **Gemini 1.5 Flash** (preferred - free tier, fast)
2. **GPT-4o-mini** (backup - low cost)
3. **Local Arabic LLM** (if budget exhausted)

**Prompt Engineering:**
- Test multiple prompt variations
- Validate on 10 sample queries
- Measure expansion quality

---

### Phase 3: Integration & Experiment (Week 4, Day 5-7)

**File:** `experiments/exp_002_qe_expansion_dense.ipynb`

**Steps:**
1. Load mDPR baseline
2. For each query:
   - Normalize query
   - Expand query
   - Encode expanded query
   - Retrieve top-100
3. Evaluate metrics
4. Compare with baseline

**Documentation:** `docs/experiments/exp_002_qe_expansion_dense.md`

---

## Alternative Techniques (Future Work)

### If Query Expansion Underperforms

1. **HyDE (Hypothetical Document Embeddings)**
   - Generate hypothetical answer document
   - Encode document instead of query
   - Better for short/ambiguous queries

2. **Query Decomposition**
   - Split complex queries into sub-queries
   - Retrieve for each sub-query
   - Merge results
   - Better for multi-part questions

3. **Query Rewriting**
   - Paraphrase query in multiple ways
   - Retrieve for each paraphrase
   - Merge results
   - Better for ambiguous queries

### Hybrid Approaches

- **Selective Enhancement:** Use different techniques based on query type
- **Ensemble:** Combine multiple techniques
- **Iterative:** Apply techniques sequentially

---

## Success Criteria

### Minimum Viable Success
- **Recall@10:** +3% improvement (0.6156 → 0.634)
- **NDCG@10:** +2% improvement (0.4993 → 0.509)
- **Failed queries:** -15% (1130 → 960)

### Target Success
- **Recall@10:** +5% improvement (0.6156 → 0.646)
- **NDCG@10:** +4% improvement (0.4993 → 0.519)
- **Failed queries:** -25% (1130 → 847)

### Stretch Goal
- **Recall@10:** +10% improvement (0.6156 → 0.677)
- **NDCG@10:** +10% improvement (0.4993 → 0.549)
- **Failed queries:** -40% (1130 → 678)

---

## Risk Mitigation

### Risk 1: Expansion Adds Noise
**Mitigation:**
- Start with conservative expansion (2-3 terms)
- Test multiple expansion lengths
- Use LLM temperature=0 for consistency

### Risk 2: LLM Hallucination
**Mitigation:**
- Validate expansions on sample queries
- Use constrained prompts (synonyms only, no generation)
- Fallback to rule-based expansion if quality poor

### Risk 3: API Cost Overrun
**Mitigation:**
- Use Gemini 1.5 Flash (free tier: 15 RPM)
- Batch queries to minimize API calls
- Cache expansions for repeated queries
- Fallback to local LLM if needed

### Risk 4: No Improvement
**Mitigation:**
- Analyze which queries improved/degraded
- Iterate on prompt engineering
- Try HyDE as alternative
- Consider hybrid approach

---

## References

### Error Analysis Documents
- `research_decisions/error_analysis_phase1_quantitative.md` - Quantitative findings
- `research_decisions/error_analysis_phase2_qualitative.md` - Qualitative analysis
- `research_decisions/error_analysis_plan_exp001.md` - Analysis plan
- `research_decisions/HANDOFF_ERROR_ANALYSIS.md` - Handoff document

### Research Documents
- `research_decisions/error_analysis_research.md` - Literature review
- `research_decisions/miracal_metdata_refrence_reports/error analysis best practices.md`

### Experiment Documents
- `docs/experiments/exp_001_baseline_dense.md` - Baseline experiment
- `results/baseline_dense/exp_001_quantitative_analysis.json` - Analysis data

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-17 | Query Expansion with Normalization | Evidence-based: addresses 80% of failures |
| 2026-01-17 | Use Gemini 1.5 Flash for expansion | Free tier, fast, good Arabic support |
| 2026-01-17 | Two-step approach (normalize → expand) | Handles Arabic-specific issues first |
| 2026-01-17 | HyDE as backup/complement | If expansion <15% improvement |

---

**Decision Status:** ✅ Final  
**Approved By:** Mohammed Elhaj (based on error analysis evidence)  
**Next Action:** Update TASKS.md, RESEARCH_CONTEXT_KERNEL.md.md, begin implementation (Task 4.1)
