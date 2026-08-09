# Remaining Work — Complete Plan to Submission

**Date:** 2026-08-04 · **Status:** PLAN. Nothing applied.
**Ownership decided by Elhaj 2026-08-04:** Osman keeps **appendices, figures and tables**.
Elhaj takes **everything else**, including items previously assigned to Osman
(Arabic abstract, dedication, temperatures).

**Facts supplied by Elhaj 2026-08-04:**
- Original proposal title: *"Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement"* — predates CSQE.
- Supervisor: **Dr. Tahani** — full name still being confirmed; use "Dr. Tahani" for now.
  ⚠️ **Spelling to confirm:** the repo uses *Tahani* throughout; verify against her own usage before printing.
- Submission: **August 2026.**
- Everything else follows the current Overleaf template.

---

## 1. Ownership split

| Osman | Elhaj |
|---|---|
| **J11** apply D2's appendix moves | **J10** front matter (title page, declaration, acknowledgments) |
| **D3** code appendix | **T1** decide the title |
| **E1 / E2 / E3** figures and tables | **C9** dedication |
| Fig 4.7 / 4.8 regeneration (H1 tail) | **B2** Arabic abstract |
| | **H1 / H2 / H3** temperature corrections |
| | **D5** conciseness pass — last |
| | Joint: **F1**, **G1**, **G2** |

---

## 2. T1 — The title

### Why the proposal title no longer fits

*"Improving Retrieval **Recall** in Arabic RAG Systems via Query Enhancement"*

Two problems, both created by work done after the proposal:

1. **"Recall" is now the wrong metric.** The thesis's headline is **NDCG@10** (0.4621 → 0.7137).
   Recall@10 and Recall@100 are reported, but every claim in the abstract and Ch.5 is stated in
   NDCG. A title promising recall improvement, followed by a thesis reporting ranking quality,
   is the kind of mismatch a committee notices immediately.
2. **"Query Enhancement" alone understates the contribution.** Phase A established that the
   thesis is about *corpus-steered* expansion and *where in a hybrid pipeline* to apply it.
   The plain term covers the Query2Doc baseline, not the finding.

### Options

| # | Title | Words | Notes |
|---|---|---|---|
| **A** | **Improving Retrieval Quality in Arabic RAG Systems via Corpus-Steered Query Enhancement** | 11 | Keeps the proposal's exact shape, so it reads as the same project matured. One word fixed (Recall→Quality), one added (Corpus-Steered). |
| **B** | Improving Arabic Retrieval in RAG Systems via LLM-Based Query Enhancement | 10 | Simplest. Safe. Does not name the contribution. |
| **C** | Corpus-Steered Query Enhancement for Arabic Retrieval-Augmented Generation | 9 | Shortest and most modern-sounding. Drops "Improving", so it reads as a method paper rather than a project. |
| **D** | Query Enhancement for Arabic Information Retrieval: Blind and Corpus-Steered Expansion | 11 | Mirrors the research question most closely. The colon makes it feel like a paper, not a B.Sc. thesis. |

**DECIDED 2026-08-08 by Elhaj — none of A–D. Option E, added below. No subtitle.**

| # | Title | Words | Notes |
|---|---|---|---|
| **E** | **Improving Retrieval Quality in Arabic RAG Systems via LLM-Based Query Enhancement** | 12 | **CHOSEN.** Keeps the proposal's exact shape. Two changes: Recall→Quality, +LLM-Based. |

**Why A was rejected.** A's *"via Corpus-Steered Query Enhancement"* narrows the thesis to its
final experiment. CSQE is objective 8 of 9 (`chapter1.tex:28-44`); the title said nothing about
the baselines, the error analysis, the Query2Doc adaptation, the ten-model comparison, the
repetition sweep, the hybrid fusion baseline, or the placement finding.

**Why "Enhancement" and not "Expansion".** Elhaj also considered *"Enhancing Arabic Information
Retrieval for RAG Systems Using LLM-Based Query Expansion"*. Rejected on the thesis's own
terminology: **QE is defined as Query *Enhancement*, the umbrella intervention**
(`chapter1.tex:9`, `5-Abstract.tex`, `7-ListofAbbreviations.tex:48`), while *query expansion*
is used throughout for the specific mechanism — CSQE, Query2Doc, the generated text (33
occurrences, all in that narrower sense). "Expansion" in the title would therefore have been
the *narrower* word, the opposite of the intent. It also broke proposal continuity three ways
(Improving→Enhancing, Retrieval Quality→Information Retrieval, via→Using).

