# Wave 2 — Execution Plan (per task)

**Date:** 2026-08-04
**Status:** PLAN ONLY. Nothing here is applied.
**Baseline for every page figure below:** the clean full build of 2026-08-04 —
124 pages total, **core Ch.1–5 = exactly 100**, 0 errors, 0 undefined refs/cites,
body font Times New Roman.

**Read order:** §1 is the summary table. §2 onward is one section per task.
Each task section has the same five headings: **Evidence · Change · Why · Page impact · After (review + verify)**.

---

## 1. Summary

| # | Task | Type | Page impact | Needs a decision from Elhaj? |
|---|---|---|---|---|
| 1 | **J3** Tables printing truncated | Critical | 0 to −1 | Yes — 1 (Table 2.1 cite column) |
| 2 | **J9** Three micro-fixes | Obvious | 0 | No |
| 3 | **J5** Delete dead file | Obvious | 0 | No |
| 4 | **C4** §1.3 → one paragraph | Obvious | **−1.7 lines** | Yes — 1 (merge only, or also condense) |
| 5 | **J7** Singleton subsubsections | Obvious | 0 to −0.1 | Yes — 1 (promote or demote) |
| 6 | **J6** Type C missing in §4.10.4 | Critical | +0.15 or 0 | Yes — 1 (add para, or reword) |
| 7 | **J2** Heading sizes | Critical (marks) | **−1 to −2** | No |
| 8 | **C10** Ch.3 has no summary | Plan | **+0.3** | Yes — 1 (form: prose or bullets) |
| 9 | **C5** Promote bold headings | Plan | **+0.5 to +1** | Yes — 2 (prose repair, orphans) |
| 10 | **J8** 17 unnumbered `\paragraph`s | Plan | +0.7 if done | Yes — 1 (ask supervisor first?) |

**Net if items 1–9 are done:** roughly **−1 to −2 pages**. J2 pays for C5 and C10.

**Ordering rule.** J2, J3 and C5 all re-flow pages. Do **J2 → J3 → C5 → C10 → C4**
in that order, then run E2/E3 **once** at the end. Doing E3 before them wastes the work.

**Deferred, not planned here:** E2, E3, D3, D5 (each needs its own session), and
everything owned by Osman (H1–H3, B2, C9, D4).

---

## 2. J3 — Six tables print with columns cut off

### Evidence

From the 2026-08-04 build log. **These are not cosmetic warnings — text is missing from the printed page.**

Proof for Table 2.1, extracted from the built PDF (page 30):

```
Paper                    Year Family      Method                             Dataset            Key result
Query2Doc (Wang et al.)  2023 generation  LLM pseudo-document concatenation  MS MARCO + BEIR    +8 nDCG@10 on
CSQE (Lei et al.)        2024 generation  Corpus-Steered Query2Doc           TREC-DL            +30% mAP over B
```

`Key result` is cut mid-word. The 7th column, `Cite key`, is entirely off the paper.

| Too wide | Table | Location | Column spec |
|---|---|---|---|
| **306.2 pt** | Table 2.1 (QE literature) | `thesis_figures/output/pdf/table_2_1.tex` | `lllllll` |
| 113.8 pt | `tab:delta_analysis` | `chapter4.tex:735-749` | `@{}lcc@{}` |
| **103.2 pt** | `tab:csqe_hybrid_configs` | `chapter4.tex:665-681` | `@{}llcccc@{}` |
| 69.9 pt | `tab:dense_leaderboard` | `chapter4.tex:250-262` | `@{}clccccc@{}` |
| 57.8 pt | `tab:full_summary` (4.28) | `chapter4.tex:955-983` | `@{}llcccc@{}` |
| 50.9 pt | `tab:system_progression` | `chapter4.tex:762-775` | `@{}llcc@{}` |

Common cause: `l` columns holding long text, which cannot wrap.

`tab:csqe_hybrid_configs` is the table carrying the thesis's central
asymmetric-placement claim.

### Change

**Two different fixes, because one size does not fit.** Text block is 452 pt wide, so:

