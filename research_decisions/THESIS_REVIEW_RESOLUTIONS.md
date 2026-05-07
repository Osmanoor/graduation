# Thesis Review — Resolutions Document

**Source:** Aggregated from 10 meeting transcripts (`meetings/23.1_2026.pt1.md`–`pt6.md`, `meetings/pt7.md`–`pt10.md`).
**Per-transcript working notes:** `meetings/analysis/pt1_notes.md` through `pt10_notes.md`.
**Original review document:** `research_decisions/THESIS_DRAFT_AI_DECISIONS_REVIEW.md`.
**Compiled:** 2026-05-06.

This document captures **decisions and discussion** for every item in the original review document that the team addressed across the 10 meetings. Each item is presented with: (a) the discussion summary, (b) the verdict (Approve / Revise / Reject / Defer), and (c) the source transcript(s).

---

## Standing Process Decisions

Set across the meetings; apply to the entire review and edit phase:

1. **Verdict per item** — every reviewable item gets one of: Approve / Revise / Reject / Defer-to-Supervisor / Verify.
2. **Honesty over narrative** — wherever the AI invented strategic rationales for what were actually constraints (mDPR weak baseline, "intentional" choices), prefer to soften or remove rather than defend a fabricated story under examination. Apply consistently throughout.
3. **AI-fabrication patterns** — five patterns identified to sweep for thesis-wide:
   - **Decorative citations** — citations inserted next to claims that the cited paper doesn't actually support (caught in 2.11).
   - **Cited-but-unread papers** — large surveys cited without verification of reading (caught in 2.14, Song & Zheng 2024).
   - **Fabricated rationales** — invented justifications never measured (caught in 3.9 "diminishing returns at 256", 3.10 "16x speedup").
   - **Decorative descriptors** — unverified model attributions (caught in 2.5 "GPT-OSS English-dominant").
   - **Statistical-test claims without tests** — wording "statistically X" when no test was run (caught in P4.4.7).
4. **Estimation-vs-measurement rule** — any time/runtime/speedup claim that came from estimation will be deleted; any such claim from actual cell output will be kept. Apply thesis-wide.
5. **"Phase 4" terminology purge** — global find-and-replace; no project-internal phasing terms in the thesis (P4.X.4).
6. **Brief-audit workstream** — the team has reduced confidence in the post-Phase-4 brief (P4.4.20 surfaced one major error). Branch a parallel Gemini chat to read the original experiment reports independently and produce a comparison thesis-update document.

---

## Chapter 2 — Theoretical Background and Literature Review

### Item 2.1 — Ch.2 organized into 4 main sections (Theoretical Background, Mathematical Models, Models Used, Related Work)
**Verdict:** **REVISE.**
**Discussion:** Osman raised that the AI's Ch.2 structure is missing a **dataset analysis** section. They had performed a research stream comparing roughly 8 candidate datasets before selecting MIRACL. That work is currently absent from Ch.2. Mohammed agreed: the Ch.2 structure should mirror the actual flow of tasks they executed.
**Action:** Add a dataset analysis section to Ch.2 (probably before "Models Used"). Re-point AI at the project's `tasks` file to ensure no other work-stream is silently dropped.
**Source:** pt1.

### Item 2.2 — Mathematical formulas placed in their own Section 2.2
**Verdict:** **REVISE.**
**Discussion:** Principle of separating math approved. Inconsistency: hybrid retrieval equation is currently inline in the theory section while BM25, Dense, and metrics live in §2.2. Hybrid is just as much a math model — should be moved to §2.2 for consistency.
**Action:** Move the hybrid retrieval equation out of theory and into §2.2 so all retrieval-method equations are co-located.
**Source:** pt1.

### Item 2.3 — Chapter Summary section (§2.5) with bullet points
**Verdict:** **DEFER TO SUPERVISOR.**
**Discussion:** Neither was sure whether to keep the chapter summary. Dr. Tahani didn't explicitly mention chapter summaries.
**Action:** Flag as a question for Dr. Tahani; check her recordings first before deciding. Keep summary in the draft as flagged-pending.
**Source:** pt1.

### Item 2.4 — Funnel structure for Related Work
**Verdict:** **APPROVE.**
**Discussion:** Osman: "ممتاز جداً" (excellent). No reservations.
**Source:** pt1.

### Item 2.5 — Described 11 models (10 evaluated + GPT-OSS)
**Verdict:** **APPROVE WITH FIX (and an open re-examination).**
**Discussion:** Initial discussion (pt1) decided to keep GPT-OSS and ALLaM since Dr. Tahani approved discussing failed models, and GPT-OSS is the only MoE in the comparison set (research value). However, the AI inserted a sentence claiming GPT-OSS is "English-dominant" — this descriptor is **not verified** in any docs. Later (pt4), Mohammed leaned toward **deleting GPT-OSS entirely** from the thesis if time permits.
**Action:**
1. Keep both GPT-OSS and ALLaM with honest "dropped due to X" framing in Ch.2 — for now.
2. Verify the "English-dominant" GPT-OSS claim before printing; if not supportable, soften or remove.
3. Re-decide whether to delete GPT-OSS entirely when revisiting Ch.2/Ch.4 model description sections (working preference: delete).
**Source:** pt1, pt4.

### Item 2.6 — IEEE format citations
**Verdict:** **APPROVE.** Dr. Tahani's instruction.
**Source:** pt1.

### Item 2.7 — Research gap: "none of these studies tested models smaller than 7B for zero-shot Arabic QE"
**Verdict:** **REVISE (multi-part) — DEFER TO SUPERVISOR for final framing.**
**Discussion:** The AI mis-framed the central problem statement as "do small (<7B) LLMs work for Arabic QE?" Both feel this is wrong. Their actual contribution is **broader**: they applied multiple QE approaches (Query2Doc / blind QE, CSQE, hybrid fusion with retriever-specific application) to improve Arabic RAG. Small models is a strength/bonus, not the primary contribution. Two framing options identified:
- **Option A (general):** "How can query enhancement improve Arabic RAG systems?" — covers all experiments naturally.
- **Option B (specific):** State as multiple sub-questions tied to each experiment.
Working preference: Option A.
Even if the framing is fixed, the literal "<7B never tested on Arabic QE" claim needs validation — new papers may have appeared.
**Action:**
1. Re-frame the problem statement to lead with QE for Arabic RAG; relegate "small models" to secondary novelty.
2. Take to Dr. Tahani: general vs specific problem statement preference.
3. Re-do literature search for any post-2024/2025 paper testing small (<7B) LLMs on Arabic QE; restructure gap claim accordingly.
4. Investigate whether the bachelor's thesis convention permits multiple research questions or requires a single problem statement.
5. Cascade fix into items 1.2, 1.3, 1.4, 1.5.
**Source:** pt1, pt2.

### Item 2.8 — HyDE, Query2Doc, GRF as the three main QE techniques
**Verdict:** **REVISE.**
**Discussion:** Literature too narrow. They had read papers on multiple QE families (expansion, rewriting, decomposition, abstraction) but only expansion + rewriting are mentioned. Decomposition and abstraction missing.
**Action:** Expand the QE techniques discussion to cover all four families with the papers actually read for each.
**Source:** pt2.

