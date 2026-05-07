# AI Decisions & Assumptions in Thesis Draft — Review Document

**Created:** 2026-03-28
**Updated:** 2026-04-22 — Expanded with Phase 4 brief additions (see `PART II — PHASE 4 UPDATES` below)
**Purpose:** Catalog ALL decisions and assumptions the AI made across thesis writing sessions so Mohammed and Osman can validate them before finalizing.
**Status:** REQUIRES HUMAN REVIEW

**Scope:**
- **Part I (items 1.x–5.x, A.x, X.x):** Initial draft (Phase 3, Tasks 5.1–5.6) — base chapters 1-5 and abstract before Phase 4 experiments.
- **Part II (items P4.x.y):** Phase 4 brief (`thesis_update_brief.md`, 2026-04-15) — new material for Exp 1.1 (BM25 repetition), Exp 1.2 (Hybrid fusion), Exp 013 (CSQE), Exp 013c/013d (ablations), Exp 2.1 (CSQE+Hybrid), and per-query error analysis.

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

# PART II — PHASE 4 UPDATES (brief dated 2026-04-15)

Everything below catalogs AI decisions/assumptions introduced in `thesis_update_brief.md` — the document used to update the thesis after Phase 4 experiments (query repetition, hybrid fusion, CSQE, CSQE+hybrid, error analysis). Items are numbered `P4.{chapter}.{n}`.

**Important standing caveat before reviewing Phase 4 items:**
The brief itself contains a **known data-provenance issue** (see item P4.4.20): the per-query error analysis was computed against **Config C RRF (0.6936)**, NOT the best system Config A RRF (0.7137). The brief honestly flags this and proposes two disclosure options; the AI chose one. Review this first before approving anything downstream in Ch. 4 §4.10 or Ch. 5.

---

## Chapter 1 — Phase 4 Additions

### New Objectives (Section 1.2)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.1.1 | Added three new objectives (query repetition, CSQE adaptation for Arabic, CSQE+hybrid with retriever-specific representation) as Objectives 6–8, appended to the existing 1–5 | **AI ASSUMPTION** | The framing turns experimental work into pre-stated objectives. **Retrospective reconstruction:** Objective 8 specifically ("examining whether applying query expansion asymmetrically to one retriever outperforms applying it to both") was a finding, not a pre-planned question. Stating it as an objective may be questioned by examiners if they ask "when did you decide to test this?" Consider rewording Objective 8 to "investigating how query expansion should be applied across retrievers in a hybrid pipeline" — more honest about the exploratory nature. |
| P4.1.2 | Retained 5-objective thesis layout implicitly by not renumbering or re-framing the original 5 — new objectives are simple appendages | **AI ASSUMPTION** | Keeps the original thesis integrity but means Objectives 1–5 no longer fully describe the work. **Alternative:** re-cluster into fewer, broader objectives (e.g., "evaluate QE across BM25, Dense, and hybrid" as one umbrella). Decide with Dr. Tahani if the expanded objectives list is too long. |
| P4.1.3 | Objective 6 (query repetition) framed as "resolving the BM25 term-dilution degradation" — positions repetition as a fix rather than a novel contribution | **AI ASSUMPTION** | This framing is accurate but downplays the contribution. **Decide:** you could alternatively frame it as "investigating the effect of query repetition on BM25 query expansion effectiveness" — presents it as investigation rather than fix. |

### Thesis Layout Updates (Section 1.3)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.1.4 | Ch.3 layout description extended to list: "query repetition methodology for resolving BM25 term-dilution, the hybrid BM25--Dense fusion methodology, and the Corpus-Steered Query Expansion (CSQE) pipeline including its component ablation design and retriever-specific application strategy" | **AI ASSUMPTION** | Dense paragraph that mentions everything. **May be too long.** Could split into a second sentence. |
| P4.1.5 | Ch.4 layout description uses "Phase 4 expanded results" terminology | **AI ASSUMPTION** | "Phase 4" is your internal project phasing and **should NOT appear in the thesis** — examiners won't know what it means. Recommend replacing with "extended experimental results" or similar. |

---

## Chapter 2 — Phase 4 Additions

