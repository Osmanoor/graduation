# Wave 2 Session Report — Planning Pass (B1, C4, C5, C10, Flags 2 & 6)

**Date:** 2026-08-01
**Session scope:** Elhaj's Wave 2 tasks plus unclosed Wave 1 items.
**Status:** **PLANNING ONLY. No `.tex` file was touched in this session.** Nothing is committed to the thesis.
**Awaiting:** answers to Q1–Q12 in §5 below.

---

## 1. What was done

1. Read `SESSION_HANDOFF.md`, `THESIS_FINAL_SUBMISSION_TASKS.md`,
   `SILMA_TEMPERATURE_RATIONALE_CHECK.md`, `CLAUDE.md`, `chapter1.tex`, `chapter5.tex`,
   and `5-Abstract.tex`.
2. Ran two read-only Opus evidence agents. Both wrote reports; neither touched a thesis file:
   - `research_decisions/C5_bold_headings_audit.md`
   - `research_decisions/C10_chapter_summaries_audit.md`
3. Drafted the B1 replacement abstract (§4) and verified every number in it against
   Ch.3/Ch.4/Ch.5 and `CLAUDE.md`.
4. Built the task-by-task plan in §3 with measured page deltas.

**Deliverables produced this session:** this report + the two audit reports. Nothing else.

---

## 2. Corrections to recorded project state

### 2.1 The page count in `TASKS.md` D1 is stale

D1 records **103 pages** (Ch.5 p.95, Bibliography p.104), measured 2026-07-29 — before the
A7 and A8 edits. Two independent clean rebuilds from current sources this session disagreed
with it *and with each other*:

| Source | Ch.5 starts | Bibliography starts | Core Ch.1–5 |
|---|---|---|---|
| D1 record (2026-07-29) | p.95 | p.104 | **103** |
| C5 agent rebuild | p.96 | p.105 | **104** |
| C10 agent rebuild | — | p.106 | **105** |

**Not reconciled.** I did not run a third build to adjudicate; I would rather do one clean
build under controlled conditions than pick between two agent numbers.

> **Working conclusion: the manuscript is 4–5 pages over the 100-page limit, not 3.**
> D1 needs re-running as its own step. D2/D5 must free one to two pages more than budgeted.

### 2.2 The committed `1-main.pdf` does not match the committed sources

`git log` shows `Chapters/chapter2.tex` and `1-main.pdf` last changed together in `14533f2`
("revert out-of-scope final-round changes"), but the committed PDF was built *before* that
commit's source reverts — it still renders the CSQE taxonomy bullet in §2.1.4 and the
"generate or select" wording, both of which `14533f2` removed.

> **Do not measure pages or check layout from the committed PDF.** It is off by ~1 page and
> shows reverted text.

### 2.3 Two document settings that change C5's cost (measured, not assumed)

| Setting | Value | Where | Consequence |
|---|---|---|---|
| `secnumdepth` | **3** | `1-main.tex:21` | `\subsubsection` **is numbered** → `2.1.4.1` renders correctly |
| `tocdepth` | **2** (default, never set) | no `\setcounter{tocdepth}` anywhere | `\subsubsection` is written to `1-main.toc` but **suppressed at render** |

Verified: `1-main.toc` contains 20 `\contentsline{subsubsection}` lines, but `pdftotext`
over the rendered Contents shows only chapter/section/subsection entries — `2.1.3
Information Retrieval Methods` appears, `2.1.3.1 Sparse Retrieval` does not.

> **Promoting to `\subsubsection` adds zero ToC lines.** And the ToC is front matter, so even
> a nonzero ToC impact would be free against the 100-page core.
>
> **Do NOT raise `tocdepth` as part of C5** — it would retroactively expose all 20 existing
> subsubsections plus 17 `\paragraph`s, ~30 ToC lines at once.

**20 numbered depth-4 headings already exist** (`chapter2.tex:60,67,76,193,205,226,288,297,
306,315,325,332,337,346,351,358,368,373`; `chapter4.tex:203,329`). C5's promotions match
established style and fix an intra-Ch.2 inconsistency — §2.1.3, §2.2.4, §2.4.1, §2.4.2 and
§2.4.3 all use numbered subsubsections while §2.1.4 and §2.1.5 alone use bold runs.