### Item 2.9 — Rewrite-Retrieve-Read as separate query rewriting category
**Verdict:** **APPROVE the categorization;** folded into 2.8 expansion.
**Source:** pt2.

### Item 2.10 — Arabic challenges section (morphology, diglossia, orthography, diacritics)
**Verdict:** **APPROVE content;** defer paragraph-vs-subsection format.
**Discussion:** Format observation: could be elevated to subsections (2.1.5.1, 2.1.5.2 …) but single-paragraph subsections look thin. Substantive observation: **Arabic challenges aren't tightly threaded into the methodology** — defense risk if examiners ask "how did this challenge inform your work?"
**Action:** Approve as-is; be ready in defense to explain why these challenges are in the thesis. Possibly tighten the connection in revision.
**Source:** pt2.

### Item 2.11 — "Morphological gap" terminology + irrelevant inserted citation
**Verdict:**
- Term: **APPROVE.**
- Citation: **REVISE / REMOVE.**

**Discussion:** The term "morphological gap" was approved as intuitive (Osman: "بديهي والله"). Separately, the AI inserted a citation (paper 12) right next to the morphological-gap discussion claiming the cited paper showed "linguistic properties affect RAG pipeline component selection." But this paper is about chunking and embedding-model selection, not QE. **Decorative-citation pattern** — first instance caught.
**Action:** Keep "morphological gap." Remove the paper-12 sentence (or replace with a citation that genuinely supports the morphological-gap claim). Sweep for similar misuses.
**Source:** pt2.

### Item 2.12 — BM25S parameter inconsistency (Ch.2 says k1=1.5, b=0.75; Ch.3 says k1=0.9, b=0.4)
**Verdict:** **VERIFY then REVISE.**
**Discussion:** Likely Ch.2 cites BM25S library defaults; Ch.3 reflects their actual configuration.
**Action:** Confirm which parameters were actually used. Make Ch.2 either say "BM25S defaults are k1=1.5, b=0.75 but we used k1=0.9, b=0.4" or just match Ch.3.
**Source:** pt2.

### Item 2.13 — 15+ papers in Related Work
**Verdict:** **APPROVE (implicit)** — flag for re-check during the citation audit (2.15).
**Source:** pt2.

### Item 2.14 — Song & Zheng 2024 cited as the QE taxonomy reference
**Verdict:** **INVESTIGATE then DECIDE.**
**Discussion:** **Cited-but-unread pattern** — first instance caught. The paper exists (arxiv) but it's a 107-page survey neither of them confidently read. Mohammed initially suspected hallucination; confirmed real.
**Action:** Either (a) actually read enough of Song & Zheng 2024 to defensibly cite it, or (b) replace with a paper they did read for the taxonomy framing.
**Source:** pt2.

### Item 2.15 — BibTeX citation keys may not match References.bib
**Verdict:** **REVISE — explicit AI task.**
**Discussion:** Mohammed explicitly addressed the AI: "task ليك يا AI" — when reading this transcript, audit every citation: verify keys exist, URLs resolve, and the cited paper actually says what the thesis claims.
**Action:** Full citation audit (key matching, URL validity, content matching) — explicit AI task.
**Source:** pt2.

---

## Chapter 3 — Methodology

### Item 3.1 — Methodology organization
**Verdict:** **APPROVE** (post-Phase 4 structure).
**Discussion:** Initial confusion ("where's corpus-steered?") resolved when they realized the item description was written before Phase 4 expansion. They walked the actual TOC and confirmed full order: dataset setup → baseline → error analysis → Query2Doc → model comparisons → parameter tuning → query repetition → hybrid → corpus-steered → per-query analysis.
**Source:** pt2.

### Item 3.2 — 1:1 mapping to Ch.4 results
**Verdict:** **APPROVE.**
**Source:** pt2.

### Item 3.3 — mDPR "intentionally selected as a weaker baseline"
**Verdict:** **REVISE.**
**Discussion:** **Honesty moment** — both admit this is **post-hoc**. Real reasons: (1) practical (existing MIRACL-compatible index for fast iteration); (2) genuine concern it might be too weak. Not a deliberate "headroom" choice.
**Action:** Drop the "intentionally weaker baseline" framing. Either (a) state factually: "mDPR was used because a MIRACL-compatible index was available; we acknowledge it sits at the weaker end of available retrievers"; or (b) just describe what was used without inventing a strategic rationale. Same decision applies to **item 5.5** in Ch.5.
**Source:** pt2, pt3.

### Item 3.4 — BM25S 96% of Pyserini performance
**Verdict:** **APPROVE.**
**Source:** pt3.

### Item 3.5 — Java 21/11 dependency conflict reason
**Verdict:** **APPROVE.**
**Source:** pt3.

### Item 3.6 — Error analysis thresholds (Failed <0.3, Mediocre 0.3–0.7, Successful ≥0.7)
**Verdict:** **REVISE.**
**Discussion:** Thresholds are arbitrary; no clear justification. Must be reconciled with the **different** thresholds used in the Phase 4 error analysis (Failure < 0.1, Big Win Δ > 0.3, Regression Δ < −0.1) — two threshold systems coexist in the thesis.
**Action:** Re-do the original error analysis with better-justified thresholds. Reconcile with Phase 4 framework so both are coherent.
**Source:** pt3.

### Item 3.7 — Query length buckets (Short 1–3, Medium 4–8, Long 9+ tokens)
**Verdict:** **REVISE.**
**Discussion:** Inconsistency: original error analysis uses 1–3 / 4–8 / 9+ in **tokens**; Phase 4 uses Short < 5 words / Medium 5–9 / Long ≥ 10 in **words**. Original buckets are too narrow ("1–3 tokens" is very short).
**Action:** Recalculate with consistent word-based buckets matching the Phase 4 analysis. Update §3.3 and downstream §4 sections. Reframe to emphasize "data-driven decisions" (the analysis motivated focusing on Query2Doc).
**Source:** pt3.

### Item 3.8 — System prompt for query expansion
**Verdict:** **APPROVE.**
**Source:** pt3.

### Item 3.9 — Max tokens 128 with claim "256 showed diminishing returns"
**Verdict:** **REVISE.**
**Discussion:** **Honesty moment** — they admit they made it up: "نجفناها أيوة" ("we just made it up"). Never measured the 256 quality; just dropped to 128 because 256 was slow.
**Action:** Either (a) state plainly: "128 was chosen for inference speed; we did not formally test 256 vs 128 quality"; or (b) run the comparison on Aya if time permits and update the justification with real data.
**Source:** pt3.

### Item 3.10 — "16x combined speedup" (8x batching × 2x token reduction)
**Verdict:** **REVISE.**
**Discussion:** **Honesty moment** — also fabricated. Real: 8 hours sequential → ~40 minutes after optimizations ≈ 12x, not 16x. The multiplicative breakdown was never measured.
**Action:** Replace "16x combined speedup" with what was actually observed: state the wall-clock change ("from ~8 hours sequential to ~40 minutes"), list contributing optimizations without claiming a precise per-optimization multiplier, and don't claim 16x. If anything, "approximately 12x wall-clock improvement."
**Source:** pt3.