### Expanded Sections

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.2.1 | Added RRF equation with k=20 stated as "typical" inside the equation block text | **GROUNDED (Literature)** | Bruch et al. 2023 standard. Labels `eq:rrf_ch2` and `eq:hybrid_cc_ch2` chosen by AI to distinguish from Ch.3 re-uses. |
| P4.2.2 | Added CC equation with min-max normalisation notation (`\hat{s}`) | **AI ASSUMPTION** | The hat notation was introduced to distinguish normalised from raw scores. Not universally standard. Acceptable but verify consistency across Ch.3 §3.7 where CC is used. |
| P4.2.3 | Expanded CSQE description in `sec:modern_qe` to include Lei et al.'s English benchmark result ("30% improvement in mAP over BM25") | **GROUNDED (Literature)** | From Lei et al. 2024. **Verify this number before citing** — the original paper should be checked for the exact comparison benchmark (passage vs document, single vs multiple datasets). |
| P4.2.4 | Added new research-gap paragraph claiming "the interaction between corpus-steered expansion and hybrid BM25–Dense fusion has not been studied" | **AI ASSUMPTION** | This is a **second-order research gap** introduced to motivate the asymmetric fusion experiments retroactively. **Verify:** a quick search for post-2024 papers combining CSQE with hybrid retrieval should be done before committing to this gap claim. If such work exists, rephrase to position your contribution differently (e.g., "not yet systematically evaluated for Arabic"). |
| P4.2.5 | Claim "whether applying query expansion asymmetrically to only one retriever in a hybrid system can outperform applying it to both is an open question" | **AI ASSUMPTION** | Possibly overclaims novelty. There is hybrid-retrieval literature discussing which component benefits more from enrichment (e.g., Ma et al. 2021 on dense+sparse asymmetries). **Have Osman search for prior work on "asymmetric query expansion in hybrid retrieval"** before publication. |

---

## Chapter 3 — Phase 4 Additions

### Section 3.6 — Query Repetition

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.3.1 | Organized methodology around **two solution families** (fixed Query2Doc-style + adaptive MuGI-style) rather than one | **AI ASSUMPTION** | Both were tested; presenting both preserves scientific record. **Alternative:** if only the winning configuration matters, present MuGI with fixed-n as a simpler baseline. **Decide based on narrative.** |
| P4.3.2 | Sweep ranges stated as n ∈ {1, 3, 5, 7, 10} and β ∈ {2, 4, 6} | **GROUNDED (Experiments)** | From exp_011 notebook. |
| P4.3.3 | Motivating prose: "3-word query paired with 200-token pseudo-document needs more repetition than 15-word query paired with 100-token pseudo-document" | **AI ASSUMPTION** | Pedagogical device — not a literal example from your data, but an intuitive explanation of why adaptive β exists. Verify the intuition holds in your actual distribution before printing. |
| P4.3.4 | Claim "no new LLM inference was needed" because expansions were reused from Task 4.0b pkls | **GROUNDED (Experiments)** | Confirmed in exp_011 design. |
| P4.3.5 | Specific runtime claim: "72 BM25 evaluations ... Total runtime approximately 73 minutes on Colab CPU" | **GROUNDED (Experiments)** | From exp_011 doc. **Quick sanity check:** 72 evals in 73 min ≈ 1 eval/min, which is reasonable for BM25S over 2,896 queries. |
| P4.3.6 | Included MuGI formula `n = max(1, ⌊|d| / (|q|·β)⌋)` with labels `eq:mugi_repetition` | **GROUNDED (Literature)** | From Zhang et al. 2024. |
| P4.3.7 | The enhanced query assembly equation `eq:query_repetition` includes **k** (number of pseudo-documents) — but all Phase 4 Query2Doc experiments used k=1 (single pseudo-doc) | **POTENTIAL CONFUSION** | Presenting the equation with general k when only k=1 was used may confuse readers. **Recommend:** either simplify to k=1 explicitly, or state clearly that "for Query2Doc single-pass, k=1" (the brief already does this parenthetically, but it should be in the main text). |

### Section 3.7 — Hybrid Fusion

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.3.8 | Plan to **cross-reference** `eq:rrf_ch2` and `eq:hybrid_cc_ch2` from Ch.2 rather than re-print equations | **AI ASSUMPTION** | Good practice (avoids duplication). Verify those labels make it into Ch.2 before finalizing Ch.3. |
| P4.3.9 | α swept over {0.1, 0.2, ..., 0.9} and k tested at {20, 60} | **GROUNDED (Experiments)** | From exp_012 doc. |
| P4.3.10 | Fusion setup described as "BM25S and mDPR retrieve top-100 candidates independently" | **GROUNDED (Experiments)** | Confirm: top-100 was the retrieval depth, not top-1000 or top-10. |