| Table | Natural width | `\resizebox` scale | Resulting text size | Fix |
|---|---|---|---|---|
| Table 2.1 | 758 pt | 0.60 | **7.2 pt — unreadable** | **structural** |
| `tab:delta_analysis` | 566 pt | 0.80 | 9.6 pt | `\resizebox` |
| `tab:csqe_hybrid_configs` | 555 pt | 0.81 | 9.8 pt | `\resizebox` |
| `tab:dense_leaderboard` | 522 pt | 0.87 | 10.4 pt | `\resizebox` |
| `tab:full_summary` | 510 pt | 0.89 | 10.7 pt | `\resizebox` |
| `tab:system_progression` | 503 pt | 0.90 | 10.8 pt | `\resizebox` |

**(a) Five Ch.4 tables — wrap in `\resizebox`:**

```latex
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}llcccc@{}}
 ...unchanged...
\end{tabular}%
}
```

Smaller type in tables is explicitly permitted: faculty guidelines, *Font* —
*"It is permissible to change point size in tables, figures, captions, footnotes,
and appendix material."* 9.6–10.8 pt is a mild reduction.

**(b) Table 2.1 — structural, fixed at the generator:**

Source of truth is `thesis_figures/data/raw/table_2_1_papers.csv`
(columns: `paper, year, family, method, dataset, key_result, cite_key`).
`output/pdf/table_2_1.tex` is generated from it, so **editing the `.tex` is wrong —
the next regeneration reverts it.**

1. **Remove the `cite_key` column from the rendered table.** It prints raw BibTeX
   keys (`wang\_2023\_query2doc`) — internal bookkeeping that does not belong in a
   thesis. It is already invisible in the current PDF, so removing it costs nothing
   visually and frees ~120 pt.
2. **Drop the `family` column.** 11 of 13 rows read `generation`; the 2 surveys are
   identifiable from their names. Frees ~55 pt.
3. **Convert `method` and `key_result` to `p{}` columns** so they wrap:
   `p{3.6cm}` and `p{3.4cm}`.

⚠️ **DECISION 1 — the `cite_key` column.** Two options:
- **(i) Drop it.** Simplest. The papers are all cited in the §2.5 prose anyway.
- **(ii) Replace it with a real citation column** rendering `\cite{key}` as `[12]`.
  Academically better — the reader can go from the table to the bibliography —
  and a `[nn]` column is only ~20 pt. Costs a change to the generator's escaping.
- **Recommendation: (ii).** It is what the column was clearly meant to be, and IEEE
  style expects table rows to carry their citation.

### Why

Passes the revert test hard: reverting leaves the thesis **printing an incomplete
version of its own central result**, and printing raw BibTeX keys.

### Page impact

`\resizebox` is page-neutral to page-negative (tables get shorter). Table 2.1
becomes taller as text wraps, but loses 2 columns. **Net: 0 to −1 page.**

### After (review + verify)

- Rebuild; confirm all six `Overfull \hbox` entries are gone from `1-main.log`.
- Extract each table from the PDF with `pdftotext -layout` and confirm the **last
  column is fully present** — the warning disappearing is not proof the text is back.
- ⚠️ Table 2.1 must be regenerated through the notebook, not hand-edited. Confirm
  `output/pdf/table_2_1.tex` changed **and** that re-running the notebook reproduces it.
- ⚠️ Re-measure page count. Table 2.1 wrapping may push §2.5 onto a new page.

---

## 3. J9 — Three micro-fixes

### Evidence
| # | Location | Now | Should be |
|---|---|---|---|
| a | `chapter4.tex:945` | `\section{Summary of All Experiments}` | `\section{Chapter Summary}` |
| b | `chapter4.tex:985` | `0.7137 nDCG@10` | `0.7137 NDCG@10` |
| c | `chapter2.tex:495` | `summarized` | `summarised` |

(a) is the only chapter summary in the thesis not called "Chapter Summary" (§2.6 is).
(b) the abbreviation list asserts `NDCG` as canonical. (c) the thesis is British English.