### Item 3.11 — Temperature 0.7 vs 0.1 SILMA comparison
**Verdict:** **VERIFY then REVISE.**
**Discussion:** AI wrote "tested at 0.0 and 0.1" — the 0.0 is wrong. Likely 0.7 vs 0.1 (Mohammed thinks possibly 0.8).
**Action:** Confirm actual temperatures from SILMA notebook; correct text.
**Source:** pt3.

### Items 3.12, 3.13 — Work division and Table 3.2 model configs
**Verdict:** **APPROVE (implicit)** — confirmed grounded; not deeply reviewed.
**Source:** Implicit across pt3-pt4.

---

## Chapter 4 — Results and Discussion

### Item 4.1 — All numerical results
**Verdict:** **APPROVE.**
**Discussion:** Osman confirmed CLAUDE.md is the source of truth. Gemini check showed numbers correct.
**Source:** pt3.

### Item 4.2 — mDPR baseline 0.4993 reproduced "with less than 0.1% difference vs published 0.499"
**Verdict:** **REVISE.**
**Discussion:** Actually they reproduced **exactly** — both got 0.4993, the published paper just rounded. Not a 0.1% difference; a presentation/rounding artifact.
**Action:** Change framing to either "reproduced exactly (rounded paper value 0.499 = our 0.4993)" or just round their own number to 0.499 throughout.
**Source:** pt3.

### Item 4.3 — Percentage improvements
**Verdict:** **APPROVE.** Math straightforward; spot-check passed.
**Source:** pt3.

### Item 4.4 — BM25 degradation attributed to "term dilution" (Wang 2023)
**Verdict:** **APPROVE.** Solid grounding in Wang's Query2Doc paper; experiment confirmed.
**Source:** pt3.

### Item 4.5 — "Arabic benefits disproportionately from vocabulary expansion" hypothesis
**Verdict:** **REJECT / REMOVE.**
**Discussion:** Used to explain why their 3B model improved BM25 by +8.9% while Wang's 175B paper reported smaller improvements. **Comparison is invalid** — different model, dataset, language, baseline, margins. Both Mohammed and Osman: remove this hypothesis from §4 entirely. Same decision applies to **item 5.2** (Ch.5 conclusions) and to the abstract (item A.3).
**Source:** pt3.

### Item 4.6 — Model parameter count positively correlated with Dense improvement
**Verdict:** **REVISE.**
**Discussion:** Trend is real, especially clean within Qwen family. But cross-family comparisons confound size with generation. Restrict any correlation coefficient to Qwen family only (4 data points).
**Action:** Add a real Pearson/Spearman correlation coefficient restricted to Qwen family (Qwen 2.5-3B, Qwen3-4B, Qwen 2.5-7B, Qwen3-8B). Note the cross-generation confound for the broader claim.
**Source:** pt3.

### Item 4.7 — "Arabic NLP benchmark scores do not directly predict QE quality"
**Verdict:** **REVISE.**
**Discussion:** Like the finding (publishable observation). But the AI says "Arabic NLP benchmark" generically — needs to specify which (OALL? AraGen? AMMLU? SILMA?). Defensibility requires specificity.
**Action:** Specify the exact benchmark(s) being referenced and verify the comparison cited (Falcon-H1 vs Qwen 2.5 3B) is correct.
**Source:** pt3.

### Item 4.8 — Jais-2 BM25 success attributed to 150K Arabic-centric vocabulary
**Verdict:** **APPROVE as hypothesis** (not proven mechanism).
**Discussion:** Plausible. **Cross-cutting addition (Osman):** "BM25" vs "BM25S" naming — must add a notation note upfront clarifying that "BM25" in the thesis refers to BM25S with their specific configuration.
**Source:** pt3.

### Item 4.9 — Aya BM25 success attributed to multilingual training
**Verdict:** **APPROVE as hypothesis** (same standard as 4.8).
**Source:** pt3.

### Item 4.10 — Qwen generational comparison (training data 36T vs 18T)
**Verdict:** **APPROVE (implicit)** — covered indirectly under 4.6.
**Source:** pt3.

### Item 4.11 — Dense "universally benefiting" while BM25 "divergent"
**Verdict:** **APPROVE (implicit).**
**Source:** pt3.

### Item 4.12 — "Best Model Recommendations" section
**Verdict:** **REVISE.**
**Discussion:** Osman pushed back on universal recommendations. They found Aya best **for their use case**; declaring "use Aya for QE" is too strong.
**Action:** Phrase as "Aya was the strongest model in our experiments on MIRACL Arabic" rather than universal recommendation.
**Source:** pt3.

### Item 4.13 — BM25 results for Osman's models
**Verdict:** **APPROVE — no changes.**
**Discussion:** AI was fooled by Osman's terser documentation style. All numbers are real measurements.
**Source:** pt3.

### Item 4.14 — 12 tables total
**Verdict:** **REVISE.**
**Discussion:** Three concerns: (1) summary table missing things; (2) some tables overflow page width; (3) figures should be preferred over tables where possible.
**Action:** Audit each table for completeness, fix rendering, move data into figures where they're better suited.
**Source:** pt3.

### Item 4.15 — Two placeholder figures
**Verdict:** **REVISE — two-phase plan.**
**Discussion:** Comprehensive figure plan needed. Process: Mohammed drafts a figure-plan document (possibly compared with a Gemini-generated version); once descriptions are agreed, Claude implements them in LaTeX.
**Source:** pt3.

### Item 4.16 — Experiment numbers in Table 4.10
**Verdict:** **REVISE — DELETE all experiment numbers.**
**Discussion:** Experiment numbers are internal-only and unstable (even Mohammed mis-uses them). Refer to experiments by descriptive name throughout.
**Action:** Replace experiment numbers with descriptive names ("Aya experiment", "Query2Doc experiments", etc.). When in a paragraph dedicated to one experiment, just say "this experiment."
**Source:** pt3, pt4.

---

## Chapter 1 — Introduction

### Item 1.1 — Four introductory paragraphs (funnel structure)
**Verdict:** **DEFER TO SUPERVISOR / REVISE.**
**Discussion:** Inconsistency: Ch.1 funnels Arabic → RAG → QE → gap; Ch.2 funnels QE → Arabic. Different ordering of same elements. **Real issue:** Ch.1 narrative is **problem-driven** but their actual research process was **technology-driven** (look at QE techniques, see what works on Arabic). Misrepresents how they worked. Recall Dr. Tahani saying "you're engineers, technology-driven approach suits you" — but unclear if that applies to the narrative too.
**Action:** Ask Dr. Tahani: technology-driven narrative acceptable for the thesis? Working preference: switch to honest technology-driven narrative. Side decision: funnel structure should only apply to **Related Work (§2.4)**, not to Ch.1.
**Source:** pt3.

### Item 1.2 — Three-gap problem framing (retrieval, language, resource)
**Verdict:** **REVISE** (cascades from 2.7 and 1.1 decisions).
**Source:** Implicit pt1, pt3.