### Section 3.8 — CSQE

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.3.11 | Pipeline described as **two-stage** (first-pass + corpus-grounded expansion) rather than three-stage (first-pass, generation, assembly) | **AI ASSUMPTION** | Matches Lei et al. framing. OK. |
| P4.3.12 | Config A/B/C naming convention | **AI ASSUMPTION** | Purely naming — the brief's letters don't map to any external convention. Acceptable but **confirm no clearer naming is possible** (e.g., "BM25-only-expanded" vs "Dense-only-expanded" vs "Both-expanded"). |
| P4.3.13 | Hypothesis stated **before results** that "BM25 benefits from vocabulary breadth; Dense encoder degrades on long inputs" in §3.8.3 | **POTENTIAL METHODOLOGICAL ISSUE** | Writing the hypothesis into the *methodology* chapter makes it look pre-planned, but this was likely a **post-hoc interpretation after seeing Config A outperform Config C**. Examiners may challenge: "How did you know Dense would degrade before running the experiment?" **Recommend:** soften to "Three fusion configurations were tested to determine the optimal retriever–query assignment; whether expansion helps or hurts each retriever was left open" — then save the causal interpretation for Ch.4. |
| P4.3.14 | α sweep "reconstructed from stored expansion pkls — no new LLM inference needed" | **GROUNDED (Experiments)** | Good. |
| P4.3.15 | CSQE configuration k=5, 2c+2b, α=4, temp=1.0, 128 tokens/doc, Aya Expanse 8B BF16 on A100 40GB | **GROUNDED (Experiments)** | Match to exp_013 notebook. **Cross-check temp=1.0** — temperature of 1.0 is unusually high; verify against the actual notebook config before printing. |
| P4.3.16 | CSQE system prompt not written out in the brief (only described abstractly) | **AI ASSUMPTION / GAP** | The Ch.3 narrative refers to a "CSQE-specific system prompt instructing extraction of topically relevant Arabic vocabulary" but doesn't print it. **For reproducibility, the exact prompt should appear in Ch.3 (as the blind Query2Doc prompt does).** Verify the actual prompt used in exp_013 and include it. |

### Section 3.9 — Error Analysis

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.3.17 | Thresholds: Failure nDCG@10 < 0.1, Big Win Δ > 0.3, Regression Δ < −0.1 | **AI ASSUMPTION** | These thresholds are different from Ch.3 §3.6 (Failed < 0.3, Mediocre 0.3-0.7, Successful ≥ 0.7). **Two different threshold systems in the same thesis.** Clarify: the original is for absolute per-query success rating; the Phase 4 set is for pair-wise comparison magnitude. Both are defensible, but the thesis should note this distinction to avoid confusion. |
| P4.3.18 | First-pass quality definition: "any qrel > 0 in top-5" | **GROUNDED (Experiments)** | From error_analysis doc. **Verify in code:** the exact definition (any relevance ≥ 1 vs ≥ 2) matters. |
| P4.3.19 | Manual regression classification into Type A (strong BM25 hurt), Type B (poisoned first-pass), Type C (partial) | **GROUNDED (Experiments)** | Manual inspection was done per the brief. **Was this inspection documented?** If not, the taxonomy and 52/36/12 percentages should have their inspection criteria spelled out in §3.9. |

---

## Chapter 4 — Phase 4 Additions

### Section 4.6 — BM25 Query Repetition Results

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.4.1 | Combined single 8-column table with n∈{1,3,5,7,10} and β∈{2,4,6} side-by-side | **AI ASSUMPTION** | Dense but readable. **Alternative:** split into two tables. Keep combined if you want at-a-glance comparison of fixed vs. adaptive. |
| P4.4.2 | Claim "Query repetition recovers all nine previously degraded BM25 models" | **GROUNDED (Experiments)** | True given n=1 had 3/9 above BM25 baseline and best-config has 9/9. |
| P4.4.3 | Interpretation "large models (8B) converge at MuGI β=2; mid-size (3-4B) plateau at fixed n=5-7; smallest (SILMA 2B) peaks at n=5 because its pseudo-documents are shorter" | **AI ASSUMPTION** | Post-hoc causal story. The 8B-at-β=2 vs 3-4B-at-n=5-7 split is visible in data, but **the "because pseudo-documents are shorter" claim needs verification** — compare actual pseudo-document lengths across models. |
| P4.4.4 | Claim "excessive repetition over-weights the original query tokens and suppresses the useful expansion vocabulary" | **AI ASSUMPTION** | Mechanistically plausible. This is the inverse-of-term-dilution explanation. **Acceptable as discussion, but present as explanation rather than proven mechanism.** |
| P4.4.5 | Framing "query repetition — not a change of model — was the missing ingredient" | **AI ASSUMPTION** | Editorial punch-line. **Decide if Dr. Tahani wants this energetic framing or prefers purely descriptive language.** |
| P4.4.6 | +26.7% improvement claim for Aya β=2 (0.5855 vs 0.4621 baseline) | **GROUNDED (Experiments)** | (0.5855 - 0.4621)/0.4621 = 26.7% — correct. |

