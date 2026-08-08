# E3 — Figures & Tables Review (report only, nothing edited)

**Date:** 2026-08-08 · **Owner:** Elhaj · **Status:** review complete, awaiting approval before any edit.

**What was checked:** every figure and table in the thesis — captions, cross-references,
labels, overflow, and whether the plotted data still matches the tables.

**What was measured, and how.** Overflow was measured by rendering all 135 pages of the
committed `1-main.pdf` at 150 dpi and finding ink outside the A4 text block
(x = 72.27–523.01 pt, from the PDF's own MediaBox). This catches prose, table rules and
figures in one pass. Earlier audits (J3, J3b) read the build log or measured `booktabs`
rules only, which is why the largest defect in this report was missed by both.

---

## 0. First — you are reading the wrong PDF

The captions you quoted come from **`f:\Desktop\graduation\1-main.pdf`** (untracked, built
2026-08-08 01:30). That build is stale. It still contains four figures that no longer exist
in the source, including the "Figure 4.6: Grouped per-model bars" you quoted.

The current build is **`University_of_Khartoum__EEE_bachelor_s_thesis_template\1-main.pdf`**
(2026-08-08 13:05, 135 pages). The figures were renumbered between the two:

| You quoted | In the current build |
|---|---|
| Figure 4.5 "Dense retrieval NDCG@10 for all evaluated LLMs" | **Figure 4.3**, and the wording changed to "for the nine retained LLMs" |
| Figure 4.6 "Grouped per-model bars…" | **deleted** — no longer in the thesis |
| Figure 4.8 "NDCG@10 on the BM25 retriever…" | **Figure 4.5** |

Your complaint is still valid — the cross-references survive in the current build, just under
different numbers. But the root `1-main.pdf` should be deleted so nobody reviews from it again.

---

## 1. THE BIG ONE — 93 of 135 pages have text past the right margin

This is not a table problem. It is body prose, and it is the most serious defect found.

| | Committed build |
|---|---|
| Pages with ink past the right margin | **93 of 135** |
| Overflowing lines | **313** |
| Worst overflow | **72.0 pt** (1 inch past the margin) |
| Pages where text runs off the paper edge and is cut off | **3** — physical pages 19, 109, 127 (printed **1**, **91**, **109**) |
| `Overfull \hbox` warnings in the log | 291 |

Printed page 1 — the first page of Chapter 1, the first page an examiner reads — has six
overflowing lines. "Retrieval-Augmented" and "Query2Doc" both run off the edge of the paper
and are physically cut in half.

### Root cause (proven)

`1-main.tex:18`

```latex
\usepackage[none]{hyphenat}
```

The `none` option **disables hyphenation for the whole document**. Combined with
`\justifying` on line 20, TeX cannot break a long word at the end of a line, so it pushes the
word past the margin instead. Every one of the 313 overflowing lines ends in a long
unbreakable word.

### The fix is free — proven by a control build

A full `xelatex` ×2 build was run in a scratch copy with only that one line changed
(`[none]` removed). Nothing else was touched.

| | Current | Hyphenation restored |
|---|---|---|
| Pages with overflow | 93 | **31** |
| Overflowing lines | 313 | **42** |
| Worst overflow | 72.0 pt | **30.7 pt** |
| Pages cut off at the paper edge | 3 | **0** |
| `Overfull \hbox` | 291 | **40** |
| Total pages | 135 | 136 |

**The extra page does not touch the page budget.** Chapter start pages are byte-identical in
both builds — Ch.1 p.1, Ch.2 p.6, Ch.3 p.30, Ch.4 p.54, Ch.5 p.88, Bibliography p.97. Front
matter is identical. The one extra page lands inside **Appendix B** (Appendix C moves
113 → 114), and appendix pages do not count toward the 100-page limit.

> **Side finding, worth checking separately:** this build puts core Ch.1–5 at **96 pages**
> (p.1 → Bibliography p.97), not the **101** that task J11 still records. J11's "1 over the
> limit, appendix moves are the only lever" premise looks out of date by 5 pages. Worth
> re-reading J11 before spending effort on D2's appendix moves.

The remaining 31 pages / 42 lines after the fix are ordinary tight lines, all inside the
margin's own slack and none reaching the paper edge. Those can be left, or mopped up
individually later.

### Why previous audits missed it

J3 counted `Overfull \hbox` lines in the log and kept only the ones that were tables. J3b
measured `booktabs` rule widths in the PDF. Neither method looks at prose lines, and the log
warnings for prose were filtered out as noise. The defect has been present since `[none]`
was added.

---

## 2. Tables and figures — no overflow. J3b's work holds.

Independently re-verified on the committed PDF, by a different method than J3b used:

- **No table rule and no figure box exceeds the text block anywhere in the thesis.**
- Checked specifically on the four pages J3b fixed (physical 37, 89, 121, 128): on each one,
  the overflowing rows sit **outside** the table's rule band — above it on p.121, below it on
  p.37 and p.89, and p.128 has no overflow at all. The overflow on those pages is the prose
  around the table, not the table.
- All 20 figures are included at `width=0.85\textwidth` or `0.95\textwidth`, so they cannot
  overflow horizontally by construction.
- Caption placement is correct throughout: **all 32 tables** caption-above, **all 20 figures**
  caption-below.

---

## 3. Your actual question — cross-references inside captions

There are **five** captions containing a cross-reference. They are not all the same thing.

### 3a. The two you spotted — these are the real problem

| Where | Caption text | Renders as |
|---|---|---|
| `chapter4.tex:268` — **Fig 4.3** | "…each model uses its consistent thesis colour, matching Figure~\ref{fig:repetition_sweep}." | "matching Figure 4.5" |
| `chapter4.tex:468` — **Fig 4.5** | "Colours match Figure~\ref{fig:dense_bar_chart}." | "Colours match Figure 4.3" |

You read this right. Three things are wrong with them:

1. **They are circular.** 4.3 points at 4.5, 4.5 points back at 4.3. A reader following either
   one is sent in a loop and learns nothing.
2. **They describe a production decision, not the data.** "its consistent thesis colour" and
   "Colours match…" are the author explaining how the document was made. A caption describes
   what the reader is looking at. Nobody needs to be told the palette was reused — they can
   see it, and if they can't, the sentence doesn't help.
3. **The same species of sentence appears once more in Fig 4.3:** "the dropped ALLaM-7B is
   omitted **so that it does not compress the scale**." That is also a plotting decision. The
   fact that ALLaM is excluded belongs in the caption; the reason it was excluded belongs in
   the body (and is already there, in §4.4).

For the record, the claim itself is **true** — both figures were rendered and the per-model
colours do match (Aya teal, Jais purple, Qwen3-8B green, Gemma gold, SILMA tan, and so on).
This is a style problem, not a factual one.

> ⚠️ **Dependency — do not delete these blindly.** `fig:dense_bar_chart` (Figure 4.3) is
> referenced **exactly once in the entire thesis: inside Figure 4.5's caption.** Remove that
> line and Figure 4.3 becomes an orphan that no prose ever points to. Figure 4.3 needs a
> sentence in the body of §4.4 introducing it *before* or *at the same time as* the caption
> is cleaned up.

### 3b. The other three — these are fine, leave them

| Where | Renders as | Verdict |
|---|---|---|
| `chapter4.tex:16` — Table 4.1 | "(detailed in Section 4.6)" | **Keep.** Points at where a number in the table is explained. |
| `chapter4.tex:488` — Table 4.13 | "the full nine-point α-sweep is given in Appendix B" | **Keep the pointer** (see 4c below for a separate problem with this caption). |
| `chapter4.tex:729` — Table 4.21 | "differs slightly from the corpus-level headline of 0.7137 reported in Table B.3" | **Keep.** This one is load-bearing — it stops an examiner thinking 0.6936 and 0.7137 are a contradiction. |

The distinction: a caption may tell the reader **where fuller data lives**. It should not tell
the reader **how the author built the document**.

---

## 4. Other caption problems found

### 4a. No table has a short caption — the List of Tables is a mess

All **20 figures** use `\caption[Short version]{Full version}`, so the List of Figures reads
cleanly. **All 32 tables** use a bare `\caption{}`, so the **List of Tables prints every
caption in full**, including its cross-references and its maths.

Worst offenders on the LoT page (xiii):

- **Table 4.21** — 57 words, three sentences, includes "…reported in Table B.3, which is
  produced by the official pooled evaluation."
- **Table B.1** — 54 words, and prints the full repetition formula
  `n = max(1, ⌊|d|/(|q|·β)⌋)` into the List of Tables.
- **Table 3.2** — 42 words, prints `\texttt{max\_new\_tokens}` and `top_p` values.
- **Table 4.1** — 37 words, and prints "(detailed in Section 4.6)".

This is visible on a single page of the front matter and is exactly the kind of presentation
defect Dr. Tahani's voice note 8 penalises. Fix = add a short caption to all 32 tables. No
prose risk, no page movement, purely additive.

### 4b. Captions that argue instead of describe

Not wrong, but worth a decision — a caption should describe the exhibit; the argument belongs
in the body, where it already is.

| Figure | Phrase | Comment |
|---|---|---|
| 4.2 | "Short queries clearly underperform, **motivating QE as a remedy for information poverty in short queries**." | Argues the thesis's case inside a caption. Also says "short queries" twice in one sentence. |
| 4.10 | "…**demonstrates** first-pass quality as the largest behavioural modulator of CSQE." | "Demonstrates" is too strong for a caption. The section heading already makes this claim. |
| 4.4 | "A weak positive trend is visible… **corroborates** the size-quality correlation" | Same species, milder. |
| 4.1, 4.5, 4.6, 4.7, 4.11 | one-clause readings of the plot | Mild and common in theses. **My call: leave these.** |

**My recommendation:** fix 4.2 and 4.10 only. Leave the rest — trimming every interpretive
clause would be a big edit for a small gain.

### 4c. Table 4.13's caption repeats the sentence directly above it

`chapter4.tex:484` (prose) — "Table 4.13 reports the baselines, the best convex-combination
setting and both RRF settings; the complete nine-point sweep is given in Appendix B."

`chapter4.tex:488` (caption) — "The best convex-combination setting and both RRF settings are
shown; the full nine-point α-sweep is given in Appendix B."

The two sit two lines apart on the page and say the same thing twice. Trim the caption.

### 4d. A factual error in a caption

`chapter3.tex:99` — **Figure 3.3** caption: "stopword-removed using **245** Arabic stopwords".

- The body of the thesis (`chapter3.tex:89`) says "**245+** words" — so the caption drops the
  hedge and asserts an exact number the body itself won't commit to.
- The NLTK Arabic stopword list actually has **754** entries (verified locally:
  `len(nltk.corpus.stopwords.words('arabic'))` → 754).
- The H1 reproduction run, which matched the stored BM25 baseline to 13 decimal places, used
  that 754-word list (recorded in `THESIS_FINAL_SUBMISSION_TASKS.md:87`).

So 245 appears to be simply wrong, in both the caption and the body. **Needs a decision from
Osman before changing** — he built the index, and it is possible an older run used a
different list. But the caption and the body must at least agree.

### 4e. Short captions spell out symbols the full captions use

- Fig 4.9 short caption: "Per-query **Delta** NDCG@10 histogram" — full caption uses `$\Delta$`.
- Fig 4.7 short caption: "Hybrid CC **alpha** sweep, all metrics" — full caption uses `$\alpha$`.
- Fig 4.5 short caption: "…across **9** models" — full caption says "nine".

Cosmetic, but the List of Figures is where an examiner sees these side by side.

---

## 5. Dead labels and orphan figures (this is the original E3 scope)

| Label | Is | Problem |
|---|---|---|
| `fig:dense_vs_bm25_gains` | **Figure 4.6** | **Never referenced anywhere.** No prose introduces it. It sits immediately after Figure 4.5 with nothing between them, then §4.6 starts. |
| `fig:csqe_scatter` | **Figure 4.9** | **Never referenced anywhere.** |
| `fig:dense_bar_chart` | **Figure 4.3** | Referenced **only** from Figure 4.5's caption (see §3a). |
| `tab:q2d_params` | **Table 3.1** | **Never referenced.** |
| `lst:systems`, `lst:oneshot`, `lst:builders`, `lst:assembly`, `lst:config` | Appendix C listings | Never referenced. Harmless — there is no List of Listings — but dead. |

Three figures and one table that the reader is never told to look at. Fix = one sentence each
in the body. Cheap, and it closes the original 4.16 task.

Also: `fig:csqe_scatter` is **named** "scatter" but the exhibit is a **histogram** (short
caption: "Per-query Delta NDCG@10 histogram"; file: `fig_4_12_delta_hist_v1.pdf`). Invisible
to the reader, but it will mislead whoever edits it next.

**Clean:** no hardcoded "Figure 4.3"/"Table 4.7" text anywhere — every reference uses `\ref`.
No `Fig.`/`Tab.` abbreviations. Capital F/T throughout. No undefined `\ref` or `\cite`.

---

## 6. Figure 4.5 still plots superseded data (carried over from H1)

`Figure 4.5` (`fig_4_7_repetition_v1.pdf`) was generated **2026-06-01** and reads
`thesis_figures/data/raw/exp11_ndcg10.csv` (confirmed by `data_manifest.yaml:124`,
`consumed_by: [fig_4_7, table_4_3]`). That CSV's **SILMA row is still the temperature-0.7
data**: n=1 = 0.4194, best = 0.4832 at n=5.

Task H1 re-ran SILMA at temperature 0.1 on 2026-08-08 and the thesis tables now print
**n=1 = 0.4277, best = 0.4786 at n=7**. The figure and the tables therefore disagree, and the
optimum marker is on the wrong point.

Also still stale:
- `thesis_figures/data/raw/model_comparison_bm25.csv:3` — pairs the corrected temp-0.1 n=1
  metrics with the **old** best config (`n=5`, 0.4832, Δ 0.0555). That Δ matches neither table.
- `thesis_figures/output/pdf/table_4_3.tex` — same feeder, same stale best config.

H1 flagged all of this and left it as Osman's. It is still open.

**Good news on the caption:** both of Figure 4.5's factual claims survive the correction —
"six of nine models start below the BM25 baseline at n=1" (SILMA is below at 0.4194 *and* at
0.4277) and "all nine recover or exceed it at their optimum n" (0.4786 > 0.4621). Only the
plotted curve needs regenerating, not the caption's wording.

> I tried to read SILMA's plotted n=1 value directly off the figure by pixel calibration to
> confirm which dataset it holds. **That was inconclusive** — the calibration error (±0.09)
> was far larger than the 0.008 difference between the two candidate values, and two of the
> nine model colours are too close to separate reliably. The file date and the feeder CSV are
> the evidence here, not the pixels.

---

## 7. Figure filenames carry obsolete numbers

Every Ch.4 figure file is named for a number it no longer has:

| Prints as | File |
|---|---|
| Figure 4.2 | `fig_4_3_length_box_v1.pdf` |
| Figure 4.3 | `fig_4_5_models_bar_v1.pdf` |
| Figure 4.4 | `fig_4_6_size_v2_labelled.pdf` |
| Figure 4.5 | `fig_4_7_repetition_v1.pdf` |
| Figure 4.6 | `fig_4_8_gains_v1.pdf` |
| Figure 4.7 | `fig_4_9_alpha_sweep_v2_all.pdf` |
| Figure 4.8 | `fig_4_11_progression_v2_annot.pdf` |
| Figure 4.9 | `fig_4_12_delta_hist_v1.pdf` |
| Figure 4.10 | `fig_4_13_firstpass_v2_annot.pdf` |
| Figure 4.11 | `fig_4_14_lengthgain_v2_grouped.pdf` |

Ch.3 has the same drift (Figure 3.2 = `fig_3_4_mdpr.pdf`, Figure 3.5 = `fig_3_7_hybrid.pdf`,
Figure 3.7 = `fig_3_9_best_system.pdf`).

Nothing renders wrong. But this is already causing real confusion — H1's handover note talks
about "Figs 4.7 and 4.8", meaning the **files**, which are Figures **4.5 and 4.6** in the
thesis. **Recommendation: do not rename the files** this close to submission (it touches
`data_manifest.yaml`, the regen scripts and the chapter). Instead add a mapping note to
`thesis_figures/README.md` so the next person doesn't get caught.

---

## Recommended order (nothing done yet — awaiting your approval)

| # | Item | Effort | Risk | Why this order |
|---|---|---|---|---|
| 1 | Remove `[none]` from `hyphenat`, rebuild | 1 line | none — control build proven page-neutral for Ch.1–5 | Biggest defect, smallest fix |
| 2 | Delete the stale root `1-main.pdf` | trivial | none | Stops reviews from the wrong file |
| 3 | Add short captions to all 32 tables | ~1h | none | Fixes the List of Tables page |
| 4 | Add prose references for Figs 4.3, 4.6, 4.9 and Table 3.1, **then** clean the two colour cross-references | ~1h | low | Must be done in this order — §3a |
| 5 | Trim Table 4.13's caption; soften Fig 4.2 and Fig 4.10 | 15 min | low | Quick wins |
| 6 | Resolve the 245 vs 754 stopword number with Osman | — | — | Needs his knowledge |
| 7 | Regenerate Figure 4.5 from corrected SILMA data (Osman, from H1) | — | — | Already open |
| 8 | Add the filename↔number map to `thesis_figures/README.md` | 10 min | none | Prevents the next mix-up |