### Item 1.3 — Research question
**Verdict:** **REVISE** (cascades from 2.7 and 1.1 decisions).
**Discussion:** Must reflect the new general framing ("how can QE improve Arabic RAG"). Verify scope, model size language, and number-of-models phrasing.
**Source:** Implicit pt1, pt3.

### Item 1.4 — Five objectives mapping to Ch.3
**Verdict:** **APPROVE** (existing 5 + Phase 4 additions). AI invited to suggest more if applicable.
**Discussion:** Both acknowledge objectives are honestly retrofit from experiments — they accept this and will defend as such if challenged.
**Source:** pt4.

### Item 1.5 — Objective 4 says "ten" open-source LLMs
**Verdict:** **REVISE — multi-part.**
**Discussion:** Inconsistency: objective says 10, methodology says 10, results say 10, but Ch.2 literature review and research-gap section say 11. GPT-OSS was a fallback that got dropped.
**Action:**
1. Use **10** consistently in objectives, methodology, results, abstract.
2. Use **11** only in Ch.2 literature review where broader research is described — and label it ("we surveyed 11 candidate models, of which 10 were ultimately evaluated").
3. Re-decide GPT-OSS retention later (working preference: delete entirely).
4. Remove any AI-invented framing for *why* GPT-OSS was included (e.g., "English-dominant MoE evaluation").
5. Reframe so the model comparison reads as extensive validation, not the central contribution.
**Source:** pt4.

### Item 1.6 — No references in Chapter 1
**Verdict:** **APPROVE.** Dr. Tahani's instruction.
**Source:** pt4.

### Item 1.7 — Thesis Layout describing Ch.2–5
**Verdict:** **DEFER TO SUPERVISOR.**
**Discussion:** Currently paragraph form, "written weirdly." They lean toward bullet points for clarity.
**Action:** Ask Dr. Tahani: paragraphs vs bullets for the layout section.
**Source:** pt4.

---

## Chapter 5 — Conclusion and Recommendations

### Item 5.1 — Six conclusion topics
**Verdict:** **APPROVE** (with new investigation triggered).
**Discussion:** Praised overall. Notable findings highlighted: dense divergence behavior, query repetition fix, hybrid always-better, corpus-steered + retriever-specific representation. **NEW WORK ITEM:** investigate whether the retriever-specific representation principle generalises to vanilla Query2Doc (asymmetric blind Q2D in hybrid). If it does, conclusions strengthen significantly.
**Source:** pt4, pt7, pt8.

### Item 5.2 — "Arabic morphological richness benefits disproportionately" reappears in conclusions
**Verdict:** **REJECT / REMOVE** (matches 4.5 decision).
**Source:** pt3 (linked).

### Item 5.3 — "Most practically significant finding" wording
**Verdict:** **REVISE** (covered indirectly in P4.4.18 discussion — multiple key findings, not a single THE-key).
**Source:** pt7.

### Item 5.4 — Six challenges
**Verdict:** **APPROVE WITH ADDITIONS / REVISIONS** (per challenge):
1. **Resource constraints:** APPROVE.
2. **BM25 term-dilution:** APPROVE WITH REWORDING — acknowledge precedent in Wang 2023; frame resolution honestly.
3. **Dropped models (ALLaM in particular):** REVISE — explicitly note ALLaM's poor result was due to a sentencepiece tokenizer artifact (`▁` leakage rendered as dashes), not a fundamental model issue. Working decision: keep result as-is, disclose the artifact.
4. **Phase 4 wording:** REVISE — remove "implemented in Phase 4" language (matches P4.X.4).
5. **Dataset scope:** APPROVE WITH ADDITION — extend to mention MIRACL's lack of metadata, which blocked the chunking-aware extension.
6. **Single QE technique / weak baseline retriever:** APPROVE; ties to 5.5 / 3.3 decision.
**Source:** pt4.

### Item 5.5 — Weak baseline framed as deliberate
**Verdict:** **REVISE** (matches 3.3 decision exactly — drop the "intentional" framing).
**Source:** pt4.

### Item 5.6 — Eight recommendations ordering
**Verdict:** Subsumed by per-recommendation decisions.

### Item 5.7 — Recommendation 1 (knowledge-base-aware / chunking-aware QE)
**Verdict:** **APPROVE WITH ADDITION.**
**Discussion:** Was in their original plan but blocked by MIRACL's metadata gap. Acknowledge honestly: "we wanted to do this; we couldn't because of dataset constraints."
**Action:** Mention dataset selection criterion (suitable metadata) for future work. Note this was an originally planned direction blocked by MIRACL.
**Source:** pt4. **(Note: pt10 found knowledge-base-aware QE is mentioned earlier in the thesis — DELETE from Ch.5 if duplicated; keep only one occurrence.)**

### Recommendation 2 (BM25 query repetition)
**Verdict:** **REJECT / DELETE.** Already implemented in Phase 4.
**Source:** pt4.

### Recommendation 4 (Hybrid retrieval with QE)
**Verdict:** **REJECT / DELETE.** Already implemented in Phase 4.
**Source:** pt4.

### Item 5.8 — Recommendation 5 (dialectal Arabic)
**Verdict:** **APPROVE WITH SOFTENING.**
**Action:** State as "may help bridge MSA-dialect retrieval gaps; this requires evaluation on dialect-aware datasets."
**Source:** pt4.

### Item 5.9 — Recommendation 8 (publication)
**Verdict:** **REJECT / DELETE.** Too presumptuous for the AI to claim publication-readiness.
**Source:** pt4.

---

## Abstract

### Item A.1 — Abstract is 334 words
**Verdict:** **REVISE.**
**Discussion:** Too long. Excessive details (query counts, passage counts, error rates). Heavy focus on "small models" framing.
**Action:** Trim significantly. Rewrite from the new (corrected) problem statement after item 2.7 is settled. Target ~250 words. Verify Dr. Tahani's expected length.
**Source:** pt5.

### Item A.2 — Abstract structure (6 sentences)
**Verdict:** **APPROVE.**
**Source:** pt5.

### Item A.3 — Key numbers including 175B comparison
**Verdict:** **REVISE — REMOVE 175B comparison from abstract** (consistent with 4.5/5.2 decision).
**Source:** pt5.

### Item A.4 — Final sentence "practical strategy" vs "promising strategy"
**Verdict:** **APPROVE — keep "practical strategy."**
**Discussion:** Osman: "promising" implies novelty; "practical" claims efficacy — the technique exists, what we're showing is that it works in Arabic.
**Source:** pt5.

### Item A.5 — Arabic abstract translation
**Verdict:** **REVISE — sequenced.**
**Action:** Finalize English first; translate to Arabic with self-review (they are the native speakers); establish terminology convention (English-preserved technical terms like RAG, mDPR; Arabic for general concepts). Reference other Arabic NLP/RAG theses for precedent if findable.
**Source:** pt5.

---

## Cross-Cutting Decisions

### Item X.1 — Passive voice
**Verdict:** **APPROVE.** Dr. Tahani's instruction.
**Source:** pt5.

