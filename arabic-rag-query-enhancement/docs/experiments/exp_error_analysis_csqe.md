# Error Analysis: CSQE+Hybrid (Config A RRF) vs Aya Blind QE

**Date:** April 11, 2026
**Owner:** Mohammed Elhaj
**Status:** ✅ Complete
**Notebook:** `docs/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb` (Section 12 + 14)
**Compares:** Config A RRF (0.7137 nDCG@10) vs Aya Blind BM25 n=1 (0.5046 nDCG@10)

---

## Setup

| Item | Value |
|------|-------|
| Dataset | MIRACL Arabic dev (2,896 queries) |
| System A | Config A RRF: BM25+CSQE (Aya 8B) + Dense original, k=20 |
| System B | Aya Blind BM25: blind Query2Doc n=1, BM25 only |
| Per-query metric | nDCG@10 (pytrec_eval) |
| Failure threshold | Config A nDCG@10 < 0.1 |
| Big-win threshold | CSQE − blind > 0.3 |
| Regression threshold | blind − CSQE > 0.1 |

---

## Per-Query Score Distribution

| Condition | Queries | % |
|-----------|---------|---|
| CSQE > blind | 1,646 | 56.8% |
| CSQE = blind (tie) | 770 | 26.6% |
| CSQE < blind | 480 | 16.6% |
| **Mean CSQE − blind delta** | **+0.1890** | |

| Category | Count | Description |
|----------|-------|-------------|
| Failures (Config A < 0.1) | 258 | nDCG@10 < 0.1 for Config A |
| Big wins (Δ > 0.3) | 1,061 | CSQE outperforms blind by >0.3 |
| Regressions (Δ < −0.1) | 367 | Blind outperforms CSQE by >0.1 |

---

## Quantitative Pattern Analysis

| Category | n | Aya Blind BM25 | CSQE+Hybrid | Δ |
|----------|---|----------------|-------------|---|
| **All queries** | 2,896 | 0.5046 | 0.6936 | **+0.1890** |
| Short queries (< 5 words) | 865 | 0.4793 | 0.6783 | +0.1990 |
| Long queries (≥ 10 words) | 131 | 0.6003 | 0.7056 | +0.1053 |
| **1st-pass IS relevant** | **1,061** | **0.6684** | **0.8877** | **+0.2193** |
| **1st-pass NOT relevant** | **1,835** | **0.4100** | **0.5814** | **+0.1714** |

*Note: "Long corpus expansion (>200 chars)" = 2,896 (all queries) — the LLM always generates at least one paragraph regardless of first-pass quality. "Short corpus expansion (<50 chars)" = 0.*

---

## Failure Analysis (258 queries, Config A nDCG@10 < 0.1)

> ⚠️ **CORRECTION (2026-05-31, Workstream 1 Task 1.1).** The "irretrievable" claim
> below is **FALSE** and is retained only for the record. A direct corpus-membership
> check (`thesis_figures/notebooks/task_1_1_corpus_integrity.py`; verdict CSV at
> `thesis_figures/data/computed/task_1_1_failure_corpus_check.csv`) found that **all
> 258 failure queries have ≥1 relevant qrel document present in the indexed corpus**
> (corpus = 2,061,414 docs = canonical MIRACL Arabic size). **0 are irretrievable;
> 258 are genuine retrieval failures.** Of the 258: 199 also score 0 on the BM25
> baseline (present but un-retrieved by every method), and **58 have BM25 baseline
> ≥ 0.1 (43 ≥ 0.3) — BM25 alone ranked the doc in the top 10 but the CSQE hybrid lost
> it** (genuine regressions). qid 1060 is one of those 58, not a unique case. The
> original claim inferred "all methods score 0 ⇒ doc absent" without a membership
> check; that inference does not hold. §4.10 must be reframed accordingly (Task 1.3):
> these are NOT a dataset ceiling. No reindex needed — the corpus is complete.