### Change
Three single-token replacements. Nothing else.

### Why
(a) visible inconsistency in the ToC. (b) contradicts the List of Abbreviations.
(c) contradicts the thesis's own spelling convention.

### Page impact
Zero.

### After (review + verify)
- ToC regenerates — needs two xelatex passes.
- ⚠️ **This does NOT close the thesis-wide `nDCG` vs `NDCG` casing problem** (81 × `NDCG@10`
  vs 46 × `nDCG@10`, still open under C3). Fixing one line and leaving 45 makes the
  inconsistency *look* deliberate. Either sweep all 46 or leave (b) until the sweep.
  **Recommendation: fold (b) into the full sweep; do only (a) and (c) now.**

---

## 4. J5 — Delete `Chapters/chapter2_generated.tex`

### Evidence
`grep -rn "chapter2_generated" --include=*.tex .` returns **nothing** — the file is not
`\include`d or `\input` anywhere. It holds an older draft of §2.1.4/§2.1.5 with 20+ bold
pseudo-headings and matched several C5 audit greps.

### Change
`git rm Chapters/chapter2_generated.tex`.

### Why
It is a live trap: any future audit or grep over `Chapters/` hits stale text and may
"fix" a file that is never compiled. It already caused noise in the C5 audit.

### Page impact
Zero — not compiled.

### After (review + verify)
- Rebuild and confirm page count is unchanged (proves it really was unused).
- Recoverable from git history if ever wanted.

---

## 5. C4 — §1.3 Thesis Layout into one paragraph

### Evidence
`chapter1.tex:52-60`. A lead-in line plus **four** paragraphs, each opening with
`\textbf{Chapter~\ref{...}}`. 404 words total (93 / 151 / 127 / 24).

Dr. Tahani, Report Q4 and the Part-3 checklist: *"Convert Section 1.3 into **one single
long paragraph**. Remove bulleted list format."* Also `meetings/17.3.2026.md`.

### Change
1. Delete the four `\textbf{...}` wrappers. The text already reads correctly without
   them — `\textbf{Chapter~\ref{chap:background}} establishes…` becomes
   `Chapter~\ref{chap:background} establishes…`.
2. Join the lead-in and all four paragraphs into one block, changing the lead-in's
   colon to a full stop.

**No rewording required.** This is a markup edit.

⚠️ **DECISION 2 — merge only, or merge and condense?**
- **(i) Merge only.** One 413-word paragraph ≈ 19 lines at 1.5 spacing, about ⅔ page.
  Readable. Satisfies the directive exactly. Passes the revert test.
- **(ii) Merge and condense to ~300 words.** Saves maybe 0.3 page more, helps D5.
  But it is *enrichment* — reverting it would leave nothing false — so it breaks our
  own working rule.
- **Recommendation: (i) now, and let D5 decide about condensing.**

### Why
Direct supervisor instruction, unfulfilled since the July review. §1.3 actually got
*longer* during A7 (fixes B2, M8, M9), so it is more visible now, not less.

### Page impact
Removes 3 paragraph breaks × 12 pt `\parskip` = **−36 pt ≈ −1.7 lines.**

### After (review + verify)
- ⚠️ **C5 conflict resolved by doing this:** the C5 audit lists §1.3 as run "R0" and marks
  it **never promote** precisely because C4 deletes those four bold leads. Do C4; do not
  promote §1.3.
- Check §1.3 does not now break awkwardly across a page.

---

## 6. J7 — Two singleton `\subsubsection`s

### Evidence
- `chapter4.tex:203` — `\subsubsection{Term Dilution Analysis}`, the only child of §4.3.2.
- `chapter4.tex:329` — `\subsubsection{ALLaM-7B}`, the only child of §4.4.3.

A 1-of-1 numbered subdivision is a style smell: `4.3.2.1` with no `4.3.2.2` implies a
missing sibling.

### Change
⚠️ **DECISION 3 — per heading:**
- **(i) Demote to bold run-in text.** Removes the number; keeps the visual break.
  Page-negative.
