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

> **✅ COMPLETED 2026-05-30, team-reviewed 2026-05-31, WS1-synced 2026-05-31 — full results + meeting notes in `research_decisions/WS4_VERIFICATION_REPORT.md`.**
> Headlines: 4.5 VERIFIED, keep as-is (30% is real on TREC DL19 **mAP**: BM25 30.1 → CSQE Llama2-7B 39.1, Table 7 — note it's mAP not nDCG);
> 4.4 → **adopt OALL** as base benchmark + standardise generic "Arabic NLP benchmark" → OALL **thesis-wide [SWEEP]** (keep Ch.2 per-model scores & MIRACL-dataset mentions); 4.15 NEEDS EDIT (MuGI + `lei_2024_csqe` title/authors fabricated — papers were read, only metadata wrong → escalate 6.4);
> 4.12 → keep الرباط المنصوري, **drop John Dewey** (blind was correct), **fix Boileau** description (businessman→computer scientist), find 3 better examples;
> 4.13 → reframe to the **general Type B** "first-pass poisoning" mode (928 ماهو-homonym, 11371 name-homonym, 11739 wrong-entity); keep ماهو التطرف as one illustration; regression bucket tables fixed (A≥0.3 / B<0.1 / C 0.1–0.3, no double-listing);
> 4.16 → only **table/figure** labels need fixing (section labels harmless).
> **WS1-closed (per `STREAM_1_COMPLETION_REPORT.md`):** 4.8 confirmed (BM25 top-1, qrel≥1); **4.11 → "irretrievable" REFUTED** (0/258 — all genuine retrieval failures, corpus complete; §4.10 must drop the dataset-ceiling wording); 4.14 → keep 3 threshold systems + signpost, "dominant predictor"→"largest modulator"; 4.17 → Config-A validated by WS1.3 (0.6936/0.5046/Δ0.1890), reconcile 0.7137 system vs 0.6936 per-query labels. WS1 also corrected a separate §4.2 baseline buggy-nDCG (dense-baseline only).

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

- **5.A.1** ✅ DONE (2026-06-15) `[REREAD][EDIT]` Add **dataset analysis section** to Ch.2 (before Models Used). Cover the ~8 datasets evaluated and why MIRACL was chosen. — *item 2.1, pt1* → added as §2.3 "Evaluation Dataset Selection" with web-verified citations.
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

### 2026-05-31 — Workstream 1 fully complete + figures pipeline rendered

Full completion report: `research_decisions/STREAM_1_COMPLETION_REPORT.md`.

| Task | Status | Notes |
|------|--------|-------|
| 1.1 | ✅ DONE | **Claim refuted.** Local corpus-membership check (`thesis_figures/notebooks/task_1_1_corpus_integrity.py`) over the full 2,061,414-doc MIRACL Arabic corpus: of 258 failures (Config A RRF nDCG@10 < 0.1), **0 irretrievable / 258 genuine retrieval failures**. 199 also miss on BM25 baseline; **58 are BM25-retrievable (43 with BM25 ≥ 0.3) but lost by the CSQE hybrid** = real regressions. Routing = "claim wrong → reframe §4.10, proceed" (NOT the indexing-bug STOP branch). Verdict CSV: `thesis_figures/data/computed/task_1_1_failure_corpus_check.csv`. Correction banner added to `exp_error_analysis_csqe.md`. |
| 1.2 | ✅ DONE | Decision A: unify on **Short 1–3 / Medium 4–8 / Long 9+ words** (preserves §4.2 short-query motivation). KEEP absolute Failed/Mediocre/Successful thresholds. **+ §4.2 nDCG correctness fix discovered:** the original `exp_001_quantitative_analysis.json` was computed with non-standard nDCG and disagrees with the canonical headline values. Recomputed locally from `exp_001_baseline_dense.txt` with `pytrec_eval` → all four headline metrics reproduce exactly (0.4993/0.6156/0.8407/0.5328). Corrected §4.2 numbers: failure 39%→**34%**, successful 5%→**33%**, short bucket nDCG 0.240→**0.345**, length↔nDCG r 0.125→**≈0**, coverage@100 99.4%→**90.1%**. Reconciliation CSV: `thesis_figures/data/computed/sec4_2_reconciliation.csv`. |
| 1.3 | ✅ DONE | Per-query export cell executed in Colab. `csqe_vs_blind_per_query.csv` produced (2,896 rows; in `thesis_figures/data/raw/`). All claimed aggregates reproduce: big wins 1,061, regressions 367, win/tie/loss 56.8/26.6/16.6%, mean Δ 0.1890, first-pass 0.8877/0.5814. First-pass definition resolved: BM25 top-1 with qrel≥1 (closes WS4 Task 4.8). |
| 1.4 | ✅ DONE | Three orthogonal threshold systems catalogued (absolute §3.3, pairwise §3.9, hybrid regression-subtyping §3.9). Resolution: keep all three + one signpost paragraph at `chapter3.tex:109`. No data dependency. **Thesis text edit pending — Track A.** |

#### Workstream 7.1 — Figure plan + implementation: Track B figures DONE
All 44 figure PDFs + 32 PNG previews rendered into `thesis_figures/output/`. Inventory:
- **12 system diagrams** (Ch 2 + 3) — all TikZ; xelatex-compiled. Excalidraw track abandoned in favour of TikZ.
- **32 data-figure variations** (Ch 4) across 15 figures, rendered from canonical post-WS1 data via 5 matplotlib notebooks (`02_baseline_figures.ipynb` through `05_error_analysis.ipynb`).
- **6 LaTeX table snippets** (Tables 4.1, 4.2 partial, 4.3, 4.4, 4.5, 4.7). Tables 2.1, 2.2, 3.1, 3.2, 4.6 + R@10/R@100/MRR columns for Osman's 5 models in Table 4.2 are hand-compile work.

Joint review document: `thesis_figures/REVIEW.html` (open in browser; per-figure ratings + side-by-side variations + sign-off slots).

Visual-quality feedback noted in `thesis_figures/README.md` "Visual feedback" section — current renders are mathematically correct and submission-eligible, but flagged for a future polish pass (color, icons, AI-illustration option for Ch 2 conceptual diagrams). Not blocking.

#### Track A — Thesis text edits per `STREAM_1_COMPLETION_REPORT.md` §3
**NOT STARTED.** Mohammed's next session. The data is settled; remaining work is pure LaTeX editing across `chapter3.tex`, `chapter4.tex`, plus syncing the supporting MD docs (`error_analysis_phase1_quantitative.md`, `exp_error_analysis_csqe.md`).

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
| 5.C.11 | ✅ DONE (RESTORED 2026-06-15) | Now that WS4 4.9/4.10 are verified, the §4.9 dense-degradation explanation was **restored with citations**: mDPR's MS-MARCO short-query fine-tuning (cite `bajaj_2016_msmarco`) + ~1,500-char expansions, as a reinforcing factor alongside the complementarity mechanism |
| 5.C.12 | ✅ DONE | Ablation discussion reframed to lead with complementarity finding |
| 5.C.13 | ✅ DONE | §4.9 retriever-specific explanation reframed to complementarity/divergence mechanism ("two ranked lists become less divergent → lower fusion ceiling"), matching task specification |
| 5.C.14 | ✅ DONE | "Key design finding of the thesis" → "this finding illustrates a principle" |
| 5.C.16 | ✅ DONE | Query ID 1060 removed; single-case example demoted to brief mention |
| 5.C.18 | ✅ DONE (2026-06-15) | Heading + prose → "largest modulator" (per WS1 1.4 / WS4 4.14); first-pass defined as top-1 |
| 5.D.3 | ✅ DONE | Recs 2 and 4 (already implemented) deleted; Rec 8 (publication) deleted; Rec 5 (dialectal) softened to "open question" framing |
| 5.D.5 | ✅ DONE | "Any multi-retriever pipeline" → "similar hybrid pipelines" |
| | | |
| \multicolumn — **2026-06-10 apply pass (WS1 Track A + WS4 + WS6 + ready WS5)** | | |
| WS1 1.1–1.4 | ✅ DONE (2026-06-10) | §4.2 canonical numbers (failed 34%, successful 33%, coverage 90.1%@100, length 0.345/0.511/0.476, r≈0, nDCG=0 → 736); §3.3 tokens→words + threshold signpost; §4.10 failure paragraph + first-pass top-1 + Medium row |
| 4.4 / 5.C.3 | ✅ DONE (2026-06-10) | Generic "Arabic NLP benchmark" → OALL (§4.5.3 + Ch.5 recap + §4.5.3 "lower OALL score") |
| 4.8 | ✅ DONE (2026-06-10) | First-pass = BM25 top-1, qrel≥1 (§3.9 + §4.10) |
| 4.11 / 5.C.15 / 5.C.16 | ✅ DONE (2026-06-10) | §4.10 failure paragraph: "irretrievable/dataset-ceiling" refuted → 199 missed-by-all + 58 BM25-lost |
| 4.12 / 5.C.17 | ✅ DONE (2026-06-10) | Big-win trio replaced (الرباط المنصوري / الأسماء الخمسة / الفن الجزيري) + blind-poisoning framing |
| 4.13 | ✅ DONE (2026-06-10) | Type B reframed to general first-pass-poisoning mode with 3 representative examples |
| 4.14 | ✅ DONE (2026-06-10) | 0.3 threshold flagged as a pragmatic boundary; "largest modulator" |
| 4.15 / 6.4 | ✅ DONE (2026-06-10) | 10 fabricated References.bib entries fixed (incl. `aya_2024` MRI-URL, `yoon` misrepresentation); +Exp4Fuse/Macmillan-Scott/Qwen3-Embedding/Swan added |
| 4.17 | ✅ DONE (2026-06-10) | §4.10 caption → BM25-expanded (Config A); 0.6936 per-query vs 0.7137 corpus-level reconciled |
| 6.1 | ✅ DONE (2026-06-10) | §2.4 gap narrowed to monolingual Arabic + Macmillan-Scott cite |
| 6.2 | ✅ DONE (2026-06-10) | §2.4 asymmetry gap reframed + Exp4Fuse cite |
| 6.5 | ✅ DONE (2026-06-10) | Rec 2/8: keep BGE-M3, replace mE5-large with Qwen3-Embedding-8B + Swan-Large |
| 5.A.5 | ✅ DONE (2026-06-10) | Decorative Alsubhi (paper-12) citation removed from morphological-gap sentence |
| 5.B.8 | ✅ DONE (2026-06-10) | Exact CSQE system prompt added to §3.8 |
| 5.C.2 | ✅ DONE (2026-06-10) | Qwen-family correlation (Pearson 0.94 / Spearman 1.00) + confound caveat in §4.5.1 |
| 5.C.19 | ✅ DONE (2026-06-10) | §4.10 implications → forward pointer; the two recs already present in Ch.5 §5.3 (Recs 6–7) |
| 5.C.20 | ✅ DONE (2026-06-10) | §4.10 length table → Scheme A (1–3/4–8/9+), Medium row filled |
| 5.D.2 | ✅ DONE (2026-06-10/15) | ALLaM `▁` disclosure present; MIRACL metadata-gap added (§5.2); `wang_2023_query2doc` cite added to challenge 2 |
| 5.D.4 | ✅ DONE (2026-06-10) | "Overall" paragraph moved to close §5.1, augmented with 0.7137 headline |
| Abstracts EN+AR | ✅ DONE (2026-06-10) | 39%→34%; "significant gap" softened; closing numbers already correct |
| | | |
| \multicolumn — **2026-06-15 session (GPT-OSS removal + remaining deferred)** | | |
| 5.A.8 | ✅ DONE (2026-06-15) | **GPT-OSS deleted completely** — Ch.2 §2.4 Experimental subsection + model_comparison row + counts; Ch.3 category/config/issues/quantisation; Ch.4 dropped-models §ALLaM-only + leaderboard + summary rows; Ch.5 challenge 3; generated `table_2_2.tex` + CSV; `gptoss_2025` bib entry removed |
| 5.E.2 | ✅ DONE (2026-06-15) | Resolved by GPT-OSS deletion: "eleven"→"ten" thesis-wide (abstract/Ch.1/Ch.2/Ch.4/Ch.5 all consistent at ten 2–8B models) |
| 5.A.2 | ✅ DONE (2026-06-15) | RRF + CC equations moved from §2.1.3 into new §2.2 "Hybrid Fusion Functions" (`sec:hybrid_math`); eq labels preserved so Ch.3 refs still resolve |
| 5.A.4 | ✅ DONE (2026-06-15) | §2.1.4 expanded to four families (expansion/decomposition/disambiguation/abstraction); `zheng_2023_take` used for abstraction (resolves an orphan) |
| 5.C.9 | ✅ DONE (2026-06-15) | No-QE hybrid (0.6267) added as a reference baseline in §4.1 table + prose |
| 5.C.21 | ✅ DONE (2026-06-15) | "Summary of All Experiments" table moved to end of Ch.4 as its own section |
| 5.A.1 | ✅ DONE (2026-06-15) | New §2.3 "Evaluation Dataset Selection" added to Ch.2 before Models Used (from `datasets/Dataset_Analysis_Report.md`): 6-dataset comparison table + MIRACL justification (hard negatives, native queries, scale) + MSA-only limitation → Ch.5. Citations **web-verified** and added: `clark_2020_tydiqa`, `abdallah_2024_arabicaqa`, `sen_2022_mintaka`, `hasan_2024_nativqa`, `mozannar_2019_arabic` |
| 3.1 | ✅ DONE (2026-06-15) | Decorative-citation audit (3 subagents → findings I web-verified). **Found 4 more fabricated bib author/title fields** (same pattern as WS6) and fixed them: `alwajih_2024_swan` (real: Bhatia/Nagoudi/El Mekki/Alwajih/Abdul-Mageed), `macmillanscott_2025_generative` (Özyiğit Eda B., not Ali H.), `liu_2025_exp4fuse` (Zhang, not Guo), `sengupta_2023_jais` (Bokang/Koto + real co-authors). Decorative-claim fixes: Query2Doc "OPT-1.3B/6.7B" → softened; GaQR "4–9x" → softened. Left Pyserini/QLoRA titles (verified correct / cosmetic). |
| 3.2 | ✅ DONE (2026-06-15) | Fabricated-rationale audit of Ch.3. **SILMA 2.5% VERIFIED correct** (0.5177 vs 0.5052) — known residual closed. Fixed ALLaM precision NF4→FP16 in Table 3.2 + dropped ALLaM from the NF4 list (internal contradiction with §2.4's "14.5 GB FP16"). Left Jais-2 Table 3.2 temp/batch (agent evidence was planning docs, not the run log; thesis internally consistent). All other Ch.3 numbers traced to experiment docs — clean. |
| 3.3 | ✅ DONE (2026-06-15) | Model-descriptor audit vs official cards. Fixed: Aya "101 languages"→**23** (ch2 + 2× ch4) + win-rate "83.9%" softened; Qwen 2.5-3B license Apache 2.0→**Qwen Research** (prose + table); SILMA RAGQA 0.3575→**0.3478**; Jais-2 SFT "4M Arabic/10M English" softened; ALLaM "6M samples/245K pairs/540B tokens" softened; Qwen3-4B "eight named Arabic dialects" softened. Left (verified OK or name-bound): SILMA "2B" (model name), Gemma "~10 pts below Falcon OALL" (corroborated by Falcon blog), internal VRAM measurements. |
| 3.5 | ✅ DONE (2026-06-15) | Estimation-vs-measurement sweep folded into 3.2: no unrecorded fabricated runtime/multiplier siblings remain in Ch.3 (16×/8×/2× already removed; ~40 min and ~8 h are measured). |
| 5.B.5 / 5.B.10 / 5.A.7 / 5.F.2 / 5.F.3 | ✅ CLOSED (bookkeeping, 2026-06-12 audit) | Already satisfied in text — see 2026-06-12 §D |

### Self-initiated changes (not from task list)

None remaining — the Both-expanded numeric change (0.6959→0.6936 / −0.0178→−0.0201) was reverted after review confirmed it had no source in the meeting notes or review document.

### Still pending (not touched)

Updated 2026-05-31 evening — after WS1 completion + figures pipeline render:

**Newly unblocked / ready to apply:**
- **Track A — thesis text edits** per `STREAM_1_COMPLETION_REPORT.md` §3 (Mohammed, next session). Specifically §4.2.1/2/3 numeric corrections (failure rate, length table, coverage), §3.3 token→word relabel + 1.4 signpost paragraph, §4.10 rewrite (failure paragraph + length-bucket Medium fill + first-pass top-1 wording), supporting MD doc sync. **Estimated: ~3 hours focused writing.**
- **WS5.C.20** (Medium length row `---`): now fillable from Mohammed's CSV (Scheme A Medium: blind 0.506 → CSQE 0.703).
- **WS5.C.16** (demote meta-description failure mode): aligns with 1.1 outcome — "1 genuine failure = meta-description" framing is gone; replaced by 58 regressions.

### 2026-06-01 — figures session 2 (color upgrade + Osman feedback consolidation)

| Action | Status | Notes |
|--------|--------|-------|
| Color palette + FontAwesome icons in TikZ | ✅ DONE | New shared `system_diagrams/_style.tex` (7-color semantic palette + icon helpers); all 12 TikZ diagrams upgraded; mplstyle prop_cycle now teal-first. Fig 4.11 best-system bar pops in deep teal. |
| Fill Osman's 5 models in `model_comparison_dense.csv` | ✅ DONE | Source: `arabic-rag-query-enhancement/docs/OSMAN_MODEL_COMPARISON_RESULTS.md`. All 5 now have full R@10/R@100/MRR. Notebook 03 re-executed; Table 4.2 + Fig 4.5/4.6 refreshed. |
| Compile remaining tables (2.1, 2.2, 3.1, 3.2, 4.6) | ✅ DONE | Source CSVs in `thesis_figures/data/raw/`; LaTeX snippets in `thesis_figures/output/pdf/`. 5 tables × ~10 rows each. |
| Archive 5 figures per Osman ("clear concepts ≠ diagrams") | ✅ DONE | Archived: Fig 2.1 (RAG arch), 2.2 (QE taxonomy), 2.3 (Dense vs Sparse), 3.2 (MIRACL dataset), 3.6 (BM25 repetition). Sources kept in `thesis_figures/archive/system_diagrams_dropped/` with rationale README. Down from 12 system diagrams to 7. |
| Update REVIEW.html + master README | ✅ DONE | Reflects archived figures, compiled tables, color upgrade. |

#### Figures-track status summary (2026-06-01 evening)
- **10 figures × ~28 variations** (Fig 4.1–4.15) + **7 system diagrams** (Fig 3.1, 3.3, 3.4, 3.5, 3.7, 3.8, 3.9) = **all rendered**, all in canonical post-WS1 data, all colorised.
- **12 of 12 thesis tables** have either source CSV + LaTeX snippet ready, or are produced by a notebook (Tables 4.1, 4.4, 4.5, 4.7 from notebooks; Tables 2.1, 2.2, 3.1, 3.2, 4.6 from hand-compiled CSVs).
- Only critical-path items left for the figures track: **embedding into chapter .tex** with `\includegraphics{}` + `\caption` + `\label` (Mohammed) and Track A text edits.

**Open tasks (status unchanged):**
- **WS4 (Osman):** 4.3–4.17 — most still need verification (4.8 first-pass definition is now resolved by 1.3).
- **WS5.C.2:** Pearson/Spearman for Qwen family — small computation, can do locally.
- **WS5.C.17:** big-win example texts (الرباط المنصوري, John Dewey, Nicolas Boileau) need qualitative verification — not derivable from the CSV.
- **WS5.D.1:** Mohammed's Ch.5 deep-dive recording was incomplete.
- **WS3.1–3.3:** ✅ DONE (2026-06-15) via three verification subagents + my web-verification — see the "Completed tasks" table and the 2026-06-15 (cont.) entry.
- **WS5.A, 5.E, 5.F:** blocked on supervisor Q2/Q3 (Ch.1/abstract rewrite).
- **Hand-compile data:** Tables 2.1, 2.2, 3.1, 3.2, 4.6 + R@10/R@100/MRR for Osman's 5 models in Table 4.2.
- **Visual upgrade of figures (optional):** see `thesis_figures/README.md` "Visual feedback" section. Not on the critical path.

---

### 2026-06-10 — Apply pass: WS1 (Track A) + WS4 + WS6 + ready WS2/3/5 items into the thesis

Grouped-by-file edit pass to fold all settled verification/research outcomes into the LaTeX so the next supervisor draft is internally consistent. Source reports: `STREAM_1_COMPLETION_REPORT.md`, `WS4_VERIFICATION_REPORT.md`, `WS6_RESEARCH_REPORT.md`.

**DONE — `References.bib`**
- Fixed all **10 fabricated entries** (WS6 6.4 + WS4 4.15): `aya_2024` (was MRI-paper URL → arXiv 2412.04261, correct title/authors), `yoon_2025_llm_retrieval`, `zhang_2024_mugi`, `lei_2024_csqe`, `lei_2025_thinkqe`, `yang_2025_aqe`, `zhang_2025_pbr`, `xia_2025_kar`, `young_2024_gaqr` (Orion→Oliver), `louis_2024_query` (→`@mastersthesis`, author Bhusal).
- Added: `macmillanscott_2025_generative` (6.1), `liu_2025_exp4fuse` (6.2), `qwen3emb_2025` + `alwajih_2024_swan` (6.5).
- **Decision #2 honoured:** the 11 orphaned entries were **kept** (harmless; deletion deferred).

**DONE — `chapter2.tex`**
- WS6 6.4e prose corrections: MuGI rewritten (Multi-Text Generation Integration + tie-in to our β repetition), **Yoon recharacterised as a skeptical "knowledge-leakage" counterpoint** (was misrepresented as supporting), Xia/Yang/ThinkQE/PBR claims corrected, "Louis and Bhusal" → "Bhusal".
- 6.1 gap narrowed to **monolingual** Arabic + Macmillan-Scott cited as concurrent corroboration (§2.4 l.~393 + research-gap item 1).
- 6.2 gap reframed + **Exp4Fuse** cited as nearest prior art (§2.4 research-gap).
- 5.A.5: removed the decorative Alsubhi (paper-12) citation at the morphological-gap sentence.
- 5.A.6: verified §2.3.2 BM25S params already consistent (k1=0.9/b=0.4) — no edit needed.

**DONE — `chapter3.tex`**
- §3.3 length buckets "tokens" → "words" (WS1 1.2); added three-threshold-systems **signpost paragraph** + 0.3/0.7-are-pragmatic note (WS1 1.4 / WS4 4.14).
- Fixed first-pass-quality definition **top-5 "≥1 relevant" → top-1, qrel≥1** (WS4 4.8 / WS1 1.3) in §3.9 methodology.
- 5.B.8: added the **exact CSQE system prompt** (verbatim, from exp_013 notebook) to §3.8, mirroring the §3.5 blind-prompt quote.

**DONE — `chapter4.tex`**
- **§4.2 numeric corrections (WS1 §2)** from the canonical pytrec_eval run: segmentation 39/56/5% → **33.9/33.2/32.9%** (n 982/962/952; per-category avg 0.053/0.511/0.948); nDCG=0 count 192 → **736**; length table → **0.345/0.511/0.476** (words; non-monotonic, 28% gap); correlation +0.125 → **≈ −0.01**; coverage 93.4/96.7/98.8/99.4 → **74.6/80.8/86.9/90.1%**, reframed as a **recall ceiling** motivating hybrid (decision #4).
- 5.C.2: added **Qwen-family correlation** (Pearson r=0.94, Spearman ρ=1.00) + cross-model confound caveat in §4.5.1.
- 4.4 / 5.C.3: §4.5.3 generic "Arabic NLP benchmark" → **OALL**.
- **§4.10 rewrite:** failure paragraph "257/258 irretrievable / dataset ceiling" → **0 irretrievable, 199 missed-by-all + 58 BM25-retrievable-but-lost** (WS1 1.1 / WS4 4.11); fixed caption "Both-expanded" → **BM25-expanded** + reconciled 0.6936 per-query vs 0.7137 corpus-level (4.17); heading "Dominant Predictor" → **"Largest Modulator"**, first-pass = top-1 (4.8/4.14); length-split table → **Scheme A (1–3/4–8/9+)**, Medium row filled (5.C.20); **big-win trio replaced** (الرباط المنصوري / الأسماء الخمسة / الفن الجزيري) with blind-poisoning framing (4.12/5.C.17); **Type B reframed to general first-pass-poisoning mode** with 3 representative examples (4.13); implications converted to a forward-pointer to Ch.5 recs (5.C.19).

**DONE — `chapter5.tex`**
- §5.1 baseline recap aligned (34%, short=72% of long, r≈0); OALL standardisation + size-confound note; **conclusion reorder (5.D.4)** — "Overall" paragraph moved to **close** §5.1, augmented with the 0.4621→0.7137 headline.
- §5.2: ALLaM sentencepiece (`▁`) disclosure already present; **added MIRACL no-metadata limitation** (5.D.2).
- §5.3: Rec 2 + Rec 8 embedding update — keep BGE-M3, replace dated mE5-large with **Qwen3-Embedding-8B + Swan-Large** + validation caveat (6.5). (First-pass-gate + asymmetric-weighting recs already present as Recs 6–7, so 5.C.19's "move from §4.10" is satisfied.)

**DONE — `chapter1.tex` + abstracts (consistency-only, NOT the Q2-gated reframe)**
- Ch.1: reviewed — carries none of the changed numbers/claims; counts already consistent ("ten" 2–8B models + GPT-OSS surveyed separately). **No edits required.**
- 5-Abstract.tex / 6-ARAbstract.tex: 39% → **34%** failure rate; "significant short-query gap" → "pronounced underperformance of very short queries" (EN + AR). Headline result numbers (0.7137 / 54.5% / 13.9%) already correct.

**DONE — supporting docs**
- `error_analysis_phase1_quantitative.md`: added a **correction banner** with the corrected §4.2 table (the doc body still holds the old buggy numbers — banner says use thesis values).
- `exp_error_analysis_csqe.md`: already carried WS1 Task-1.1 correction banners (no new edit).

---

#### LEFT / DEFERRED / NEEDS A DECISION

- **GPT-OSS deletion (5.A.8) — ✅ RESOLVED 2026-06-15: deleted completely** (prose + generated tables + bib + counts eleven→ten). *(Original deferral rationale, kept for history: it conflicted with the "include negative results" principle and required touching the generated table snippets `table_2_2.tex` / `table_2_2_models.csv` alongside the prose; the user confirmed deletion, so it was done coordinated across all locations. See the 2026-06-15 entry.)*
- **5.C.9 / 5.C.21 (structural moves) — ✅ DONE 2026-06-15.** Hybrid-no-QE added to §4.1 baselines; "Summary of All Experiments" table moved to chapter end. (No broken cross-refs; verified.)
- **Supervisor-gated — not touched:** Ch.1 problem-statement reframe (5.A.3 / 5.E.1 / 5.E.3 / 5.E.4) and the full abstract rewrite (5.F.1) await Dr. Tahani's Q2/Q3/Q5. Only consistency fixes were applied to Ch.1/abstracts.
- **5.A.1 (dataset-analysis section) / 5.A.4 (QE-families expansion) — ✅ DONE 2026-06-15.** 5.A.4 in the GPT-OSS pass; 5.A.1 after the user supplied `datasets/Dataset_Analysis_Report.md`, added as §2.3 with web-verified citations.
- **4.16 (dead table/figure labels):** do after figures are embedded/finalised.
- **WS3.1–3.3 broad sweeps:** ✅ DONE 2026-06-15. The exhaustive decorative-citation, fabricated-rationale, and model-descriptor sweeps were completed via three subagents whose findings I web-verified before applying. Notably caught 4 more fabricated bib author/title fields + several wrong model-descriptor facts (Aya 23 langs, Qwen2.5-3B license, SILMA RAGQA). See the 2026-06-15 (cont.) entry below.
- **Residual:** `exp_error_analysis_csqe.md` big-win example table still lists the old John Dewey trio (banner-covered; thesis now uses the verified trio).

---

#### ⚠️ FIGURE CONCERns (for the later figures session)

1. **Three §4.2 figures must be regenerated from the canonical run — the text is now AHEAD of them:**
   - **Fig 4.2** (`fig_4_2_failure_cliff_v1.pdf`): built on the buggy per-query nDCG; the whole distribution shifts and the "39%" annotation is now **34%**. Regenerate from the canonical run, and consider softening the "failure cliff" name (the distribution is now ~34/33/33, not a cliff).
   - **Fig 4.3** (`fig_4_3_length_box_v1.pdf`): new bucket means **0.345 / 0.511 / 0.476**, axis label "words" not "tokens".
   - **Fig 4.4** (`fig_4_4_recall_curve.pdf`) / coverage: must reflect the corrected coverage (90.1% @100, not 99.4%).
2. **Fig 4.13 / 4.14 are OK:** Fig 4.13 caption already uses top-1 (0.8877/0.5814); Fig 4.14 already uses the 1–3/4–8/9+ buckets — the §4.10 table was updated to match it this session.
3. **Figures rendered but not yet `\includegraphics`-embedded/verified.** Confirm every `fig_*` PDF referenced in Ch.2–4 exists and is the **post-WS1** version before compiling the supervisor draft.
4. **GPT-OSS lives in the generated Ch.2 tables** (`table_2_1.tex`, `table_2_2.tex`, `table_2_2_models.csv`). If GPT-OSS is deleted (5.A.8), these must be regenerated together with the prose, or the table will contradict the text.
5. **Big-win "golden diagram"** (WS4 4.12 suggested الأسماء الخمسة as a worked blind-vs-CSQE figure) is **not** implemented; the examples are currently an inline table only.
6. Verify the hand-compiled tables (2.1, 2.2, 3.1, 3.2, 4.6) did not inherit any of the corrected §4.2 numbers (they shouldn't have, but confirm during the figures pass).

---

### 2026-06-12 — Apply-pass verification audit (research only; no thesis edits made)

Audited the uncommitted 2026-06-10 apply pass (git diff vs HEAD) against this task list. **All edits claimed DONE in the 2026-06-10 log are confirmed present in the .tex/.bib files** (spot-verified: §4.2 corrected numbers, §3.3 words+signpost, §4.10 rewrite incl. failure paragraph / big-win trio / Type-B reframe / "Largest Modulator" / Medium row, CSQE prompt in §3.8, first-pass top-1 in §3.9, OALL conversion, Qwen correlation, References.bib fixes incl. `aya_2024`, abstract 34% fix, Ch.5 reorder + MIRACL-metadata + embedding-model update). Sweeps re-verified clean: no "Phase 4", no exp-number refs, no Config A/B/C, no unjustified "statistically", no 0.9466, abstract closing numbers 0.7137/54.5/13.9 correct in EN+AR.

#### C. GAPS — ready to apply but neither applied nor recorded as deferred (fix the bookkeeping or apply next session)

| Item | Status found | Action needed |
|------|-------------|---------------|
| **5.A.2** hybrid-equation move | **ORPHAN — not applied, not recorded.** RRF + CC equations still live in §2.1.3 Hybrid Retrieval (`chapter2.tex:80–92`, `eq:hybrid_cc_ch2`), not in §2.2 Mathematical Models. Pure edit, no dependency. | Apply (move or duplicate-with-pointer), or explicitly defer. |
| **5.E.2** ten-vs-eleven | **Mislabelled as supervisor-blocked; it is not.** Real inconsistency exists: abstract says "Ten … were evaluated" but `chapter2.tex:229` ("the eleven LLMs evaluated"), `:452` ("systematic evaluation of eleven"), `:467` ("Eleven … described"), and `chapter5.tex:45` ("Two of the eleven models evaluated") all use eleven without the "surveyed 11 / evaluated 10" framing the task prescribes. | Apply the 10/11 convention edit (independent of Q2/Q3). |
| **5.C.11 restore** | **Unrecorded [DECIDE].** WS4 verified both 4.9 (~1,500 chars: mean 1486/median 1530) and 4.10 (mDPR = MS-MARCO-fine-tuned, short queries; cite Bajaj et al. 2016) AFTER the claims were dropped via the fallback path. WS4 report explicitly says the §4.8 dense-degradation explanation "can now be restored with a verified source if desired". | Decide: restore with citations, or keep dropped. |
| **7.2** Gemini brief verification | **Never logged anywhere.** Likely mooted: WS1 1.3 re-ran the per-query analysis from raw outputs (the brief-distrust motivation), and WS4 4.17 spot-checked the brief's numbers. | Record explicit close-out (recommend: CLOSED — superseded by WS1.3 + WS4.17) or run it. |
| **5.C.5** Ch.4 table audit | Implicitly deferred behind figure embedding via the 4.16 team decision, but never named in the LEFT list. | Add to deferred list: do together with 4.16 after figures are embedded. |

#### D. Bookkeeping closures — already satisfied in the text but never marked done

- **5.B.5** SILMA temperature: `chapter3.tex:325` already reads "(0.7 and 0.1)" matching WS4 4.3. ✅ CLOSE. ⚠️ Caveat: the same sentence claims "0.1 yielded a 2.5\% improvement" — the 2.5% figure was NOT verified by 4.3 (only the two pkls' existence was). Flag for the WS3.2 fabricated-rationale sweep.
- **5.B.10** retrieval depth: `chapter3.tex:404` says top-100, matching WS4 4.6 (verified top-100 everywhere). ✅ CLOSE.
- **5.A.7** Song & Zheng: WS6 6.3 verdict = KEEP (entry correct, taxonomy matches §2.4). Citation stays; no edit needed. ✅ CLOSE.
- **5.F.3** Arabic abstract numerals: `6-ARAbstract.tex` consistently uses Western/ASCII digits (2,896 / 34\% / 0.7137 / 54.5\%); convention is internally consistent. ✅ CLOSE (matching existing convention = ASCII).
- **5.D.2 (Wang precedent sub-item):** Ch.5 challenge 2 already acknowledges "the query repetition strategy recommended by the original Query2Doc paper" — substantively applied. Optional polish: add explicit `\cite{wang_2023_query2doc}`.
- **5.F.2** closing numbers: verified correct in both abstracts. ✅ CLOSE.

#### E. Stale notes inside this file (superseded; do not act on them)

- The 2026-06-01 "Open tasks (status unchanged)" block still lists WS4 4.3–4.17 as needing verification, 5.C.2 + 5.C.17 as open, and hand-compile tables as pending — **all superseded** by WS4 completion (2026-05-30/31), the 2026-06-10 apply pass, and the 2026-06-01 table-compile session respectively. The blanket "WS5.A, 5.E, 5.F blocked on supervisor" is too broad: only 5.A.3 / 5.E.1 / 5.E.3 / 5.E.4 / 5.F.1 / 5.F.4 are genuinely gated.

#### F. Minor polish candidates (optional, non-blocking)

- `chapter4.tex:400`: "a multilingual model with a lower Arabic benchmark score" → "lower OALL score" for full 4.4-sweep compliance (OALL is named earlier in the same sentence, so low risk either way).
- `chapter2.tex:151`: generic formula text says "typically $k_1 = 1.2$, $b = 0.75$" — fine as textbook description since the §2.3.2 Notation paragraph pins the operative k1=0.9/b=0.4, but be aware it's the last remaining "other" BM25 parameter mention.

---

### 2026-06-15 — GPT-OSS removal + remaining deferred items applied

User instruction: delete GPT-OSS completely (10 models, not 11); apply all remaining deferred items except those gated on supervisor questions or figures; apply the ready tasks surfaced by the 2026-06-12 audit; mark everything done. All edits are in the .tex/.bib (see the "Completed tasks" table above for the per-item rows).

**Applied this session:**
- **5.A.8 — GPT-OSS deleted completely**, with all indirect references adjusted to **ten models**: Ch.2 (Experimental-Models subsection + §2.4.10 + model-comparison table row/footnote + counts), Ch.3 (category list, config table, model-issues bullet, quantisation sentence, work-division), Ch.4 (dense-leaderboard dropped row, "Dropped Models Analysis" → ALLaM-only, summary-table row), Ch.5 (challenge 3 → ALLaM-only), generated `table_2_2.tex` + `table_2_2_models.csv`, and the orphaned `gptoss_2025` entry removed from `References.bib`. Verified: zero "GPT-OSS"/"eleven"/`sec:gptoss` matches remain in the .tex.
- **5.E.2** resolved by the above (consistent "ten" everywhere).
- **5.A.2** hybrid equations moved to §2.2 (`sec:hybrid_math`). **5.A.4** QE-techniques expanded to four families. **5.C.9** hybrid no-QE reference baseline added to §4.1. **5.C.21** summary table moved to chapter end. **5.C.11** dense-degradation explanation restored with `bajaj_2016_msmarco`. Polish F applied (OALL phrasing; Wang cite).

**2026-06-12 audit gaps — now closed:**
- 5.A.2 ✅ applied · 5.E.2 ✅ applied · 5.C.11 ✅ restored.
- **7.2 (Gemini brief verification): CLOSED — superseded** by WS1 1.3 (per-query analysis re-run from raw outputs) + WS4 4.17 (brief headline numbers spot-checked). Not run; no longer needed.
- **5.C.5 (Ch.4 table audit): DEFERRED** — bundle with **4.16** (dead table/figure labels) and do **after figures are embedded** (team decision under 4.16). Figure-gated, so out of scope for this pass.

**5.A.1 — now DONE (later in the same session).** The user supplied `datasets/Dataset_Analysis_Report.md`, removing the fabrication risk. A focused §2.3 "Evaluation Dataset Selection" was added to Ch.2 (6-dataset comparison table + MIRACL justification + MSA-only limitation). All five new dataset citations were **verified on the web against primary sources** (arXiv/ACL Anthology) before being added to `References.bib` — not taken from the report uncritically.

**Still genuinely blocked (unchanged):**
- Supervisor-gated: 5.A.3 / 5.E.1 / 5.E.3 / 5.E.4 (Ch.1 reframe), 5.F.1 / 5.F.4 (abstract rewrite/translation) — await Dr. Tahani Q2/Q3/Q5.
- Figure-gated: 4.16 + 5.C.5 (after embedding); **§4.2 figures (Fig 4.2/4.3/4.4) still need regeneration from canonical data** — thesis text is ahead of them. GPT-OSS is now gone from prose + generated tables, so the model tables (2.2) are consistent.

---

### 2026-06-15 (cont.) — WS3.1–3.3 AI-pattern sweeps (subagents + my web-verification)

Three `general-purpose` subagents were dispatched (one per sweep) to *report findings only*; every ❌/⚠️ recommendation was then re-verified by me against the primary source before any edit (the agents are auditing for fabrication, so I did not trust their corrections blindly — and indeed had to discard a couple of over-corrections, e.g. the Pyserini title).

**Highest-value catches (all verified, then fixed):**
- **More fabricated citations** (same "correct URL, wrong author/title" pattern WS6 found) — including in 3 entries *I myself added last session*: `alwajih_2024_swan`, `macmillanscott_2025_generative`, `liu_2025_exp4fuse`, plus pre-existing `sengupta_2023_jais`. All corrected against arXiv author lists I fetched directly.
- **Wrong model facts:** Aya Expanse is **23 languages, not 101** (101 = the older Aya-101; this propagated into 2 Ch.4 sentences used to *explain* the BM25 result); **Qwen 2.5-3B is the Qwen Research License, not Apache 2.0**; **SILMA RAGQA = 0.3478, not 0.3575**.
- **Ch.3 internal contradiction:** ALLaM listed as NF4-quantised in Table 3.2 but FP16 (14.5 GB) in §2.4 → fixed to FP16.
- **SILMA 2.5% temperature claim VERIFIED correct** (0.5177 vs 0.5052) — closes the long-standing residual.

**Deliberately NOT changed (verified OK or too risky to assert a replacement):** Pyserini/QLoRA bib titles (correct/cosmetic); Jais-2 release date + Table 3.2 temp/batch (project records say Dec 2024 / the thesis is internally consistent; agent evidence was planning docs, not run logs); SILMA "2B" (matches the official model name); Gemma "~10 pts below Falcon on OALL" (corroborated by the Falcon blog); internal VRAM measurements (legitimate, just unsourced). Unverified specifics (ALLaM 6M/245K, Jais-2 SFT split, GaQR multiplier, Query2Doc model names) were **softened/removed** rather than swapped for an unconfirmed number.

Net: WS3 is the last non-supervisor/non-figure workstream. Remaining open work = supervisor-gated Ch.1/abstract reframe and the figure track only.

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