---

## 3. Plan — shape of the whole scope

| # | Task | What it actually is | Page delta | Blocked on |
|---|---|---|---|---|
| 1 | **B1** English abstract | Full rewrite. Front matter — **does not touch the 100-page core**. Real constraint is Dr. Tahani's 250–350 words. | 0 | Q1–Q4 |
| 2 | **C4** §1.3 → one paragraph | Near-pure markup: delete 4 `\textbf{Chapter~\ref{}}` wrappers, join paragraphs. Text already reads "Chapter 2 establishes…" without the bold. | **−36 pt (≈ −1.7 lines)** | Q5 |
| 3 | **C5** promote bold headings | §2.1.4 + §2.1.5 only (8 headings → `\subsubsection`). | **+0.53 page → budget +1** | Q6–Q8 |
| 4 | **C10** chapter summaries | Ch.3 summary missing; Table 4.28 overflows. | 0 if capped at 150 w | Q11 |
| 5 | **Flag 2** reinstate "small" | Objective 4 wording. | 0 | Q9 |
| 6 | **Flag 6** Aya licence caveat | Ch.5 "Overall" ¶ vs Challenges item 8. | 0 to −30 words | Q10 |
| — | **H1/H2/H3** | Osman's. No action taken or planned here. | — | Osman |

**Net if everything is done as scoped: roughly +1 page.** That lands the manuscript at ~105–106
against 100. D2/D5 has to absorb it. This is the honest picture, not a rounding-down.

### 3.1 C5 detail — recommended scope

From `C5_bold_headings_audit.md`. Nine runs of parallel bold pseudo-headings exist in the thesis.

| Do | Runs | Page cost |
|---|---|---|
| **Now (supervisor directive)** | R1 §2.1.4, R2 §2.1.5 | **+0.53 → budget +1** |
| Defer to post-D2/D5 | R3 §2.3, R4 §3.6, R7 §3.9 | +0.76 |
| Never | R0 §1.3 (C4 conflict), R5 §3.7, R6 §3.8.1, R8 §4.10.4, R9 §5.1 | — |

**The largest run in the thesis is §5.1 Conclusions — 12 sibling bold leads over 5 pages —
and it is the one to leave alone.** Anyone re-running the "audit for other sections" step will
land there first. Four reasons not to: 0.88 page cost; the "headings" are full sentences
(`5.1.8 Corpus-steered expansion validates the corpus grounding hypothesis` is a claim, not a
title); 12 subsections for a 5-page section is over-fragmentation; and `\subsection` is the only
free level there, so all 12 *would* enter the ToC.

**Proposed promotions (titles verbatim from current bold text, no rewording):**

| New number | Title | Source |
|---|---|---|
| 2.1.4.1 | Query Expansion | `chapter2.tex:86` |
| 2.1.4.2 | Query Decomposition | `chapter2.tex:94` |
| 2.1.4.3 | Query Disambiguation | `chapter2.tex:96` |
| 2.1.4.4 | Query Abstraction | `chapter2.tex:98` |
| 2.1.5.1 | Morphological Richness | `chapter2.tex:117` |
| 2.1.5.2 | Diglossia | `chapter2.tex:119` |
| 2.1.5.3 | Orthographic Variations | `chapter2.tex:121` |
| 2.1.5.4 | Diacritical Marks | `chapter2.tex:123` |

**§2.1.5 promotes with zero prose change** — the leads already carry a terminal period inside
the braces (`\textbf{Diglossia.} Arabic exhibits…`), so deleting the bold run leaves a complete
sentence. This is the one run in the thesis that is a pure markup edit.

**§2.1.4 does not.** All four leads are the grammatical *subject*
(`\textbf{Query Expansion} broadens the scope of a query…`), so promotion leaves four sentence
fragments. Each needs its subject restored ("Query expansion broadens the scope…"). That is a
forced consequence of the structural change, not a wording proposal — but it means R1 must be
reviewed for sense. See **Q7**.