- **(ii) Promote to `\subsection`.** Makes them `4.3.3` / `4.4.4` — but then they stop
  being *inside* their parent, which changes the argument structure.
- **(iii) Leave.**
- **Recommendation: (i) for `Term Dilution Analysis`** (it is a sub-point of the BM25
  results and reads fine as a labelled paragraph), and **(iii) leave `ALLaM-7B`** —
  §4.4.3 is "Dropped Models Analysis" and the single named model under it is a
  deliberate, meaningful subdivision.

⚠️ Both carry `\label`s (`sec:res_term_dilution`, `sec:res_allam`) that **are referenced**
— `sec:res_term_dilution` from `chapter4.tex:936` and `chapter5.tex:24`. Demoting must
keep the `\label` attached to something, or `\ref` breaks.

### Page impact
0 to −0.1 page.

### After (review + verify)
- Confirm 0 undefined references in the log.
- Confirm §4.3.2's numbering did not shift.

---

## 7. J6 — Type C is reported in the table but never discussed

### Evidence
- `chapter4.tex:900-913`, Table 4.25: three types — **A 191 (52%), B 131 (36%),
  C: Partial BM25 45 (12%)**.
- `chapter4.tex:935-942`: `\paragraph{Type A…}`, `\paragraph{Type B…}`, then
  `\paragraph{Implications.}`. **No Type C paragraph.**
- `chapter4.tex:942` opens *"These **two** failure modes…"* — correct for A and B,
  but the table above it lists three.
- `chapter4.tex:918`, Fig 4.15 caption calls it **"Type C (other)"** while the table
  calls it **"Type C: Partial BM25"**. Inconsistent naming.
- **Chapter 3 already defines Type C properly** (methodology, end of `chapter3.tex`):
  *"The BM25 baseline achieved NDCG@10 between 0.1 and 0.3; a mixed-quality scenario…"*
  So the gap is in the **results** chapter only.

### Change
⚠️ **DECISION 4:**
- **(i) Add a short `\paragraph{Type C: Partial BM25.}`** — 2–3 sentences, drawn from
  the Ch.3 definition and the table's own row. Costs ~4 lines.
- **(ii) Reword only.** Change *"These two failure modes"* → *"These failure modes"*,
  and add a clause to the Type B paragraph noting that the remaining 12% (Type C) sit
  in an intermediate band where the effect is mixed. Costs ~1 line.
- **Recommendation: (ii).** Cheaper, page-friendly, and honest — we do not have a
  distinct *mechanism* for Type C, only a score band. Inventing a paragraph implies an
  analysis we did not do.
- **Either way, fix the Fig 4.15 caption** so "Type C (other)" matches "Partial BM25".

### Why
As printed, the chapter enumerates three categories and explains two, then calls them
"two failure modes". That is self-contradicting on the page — it passes the revert test.

### Page impact
(i) +0.15 page. (ii) ~0.

### After (review + verify)
- ⚠️ Check Ch.5 does not repeat the "two failure modes" phrasing. `chapter5.tex:81` and
  `:83` name Type B and Type A recommendations only — verify that is still consistent.
- Verify 45 / 12% against the raw per-query analysis before printing any new number.

---

## 8. J2 — Heading sizes do not match the supervisor's spec

### Evidence
Dr. Tahani, voice note 1 (`meetings/2026-07_supervisor_voice_notes_transcripts.md`):
- **[01:47]** cover-page project name: *"تايمز نيو رومان 20. بولد"* — **20 bold**
- **[03:27]** chapter title: *"شابتر 1 انت كتبتوها ب 18 بولد"* — **18 bold**
- **[04:06]** side headings: *"16 تايمز نيو رومان 16 بولد"* — **16 bold**;
  body: *"البودي بتاع المحتوى ب 12"* — **12**

Current, measured:

