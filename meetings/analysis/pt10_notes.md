# pt10 Analysis Notes — Part 10 (final)

**Source:** `meetings/pt10.md` (heavy duplication after ~line 245; unique substantive content is lines 1–245)
**Speakers:** Mohammed, Osman
**Coverage:** Continuation of **P4.4.23**, then **P4.4.24, P4.4.25, P4.4.26, P4.4.28**, then a brief sweep of **P4.5.x** conclusions/recommendations. Recording ends with the explicit statement that Ch.5 was not fully walked through.
**Notable:** Mohammed pulls apart the Type A/B regression classification and finds the threshold logic questionable. They confirm the per-query analysis section is useful enough to keep (despite Osman's earlier deletion proposal in pt9). The recording ends with an off-topic tangent about Claude Code usage limits.

---

## Per-Item Discussion & Decisions

### Item P4.4.23 (revisited from pt9) — Three big-win examples

**Discussion (presentation issues):**
- They re-examined the table format. Current issues:
  - **Mixed Arabic and English** in the same table → unclean.
  - **Summary text instead of actual expansion content** → not citable, not directly inspectable by a reader.
  - **Too compact** for the level of detail needed.
- Their preferred format:
  - All English (with the query as Arabic but explained in English).
  - Show the actual blind QE expansion and CSQE expansion side-by-side, not a summary.
  - **Move to appendix** if it doesn't fit cleanly in Ch.4 — or have a short illustrative version in Ch.4 with the full version in the appendix.
- Per-example verdict (consolidating pt9 + pt10):
  - **الرباط المنصوري:** strongest. Intuitive (blind interprets it as "ligament/surgery"; CSQE correctly identifies the Mamluk caravanserai because the corpus disambiguates). Keep.
  - **John Dewey & Nicolas Boileau:** uncertain. Mohammed: "I'm honestly not sure about the second and third examples — if there are better ones, swap them in."
- Both reaffirmed: the *purpose* of these examples is to make the value of corpus grounding **intuitive** for the reader. They must succeed at that bar; the current second and third examples don't clearly meet it.

**Decision:** **REVISE — multi-part:**
1. Reformat the table: all English, side-by-side blind vs CSQE expansion content (not summaries), and consider moving to appendix (or short version Ch.4 + extended in appendix).
2. **Keep الرباط المنصوري** as the lead illustration.
3. **Replace or verify** John Dewey and Nicolas Boileau examples — search the per-query results for stronger illustrative pairs. If equivalent or better candidates exist, use them.
4. The intuition principle is the selection criterion, not just statistical magnitude of improvement.

---

### Item P4.4.24 — "First-pass recall as the dominant predictor of CSQE effectiveness"

**Discussion (deep dive — they critique the analysis):**

Mohammed walked through the AI's regression analysis section and identified several logical issues:

- **What the AI did:** classified the 376 regression cases into Type A (strong BM25 hurt by expansion) and Type B (poisoned first-pass — BM25 retrieved irrelevant documents that contaminated the LLM expansion).
- **Mohammed's first concern (threshold rationale):** the AI uses **BM25 baseline > 0.3** as the cutoff for "BM25 already handled the query well." But the dataset's average BM25 baseline is around **0.6–0.7**. So 0.3 is well below average — calling it "well handled" is misleading. A query with baseline 0.3 is mediocre, not strong.
- **Mohammed's second concern (analytical scope):** the AI tested two extremes (strong BM25 and weak BM25) and found *both* had problems. But it didn't actually identify a root cause — it just recommended "rely more on blind in both cases." That's not a causal analysis; it's a uniform fallback.
- **Osman's defence:** "the recommendations that come out of the analysis are useful, even if the analysis itself isn't a clean root cause story."
- **Both agreed:** the recommendations (first-pass quality gate, asymmetric expansion weighting) are **valuable additions**. The analysis methodology behind them deserves verification but the output is acceptable.

**Decision:** **REVISE WITH VERIFICATION:**
1. **Soften "dominant predictor" wording** to "the largest observed modulator" or similar (matches the brief's recommendation) since no formal regression analysis was actually performed.
2. **Verify the threshold rationale** — why 0.3? If there's no good reason, either change to a more defensible cutoff (e.g., median BM25 baseline) or just describe the threshold descriptively without claiming it represents "well handled."
3. **Keep the two recommendations** (first-pass quality gate, asymmetric expansion weighting) but move them to Ch.5 (per P4.4.26 below).
4. **Don't oversell the analysis** — present it as exploratory observation that motivates two specific improvement directions, not as a definitive root-cause investigation.

---

### Item P4.4.25 — Arabic regression example (ما هو التطرف retrieving لهجة جنوبية)

**Discussion:**
- Mohammed and Osman confirmed the example is illustrative: the BM25 stemmer/tokenizer matched "ما هو" (interrogative "what is") with a dialectal usage of the phrase, surfacing irrelevant articles about southern Arabic dialects rather than about "extremism."
- The CSQE expansion then becomes grounded in the dialect content, propagating the error — a clean illustration of Type B (poisoned first-pass).
- Verification needed: confirm the actual top-1 result for this query was indeed the dialect article.

**Decision:** **VERIFY then APPROVE** — confirm the actual retrieval behavior on this specific query. If correct as described, keep as the Type B example.

---

### Item P4.4.26 — Recommendations embedded in §4.10.4 (move to Ch.5)

**Discussion:**
- Both agree the implications/recommendations should **move to Ch.5**. Embedding them in Ch.4 results is unusual and creates duplication if also included in Ch.5.
- The two specific recommendations to move:
  - First-pass quality gate (fall back to blind QE when top-1 BM25 has low lexical overlap with the query).
  - Asymmetric expansion weighting (lower expansion weight when BM25 is already strong).
- They also walked Ch.5's existing recommendations and found duplication risk:
  - **Knowledge-base-aware QE:** already mentioned earlier in the thesis → DELETE from Ch.5 to avoid repetition.
  - **Multi-stage QE:** new → KEEP in Ch.5.
  - **Few-shot and chain-of-thought prompting:** new → KEEP in Ch.5.
  - First-pass quality gate, asymmetric expansion weighting: NEW (moved from §4.10.4) → ADD to Ch.5.

**Decision:** **REVISE — Ch.5 recommendations cleanup:**
1. **Move** the two §4.10.4 recommendations to Ch.5.
2. **Delete** any Ch.5 recommendation that is already mentioned elsewhere in the thesis (specifically: Knowledge-base-aware QE).
3. **Keep** Multi-stage QE, Few-shot/CoT prompting, the two new ones from §4.10.4, and the existing strong-retrievers recommendation (BGE-M3 / mE5-large).
4. Reorder so each recommendation appears only once, with a clear logical sequence.

---

### Item P4.4.27 — Medium query-length row with "—" entries

**Discussion:** Not explicitly addressed in pt10 (but the principle was implicitly accepted: don't show empty rows).

**Decision (carried from brief recommendation):** **REVISE** — either populate the Medium row (data exists in the error analysis doc) or drop the row entirely. Don't print "—".

---

### Item P4.4.28 — Plan to add Phase 4 rows to Table 4.10 (full summary)

**Discussion (table layout decisions):**
- Mohammed and Osman opened the actual table (Table 4.5.6 / "summary of all experiments"). They had previously observed it's "ugly" with phase-4 rows tacked onto the bottom.
- The brief asks: combine Phase 4 rows into the existing table, or split into a dedicated Phase 4 summary table?
- They prefer either:
  - (a) Put summary tables in the **appendix** (cleaner main thesis flow), OR
  - (b) Put the summary at the **END of each chapter** (Mohammed: "summary always goes at the end").
- Currently the AI placed an "Overall" paragraph then added Phase 4 results AFTER it, which is structurally wrong — the overall should be the actual ending.

**Decision:** **REVISE — structural fix:**
1. **Move the summary table to the end of Ch.4** (or to the appendix). It should not appear in the middle.
2. **Move the "Overall" paragraph (and Phase 4 conclusions) to the actual end of Ch.5**, not before later content. Whatever is the last thing in the chapter is what the reader leaves with — make it the strongest summary statement.
3. **Phase 4 rows can integrate** into one combined summary table provided it doesn't overflow a page. If it does, split into two tables but keep them adjacent.

---

### Items P4.5.x — Conclusions Phase 4 Additions (cursory pass)

**Discussion (light coverage — meeting wound down before deep dive):**
- They scrolled through the conclusion paragraphs and recognized most content was already addressed in earlier transcripts.
- Re-affirmed:
  - **P4.5.1** (four new conclusion paragraphs after "Overall"): structurally wrong — fixed by P4.4.28 decision (move "Overall" to end, place new content before it OR redesignate the new paragraphs as the actual ending).
  - **P4.5.2** (terminology "retriever-specific representation"): keep, but reframe per pt7 P4.4.16 (less about Dense degradation, more about fusion complementarity).
  - **P4.5.3** ("any multi-retriever pipeline" overreach): SOFTEN — match the brief's recommendation. Replace with "similar hybrid pipelines" or drop the generalization.
  - **P4.5.4** (54.5% / 13.9% improvement headline): math correct → APPROVE.
  - **P4.5.5** (BM25 term-dilution challenge resolved in-place): APPROVE — good narrative move.
  - **P4.5.6** (new challenge: first-pass quality dependence): APPROVE.
  - **P4.5.7** (move Recommendations 2 and 4 to "now-implemented" note): superseded by their pt4 decision to **delete entirely** rather than note them.
  - **P4.5.8** (three new recommendations: first-pass quality gate, asymmetric expansion, stronger retrievers): APPROVE the three; note that ranking pioneer models (BGE-M3, mE5-large) need to be verified as still SOTA at submission time.
  - **P4.5.9** (recommendation ordering): APPROVE quality-gate-first ordering.

**Decision:** **APPROVE most P4.5.x items** with the cross-references to earlier decisions. **REVISE P4.5.3** (soften overreach). Mohammed explicitly closed by saying "Chapter 5 has my opinion — I think we'll finish it" but the recording ended before the deep walkthrough.

---

### Items P4.A.x and P4.X.x — Implicit / not directly addressed

**Discussion:** Most of these were addressed in pt5. The brief items remaining:
- **P4.A.2** (abstract internal consistency — earlier sentences may still describe pre-Phase-4 results): consistent with pt5 decision to rewrite the abstract from the corrected problem statement.
- **P4.A.3** (Arabic abstract numerals — Eastern vs ASCII): match existing convention. Need to check the existing Arabic abstract.
- **P4.A.4** (Arabic translation native review): same as A.5 from pt5.
- **P4.X.1** (CSQE terminology consistent): APPROVE.
- **P4.X.2** ("retriever-specific query representation" coinage): APPROVE — keep (per the pt7 decision to reframe meaning, not eliminate the term).
- **P4.X.3** ("meta-description failure mode" coinage): REJECT (per pt7/pt9 decisions to demote to illustrative example).
- **P4.X.4** ("Phase 4" project-internal terminology): REJECT (per pt5 decision to global-purge).
- **P4.X.5** (table caption formatting): APPROVE.
- **P4.X.6** (References.bib additions): VERIFY each entry, especially `zhang_2024_mugi`.
- **P4.X.7** (cross-reference labels): VERIFY usage.
- **P4.X.8** (Quick Reference numbers as single source of truth): spot-check 5–10 numbers against original experiment docs.

**Decision:** Mostly carried by earlier transcripts; final action items consolidated in the aggregated resolutions document.

---

## Cross-Cutting Insights & Action Items Raised in pt10

- **Per-query analysis section verdict:** despite Osman's pt9 proposal to delete it, after closer review they keep it because the recommendations it produces (first-pass quality gate, asymmetric expansion weighting) are valuable. Section stays but with critical edits per P4.4.24.
- **Table placement principle:** summary tables at the end of chapters or in the appendix; never in the middle (matches P4.4.28).
- **Concluding-paragraph principle:** what comes last is what the reader remembers. Reorder Ch.5 so the strongest statement closes the thesis.
- **Recommendation deduplication:** sweep the thesis for any recommendation appearing more than once; keep only one occurrence.
- **Big-win example intuition principle:** examples in §4.10 must be intuitive for a reader unfamiliar with the data, not just statistically large wins.
- **Ch.5 final pass:** Mohammed flagged he has more to say about Ch.5 — the recording ended before completing this. Note for the supervisor meeting prep or the next session.

---

## Items Touched But Deferred

- **Final Ch.5 review** — recording ended before completing this. Mohammed: "I have an opinion on Ch.5, want to finish it." Schedule for the next working session.

---

## Items Not Yet Discussed (END OF TRANSCRIPT SET)

Across all 10 transcripts, the following review items were touched only briefly or not at all:
- **3.12, 3.13** (work division, Table 3.2 model configs) — confirmed grounded but never deeply reviewed.
- **4.10, 4.11, 4.12** (Qwen generational comparison, "universally vs divergent" wording, Best Model Recommendations section) — partially covered.
- **A.4 final sentence wording** — addressed in pt5 (kept "practical").
- Most P4.X.x cross-cutting items — addressed cursorily.
- Final **Chapter 5 walkthrough** — the recording ended before this happened.

---

## End of pt10 — All transcripts processed
