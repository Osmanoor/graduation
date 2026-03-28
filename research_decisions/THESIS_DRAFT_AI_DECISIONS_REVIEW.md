# AI Decisions & Assumptions in Thesis Draft — Review Document

**Created:** 2026-03-28
**Purpose:** Catalog ALL decisions and assumptions the AI made across thesis writing sessions (Phase 3, Tasks 5.1–5.6) so Mohammed and Osman can validate them before finalizing.
**Status:** REQUIRES HUMAN REVIEW

---

## How to Use This Document

Each item is tagged:
- **GROUNDED (Dr. Tahani)** — Decision based on explicit supervisor guidance from the 17 March meeting
- **GROUNDED (Experiments)** — Decision based on experiment docs, notebooks, or measured results
- **GROUNDED (Literature)** — Decision based on cited papers read during the session
- **AI ASSUMPTION** — Decision the AI made independently; needs your validation

For each AI ASSUMPTION, a justification is provided. Mark each item:
- Approve / Revise / Reject

---

## Chapter 2: Theoretical Background and Literature Review

### Structure & Organization

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 2.1 | Organized into 4 main sections: Theoretical Background, Mathematical Models, Models Used, Related Work | **AI ASSUMPTION** | Follows standard thesis literature review structure (broad theory → math → specifics → gap). Dr. Tahani said Ch.2 should be "background and review" but did not prescribe specific sections. |
| 2.2 | Placed mathematical formulations (BM25, cosine similarity, NDCG, Recall, MRR) in their own Section 2.2 rather than inline with theory | **AI ASSUMPTION** | Keeps theory readable and provides a single reference point for equations cited in Ch.3/4. Could alternatively be merged into Section 2.1. |
| 2.3 | Included a Chapter Summary section (Section 2.5) with bullet points | **AI ASSUMPTION** | Provides a quick recap before the methodology chapter. Dr. Tahani did not mention chapter summaries. Some supervisors prefer them; some consider them filler. |
| 2.4 | Funnel structure for Related Work: Foundational QE (2022–23) → Modern QE (2024–25) → Arabic IR → Research Gap | **AI ASSUMPTION** | Chronological-then-thematic organization. The "research gap" subsection explicitly bridges to the thesis objectives. This structure is common but not the only valid approach. |

### Content Decisions

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 2.5 | Described 11 models (10 evaluated + GPT-OSS) each with architecture, training data, Arabic benchmarks, and VRAM requirements | **GROUNDED (Experiments)** | All model details sourced from research docs (`falcon_h1_research.md`, `jais_2_research.md`, `qwen3_4b_research.md`, etc.) and official model cards. |
| 2.6 | Cited ~40 references total, organized by IEEE order-of-appearance numbering | **GROUNDED (Dr. Tahani)** | Dr. Tahani explicitly said "IEEE format — numbered by order of appearance." |
| 2.7 | Stated "none of these studies tested models smaller than 7B for zero-shot query expansion on Arabic text" as the research gap | **AI ASSUMPTION** | Based on the literature surveyed in the session. This is the central gap claim. **You should verify this is accurate** — if any paper does test <7B on Arabic QE, this claim needs revision. |
| 2.8 | Described HyDE, Query2Doc, and GRF as the three main LLM-based QE techniques | **GROUNDED (Literature)** | These are the three most-cited techniques in the papers surveyed (Gao 2022, Wang 2023, Mackie 2023). Other techniques exist but are less established. |
| 2.9 | Included Rewrite-Retrieve-Read (Ma et al. 2023) as a separate "Query Rewriting" category distinct from expansion | **AI ASSUMPTION** | Categorization follows Song & Zheng (2024) taxonomy of QE operations. Could be grouped differently. |
| 2.10 | Arabic challenges section covers: morphological richness, diglossia, orthographic variations, diacritical marks | **GROUNDED (Literature)** | Standard Arabic NLP challenges cited in Alsubhi 2025 and El-Beltagy 2024. Matches the problem framing in Ch.1. |
| 2.11 | Used the term "morphological gap" to describe Arabic-specific vocabulary mismatch | **AI ASSUMPTION** | This term is not from a specific paper — it was coined to unify the Arabic challenges under one concept. If you prefer a different term or want to cite a specific source, revise. |
| 2.12 | BM25S described with parameters k1=1.5, b=0.75 in Section 2.3 (Models Used) but k1=0.9, b=0.4 in Chapter 3 (methodology) | **POTENTIAL INCONSISTENCY** | Section 2.3.2 says "default parameters (k1=1.5, b=0.75)" but Chapter 3 Section 3.2.2 says "Lucene-style scoring with k1=0.9, b=0.4". **Check which values were actually used in experiments.** The Ch.3 values are more specific and likely correct — the Ch.2 values may describe BM25S defaults vs. your configured values. |