| Element | Spec | Actual | Source |
|---|---|---|---|
| Chapter title | 18 bold | `\huge` ≈ **24.9 pt** | `1-main.tex:49` |
| Section | 16 bold | `\Large` ≈ **17.3 pt** | `report.cls` default |
| Subsection | — | `\large` ≈ 14.4 pt | default |
| Body | 12 | **12** ✅ | `\documentclass[12pt]` |
| Cover project name | 20 bold | **not yet audited** | — |

Marks context: the write-up is **10 of 60**; `2026-07_supervisor_voice_notes_key_points.md:97`
records that presentation faults *"can cost 5–6 of those 10"*.

### Change
1. `1-main.tex:49` — replace `\normalfont\huge\bfseries\centering` with
   `\normalfont\fontsize{18}{22}\selectfont\bfseries\centering`.
2. Add a `\titleformat{\section}` at `\fontsize{16}{19}\selectfont\bfseries`.
3. Audit the title page against **20 bold** and fix if needed.
4. Leave `\subsection` and `\subsubsection` alone — she did not specify them, and
   14.4 / 12 already sit correctly between 16 and body.

### Why
Explicit, repeated supervisor instruction, and it carries marks. Chapter titles are
currently ~38% larger than asked.

### Page impact
**−1 to −2 pages.** Every chapter title loses ~7 pt of height and every `\section`
~1.3 pt, across 5 chapters and ~40 sections. **This is where C5's +1 page comes from.**

### After (review + verify)
- ⚠️ **Re-flows every page again.** Do this *before* J3 and C5, not after.
- Confirm the chapter heading still fits on one line at 18 pt (the longest is
  "Theoretical Background and Literature Review").
- Re-measure the core page count; update the flags in `SESSION_HANDOFF.md`.
- ⚠️ The title page is `1-main.tex`'s `titlepage` environment, which may set its own
  sizes — check before assuming point 3 is needed.

---

## 9. C10 — Chapter 3 has no summary

### Evidence
From `C10_chapter_summaries_audit.md`:

| Chapter | Summary | Verdict |
|---|---|---|
| 1 | none | **correct** — §1.3 does the job, and Dr. Tahani put it there |
| 2 | `\section{Chapter Summary}` `chapter2.tex:491` | ✅ |
| 3 | **none** | ❌ **the gap** |
| 4 | `\section{Summary of All Experiments}` `chapter4.tex:945` | ✅ (retitle — J9a) |
| 5 | none | **correct** — §5.1 *is* the summary; `chapter5.tex:5` says so |

Ch.3 currently **ends mid-list** — its last content is the Type A/B/C `itemize` of the
regression classification. The ToC reads
`2.6 Chapter Summary / 3.9 Per-Query Error Analysis / 4.11 Summary of All Experiments`,
so the gap is visible without opening the thesis.

Decision to keep summaries is already made (Dr. Tahani Q1: optional, keeping them is
*"ممتاز"*). This task is only *verify presence and consistency*.

### Change
Add `\section{Chapter Summary}` + `\label{sec:ch3_summary}` at the end of `chapter3.tex`.

⚠️ **DECISION 5 — form and length.**
- **(i) Continuous prose, ≤150 words.** Denser; the audit measured printed p.61 as ~70%
  blank, so ≤150 words costs **0 pages**.
- **(ii) Match Ch.2's style** — intro sentence + `itemize` of key points. Ch.2's is
  **377 words** with 10 bullets; the same here costs **+1 page**.
- **Recommendation: (i).** The page budget has zero margin, and a methodology chapter
  summarises naturally as prose. Note honestly that this makes Ch.3's summary a
  different genre from Ch.2's — which the audit already flags as an existing
  inconsistency between Ch.2 and Ch.4 anyway.

Content: one sentence each for the baseline setup, the error-analysis method, the
Query2Doc adaptation, the model-comparison protocol, repetition + fusion + CSQE, and
the per-query analysis. **No new numbers** — a methodology summary states what was
done, not what was found.

### Why
Two of five chapters having summaries, with the gap in the middle chapter, is the kind
of asymmetry a committee notices from the ToC alone.

