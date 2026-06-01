# Thesis Next-Steps — Task List

**Source documents (read these first if picking up in a new chat):**
- `research_decisions/THESIS_REVIEW_RESOLUTIONS.md` — full per-item decisions with discussion + verdicts.
- `meetings/analysis/pt1_notes.md` through `pt10_notes.md` — per-transcript working notes.
- `research_decisions/THESIS_DRAFT_AI_DECISIONS_REVIEW.md` — original review document with item numbers.
- `University_of_Khartoum__EEE_bachelor_s_thesis_template/` — the LaTeX thesis source (chapters live here).

**User-set priority order (from this conversation):**
1. **Workstream 1 — Error Analysis** is **PRIORITY**, do first.
2. **Workstream 8 — Experimental backlog** is "if time permits" — do only after the rest is finalized.
3. The other workstreams (2–7) run in parallel and are normal-priority.

**Task tags used:**
- `[EDIT]` — direct text edit; can be done from the resolutions doc without re-reading the thesis section
- `[REREAD]` — need to read the relevant thesis section before editing
- `[VERIFY]` — fact-check against notebook/paper/data; outcome may flip the decision
- `[RESEARCH]` — literature search or external lookup
- `[EXPERIMENT]` — run a new experiment in a notebook
- `[ASK]` — supervisor question; do not decide unilaterally
- `[SWEEP]` — thesis-wide pattern audit (read every chapter)
- `[DECIDE]` — judgement call still pending; needs Mohammed/Osman to settle

---

## Workstream 1 — Error Analysis (PRIORITY — do first)

> User decision: prioritize this workstream over experimental tasks. Get §3.3 and §4.10 to a final state before touching the experimental backlog.

### Task 1.1 — Verify dataset integrity (BLOCKING — do this very first)
- **Tags:** `[VERIFY]` `[EXPERIMENT]`
- **Source:** P4.4.21 (pt9)
- **What:** Run the AI-proposed verification cell that checks whether the 258 failure queries' relevant qrel documents are actually present in the indexed Wikipedia corpus.
- **Outcome paths:**
  - **If documents ARE present** → "irretrievable" claim is wrong; the failures are genuine retrieval failures. Update §4.10 wording accordingly. Continue to Task 1.2.
  - **If documents are NOT present** → there's a corpus preprocessing bug. Investigate the pipeline (deduplication, length filter, encoding). Possibly need to reindex and rerun **all baselines** — this is a much larger remediation. **STOP and consult before proceeding** if this happens.
- **Why first:** the outcome of this changes how Tasks 1.2 and 1.3 should be written. It also has the largest blast radius.

### Task 1.2 — Re-run the original error analysis with consistent buckets/thresholds
- **Tags:** `[EXPERIMENT]` `[REREAD]`
- **Source:** items 3.6, 3.7 (pt3)
- **What:**
  1. Recompute the original error analysis with **word-based query length buckets** (Short < 5 words, Medium 5–9, Long ≥ 10) — match the Phase 4 framework, not the original 1–3 / 4–8 / 9+ tokens.
  2. Choose better-justified absolute thresholds (or eliminate fixed thresholds and present the analysis distributionally).
  3. Files are saved in Drive; recalculation is cheap.
- **Where in thesis:** §3.3 (methodology — Error Analysis section), and downstream §4 sections that reference these numbers.
- **Outcome:** updated tables and any prose that cites the bucket counts or thresholds.

### Task 1.3 — Re-run per-query error analysis for Config A (replaces Config C analysis)
- **Tags:** `[EXPERIMENT]` `[REREAD]`
- **Source:** P4.4.20 (pt5, pt7, pt9)
- **What:** Full re-run of the per-query analysis from raw Config A outputs. Mohammed personally vets each step rather than relying on the brief.
- **Where in thesis:** §4.10 entirely. Replace all Config C references with Config A. Re-do the failure-mode analysis, recovery rate (currently 56.8% improved by CSQE), and first-pass dependence numbers (currently 0.8877 vs 0.5814).
- **Dependencies:** Task 1.1 outcome (if dataset issue is real, this needs to wait for reindexing).

### Task 1.4 — Reconcile threshold systems thesis-wide
- **Tags:** `[SWEEP]` `[EDIT]`
- **Source:** items 3.6 + P4.3.17 (pt3, pt7 implicit)
- **What:** Currently §3.3 uses absolute thresholds (Failed < 0.3 / Mediocre / Successful) and §3.9 uses paired-comparison thresholds (Failure < 0.1 / Big Win / Regression). Either:
  - Choose one system and apply uniformly, OR
  - Keep both with explicit signposting that they answer different questions (absolute success rating vs pairwise comparison magnitude).
- **Where in thesis:** §3.3 and §3.9; verify §4 sections that reference either.

---

## Workstream 2 — Thesis-wide sweeps (no per-section reading; global edits)

> These are mechanical edits applied across the whole thesis. Each can be done as a single pass.

### Task 2.1 — Purge "Phase 4" terminology
- **Tags:** `[SWEEP]` `[EDIT]`
- **Source:** P4.X.4 (pt5, pt6)
- **What:** Global find-and-replace. Remove all instances of "Phase 4" from chapters, layout, captions, and §4.6/4.10 boilerplate. Replace with neutral phrasing ("subsequent experiments", "the extended experimental phase", or simply nothing if removable).