### References & Citations

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 2.13 | Included 15+ papers in Related Work from 2022–2025 | **GROUNDED (Literature)** | Sourced from papers in `papers/arxiv_downloads/` and web searches during the session. |
| 2.14 | Cited Song & Zheng (2024) as the taxonomy reference for query enhancement | **AI ASSUMPTION** | This paper was identified during the session as providing a useful categorization framework. Verify this is a paper you're comfortable citing — check if it's peer-reviewed or a preprint. |
| 2.15 | Used `\cite{key}` format with specific BibTeX keys that may not match your References.bib | **AI ASSUMPTION** | The session generated citation keys like `wang_2023_query2doc`, `gao_2022_precise`, etc. **These must be cross-checked against your actual `References.bib` file to ensure all keys exist and are correct.** |

---

## Chapter 3: Methodology

### Structure & Organization

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 3.1 | Organized as: Dataset/Setup → Baseline → Error Analysis → Query2Doc → Model Comparison | **GROUNDED (Dr. Tahani)** | Dr. Tahani said methodology should follow the zigzag pattern with Ch.4. This order mirrors the actual experimental sequence. |
| 3.2 | Each methodology section maps 1:1 to a Ch.4 results section | **GROUNDED (Dr. Tahani)** | Dr. Tahani explicitly said "zigzag — each methodology section should have a corresponding results section." |

### Technical Decisions

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 3.3 | Stated mDPR was "intentionally selected as a weaker baseline" to maximize headroom | **GROUNDED (Experiments)** | This rationale appears in your experiment documentation. mDPR was pre-trained on MS MARCO, not fine-tuned on MIRACL. |
| 3.4 | Described BM25S as achieving "96% of official Pyserini BM25 performance" with the 4% gap deemed acceptable | **GROUNDED (Experiments)** | This comparison was documented in your baseline experiment results. |
| 3.5 | Stated the Java 21/11 dependency conflict as the reason for choosing BM25S over Pyserini | **GROUNDED (Experiments)** | This technical issue was documented in your experiment notebooks. |
| 3.6 | Error analysis thresholds: Failed (<0.3), Mediocre (0.3–0.7), Successful (>=0.7) | **GROUNDED (Experiments)** | These thresholds come from your error analysis documentation (`error_analysis_phase1_quantitative.md`). |
| 3.7 | Query length buckets: Short (1–3), Medium (4–8), Long (9+) | **GROUNDED (Experiments)** | Defined in your error analysis experiment. |
| 3.8 | System prompt: "You are asked to write a passage that answers the given query. Do not ask the user for further clarification. Respond in Arabic only." | **GROUNDED (Experiments)** | This is the actual prompt used across all experiments, documented in your notebooks. |
| 3.9 | Max tokens = 128 described as "balance between expansion quality and inference speed" with "256 tokens showed diminishing returns" | **AI ASSUMPTION** | The 128-token limit is from your experiments, but the specific claim about "diminishing returns at 256" — **verify this was actually tested** or if 128 was simply the chosen value. |
| 3.10 | Described "16x combined speedup" from batch processing + reduced tokens + inference optimizations | **AI ASSUMPTION** | The individual optimizations are documented, but the "16x" multiplier (8x batching × 2x token reduction) is a calculated estimate. **Verify this matches your actual observed speedup.** |
| 3.11 | Temperature selection rationale: SILMA tested at 0.7 vs 0.1, with 0.1 yielding +2.5% improvement | **GROUNDED (Experiments)** | This comparison was documented in the SILMA experiment results. |
| 3.12 | Described work division: "one researcher tested [Mohammed's 5 models], while the other tested [Osman's 5 models]" | **GROUNDED (Experiments)** | Matches the documented task split in `model_comparison_guide.md`. |
| 3.13 | Included Table 3.2 with specific model configs (precision, temperature, batch size, GPU) for all 11 models | **GROUNDED (Experiments)** | All values sourced from individual experiment notebooks and research documents. **Cross-check each row against your actual experiment configs.** |