**Cross-references: no breakage.** Every `\ref` touching these sections points at the *parent*
label, which stays attached to the parent `\subsection`. Verified that `\label{sec:qe_techniques}`
(`chapter2.tex:82`) and `\label{sec:arabic_challenges}` (`:113`) both sit on the line directly
after their `\subsection` and before any body text, so inserting `\subsubsection`s below them
rebinds nothing.

### 3.2 C10 detail

From `C10_chapter_summaries_audit.md`.

**Presence — 2 of 5 chapters:**

| Chapter | Summary | Verdict |
|---|---|---|
| Ch.1 | none | **correct** — §1.3 Thesis Layout already performs the closing-overview role, and Dr. Tahani's Q6 answer puts it there |
| Ch.2 | `\section{Chapter Summary}` `chapter2.tex:491`, last section | ✅ |
| Ch.3 | **none** | ❌ **the real defect** — no structural substitute, ends mid-taxonomy |
| Ch.4 | `\section{Summary of All Experiments}` `chapter4.tex:945`, last section | ✅ |
| Ch.5 | none | **correct** — §5.1 Conclusions *is* the summary; `chapter5.tex:5` already says so |

Adding a summary to Ch.1 or Ch.5 would be a summary of a summary. Not recommended.

**Style axes — consistent.** Sectioning level, placement, tense and voice all match. Label
schemes differ (`sec:chapter_summary` vs `sec:res_summary`) but each matches its own chapter's
convention — not a defect.

**One genuine divergence, deliberately NOT fixed:** Ch.2's summary is a 377-word
section-by-section recap with 10 cross-referenced bullets and a hand-off to Ch.3; Ch.4's is a
table plus 103 words covering only §4.6–4.10 with no preview of Ch.5. Expanding §4.11 to match
fails the revert test and costs +1 page. **Recommendation: leave it; take only the free part of
the alignment (retitle).**

**Numeric verification: zero defects.** All 17 rows of Table 4.28 match `CLAUDE.md` and the
chapter body; 54.5% and 13.9% both recompute; all 11 cross-references resolve. Both `CLAUDE.md`
traps avoided — §4.11 quotes only the corpus-level 0.7137 and never the 0.6936 per-query mean,
and neither summary mentions query-length buckets.

### 3.3 Escalation — five Ch.4 tables are printed with columns cut off

This is **not C10's**, and it is more serious than anything else found this session.

| Table | Overflow | Consequence |
|---|---|---|
| `tab:csqe_hybrid_configs` (`chapter4.tex:665–681`) | **168.5 pt too wide** | **The table carrying the thesis's central asymmetric-placement claim is printed missing a column.** |
| Table 4.28 (`chapter4.tex:955–983`) | 105.6 pt too wide | On printed p.96 the Status column reads "Baselin", "Degrade", "Best overa" |
| + three more Ch.4 tables | — | per `1-main.log` `Overfull \hbox` warnings |

Currently sheltering under **E3**, which is figure-gated — but these overflows are independent
of the figure work and need not wait. Fix is a `\resizebox{\textwidth}{!}{…}` wrapper per table:
page-neutral or page-negative, zero prose risk. See **Q12**.

---

## 4. B1 — the plan and the draft

### 4.1 What changes vs. the current abstract

- **`5-Abstract.tex:5` opening replaced.** "small open-source LLMs … and identifies the model
  characteristics that determine effectiveness" is the pre-A1 framing and directly contradicts
  **A2**, which de-scoped model-characteristics analysis. → replaced with the new RQ verbatim.
- **CSQE named and defined** — currently absent from the abstract entirely.
- **Asymmetric-placement finding stated**, using the like-for-like RRF column throughout
  (0.7137 sparse-only / 0.6936 both / 0.6474 dense-only). Ch.5 ¶10 calls this the principal
  contribution; the abstract never mentions it. Using one fusion method avoids the M10 trap of
  comparing an RRF result against a CC result.