### Page impact
**+0.3 page** at ≤150 words; the audit's measurement says it lands in existing whitespace,
so realistically **+0**.

### After (review + verify)
- Confirm it did not push Ch.4 onto a new page.
- ⚠️ Re-check after **J2**, since heading resizing changes where p.61's whitespace is.
- ⚠️ Do **not** expand §4.11 to match Ch.2 — the audit's explicit recommendation;
  it fails the revert test and costs +1 page.

---

## 10. C5 — Promote bold headings in §2.1.4 and §2.1.5

### Evidence
Full detail in `C5_bold_headings_audit.md`. Supervisor directive: Report §7, video 2
06:10–07:20 — §2.1.4 → 2.1.4.1…, §2.1.5 → 2.1.5.1…, and audit for others.

Two settings, **measured not assumed**:
- `secnumdepth` = **3** (`1-main.tex:21`) → `2.1.4.1` **will be numbered**.
- `tocdepth` = **2** (never set; `report.cls` default) → subsubsections are written to
  `1-main.toc` but **suppressed at render**. **Promotion adds zero ToC lines.**
- **20 numbered depth-4 headings already exist** in Ch.2 (2.1.3.1, 2.2.4.2, 2.4.3.1 …),
  so this *fixes* an intra-chapter inconsistency rather than introducing a style.

### Change
Promote 8 bold leads to `\subsubsection`, titles verbatim:

| New | Title | Source |
|---|---|---|
| 2.1.4.1 | Query Expansion | `chapter2.tex:86` |
| 2.1.4.2 | Query Decomposition | `:94` |
| 2.1.4.3 | Query Disambiguation | `:96` |
| 2.1.4.4 | Query Abstraction | `:98` |
| 2.1.5.1 | Morphological Richness | `:117` |
| 2.1.5.2 | Diglossia | `:119` |
| 2.1.5.3 | Orthographic Variations | `:121` |
| 2.1.5.4 | Diacritical Marks | `:123` |

**§2.1.5 is a pure markup edit** — its leads already end with a period inside the braces
(`\textbf{Diglossia.} Arabic exhibits…`), so deleting the bold leaves a complete sentence.

⚠️ **DECISION 6 — §2.1.4 needs four sentence repairs.** Its leads are the grammatical
*subject*: `\textbf{Query Expansion} broadens the scope…`. Pulling the label into a
heading leaves `broadens the scope…`, a fragment. Each needs its subject restored
("Query expansion broadens the scope…"). This is a **forced consequence** of the
structural change, not enrichment — but it is prose, so it needs your sign-off.

⚠️ **DECISION 7 — orphaned closing paragraphs.** `chapter2.tex:100`, `:102` and Table 2.1
belong to §2.1.4 *as a whole*, and `:125` to §2.1.5 as a whole. After promotion they fall
under the **last** subsubsection.
- **(i) Accept.** Mild misattribution, common in published theses. Zero cost.
- **(ii) Move them above the first subsubsection.** Not viable — `:100` opens
  *"Among these four families…"*, so it cannot precede them.
- **(iii) Add a fifth subsubsection to hold them.** Costs a heading and requires
  inventing a title.
- **Recommendation: (i).**

### Why
Direct supervisor directive, still unfulfilled.

### Page impact
8 headings × 46.3 pt = 370 pt = **+0.53 page → budget +1.**

### After (review + verify)
- ⚠️ `\label{sec:qe_techniques}` (`:82`) and `\label{sec:arabic_challenges}` (`:113`) sit
  directly under their `\subsection`. **Insert the new `\subsubsection`s *after* those
  labels** or the labels rebind to the subsubsection and 3 cross-references break
  (`chapter2.tex:500,501`, `chapter3.tex:169`).
- Confirm the ToC is unchanged (proves `tocdepth` behaved as measured).
- Confirm 0 undefined references.
- ⚠️ **Do NOT extend this to §5.1.** It is the largest bold run in the thesis (12 leads,
  5 pages) and the audit's strongest "do not do this" — its leads are full sentences,
  not titles, and it would cost 0.88 page plus 12 ToC lines.
