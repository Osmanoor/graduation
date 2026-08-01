# C10 — Chapter Summaries: Presence & Style Audit

**Task:** C10 (`research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md:167-168`) — *"Dr. Tahani: optional but keeping them is 'ممتاز'. **Decision: keep.** Just verify every chapter actually has one and the style is consistent."*
**Date:** 2026-08-01 · **Scope:** READ-ONLY audit. No `.tex` file was modified.
**Supervisor source verified:** `meetings/Thesis Review Report.md:8-10` — *"You are not strictly required to have a 'Chapter Summary' at the end of each chapter, but keeping them is **excellent** ('ممتاز'). It provides a clean recap of the chapter's contents and does not disrupt the flow."*

**Headline verdict: C10 does NOT pass as-is.** Two genuine defects (one structural, one typographic-in-print), plus three cosmetic. All numeric claims inside the summaries are correct. The recommended fix set is **page-neutral (0 pages)**.

---

## 0. Page-budget baseline (measured, not assumed)

From the last clean build artefacts (`1-main.aux`, `1-main.pdf`, `1-main.log`, all dated 2026-07-29 22:38) and the per-chapter `.aux` files:

| Chapter | Starts (printed p.) | Ends | Pages |
|---|---|---|---|
| Ch.1 Introduction | 1 | 6 | 6 |
| Ch.2 Background | 7 | 36 | 30 |
| Ch.3 Methodology | 37 | 61 | 25 |
| Ch.4 Results | 62 | 96 | 35 |
| Ch.5 Conclusion | 97 | 105 | 9 |
| **Core manuscript (Ch.1–5)** | | | **105** |
| Bibliography starts | 106 | — | (excluded) |

> ⚠️ **The page count has drifted.** Task D1 (`THESIS_FINAL_SUBMISSION_TASKS.md:175-176`) records **103 pages, bibliography at p.104**. The current build gives **105 pages, bibliography at p.106** — the manuscript has grown 2 pages since D1 was written, so it is now **5 over the 100-page limit**, not 3. Also note `Chapters/chapter5.tex` was modified 2026-07-31, *after* this build, so a re-measure is due. The brief's "~104" is between the two figures. **AI Suggestion:** D1 should be re-run and the number in the task list updated.

Printed page = PDF page − 19 (arabic numbering starts at PDF p.20, per `1-main.aux` `\HyPL@Entry{19<</S/D>>}`). `\documentclass[12pt,a4paper]{report}`, `\geometry{margin=1in}` → `\textwidth` ≈ 452 pt. Chapters open on any page (Ch.4 begins on even p.62), so no forced blank versos.

---

## 1. Presence table

| Ch. | Closing summary? | Exact command | Title | file:line | Is it the LAST section? | Printed pages occupied |
|---|---|---|---|---|---|---|
| 1 | **No** | — (last section is `\section{Thesis Layout}`) | — | `Chapters/chapter1.tex:48` | n/a — §1.3 is last | — |
| 2 | **Yes** | `\section{Chapter Summary}` | "Chapter Summary" | `Chapters/chapter2.tex:491` | ✅ Yes (§2.6, file ends l.510) | p.34 (bottom ~15 %) + p.35 (full) + p.36 (top ~12 %) |
| 3 | **No** | — (last section is `\section{Per-Query Error Analysis}`) | — | `Chapters/chapter3.tex:491` | n/a — §3.9 is last | — |
| 4 | **Yes** | `\section{Summary of All Experiments}` | "Summary of All Experiments" | `Chapters/chapter4.tex:945` | ✅ Yes (§4.11, file ends l.985) | p.95 (bottom ~40 %) + p.96 (Table 4.28) |
| 5 | **No** | — (last section is `\section{Recommendations for Future Work}`) | — | `Chapters/chapter5.tex:64` | n/a — §5.3 is last | — |

**Both existing summaries are correctly placed as the final `\section` of their chapter.** Neither uses `\section*`; neither is nested at the wrong depth. There is no summary anywhere in Ch.1, Ch.3 or Ch.5 (verified by exhaustive grep of `^\\(chapter|section|subsection)\*?\{` and of the string `summar` across `chapter[1-5].tex`).

**Table of Contents as a committee will read it:**

```
2.6  Chapter Summary
3.9  Per-Query Error Analysis      ← no summary; the chapter just stops
4.11 Summary of All Experiments
5.1  Conclusions / 5.2 Challenges / 5.3 Recommendations
```

