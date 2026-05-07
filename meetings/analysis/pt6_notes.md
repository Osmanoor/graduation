# pt6 Analysis Notes — 23.1.2026 Part 6

**Source:** `meetings/23.1_2026.pt6.md` (220 lines)
**Speakers:** Mohammed, Osman
**Coverage:** **P4.2.3 → P4.2.5**, then **P4.3.1 → P4.3.13**.
**Notable:** A new thesis-wide rule established (estimation-vs-measurement for time claims). Identification of a gap in their own work (asymmetric vanilla Q2D never tested). Meeting ends pivoting to prepare slides for an upcoming supervisor meeting.

---

## Per-Item Discussion & Decisions

### Item P4.2.3 — Lei et al.'s "30% mAP improvement over BM25" cited for CSQE

**Discussion:**
- They want to verify the number against the original Lei et al. 2024 paper before including it in Ch.2.
- Question of comparison benchmark: passage-level vs document-level, single dataset vs multiple datasets — the precise comparison setting matters.

**Decision:** **VERIFY then APPROVE** — read Lei et al. 2024 again and confirm the exact "30% improvement in mAP" claim. Match the comparison setting. If the number or setting differs, update the citation.

---

### Item P4.2.4 — New research gap claim: asymmetric CSQE × hybrid not yet studied

**Discussion (substantive):**
- The AI introduced this as a new "second-order research gap" to motivate the asymmetric fusion experiments retroactively.
- They debated the novelty layers:
  - **Layer 1 (general):** Has anyone studied CSQE × hybrid asymmetric fusion globally? Probably not — but a literature search is needed to be sure.
  - **Layer 2 (low-resource):** Even if someone has done it for English, doing it for low-resource languages is still novel.
  - **Layer 3 (Arabic specifically):** No one has done this for Arabic. This layer is firm.
- Osman: "even if globally someone has done it, our doing it in low-resource [Arabic] is itself a contribution."
- Mohammed agrees the safest claim: "no one has done this in Arabic."