---

## Chapter 4: Results and Discussion

### Numerical Results

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 4.1 | All numerical results (NDCG@10, Recall@10, Recall@100, MRR) for all models | **GROUNDED (Experiments)** | All numbers sourced from experiment documentation and the reference baselines in CLAUDE.md. |
| 4.2 | mDPR baseline "reproduced with less than 0.1% difference" (0.4993 vs published 0.499) | **AI ASSUMPTION** | The 0.4993 value is from your experiments. The "published 0.499" was cited as the official MIRACL result. **Verify the official published mDPR score is indeed 0.499.** |
| 4.3 | Percentage improvements calculated relative to baselines (e.g., Aya = +23.5%) | **GROUNDED (Experiments)** | Calculated as (new - baseline) / baseline × 100. Math is straightforward but **spot-check a few**: e.g., Aya dense: (0.6164 - 0.4993) / 0.4993 = 23.46% ≈ 23.5%. |

### Analytical Claims & Interpretations

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 4.4 | Attributed BM25 degradation to "term dilution" — the pseudo-document vocabulary diluting original query keyword weights | **GROUNDED (Literature)** | Wang et al. (2023) describe this phenomenon and recommend query repetition (n=5) as mitigation. Your experiments confirmed the effect. |
| 4.5 | Hypothesized Arabic benefits "disproportionately" from vocabulary expansion due to morphological richness | **AI ASSUMPTION** | This is an interpretive claim explaining why +8.9% with 3B zero-shot exceeded original paper's +2-5% with 175B few-shot. It's plausible but not proven. Two alternative explanations are also mentioned (weaker baseline = more headroom). **Decide if you want to present this as a hypothesis or a conclusion.** |
| 4.6 | Stated "model parameter count was positively correlated with dense retrieval improvement" with size tiers | **GROUNDED (Experiments)** | The size tiers (2-3B: +3.7-8.9%, 4B: +8.0-14.0%, 7-8B: +16.4-23.5%) are directly from the results. However, no formal correlation coefficient was computed — **the claim is based on visual trend, not statistical test.** |
| 4.7 | Claimed "Arabic NLP benchmark scores do not directly predict query expansion quality" | **AI ASSUMPTION** | Based on observation that Falcon-H1 (highest OALL at 3B) was outperformed by Qwen 2.5 3B (lower OALL). This is a notable claim that examiners may challenge. **Consider whether you want to state this as a definitive finding or a preliminary observation.** |
| 4.8 | Attributed Jais-2's BM25 success to its "150,000-token Arabic-centric vocabulary" | **AI ASSUMPTION** | Plausible mechanistic explanation — larger Arabic vocabulary means generated pseudo-documents use terms closer to BM25 index vocabulary. But this was not experimentally tested (e.g., by comparing tokenized output distributions). **Present as hypothesis, not proven mechanism.** |
| 4.9 | Claimed Aya's BM25 success is due to "purpose-built multilingual training (101 languages with explicit Arabic optimization)" | **AI ASSUMPTION** | Similar to 4.8 — plausible but not experimentally isolated. The actual cause could be training data quality, instruction tuning quality, or other factors. |
| 4.10 | Qwen generational comparison table: attributed improvement to "doubled training data volume (36T vs 18T tokens)" | **GROUNDED (Literature)** | Training data volumes from official Qwen technical reports. The causal attribution is reasonable but other factors (architecture changes, alignment techniques) also changed between generations. |
| 4.11 | Described dense retrieval as "universally benefiting" while BM25 showed "divergent behavior" | **GROUNDED (Experiments)** | 9/9 improved dense, 3/9 improved BM25 — this is factual from the results. |
| 4.12 | "Best Model Recommendations" section with 4 recommendations (Aya overall, Jais-2 BM25, Qwen3-4B constrained, temp 0.1) | **AI ASSUMPTION** | These recommendations follow logically from the data, but presenting them as formal "recommendations" is an editorial choice. **Decide if this belongs in Ch.4 (results) or only in Ch.5 (conclusions).** Dr. Tahani said Ch.4 should include discussion, so recommendations-from-data seem appropriate here. |
| 4.13 | Included BM25 results for Osman's models (SILMA, Qwen 2.5-7B, Qwen3-8B, Gemma 3, Aya) even though some BM25 experiments may not have been documented as extensively as Mohammed's | **AI ASSUMPTION** | The BM25 leaderboard includes all 9 models. **Verify that all BM25 numbers for Osman's models are accurate — check if they were all actually run or if some are projected.** |