### Item X.2 — Cross-reference labels (33 / 26 / 29 counts)
**Verdict:** **DEFER TO SUPERVISOR / VERIFY.**
**Discussion:** Mohammed couldn't figure out what the AI meant by these counts. Osman: "this is exactly the kind of nitpicky detail Dr. Tahani notices."
**Action:** Flag as supervisor question. Independent grep for `\label`/`\ref` counts to verify the AI's numbers.
**Source:** pt5.

### Item X.3 — "query enhancement" not "query expansion" as umbrella term
**Verdict:** **APPROVE.**
**Source:** pt5.

### Item X.4 — Abbreviation handling
**Verdict:** **APPROVE.**
**Source:** pt5.

### Item X.5 — British English spelling
**Verdict:** **APPROVE.** ("Out of respect for Gordon" — University of Khartoum convention.)
**Source:** pt5.

### Item X.6 — Placeholder figures
**Verdict:** **APPROVE the placeholder approach;** real figures via the figure-plan workstream (item 4.15).
**Source:** pt5.

---

# PART II — PHASE 4 RESOLUTIONS

## Phase 4: Chapter 1 Additions

### Item P4.1.1 — Three new objectives appended (6, 7, 8)
**Verdict:** **APPROVE — with caveat that objectives are honestly retrofit.**
**Source:** pt4.

### Item P4.1.2 — Five-objective layout retained
**Verdict:** **APPROVE.**
**Source:** Implicit pt4.

### Item P4.1.3 — Objective 6 framing as "fix" vs "investigation"
**Verdict:** **APPROVE current framing.**
**Source:** Implicit pt4.

### Item P4.1.4 — Ch.3 layout description extended
**Verdict:** **APPROVE.** May tighten if too dense.
**Source:** Implicit pt5.

### Item P4.1.5 — "Phase 4" wording in Ch.4 layout description
**Verdict:** **REJECT / REMOVE** (matches P4.X.4 global purge).
**Source:** pt5.

---

## Phase 4: Chapter 2 Additions

### Item P4.2.1 — RRF equation with k=20 stated as "typical"
**Verdict:** **APPROVE.**
**Source:** pt5.

### Item P4.2.2 — CC equation with min-max normalization (hat notation)
**Verdict:** **DEFER — VERIFY consistency.**
**Action:** Confirm hat-notation consistency between Ch.2 §2.2 and Ch.3 §3.7.
**Source:** pt5.

### Item P4.2.3 — Lei et al.'s "30% mAP improvement over BM25" cited for CSQE
**Verdict:** **VERIFY then APPROVE.**
**Action:** Read Lei et al. 2024 again; confirm exact "30% improvement" claim and comparison setting.
**Source:** pt6.

### Item P4.2.4 — New research gap: asymmetric CSQE × hybrid not yet studied
**Verdict:** **APPROVE WITH FRAMING REVISION** ("not yet studied for Arabic").
**Action:** Osman to do literature search for any post-2024 work; if found, downgrade gap claim accordingly.
**Source:** pt6.

### Item P4.2.5 — Open question on asymmetric expansion in hybrid
**Verdict:** **APPROVE qualified to Arabic.**
**NEW EXPERIMENTAL TASK:** Test asymmetric vanilla Query2Doc (apply QE only to BM25 in hybrid; only to Dense; both) — if Config A pattern repeats, retriever-specific finding generalises.
**Source:** pt6, pt8.

---

## Phase 4: Chapter 3 Additions

### Item P4.3.1 — Two solution families for repetition (fixed Q2D + adaptive MuGI)
**Verdict:** **APPROVE.** Present both.
**Source:** pt6.

### Item P4.3.2 — Sweep ranges n ∈ {1, 3, 5, 7, 10}, β ∈ {2, 4, 6}
**Verdict:** **APPROVE.**
**Source:** pt6.

### Item P4.3.3 — Motivating prose (3-word vs 15-word query)
**Verdict:** **APPROVE.** Intuition ratified.
**Source:** pt6.

### Item P4.3.4 — No new LLM inference for repetition
**Verdict:** **APPROVE.**
**Source:** pt6.

### Item P4.3.5 — Runtime claim "~73 minutes on Colab CPU"
**Verdict:** **REVISE.**
**Discussion:** **NEW THESIS-WIDE RULE established here:** any time/runtime claim from estimation will be deleted; only cell-output measurements retained. This rule retroactively affects item 3.10.
**Action:** Replace "73 minutes" with actual cell-output runtime if extractable; otherwise drop the runtime claim.
**Source:** pt6.

### Item P4.3.6 — MuGI formula
**Verdict:** **APPROVE.**
**Source:** pt6.

### Item P4.3.7 — Query assembly equation (general k vs k=1 used)
**Verdict:** **APPROVE WITH ADDITION.**
**Action:** Keep general-k equation; add a sentence in main text stating "in our experiments k=1 (single pseudo-document)."
**Source:** pt6.

### Item P4.3.8 — Cross-reference RRF/CC equations from Ch.2
**Verdict:** **APPROVE.**
**Source:** pt6.

### Item P4.3.9 — α swept over {0.1,…,0.9}, k tested at {20, 60}
**Verdict:** **APPROVE.**
**Source:** pt6.

### Item P4.3.10 — Top-100 candidates retrieval depth
**Verdict:** **VERIFY then APPROVE.**
**Action:** Confirm in exp_012 notebook that top-100 was used (not top-1000).
**Source:** pt6.

### Item P4.3.11 — CSQE pipeline as two-stage
**Verdict:** **APPROVE.** Concatenation isn't a meaningful third stage.
**Source:** pt6.

### Item P4.3.12 — Config A/B/C naming convention
**Verdict:** **REVISE — global rename.**
**Action:** Rename throughout the thesis:
- Config A → BM25-only-expanded
- Config B → Dense-only-expanded
- Config C → Both-expanded
Verify B labeling matches the brief.
**Source:** pt6.

### Item P4.3.13 — Hypothesis stated in §3.8.3 (Dense degrades on long inputs)
**Verdict:** **REVISE.**
**Discussion:** **Honesty moment** — Osman: "we couldn't have known this in advance; Dense+CSQE alone actually improves." Pre-stating this as methodology is post-hoc.
**Action:** §3.8.3 wording becomes: "Three fusion configurations were tested to determine the optimal retriever–query assignment; whether expansion helps or hurts each retriever was left open." Save causal interpretation for Ch.4.
**Source:** pt6.

### Item P4.3.14 — α sweep "reconstructed from stored expansion pkls"
**Verdict:** **APPROVE.**
**Source:** Implicit.

### Item P4.3.15 — CSQE configuration (k=5, 2c+2b, α=4, temp=1.0)
**Verdict:** **VERIFY then APPROVE.** Cross-check temp=1.0 against actual exp_013 notebook.
**Source:** Brief priority item.

### Item P4.3.16 — CSQE system prompt missing in Ch.3
**Verdict:** **REVISE.**
**Action:** Print the exact CSQE system prompt in §3.8 for reproducibility.
**Source:** Brief priority item.

### Item P4.3.17 — Phase 4 error analysis thresholds (Failure < 0.1, Big Win Δ > 0.3, Regression Δ < −0.1)
**Verdict:** **REVISE** (per item 3.6 — reconcile threshold systems).
**Source:** Linked from pt3 / 3.6.

