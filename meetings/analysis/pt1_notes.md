# pt1 Analysis Notes — 23.1.2026 Part 1

**Source:** `meetings/23.1_2026.pt1.md` (167 lines)
**Speakers:** Mohammed Elhaj Sani (driving), Osman Bashir
**Coverage:** Review items **2.1 through 2.7** (Chapter 2 — Structure & Content)
**Duration / scope:** Short opening session that ended at prayer time. Sets the methodology for the whole review series.

---

## Meta / Process Decisions (set in this transcript)

- **Review framework:** For each AI-decision item, they will mark **Approve / Revise / Reject**. Items grouped by source: Dr. Tahani's guidance, experiments, literature, or pure AI assumption needing validation.
- **Action item raised:** Transcribe Dr. Tahani's recordings (separate from these meetings) and cross-check against the thesis to find anything she said that the AI missed or got wrong. Treated as an important standalone task.
- **Action item raised:** Have the AI re-review the `tasks` file when revising Ch.2 so no work-stream they completed gets omitted from the thesis (e.g., the dataset analysis stream that Osman flagged).
- **Flagging convention:** Items they're unsure about should be flagged as questions to ask Dr. Tahani in a future supervisor meeting, rather than decided unilaterally.

---

## Per-Item Discussion & Decisions

### Item 2.1 — Ch.2 organized into 4 main sections (Theoretical Background, Mathematical Models, Models Used, Related Work)

**Discussion:**
- Osman raised that the AI's Ch.2 structure is missing a **dataset analysis** section. They had performed a research stream comparing roughly 8 candidate datasets before selecting MIRACL (Arabic). That work is currently absent from Ch.2 — the AI jumped straight to "models used."
- Mohammed agreed: the Ch.2 structure should mirror the actual flow of tasks they executed. Anything they did real research on (datasets included) should be reflected in Ch.2.
- They suspect the dataset section should appear **before** "Models Used."

**Decision:** **REVISE**. Add a dataset analysis section to Ch.2 (probably before "Models Used"). The AI should be re-pointed at the project's `tasks` file to make sure no other work-stream is being silently dropped from the thesis.

---

### Item 2.2 — Mathematical formulas placed in their own Section 2.2

**Discussion:**
- The principle of separating math into its own referenceable section was approved.
- **However, Osman raised an inconsistency:** in the Theoretical Background section, the AI writes the **hybrid retrieval equation inline**, but for BM25, Dense, and the evaluation metrics, the equations are kept in the Mathematical Models section. So the rule "math goes in section 2.2" is broken specifically for hybrid.
- Mohammed agreed: hybrid is just as much a mathematical model as BM25 or dense, so its equation should be moved to the math section for consistency.

**Decision:** **REVISE**. Move the hybrid retrieval equation out of the Theoretical Background section and into the Mathematical Models section so all retrieval-method equations live in one place.

---

### Item 2.3 — Chapter Summary section (Section 2.5) with bullet points

**Discussion:**
- Neither was sure whether to keep the chapter summary. Dr. Tahani didn't explicitly mention chapter summaries.
- Mohammed proposed checking Dr. Tahani's recordings (via transcription) before deciding — she might have mentioned it implicitly somewhere.
- Fallback plan: **flag this as a question to ask Dr. Tahani directly** in a future meeting. Keep the summary in the draft as a flagged-pending-decision item.

**Decision:** **DEFER / FLAG TO SUPERVISOR**. Don't remove yet. Mark as a question for Dr. Tahani. Note it in the working notes so the team knows it's an open item.

---

### Item 2.4 — Funnel structure for Related Work (Foundational → Modern → Arabic → Gap)

**Discussion:**
- Osman: "ممتاز جداً" (excellent). No reservations from either side.

**Decision:** **APPROVE**.

---

### Item 2.5 — Described 11 models (10 evaluated + GPT-OSS)

**Discussion:**
- Mohammed initially wanted to **drop GPT-OSS and ALLaM** from Ch.2 because GPT-OSS was abandoned mid-experiment (resource constraints) and ALLaM produced very poor results.
- Osman pushed back on dropping them — there's value in including them honestly:
  - **GPT-OSS is the only Mixture-of-Experts model** in the comparison set. Including it tests whether an English-dominant MoE can do effective Arabic QE, which is a meaningfully different research question.
  - Dr. Tahani had already said during their presentation call that mentioning what didn't work is fine.
- Mohammed eventually agreed to keep both, but flagged a concern about a specific AI-written sentence on page 39 (highlighted in blue): the claim that GPT-OSS is "English-dominant" is **not actually verified in any docs** Osman has — it's an AI-introduced framing.