The Ch.3 gap is visible from the ToC alone. That is the core C10 failure.

---

## 2. Style-consistency comparison

| Axis | Ch.2 §2.6 (`chapter2.tex:491-510`) | Ch.4 §4.11 (`chapter4.tex:945-985`) | Consistent? |
|---|---|---|---|
| **Title wording** | "Chapter Summary" | "Summary of All Experiments" | ❌ **No** |
| **Sectioning level** | `\section` (numbered, in ToC) | `\section` (numbered, in ToC) | ✅ Yes |
| **Starred?** | No | No | ✅ Yes |
| **Label** | `\label{sec:chapter_summary}` (l.492) | `\label{sec:res_summary}` (l.946) | ⚠️ Different scheme, but each matches its own chapter's convention (Ch.2 uses bare topical labels `sec:rag`, `sec:related_work`…; Ch.4 uses the `sec:res_*` prefix throughout). **Not a defect.** |
| **Label referenced anywhere?** | No — orphan | No — orphan | ✅ Consistent (both orphaned; belongs to task E3, dead-label sweep) |
| **Total words** (LaTeX stripped) | **377** | **103** prose + a 17-data-row table | ❌ **No** — 3.7× ratio in prose |
| **Paragraph / block count** | 1 intro sentence (22 w) + `itemize` of 10 bullets (300 w) + 1 closing paragraph (55 w) | 1 framing sentence (34 w) + `table` float + 1 closing paragraph (69 w) | ❌ **No** |
| **Form** | Bulleted list, prose bullets, no bold leads | Table-centric; continuous prose around it | ❌ **No** |
| **Per-bullet section cross-refs** | Yes — every one of the 10 bullets ends `(Section~\ref{...})`; all 9 distinct targets resolve | No per-item refs; one range ref `Sections~\ref{sec:res_repetition}--\ref{sec:res_error_csqe}` at l.985 | ❌ **No** |
| **Contains numbers/metrics** | Essentially none ("Ten language models", "7–8 billion parameters") | Heavy — a full 17-row results table plus 0.7137 / 54.5 % / 13.9 % in prose | ❌ **No** — but see note below |
| **Tense** | Mixed *by design*: present for standing facts ("RAG systems address…", "Arabic presents…"), past for thesis actions ("were formulated", "was selected", "were described"); framing sentence past ("This chapter established…") | Present for the artefact ("Table 4.28 provides…"), past for results ("The best system … achieved", "were presented") | ✅ Yes — same convention |
| **Voice** | Formal academic; passive for research actions, active only with inanimate subjects | Same | ✅ Yes |
| **Content pattern** | Recaps what the chapter did, section by section, **and** previews the next chapter (l.510) | Consolidates findings; **no** forward reference to Ch.5 | ❌ **No** |
| **Spelling register** | "summariz**ed**" (l.495), "Arabic-specializ**ed**" (l.504) — American | "nDCG@10" in prose (l.985) vs. "NDCG@10" in its own table header (l.957) | ⚠️ Both deviate, differently — see §4 |

### Prose notes

**The two summaries are different genres, not two instances of one genre.** Ch.2's §2.6 is a *chapter recap*: it walks the chapter's own sections in order, cross-references each, and hands off to Ch.3. Ch.4's §4.11 is a *consolidated results appendix in section clothing*: it exists to give one table that gathers every experiment, and the surrounding prose is a caption-extension rather than a recap. §4.11 never mentions §4.1–4.5 (baselines, error analysis, Query2Doc, model comparison, cross-cutting findings) — its one cross-reference (`Sections 4.6–4.10`) explicitly covers only the *second half* of the chapter, so §4.11 does not in fact summarise Chapter 4.

That said, the *register* is uniform: both are formal, both use passive for research actions and past tense for results, and neither slips into first person or informality. The divergence is structural (title, form, coverage), not tonal.

**On the numbers asymmetry:** Ch.2 has no metrics because Ch.2 reports no experiments — this is correct, not an inconsistency. What *is* inconsistent is that Ch.2's summary forward-references the next chapter and Ch.4's does not; and that Ch.2's enumerates the chapter's sections and Ch.4's does not.

---

## 3. Chapter 1 and Chapter 5 special cases

### Chapter 1 (Introduction) — absence is **CORRECT, not a defect**