**[SUPERSEDED] 257/258 failures are universally irretrievable** — CSQE, blind QE, and BM25 baseline all score 0.000. These are MIRACL queries whose positive passage is not present in the Wikipedia corpus dump used for indexing (a known dataset limitation). They are not CSQE failures.

**[SUPERSEDED] 1 genuine CSQE failure** (qid=1060, "ما هو أكبر القصور الموجودة في العراق؟"):
- BM25 baseline = 0.387, blind QE = 0.387, but Config A RRF = 0.000
- The corpus expansion was a meta-description rather than vocabulary-rich content, causing the CSQE BM25 run to push the relevant document below rank 10 in RRF fusion.

**[SUPERSEDED] Conclusion:** 258 "failures" are a ~8.9% ceiling imposed by the dataset, not a system limitation.

---

## Big Win Analysis (1,061 queries, CSQE − blind > 0.3)

**Pattern: all 1,061 have CSQE = 1.000, blind = 0.000.**

The blind LLM hallucinates a plausible but wrong entity; CSQE's first-pass corpus doc anchors the expansion to the correct Wikipedia article.

**Representative examples:**

| QID | Query | Blind QE says | Corpus grounds to | CSQE |
|-----|-------|--------------|------------------|------|
| 10061 | ما هو الرباط المنصوري؟ | A spinal surgery procedure | Mamluk-era building in Cairo | 1.000 |
| 10081 | ما هي الفيتوكيميكال؟ | General plant chemistry | Actual فيتوكيميكال Wikipedia list | 1.000 |
| 10320 | من هو مؤسس الفلسفة البراغماتية؟ | (hallucinated person) | John Dewey article | 1.000 |
| 11213 | من هو نيكولا بوالو؟ | A French businessman | 17th-century French poet article | 1.000 |

**The "mufti hypothesis" validated:** for niche or ambiguous Arabic terms, blind QE confidently hallucinates a common/modern interpretation while corpus grounding locks onto the actual Wikipedia entity.

---

## Regression Analysis (367 queries, blind − CSQE > 0.1)

### Root Cause Breakdown

| Type | Count | % | Description |
|------|-------|---|-------------|
| **A: Strong BM25 hurt** | **191** | **52%** | BM25 baseline ≥ 0.3; CSQE vocabulary injection introduces noise that pushes relevant doc below rank 10 |
| **B: Poisoned first-pass** | **131** | **36%** | BM25 baseline < 0.1; first-pass retrieves irrelevant docs → corpus expansion grounded on wrong content |
| **C: Partial BM25** | **45** | **12%** | BM25 baseline 0.1–0.3; mixed retrieval quality |

### Type A examples — CSQE hurts well-handled queries

| QID | Query | BM25 | Blind | CSQE |
|-----|-------|------|-------|------|
| 84 | كم يوم يصوم المسلمون في رمضان؟ | 0.000 | 1.000 | 0.000 |
| 928 | ماهو التطرف؟ | 0.000 | 1.000 | 0.000 |
| 3164 | ما هي نظرية الانفجار العظيم؟ | 0.000 | 1.000 | 0.264 |

### Type B examples — First-pass poisoning

| QID | Query | Top doc retrieved | Blind | CSQE |
|-----|-------|------------------|-------|------|
| 928 | ماهو التطرف؟ | لهجة جنوبية (ماهو = dialect phrase) | 1.000 | 0.000 |
| 11739 | من هو مصمم موقع ويكيبيديا؟ | حظر ويكيبيديا في تركيا (Turkey ban article) | 1.000 | 0.000 |
| 3702 | هل يمكن توليد الطاقة بالكهرباء الساكنة؟ | توليد الكهرباء (general, not static) | 1.000 | 0.000 |

**Root cause of Type B:** BM25 first-pass is susceptible to Arabic homonyms and short/ambiguous queries. When the top-k docs are off-topic, the LLM grounding is poisoned regardless of generation quality.

