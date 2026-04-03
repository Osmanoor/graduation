# Phase 4 Experiment Plan: Expanding Arabic Query2Doc

**Date:** 2026-04-03 (updated from 2026-03-28 draft)
**Status:** Plan Finalized — Ready for Implementation
**Task:** 6.2 Complete → 6.3a/b/c next
**Decided by:** Mohammed + Claude Code research session

**Lean Critical Path (finalized 3 April 2026):**
Directions 1 & 2 are NOT full prerequisites for Direction 3. The minimal path is:
1. **Phase A (2 days):** BM25 repetition fix (Exp 1.1) + Hybrid baseline (Exp 1.2) — these numbers are needed in the final thesis table regardless
2. **Phase B-Research (3-5 days):** Deep-dive research into corpus-steered / chunking-aware QE — finalize the exact approach, prompt design, and context extraction strategy BEFORE coding
3. **Phase B-Implement (1-1.5 weeks):** Corpus-Steered Query2Doc (Direction 3) — the main contribution
4. **Phase C (3-5 days):** Combine Direction 3 with hybrid fusion + run remaining quick wins (HyDE, prompt variants) as supporting experiments
5. The ablation study happens ONCE, inside Phase B-Implement — not duplicated.

Experiments 1.3, 1.4, 2.2, 2.3 are optional supporting experiments that strengthen the thesis but are not prerequisites for the core contribution.

**Important:** The breadth-first literature review (Task 6.1) is done — we mapped 50+ papers across all directions. But Direction 3 (Corpus-Steered QE) requires focused depth research before implementation. See "Direction 3 — Research Phase" below for what still needs investigation.

---

## Overview

This plan outlines three experiment directions that build on our existing Query2Doc pipeline. Based on a comprehensive literature review of 50+ papers across 5 research areas.

### Current Results (Baseline Reference)

| Method | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| mDPR baseline | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| BM25 baseline | 0.4621 | 0.5622 | 0.8577 | 0.4862 |
| Best QE: Aya (Dense) | 0.6166 | 0.7231 | 0.9001 | 0.6490 |
| Best QE: Aya (BM25) | 0.5047 | 0.6107 | 0.8734 | 0.5279 |
| **MIRACL hybrid baseline (no QE)** | **0.673** | **—** | **0.941** | **���** |

**Critical finding (verified):** The MIRACL paper (Table 2) reports BM25+mDPR hybrid = 0.673 nDCG@10 for Arabic using simple convex combination (alpha=0.5, untuned). This exceeds our best QE result by +9%. Our hybrid will be slightly lower (~0.63-0.66) because our BM25S implementation is ~4% weaker than Pyserini BM25.

---

## Direction 1: Quick Wins (Est. 5-7 days)

*Goal: Complete the empirical story for current pipeline, fix known weaknesses*

### Experiment 1.1: Fix BM25 with Query Repetition

**What:** Modify BM25 evaluation to prepend original query n times: `expanded = query * n + pseudo_doc`

**Configurations:**
- Fixed repetition: n ∈ {1, 3, 5, 7, 10}
- Adaptive (MuGI formula): λ = floor(Σlen(pseudo_docs) / (len(query) · β)), β ∈ {2, 4, 6}

**Models:** ALL 9 viable models (no new LLM inference — reuse existing pseudo-documents)

**Metrics:** nDCG@10, Recall@10, Recall@100, MRR

**Expected output:** Table "Effect of Query Repetition on BM25" — 9 models × repetition values. Should flip most of the 6 degraded models to positive.

**Key papers:** Query2Doc (Wang et al., EMNLP 2023), MuGI (Zhang et al., EMNLP 2024 Findings, arXiv:2401.06311)

**Effort:** 1 day | **Reuses:** All existing pseudo-documents, BM25S index | **New:** Modified concatenation function

---

### Experiment 1.2: Hybrid Baseline (BM25 + mDPR)

**What:** Compute hybrid scores: `s = α · s_BM25_norm + (1-α) · s_mDPR_norm` (min-max normalized)

**Configurations:** α ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}

**Models:** None (pure retriever fusion of existing baselines)