### Section 4.7 — Hybrid Fusion Results

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.4.7 | Claim "RRF k=20 and CC α=0.5 are statistically indistinguishable on nDCG@10" | **AI ASSUMPTION** | No formal statistical test (e.g., paired t-test or permutation test) was done. 0.6267 vs 0.6266 differ by 1 in the 4th decimal — practically identical, but "statistically indistinguishable" implies a test. **Recommend:** soften to "numerically indistinguishable" unless you run a significance test. |
| P4.4.8 | Interpretation of CC boundaries: "at α=0.9 the result (0.4996) is essentially mDPR-alone; at α=0.1 the result (0.5248) is higher than BM25 alone because CC still picks up Dense's tie-breaking contribution" | **AI ASSUMPTION** | The "tie-breaking" explanation is plausible but unproven. Could also be that min-max normalisation re-scales scores. **Present as possibility, not established mechanism.** |
| P4.4.9 | Editorial claim "0.6267 nDCG@10 hybrid baseline is the target that all subsequent QE methods must surpass" | **AI ASSUMPTION** | Strong framing. Factually correct (it's your non-QE ceiling) but declarative. **Acceptable as thesis narrative.** |
| P4.4.10 | Recall@100 cited as 0.9467 (from exp_012 source) rather than 0.9466 (CLAUDE.md/exp_021 downstream) | **FLAGGED INCONSISTENCY** | Brief correctly identifies this and recommends 0.9467. **Verify across all tables in Ch.4 before submission.** The 1-unit 4th-decimal difference doesn't affect conclusions but thesis-wide consistency matters. |

### Section 4.8 — CSQE Results

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.4.11 | Interpretation "Dense encoder was trained on short natural-language queries, and the long CSQE expansion (≈1,500 characters) degrades the embedding quality" | **AI ASSUMPTION** | Plausible but untested mechanistically. **Have you verified expansion length ≈1,500 chars?** And "trained on short queries" is true for mDPR (MS MARCO) but should be cited. |
| P4.4.12 | Interpretation "BM25 benefits from vocabulary breadth — blind generation produces full answer paragraphs with diverse Arabic term variants, while corpus extraction produces passage-level excerpts structurally similar to the query" | **AI ASSUMPTION** | Explains why Blind-only > Corpus-only on BM25 individually. **Counter-intuitive finding requires explanation, and this one is the most plausible — keep but mark as interpretation.** |
| P4.4.13 | Claim "combined 2+2 system exceeds both components individually (+0.0405 over blind-only), confirming that corpus and blind expansions are complementary" | **GROUNDED (Experiments)** | 0.6157 - 0.5752 = 0.0405 — correct. "Complementary" is the right word. |
| P4.4.14 | α sweep conclusion "α=1 already captures 98.9% of the α=4 nDCG@10" and "not a critical hyperparameter" | **GROUNDED (Experiments)** + **AI ASSUMPTION** | 0.6095/0.6157 = 98.99% — correct. "Not a critical hyperparameter" is editorial and possibly overclaims — α does shift from 0.7123 to 0.7137 in Config A (small but consistent). **Soften to "has minor effect in this configuration".** |

### Section 4.9 — CSQE + Hybrid

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.4.15 | Framing "Config A is the winner despite giving Dense the weaker input" | **AI ASSUMPTION** | Accurate and striking. Good narrative hook. **Keep.** |
| P4.4.16 | **New terminology "retriever–query representation mismatch"** introduced as the explanatory concept | **AI ASSUMPTION — NEW COINAGE** | This phrase does not appear in prior literature as-is. **Decide:** is this a term you want to claim and define, or should it be rephrased using existing vocabulary (e.g., "input-distribution shift" or "query-length sensitivity")? Coining new terms raises the bar for defense. |
| P4.4.17 | Claim "the relative quality of the two ranked lists matters for RRF — a less discriminative Dense run reduces the fusion ceiling even when it improves individually" | **AI ASSUMPTION** | Plausible and consistent with RRF literature, but stated as a finding. **Present as explanation of Config C < Config A rather than a general RRF claim.** |
| P4.4.18 | Claim "Config A is the winner" elevated to "key design finding of the thesis" in the Ch.3+4 prompt wording | **AI ASSUMPTION** | Editorial priority claim. **Decide:** is this THE key finding, or is it one of several (along with 3B > 175B, corpus grounding fixes hallucinations, etc.)? Ranking importance is a judgement call. |
| P4.4.19 | Delta analysis table (`tab:delta_analysis`) with seven comparisons (Config A vs BM25/mDPR/blind-BM25-QE/blind-Dense-QE/hybrid/ConfigC-vs-A/ConfigB-vs-hybrid) | **AI ASSUMPTION** | Well-chosen comparisons. Verify each calculation. |

### Section 4.10 — Per-Query Error Analysis

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.4.20 | **⚠ CRITICAL: Data provenance — error analysis uses Config C RRF (0.6936), NOT Config A RRF (0.7137)** | **FLAGGED INCONSISTENCY** | The brief honestly discloses this and proposes two options: (a) state explicitly "Config C RRF, 0.6936"; (b) use generic "a CSQE-hybrid system". **The AI chose option (a) and wrote the table caption as "Config C RRF".** Consequences: the per-query analysis is NOT describing the best system (Config A). Mohammed/Osman must approve one of three paths: (i) keep the Config C analysis and explain why (corpus-grounded run shared between A and C, so the BM25-side analysis holds); (ii) re-run the per-query analysis against Config A; (iii) describe as "the Dense+CSQE variant of the hybrid pipeline" to reduce the jar for non-technical readers. **This is the most important review item in Phase 4.** |
| P4.4.21 | Failure-mode analysis: "257 of 258 are irretrievable regardless of QE method — the relevant passage is absent from the Wikipedia corpus dump" | **GROUNDED (Experiments)** | Manual inspection finding. **Verify:** was this actually verified for all 258, or a sample? |
| P4.4.22 | **New terminology "meta-description failure mode"** for the single genuine CSQE failure (qid=1060) | **AI ASSUMPTION — NEW COINAGE** | Naming a single-case failure mode after one query is fragile. **Recommend:** demote from named mode to illustrative example, or find 2-3 more instances before naming. |
| P4.4.23 | Selection of three representative "big win" examples: الرباط المنصوري (Mamluk building), John Dewey (pragmatism), Nicolas Boileau (French poet) | **AI ASSUMPTION** | Out of 1,061 big-wins, three were chosen. Criteria unclear — presumably visually diverse. **Verify these examples are accurate** (query and blind-vs-CSQE comparison exact) and that they are the best illustrations. |
| P4.4.24 | Claim "first-pass recall as the dominant predictor of CSQE effectiveness" based on +0.3063 gap between first-pass-success (0.8877) and first-pass-fail (0.5814) groups | **AI ASSUMPTION** | Strong claim. The gap is real but "dominant predictor" implies a regression/ANOVA was run. Without it, state "the largest observed modulator" or similar. |
| P4.4.25 | Arabic regression example (ماهو التطرف? retrieving "لهجة جنوبية" dialect article) selected as Type B exemplar | **AI ASSUMPTION** | Plausible and illustrative. **Verify the actual behavior on this specific query.** |
| P4.4.26 | Implications/recommendations embedded in Ch.4 §4.10.4: "first-pass quality gate" and "asymmetric expansion weighting" | **AI ASSUMPTION** | Embedding recommendations in Ch.4 is unusual — they more naturally belong in Ch.5. **Decide:** keep the implication paragraph in Ch.4 as preview of Ch.5 recommendations, or move entirely to Ch.5. |
| P4.4.27 | `tab:query_length_split` includes Medium (5-9 words, n=1,900) row but with "—" entries | **AI ASSUMPTION** | Showing a row with no data looks odd. **Either populate the Medium row with actual numbers (they exist in the error analysis doc) or remove the row entirely.** |

### Update to Table 4.10 (Full Summary in §4.5.6)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.4.28 | Plan to add Phase 4 rows to `tab:full_summary`: Aya β=2 BM25, hybrid RRF k=20, BM25+CSQE, Dense+CSQE, Config A RRF | **AI ASSUMPTION** | Five-row addition. Check if this pushes the table over a page; if so, consider separating into a new "Phase 4 summary" table. |

---

## Chapter 5 — Phase 4 Additions

### Conclusions (Section 5.1)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.5.1 | Four new conclusion paragraphs appended after existing "Overall" paragraph | **AI ASSUMPTION** | Breaks the current final-paragraph-summary structure. **Decide:** keep "Overall" as truly final paragraph (move Phase 4 conclusions before it), or let "Overall" be an early summary with Phase 4 conclusions as the actual ending. |
| P4.5.2 | Paragraph heading "Retriever-specific query representation is critical" | **AI ASSUMPTION** | Uses the new coinage from P4.4.16. If you accept/reject that term there, apply same decision here. |
| P4.5.3 | Claim "This retriever-specific representation principle has practical implications for any multi-retriever pipeline" | **AI ASSUMPTION** | **Overreach** — generalises from a single experiment on one dataset to all multi-retriever pipelines. Recommend: "has practical implications for similar hybrid pipelines" or drop the generalisation. |
| P4.5.4 | Final headline number: "0.7137 nDCG@10 — a 54.5% improvement over BM25 alone and a 13.9% improvement over the no-QE hybrid baseline" | **GROUNDED (Experiments)** | Both improvements calculate correctly. |

### Challenges (Section 5.2)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.5.5 | Mark existing BM25 term-dilution challenge as RESOLVED in-place with a follow-up sentence | **AI ASSUMPTION** | Good approach. Keeps the historical narrative (the challenge was real at the time) while noting the resolution. |
| P4.5.6 | New challenge "First-pass quality dependence" added with Arabic homonym example | **GROUNDED (Experiments)** | From Type B regression analysis. |

### Recommendations (Section 5.3)

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.5.7 | Move Recommendation 2 (BM25 query repetition) and Recommendation 4 (Hybrid retrieval with QE) to a "now-implemented" note rather than deleting | **AI ASSUMPTION** | Good approach — preserves the historical story. **Alternative:** move them to Ch.4 as "these were listed as future work at the proposal stage and have since been completed". |
| P4.5.8 | Three new recommendations: (1) first-pass quality gate, (2) asymmetric expansion weighting, (3) CSQE with stronger dense retrievers (BGE-M3, mE5-large) | **AI ASSUMPTION** | Reasonable extensions. Recommendation 3 names specific models — **verify those are current state-of-the-art** at submission time; if newer models are published by Feb 2026, update. |
| P4.5.9 | Recommendation ordering: quality gate first (directly addresses Type B regressions) | **AI ASSUMPTION** | Ordering is editorial. Acceptable. |

---

## Abstract — Phase 4 Additions

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.A.1 | Replace closing result sentence with: "...achieved 0.7137 nDCG@10 on the MIRACL Arabic benchmark — a 54.5% improvement over the BM25 baseline and a 13.9% improvement over a strong no-QE hybrid system" | **AI ASSUMPTION** | Benchmark comparisons are correct. **"Strong" is editorial** — some reviewers may want you to qualify (e.g., "a competitive no-QE hybrid baseline"). Match your Ch.4 framing. |
| P4.A.2 | Replace only the closing sentence, keep rest of abstract unchanged | **AI ASSUMPTION** | **Risk:** the rest of the abstract still describes the previous best result (~0.62 from model comparison). Check that the abstract's methodology/results narrative is internally consistent. If earlier sentences claim "Aya Expanse 8B was the best-performing system (+23.5%)", that needs updating too — the Phase 4 numbers are now the lead finding. |
| P4.A.3 | Arabic abstract: new sentence with standard ASCII digits (0.7137, 54.5%) | **AI ASSUMPTION** | Decision was made conditional on "unless the existing Arabic abstract uses Eastern Arabic numerals". **Check the existing file first** — if it uses Eastern Arabic numerals (٠–٩) throughout, match that convention; if mixed, pick one and apply consistently. |
| P4.A.4 | Arabic translation quality for new sentence | **AI ASSUMPTION** | Same issue as A.5 in Part I — machine Arabic in academic register needs native speaker review. |

---

## Cross-Cutting — Phase 4 Additions

| # | Decision | Tag | Justification |
|---|----------|-----|---------------|
| P4.X.1 | Terminology choice: "Corpus-Steered Query Expansion (CSQE)" used uniformly | **GROUNDED (Literature)** | Matches Lei et al. 2024. |
| P4.X.2 | **New coinage: "retriever-specific query representation"** used in Ch.3 §3.8.3, Ch.4 §4.9.1, Ch.5 §5.1 | **AI ASSUMPTION** | Decide once (P4.4.16) and apply consistently or drop consistently. |
| P4.X.3 | **New coinage: "meta-description failure mode"** used in Ch.4 §4.10.1 | **AI ASSUMPTION** | Decide once (P4.4.22). |
| P4.X.4 | Use of project-internal phrase "Phase 4" in Ch.1 thesis layout | **AI ASSUMPTION — DO NOT KEEP** | Examiners don't know Phase 4. **Global find-and-replace before submission.** |
| P4.X.5 | All new tables caption format: caption ABOVE, `\label{tab:xxx}` below | **GROUNDED (Dr. Tahani)** | Standard. |
| P4.X.6 | References.bib additions: `lei_2024_csqe`, `bruch_2023_rrf`, `zhang_2024_mugi`, verify `zhang_2023_miracl` | **GROUNDED (Literature)** | **Verify the brief's proposed BibTeX entry for `zhang_2024_mugi` matches the actual publication** — EMNLP Findings 2024 is claimed but arxiv 2401.06311 may have been published elsewhere. Check. |
| P4.X.7 | Cross-reference labels added to READMEs per brief (23 new Ch.3 + Ch.4 labels) | **AI ASSUMPTION** | Large addition. Verify each label is actually used in the thesis (unused labels are harmless but look sloppy on review). |
| P4.X.8 | All numeric values taken verbatim from brief's Quick Reference block | **GROUNDED (Experiments)** | **Mohammed must sign off on the Quick Reference block being the single source of truth** — if any number there is wrong, it propagates everywhere. Spot-check 5-10 numbers against original experiment docs before thesis submission. |

---

---

## Priority Review Items

### MUST review before finalizing (could affect thesis correctness):

**From initial draft (Part I):**
1. **2.7** — Research gap claim ("none tested <7B on Arabic QE") — verify accuracy
2. **2.12** — BM25S parameter inconsistency between Ch.2 and Ch.3
3. **4.2** — Official mDPR baseline score verification
4. **4.13** — BM25 numbers for Osman's models — verify all were actually run
5. **4.16** — Assign experiment numbers to Osman's experiments
6. **A.5** — Arabic abstract quality review by native speaker
7. **2.15** — BibTeX citation keys must match `References.bib`
8. **1.3** — Research question wording

**From Phase 4 (Part II) — NEW, highest priority:**
9. **P4.4.20** — ⚠ CRITICAL: per-query error analysis uses Config C (0.6936), not Config A (0.7137). Decide disclosure/re-run strategy.
10. **P4.A.2** — Abstract internal consistency — earlier sentences may still describe pre-Phase-4 results.
11. **P4.X.4** — Remove all instances of "Phase 4" from thesis layout — internal-only terminology.
12. **P4.4.10** — Recall@100 value 0.9466 vs 0.9467 — choose one and apply thesis-wide.
13. **P4.3.15** — Verify CSQE temp=1.0 against actual exp_013 notebook config.
14. **P4.3.16** — Include the exact CSQE system prompt in Ch.3 §3.8 (for reproducibility).
15. **P4.X.6** — Verify `zhang_2024_mugi` BibTeX entry (publication venue).
16. **P4.X.8** — Spot-check 5-10 brief numbers against original experiment docs.
17. **P4.2.4** / **P4.2.5** — Verify the "asymmetric expansion in hybrid" gap has not been covered by post-2024 prior work.
18. **P4.A.3** — Arabic abstract numeral convention (Eastern Arabic vs ASCII).
19. **P4.A.4** — Native speaker review of new Arabic closing sentence.

### SHOULD review (editorial choices that affect thesis narrative):

**From initial draft (Part I):**
20. **1.2** — Three-gap problem framing
21. **4.5/5.2** — "Arabic benefits disproportionately" hypothesis — keep or weaken?
22. **4.7** — "Benchmark scores don't predict QE quality" — finding or observation?
23. **4.8/4.9** — Mechanistic explanations for Jais-2/Aya BM25 success
24. **5.3** — Which finding is "most practically significant"?
25. **5.5** — Was weak baseline intentional or pragmatic?
26. **A.4** — "Practical strategy" vs "promising strategy"

**From Phase 4 (Part II):**
27. **P4.1.1 / P4.1.3** — Objectives 6–8 wording: fix/investigation framing; retrospective-reconstruction risk.
28. **P4.3.13** — Ch.3 §3.8.3 states a hypothesis that was actually post-hoc. Soften.
29. **P4.4.16 / P4.X.2** — "retriever–query representation mismatch" / "retriever-specific query representation" — keep new terminology or use existing vocabulary.
30. **P4.4.22 / P4.X.3** — "meta-description failure mode" — name a mode based on one query?
31. **P4.4.7** — "Statistically indistinguishable" vs "numerically indistinguishable" for RRF vs CC.
32. **P4.4.9** — "Must surpass 0.6267" framing — keep or soften.
33. **P4.4.18** — Is Config A "THE key finding of the thesis" or one of several?
34. **P4.4.24** — "Dominant predictor" language without regression/ANOVA.
35. **P4.4.26** — Embed recommendations in Ch.4 §4.10.4 or move to Ch.5?
36. **P4.4.27** — Medium query-length row with "—" — populate or drop.
37. **P4.5.1** — Four new conclusion paragraphs: order relative to "Overall" paragraph.
38. **P4.5.3** — "Any multi-retriever pipeline" — overreach; soften.

### CAN defer (style preferences, low risk):

**From initial draft (Part I):**
39. **2.1–2.4** — Chapter 2 section structure
40. **2.11** — "Morphological gap" terminology
41. **X.5** — British vs American English
42. **5.6–5.9** — Recommendation ordering and content

**From Phase 4 (Part II):**
43. **P4.3.1** — Present two repetition families or only winning MuGI?
44. **P4.3.7** — Query assembly equation: simplify to k=1 or keep general?
45. **P4.3.12** — Config A/B/C naming vs. descriptive names.
46. **P4.4.1** — One 8-column table vs. two (fixed + adaptive).
47. **P4.4.23** — Three big-win example queries selected — are these the best illustrations?
48. **P4.4.28** — Does `tab:full_summary` fit on one page with 5 new rows?
49. **P4.5.7** — Moved recommendations: now-implemented note or Ch.4 placement?

---

## Instructions for Review Meeting

1. **Start with P4.4.20** — the Config C vs Config A error analysis provenance issue. This affects whether any of §4.10 can be written as the brief proposes, and it affects downstream conclusions in Ch.5.
2. **Then Part II MUST-review items (P4.x)** — these are new claims/numbers and carry more risk than the initial-draft items you've already seen once.
3. Go through the **MUST review** items from Part I next — still relevant, not yet resolved.
4. Discuss the **SHOULD review** items — these shape the thesis narrative. Note: several Phase 4 SHOULD items (P4.4.16, P4.4.22) involve new terminology the AI coined — decide up-front whether this thesis will introduce new terms or stay within established vocabulary.
5. For each item, decide: **Approve / Revise / Reject**.
6. After the review, update all chapters to reflect the decisions.
7. Pay special attention to items where the AI made **interpretive claims** (Part I: 4.5, 4.7, 4.8, 4.9, 5.2, 5.3; Part II: P4.4.3, P4.4.4, P4.4.8, P4.4.11, P4.4.12, P4.4.15, P4.4.17, P4.5.3) — these are the places where the thesis makes claims beyond what the raw data shows.

---

## Quick-Triage Summary of Phase 4 Items

| Severity | Count | Action |
|----------|-------|--------|
| ⚠ Critical (correctness risk) | 1 | P4.4.20 |
| High (verify before printing) | ~10 | P4.A.2, P4.X.4, P4.4.10, P4.3.15, P4.3.16, P4.X.6, P4.X.8, P4.2.4, P4.2.5, P4.A.3, P4.A.4 |
| Medium (editorial) | ~15 | P4.1.x, P4.3.13, new terminology items, narrative framing items |
| Low (style) | ~7 | table layout, naming conventions, ordering |

Total new Phase 4 items: **51** across Chapters 1–5, abstract, and cross-cutting.
