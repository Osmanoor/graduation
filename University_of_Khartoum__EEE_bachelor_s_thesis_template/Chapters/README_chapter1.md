# Chapter 1: Introduction — Tracking Document

**Created:** 2026-03-27
**Last Updated:** 2026-03-27
**Status:** First complete draft
**File:** `Chapters/chapter1.tex`

---

## Final Outline

### Chapter Introduction (no section number)
Four paragraphs introducing the topic area, narrowing from digital Arabic content → RAG → Arabic retrieval challenges → query enhancement → the gap in existing research. No references.

### 1.1 Problem Definition
Three interlocking gaps framing the research problem.

| Gap | Content |
|-----|---------|
| The retrieval gap | Arabic IR exhibits high failure rates; short queries disproportionately affected by information poverty |
| The language gap | QE techniques developed for English; transferability to Arabic unverified |
| The resource gap | Existing QE relies on 175B+ proprietary models; viability of small open-source models unknown |
| Research question | "To what extent can small, open-source LLMs improve Arabic information retrieval through query enhancement, and what model characteristics determine effectiveness?" |

### 1.2 Objectives
Five objectives, each mapping to a Chapter 3 methodology section.

| # | Objective | Maps to |
|---|-----------|---------|
| 1 | Establish dense (mDPR) and sparse (BM25S) baselines, tested independently | Ch.3 §3.2 |
| 2 | Conduct systematic error analysis to identify failure patterns and guide technique selection | Ch.3 §3.3 |
| 3 | Adapt Query2Doc for Arabic zero-shot application with small open-source LLMs + engineering optimisations | Ch.3 §3.4 |
| 4 | Evaluate 10 open-source LLMs (2–8B) across both retrieval paradigms using standardised protocol | Ch.3 §3.5 |
| 5 | Analyse interaction between QE and retrieval paradigm; identify model characteristics predicting effectiveness | Ch.3 §3.5 + Ch.4 §4.5 |

### 1.3 Thesis Layout
One paragraph per chapter (Chapters 1–5), describing scope and content.

---

## How to Update This Chapter

### After Expanded Experiments (Phase 4)
1. If new objectives are added (e.g., chunking-aware QE), add to Section 1.2
2. Update Section 1.3 thesis layout if new chapter sections are added
3. Do NOT add results or methodology details — those belong in Ch.3/4
4. Preamble may need minor updates if new techniques are introduced

### After Thesis Review
- Check that objectives still match Chapter 3 methodology exactly
- Ensure thesis layout descriptions match actual chapter content
- Dr. Tahani's rule: "You cannot write objectives and then have done something different in the methodology"

---

## Cross-Reference Labels

| Label | Section | Usage |
|-------|---------|-------|
| `chap:introduction` | Chapter 1 | "As stated in Chapter~\ref{chap:introduction}" |
| `sec:problem_definition` | 1.1 | Problem definition |
| `sec:objectives` | 1.2 | Objectives |
| `sec:thesis_layout` | 1.3 | Thesis layout |

---

## Formatting Rules
- **Passive voice** throughout
- **No references** — Chapter 1 is your own framing (per Dr. Tahani)
- **No methodology details** — objectives state what was done, not how
- **No results** — no numbers, no findings
- **Abbreviations**: Full form (ABBR) on first use, then ABBR only
- Objectives use numbered list with `enumerate`