### Item P4.3.18 — First-pass quality definition ("any qrel > 0 in top-5")
**Verdict:** **VERIFY.** Confirm exact definition in code (any relevance ≥ 1 vs ≥ 2).
**Source:** Implicit.

### Item P4.3.19 — Manual regression classification (Type A / B / C)
**Verdict:** **REVISE** (per item P4.4.24 — questionable threshold rationale).
**Source:** pt10.

---

## Phase 4: Chapter 4 Additions

### Item P4.4.1 — Combined 8-column repetition table
**Verdict:** **APPROVE.** Keep combined for at-a-glance comparison.
**Source:** pt8.

### Item P4.4.2 — "Recovers all 9 previously degraded BM25 models"
**Verdict:** **REVISE — multi-part.**
**Discussion:** Factual correction: only **6/9 were below baseline at n=1**; 3 were already above. Fix wording.
**Action:**
1. Correct claim to "6 of 9 were below baseline at n=1; all 9 reached or exceeded baseline at appropriate repetition setting."
2. Add a recovery graph (line plot per model with horizontal baseline line). Add to figure-plan workstream.
**Source:** pt8.

### Item P4.4.3 — Interpretation about model size and optimal repetition
**Verdict:** **REJECT.** Differences (~0.001) too small to support size-based interpretation. All models had max_tokens=128 so "smaller models produce shorter docs" is also unsupported.
**Action:** Drop the size-based interpretation. Keep only the empirical observation that different models settle on different optima.
**Source:** pt8.

### Item P4.4.4 — Excessive repetition over-weights query tokens
**Verdict:** **APPROVE WITH FRAMING.**
**Action:** Keep as discussion (not proven mechanism). Possibly mention that going to n=20 would likely show clearer decline.
**Source:** pt8.

### Item P4.4.5 — Framing "query repetition was the missing ingredient"
**Verdict:** **REVISE.**
**Action:** Drop "missing ingredient." Replace with scientific phrasing: "for the originally underperforming systems, the deficiency was not in the model itself but in the absence of query repetition."
**Source:** pt8.

### Item P4.4.6 — +26.7% Aya β=2 BM25
**Verdict:** **APPROVE** (math verified).
**Source:** pt8.

### Item P4.4.7 — RRF k=20 and CC α=0.5 "statistically indistinguishable"
**Verdict:** **REVISE.**
**Action:** Change "statistically indistinguishable" to **"numerically indistinguishable"** (no statistical test was actually run). Apply this discipline thesis-wide.
**Source:** pt8.

### Item P4.4.8 — CC boundary interpretation (tie-breaking explanation)
**Verdict:** **REVISE.**
**Discussion:** Both admit they don't fully understand the CC tie-breaking mechanism. Also unclear whether min-max normalization or tie-breaking is the actual cause.
**Action:** Present as "a possible explanation is …" not as established mechanism. Investigate the actual tie-breaking behavior of the CC implementation if time allows.
**Source:** pt8.

### Item P4.4.9 — "0.6267 nDCG@10 hybrid baseline must be surpassed"
**Verdict:** **APPROVE with structural change.**
**Action:** Add hybrid (no QE) to the baselines section alongside BM25-alone and mDPR-alone, so it sits as a reference baseline.
**Source:** pt8.

### Item P4.4.10 — Recall@100 0.9466 vs 0.9467
**Verdict:** **REVISE — pick 0.9467 thesis-wide.**
**Source:** pt8.

### Item P4.4.11 — Dense degradation explanation (1500 chars / mDPR short queries)
**Verdict:** **REVISE.**
**Discussion:** Dense degradation is real and verified (Aya CSQE Dense 0.5915 vs Aya blind Q2D Dense 0.6164). The two specific explanatory claims need verification.
**Action:**
1. State degradation as fact.
2. Verify 1500-char claim by computing actual expansion-length statistics from saved CSQE outputs.
3. Verify and cite "mDPR trained on short queries" claim.
4. If both fail verification, present degradation without specific explanation.
**NEW EXPERIMENT:** run blind+blind hybrid (apply vanilla Q2D to BM25 and Dense in hybrid). Compare against Configs A/B/C — generalises the retriever-specific finding if Config A pattern holds.
**Source:** pt7, pt8.

### Item P4.4.12 — BM25 benefits from vocabulary breadth (blind > corpus on BM25)
**Verdict:** **REVISE the framing** to lead with complementarity, not "blind beats corpus."
**Action:** Reframe from "blind > corpus on BM25 alone" to "2 corpus + 2 blind exceeds either component alone, demonstrating they are complementary; on BM25 specifically, blind contributes more than corpus when used in isolation."
**Source:** pt7.

### Item P4.4.13 — Combined 2+2 exceeds both components individually
**Verdict:** **APPROVE.** Central result of the ablation. Numbers verified.
**Source:** pt7.

### Item P4.4.14 — α sweep "α=1 captures 98.9% of α=4" / "not critical"
**Verdict:** **APPROVE WITH MINOR SOFTENING.**
**Action:** Change "not critical" to "has minor effect in this configuration."
**Source:** pt7.

### Item P4.4.15 — "Config A is the winner despite weaker Dense input"
**Verdict:** **APPROVE.** Striking and accurate.
**Source:** Implicit.

### Item P4.4.16 — "Retriever-specific query representation" coinage
**Verdict:** **REVISE the explanation** (keep the term).
**Discussion:** Inconsistency: Dense + CSQE alone actually improves; "Dense degrades on long inputs" is too strong. Real mechanism is **fusion complementarity**.
**Action:** Reframe as "Dense + CSQE in fusion reduces complementarity with BM25 + CSQE; the two ranked lists become less divergent, lowering the fusion ceiling." Keep the umbrella term "retriever-specific query representation" but change the underlying explanation.
**Source:** pt7.

### Item P4.4.17 — RRF less discriminative reduces fusion ceiling
**Verdict:** **APPROVE WITH SCOPING** — present as local explanation for Config A > Config C, not general RRF principle.
**Source:** pt7.

### Item P4.4.18 — Config A as "key design finding of the thesis"
**Verdict:** **REVISE.**
**Action:** Soften "key design finding of the thesis" to "one of the principal findings, alongside [other findings]." Don't declare a single THE-key finding — risk under examination.
**Source:** pt7.

### Item P4.4.19 — Delta analysis table with 7 comparisons
**Verdict:** **APPROVE (implicit)** — verify each delta calculation when polishing.
**Source:** Implicit.