**Expected output:** Table "Hybrid BM25+mDPR Baseline" + α sensitivity figure. Expected nDCG@10 ~0.63-0.66.

**Key papers:** MIRACL (Zhang et al., TACL 2023), Bruch et al. (ACM TOIS 2023, arXiv:2210.11934)

**Effort:** 0.5 days | **Reuses:** All existing BM25/mDPR run files | **New:** Score normalization + fusion script

---

### Experiment 1.3: HyDE vs Query2Doc Comparison

**What:** Encode pseudo-documents alone through mDPR (HyDE-style), compare vs concatenating with query (Query2Doc-style)

**Models:** Top 3: Aya Expanse 8B, Jais-2-8B, Qwen3-4B

**Expected output:** Table "HyDE vs Query2Doc on MIRACL Arabic" — 3 models × 2 methods. **Novel: no Arabic comparison exists in literature.**

**Key papers:** HyDE (Gao et al., ACL 2023, arXiv:2212.10496)

**Effort:** 1 day | **Reuses:** Existing pseudo-documents, mDPR index | **New:** Script to encode pseudo-docs through mDPR encoder

---

### Experiment 1.4: Prompt Variant Comparison

**What:** Same model (Aya 8B), 4 prompt strategies:
- **A (current):** "Write a passage that answers this query" → pseudo-document
- **B (CoT-QE):** "Think step by step about key concepts and related terms" → reasoning chain
- **C (Keywords):** "List 10-15 Arabic keywords related to this query" → keyword list
- **D (Rewrite):** "Rewrite this query to be more specific for search" → rewritten query

**Configurations:** 4 prompts × 2 retrievers (mDPR + BM25 with optimal repetition from 1.1)

**Expected output:** Table "Effect of Prompt Strategy on Retrieval" — 4 prompts × 2 retrievers

**Key papers:** GRF (Mackie et al., SIGIR 2023, arXiv:2304.13157), CoT-QE (Jagerman et al., 2023, arXiv:2305.03653)

**Effort:** 2-3 days | **Reuses:** Aya model setup, evaluation pipeline | **New:** 3 new prompt templates, generation runs (~8,688 LLM calls)

---

### Direction 1 Dependencies

```
[Existing pseudo-documents]
 ├── [1.1 BM25 Fix]      ──┐
 ├── [1.2 Hybrid Baseline] ─┤── All 3 run in parallel
 └── [1.3 HyDE vs Q2D]   ──┘
                              │
                              ▼
                    [1.4 Prompt Variants]
                    (needs optimal n from 1.1)
```

---

## Direction 2: Hybrid + QE Fusion (Est. 4-6 days)

*Goal: Combine QE gains with hybrid retrieval for maximum performance*

**Prerequisite:** Direction 1 experiments 1.1 and 1.2

### Experiment 2.1: QE-Enhanced Hybrid (4-Way Fusion)

**What:** Fuse 4 ranked lists per query:
1. BM25(original) — already have
2. BM25(expanded with repetition) — from 1.1
3. mDPR(original) — already have
4. mDPR(expanded) — already have

**Fusion:** Convex combination with weight optimization on dev set. Also test RRF (k=60) for comparison.

**Models:** Aya Expanse 8B, Jais-2-8B

**Expected output:** Table "4-Way Fusion Results" showing progression from baseline → QE → hybrid → QE+hybrid. **This should be our best overall result.**

**Key papers:** Exp4Fuse (Liu et al., ACL 2025 Findings, arXiv:2506.04760)

**Effort:** 1-2 days | **Reuses:** ALL existing run files | **New:** 4-way fusion script with weight optimization

---

### Experiment 2.2: Retriever-Specific Prompts (LevelRAG-lite)

**What:** Different prompts for different retrievers:
- **BM25 prompt:** "List Arabic keywords, named entities, and specific terms related to: {query}"
- **Dense prompt:** Current Query2Doc pseudo-document prompt (already have results)

**Models:** Aya Expanse 8B

**Expected output:** Table "Retriever-Specific vs Generic QE" — generic vs tailored × fused. **Novel contribution.**

**Key papers:** LevelRAG (Zhang et al., 2025, arXiv:2502.18139)