### Tables & Figures

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 4.14 | 12 tables total covering: baselines, error analysis, Q2D results, leaderboards, comparisons, summary | **AI ASSUMPTION** | The number and organization of tables was determined by the AI. Some tables could be combined or split differently. |
| 4.15 | 2 placeholder figures: bar chart (dense NDCG) and scatter plot (size vs. performance) | **AI ASSUMPTION** | These are the two most informative visualizations. **You need to create actual figures** — the placeholders are `\fbox` boxes with text descriptions. Consider if you want different/additional figures. |
| 4.16 | Full experiment summary table (Table 4.10) includes experiment numbers, some marked "---" for Osman's experiments | **AI ASSUMPTION** | Mohammed's experiments have clear exp numbers (001-009). Osman's experiments are listed without experiment numbers (marked "---"). **Assign proper experiment numbers to Osman's work.** |

---

## Chapter 1: Introduction

### Structure & Organization

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 1.1 | Four introductory paragraphs narrowing from digital Arabic content → RAG → Arabic challenges → QE → gap | **AI ASSUMPTION** | Standard funnel introduction. Dr. Tahani said Ch.1 should have "no references" and be "your own framing" — the AI wrote it purely in the authors' voice. |
| 1.2 | Problem Definition structured as three "gaps": retrieval gap, language gap, resource gap | **AI ASSUMPTION** | This three-gap framing is an editorial choice. It effectively structures the problem but was not prescribed by Dr. Tahani. **Decide if you prefer a different framing** (e.g., two gaps, or a single narrative paragraph). |
| 1.3 | Research question: "To what extent can small, open-source LLMs improve Arabic information retrieval through query enhancement, and what model characteristics determine effectiveness?" | **AI ASSUMPTION** | This was crafted to encompass all 5 objectives. **This is arguably the single most important sentence in the thesis — review carefully.** Does it capture what you actually investigated? Is "small" the right word? Should "2–8 billion parameters" be in the question? |

### Content Decisions

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 1.4 | Five objectives mapping to Ch.3 methodology sections | **AI ASSUMPTION** | The objectives were synthesized from the actual experimental work. **Verify each objective matches what was actually done**: (1) baselines, (2) error analysis, (3) Query2Doc adaptation, (4) 10-model comparison, (5) analysis of model characteristics. |
| 1.5 | Objective 4 says "ten open-source LLMs" — this counts the 10 evaluated models (not 11 attempted) | **AI ASSUMPTION** | Could say "eleven" (including GPT-OSS which was attempted) or "ten" (successfully evaluated, minus ALLaM as dropped). The AI chose "ten" to match the protocol. **Decide: ten or eleven?** |
| 1.6 | No references in Chapter 1 | **GROUNDED (Dr. Tahani)** | Dr. Tahani explicitly said "Chapter 1 has no references — it's your framing." |
| 1.7 | Thesis Layout describes Ch.2-5 in one paragraph each | **AI ASSUMPTION** | Standard thesis layout section. The descriptions summarize what each chapter contains. **Review that each description accurately reflects the actual chapter content.** |