### Item P4.4.20 — ⚠ CRITICAL: Per-query error analysis Config C (0.6936) vs Config A (0.7137)
**Verdict:** **REVISE — full re-run for Config A.**
**Discussion:** Config A was computed in memory but never saved to disk; only Config C was saved. The brief honestly disclosed this. Mohammed wants a full re-run with personal vetting (not relying on the brief).
**Action:** Re-run the per-query error analysis end-to-end against Config A. Mohammed personally vets each step. Update §4.10 entirely.
**ALSO:** This triggered a broader brief-audit workstream (see Standing Process Decision #6).
**Source:** pt5, pt7, pt9.

### Item P4.4.21 — "257 of 258 are irretrievable"
**Verdict:** **REVISE — investigate dataset integrity FIRST.**
**Discussion:** **POSSIBLE DATASET BUG.** The 258 failure queries have nDCG@10 = exactly 0, implying relevant qrel documents are absent from the indexed Wikipedia corpus. If true, this is a preprocessing bug that could affect baselines.
**Action:**
1. Run a verification cell: check whether relevant qrel documents for the 258 failures are present in the indexed corpus.
2. If present → "irretrievable" claim is wrong; revise explanation.
3. If absent → investigate corpus preprocessing pipeline; possibly reindex and rerun baselines.
4. Don't print the "257 of 258" claim until verified.
**Source:** pt9.

### Item P4.4.22 — "Meta-description failure mode" for single query
**Verdict:** **REVISE — DEMOTE to illustrative example.** Don't name a failure mode after one query.
**Source:** pt7, pt9.

### Item P4.4.23 — Three big-win examples (الرباط المنصوري, John Dewey, Nicolas Boileau)
**Verdict:** **REVISE — multi-part.**
**Discussion:** Selection criterion is intuitiveness, not just statistical magnitude. الرباط المنصوري is the strongest example. John Dewey and Nicolas Boileau are uncertain.
**Action:**
1. Reformat the table: all English, side-by-side blind vs CSQE expansion content (not summaries).
2. Consider moving to appendix or providing short version Ch.4 + extended appendix.
3. **Keep الرباط المنصوري** as lead.
4. **Replace or verify** the other two examples; search for stronger candidates.
**Source:** pt9, pt10.

### Item P4.4.24 — "First-pass recall as the dominant predictor"
**Verdict:** **REVISE WITH VERIFICATION.**
**Discussion:** Mohammed found the analysis methodology questionable: the AI uses BM25 baseline > 0.3 as "well handled" but average baseline is 0.6–0.7. Also no formal regression was actually run.
**Action:**
1. Soften "dominant predictor" to "the largest observed modulator."
2. Verify the 0.3 threshold rationale; if undefendable, change or describe descriptively.
3. Keep the two recommendations (first-pass quality gate, asymmetric expansion weighting) but move to Ch.5 (per P4.4.26).
4. Don't oversell the analysis; present as exploratory observation that motivates two specific improvements.
**Source:** pt10.

### Item P4.4.25 — Arabic regression example (ما هو التطرف → لهجة جنوبية)
**Verdict:** **VERIFY then APPROVE.** Confirm the actual top-1 retrieval for this query.
**Source:** pt10.

### Item P4.4.26 — Recommendations embedded in §4.10.4
**Verdict:** **REVISE — move to Ch.5.**
**Action:**
1. Move first-pass quality gate and asymmetric expansion weighting to Ch.5.
2. Sweep Ch.5 for duplicates: knowledge-base-aware QE is mentioned earlier — DELETE from Ch.5.
3. Keep multi-stage QE, few-shot/CoT prompting, the two new ones, and stronger-retrievers as Ch.5 recommendations.
4. Reorder so each appears once with logical sequence.
**Source:** pt9, pt10.

### Item P4.4.27 — Medium query-length row with "—"
**Verdict:** **REVISE.** Either populate with actual data or drop the row entirely.
**Source:** Brief recommendation, implicit.

### Item P4.4.28 — Plan to add Phase 4 rows to Table 4.10
**Verdict:** **REVISE — structural fix.**
**Action:**
1. Move summary table to end of Ch.4 (or to appendix) — never in the middle.
2. Move "Overall" paragraph to actual end of Ch.5; reorder content so the strongest summary closes the chapter.
3. Combine Phase 4 rows into one summary table provided no page overflow; if overflow, split but keep adjacent.
**Source:** pt10.

---

## Phase 4: Chapter 5 Additions

### Item P4.5.1 — Four new conclusion paragraphs after "Overall"
**Verdict:** **REVISE** (per P4.4.28 — structural fix; "Overall" should be the actual closing paragraph or be repositioned).
**Source:** pt10.

### Item P4.5.2 — "Retriever-specific query representation is critical" heading
**Verdict:** **APPROVE the heading;** reframe meaning per P4.4.16.
**Source:** pt10.

### Item P4.5.3 — "Practical implications for any multi-retriever pipeline"
**Verdict:** **REVISE.** Soften: "has practical implications for similar hybrid pipelines" or drop the generalisation.
**Source:** pt10.

### Item P4.5.4 — 0.7137 / 54.5% / 13.9% headline numbers
**Verdict:** **APPROVE** (math verified).
**Source:** pt10.

### Item P4.5.5 — BM25 term-dilution challenge marked RESOLVED in-place
**Verdict:** **APPROVE** — good narrative move.
**Source:** pt10.

### Item P4.5.6 — New challenge "First-pass quality dependence"
**Verdict:** **APPROVE.**
**Source:** pt10.

### Item P4.5.7 — Move Recommendations 2 and 4 to "now-implemented" note
**Verdict:** **SUPERSEDED — DELETE entirely** (per pt4 decision on Recs 2 and 4).
**Source:** pt4, pt10.

### Item P4.5.8 — Three new recommendations (first-pass gate, asymmetric expansion, stronger retrievers)
**Verdict:** **APPROVE** all three.
**Action:** Verify BGE-M3 / mE5-large are still SOTA at submission time; update if newer models exist.
**Source:** pt4, pt10.

### Item P4.5.9 — Recommendation ordering (quality gate first)
**Verdict:** **APPROVE.**
**Source:** pt10.

---

## Phase 4: Abstract Additions

### Item P4.A.1 — Replace closing sentence with 0.7137 + 54.5% + 13.9%
**Verdict:** **APPROVE the numbers.** Wording "strong" may be softened to "competitive."
**Source:** Implicit pt5/pt10.

### Item P4.A.2 — Replace only closing sentence; rest unchanged
**Verdict:** **REVISE — full abstract rewrite needed** (per A.1 / 2.7 — abstract regenerated from corrected problem statement).
**Source:** pt5.

### Item P4.A.3 — Arabic abstract uses ASCII numerals
**Verdict:** **VERIFY.** Check existing Arabic abstract for numeral convention; match it.
**Source:** Implicit pt5.

### Item P4.A.4 — Arabic translation native review
**Verdict:** **REVISE** (per A.5 from Part I).
**Source:** Implicit pt5.

---

## Phase 4: Cross-Cutting

### Item P4.X.1 — CSQE terminology consistent
**Verdict:** **APPROVE.**
**Source:** pt6.

### Item P4.X.2 — "Retriever-specific query representation" coinage
**Verdict:** **APPROVE the term;** reframe meaning per P4.4.16.
**Source:** pt7, pt10.

### Item P4.X.3 — "Meta-description failure mode" coinage
**Verdict:** **REJECT** (per P4.4.22 — demote to illustrative example).
**Source:** pt7, pt9.

### Item P4.X.4 — "Phase 4" project-internal terminology in thesis
**Verdict:** **REJECT — global purge.**
**Source:** pt5, pt6.

### Item P4.X.5 — Table caption format
**Verdict:** **APPROVE.**
**Source:** pt10.

### Item P4.X.6 — References.bib additions
**Verdict:** **VERIFY each entry,** especially `zhang_2024_mugi` (verify EMNLP Findings 2024 venue).
**Source:** Brief priority item.

### Item P4.X.7 — Cross-reference labels added (23 new)
**Verdict:** **VERIFY usage** — confirm each label is actually used.
**Source:** Brief priority item.

### Item P4.X.8 — Quick Reference numbers as single source of truth
**Verdict:** **REVISE.** Spot-check 5–10 numbers against original experiment docs (matches the brief-audit workstream).
**Source:** pt5.

---

# CONSOLIDATED ACTION ITEMS

## A. New Experimental Tasks Identified

| Task | Priority | Reference |
|------|----------|-----------|
| **Asymmetric vanilla Query2Doc in hybrid** (apply Q2D only to BM25, only to Dense, both — parallel to Config A/B/C) | HIGH if time allows | P4.2.5, P4.4.11 (pt6, pt8) |
| **256 vs 128 max_tokens comparison** on Aya | LOW (do if time) | 3.9 (pt3) |
| **Re-run per-query error analysis for Config A** (replaces Config C) | HIGH | P4.4.20 (pt5, pt7, pt9) |
| **Verify dataset integrity:** check whether relevant qrel documents for 258 failure queries are in indexed corpus | CRITICAL — blocks P4.4.21 | pt9 |
| **Re-do original error analysis with consistent buckets/thresholds** (matches Phase 4) | MEDIUM | 3.6, 3.7 (pt3) |

## B. Verification Queue (small fact-checks)

| Item | What to verify | Reference |
|------|---------------|-----------|
| 2.5 | "GPT-OSS English-dominant" claim | pt1 |
| 2.7 | Literature search for new <7B Arabic QE papers | pt1 |
| 2.12 | Actual BM25S parameters used in experiments | pt2 |
| 2.14 | Read Song & Zheng 2024 or replace citation | pt2 |
| 2.15 | Full citation audit (keys, URLs, content) | pt2 |
| 3.11 | Actual SILMA temperatures tested (0.7? 0.8?) | pt3 |
| 4.7 | Specify which Arabic NLP benchmark is being claimed | pt3 |
| P4.2.3 | Lei et al. 2024 "30% mAP improvement" exact claim | pt6 |
| P4.2.4 | Literature search for asymmetric CSQE × hybrid prior work | pt6 |
| P4.3.10 | Top-100 vs top-1000 retrieval depth in exp_012 | pt6 |
| P4.3.15 | CSQE temp=1.0 in exp_013 notebook | Brief |
| P4.3.18 | First-pass quality definition (qrel ≥ 1 vs ≥ 2) | Brief |
| P4.4.10 | Recall@100 = 0.9467 (not 0.9466) thesis-wide | pt8 |
| P4.4.11 | CSQE expansion length ≈ 1500 chars (compute) | pt7 |
| P4.4.11 | mDPR trained on short queries (cite source) | pt7 |
| P4.4.21 | 258 failure queries inspection (exhaustive vs sampled) | pt7 |
| P4.4.23 | Three big-win examples accuracy + find better candidates | pt10 |
| P4.4.24 | 0.3 threshold rationale for "BM25 well handled" | pt10 |
| P4.4.25 | "ما هو التطرف" actually retrieves dialect content | pt10 |
| P4.X.6 | `zhang_2024_mugi` BibTeX (EMNLP Findings 2024 venue) | Brief |
| P4.X.7 | Each cross-reference label is actually used | Brief |
| P4.X.8 | Spot-check 5–10 brief numbers against experiment docs | Brief |

## C. Supervisor Questions Accumulated (for next Dr. Tahani meeting)

| # | Question | Source |
|---|---------|--------|
| Q1 | Should the thesis include a Chapter Summary section? (item 2.3) | pt1 |
| Q2 | Problem statement: general ("how can QE improve Arabic RAG") or specific (sub-questions per experiment)? (item 2.7) | pt1 |
| Q3 | Is a technology-driven narrative acceptable for Chapter 1? (item 1.1) | pt3 |
| Q4 | Thesis Layout section: paragraphs or bullet points? (item 1.7) | pt4 |
| Q5 | Abstract length expectation: 1 page or shorter? (item A.1) | pt5 |
| Q6 | What does "33 cross-reference labels in Ch.2" mean — internal labels or citation count? (item X.2) | pt5 |

## D. Cross-Cutting Tasks (sweeps)

| Sweep | What to do | Reference |
|-------|-----------|-----------|
| Decorative-citation sweep | Find all citations near claims; verify each cited paper actually supports the claim | 2.11 pattern |
| Fabricated-rationale sweep | Find any precise multiplier/threshold/"X tested vs Y" claim; verify or remove | 3.9, 3.10, P4.3.5 pattern |
| Decorative-descriptor sweep | Verify model attributions ("English-dominant", "Arabic-centric vocabulary", etc.) against official sources | 2.5 pattern |
| Statistical-test sweep | Replace "statistically X" with "numerically X" wherever no test was run | P4.4.7 pattern |
| Estimation-vs-measurement sweep | Delete all estimated time/runtime/speedup claims; keep only cell-output measurements | 3.10, P4.3.5 |
| "Phase 4" terminology purge | Global find-and-replace; remove all instances of "Phase 4" | P4.X.4 |
| Experiment-number purge | Remove all experiment numbers from the thesis; replace with descriptive names | 4.16 |
| BM25 vs BM25S notation | Add notation note upfront ("BM25 in this thesis = BM25S with [config]") | 4.8 |
| 0.4993 vs 0.499 / 0.9466 vs 0.9467 | Pick one of each; apply consistently thesis-wide | 4.2, P4.4.10 |
| Config A/B/C → descriptive names | Global rename (BM25-only-expanded / Dense-only-expanded / Both-expanded) | P4.3.12 |
| Recommendation deduplication | Sweep Ch.5; keep each recommendation once | P4.4.26 |
| Citation audit | Match every BibTeX key against References.bib; verify URLs and content | 2.15 |

## E. Items Pending Final Pass

These items were not fully closed in any transcript and need attention:

- **Final Chapter 5 walkthrough** — pt10 ended before Mohammed completed his Ch.5 review. Schedule for next session.
- **Final figure plan** — figure descriptions to be drafted (Mohammed primary, possibly with Gemini comparison) before Claude implements.
- **GPT-OSS retain-or-delete final decision** — working preference is delete; deferred to Ch.2/Ch.4 model-section pass.
- **§4.10 keep-or-delete decision** — depends on outcome of dataset integrity investigation (P4.4.21).

---

# Index

- **Original review document:** `research_decisions/THESIS_DRAFT_AI_DECISIONS_REVIEW.md` (492 lines, 51 Phase-4 items + 49 Part-I items + 6 cross-cutting + 5 abstract = ~111 review items).
- **Per-transcript notes:** `meetings/analysis/pt1_notes.md` through `pt10_notes.md`.
- **Items addressed in this resolution document:** ~110 (essentially full coverage).
- **Items pending re-examination:** Ch.5 deep dive (Mohammed flagged unfinished business in pt10).

**END OF RESOLUTIONS DOCUMENT.**
