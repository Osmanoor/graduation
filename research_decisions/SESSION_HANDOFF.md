# Session Handoff — Thesis Final Submission

**Written:** 2026-07-29, end of the Phase A session. Load this first in a new chat.
**Repo state:** `main` pushed and current (see `git log`). Working tree clean except three non-thesis files.
**Master task list:** `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md` — that file is the source of truth, this is the orientation.

---

## 1. Working rules (agreed 2026-07-29, after a round of scope creep)

1. **No thesis edit without a task-list entry.** If work uncovers something worth changing that is not a task, it gets *written down as a task*, not edited on the spot.
2. **Small, fully planned batches.** Decide exactly what changes before touching a `.tex` file. No "while I'm here" fixes.
3. **The revert test:** a change is only justified if reverting it would leave a *false or self-contradicting* statement in the thesis. Enrichment, extra citations, and nicer phrasing are not justifications.
4. **Verify before asserting.** Numbers against raw data; literature claims against papers we actually hold in `papers/`. Do not add citations to papers we have not read.
5. Agents are for *gathering evidence and reporting*; edits are applied in the main session after review.

---

## 2. What is DONE

**Phase A — core narrative rewrite (Elhaj, complete):**
- **A1/A2/A3** — §1.1 is one continuous funnel paragraph ending in the new RQ: *"To what extent can LLM-based QE---blind and corpus-steered---improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms?"* The de-scoped "model characteristics" clause is gone thesis-wide.
- **A4** — 9 measurable objectives, 1:1 with experiments and with Ch.5 paragraphs.
- **A5** — old "small open-source models" framing swept from Ch.2–5 (55 occurrences audited, 14 fixed, 41 kept as legitimate facts). Ch.2 Research Gap rebuilt as 4 gaps + 7 questions.
- **A6** — conclusion now covers all 9 objectives (3 paragraphs added, every figure verified against raw data).
- **A7** — full Problem↔Objectives↔Methodology/Results↔Conclusions audit. Chain verified sound; 6 blockers fixed.
- Reports: `A5_small_models_sweep_report.md`, `A5_edit_verification.md`, `A6_number_verification.md`, `A7_mapping_audit.md`, `PHASE_A_COMPLETION_REPORT.md`.
- A later out-of-scope revision round was **reverted** to the Phase A text (kept only 6 defect fixes). See the SCOPE DECISION note in the task file.

**Osman (complete):** C1 front matter order · C2 List of Abbreviations · C3 first-mention sweep · C6 citations/IEEE order · C7 caption placement (verdict: no change needed) · C8 page numbers (verdict: correct).

**Measured:** **D1 — core manuscript Ch.1–5 = 103 pages, 3 OVER the 100-page limit.** No appendices exist yet. Ch.4 alone is 35 pages.

---

## 3. Decisions waiting on Elhaj (blockers for other work)

| # | Item | Options |
|---|---|---|
| ~~H1~~ | **SILMA temperature — REASSIGNED TO OSMAN 2026-07-29.** Investigation complete; SILMA's temperature *decision* (0.1, chosen empirically) is confirmed correct and is not in question — only which pickle the Exp 1.1 sweep loaded. Handover note with all evidence and sources is in the H1 task entry. **H2 and H3 (Table 3.2 hyperparameter cells) also went to Osman.** Elhaj: no action. | — |
| Flag 2 | Reinstate the word "small" once in Objective 4? | Optional; numeric range already carries it |
| Flag 6 | Aya CC-BY-NC caveat currently in Ch.5 "Overall" *and* Challenges item 8 | Keep both / trim the Overall |

---

## 4. Recommended next work (one task at a time)

**Immediate, small, self-contained:**
1. ~~Ch.5 ¶1 sentence for Objective 2~~ — **DONE as task A8, 2026-07-29.** The last mapping gap is closed.
2. **C4 — §1.3 Thesis Layout → one single paragraph.** A direct supervisor instruction, still unfulfilled; §1.3 is currently four bold-led paragraphs and got *longer* during A7. Low risk, high visibility.

**Then Phase B:**
3. **B1 — English abstract.** The biggest remaining gap: it still states the old research question, never names CSQE, and never mentions the asymmetric-placement finding (A7 blocker B5 lands here). Target ≈ 3/4 page; structure Context → Problem → Objectives → Methodology → Key Findings → Conclusion. Starter sentences in `A7_mapping_audit.md` §(g) B5.
4. **B2 — Arabic abstract** (Osman, after B1).

**Then the page-count campaign** (needs ≥3 pages, ideally more): D2 appendix analysis → D3 code appendix → E1 figure/table duplication → D5 conciseness pass (explicitly last).

**Elhaj also owns:** C5 (promote bold inline headings to numbered sub-headings in §2.1.4 / §2.1.5), E2 (regenerate Figs 4.2/4.3/4.4 from canonical post-WS1 data), E3 (dead labels, figure-gated).

---

## 5. Known debt (not blocking, do before submission)

- **Unverified literature:** Macmillan-Scott et al. 2025 (arXiv 2511.19325) is cited but not in `papers/`; WS6 notes say it evaluates MuGI and Exp4Fuse across eight languages *including* Arabic — confirm our gap claims survive reading it. MuGI and Exp4Fuse also have no first-hand summaries.
- **The monolingual-Arabic gap claim** was only ever searched at sub-7B scope — re-run unfiltered.
- **Acronym audit was partial** — only Ch.1-defined acronyms were checked for first-mention violations; RRF, CC, VRAM, OALL and others were not.
- **A7 was not re-run after its own fixes** were applied — that is how the Objective 2 gap (since fixed as A8) was missed. If objectives are edited again, re-check the Ch.5 check-off.
- Deferred to D5/terminology: full "open-source" → "openly available" sweep; SILMA Kashif-2B vs SILMA 2B naming.
- **CSQE is absent from the Ch.2 technique taxonomy** (§2.1.4 lists HyDE/Query2Doc/GRF only) — natural to fold into C5 if wanted. *Deliberately not done; would add ~80 words to a thesis already over the page limit.*