`chapter1.tex` runs: opening framing (l.5–11) → §1.1 Problem Definition (l.14) → §1.2 Objectives (l.21) → §1.3 Thesis Layout (l.48–60). §1.3 already performs the closing-recap function — it walks Ch.2 through Ch.5 and tells the reader what each contains. A "Chapter Summary" after it would summarise a section that is itself a summary.

This is also what the supervisor asked for: `meetings/Thesis Review Report.md:31-33` (Q6) directs that "the section at the end of Chapter 1 (Thesis Layout / Outline) should be one long paragraph summarizing the structure of the manuscript." She placed the closing-overview role in §1.3 explicitly. Normal thesis convention agrees: an Introduction ends with the thesis outline, not with a summary of the introduction.

**Verdict: no summary needed in Ch.1. Do not add one.** (Adding a ~150-word one would cost 0 pages — p.6 is ~60 % white — but it would be redundant prose in a manuscript that is already 5 pages over budget.)

### Chapter 5 (Conclusion and Recommendations) — absence is **CORRECT, not a defect**

`chapter5.tex:5` opens: *"This chapter summarises the key findings of the research, discusses the challenges encountered during the experimental work, and presents recommendations…"* — §5.1 Conclusions (l.8–36) **is** the thesis-level summary, organised as eleven bold-led findings. Appending a "§5.4 Chapter Summary" would be a summary of a summary, and would sit after the future-work section, ending the manuscript on a backward-looking note.

Ch.5 is also the one chapter where a closing summary would violate convention rather than satisfy it: a conclusions chapter does not get summarised.

**Verdict: no summary needed in Ch.5. Do not add one.**

### Chapter 3 (Methodology) — absence **IS** the defect

Unlike Ch.1 and Ch.5, Ch.3 has no structural substitute. It ends at `chapter3.tex:519` on the third bullet of a regression-type taxonomy (printed p.61, with ~70 % of the page blank) and then Ch.4 simply begins. A reader moving Ch.2 → Ch.3 → Ch.4 gets *summary → nothing → summary*. This is exactly the inconsistency C10 exists to catch.

---

## 4. Defect list, ranked

Revert test applied to every item: *would reverting the change leave a false, self-contradicting, or visibly inconsistent thesis?* Items failing the test are marked ENRICHMENT and excluded from §5.

---

### 🔴 D-1 — BLOCKER — Chapter 3 has no chapter summary