- ⚠️ **Do NOT raise `tocdepth`** — it would expose all 20 existing subsubsections plus
  17 `\paragraph`s at once, ~30 new ToC lines.

---

## 11. J8 — 17 `\paragraph{}` headings render unnumbered and invisible in the ToC

### Evidence
`chapter3.tex` §3.6 (4), §3.7 (3), §3.8.1 (2), §3.9 (4); `chapter4.tex` §4.10.4 (3);
`chapter2.tex:378` (1). With `secnumdepth=3` a `\paragraph` gets **no number**, and with
`tocdepth=2` **no ToC line** — visually identical to the bold pseudo-headings the
supervisor objected to in §2.1.4/§2.1.5.

### Change
⚠️ **DECISION 8 — this one is genuinely a question for Dr. Tahani, not for us.**
- **(i) Ask her at the next meeting** whether her §2.1.4/§2.1.5 objection extends to Ch.3.
  Zero cost now; keeps the option open.
- **(ii) Promote §3.6, §3.7, §3.9 to `\subsection`** (audit runs R4, R5, R7). Costs
  **+0.7 page** and adds ~11 ToC lines. §3.6 and §3.9 are the strongest candidates —
  each is a 2–3 page section with *no* subsections at all, unlike §3.1–§3.5.
- **(iii) Leave.**
- **Recommendation: (i).** We have no directive covering Ch.3, the page budget is at
  zero, and guessing wrong costs a page either way. Add it to **G1**'s meeting agenda.

### Why
Not currently false or self-contradicting — so by our own revert test this is *not* an
edit we should make unprompted. It is a question to ask.

### Page impact
0 if deferred; +0.7 if done.

### After (review + verify)
- Record the answer in the task file whichever way it goes.

---

## 12. What changes globally, and what must be re-reviewed afterwards

**Flag these when the batch is done:**

1. **Page count will move at least three times** (J2, J3, C5). Only the *final* number
   is meaningful. Update `SESSION_HANDOFF.md` §0 and supersede J1's "exactly 100" once.
2. **E2 and E3 are downstream of all of this.** E3 (dead labels, table audit) must run
   **last**, once. Running it earlier wastes it.
3. **Table 2.1 must be regenerated, not hand-edited** — otherwise the next figure
   regeneration silently reverts J3.
4. **The `nDCG`/`NDCG` sweep (C3 leftover) is still open** and J9(b) touches one instance
   of it. Decide sweep-or-defer before applying J9(b).
5. **Ch.3's summary will be a different genre from Ch.2's** (prose vs bullets). That is a
   deliberate, budget-driven choice — record it so a later reviewer does not "fix" it.
6. **§1.3 stops being a promotion candidate** once C4 merges it. The C5 audit already
   marks it "never" for this reason; C4 makes that permanent.
7. **Nothing here touches a number.** No metric, table value, or claim changes in any of
   these ten tasks except J6, which only removes the word "two". If a rebuild changes a
   reported figure, something went wrong.

---

## 13. Decisions needed before execution

| # | Task | Question | My recommendation |
|---|---|---|---|
| 1 | J3 | Table 2.1 `cite_key` column: drop, or render as `[12]`? | **Render as `[12]`** |
| 2 | C4 | Merge only, or merge and condense? | **Merge only** |
| 3 | J7 | Demote, promote, or leave each singleton? | **Demote Term Dilution; leave ALLaM** |
| 4 | J6 | Add a Type C paragraph, or just reword "two failure modes"? | **Reword** |
| 5 | C10 | Ch.3 summary: prose ≤150 words, or Ch.2-style bullets? | **Prose ≤150** |
| 6 | C5 | OK to repair the four §2.1.4 sentence openings? | **Yes — forced by the change** |
| 7 | C5 | Orphan closers: accept, or add a fifth subsubsection? | **Accept** |
| 8 | J8 | Ask Dr. Tahani, or decide ourselves? | **Ask her; add to G1** |