⚠️ **Known inconsistency, not fixed here:** the body prose favours "query expansion" while the
abbreviation list defines QE as "Query Enhancement". The title now follows the abbreviation
list. If D5 standardises the body, the two must stay aligned.

**A subtitle was drafted and dropped.** *"A Comparative Study of Models, Retrievers, and
Corpus-Steered Expansion"* was built and rendered, then removed — Elhaj preferred a clean
single title. The breadth argument it carried is satisfied by "LLM-Based Query Enhancement"
being the umbrella term.

**Applied:** `1-main.tex:136-151`, 20 pt bold, two lines, `xelatex`-verified to fit one page.

⚠️ **Check before deciding:** if the title is **formally registered** with the department, it
may not be changeable, and the proposal title must be used as-is.

---

## 3. J10 — Front matter

### 3.1 Title page — `1-main.tex:100-119`

| Field | Now | Becomes |
|---|---|---|
| Title | "This is the Thesis Title" | *the T1 decision* |
| Size | `\Large` ≈ 17.3 pt | **20 pt bold** — voice note 1 [01:47] |
| Student 1 | "Student Name (Index)" | **Mohammed Elhaj Sami** (index needed) |
| Student 2 | "Student Name (Index)" | **Osman Bashir** (index needed) |
| Supervisor | "Supervisor name" | **Dr. Tahani** *(full name pending)* |
| Date | "September 2024" | **August 2026** |

