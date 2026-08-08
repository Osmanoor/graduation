# Plan — remove the chapter summaries (reverses C10)

**Requested by:** Elhaj, 2026-08-08 · **Status:** PLAN ONLY, nothing applied
**Reverses:** C10 (closed 2026-08-04 with "Decision: keep")
**Decided by Elhaj:** remove all three, including Chapter 3's · pointer goes at the end of **§4.9**

---

## 1. What exists right now

Line numbers verified against the tree **after** merging Osman's J3b commits (they shifted Ch.4 by +2).

| # | Section | File · lines to delete | Length | Notes |
|---|---|---|---|---|
| §2.6 | Chapter Summary | `chapter2.tex:399–419` (to EOF) | intro + **10-item itemize** + closing forward-link paragraph | the big one |
| §3.10 | Chapter Summary | `chapter3.tex:498–503` (to EOF) | one 139-word paragraph | **added by C10 four days ago** |
| §4.11 | Chapter Summary | `chapter4.tex:817–824` (to EOF) | two paragraphs | para 1 is the *only* prose pointer to Table B.3 |

All three are labelled: `sec:chapter_summary`, `sec:ch3_summary`, `sec:res_summary`.

---

## 2. Your reasoning checks out — here is the evidence

**§4.11 is redundant with Chapter 5.** Its second paragraph says the best system reached 0.7137,
+54.5% over BM25, +13.9% over the hybrid. Chapter 5 §5.1 begins on the very next page and states
the same findings as twelve numbered conclusions. Nothing is lost.