**Effort:** 2-3 days | **Reuses:** Existing mDPR QE results | **New:** BM25-specific prompt, new generation run

---

### Experiment 2.3: Dual-List BM25 Fusion (Exp4Fuse-style)

**What:** For BM25 only: fuse BM25(original) and BM25(expanded) via RRF (k=60)

**Models:** All 9 models

**Expected output:** Table "Dual-List BM25 Fusion" — should eliminate ALL BM25 degradation

**Effort:** 1 day | **Reuses:** All existing BM25 runs | **New:** RRF fusion script

---

### Direction 2 Dependencies

```
[1.1 BM25 Fix] ───┬──→ [2.1 4-Way Fusion]
[1.2 Hybrid]   ───┘          │
                              │
[1.1 BM25 Fix] ──→ [2.3 Dual-List BM25]  (parallel with 2.1)
                              │
[2.1 results] ────→ [2.2 Retriever-Specific Prompts]
```

---

## Direction 3: Corpus-Steered Query2Doc — "The Mufti Approach" (Est. 12-15 days incl. research)

*Goal: The novel thesis contribution — grounding Query2Doc in corpus structure*

**Prerequisite:** Direction 1 baselines (1.1, 1.2) + Deep research phase below

---

### RESEARCH PHASE (Phase B-Research): Deep-Dive Before Implementation (3-5 days)

**Status:** NOT YET DONE — breadth-first mapping is complete but depth research is needed

**Why this matters:** Our breadth-first review (Task 6.1) identified corpus-steered QE as the most promising direction from 50+ papers. But we mapped many directions at a surface level. Before writing code, we need to go deep into the specific papers and techniques that directly inform our implementation. Otherwise we risk building something that misses key insights from the literature or duplicates existing work poorly.

**What still needs investigation:**