- **Where:** `Chapters/chapter3.tex:519` (end of file; §3.9 is the last section, `chapter3.tex:491`).
- **Why a committee flags it:** the ToC shows "2.6 Chapter Summary" and "4.11 Summary of All Experiments" but nothing for Ch.3. The supervisor's guidance is phrased "at the end of each chapter" (`Thesis Review Report.md:10`) — having them in two of the three body chapters reads as an oversight, which is worse than having none at all. Ch.3 is also the longest continuous methodology stretch (25 pages, 9 sections) and is precisely the chapter that most benefits from a recap.
- **Revert test:** PASS — reverting restores a visibly inconsistent thesis.
- **Minimal fix:** append a `\section{Chapter Summary}` + `\label{sec:meth_summary}` (matching Ch.3's `sec:meth_*` convention) after `chapter3.tex:519`, styled on Ch.2's §2.6: one framing sentence, a short `itemize` where each bullet ends with a `Section~\ref{}` to a §3.x, and a one-sentence hand-off to Ch.4.
- **Page cost: 0 pages — IF kept to ≤ 150 words.** Printed p.61 is ~70 % blank (verified in `1-main.pdf`, PDF p.80). Available: ~21 lines. Subtract ~4 lines for the `\section` heading and its vertical skip, ~3 lines for `itemize` inter-item spacing → **~14 lines ≈ 150 words** of usable space. **At 150–200 words this spills to p.62 and costs +1 page.** Ch.2's §2.6 at 377 words would cost +1 page here — do not copy its length.
  - Suggested shape to hit the budget: 1 framing sentence (~18 w) + 6 bullets × ~20 w (~120 w) + fold the Ch.4 hand-off into the last bullet instead of a separate paragraph. Total ≈ 140 w.
  - Section targets available for the bullets: `sec:meth_dataset`, `sec:meth_baseline`, `sec:meth_error`, `sec:meth_query2doc`, `sec:meth_model_comparison`, `sec:meth_repetition`, `sec:meth_hybrid`, `sec:meth_csqe`, `sec:meth_error_csqe` (all confirmed to exist).

---

### 🔴 D-2 — BLOCKER — Table 4.28, the centrepiece of Ch.4's summary, overflows the page and is printed with its last column cut off

- **Where:** `Chapters/chapter4.tex:955-982` (`\begin{tabular}{@{}llcccc@{}}` … `\end{tabular}`, `\label{tab:full_summary}` at l.954).
- **Evidence:** `1-main.log` — `Overfull \hbox (105.60811pt too wide) in paragraph at lines 955--983`. Confirmed visually: on printed p.96 (PDF p.115) the `Status` column runs off the right margin and off the paper — the rendered values read "Baselin", "Best no-Q", "Degrade", "Best BM25 ", "Best Dense ", "Best BM25 ", "Best overa". 105.6 pt ≈ 3.7 cm of overflow against a 452 pt `\textwidth`.
- **Why a committee flags it:** this is the single table a reader turns to for the whole thesis at a glance, and a column of it is physically missing from the printed page. It is the most conspicuous formatting fault in either summary section.
- **Revert test:** PASS — reverting restores a table that is literally unreadable in print.
- **Minimal fix (recommended), page-neutral:** wrap the tabular in `\resizebox`. Table height is unchanged, so the float still occupies p.96.

  Before — `chapter4.tex:955` and `:982`:
  ```latex
      \begin{tabular}{@{}llcccc@{}}
      ...
      \end{tabular}
  ```
  After:
  ```latex
      \resizebox{\textwidth}{!}{%
      \begin{tabular}{@{}llcccc@{}}
      ...
      \end{tabular}}
  ```
  Scale factor lands at ≈ 0.81 (effective ~9.7 pt) — legible and deterministic.

- **Alternative fix A (matches in-thesis precedent):** insert `\footnotesize` and `\setlength{\tabcolsep}{3pt}` immediately after `\centering` (`chapter4.tex:952`). `\footnotesize` alone is *not* sufficient — it scales glyphs by 10/12 but leaves the 10 `\tabcolsep` gaps (60 pt) untouched, landing ~23 pt still over; with `\tabcolsep=3pt` it fits with ~7 pt to spare. Precedent: `chapter2.tex:281` uses bare `\footnotesize` for Table 2.2 — the only table-narrowing precedent in the whole manuscript.
- **Alternative fix B (page-neutral, removes clutter):** delete the `Status` column entirely (6 → 5 columns). Its content is editorial commentary — "OK", "Good", "Degraded" — and its "Best …" entries duplicate what the caption at l.953 already says the bold values indicate. This removes ~110 pt at a stroke. Costs a small amount of information; use only if the team prefers a cleaner table.
- **Page cost of all three options: 0 pages.**

---

### 🟡 D-3 — MINOR — The two summaries have different section titles

- **Where:** `Chapters/chapter2.tex:491` `\section{Chapter Summary}` vs. `Chapters/chapter4.tex:945` `\section{Summary of All Experiments}`.
- **Why it matters:** it is visible in the ToC, and C10's brief is precisely "the style is consistent". With D-1 fixed, the ToC would otherwise read "Chapter Summary / Chapter Summary / Summary of All Experiments".
- **Revert test:** BORDERLINE-PASS — reverting does not make anything false, but it leaves the one artefact C10 was asked to make uniform visibly non-uniform across three chapters. Included on the strength of the task wording.
- **Minimal fix:**
  - Before (`chapter4.tex:945`): `\section{Summary of All Experiments}`
  - After: `\section{Chapter Summary}`
  - The "summary of all experiments" wording survives verbatim in the table caption (`chapter4.tex:953`), so no information is lost.
- **Page cost: 0 pages** (title shortens by 15 characters; no reflow of body text).
- **Note:** the `\label{sec:res_summary}` should NOT be renamed — it is orphaned but renaming it is churn with zero visible effect.

---

### 🟡 D-4 — MINOR — `nDCG@10` vs `NDCG@10` *inside a single summary section*

- **Where:** `Chapters/chapter4.tex:985` writes "achieved 0.7137 nDCG@10", while the table header three lines of code above it — `chapter4.tex:957` — writes `\textbf{NDCG@10}`, and Ch.2's summary at `chapter2.tex:502` writes "NDCG@$k$".
- **Why it matters:** the two casings appear on facing pages of the same section (p.95 prose, p.96 table). Cross-summary, Ch.2 says NDCG and Ch.4 says nDCG.
- **Revert test:** BORDERLINE-PASS locally (same acronym, two casings, one section).
- **Minimal fix:** `chapter4.tex:985` — `0.7137 nDCG@10` → `0.7137 NDCG@10`.
- **Page cost: 0 pages.**
- ⚠️ **Caveat:** this is a *thesis-wide* problem, not a summary problem — the chapters contain **100 `NDCG`** and **48 `nDCG`** occurrences. Fixing only l.985 makes §4.11 internally consistent but leaves the document mixed. See OUT OF SCOPE §7.

---

### 🟡 D-5 — MINOR — American spelling inside Ch.2's summary, against the thesis's British register

- **Where:** `Chapters/chapter2.tex:495` "The key points are **summarized** as follows" and `chapter2.tex:504` "Arabic-**specialized**".
- **Evidence of the norm:** the chapters use British `-ise/-isation` 47:0 for *analysis/analysed*, 10:1 for *summarise*, 15:5 for *quantisation*, 4:7 for *specialise* (the one near-even case). `chapter2.tex:275`, twenty lines from the summary, already writes "Table 2.2 **summarises** the ten LLMs".
- **Revert test:** BORDERLINE-PASS for l.495 (the same verb spelled two ways within one chapter); FAIL for l.504 (*specialize* is genuinely mixed thesis-wide, so changing one instance fixes nothing).
- **Minimal fix (l.495 only):** `are summarized as follows` → `are summarised as follows`.
- **Page cost: 0 pages.**

---

### ⚪ D-6 — ENRICHMENT — do not do — Table 4.28 lists the no-QE hybrid twice

`chapter4.tex:962` (`None (baseline) & BM25+Dense (RRF) & 0.6267 & 0.7597 & 0.6517 & Best no-QE`) and `chapter4.tex:977` (`Hybrid RRF $k=20$ & BM25+Dense & 0.6267 & 0.7597 & 0.6517 & Best no-QE hybrid`) are the same system with identical numbers and two different status labels. It is deliberate — the second occurrence anchors the "Expanded experiments" block. **Revert test: FAIL** (nothing false or contradictory; the duplication is a legible design choice). Leave it. *(If D2/D5 later need a row, this is the first candidate — saves ~1 line, 0 pages.)*

### ⚪ D-7 — ENRICHMENT — do not do — §4.11 does not recap §4.1–4.5

Making §4.11 a true chapter recap (adding bullets for baselines, error analysis, Query2Doc, model comparison, cross-cutting findings) would fully align it with Ch.2's form. **Revert test: FAIL** — nothing in the current text is false, and this would add ~150–250 words to a chapter already 35 pages long, costing **+1 page** in a manuscript 5 pages over limit. Structural symmetry is not worth a page here. **Excluded.**

### ⚪ D-8 — ENRICHMENT — do not do — §4.11 has no forward reference to Ch.5

Ch.2's summary ends by previewing Ch.3 (`chapter2.tex:510`); Ch.4's does not preview Ch.5. **Revert test: FAIL** — §4.10 already ends by handing off to Ch.5 (`chapter4.tex:942`: *"Both are developed as recommendations in Chapter~\ref{chap:conclusion}"*), so the hand-off exists, one section earlier. Adding a second one is redundant. **Excluded.**

---

## 5. Recommended minimal action set

The shortest edit list that makes C10 pass:

| # | Edit | File:line | Page delta |
|---|---|---|---|
| 1 | Add `\section{Chapter Summary}` + `\label{sec:meth_summary}` + **≤ 150 words** of bulleted recap | append after `Chapters/chapter3.tex:519` | **0** (fits p.61's white space; +1 if it exceeds ~150 words) |
| 2 | Wrap Table 4.28's `tabular` in `\resizebox{\textwidth}{!}{…}` | `Chapters/chapter4.tex:955` and `:982` | **0** |
| 3 | Retitle `\section{Summary of All Experiments}` → `\section{Chapter Summary}` | `Chapters/chapter4.tex:945` | **0** |
| 4 | `nDCG@10` → `NDCG@10` | `Chapters/chapter4.tex:985` | **0** |
| 5 | `summarized` → `summarised` | `Chapters/chapter2.tex:495` | **0** |
| | **TOTAL** | | **0 pages** |

**Explicitly NOT recommended:** adding a summary to Ch.1 or Ch.5 (§3 — both absences are correct); expanding §4.11 into a full chapter recap (D-7, +1 page); any change to Ch.2's §2.6 beyond edit 5.

Items 1 and 2 are the ones a committee would actually catch. Items 3–5 are 60 seconds of work and are only worth doing in the same sitting.

**Ordering note:** item 1 must be written *after* the Ch.3 content edits settle, per the original deferral rationale (`OSMAN_WAVE1_PROMPTS.md:5`). Ch.3 has been stable since 2026-07-30, so it is now safe to write.

---

## 6. Verification of factual claims inside the summaries

Every number appearing in either summary was checked against `CLAUDE.md` ("Reference Baselines…" / "Error Analysis Key Numbers") **and** against the chapter body it summarises.

### Table 4.28 (`chapter4.tex:955-982`) — 17 data rows, **all correct**

| Row | Table 4.28 | CLAUDE.md canon | Chapter-body cross-check | ✓ |
|---|---|---|---|---|
| Dense baseline | 0.4993 / 0.6156 / 0.5328 | 0.4993 / 0.6156 / 0.5328 | — | ✅ |
| BM25 baseline | 0.4621 / 0.5964 / 0.4836 | 0.4621 / 0.5964 / 0.4836 | `ch4:192-196` | ✅ |
| Hybrid RRF (baselines block) | 0.6267 / 0.7597 / 0.6517 | 0.6267 / 0.7597 / 0.6517 | — | ✅ |
| Qwen 2.5 3B Dense | 0.5435 / 0.6608 / 0.5742 | identical | — | ✅ |
| Qwen 2.5 3B BM25 | 0.4090 / 0.5384 / 0.4342 | 0.4090 (n=1) | `ch4:193-195`, `ch4:310` | ✅ |
| Falcon-H1 3B Dense | 0.5359 / 0.6484 / 0.5681 | identical | — | ✅ |
| Jais-2 8B Dense | 0.6018 / 0.7161 / 0.6356 | identical | `ch4:260` | ✅ |
| Jais-2 8B BM25 | 0.5122 / 0.6448 / 0.5397 | 0.5122 (n=1) | `ch4:305` (rank 1, +10.8 %) | ✅ |
| Qwen3-4B Dense | 0.5691 / 0.6824 / 0.6015 | identical | — | ✅ |
| ALLaM 7B Dense | 0.2550 / 0.3335 / 0.2708 | identical (struck-through = dropped) | `ch5:50` | ✅ |
| Aya 8B Dense | 0.6164 / 0.7256 / 0.6493 | identical | `ch4:259` | ✅ |
| Aya 8B BM25 | 0.5046 / 0.6284 / 0.5377 | 0.5046 (n=1) | `ch4:306` | ✅ |
| Aya 8B β=2 BM25 | 0.5855 / 0.7128 / 0.6165 | 0.5855 | `ch4:477` exact match | ✅ |
| Hybrid RRF k=20 | 0.6267 / 0.7597 / 0.6517 | identical | — | ✅ |
| BM25+CSQE | 0.6157 / 0.7447 / 0.6380 | identical | — | ✅ |
| Dense+CSQE | 0.5915 / 0.7073 / 0.6225 | identical | — | ✅ |
| **BM25-expanded RRF** | **0.7137 / 0.8363 / 0.7362** | **0.7137 / 0.8363 / 0.7362** | — | ✅ |

### Prose claims

| Claim | Location | Check | ✓ |
|---|---|---|---|
| "0.7137 nDCG@10 — a 54.5 % improvement over the BM25 baseline" | `ch4:985` | (0.7137 − 0.4621)/0.4621 = **+54.45 %** | ✅ |
| "a 13.9 % improvement over the no-QE hybrid system" | `ch4:985` | (0.7137 − 0.6267)/0.6267 = **+13.88 %** | ✅ |
| "Ten language models … were described" | `ch2:504` | Table 2.3 (`ch2:394-406`) lists exactly 10; `ch2:275` "the ten LLMs evaluated" | ✅ |
| "openly available LLMs of 7–8 billion parameters are capable expansion generators" | `ch2:505` | matches §2.5.2 (`ch2:431-447`) and `LITERATURE_VERIFICATION_FINAL.md` | ✅ |
| All 9 `Section~\ref{}` targets in §2.6's bullets | `ch2:498-507` | `sec:rag`, `sec:ir_methods`, `sec:qe_techniques`, `sec:arabic_challenges`, `sec:math_models`, `sec:dataset_selection`, `sec:models_used`, `sec:related_work`, `sec:research_gap` — **all resolve** | ✅ |
| `Sections~\ref{sec:res_repetition}--\ref{sec:res_error_csqe}` | `ch4:985` | both resolve (`ch4:438`, `ch4:781`) | ✅ |

### The two CLAUDE.md traps — both cleanly avoided

1. **0.7137 (corpus-level pooled) vs. 0.6936 (per-query mean of the best system).** §4.11 quotes **only 0.7137**, and only ever as a corpus-level system score, alongside the 54.5 % / 13.9 % deltas that are themselves corpus-level. The per-query mean never appears in either summary. **No mixing. ✅**
2. **Query-length buckets (canon: 1-3 / 4-8 / 9+ words).** Neither summary mentions query-length buckets at all. **No violation possible. ✅**

**Result: ZERO numeric defects in either summary section.** This defect class — the highest-severity one — is empty.

---

## 7. OUT OF SCOPE — candidate new tasks

Real problems found while auditing, that C10 should not absorb:

1. **🔴 Four more Ch.4 tables overflow the text block** — same defect class as D-2, outside the summary sections. From `1-main.log`:
   - `chapter4.tex:665-681` (`tab:csqe_hybrid_configs`) — **168.5 pt** too wide (worst in the thesis)
   - `chapter4.tex:735-749` (`tab:delta_analysis`) — **151.6 pt**
   - `chapter4.tex:762-775` (`tab:system_progression`) — **126.4 pt**
   - `chapter4.tex:828-838` (`tab:error_patterns`) — **81.5 pt**
   - Plus `chapter2.tex:390-409` (`tab:model_comparison`) — **87.5 pt**, the only one LaTeX reports as `in alignment`.
   → **Belongs to task E3** (`THESIS_FINAL_SUBMISSION_TASKS.md:207-208`, "every Ch.4 table … doesn't overflow pages"). E3 is currently figure-gated; these five are independent of the figure work and could be fixed now. `tab:csqe_hybrid_configs` carries the thesis's central placement claim (0.7137 > 0.6936 > 0.6474) and is currently printed with a column missing — arguably the most damaging single formatting fault in the manuscript.

2. **🟡 `NDCG` vs `nDCG` casing is mixed thesis-wide** — 100 vs 48 occurrences across `chapter[1-5].tex`. Ch.2 and Ch.5 use `NDCG` almost exclusively; Ch.3's figure captions (`ch3:441`, `ch3:486`) and most of Ch.4's table headers use `nDCG`. A single global decision + sed is ~10 minutes and costs 0 pages. → **Candidate: fold into D5 (conciseness/proofread pass) or E3.**

3. **🟡 British/American spelling is mixed thesis-wide** — `specialise` 4 : `specialize` 7; `quantisation` 15 : `quantization` 5; `optimisation` 3 : `optimization` 4; `normalisation` 3 : `normalization` 3. The document is ~80 % British overall. → **Candidate: fold into D5.**

4. **🟡 §1.3 Thesis Layout is still four bold-led paragraphs, not one continuous paragraph** — `chapter1.tex:52-60` uses `\textbf{Chapter~\ref{...}}` leads, one paragraph per chapter. Dr. Tahani's Q6 answer (`Thesis Review Report.md:31-33`) requires **one single continuous paragraph, no bullets**. This is already logged as **task C4** (`THESIS_FINAL_SUBMISSION_TASKS.md:139-140`) and is still open — flagged here only because §1.3 is Ch.1's summary-substitute and therefore load-bearing for C10's Ch.1 verdict. Merging the four paragraphs would also recover ~4 lines on p.5–6 (0 to −1 page).

5. **ℹ️ Page-budget lever, informational only — NOT a C10 recommendation.** Ch.2's §2.6 currently forces printed p.36, a page that is ~88 % white. Deleting §2.6 would end Ch.2 on p.34 and save **2 pages**. The decision to keep summaries is settled and this audit does not reopen it — recorded solely so that D5/D2 know the number when hunting the 5 pages the manuscript is over. A cheaper variant with no policy implications: trimming §2.6 from 377 to ~290 words (drop the 55-word closing paragraph at `ch2:510`, whose content duplicates §1.3's Ch.3 paragraph) would pull the section back onto pp.34–35 and save **1 page** while keeping the summary.