### Task 2.2 — Purge experiment numbers
- **Tags:** `[SWEEP]` `[EDIT]`
- **Source:** item 4.16 (pt3, pt4)
- **What:** Remove all experiment-number references (exp_005, exp_013, etc.) from the thesis text and tables. Replace with descriptive names ("Aya experiment", "Query2Doc experiment", "BM25 repetition experiment"). When in a paragraph dedicated to one experiment, just say "this experiment."

### Task 2.3 — Establish BM25 / BM25S notation
- **Tags:** `[EDIT]`
- **Source:** item 4.8 (pt3)
- **What:** Add a single notation note at first mention (probably end of §2.2 or beginning of §3.2): "Throughout this thesis, 'BM25' refers to the BM25S implementation with [k1=X, b=Y]." Then use "BM25" generically thereafter. Eliminates the BM25-vs-BM25S confusion.
- **Depends on:** item 2.12 verification of which parameters were actually used.

### Task 2.4 — Rename Config A/B/C → descriptive names
- **Tags:** `[SWEEP]` `[EDIT]`
- **Source:** P4.3.12 (pt6)
- **What:** Global rename throughout the thesis:
  - Config A → **BM25-only-expanded** (CSQE applied to BM25; Dense uses raw query)
  - Config B → **Dense-only-expanded** (Dense uses CSQE; BM25 uses raw query) — verify B labeling matches the brief
  - Config C → **Both-expanded** (CSQE applied to both retrievers)
  - Apply in §3.8.3, §4.9, §5.1, abstract, all tables, all cross-references.

### Task 2.5 — Numeric consistency: 0.4993 vs 0.499; 0.9466 vs 0.9467
- **Tags:** `[SWEEP]` `[EDIT]`
- **Source:** items 4.2 + P4.4.10 (pt3, pt8)
- **What:**
  - mDPR baseline: pick **0.499** (round their value to match published) OR explicitly state "reproduced exactly; the published paper reports 0.499 = our 0.4993 rounded." Apply consistently.
  - Recall@100 hybrid: pick **0.9467** (per pt8 decision); apply across all tables, abstract, and downstream references.

---

## Workstream 3 — AI-pattern audits (sweeps that need thesis reading)

> These five patterns were caught in specific items but likely repeat elsewhere. Each requires reading the relevant chapter(s) to find more instances.

### Task 3.1 — Decorative-citation audit
- **Tags:** `[SWEEP]` `[REREAD]` `[VERIFY]`
- **Source:** item 2.11 pattern (pt2)
- **What:** Read every citation in Ch.2 (and any literature-citing parts of Ch.4/Ch.5). For each, verify the cited paper actually supports the surrounding claim. Remove or replace decorative citations. Known instance: paper-12 next to morphological-gap (already on the edit list).

### Task 3.2 — Fabricated-rationale audit
- **Tags:** `[SWEEP]` `[REREAD]` `[VERIFY]`
- **Source:** items 3.9, 3.10, P4.3.5 pattern (pt3, pt6)
- **What:** Read Ch.3 looking for any precise multiplier, threshold, or "X tested vs Y" claim. For each, verify it was actually measured. Examples already known: "256 diminishing returns" (3.9), "16x speedup" (3.10), "73 min on Colab" (P4.3.5). Sweep for siblings.

### Task 3.3 — Decorative-descriptor audit (model attributions)
- **Tags:** `[SWEEP]` `[REREAD]` `[VERIFY]`
- **Source:** items 2.5, 4.8, 4.9 pattern (pt1, pt3)
- **What:** Read Ch.2 §2.4 (Models Used) and Ch.4 §4.5 (model results discussion). For each model, verify attributions like "English-dominant", "Arabic-centric vocabulary", "purpose-built multilingual training" against the official model card or technical report. Soften unverifiable claims.

### Task 3.4 — Statistical-test wording sweep
- **Tags:** `[SWEEP]` `[EDIT]`
- **Source:** P4.4.7 pattern (pt8)
- **What:** Find every "statistically X" / "statistically significant" / "indistinguishable" instance. Replace with "numerically X" wherever no statistical test was actually run. Apply uniformly.

### Task 3.5 — Estimation-vs-measurement sweep
- **Tags:** `[SWEEP]` `[EDIT]`
- **Source:** items 3.10, P4.3.5 pattern (pt3, pt6)
- **What:** Find every time/runtime/speedup claim. Delete estimates; keep only measurements with verifiable cell-output sources. Already known instances (3.10, P4.3.5) handled in Workstream 5; sweep for unrecorded siblings.

---

## Workstream 4 — Verifications (small fact-checks)

> Each is a single lookup or computation. Outcome may flip a decision.

