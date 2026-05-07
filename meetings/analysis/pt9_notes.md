# pt9 Analysis Notes — Part 9

**Source:** `meetings/pt9.md`
**Speakers:** Mohammed, Osman
**Coverage:** **P4.4.21 (Wikipedia corpus integrity discovery), P4.4.22, P4.4.23, P4.4.26.** Meeting cuts short for prayer.
**Notable:** Possible **dataset/indexing integrity bug** discovered when probing P4.4.21. Osman raises the option of **deleting the per-query analysis section entirely** if the underlying issue is fixed. Reconfirmation of the Config C → Config A redo from pt5.

---

## Per-Item Discussion & Decisions

### Item P4.4.20 (re-confirmed) — Config C → Config A error analysis redo

**Discussion:** Brief — Mohammed re-affirmed: "we computed for Config C; we should have computed for Config A. We need to redo this." Same decision as pt5 and pt7. No new content.

**Decision:** Already decided — **REVISE** (per-query error analysis to be re-run for Config A).

---

### Item P4.4.21 — Failure mode analysis: "257 of 258 are irretrievable; relevant passage absent from Wikipedia corpus dump"

**Discussion (CRITICAL — possible dataset integrity issue):**

This drove the bulk of pt9. The team probed into what the AI's claim actually means and discovered something alarming.

- **What the claim means:** The 258 "failure" queries have **nDCG@10 = exactly 0** — not just below 0.1, but literally zero. A nDCG@10 of 0 implies that none of the relevant (qrel-judged) documents appeared in the top-10 retrieved.
- **What the AI says caused this:** the relevant passage is **absent from the Wikipedia corpus dump used for indexing**. If true, no retrieval method (regardless of QE) could ever find these documents because they were never indexed.
- **What this implies:** if the Wikipedia corpus the team indexed is missing documents that MIRACL marked as relevant, that's a **data preprocessing bug**. It would mean their entire evaluation may have a small but real systematic error against the official MIRACL benchmark.
- Both reactions:
  - Osman: "this is strange — relevance to a query should at least give a small score, not exactly zero."
  - Mohammed: "we should investigate. If the dataset is wrong from the beginning, we'd hide it [i.e., redo the indexing]."
- Mohammed pulled up the AI's added cell ("a cell to perform this verification") — confirmed the AI had already proposed an investigation step in the analysis.

**Decision:** **REVISE — multi-part investigation:**
1. **Run the verification cell** the AI proposed: check whether the relevant qrel documents for the 258 failure queries are actually present in the indexed Wikipedia corpus.
2. If they ARE present → the AI's "irretrievable" explanation is wrong; the failure is something else (true model failure to rank them in top 10). Update the explanation.
3. If they are NOT present → investigate the corpus preprocessing pipeline. Identify what went wrong (e.g., document length filter, encoding issue, deduplication). Reindex if necessary and re-run baselines.
4. **DO NOT print** the "257 of 258 are irretrievable" claim until verified. This is a flagged data-integrity item.

---

### Possible REMOVAL of per-query analysis section (Osman's proposal)

**Discussion (separate from any specific item):**
- Osman raised a structural objection: "the per-query analysis at the end of all our work is illogical. Normally, an error analysis is done at the **start** to identify a problem we then solve. We did one at the start to motivate Query2Doc. But the Phase 4 per-query analysis is done at the end, just to display problems — without follow-up work. That's not very meaningful."
- Mohammed: "valid point. It would make our work look exhausted [in a good way], but if it doesn't lead to action, maybe we should drop it entirely."
- Joint thinking: if they fix the dataset integrity issue (P4.4.21 above), or if they delete the per-query analysis section, several Phase 4 items collapse (P4.4.20–P4.4.27 mostly).

**Decision:** **OPEN — consider deleting Section 4.10 (per-query error analysis) entirely.** Tradeoffs:
- Deletion pros: avoids the Config A vs Config C redo work, avoids the data-integrity investigation, removes weakly-motivated content.
- Deletion cons: loses the recovery-rate insights (56.8% improved by CSQE) and the first-pass dependence finding.
- **Action:** investigate the dataset integrity first. If it's resolved cheaply, decide based on remaining content quality. If it's expensive to fix, deletion becomes more attractive.

---

### Item P4.4.22 — "Meta-description failure mode" for single-case CSQE failure (qid=1060)

**Discussion:**
- They confirmed: this is a single failure (1 query out of 2,896). Naming a failure mode after one query is methodologically thin.
- Failure: CSQE generated a "meta-description" (how a topic might be described, rather than actual vocabulary) — this was a generation failure, not a retrieval failure per se.
- The AI itself flagged this as fragile (in the brief).