---

## Chapter 5: Conclusion and Recommendations

### Conclusions (Section 5.1)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 5.1 | Six conclusion topics: baseline & error analysis, Query2Doc transfer, model comparison, analytical findings, dense vs. BM25 divergence, overall | **AI ASSUMPTION** | These map to the main findings in Ch.4. The grouping and ordering was determined by the AI. **Verify nothing important was omitted and the emphasis is correct.** |
| 5.2 | Stated "Arabic's morphological richness may cause it to benefit disproportionately from vocabulary expansion" | **AI ASSUMPTION** | Same as 4.5 — this is a hypothesis, not a proven finding. It appears in both Ch.4 (discussion) and Ch.5 (conclusion). **Decide if you want this in the conclusions or only as a discussion point in Ch.4.** |
| 5.3 | Used phrase "the most practically significant finding" for dense/BM25 divergence | **AI ASSUMPTION** | Editorial judgment about which finding is "most significant." **You may disagree** — perhaps the 3B outperforming 175B result is more significant to you. |

### Challenges (Section 5.2)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 5.4 | Six challenges listed: resource constraints, BM25 term dilution, dropped models, dataset scope, single QE technique, baseline retriever strength | **GROUNDED (Experiments)** | All six challenges were actually encountered and documented. |
| 5.5 | Challenge 6 frames weak baseline as a deliberate choice: "intentionally selected as a weaker baseline" | **AI ASSUMPTION** | This frames a potential limitation as a design decision. **Examiners may ask: was it intentional from the start, or a post-hoc justification?** If it was genuinely intentional, keep it. If mDPR was used because it was the available pre-built index, say so honestly. |

### Recommendations (Section 5.3)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| 5.6 | Eight recommendations ordered from direct extensions to broader directions | **AI ASSUMPTION** | The ordering and scope of recommendations was determined by the AI. |
| 5.7 | Recommendation 1 (knowledge-base-aware / chunking-aware QE) positioned first and described in most detail | **AI ASSUMPTION** | Strategically positioned to set up Phase 4 work. This is a genuine research direction but **its prominent placement was an editorial choice** to create narrative continuity with your next experiments. |
| 5.8 | Recommendation 5 (dialectal Arabic) suggests QE "may help bridge MSA-dialect gaps by generating MSA-vocabulary pseudo-documents from dialectal queries" | **AI ASSUMPTION** | This is a speculative hypothesis. It's plausible but untested. **Decide if this speculation belongs in a recommendations section or is too speculative.** |
| 5.9 | Recommendation 8 (publication) states the results are "suitable for publication" and recommends "pre-print submission or faculty journal publication" | **AI ASSUMPTION** | This reflects the ambition discussed in the 17 March meeting. **Dr. Tahani mentioned publication as a goal, but claiming results are "suitable for publication" is an assertion the AI made.** Let your supervisor confirm this. |

---

## Abstract (English & Arabic)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| A.1 | 334 words — within the typical 250-350 word range for a bachelor's thesis abstract | **AI ASSUMPTION** | Dr. Tahani said "short and to the point." 334 words is on the longer end. **Consider trimming if your department has a specific word limit.** |
| A.2 | Structure: context → problem → objectives → methodology → results → conclusion (6 sentences) | **GROUNDED (Dr. Tahani)** | Dr. Tahani described this structure for the abstract. |
| A.3 | Key numbers highlighted: +3.7% to +23.5%, Aya +23.5% dense / +9.2% BM25, Jais-2 +10.8% BM25, 3B > 175B | **GROUNDED (Experiments)** | All numbers from experiment results. |
| A.4 | Final sentence: "establishing LLM-based query enhancement as a practical strategy for Arabic RAG systems" | **AI ASSUMPTION** | This is a strong concluding claim. **"Practical strategy" implies deployment readiness, which may be stronger than what the experiments prove** (they show retrieval improvement on a benchmark, not production deployment). Consider "a promising strategy" if you want to be more conservative. |
| A.5 | Arabic translation is a "faithful" translation of the English abstract | **AI ASSUMPTION** | The Arabic was generated by the AI. **Have a native Arabic speaker review the Arabic abstract for accuracy, natural phrasing, and correct technical terminology.** Machine-translated academic Arabic often sounds unnatural. |