---

## Corpus Expansion Quality (Meta-Description Detection)

The Aya 8B model sometimes generates preamble text ("بناءً على استعراض الوثائق...") that describes the retrieval task rather than extracting corpus-grounded content.

| Group | n | Aya Blind nDCG@10 | CSQE+Hybrid nDCG@10 | Δ |
|-------|---|------------------|---------------------|---|
| All queries | 2,896 | 0.5046 | 0.6936 | +0.1890 |
| Clean expansion | ~17 | 0.6462 | 0.6688 | +0.0226 |
| Meta-desc expansion | ~2,879 | 0.5038 | 0.6938 | +0.1900 |

**Key finding: Meta-descriptions do not hurt performance.** Despite the LLM prepending a description of its retrieval process, the RRF fusion extracts value from the expansion (the meta-description itself contains the original Arabic query terms multiple times, providing partial vocabulary signal). CSQE+Hybrid performance is nearly identical for meta-desc and clean queries (0.6938 vs 0.6688 — meta-desc is actually *marginally higher* because those 2,879 queries are representative of the full distribution).

---

## Key Findings for Thesis

### Finding 1 — First-pass quality is the dominant predictor
When BM25 first-pass retrieves a relevant document (1,061 queries, 36.6% of dev set), CSQE+Hybrid achieves **0.8877 nDCG@10** — near-ceiling retrieval. When first-pass fails (1,835 queries), it achieves 0.5814. The first-pass recall gap (+0.3063 nDCG@10) is larger than the overall system gap over blind QE (+0.1890).

### Finding 2 — Short queries benefit most from CSQE
Short queries (< 5 words, n=865) gain **+0.1990** vs +0.1053 for long queries (≥10 words). Short queries are most underspecified and benefit most from both vocabulary expansion and corpus grounding.

### Finding 3 — Two distinct failure modes
- **Type B (36%):** First-pass poisoning from BM25 homonym sensitivity. Fix: add a first-pass quality gate (check if top-1 doc text overlaps with the query's likely topic before grounding).
- **Type A (52%):** Strong-query degradation where CSQE expansion introduces off-topic Arabic terms. Fix: weight original query more heavily in the final expanded string (higher α, or use expansion as a separate BM25 field).

### Finding 4 — Meta-descriptions are harmless noise
The LLM wraps content in conversational Arabic framing 99.4% of the time. RRF fusion is completely resilient to this — the pattern does not need to be fixed.

---

## Implications for Future Work

1. **First-pass quality gate:** If the top-1 BM25 first-pass document has low overlap with the query (cosine similarity of BM25 doc embedding vs query < threshold), fall back to blind QE. Expected gain: recover ~131 Type B regressions.

2. **Asymmetric query weighting:** For Type A queries (BM25 already strong), a smaller expansion weight (lower α, or mixing original query separately) could prevent vocabulary dilution. Field-based indexing (original query in one field, expansion in another with lower boost) is a natural BM25-native solution.

3. **CSQE with larger k first-pass:** Current k=5. Increasing to k=10 gives the LLM more diversity in corpus grounding, potentially reducing the homonym/poisoning failure rate.

4. **Jais-2-8B for CSQE:** Jais-2-8B achieved 0.6018 in blind Dense retrieval — the best among tested models. Its stronger Arabic understanding may produce better corpus extraction and fewer meta-descriptions.

---

## Artifacts

| File | Description |
|------|-------------|
| `docs/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb` | Full evaluation notebook (Sections 12+14) |
| `results/exp_11_ablations/error_analysis_patterns.csv` | Quantitative pattern table |
| `results/exp_11_ablations/scatter_csqe_vs_blind.png` | Per-query win/loss scatter |
| `results/exp_11_ablations/meta_desc_analysis.png` | Expansion quality bar chart |
| `results/exp_11_ablations/regression_causes.png` | Regression root-cause pie chart |