**Decision:** **REVISE** — demote from a named failure mode to an illustrative single-case example. Match the brief's recommendation. (Same decision as in pt7.)

---

### Item P4.4.23 — Three representative big-win examples (الرباط المنصوري, John Dewey, Nicolas Boileau)

**Discussion (per-example):**

1. **الرباط المنصوري (Mansouri ligament/building):** Mohammed and Osman both initially debated what this is. Osman explained: blind QE interprets it as a surgery procedure ("ligament/knot"), while CSQE correctly identifies it as a Mamluk-era building (because the corpus context provides the disambiguation). This is an excellent illustrative example because the disambiguation requires corpus knowledge — exactly what CSQE provides.
   - **Verdict:** STRONG example, keep.

2. **John Dewey (founder of pragmatism):** less clear. The discussion didn't probe this example deeply.
   - **Verdict:** UNCLEAR — needs further verification of what blind vs CSQE produced for this query, and whether it's as illustrative as الرباط المنصوري.

3. **Nicolas Boileau (17th-century French poet):** Mohammed and Osman walked through:
   - Blind QE: "A French businessman" (wrong attribution).
   - CSQE: "17th century French poet" (correct, because the corpus has this information).
   - Both find this illustrative — CSQE wins because it grounds in actual corpus content.
   - **Verdict:** APPROVE as illustrative.

- General observation: examples should be **intuitively compelling** (Osman's standard from pt10's discussion of intuition) — both الرباط المنصوري and Nicolas Boileau pass that bar. John Dewey is less obvious.

**Decision:** **REVISE — verify and curate:**
1. **Keep الرباط المنصوري and Nicolas Boileau** — both are strong illustrations where corpus grounding makes a clear difference.
2. **Verify John Dewey:** check the actual blind-vs-CSQE comparison for this query. If clearly illustrative, keep. If ambiguous, replace with another big-win example from the dataset.
3. Verify all three: the queries, the blind QE outputs, and the CSQE outputs are correctly transcribed in the thesis.
4. Optional: search for a 4th example to have a backup if any of the three doesn't survive verification.

---

### Item P4.4.24 (briefly touched) — "First-pass recall as the dominant predictor of CSQE effectiveness"

**Discussion (very brief):**
- Will be addressed in conjunction with the Config A redo and the per-query analysis fate (delete vs keep).

**Decision (deferred):** Final wording depends on whether §4.10 stays or goes. If kept, soften "dominant predictor" to "the largest observed modulator" (per brief recommendation). If deleted, no decision needed.

---

### Item P4.4.26 — Recommendations embedded in §4.10.4 (first-pass quality gate, asymmetric expansion)

**Discussion (brief):**
- Connects to the broader question of whether §4.10 is kept at all.
- If kept: these recommendations should move to Ch.5 (per the brief's preference) rather than embedding implications in a results section.
- If §4.10 is deleted: these recommendations migrate naturally to Ch.5.

**Decision:** **REVISE — conditional:**
- If §4.10 stays → move embedded recommendations to Ch.5.
- If §4.10 is deleted → fold the recommendation content into Ch.5 directly.

---

## Cross-Cutting Insights & Action Items Raised in pt9

- **Dataset integrity investigation (HIGH PRIORITY):** verify whether the 258 failure queries' relevant documents are present in the indexed Wikipedia corpus. If absent, identify the preprocessing bug and decide whether to reindex (which would change all baselines).
- **Section 4.10 (per-query analysis) — possible deletion:** weighed cost/benefit:
  - Benefits of deletion: avoids Config A redo work, avoids most P4.4.20–28 items, removes weakly-motivated content.
  - Cost of deletion: loses the recovery rate finding (56.8% improved), loses the first-pass dependence insight.
  - **Decision pending the dataset investigation.**
- **Single-case failure naming (P4.4.22):** confirmed — demote from named mode to illustrative example.
- **Big-win examples (P4.4.23):** verify all three in detail before publication; consider a backup example.
- **AI-added verification cell:** Mohammed had earlier deleted a verification cell the AI added; he should run it now or have it re-added. (This is a minor process fix.)

---

## Items Touched But Deferred

- **P4.4.24** — wording depends on §4.10 fate.
- **P4.4.27, P4.4.28** — depend on §4.10 fate (the medium query-length row in `tab:query_length_split`, the Phase 4 rows in `tab:full_summary`).

---

## Items Not Yet Discussed

The remaining P4.5.x conclusion paragraphs, P4.A.x abstract additions, and most P4.X.x cross-cutting items (some addressed in pt5/pt6). All would be in pt10.