⚠️ **Still needed: both index numbers.** Nothing in the repo has them.
⚠️ **Full names must be printed in full** (Elhaj's instruction) — confirm Osman's full name; the
repo has only "Osman Bashir".

### 3.2 Declaration of Authorship — `2-DeclarationofAuthorship.tex`

Currently one template instruction sentence and no declaration. Two signature blocks (two
authors). Draft wording is in `FRONT_MATTER_PLAN.md` §5.
⚠️ Confirm the department has no mandated wording before printing a generic one.

### 3.3 Acknowledgments — `4-Acknowledgements.tex`

Elhaj's brief: mention **Dr. Tahani**, **the war and the current circumstances in Sudan**,
**families and friends**, **the University of Khartoum**, and **our hopes**. It should be
heartfelt, not formulaic.

⚠️ **This page should be written by Elhaj and Osman personally**, in a dedicated session.
A generated acknowledgement is the one page where that is obvious to a reader. What can be
prepared in advance is the *structure* and a first draft to react to — not the final text.

### 3.4 Dedication — `3-Dedication.tex` (task C9)

Bare heading. Personal. Elhaj now owns it.

### 3.5 Page-numbering conflict — fold in here

`1-main.tex:122` places `\pagenumbering{roman}` **after** the titlepage, so the Declaration is
numbered **i** instead of **ii**. The faculty guidelines say roman numerals begin *with* the
title page. One-line fix; shifts every front-matter numeral. Open since C8 (2026-07-28).

---

## 4. H1 / H2 / H3 — the temperature corrections

Three separate defects in **Chapter 3, Table 3.2** (the generation-hyperparameter table) and
one in Chapter 4. None changes a headline result.

### H2 — Jais-2 8B temperature is wrong *(smallest; do first)*
`chapter3.tex:294` prints Jais-2 8B at **0.1**. Its own notebook sets `TEMPERATURE = 0.7`, and
the feeder CSV `table_3_2_gen_hyperparams.csv:8` says **0.7**. The `.tex` cell is the outlier.
**Fix: change one cell to 0.7.** No Ch.4/Ch.5 numbers move.

### H3 — Table 3.2 caption may misstate `top_p`
The caption says *"top_p = 0.9 unless otherwise noted"*. An earlier investigation reported
Qwen3-4B actually used `top_p=0.8, top_k=20` (Qwen3's developer-recommended settings), but the
CSV records `0.9`. **Agent and CSV disagree — read `Query_generator_qwen3_4B.ipynb` before
changing anything.** If the notebook confirms 0.8, both the CSV and the caption need correcting.

### H1 — SILMA's repetition sweep used the wrong file
The Exp 1.1 sweep loaded `silma_2b_temp07.pkl` while every other model used its temp-0.1
expansions. Result: **Table 4.7 says 0.4277 and Table 4.11 says 0.4194 for the same
configuration.**

**Osman has already fixed the notebook** (`0d7bfe3` — one line in `phase4_quick_wins (1).ipynb`).
**The re-run has not happened**, so the thesis still prints the wrong number.

- **Option A (recommended):** re-run the 8 SILMA repetition configs in Colab. **~8 minutes, no
  LLM inference** — it only reloads the already-generated temp-0.1 expansions. Sanity check:
  the new n=1 must land on **0.4277**, which doubles as proof the re-run is wired correctly.
  Then update Tables 4.11/4.12.
- **Option B:** keep 0.4277 in Table 4.7 and footnote Table 4.11 that SILMA's sweep used
  temp 0.7. Table 4.12's Δ=+0.0639 stays correct as printed.
- **Rejected:** changing Table 4.7 to 0.4194 — it would split SILMA's dense and sparse rows
  across two temperatures.

⚠️ **Figures 4.7 and 4.8 currently plot different SILMA values** because they read different
CSVs. They need regenerating from one source **regardless of which option is chosen** — and
that part is **Osman's**, under the figures split.
⚠️ Also independent of the choice: `model_comparison_bm25.csv:3` and `table_4_3.tex:6` pair
temp-0.1 n=1 metrics with the temp-0.7 best config, giving Δ=0.0555, which matches neither table.

Full evidence: `SILMA_CONFLICT_RESOLUTION.md`, `SILMA_TEMPERATURE_RATIONALE_CHECK.md`.

---

## 5. B2 — Arabic abstract

Currently ~1.5 pages; must become ≈ ¾ page and **be re-derived from the new English abstract**
(315 words, rewritten 2026-08-01), not from the old one.

Rules (Report §9, video 2 08:08–09:20):
- Full Arabisation of technical terms where standard equivalents exist —
  الاسترجاع الكثيف, التوليد المعزز بالاسترجاع (RAG).
- Arabic term first, English acronym in parentheses at first mention.
- **ASCII/Western numerals** (0, 1, 2 …) throughout, matching the English side.
- ⚠️ The faculty guideline *"no multiple paragraphs"* applies here too — the English abstract
  is now a single paragraph, so the Arabic one should match.

---

## 6. D5 — Conciseness pass (last)

Agreed method (video 2 21:00–24:25): for each flagged passage give current text → proposed
shorter text → **a confidence score**. High-confidence trims batch-approved; low-confidence
reviewed individually.

⚠️ **Do not start until Osman's appendix moves (J11) land** — they change what is left to trim,
and D2 estimates ~3.5 pages recoverable from §2.4 alone.
Current core: **101 pages**. Target: comfortably under 100.

---

## 7. Suggested order

| Step | Task | Blocked by |
|---|---|---|
| 1 | **T1** decide the title | — |
| 2 | **H2** (one cell) | — |
| 3 | **H3** — read the Qwen3-4B notebook, then decide | — |
| 4 | **J10** title page + declaration + numbering fix | T1, index numbers |
| 5 | **H1** — Colab re-run, then Tables 4.11/4.12 | Figs 4.7/4.8 are Osman's |
| 6 | **B2** Arabic abstract | — (English abstract is final) |
| 7 | **Acknowledgments + C9 dedication** — dedicated session, written personally | — |
| 8 | **F1** intuitive explanation (defence prep) | — |
| 9 | **G1** review the task list | everything logged |
| 10 | **D5** conciseness | Osman's J11 |
| 11 | **G2** final joint read-through | all of the above |

---

## 8. Open questions for Elhaj

1. **Title** — pick from §2, or confirm the registered proposal title must be kept.
2. **Index numbers** — both.
3. **Osman's full name** as it should be printed.
4. **Dr. Tahani's full name and title** — and confirm the spelling *Tahani*.
5. **H1** — Option A (re-run, ~8 min) or Option B (footnote)?
6. **Declaration wording** — is there a department-mandated text?