- **DROPPED:** *"Model size was positively correlated with dense retrieval improvement, and
  training data diversity was found to be a more significant predictor of query expansion
  quality than Arabic-specific benchmark scores."*
  Two reasons: it is the de-scoped framing, **and it is stronger than Ch.5 now says.**
  `chapter5.tex:20` hedges it — "parameter count is confounded with architecture and training
  data; the cleanest evidence comes from the Qwen family, where size and dense NDCG@10 are
  strongly associated once architecture is held constant". Leaving the abstract's flat claim
  in place would be a self-contradiction, so removal passes the revert test.

### 4.2 Draft — 377 words (over the 350 ceiling; see Q1)

Paragraph word counts: 131 / 94 / 96 / 56.

> Retrieval-Augmented Generation (RAG) systems depend on effective retrieval to ground Large
> Language Model (LLM) outputs in external knowledge, yet Arabic information retrieval fails on
> a substantial proportion of queries because of morphological richness, orthographic variation,
> and vocabulary mismatch between short queries and documents. Query enhancement (QE)---the
> modification of a query before retrieval---offers a modular, retriever-agnostic remedy, but its
> established techniques were developed for English using proprietary models of 175 billion or
> more parameters, and neither their transfer to Arabic nor the retriever within a hybrid
> architecture that should receive an expanded query has been established. This thesis
> investigates the extent to which LLM-based QE---generated blindly or steered by the target
> corpus---can improve Arabic information retrieval across sparse, dense, and hybrid retrieval
> paradigms, using only openly available models of 2--8 billion parameters.
>
> Experiments used the Arabic subset of the Multilingual Information Retrieval Across a Continuum
> of Languages (MIRACL) benchmark, comprising 2,896 queries over 2.06 million passages, with the
> Multilingual Dense Passage Retriever (mDPR) and BM25S, an implementation of Best Matching 25
> (BM25), as the dense and sparse baselines. An error analysis identifying a 34\% query failure
> rate and the weakness of very short queries motivated adapting Query2Doc for Arabic zero-shot
> application. Ten openly available LLMs were compared as expansion generators, after which query
> repetition, hybrid sparse--dense fusion, and Corpus-Steered Query Expansion (CSQE) were
> evaluated in turn.
>
> QE improved dense retrieval for all nine viable models, with Normalised Discounted Cumulative
> Gain at rank 10 (NDCG@10) gains between +3.7\% and +23.5\%, but degraded sparse retrieval for
> six of the nine through dilution of the original query terms---a degradation fully removed by
> query repetition. Hybrid fusion without QE established a ceiling of 0.6267 NDCG@10. CSQE reached
> 0.6157 on BM25 alone, and its placement within the hybrid pipeline proved decisive: applied to
> the sparse retriever alone it achieved 0.7137 NDCG@10, against 0.6936 when both retrievers
> received the expansion and 0.6474 when only the dense retriever did.
>
> The final system therefore exceeded the BM25 baseline by 54.5\% and the strongest unenhanced
> hybrid baseline by 13.9\%, using an openly available 8-billion-parameter generator and without
> proprietary APIs. LLM-based QE is effective across all three retrieval paradigms, provided that
> both the form of the expansion and the retriever that receives it are adapted to the paradigm.

### 4.3 Number provenance

| Figure | Source | Check |
|---|---|---|
| 2,896 queries / 2.06 M passages | `chapter3.tex:17` (2,061,414 passages) | ✅ |
| 34\% failure rate | `chapter5.tex:14`, `CLAUDE.md` | ✅ |
| +3.7\% … +23.5\% dense range | `chapter5.tex:18` | ✅ |
| six of nine degraded on BM25 | `chapter5.tex:22` | ✅ |
| 0.6267 hybrid RRF ceiling | `CLAUDE.md` Exp 1.2 | ✅ |
| 0.6157 CSQE on BM25 | `CLAUDE.md` Exp 013 | ✅ |
| 0.7137 / 0.6936 / 0.6474 | `CLAUDE.md` Exp 2.1 — all three RRF, like-for-like | ✅ |
| +54.5\% over BM25 | 0.7137 / 0.4621 = 1.5445 | ✅ recomputed |
| +13.9\% over hybrid | 0.7137 / 0.6267 = 1.1388 | ✅ recomputed |