**Decision:** **APPROVE WITH FIX** — keep both GPT-OSS and ALLaM in Ch.2, including the rationale for inclusion (MoE comparison, dropped/failed honestly reported). **BUT** verify the specific claim that GPT-OSS is "English-dominant" before printing — if not supportable from official sources, soften or remove that wording. Osman said he can fix this himself.

---

### Item 2.6 — IEEE format, ~40 references, numbered by order of appearance

**Discussion:**
- Both noted this is directly Dr. Tahani's instruction. Nothing to debate.

**Decision:** **APPROVE**.

---

### Item 2.7 — Research gap claim: "none of these studies tested models smaller than 7B for zero-shot QE on Arabic text"

This was the **major discussion of pt1** — they spent a substantial portion of the meeting on this and treat it as foundational. The discussion is also tightly connected to item **1.3 (research question)**, item **1.2 (problem framing)**, and item **1.4 (objectives)**.

**Discussion — what they think the AI got wrong:**
- The AI framed the central problem statement narrowly as "do small (<7B) LLMs work for Arabic query enhancement?" Both feel this **mis-represents the actual contribution** of the thesis.
- Their actual contribution is broader: they applied **multiple query enhancement approaches** (Query2Doc / blind QE, CSQE, hybrid fusion with retriever-specific application) **to improve Arabic RAG**. The "small models" angle is a strength/bonus, not the primary contribution.
- Osman's framing: "We applied query enhancement to improve Arabic RAG systems. The fact that we did it with small models is something extra." Mohammed agreed.

**Discussion — concerns about the gap claim itself:**
- Even if the framing is fixed, the literal claim "no prior paper tested <7B on Arabic QE" needs validation. They listed the papers they looked at (DaVinci, LLaMA 70B, etc. — all large) but couldn't confirm none used smaller Arabic-specific models. Osman noted **new papers may have appeared since they did the literature review** — the claim's freshness is uncertain.
- They considered whether a paper might exist that already used small models for Arabic QE. If so, the gap claim collapses.

**Discussion — alternative framing they considered:**
- Make the problem statement a more general question: "Do query expansion techniques improve retrieval quality in Arabic?" — under which all their experiments (model comparison + CSQE + hybrid + repetition) become objectives.
- Multiple research questions vs. single problem statement: Mohammed observed that some papers state several research questions (RQ1, RQ2, RQ3). They were unsure whether the bachelor's thesis convention permits this.
- The "small models" claim could be retained as a secondary novelty hook ("and we did it with small open-source models") rather than the primary gap.

**Decision:** **REVISE** — multi-part:
1. **Re-frame the problem statement / research gap** to lead with "applying query enhancement to Arabic RAG" with multiple approaches as the main contribution. Move "small models" to a secondary novelty point, not the central claim.
2. **Validate the gap claim** by re-doing a literature search for any post-2024/2025 paper testing small (<7B) LLMs on Arabic QE. If found, restructure the gap accordingly.
3. **Investigate whether the thesis should have one problem statement or multiple research questions** (look at examples in published papers / ask Dr. Tahani).
4. The objectives section (item 1.4) should then enumerate every approach they tried (small models, CSQE, hybrid, repetition, retriever-specific application) so the thesis covers the full breadth of work.

---

## Cross-Cutting Insights Raised in pt1

- **Implicit principle:** The thesis structure should mirror the actual sequence and breadth of work performed. If a research stream was completed (datasets, repetition experiments, hybrid, CSQE, etc.) it must surface somewhere in Ch.2 / Ch.3 / Ch.4. The AI's current draft drops some of this work silently — this is the meta-problem they want corrected.
- **Honest reporting principle:** Both agreed it's acceptable (even good practice) to mention models that were attempted but failed (GPT-OSS, ALLaM), as long as the reasons are clear. Dr. Tahani approved this stance during a prior call.
- **Verification principle:** Any AI-introduced descriptive claim about a model (e.g., "English-dominant", "Arabic-centric vocabulary") must be cross-checked against official model cards / docs before printing — the AI has been observed to insert unsupported descriptors.

---

## Items Touched But Deferred (mentioned in passing, not resolved in pt1)

- **Item 1.2 / 1.3 / 1.4** (problem statement, research question, objectives) — implicitly modified by the 2.7 discussion. Will need explicit reconciliation when the team reaches Ch.1 in a later transcript.

---

## Items Not Yet Discussed

Everything from item 2.8 onward, all of Ch.3, Ch.4, Ch.5, abstract, cross-cutting, and all Phase 4 items remain unaddressed in pt1. Picks up in pt2.