**Decision:** **APPROVE with FRAMING REVISION** — keep the gap claim, but frame it as "not yet studied for Arabic" rather than the universal "not yet studied." Action: Osman to do a literature search (the AI's recommendation explicitly tagged him — "Osman search") to check for any post-2024 work on asymmetric CSQE × hybrid before publication. If found, downgrade the claim to "not yet studied for Arabic."

---

### Item P4.2.5 — Claim that asymmetric query expansion in hybrid is an open question

**Discussion:**
- Connected to P4.2.4. Same framing decision (Arabic-specific is the safe layer).
- Then Mohammed asked a deeper question: "did we ever try **asymmetric Query2Doc (vanilla, not CSQE)** in our experiments — apply QE to only one of BM25/Dense?"
- Osman clarified what was actually done:
  - Hybrid with no QE: ✓ tested
  - Hybrid with CSQE asymmetric (BM25-only-expanded vs Dense-only-expanded vs both-expanded): ✓ tested (this is Phase 4 Config A/B/C)
  - **Hybrid with vanilla Query2Doc asymmetric: ✗ NOT tested**
- This is a gap in their own work. The reviewer's flag in P4.2.5 was effectively pointing at this. If they tested asymmetric vanilla Q2D and it also showed Config A wins, that would be a much stronger generalisation of the finding.

**Decision:** **APPROVE the open-question framing** (qualified to Arabic). **NEW EXPERIMENTAL TASK:** test asymmetric vanilla Query2Doc (apply QE only to BM25 in a hybrid setup, vs only to Dense, vs to both) — if it confirms Config A wins, the retriever-specific representation finding generalises beyond CSQE.

---

### Item P4.3.1 — Two solution families for repetition (fixed Q2D + adaptive MuGI)

**Discussion:** Both want both methods presented, since both were tested. Scientific record matters more than narrative simplicity.

**Decision:** **APPROVE** — present both families.

---

### Item P4.3.2 — Sweep ranges n ∈ {1, 3, 5, 7, 10} and β ∈ {2, 4, 6}

**Discussion:** Brief — confirmed grounded in exp_011.

**Decision:** **APPROVE.**

---

### Item P4.3.3 — Motivating prose about 3-word vs 15-word query needing different repetition

**Discussion:**
- Osman: "the example is intuitive, captures the MuGI logic well, and the actual data supports it (smaller models settle on different n than larger models)."
- They ratified the example.

**Decision:** **APPROVE** — keep the motivating example. Confirms the MuGI intuition.

---

### Item P4.3.4 — No new LLM inference needed for repetition

**Discussion:** Confirmed — Mohammed reused saved expansion pkls from the original Task 4.0b model comparison work.

**Decision:** **APPROVE.**

---

### Item P4.3.5 — Runtime claim "approximately 73 minutes on Colab CPU"

**Discussion (rule-establishing):**
- Mohammed wants to remove the 73-minute claim because it was an estimation, not a measurement. He doesn't trust his own estimates.
- Osman noted that some cells *do* output their actual runtime ("this took X seconds"). Those are genuine measurements.
- **They established a thesis-wide rule:** any time-related claim that came from estimation will be deleted; any time-related claim that came from actual cell output will be kept (and verified). Apply this rule throughout the thesis.
- This rule retroactively affects **item 3.10** (the "16x speedup" — also estimated, also gets deleted).

**Decision:** **REVISE** — apply the new estimation-vs-measurement rule:
- For P4.3.5 specifically: replace the "73 minutes" claim with either (a) the actual cell-output runtime if extractable, or (b) delete the runtime claim entirely.
- **Cross-cutting:** sweep all thesis sections for time/speedup claims. Delete estimates; verify and keep measurements.

---

### Item P4.3.6 — MuGI formula `n = max(1, ⌊|d| / (|q|·β)⌋)`

**Discussion:** Brief — grounded in Zhang et al. 2024.

**Decision:** **APPROVE.**

---

### Item P4.3.7 — Enhanced query assembly equation includes general k but only k=1 was used

**Discussion:**
- Mohammed wants to keep the equation as it appears in the original paper (general k), and add a clarifying note: "for our work k=1."
- This is more honest than rewriting the equation specifically for k=1.

**Decision:** **APPROVE WITH ADDITION** — keep the general-k equation; add a sentence in the main text (not just parenthetically) stating "in our experiments k=1 (single pseudo-document)."

---

### Item P4.3.8 — Plan to cross-reference RRF/CC equations from Ch.2 in §3.7

**Discussion:** Brief — both agree it's good practice; avoids duplication.

**Decision:** **APPROVE.**

---

### Item P4.3.9 — α swept over {0.1, …, 0.9} and k tested at {20, 60}

**Discussion:** Brief — grounded in exp_012.

**Decision:** **APPROVE.**

---

### Item P4.3.10 — Fusion setup: BM25S and mDPR retrieve top-100 candidates

**Discussion:**
- Osman: "honestly, I'm not sure — did we use top-100 or top-1000? We were experimenting with both."
- Mohammed initially thought they had stored top-1000 candidates. Confused for a moment.
- Eventually settled: in the actual hybrid implementation, top-100 is correct.

**Decision:** **VERIFY then APPROVE** — confirm in the exp_012 notebook that top-100 (not top-1000) was used. If 100 → APPROVE. If 1000 → correct in the thesis.

---

### Item P4.3.11 — CSQE pipeline described as two-stage rather than three-stage

**Discussion:**
- Mohammed initially asked whether they should describe CSQE as 3 steps (first-pass, generation, assembly).
- Osman: "the assembly is just concatenation — concatenate the corpus-extracted passages with the query, that's it. It's not a meaningful third stage."
- Mohammed acknowledges concatenation is just plumbing, not a methodological step.

**Decision:** **APPROVE** — keep the two-stage description (first-pass retrieval + corpus-grounded expansion). The assembly is implementation detail, not a stage.

---

### Item P4.3.12 — Config A/B/C naming convention

**Discussion:**
- Both strongly prefer descriptive names over A/B/C.
- Mohammed: "throughout the entire thesis, replace A/B/C with descriptive names. We shouldn't say 'Config A gave us good results' — we should say 'both-expanded' or 'BM25-only-expanded'."

**Decision:** **REVISE** — global rename throughout the thesis:
- Config A → BM25-only-expanded (CSQE applied to BM25; Dense uses raw query)
- Config B → Dense-only-expanded (Dense uses CSQE; BM25 uses raw query) — *verify this matches the brief's labeling*
- Config C → Both-expanded (CSQE applied to both retrievers)
- Apply consistently in §3.8.3, §4.9, §5.1, abstract, and all related cross-references.

---

### Item P4.3.13 — Hypothesis stated before results in §3.8.3 (Dense degrades on long inputs)

**Discussion (major honesty moment — second one in this transcript):**
- The AI's draft places "BM25 benefits from vocabulary breadth; Dense encoder degrades on long inputs" inside the methodology chapter — making it look pre-planned.
- Osman: "this would be impossible to know in advance. In the dense-only case (no hybrid), Dense actually showed improvement across most models. We couldn't have known the degradation would happen specifically when long expansions are used in fusion."
- Both agree this is a clear post-hoc interpretation that snuck into the methodology section.

**Decision:** **REVISE** — adopt the brief's recommendation:
- §3.8.3 wording becomes: "Three fusion configurations were tested to determine the optimal retriever–query assignment; whether expansion helps or hurts each retriever was left open."
- Save the causal interpretation ("Dense degrades on long inputs") for Ch.4 (results discussion).
- This honesty fix protects against examiner challenges of "how did you know before running the experiment?"

---

## Cross-Cutting Insights & Action Items Raised in pt6

- **NEW THESIS-WIDE RULE — Estimation vs Measurement:** any time/speedup/runtime claim that came from estimation must be removed. Only retain claims derived from actual cell outputs (with the source verifiable). This rule retroactively affects items **3.10** (16x speedup) and **P4.3.5** (73 min runtime). Sweep the entire thesis.
- **Asymmetric vanilla Q2D experiment:** new experimental task — test whether the retriever-specific representation principle generalises beyond CSQE to vanilla Query2Doc.
- **Lei et al. CSQE 30% claim:** verify number and setting before printing.
- **Asymmetric CSQE × hybrid literature search (Osman):** check for prior post-2024 work; if any exists, downgrade gap claim to "not yet for Arabic."
- **Top-100 vs top-1000 retrieval depth verification:** confirm in exp_012 notebook.
- **Configuration naming global rename:** A/B/C → descriptive names throughout the thesis.
- **Methodology hypothesis demotion:** the §3.8.3 hypothesis must be moved to Ch.4 results-discussion. Don't leave post-hoc interpretations in methodology chapters.

### Pivot to supervisor meeting prep
At the end of pt6 they shifted focus:
- **Mohammed:** read the brief, extract the work that was completed since the last supervisor meeting.
- **Osman:** use the existing transcripts (pt1–pt3 at minimum) to extract the questions for Dr. Tahani.
- **Joint output:** quick slides for the supervisor meeting.

This is a *parallel* workstream to the review-document analysis — they don't pause the AI-decisions review, just bookmark and prepare slides in parallel.

---

## Items Touched But Deferred

- The asymmetric vanilla Q2D experiment ties back to item **5.1** (conclusions) and **P4.4.16** (retriever-specific representation terminology). If the experiment confirms generalisation, all three sections strengthen.

---

## Items Not Yet Discussed

Continues from item P4.3.14 (CSQE configuration), P4.3.15 (CSQE temp=1.0), P4.3.16 (CSQE prompt missing), P4.3.17 onward (error analysis thresholds), all P4.4.x, all P4.5.x, all remaining P4.X.x. Continues in pt7.