#### 1. Deep-dive into CSQE (Corpus-Steered Query Expansion)
- Read the FULL CSQE paper (Lei et al., EACL 2024, arXiv:2402.18031), not just the summary
- Understand exactly how they select "pivotal sentences" from retrieved documents
- What retriever did they use for the first pass? How many documents? What prompt format?
- Their results on different benchmarks — where does it work vs fail?
- Read their code (https://github.com/Yibin-Lei/CSQE) to understand implementation details
- **Key question:** How do they balance corpus-grounded content vs LLM-generated content?

#### 2. Deep-dive into chunking-aware / structure-aware retrieval
- Read DAPR (Wang et al., ACL 2024, arXiv:2305.13915) in full — the finding that 53.5% of retriever errors come from missing document context is central to our thesis argument
- How exactly does prepending document titles help? What's the quantitative effect?
- Heading-aware chunking (Pham et al., 2025) — how does heading hierarchy affect retrieval?
- MIRACL-specific: What structural information is actually available in the MIRACL corpus? Just titles and passage positions, or is there more (section headings, categories)?
- **Key question:** Can we extract Wikipedia section headings from the MIRACL data, or do we need the MediaWiki API?

#### 3. Deep-dive into ontology/metadata-guided QE
- Read BMQExpander (arXiv:2508.11784) in full — they serialize ontology subgraphs into prompts. How exactly?
- What's the closest equivalent to a biomedical ontology for Arabic Wikipedia? (Categories? Article link structure? Wikidata?)
- Multi-Meta-RAG (Poliakov et al., 2024) — how do they extract metadata from queries?
- **Key question:** Is Wikipedia category information accessible for MIRACL passages without API calls? If not, is the article title + passage position enough?

#### 4. Understand what's novel vs what exists
- Does ANY paper do corpus-steered QE specifically for Arabic? (We believe no, but need to confirm exhaustively)
- Does any paper combine first-pass BM25 context with Query2Doc-style generation? (CSQE is close but not identical)
- What's the exact novelty claim we can make? Options:
  a. "First corpus-steered QE for Arabic" (language novelty)
  b. "First to use Wikipedia article structure in QE prompts" (method novelty)
  c. "First to combine corpus-steered QE with hybrid retrieval" (combination novelty)
  d. Some combination of the above

#### 5. Finalize the prompt design
- What goes in the context block? Options to investigate:
  - Article titles only (lightest, most scalable)
  - Article titles + first-N-tokens of passages
  - Article titles + passage snippets + passage position info
  - Article titles + Wikipedia categories (if accessible)
  - Article titles + co-occurring passage titles from same article
- How much context can we fit in the LLM's input? (Aya 8B context window = 8192 tokens)
- Should the prompt instruct the LLM to focus on specific aspects of the context?
- **Key question:** What's the optimal trade-off between context richness and prompt length for a 2-8B model?

#### 6. Investigate the first-pass retriever question
- Should the first pass be BM25 (fast, keyword-based) or mDPR (semantic)?
- What if the first-pass retriever misses the relevant article entirely? (coverage analysis in Exp 3.1 will answer this, but we should have expectations from literature)
- How many first-pass documents (K) do similar approaches use?
- CSQE uses K=10, BMQExpander uses ontology (no first pass) — what works for our scale?

#### Research Phase Deliverables
- [ ] `research_decisions/mufti_approach_deep_research.md` — detailed findings from papers above
- [ ] Finalized prompt template (or 2-3 candidates to A/B test)
- [ ] Decision on context extraction strategy (what metadata, from where)
- [ ] Confirmed novelty claim with evidence
- [ ] Updated experiment plan with any changes from deep research

---

### IMPLEMENTATION PHASE (Phase B-Implement): Experiments 3.1–3.4

### Experiment 3.1: First-Pass Context Extraction

**What:** For each query:
1. BM25 first-pass → top-K passages (K ∈ {3, 5, 10})
2. Extract metadata from MIRACL corpus: article title (from docid "X#Y"), passage position, co-occurring passages
3. Build context block for LLM prompt

**Expected output:** Table "First-Pass BM25 Coverage" — % of relevant articles found at K=3,5,10

**Effort:** 1 day | **Reuses:** BM25 index, MIRACL corpus | **New:** Metadata extraction script

---

### Experiment 3.2: Context-Aware Pseudo-Document Generation

**What:** New prompt template including corpus context:
```
Given the Arabic query: "{query}"

The following relevant information was found in the knowledge base:
- From article "{title_1}": "{passage_snippet_1}"
- From article "{title_2}": "{passage_snippet_2}"
- From article "{title_3}": "{passage_snippet_3}"

Based on this context, generate a detailed Arabic passage that
would help answer this query. Focus on the specific topics and
terminology found in the knowledge base.
```

**Models:** Aya Expanse 8B (primary), Jais-2-8B (if time permits)

**Expected output:** Table "Blind vs Corpus-Steered Query2Doc" on both Dense and BM25

**Key papers:** CSQE (Lei et al., EACL 2024, arXiv:2402.18031), BMQExpander (arXiv:2508.11784), DAPR (Wang et al., ACL 2024, arXiv:2305.13915)

**Effort:** 3-4 days | **Reuses:** BM25 index, Aya model, mDPR index | **New:** Context extraction pipeline, new prompt, generation run

---

### Experiment 3.3: Ablation Study

**What:** Test which context components matter:
- No context (baseline Query2Doc)
- Title only (article titles in prompt)
- Passage only (passage snippets, no titles)
- Full context (titles + passages)
- K variation (K=1,3,5,10)

**Models:** Aya Expanse 8B

**Expected output:** Table "Ablation: What Context Helps?" + figure (performance vs K)

**Effort:** 3-4 days (multiple generation runs)

---

### Experiment 3.4: Full Pipeline (Corpus-Steered + Hybrid)

**What:** Combine best from 3.2/3.3 with 4-way hybrid fusion from 2.1

**Expected output:** Table "Full Pipeline Results" — the culminating headline result

**Effort:** 1-2 days (if all components ready)

---

### Direction 3 Dependencies

```
[3.1: Context Extraction]
         │
         ▼
[3.2: Context-Aware Generation] ──→ [3.3: Ablation]
         │                                │
         └──────────┬─────────────────────┘
                    ▼
          [3.4: Full Pipeline]
          (also needs 2.1 done)
```

---

## Master Timeline

```
WEEK 1 (Quick Wins):
  Day 1:   [1.1] BM25 query repetition — re-evaluate ALL 9 models
  Day 2:   [1.2] Hybrid baseline (BM25+mDPR CC fusion)
  Day 3:   [1.3] HyDE comparison using existing pseudo-documents
  Day 4-5: [1.4] Prompt variants (CoT, keywords, rewriting)

WEEK 2 (Hybrid + QE):
  Day 1-2: [2.1] 4-way fusion with Aya
  Day 2:   [2.3] Dual-list BM25 fusion (parallel with 2.1)
  Day 3-5: [2.2] Retriever-specific prompts

WEEK 3 (Corpus-Steered):
  Day 1:   [3.1] First-pass context extraction + coverage analysis
  Day 2-4: [3.2] Context-aware generation
  Day 5:   [3.3] Begin ablation study

WEEK 4 (Polish):
  Day 1-2: [3.3] Complete ablation study
  Day 3:   [3.4] Full pipeline (corpus-steered + hybrid)
  Day 4-5: Error analysis, write-up, update thesis chapters
```

---

## Thesis Chapter Updates

| Chapter | Addition | Source Experiments |
|---------|----------|-------------------|
| Ch. 2 (Literature Review) | HyDE vs Query2Doc positioning, hybrid retrieval background, corpus-steered QE concept, term dilution explanation | All directions |
| Ch. 3 (Methodology) | Hybrid fusion method, query repetition strategy, corpus-steered pipeline description, retriever-specific prompts | 1.1, 1.2, 2.2, 3.2 |
| Ch. 4 (Experiments) | ~8 new result tables, 2-3 new figures | All experiments |
| Ch. 5 (Analysis) | BM25 degradation root cause + fix, dense-sparse complementarity, ablation insights, "mufti" validation | 1.1, 2.1, 3.3 |

---

## Which Direction is the Strongest Thesis Contribution?

**Direction 3 (Corpus-Steered Query2Doc)** is the strongest thesis contribution because:

1. **Novelty:** No existing paper does corpus-steered QE for Arabic with Wikipedia structural metadata
2. **Thesis narrative:** The "mufti analogy" gives the thesis a compelling central metaphor — progression from "blind answering" (Query2Doc) to "expert search" (knowing WHERE to look)
3. **Research contribution:** Introduces a genuinely new idea (grounding QE in corpus structure) vs. engineering improvements
4. **Publication potential:** Clear contribution suitable for a standalone paper
5. **Generalizability:** The approach works for any domain with structured documents, not just Arabic/MIRACL

**However**, Directions 1 & 2 are prerequisites — you need proper baselines (hybrid, BM25 fix) before claiming corpus-steered QE adds value on top of them.

---

## Key Literature References

### Direction 1
- Query2Doc: Wang et al., EMNLP 2023, arXiv:2303.07678
- HyDE: Gao et al., ACL 2023, arXiv:2212.10496
- MuGI: Zhang et al., EMNLP 2024 Findings, arXiv:2401.06311
- GRF: Mackie et al., SIGIR 2023, arXiv:2304.13157
- CoT-QE: Jagerman et al., 2023, arXiv:2305.03653
- Knowledge leakage: Yoon et al., 2025, arXiv:2504.14175
- Arabic QE validation: Macmillan-Scott et al., 2025, arXiv:2511.19325

### Direction 2
- MIRACL: Zhang et al., TACL 2023, arXiv:2210.09984
- Exp4Fuse: Liu et al., ACL 2025 Findings, arXiv:2506.04760
- CC vs RRF: Bruch et al., ACM TOIS 2023, arXiv:2210.11934
- LevelRAG: Zhang et al., 2025, arXiv:2502.18139
- Dense-sparse complementarity: Lee et al., ACL 2023

### Direction 3
- CSQE: Lei et al., EACL 2024, arXiv:2402.18031
- BMQExpander: arXiv:2508.11784
- DAPR: Wang et al., ACL 2024, arXiv:2305.13915
- Contextual Retrieval: Anthropic, September 2024
- KAR: Sharifymoghaddam et al., NAACL 2025, arXiv:2410.13765