Current abstract for comparison: **369 words** (88 / 125 / 122 / 34).

---

## 5. Pending questions — Q1–Q12

Nothing will be edited until these are answered.

### B1

**Q1 — Length.** Draft is 377 words against Dr. Tahani's 250–350. Reach ~340 by cutting one of:
(a) the `+3.7%–+23.5%` model-comparison range; (b) the "0.6267 hybrid ceiling" sentence — but
then "+13.9% over the strongest unenhanced hybrid" loses its anchor; (c) tightening ¶1's problem
statement by ~25 words with no content loss.
**Recommendation: (c) only, land ~350.** Or accept 377, since it still fits well under one page?

**Q2 — Named models.** The current abstract names Aya Expanse 8B (+23.5% dense, +9.2% BM25) and
Jais-2 8B (+10.8% sparse). The draft drops both to save ~35 words and keeps only the range.
Objective 4 is "identify the most effective model under each paradigm". Acceptable to drop from
the abstract, or should the names go back in?

**Q3 — The "3B beats 175B GPT-3" claim.** Currently in the abstract, true, rhetorically strong.
The draft drops it for space. Keep or drop?

**Q4 — Acronym expansions.** C3 established that the abstract carries its own first mentions.
Full expansions of MIRACL + mDPR + BM25 cost ~25 words. mDPR's expansion could be dropped
entirely ("dense and sparse baselines") without violating C3 — the rule is *at most* once, not
*at least*. Take the ~15-word saving, or keep the abstract fully self-contained?

### C4

**Q5 — Scope.** §1.3 is 404 words across 4 paragraphs. Pure merge = one 413-word paragraph
(~19 lines, about 2/3 page — readable, not unwieldy), page-negative, essentially a markup edit.
Just the merge, or merge **and** condense? Condensing is outside the revert test but would help D5.

### C5

**Q6 — Timing.** §2.1.4 + §2.1.5 costs ~+1 page on a manuscript already 4–5 over. Do it now
(supervisor directive; D5 absorbs it later), or hold until after D5 frees pages?

**Q7 — Prose repair.** §2.1.5 promotes with zero prose change. §2.1.4 does not — all four leads
are the grammatical subject, so promotion leaves four fragments needing the subject restored
("Query expansion broadens the scope…"). Forced consequence, not enrichment. Confirm you are OK
with those four sentence-opening repairs?

**Q8 — Orphaned closers.** In both sections the closing paragraphs (`chapter2.tex:100,102` +
Table 2.1; `:125`) are section-level and would fall under the *last* subsubsection after
promotion. Options: (a) accept the mild misattribution — cheapest, common in published theses;
(b) add a fifth subsubsection to hold them — costs a heading and requires inventing a title.
**Recommendation: (a).**

### Phase A flags

**Q9 — Flag 2 ("small" in Objective 4).** **Recommendation: no.** The numeric range
("openly available LLMs spanning 2--8 billion parameters") already carries the scope, and
reinstating the word walks back the exact framing identified in video 2 as
*"أكبر غلط حالياً في التزيس"*. Nothing is false without it. Confirm?

**Q10 — Flag 6 (Aya licence).** Ch.5 ¶12 currently ends with a ~35-word licence clause naming
Aya CC-BY-NC and Jais-2-8B; Challenges item 8 (`chapter5.tex:60`) covers the same ground in full
with the 2.4%/2.1% numbers. **Recommendation: trim the "Overall" to
`…subject to the licence of the chosen generator (Section~\ref{sec:challenges}).`** —
page-negative, removes the duplication, keeps the caveat. Or keep both as-is?

### C10