**§2.6 is redundant twice over.** Its closing paragraph ("The following chapter presents the
methodology employed…") is a near-restatement of **Chapter 3's opening paragraph**, which lists the
same sections in the same order — exactly what you spotted. And §1.3 *Thesis Layout* already
describes all five chapters in detail. That is the same content in three places.

---

## 3. What breaks — and this is the important part

`tab:full_summary` (the all-experiments table, now **Table B.3** in Appendix B) is referenced from
exactly three places:

| Where | What it says | Survives deletion? |
|---|---|---|
| `appendixB.tex:82` | `Section~\ref{sec:res_summary} discusses the progression it records.` | ❌ **breaks** — becomes `??` |
| `chapter4.tex:820` (§4.11) | the prose pointer sending the reader to the appendix | ❌ deleted with the section |
| `chapter4.tex:729` | a *caption* reference, in Table 4.25's caption | ✅ survives |

So after deletion the main text points at Table B.3 **only from inside a caption** — the table is
effectively orphaned, and the appendix carries a dangling reference to a section that no longer
exists. Both must be fixed in the same commit as the deletion.

---

## 4. Recommended fix for the Table B.3 reference

**Two moves, and they cost nothing in main-text pages.**

**(a) Move §4.11's first paragraph into Appendix B as the section intro.** It is good prose and it
explains *why* the table exists:

> "The experiments in this chapter were reported in the order they were conducted, each one
> motivated by the outcome of the last. Read that way the argument is cumulative but dispersed…"

That rationale belongs beside the table now that the table lives in the appendix. Rewrite "in this
chapter" → "in Chapter~\ref{chap:results}", and it replaces the broken
`Section~\ref{sec:res_summary}` sentence. **Nothing is lost, the dangling reference is fixed, and
appendix pages do not count toward the 100-page limit.**

**(b) Add one sentence at the end of §4.9** — *CSQE with Hybrid Fusion*, per Elhaj's call, which is
the right one and better than the §4.10 I first proposed:

- §4.9 is where the progression **culminates** — its closing paragraph already walks the three stages
  and lands on "0.7137 NDCG@10 — a 54.5% improvement over BM25 alone."
- §4.9 already carries **Figure 4.11, *System progression to the best system***. Table B.3 is the
  tabular twin of that figure, so the pointer sits directly beside the thing it complements.
- §4.10 (per-query error analysis) is a **diagnostic detour** after the result is established. A
  reader arriving at a consolidated progression table from there would be going backwards.

Insert after `chapter4.tex:715` (the paragraph ending "…strong upper bound for downstream
reranking."), before the `%===` rule at 717:

> A consolidated view of every experiment reported in this thesis, grouped by phase, is given in
> Table~\ref{tab:full_summary} of Appendix~\ref{app:tab_summary}.

*Rejected alternative:* Chapter 5 §5.1. It opens by restating the research question; a table
reference there interrupts the argument.

---

## 5. What must be written back — checked chapter by chapter

Elhaj's instruction: *make sure if there is any text that needs to be added to the previous
section.* Checked all three. **Only Chapter 3 needs anything.**

### ⚠️ Chapter 3 — WILL END MID-LIST. Needs a closing sentence.

§3.9 *Per-Query Error Analysis* ends on `\end{itemize}` — the Type A / Type B / Type C bullets.
Deleting §3.10 makes **Chapter 3 end on a bullet point**. That is exactly the defect C10 was
opened to fix; it is why the summary was written in the first place.

So the summary goes, but a **closing sentence** must be appended to §3.9. Not a section — one or
two lines of prose, no heading, no label. Proposed:

> This classification, together with the aggregate comparison and the query-length and first-pass
> splits defined above, forms the interpretive framework applied to the final system in
> Chapter~\ref{chap:results}.

Closes the list, closes the chapter, and carries the forward link that §3.10 used to carry.

### ✅ Chapter 2 — needs nothing

§2.5 *Research Gap* already ends with a full prose paragraph: *"These questions are addressed in
this thesis through a staged experimental programme… **as described in the following chapter.**"*
The forward link to Ch.3 is already there — which is precisely why §2.6's closing paragraph was
redundant.

### ✅ Chapter 4 — needs nothing

§4.10 ends with *"Both are developed as recommendations in Chapter~\ref{chap:conclusion}."* A clean
prose close with a forward link straight into Chapter 5. Ideal handoff.

### ✅ No unique content is lost — verified

The only numbers in §4.11's second paragraph are **0.7137**, **54.5%** and **13.9%**. All three
already appear in §4.9 (`chapter4.tex:693, 697, 706, 715`) and again in Chapter 5 §5.1. Every
itemize bullet in §2.6 is a restatement of a section it cites. §3.10 is pure restatement.
**Nothing in any of the three sections exists only there.**

---

## 6. Execution order

1. `chapter2.tex` — delete **399–419** (the `%===` rule through EOF).
2. `chapter3.tex` — delete **498–503**, then append the closing sentence to §3.9.
3. `chapter4.tex` — delete **817–824**.
4. `chapter4.tex` — insert the Table B.3 pointer after line **715**, at the end of §4.9.
5. `appendixB.tex:81–82` — replace the broken sentence with the relocated §4.11 paragraph.
6. Rebuild: `xelatex → bibtex → xelatex ×2`. **Gate: 0 undefined references.** `sec:res_summary`
   is the one at risk — if it survives anywhere, the build will say so.
7. Record the new core Ch.1–5 page count.
8. Append a reversal note to C10 in `THESIS_FINAL_SUBMISSION_TASKS.md` and to
   `C10_chapter_summaries_audit.md` — do not rewrite the original entry.

---

## 6. Page impact — this is a real lever

| Section | Estimated saving |
|---|---|
| §2.6 (10-item itemize + 2 paragraphs) | **~1 page** |
| §4.11 (2 paragraphs, chapter tail) | ~0.3 page |
| §3.10 (139 words) | **~0** — C10 recorded it landing in existing whitespace at 0 page cost, so removing it likely frees nothing |

**Realistic total: ~1–1.5 pages off the core.** Core Ch.1–5 is currently **101** against a 100-page
limit. This alone may close the gap — and unlike J11 it has no cross-report conflicts.

---

## 7. Decisions — both settled

| Question | Decision | By |
|---|---|---|
| Chapter 3's summary — remove too? | **Yes, remove.** A single chapter carrying a summary while four do not reads as an oversight, not a decision. Its content is pure restatement of §3.1–3.9. | Elhaj, 2026-08-08 |
| Where does the main text point at Table B.3? | **End of §4.9**, not §4.10 — see §4(b) for why this is the stronger placement. | Elhaj, 2026-08-08 |

Nothing is blocking. This is ready to execute.

---

## 8. Two things to be ready for

**Dr. Tahani called keeping the summaries "ممتاز".** She said optional, but she did express a
preference, and this reverses it. Have the answer ready: *§4.11 restated Chapter 5's conclusions
one page before Chapter 5 delivered them, and §2.6 restated both §1.3 and Chapter 3's opening.
Removing them cut repetition, not content.* That is a good answer — but do not be surprised by the
question.

**This interacts with J11.** J11's flagged conflict was: E1 says drop Table 4.22 because Table 4.28
covers it, while D2 says move 4.28 to an appendix. **Half of that has already happened** — 4.28 is
now Table B.3 in Appendix B. So if E1's recommendation to drop Table 4.22 is also applied, the main
text ends up with **no progression table at all**. Settle that before J11, not during it.