---

## Cross-Cutting Decisions (All Chapters)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| X.1 | Passive voice throughout all chapters | **GROUNDED (Dr. Tahani)** | Dr. Tahani explicitly said "passive voice — this is standard for UofK theses." |
| X.2 | Cross-reference labels (33 in Ch.2, 26 in Ch.3, 29 in Ch.4) for internal linking | **AI ASSUMPTION** | Heavy cross-referencing keeps the thesis internally consistent, but some labels may never be used. **Not a problem — unused labels are harmless in LaTeX.** |
| X.3 | Consistent use of "query enhancement" (not "query expansion" or "query optimization") as the umbrella term | **AI ASSUMPTION** | "Query enhancement" was chosen to encompass all techniques (expansion, rewriting, etc.). Your experiments focus on query expansion specifically, but the broader term is used when discussing the field. **Verify this is consistent across all chapters.** |
| X.4 | Abbreviation handling: full form (ABBR) on first use per chapter | **GROUNDED (Dr. Tahani)** | Standard academic convention, confirmed by Dr. Tahani. |
| X.5 | British English spelling conventions (e.g., "organised", "optimisation") | **AI ASSUMPTION** | The AI defaulted to British English based on writing style. **If your department requires American English, all chapters need spelling review.** |
| X.6 | All placeholder figures use `\fbox{\parbox{...}}` with descriptive text | **AI ASSUMPTION** | Placeholder approach so you can see where figures go. **You must create actual figures before submission.** The placeholders describe what each figure should show. |

---

## Priority Review Items

### MUST review before finalizing (could affect thesis correctness):

1. **2.7** — Research gap claim ("none tested <7B on Arabic QE") — verify accuracy
2. **2.12** — BM25S parameter inconsistency between Ch.2 and Ch.3
3. **4.2** — Official mDPR baseline score verification
4. **4.13** — BM25 numbers for Osman's models — verify all were actually run
5. **4.16** — Assign experiment numbers to Osman's experiments
6. **A.5** — Arabic abstract quality review by native speaker
7. **2.15** — BibTeX citation keys must match `References.bib`
8. **1.3** — Research question wording

### SHOULD review (editorial choices that affect thesis narrative):

9. **1.2** — Three-gap problem framing
10. **4.5/5.2** — "Arabic benefits disproportionately" hypothesis — keep or weaken?
11. **4.7** — "Benchmark scores don't predict QE quality" — finding or observation?
12. **4.8/4.9** — Mechanistic explanations for Jais-2/Aya BM25 success
13. **5.3** — Which finding is "most practically significant"?
14. **5.5** — Was weak baseline intentional or pragmatic?
15. **A.4** — "Practical strategy" vs "promising strategy"

### CAN defer (style preferences, low risk):

16. **2.1–2.4** — Chapter 2 section structure
17. **2.11** — "Morphological gap" terminology
18. **X.5** — British vs American English
19. **5.6–5.9** — Recommendation ordering and content

---

## Instructions for Review Meeting

1. Go through the **MUST review** items first — these could affect correctness
2. Discuss the **SHOULD review** items — these shape the thesis narrative
3. For each item, decide: Approve / Revise / Reject
4. After the review, the AI will update all chapters to reflect your decisions
5. Pay special attention to items where the AI made **interpretive claims** (4.5, 4.7, 4.8, 4.9, 5.2, 5.3) — these are the places where the thesis makes claims beyond what the raw data shows