> **✅ COMPLETED 2026-05-30, team-reviewed 2026-05-31 — full results + meeting notes in `research_decisions/WS4_VERIFICATION_REPORT.md`.**
> Headlines: 4.5 VERIFIED, keep as-is (30% is real on TREC DL19 **mAP**: BM25 30.1 → CSQE Llama2-7B 39.1, Table 7 — note it's mAP not nDCG);
> 4.4 → **adopt OALL** as base benchmark + standardise generic "Arabic NLP benchmark" → OALL **thesis-wide [SWEEP]** (keep Ch.2 per-model scores & MIRACL-dataset mentions); 4.15 NEEDS EDIT (MuGI + `lei_2024_csqe` title/authors fabricated — papers were read, only metadata wrong → escalate 6.4);
> 4.12 → keep الرباط المنصوري, **drop John Dewey** (blind was correct), **fix Boileau** description (businessman→computer scientist), find 3 better examples;
> 4.13 → reframe to the **general Type B** "first-pass poisoning" mode (928 ماهو-homonym, 11371 name-homonym, 11739 wrong-entity); keep ماهو التطرف as one illustration; regression bucket tables fixed (A≥0.3 / B<0.1 / C 0.1–0.3, no double-listing);
> 4.11 → **PARTIAL** (irretrievability pending WS1 integrity check); 4.16 → only **table/figure** labels need fixing (section labels harmless);
> 4.17 → Config-A/C naming + Config-A error-analysis re-run assigned to **WS1.3**.

| Task | What to verify | Source |
|------|---------------|--------|
| 4.1 | "GPT-OSS English-dominant" claim — check official model card | item 2.5 |
| 4.2 | Actual BM25S parameters used in experiments (k1=1.5/b=0.75 vs k1=0.9/b=0.4) | item 2.12 |
| 4.3 | Actual SILMA temperatures tested (0.7? 0.8? — not 0.0) | item 3.11 |
| 4.4 | Specify which Arabic NLP benchmark is being claimed in 4.7 (OALL? AraGen? AMMLU?) | item 4.7 |
| 4.5 | Lei et al. 2024 "30% mAP improvement over BM25" exact claim and benchmark setting | P4.2.3 |
| 4.6 | Top-100 vs top-1000 retrieval depth in exp_012 | P4.3.10 |
| 4.7 | CSQE temp=1.0 in exp_013 notebook | P4.3.15 |
| 4.8 | First-pass quality definition (qrel ≥ 1 vs ≥ 2) | P4.3.18 |
| 4.9 | CSQE expansion length ≈1500 chars — compute from saved CSQE outputs | P4.4.11 |
| 4.10 | mDPR trained on short queries — find a citable source | P4.4.11 |
| 4.11 | 258 failure queries inspection — exhaustive or sampled? | P4.4.21 |
| 4.12 | Three big-win example accuracy (الرباط المنصوري, John Dewey, Nicolas Boileau) — query, blind output, CSQE output | P4.4.23 |
| 4.13 | "ما هو التطرف" actually retrieves dialect content (Type B example) | P4.4.25 |
| 4.14 | 0.3 threshold rationale for "BM25 well handled" in regression analysis | P4.4.24 |
| 4.15 | `zhang_2024_mugi` BibTeX entry — is the EMNLP Findings 2024 venue claim correct? | P4.X.6 |
| 4.16 | Each cross-reference label (23 new in Ch.3 + Ch.4) is actually used | P4.X.7 |
| 4.17 | Spot-check 5–10 numbers in the brief's Quick Reference block against original experiment docs | P4.X.8 |

---

## Workstream 5 — Per-item rewrites (read section, then edit)

> The bulk of the editing work. Each item lives in a specific chapter section.

### 5.A — Chapter 2 rewrites

- **5.A.1** `[REREAD][EDIT]` Add **dataset analysis section** to Ch.2 (before Models Used). Cover the ~8 datasets evaluated and why MIRACL was chosen. — *item 2.1, pt1*
- **5.A.2** `[EDIT]` Move the **hybrid retrieval equation** from theory section into §2.2 (Mathematical Models) for consistency. — *item 2.2, pt1*
- **5.A.3** `[REREAD][EDIT]` **Re-frame the problem statement** — lead with "applying QE to improve Arabic RAG" with multiple approaches as the main contribution. Move "small models" to secondary novelty. Cascade into 1.2/1.3/1.4. *Depends on Q2 supervisor answer.* — *item 2.7, pt1/pt2*
- **5.A.4** `[REREAD][EDIT]` **Expand the QE techniques section (§2.4 area)** to cover all four families (expansion, rewriting, decomposition, abstraction) with the papers actually read for each. — *items 2.8/2.9, pt2*
- **5.A.5** `[EDIT]` **Remove the irrelevant paper-12 citation** next to the morphological-gap discussion. (Verify the paper number ID before editing — it's the one about chunking + embedding selection.) — *item 2.11, pt2*
- **5.A.6** `[EDIT]` Once Task 4.2 verifies BM25S parameters, **fix the §2.3.2 vs §3.2.2 inconsistency** (k1=1.5/b=0.75 vs k1=0.9/b=0.4). — *item 2.12*
- **5.A.7** `[DECIDE][EDIT]` After Task 6.3 (read or replace Song & Zheng): either keep the citation, or replace it with a paper actually read for the QE taxonomy. — *item 2.14*
- **5.A.8** `[REREAD][EDIT]` **GPT-OSS retain-or-delete final decision.** Working preference is delete entirely. Decide and apply (text + tables + Ch.4 references). — *item 2.5, pt1/pt4*

### 5.B — Chapter 3 rewrites

- **5.B.1** `[EDIT]` **Drop the "intentionally weaker baseline" framing** for mDPR. Replace with neutral statement. Also fix Ch.5 §5.5 with the same wording. — *items 3.3 + 5.5, pt2/pt3/pt4*
- **5.B.2** Tasks 1.2 + 1.4 already cover §3.3 / §3.9 error analysis sections.
- **5.B.3** `[EDIT]` **Drop the "256 diminishing returns" justification** for max_tokens=128. Replace with honest statement (or cite Task 8.2 if the experiment is run). — *item 3.9, pt3*
- **5.B.4** `[EDIT]` **Replace "16x combined speedup"** with measured wall-clock improvement (e.g., "~8 hours sequential to ~40 minutes"). Drop the multiplier breakdown. — *item 3.10, pt3*
- **5.B.5** `[EDIT]` After Task 4.3 verifies SILMA temperatures, **fix the temperature claim in §3.6.x** (likely 0.7 vs 0.1, not 0.0 vs 0.1). — *item 3.11, pt3*
- **5.B.6** `[EDIT]` **Drop or replace the "73 min Colab CPU" runtime claim** in §3.6 (BM25 query repetition methodology). Replace with cell-output number if extractable. — *item P4.3.5, pt6*
- **5.B.7** `[EDIT]` **Soften the §3.8.3 hypothesis** from "BM25 benefits / Dense degrades" to: "Three fusion configurations were tested to determine the optimal retriever–query assignment; whether expansion helps or hurts each retriever was left open." Save the causal interpretation for Ch.4. — *item P4.3.13, pt6*
- **5.B.8** `[EDIT]` **Add the exact CSQE system prompt** to §3.8 for reproducibility (mirror how the blind Q2D prompt is shown in §3.5). Source: exp_013 notebook. — *item P4.3.16*
- **5.B.9** `[EDIT]` **Add "k=1 in our experiments" clarification** to the assembly equation in §3.6 (the general-k MuGI formula). — *item P4.3.7, pt6*
- **5.B.10** `[VERIFY][EDIT]` After Task 4.6 verifies top-100, **confirm or fix §3.7 retrieval-depth wording**. — *item P4.3.10*

### 5.C — Chapter 4 rewrites

- **5.C.1** `[EDIT]` **Remove the "Arabic morphological richness benefits disproportionately" hypothesis** from §4 (Q2D results discussion). Also remove from Ch.5 §5.1 and from the abstract. — *items 4.5 + 5.2 + A.3, pt3/pt5*
- **5.C.2** `[EDIT]` **Add a Pearson/Spearman correlation coefficient restricted to the Qwen family** (4 data points: 2.5-3B, 3-4B, 2.5-7B, 3-8B) in §4.5 / §4.6. Note the cross-generation confound for the broader claim. — *item 4.6, pt3*
- **5.C.3** `[EDIT]` After Task 4.4, **specify the exact Arabic benchmark** in the "benchmarks don't predict QE quality" claim. — *item 4.7, pt3*
- **5.C.4** `[EDIT]` **Soften "Best Model Recommendations"** wording — "Aya was strongest in our experiments on MIRACL Arabic" rather than universal recommendation. — *item 4.12, pt3*
- **5.C.5** `[REREAD][EDIT]` **Audit each table** in Ch.4 for completeness, accuracy, and page-overflow. Move tabular data into figures where figures work better. (Pairs with Workstream 7.1 figure plan.) — *item 4.14, pt3*
- **5.C.6** `[EDIT]` **Correct the BM25 repetition recovery claim** in §4.6: was "9 of 9 recovered" — should be "6 of 9 were below baseline at n=1; all 9 reached or exceeded baseline at appropriate repetition." — *item P4.4.2, pt8*
- **5.C.7** `[EDIT]` **Drop the size-based interpretation** of optimal repetition (8B at β=2 vs 3-4B at n=5–7). Differences are too small to support causal claim. — *item P4.4.3, pt8*
- **5.C.8** `[EDIT]` **Rephrase "missing ingredient"** in §4.6 to scientific wording: "for the originally underperforming systems, the deficiency was not in the model itself but in the absence of query repetition." — *item P4.4.5, pt8*
- **5.C.9** `[EDIT]` **Move hybrid no-QE result to the baselines section** so it sits alongside BM25-alone and mDPR-alone as a reference baseline. — *item P4.4.9, pt8*
- **5.C.10** `[EDIT]` **Soften the CC tie-breaking explanation** to "a possible explanation is …" not established mechanism. — *item P4.4.8, pt8*
- **5.C.11** `[EDIT]` After Task 4.9/4.10 verifications, **revise §4.8 dense degradation explanation**. If verifications fail, drop the specific claims (1500 chars, "trained on short queries") and present degradation without the speculative explanation. — *item P4.4.11, pt7/pt8*
- **5.C.12** `[EDIT]` **Reframe §4.8 ablation discussion** to lead with complementarity (2+2 > 4+0 and 0+4) rather than "blind beats corpus on BM25." — *item P4.4.12, pt7*
- **5.C.13** `[EDIT]` **Reframe §4.9 retriever-specific representation explanation**: from "Dense degrades on long inputs" to "Dense + CSQE in fusion reduces complementarity with BM25 + CSQE; the two ranked lists become less divergent, lowering the fusion ceiling." — *item P4.4.16, pt7*
- **5.C.14** `[EDIT]` **Soften "key design finding of the thesis"** to "one of the principal findings, alongside [list other principal findings]." Avoid declaring single THE-key. — *item P4.4.18, pt7*
- **5.C.15** Tasks 1.1–1.3 cover §4.10 (per-query analysis Config A redo and dataset integrity).
- **5.C.16** `[EDIT]` **Demote the meta-description failure mode** to an illustrative single-case example. Don't name a failure mode after one query. — *item P4.4.22, pt7/pt9*
- **5.C.17** `[REREAD][EDIT]` **Reformat the big-win examples table**: all English, side-by-side blind-vs-CSQE expansion text (not summaries). Consider moving extended detail to the appendix. **Verify الرباط المنصوري + replace or verify John Dewey and Nicolas Boileau.** Search for stronger illustrations if needed. — *item P4.4.23, pt9/pt10*
- **5.C.18** `[EDIT]` **Soften "first-pass recall is dominant predictor"** to "the largest observed modulator." After Task 4.14 verifies the 0.3 threshold rationale, fix or remove that justification. — *item P4.4.24, pt10*
- **5.C.19** `[EDIT]` **Move §4.10.4 implications/recommendations to Ch.5** (first-pass quality gate, asymmetric expansion weighting). — *item P4.4.26, pt9/pt10*
- **5.C.20** `[EDIT]` **Drop the Medium query-length row with "—" entries** OR populate it with actual data. — *item P4.4.27*
- **5.C.21** `[EDIT]` **Move the summary table to end of Ch.4 (or appendix)**, not in the middle. Combine Phase 4 rows into one summary table provided no page overflow. — *item P4.4.28, pt10*

### 5.D — Chapter 5 rewrites

- **5.D.1** `[REREAD][DECIDE]` **Mohammed's pending Ch.5 deep dive** — recording ended in pt10 before he completed his Ch.5 review. Decide what's still to revisit before doing other Ch.5 edits.
- **5.D.2** `[EDIT]` **Per-challenge edits in §5.2** (six challenges):
  - Resource constraints: keep.
  - BM25 term-dilution: reword to acknowledge precedent in Wang 2023.
  - Dropped models (ALLaM): explicitly disclose the sentencepiece tokenizer artifact (`▁` → dashes) that caused ALLaM's poor result; keep result as-is, document the artifact.
  - "Phase 4" wording: removed by Task 2.1.
  - Dataset scope: extend to mention MIRACL's lack of metadata (blocks chunking-aware extension).
  - Single QE technique / weak baseline: handled by 5.B.1.
  — *item 5.4, pt4*
- **5.D.3** `[EDIT]` **Recommendations cleanup in §5.3:**
  - **DELETE** Recommendations 2 (BM25 query repetition) and 4 (Hybrid retrieval with QE) — already implemented.
  - **DELETE** Recommendation 8 (publication) — too presumptuous.
  - **KEEP with addition** Recommendation 1 (knowledge-base-aware QE) — mention dataset metadata gap that blocked it; was original plan. *(BUT check duplication: pt10 noted it's mentioned earlier in the thesis — keep one occurrence only.)*
  - **KEEP with softening** Recommendation 5 (dialectal Arabic) — phrase as "may help bridge MSA-dialect retrieval gaps; requires evaluation on dialect-aware datasets."
  - **ADD** the two recommendations moved from §4.10 (first-pass quality gate, asymmetric expansion weighting).
  - **KEEP** the three Phase 4 recommendations (first-pass quality gate, asymmetric expansion, stronger retrievers) — verify BGE-M3/mE5-large are still SOTA at submission time.
  — *items 5.6–5.9, P4.5.7, P4.5.8, pt4/pt10*
- **5.D.4** `[EDIT]` **Reorder Phase 4 conclusion paragraphs** so the strongest summary closes the chapter. Currently the AI placed an "Overall" paragraph and then added Phase 4 conclusions after it — structurally backwards. — *item P4.5.1, pt10*
- **5.D.5** `[EDIT]` **Soften "any multi-retriever pipeline"** to "similar hybrid pipelines" or drop the generalization. — *item P4.5.3, pt10*

### 5.E — Chapter 1 rewrites (cascade from 2.7)

- **5.E.1** `[REREAD][EDIT]` **Re-frame Ch.1 narrative** based on the chosen problem statement (general vs specific). *Depends on Q2 supervisor answer + Task 5.A.3.* — *items 1.1, 1.2, 1.3, pt3*
- **5.E.2** `[EDIT]` **Use 10 (not 11) consistently** in objectives, methodology, results, abstract. Use 11 only in Ch.2 literature with explicit framing ("we surveyed 11 candidate models, of which 10 were ultimately evaluated"). — *item 1.5, pt4*
- **5.E.3** `[EDIT]` **Reframe model comparison** so it reads as extensive validation, not the central contribution. — *items 1.5, 4.12*
- **5.E.4** `[EDIT]` After Task 7.4 supervisor answer on Q4: format the **Thesis Layout section** as paragraphs or bullets. — *item 1.7*

### 5.F — Abstract rewrites

- **5.F.1** `[REREAD][EDIT]` **Rewrite the abstract** from the corrected problem statement. Target ~250 words. Drop excessive detail, drop the 175B comparison, drop "small models" overemphasis. Keep "practical strategy" closing. — *items A.1, A.3, A.4, P4.A.2, pt5*
- **5.F.2** `[EDIT]` **Update the closing result sentence** with the post-Phase-4 numbers (0.7137 / 54.5% / 13.9%). — *item P4.A.1*
- **5.F.3** `[VERIFY][EDIT]` **Check Arabic abstract numeral convention** (Eastern Arabic vs ASCII). Match existing convention. — *item P4.A.3*
- **5.F.4** `[EDIT]` **Translate the new English abstract to Arabic** with self-review (Mohammed/Osman). Establish terminology convention (preserve English for technical terms like RAG, mDPR; use Arabic for general concepts). — *items A.5, P4.A.4*

---

## Workstream 6 — Research / external lookups

> **✅ COMPLETED 2026-05-30 — full results in `research_decisions/WS6_RESEARCH_REPORT.md`.**
> Headlines: 6.1 NEEDS EDIT (a concurrent Nov-2025 paper uses Gemma-3-4B for Arabic QE but **cross-lingual**, not monolingual MIRACL → narrow the gap claim);
> 6.2 NEEDS EDIT (**Exp4Fuse**, ACL 2025 Findings, is the nearest prior art but is **sparse-only**, not dense–sparse hybrid → cite it + downgrade novelty to "Arabic + heterogeneous hybrid");
> 6.3 KEEP (Song & Zheng entry correct; four-operation taxonomy matches §2.4 exactly — use "disambiguation", not "rewriting", in 5.A.4);
> 6.4 MAJOR (**10 wrong entries** incl. `aya_2024` URL→unrelated MRI paper and `yoon_2025` skeptical paper cited as supporting; corrected BibTeX provided; feeds WS3.1/WS3.2);
> 6.5 NEEDS EDIT (BGE-M3 still SOTA-class, but mE5-large dated — Swan/ArabicMTEB beats it on Arabic; add Arctic-Embed 2.0 / Nomic-multilingual to Recommendation 3).

### Task 6.1 — Literature search: post-2024 small-LLM Arabic QE papers
- **Tags:** `[RESEARCH]`
- **Source:** item 2.7 (pt1)
- **What:** Search arxiv / Google Scholar / ACL Anthology for any paper published 2024–2026 testing small (<7B) LLMs for query enhancement on Arabic text. If any exist, the gap claim must be revised.
- **Outcome:** updated gap framing in §2.4 / §1.2.

### Task 6.2 — Literature search: post-2024 asymmetric CSQE × hybrid
- **Tags:** `[RESEARCH]`
- **Source:** P4.2.4 (pt6) — Osman tagged for this in the brief
- **What:** Search for any work on asymmetric query expansion in hybrid retrieval (applying QE to only one retriever in a fusion setup). If any exist, downgrade the gap claim to "not yet for Arabic."
- **Outcome:** updated gap framing in §2.4.

### Task 6.3 — Read or replace Song & Zheng 2024
- **Tags:** `[RESEARCH][DECIDE]`
- **Source:** item 2.14 (pt2)
- **What:** Either read enough of Song & Zheng 2024 (107-page survey) to defensibly cite it, or replace with a survey actually read for the QE taxonomy framing.
- **Outcome:** finalized §2.4 citation.

### Task 6.4 — Full citation audit
- **Tags:** `[VERIFY][SWEEP]`
- **Source:** item 2.15 (pt2)
- **What:** For every citation in the thesis: verify the BibTeX key exists in `References.bib`, the URL resolves, and the cited paper actually says what the thesis claims it says. Mohammed explicitly tagged this as an AI task ("task ليك يا AI").
- **Outcome:** clean References.bib + revised citations where wrong.

### Task 6.5 — Verify SOTA Arabic retrievers at submission time
- **Tags:** `[RESEARCH]`
- **Source:** item P4.5.8 (pt4/pt10)
- **What:** Recommendation lists BGE-M3 and mE5-large as "stronger embedding models." Check at submission time whether these are still SOTA Arabic retrievers, or if newer alternatives have been published.
- **Outcome:** updated Recommendation 3 / final recommendations list.

---

## Workstream 7 — Multi-step deliverables (workstreams)

### Task 7.1 — Figure plan document → Claude implements
- **Tags:** `[REREAD][EDIT]`
- **Source:** item 4.15 (pt3)
- **Phases:**
  1. Mohammed drafts a figure-plan document listing each figure: which results it visualizes, which section it belongs to, and a description of what it should show. Possibly compare with a Gemini-generated version.
  2. Add the BM25 repetition recovery graph (Task 5.C.6) as a known required figure.
  3. Once descriptions are agreed, Claude implements them in LaTeX (TikZ or matplotlib → image).
- **Output:** a `figures/figure_plan.md` document, then actual figure files inserted into the LaTeX source.

### Task 7.2 — Brief verification (parallel Gemini chat)
- **Tags:** `[VERIFY]`
- **Source:** P4.4.20 surfaced (pt5) — Mohammed's pt5 mitigation idea
- **What:** Spin up an independent Gemini chat. Feed it only the original experiment reports (not the brief). Ask it to produce its own thesis-update document. Diff against the existing brief to detect other context-pollution errors like P4.4.20.
- **Why:** after one major brief error was discovered, confidence in the brief is reduced. Independent regeneration is the cheapest verification.

### Task 7.3 — Slides for next supervisor meeting
- **Tags:** `[EDIT]`
- **Source:** pt6 wrap-up
- **What:**
  - Mohammed extracts work completed since the last supervisor meeting (from the Phase 4 brief).
  - Osman extracts the open questions (pulled from pt1–pt3 transcripts initially, plus the consolidated Q1–Q6 list below).
  - Joint output: short slide deck for the meeting.

### Task 7.4 — Supervisor meeting (asks Q1–Q6)
- **Tags:** `[ASK]`
- **Source:** consolidated across pt1–pt5
- **Questions to ask Dr. Tahani:**
  - **Q1** — Should the thesis include a Chapter Summary section? (item 2.3, pt1)
  - **Q2** — Problem statement: general or specific? (item 2.7, pt1)
  - **Q3** — Is a technology-driven narrative acceptable for Chapter 1? (item 1.1, pt3)
  - **Q4** — Thesis Layout section: paragraphs or bullet points? (item 1.7, pt4)
  - **Q5** — Abstract length expectation: 1 page or shorter? (item A.1, pt5)
  - **Q6** — What does "33 cross-reference labels in Ch.2" mean — internal labels or citation count? (item X.2, pt5)
- **Optional context to bring:** Dr. Tahani's recordings transcribed and cross-checked against the thesis (action item from pt1) — defer if no time.

---

## Workstream 8 — Experimental backlog (LOW PRIORITY — if time)

> User decision: do these only if the rest is finalized and time allows.

### Task 8.1 — Asymmetric vanilla Query2Doc in hybrid
- **Tags:** `[EXPERIMENT]`
- **Source:** P4.2.5 + P4.4.11 (pt6, pt8)
- **What:** Run hybrid fusion with vanilla blind Q2D applied:
  - To BM25 only (Dense uses raw query)
  - To Dense only (BM25 uses raw query)
  - To both
- Compare against Configs A/B/C (CSQE-based) and the no-QE hybrid baseline (0.6267).
- **Outcome:** if Config-A-style asymmetric pattern repeats with vanilla Q2D → the retriever-specific representation finding generalises beyond CSQE; thesis conclusions strengthen substantially.
- **Effort:** moderate — methodology already exists, just need a new experiment notebook.

### Task 8.2 — 256 vs 128 max_tokens comparison on Aya
- **Tags:** `[EXPERIMENT]`
- **Source:** item 3.9 (pt3)
- **What:** Run Aya QE with max_tokens=256 vs 128 on the main experiment (pre-hybrid, pre-CSQE). Compare nDCG@10. If similar, the 128 choice is justified by data. If different, revisit.
- **Outcome:** either justify the 128 choice empirically, or revisit the choice.
- **Effort:** small — single experiment.

### Task 8.3 — ALLaM rerun with uniform post-processing
- **Tags:** `[EXPERIMENT][DECIDE]`
- **Source:** item 5.4 challenge 3 (pt4)
- **What:** Apply post-processing (e.g., strip dashes/spaces from outputs) uniformly to all 10 models, including ALLaM. Re-evaluate the leaderboard.
- **Why considered:** Osman's pt4 frustration that ALLaM was unfairly penalized by a tokenizer artifact.
- **Why deprioritized:** uniform application across all 10 models is expensive; the artifact-disclosure approach (Task 5.D.2) is the cheaper alternative.
- **Decision needed before running:** is the disclosure-only approach acceptable, or is rerun necessary for honesty?

---

## Progress Log

> Updated 2026-05-07 after sessions on 2026-05-06 and 2026-05-07. All edits committed in `01ec759` (initial batch) and corrective follow-up commit.

### Completed tasks (verified against task descriptions)

| Task | Status | Notes |
|------|--------|-------|
| 2.1 | ✅ DONE | All "Phase 4" instances purged from Ch1–Ch5 |
| 2.2 | ✅ DONE | All experiment-number parentheticals removed from Ch3/Ch4; Table 4.10 Exp. column removed |
| 2.3 | ✅ DONE | k1=0.9, b=0.4 verified from notebook line 198–199; notation paragraph added end of §2.2 |
| 2.4 | ✅ DONE | Config A/B/C → BM25-expanded/Dense-expanded/Both-expanded globally (Ch3, Ch4, Ch5); §3.8.3 hypothesis softened (combined with 5.B.7) |
| 2.5 | ✅ DONE | mDPR baseline framing fixed ("reproduced exactly"); Recall@100 already consistent at 0.9467 |
| 3.4 | ✅ DONE | One instance: "statistically indistinguishable" → "numerically" in §4.7 (CC/RRF comparison) |
| 3.5 | ✅ DONE | 8×/2×/16× speedup multipliers removed; 73-min Colab CPU sentence deleted; "~40 minutes" kept as measured value |
| 5.B.1 | ✅ DONE | "Intentionally weaker baseline / headroom" framing removed from Ch2.tex line 314, Ch3.tex §3.2.1, Ch5.tex §5.5 |
| 5.B.3 | ✅ DONE | "256 diminishing returns" sentence deleted from §3.5 |
| 5.B.4 | ✅ DONE | 8×/2×/16× multipliers removed; "~40 minutes per model" kept |
| 5.B.7 | ✅ DONE | §3.8.3 hypothesis softened to empirical framing (done as part of 2.4) |
| 5.B.9 | ✅ DONE | "k=1 in MuGI notation" clarification added to assembly equation note |
| 5.C.1 | ✅ DONE | "Arabic morphological richness disproportionate" removed from §4.3 and §5.1 |
| 5.C.4 | ✅ DONE | "Best Model Recommendations" → "Model Selection Summary"; prescriptive language softened |
| 5.C.6 | ✅ DONE | "nine previously degraded models" → "six" corrected in §4.6 and §5.2 |
| 5.C.7 | ✅ DONE | Size-based repetition interpretation dropped; replaced with pseudo-document-length explanation |
| 5.C.8 | ✅ DONE | "Missing ingredient" → empirical restatement |
| 5.C.10 | ✅ DONE | CC tie-breaking hedged to "a possible explanation is…" |
| 5.C.11 | ✅ DONE | "~1,500 chars" and "trained on short queries" claims **dropped** (fallback path: verifications 4.9/4.10 not done); degradation now stated as empirical observation only |
| 5.C.12 | ✅ DONE | Ablation discussion reframed to lead with complementarity finding |
| 5.C.13 | ✅ DONE | §4.9 retriever-specific explanation reframed to complementarity/divergence mechanism ("two ranked lists become less divergent → lower fusion ceiling"), matching task specification |
| 5.C.14 | ✅ DONE | "Key design finding of the thesis" → "this finding illustrates a principle" |
| 5.C.16 | ✅ DONE | Query ID 1060 removed; single-case example demoted to brief mention |
| 5.C.18 | ✅ DONE | "Dominant predictor" → "primary driver" |
| 5.D.3 | ✅ DONE | Recs 2 and 4 (already implemented) deleted; Rec 8 (publication) deleted; Rec 5 (dialectal) softened to "open question" framing |
| 5.D.5 | ✅ DONE | "Any multi-retriever pipeline" → "similar hybrid pipelines" |

### Self-initiated changes (not from task list)

None remaining — the Both-expanded numeric change (0.6959→0.6936 / −0.0178→−0.0201) was reverted after review confirmed it had no source in the meeting notes or review document.

### Still pending (not touched)

All tasks not listed above remain pending as specified. Key blockers:
- WS1 (1.1–1.4): require Colab notebook runs with MIRACL data
- WS4 (4.3–4.17 most): require notebook lookups or external verification
- WS5.C.2: requires computing Pearson/Spearman for Qwen family
- WS5.C.17: big-win examples need verification (Task 4.12)
- WS5.D.1: Mohammed's Ch.5 deep-dive recording was incomplete
- WS3.1–3.3: require reading each chapter section carefully
- WS5.A, 5.E, 5.F: blocked on supervisor Q2/Q3 (Ch.1/abstract rewrite)

---

## Suggested execution order

A reasonable next-chat / next-session sequence:

1. **Workstream 1** in order (1.1 → 1.2 → 1.3 → 1.4). Get §3.3 and §4.10 to final.
2. **Workstream 4** (verifications) in parallel — single lookups, can be batched. The outcomes feed many edits in Workstream 5.
3. **Workstream 2** (thesis-wide sweeps) — quick wins, mechanical, set up downstream edits.
4. **Workstream 6** research tasks (6.1, 6.2, 6.4) in parallel — these don't block writing but their outcomes refine specific items.
5. **Workstream 7.4** supervisor meeting — pull the trigger when Q1–Q6 are blocking next steps (currently only Q2 and Q3 cascade into Ch.1/abstract rewrites).
6. **Workstream 5** per-item rewrites — the big writing pass. Order: Ch.2 → Ch.3 → Ch.4 → Ch.5 → Ch.1 → Abstract. (Ch.1 last because it cascades from Ch.2 and Ch.5.)
7. **Workstream 3** (AI-pattern audits) — interleaved with Workstream 5 reading passes; "while you're in Ch.X, sweep for the patterns."
8. **Workstream 7.1** figure plan — once Ch.4 content stabilizes; then Claude implementation.
9. **Workstream 7.2** brief verification — can run in background early; review output once available.
10. **Workstream 8** experiments — only if time after the above.

---

## Handoff note for a fresh chat

If picking this up cold:
1. Read `THESIS_REVIEW_RESOLUTIONS.md` first — that has full discussion + verdict per item.
2. This file (`THESIS_NEXT_STEPS_TASKS.md`) is the actionable to-do.
3. Mohammed's user-set priority: **Workstream 1 first, then anything else, experiments last.**
4. The original review document `THESIS_DRAFT_AI_DECISIONS_REVIEW.md` is the source of item numbers — don't renumber.
5. Per-transcript notes in `meetings/analysis/` if you need verbatim discussion context for a specific item.
6. The thesis LaTeX source is in `University_of_Khartoum__EEE_bachelor_s_thesis_template/` — chapter files inside.
7. Update this file as tasks are completed (check off with `- [x]` if you switch to checklist format, or strike through, or move to a "completed" section).

**END.**
