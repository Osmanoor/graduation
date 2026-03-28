# Chapter 5: Conclusion and Recommendations — Tracking Document

**Created:** 2026-03-27
**Last Updated:** 2026-03-27
**Status:** First complete draft
**File:** `Chapters/chapter5.tex`

---

## Final Outline

### Chapter Introduction (no section number)
Brief paragraph introducing the chapter scope: conclusions, challenges, and recommendations.

### 5.1 Conclusions
Summary of proven findings, structured as a progression.

| Topic | Content |
|-------|---------|
| Baseline & error analysis | Complementary dense/sparse strengths; 39% failure rate; short query gap validated QE approach |
| Query2Doc for Arabic | Zero-shot 3B model (+8.9%) exceeded original paper's 175B few-shot English results (+2–5%) |
| Model comparison | 9/9 improved dense (+3.7% to +23.5%); Aya best overall; Jais-2 best BM25; Qwen3-4B best constrained |
| Analytical findings | Size correlates with performance; Arabic benchmarks ≠ QE quality; training data diversity matters more |
| Dense vs BM25 divergence | 9/9 improve dense, 6/9 degrade BM25 (term dilution); retriever-specific strategies needed |
| Overall | QE via Query2Doc is effective, modular, resource-efficient for Arabic RAG |

### 5.2 Challenges
Six challenges encountered during the research.

| # | Challenge | Details |
|---|-----------|---------|
| 1 | Resource constraints | Colab T4/A100, 8B max, engineering optimisations needed |
| 2 | BM25 term dilution | 6/9 models degrade BM25; query repetition (n=5) not implemented |
| 3 | Dropped models | ALLaM tokenizer bug (-48.9%); GPT-OSS 70x slower + hallucinations |
| 4 | Dataset scope | MSA-only (MIRACL); dialectal Arabic untested |
| 5 | Single QE technique | Only Query2Doc; HyDE, GRF, rewriting not compared |
| 6 | Baseline retriever strength | mDPR intentionally weak; improvement magnitude may differ with stronger models |

### 5.3 Recommendations for Future Work
Eight recommendations, ordered from direct extensions to broader directions.

| # | Recommendation | Phase 4 Link |
|---|---------------|-------------|
| 1 | Knowledge-base-aware / chunking-aware QE | Task 6.1–6.3 |
| 2 | BM25 query repetition + retriever-specific strategies | Addresses main BM25 limitation |
| 3 | Stronger embedding models (BGE-M3, mE5-large) | Task 6.3 variant |
| 4 | Hybrid retrieval (RRF) with QE | Task 6.2 candidate |
| 5 | Dialectal Arabic evaluation | Future direction (beyond MIRACL) |
| 6 | Few-shot and chain-of-thought prompting | Task 6.2 candidate |
| 7 | Multi-stage QE / iterative refinement | Task 6.2 candidate |
| 8 | Publication and reproducibility | Task 6.5 |

---

## How to Update This Chapter

### After Expanded Experiments (Phase 4)
1. **Section 5.1:** Add new conclusions from expanded experiments (e.g., "Chunking-aware QE further improved..." or "Stronger embedding models showed...")
2. **Section 5.2:** Update challenges if new ones were encountered; mark resolved challenges
3. **Section 5.3:** Move implemented recommendations from "future work" to "completed" in Section 5.1. Add new recommendations discovered during expanded experiments
4. If a recommendation was implemented (e.g., chunking-aware QE), rewrite it as a conclusion instead

### After Full Thesis Review
- Ensure Section 5.1 conclusions match actual Chapter 4 findings
- Ensure no conclusion is stated that isn't supported by experimental evidence
- Verify that recommendations don't repeat challenges — challenges = what we faced; recommendations = what should be done next

---

## Cross-Reference Labels

| Label | Section | Usage |
|-------|---------|-------|
| `chap:conclusion` | Chapter 5 | "As discussed in Chapter~\ref{chap:conclusion}" |
| `sec:conclusions` | 5.1 | Conclusions |
| `sec:challenges` | 5.2 | Challenges |
| `sec:recommendations` | 5.3 | Recommendations for future work |

---

## Formatting Rules
- **Passive voice** throughout
- **No new data or figures** — Chapter 5 only summarises/synthesises from Ch.4
- **No re-explanation** of methodology — reference Chapter 3 if needed
- **Recommendations** are forward-looking and actionable (Dr. Tahani: "You are the domain experts")
- **Challenges** are factual and specific — not excuses, but honest limitations
- Numbered lists for challenges and recommendations (using `enumerate`)