**Q11 — Ch.3 summary.** This is the one place C10 forces an *addition*, against the page
constraint. The C10 agent's claim is that printed p.61 is ~70% blank, so ≤150 words costs 0 pages
(Ch.2's 377-word style would cost +1). Write it at ≤150 words, or leave Ch.3 without a summary
and record the asymmetry as a deliberate choice?

**Q12 — Table overflows.** (a) Log all five as a new task and leave them; (b) fix only
`tab:csqe_hybrid_configs` and Table 4.28 now, since they print wrong claims; (c) fix all five now.
They are `\resizebox` one-liners, page-neutral or page-negative.
**Recommendation: (c)** — a table printed with a missing column reads as carelessness to a
committee, and the fix carries no prose risk.

---

## 6. Candidate new task-list entries

Per the working rule *"no thesis edit without a task-list entry"*, these were found this session
and were **not** fixed. They need entries in `THESIS_FINAL_SUBMISSION_TASKS.md` before anyone
touches them.

| # | Item | Severity | Cost |
|---|---|---|---|
| N1 | **D1 page count is stale** — 103 recorded; rebuilds give 104 and 105. Needs one controlled re-run. | HIGH — drives D2/D5 sizing | S |
| N2 | **Committed `1-main.pdf` does not match committed sources** (built before `14533f2`'s reverts). Rebuild-and-commit, or drop the PDF from version control. | MEDIUM — misleads anyone measuring | S |
| N3 | **Five Ch.4 tables overflow the text block**, printed with columns cut off — incl. `tab:csqe_hybrid_configs` (168.5 pt), which carries the central placement claim. Currently sheltering under E3's figure gate; independent of the figure work. | **HIGH — the thesis prints an incomplete central result** | S |
| N4 | **§4.10.4 documents Type A and Type B but not Type C**, while Table 4.25 reports Type C as 45 queries / 12%. Content gap. | MEDIUM | S |
| N5 | **`Chapters/chapter2_generated.tex` is dead weight** — not `\include`d by `1-main.tex`, contains an old draft of §2.1.4/§2.1.5 with 20+ bold pseudo-headings, pollutes every grep. | LOW | S |
| N6 | **Two singleton `\subsubsection`s** — `chapter4.tex:203` (4.3.2.1, only child of §4.3.2) and `:329` (4.4.3.1, only child of §4.4.3). A 1-of-1 numbered subdivision is a style smell. | LOW | S |
| N7 | **17 `\paragraph{}` headings in Ch.2–4 render unnumbered and invisible in the ToC** — the same visual defect the supervisor objected to for §2.1.4/§2.1.5. Worth pre-empting before she raises it. (Runs R4 §3.6, R5 §3.7, R7 §3.9, R8 §4.10.4.) | MEDIUM | M |
| N8 | **Consistency micro-fixes** found by the C10 audit: retitle §4.11 "Summary of All Experiments" → "Chapter Summary"; `nDCG`→`NDCG` at `chapter4.tex:985`; `summarized`→`summarised` at `chapter2.tex:495`. | LOW | S |

Also still open from the previous handoff and unchanged by this session: the `nDCG` vs `NDCG`
casing sweep (81 × `NDCG@10` vs 46 × `nDCG@10` thesis-wide), and the deferred M12 terminology
sweep.

---

## 7. Not touched this session

- **H1 / H2 / H3** — Osman's, per Elhaj's instruction. H1's Option A (re-run SILMA at temp 0.1)
  vs Option B (footnote) still blocks Tables 4.11/4.12 and Figs 4.7/4.8.
- **B2** (Arabic abstract) — Osman's, and gated on B1.
- Every other Phase D / E / F / G task.

---

## 8. Next move once Q1–Q12 are answered

1. Finalise B1, show the diff, apply to `5-Abstract.tex`.
2. C4 (single-paragraph merge) — smallest and lowest-risk; diff shown before applying.
3. C5 R1 + R2 — markup for §2.1.5 first (zero prose change), then §2.1.4 with the four
   subject repairs.
4. C10 — per the Q11 decision.
5. Flags 2 and 6 — per Q9 / Q10.
6. Add N1–N8 to `THESIS_FINAL_SUBMISSION_TASKS.md`.

One task at a time, diff shown before each.
