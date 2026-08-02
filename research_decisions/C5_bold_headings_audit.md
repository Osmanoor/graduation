# C5 — Bold Pseudo-Heading Audit (Ch. 1–5)

**Date:** 2026-07-31 · **Task:** C5 (`research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md:142`) · **Status:** analysis only, no thesis file touched
**Scope:** structural only. No prose rewording is proposed except where a promotion makes a sentence ungrammatical — those cases are flagged explicitly, not authored.

---

## 0. Executive summary

| Question | Answer |
|---|---|
| Does the thesis already use numbered depth-4 headings? | **Yes.** 20 existing `\subsubsection`s render as e.g. `2.1.3.1 Sparse Retrieval`. |
| Will `2.1.4.1` be *numbered*? | **Yes** — `\setcounter{secnumdepth}{3}` at `1-main.tex:21`. |
| Will `2.1.4.1` appear in the **ToC**? | **No.** `tocdepth` is never set, so `report.cls`'s default of **2** applies. Subsubsections are written to `1-main.toc` but suppressed at render time. **Promoting to `\subsubsection` costs ZERO ToC lines.** |
| Will it get a PDF bookmark? | **No.** `bookmarksdepth=2` (`1-main.tex:82`). |
| Page cost of C5 as literally scoped (§2.1.4 + §2.1.5) | **≈ 0.53 page** (8 headings × 46.3 pt against a ~700 pt text block). Realistically **+0 or +1 page** after pagination knock-on. |
| Page cost if the audit is applied to *every* run found | **≈ 2.7 pages → +3 pages in practice.** The manuscript is already 4 over. |
| Recommendation | **Do §2.1.4 and §2.1.5 (the supervisor's explicit ask). Do NOT extend to the other seven runs** — the three biggest ones are already real sectioning commands or conflict with other tasks. Detail in §5. |

**Headline warning:** the single largest bold-pseudo-heading run in the thesis is **not** §2.1.4 or §2.1.5 — it is **§5.1 Conclusions, with 12 sibling bold leads** across 5 pages. It is also the run that should *least* be promoted (see R9).

---

## 1. Document settings — measured, not assumed

| Setting | Value | Where | Consequence |
|---|---|---|---|
| `secnumdepth` | **3** | `1-main.tex:21` (overrides `report.cls:262`, which is 2) | `\subsubsection` **is numbered** → `2.1.4.1`. `\paragraph` (level 4) is **not** numbered. |
| `tocdepth` | **2** (default, never overridden) | `report.cls:582`; no `\setcounter{tocdepth}` anywhere in `1-main.tex` or `Chapters/*.tex` | `\subsubsection` and `\paragraph` are **absent from the rendered ToC**. |
| `bookmarksdepth` | **2** | `1-main.tex:82` | No PDF bookmark for subsubsections. |
| `titlesec` | loaded, `\titleformat`/`\titlespacing*` applied to `\chapter` and `\section` **only** | `1-main.tex:39–46` | `\subsection` / `\subsubsection` / `\paragraph` keep `report.cls` spacing verbatim. |

**Verification of the tocdepth finding.** `1-main.toc` contains 20 `\contentsline{subsubsection}` lines and 17 `\contentsline{paragraph}` lines, but `pdftotext` over the rendered Contents pages (PDF pp. 9–13) shows **only** chapter/section/subsection entries — e.g. `2.1.3 Information Retrieval Methods` appears, `2.1.3.1 Sparse Retrieval` does not. `\addcontentsline` always writes; `\@dottedtocline` filters on `tocdepth` at read-back. This is the single most important fact for C5's cost:

> **Promotion to `\subsubsection` adds no ToC lines at all.** And even if `tocdepth` were raised, the ToC is front matter and **does not count toward the 100-page core limit**.

**Existing depth-4 style to match** (all 20 render identically — flush-left, bold, `\normalsize`, own line, numbered):
`chapter2.tex:60,67,76` (2.1.3.1–3) · `:193,205,226` (2.2.4.1–3) · `:288,297,306,315` (2.4.1.1–4) · `:325,332,337,346,351,358` (2.4.2.1–6) · `:368,373` (2.4.3.1–2) · `chapter4.tex:203` (4.3.2.1) · `:329` (4.4.3.1).

---

## 2. Page-budget baseline (re-measured)

`TASKS.md` D1 records **103 pages** as of 2026-07-29. That number is stale in both directions, so I rebuilt from the current sources in an isolated scratch copy (no repo file written, no repo artefact overwritten):

| Source | Ch.1 | Ch.2 | Ch.3 | Ch.4 | Ch.5 | Bibliography | **Core Ch.1–5** |
|---|---|---|---|---|---|---|---|
| D1 record (2026-07-29) | 1 | 7 | 36 | 60 | 95 | 104 | **103** |
| Committed `1-main.pdf` (**stale**, see §6d) | 1 | 7 | 36 | 61 | 97 | 106 | 105 |
| **Clean rebuild of current sources** | 1 | 7 | 36 | 61 | **96** | **105** | **104** |

> **Working number: Ch.1–5 = 104 pages. 4 over the 100-page limit.**

Text block ≈ **700 pt** (A4 297 mm − 2 × 1 in). `\parskip = 1em = 12 pt` (`1-main.tex:22`); `\setstretch{1.5}` (`:18`) → `\normalsize` line ≈ **21.75 pt**, `\large` line ≈ 27 pt. Observed density: ~32 body lines on a long-paragraph page (e.g. Ch.5 p. 98), ~26 on a short-paragraph page like §2.1.4.

### 2.1 Cost model per promoted heading

Derived from `report.cls:381–397` (`\@startsection` skips, unmodified by `titlesec` here), 1 ex ≈ 5.17 pt at 12 pt:

| Promotion | Arithmetic | Cost each | Headings per page |
|---|---|---|---|
| bold-inline → `\subsubsection` | 3.25ex (16.8) + line (21.75) + 1.5ex (7.8) | **46.3 pt** | **≈ 15** |
| bold-inline → `\subsection` | 3.25ex (16.8) + `\large` line (27) + 1.5ex (7.8) | **51.6 pt** | ≈ 13.6 |
| `\paragraph` → `\subsection` | `\large` line (27) + 1.5ex (7.8) + `\parskip` (12); the 3.25ex before-skip already exists | **46.8 pt** | ≈ 15 |
| `\paragraph` → `\subsubsection` | line (21.75) + 1.5ex (7.8) + `\parskip` (12) | **41.5 pt** | ≈ 17 |

Net of a small offset: pulling a 2–4-word bold lead out of the body paragraph gives back ~⅓ line (~7 pt) on average, so treat the figures as slight over-estimates of pure vertical space — and slight *under*-estimates once page-break alignment is factored in (a display heading carries `\nobreak` after it, so a heading landing near a page bottom pushes 2–3 lines to the next page).

---

## 3. Complete inventory of bold pseudo-headings

**Definition used:** a `\textbf{}` / `\paragraph{}` that *starts a block and labels the content following it*. Excluded: bold inside `tabular`, `\caption`, figures; bold used for emphasis mid-prose; bold numerals in results tables.

### 3a. Genuine bold pseudo-headings (paragraph-initial, label the block)

| # | File:line | Exact bold text | Sits under | Governs |
|---|---|---|---|---|
| 1 | `chapter1.tex:54` | `\textbf{Chapter~\ref{chap:background}}` | §1.3 Thesis Layout | 1 para (5 lines) |
| 2 | `chapter1.tex:56` | `\textbf{Chapter~\ref{chap:methodology}}` | §1.3 | 1 para (9 lines) |
| 3 | `chapter1.tex:58` | `\textbf{Chapter~\ref{chap:results}}` | §1.3 | 1 para (8 lines) |
| 4 | `chapter1.tex:60` | `\textbf{Chapter~\ref{chap:conclusion}}` | §1.3 | 1 para (2 lines) |
| 5 | `chapter2.tex:86` | `\textbf{Query Expansion}` | §2.1.4 | 1 para + 3-item itemize (≈17 lines) |
| 6 | `chapter2.tex:94` | `\textbf{Query Decomposition}` | §2.1.4 | 1 para (4 lines) |
| 7 | `chapter2.tex:96` | `\textbf{Query Disambiguation}` | §2.1.4 | 1 para (5 lines) |
| 8 | `chapter2.tex:98` | `\textbf{Query Abstraction}` | §2.1.4 | 1 para (5 lines) |
| 9 | `chapter2.tex:117` | `\textbf{Morphological Richness.}` | §2.1.5 | 1 para (7 lines) |
| 10 | `chapter2.tex:119` | `\textbf{Diglossia.}` | §2.1.5 | 1 para (6 lines) |
| 11 | `chapter2.tex:121` | `\textbf{Orthographic Variations.}` | §2.1.5 | 1 para (5 lines) |
| 12 | `chapter2.tex:123` | `\textbf{Diacritical Marks.}` | §2.1.5 | 1 para (4 lines) |
| 13 | `chapter2.tex:264` | `\textbf{Selected benchmark: MIRACL (Arabic).}` | §2.3 | 1 para (9 lines) |
| 14 | `chapter2.tex:266` | `\textbf{Alternatives considered.}` | §2.3 | 1 para (9 lines) |
| 15 | `chapter2.tex:268` | `\textbf{Limitation.}` | §2.3 | 1 para (3 lines) |
| 16 | `chapter5.tex:14` | `\textbf{Baseline establishment and error analysis.}` | §5.1 | 1 para (16 lines) |
| 17 | `chapter5.tex:16` | `\textbf{Query2Doc transfers effectively to Arabic.}` | §5.1 | 1 para (16 lines) |
| 18 | `chapter5.tex:18` | `\textbf{Comprehensive model comparison.}` | §5.1 | 1 para (9 lines) |
| 19 | `chapter5.tex:20` | `\textbf{Patterns observed across model families.}` | §5.1 | 1 para (10 lines) |
| 20 | `chapter5.tex:22` | `\textbf{Dense and sparse retrieval respond differently to QE.}` | §5.1 | 1 para (10 lines) |
| 21 | `chapter5.tex:24` | `\textbf{Query repetition resolves sparse retrieval degradation.}` | §5.1 | 1 para (11 lines) |
| 22 | `chapter5.tex:26` | `\textbf{Hybrid retrieval establishes a strong non-QE ceiling.}` | §5.1 | 1 para (4 lines) |
| 23 | `chapter5.tex:28` | `\textbf{Corpus-steered expansion validates the corpus grounding hypothesis.}` | §5.1 | 1 para (14 lines) |
| 24 | `chapter5.tex:30` | `\textbf{Corpus-grounded and blind expansion are complementary.}` | §5.1 | 1 para (12 lines) |
| 25 | `chapter5.tex:32` | `\textbf{Retriever-specific query representation is critical.}` | §5.1 | 1 para (8 lines) |
| 26 | `chapter5.tex:34` | `\textbf{Per-query analysis localises where the gains arise.}` | §5.1 | 1 para (12 lines) |
| 27 | `chapter5.tex:36` | `\textbf{Overall.}` | §5.1 | 1 para (11 lines) |

### 3b. `\paragraph{}` pseudo-headings — already sectioning commands, but **unnumbered and invisible in the ToC**

Functionally identical to a bold pseudo-heading (`\paragraph` is a run-in bold label; `secnumdepth=3` suppresses its number, `tocdepth=2` suppresses its ToC line).

| File:line | Title | Sits under | Governs |
|---|---|---|---|
| `chapter2.tex:378` | `Notation.` | §2.4.3.2 BM25S | 1 para — **isolated, not a run** |
| `chapter3.tex:362` | `Fixed Repetition (Query2Doc-style).` | §3.6 | 1 para + eq. |
| `chapter3.tex:372` | `Adaptive Repetition (MuGI-style).` | §3.6 | 1 para + eq. |
| `chapter3.tex:382` | `Motivation for the Adaptive Variant.` | §3.6 | 1 para |
| `chapter3.tex:385` | `Sweep Design.` | §3.6 | 1 para |
| `chapter3.tex:394` | `RRF.` | §3.7 | 1 para |
| `chapter3.tex:397` | `CC.` | §3.7 | 1 para |
| `chapter3.tex:400` | `Setup.` | §3.7 | 1 para + figure |
| `chapter3.tex:445` | `CSQE System Prompt.` | §3.8.1 | 2 paras + quote |
| `chapter3.tex:454` | `Rationale for Combining Corpus and Blind Samples.` | §3.8.1 | 1 para |
| `chapter3.tex:497` | `Per-Query Metric Computation.` | §3.9 | 1 para |
| `chapter3.tex:500` | `Classification Thresholds.` | §3.9 | 1 para + itemize |
| `chapter3.tex:509` | `First-Pass Quality Split.` | §3.9 | 1 para |
| `chapter3.tex:512` | `Regression Classification.` | §3.9 | 1 para + itemize |
| `chapter4.tex:935` | `Type A: Strong BM25 Hurt by Expansion.` | §4.10.4 | 1 para |
| `chapter4.tex:938` | `Type B: Poisoned First-Pass.` | §4.10.4 | 1 para |
| `chapter4.tex:941` | `Implications.` | §4.10.4 | 1 para |

### 3c. Explicitly EXCLUDED — bold-led **list items**, not pseudo-headings

These sit inside `itemize`/`enumerate`, are indented under a bullet or number, and the list itself is the semantic unit. Promoting any of them would destroy a deliberate list. **Not promotion candidates.**

`chapter2.tex:40,41` (Retriever/Generator) · `:89,90,91` (HyDE/Query2Doc/GRF) · `:467,469,471,473` (the four research gaps — the numbering *is* the content) ·
`chapter3.tex:27,28` · `:39,40,41` · `:89,90,91` · `:121,122,123` · `:131–134` · `:145,146,147` · `:184,186,188,190` · `:229,230,231` · `:273,274` · `:309–312` · `:323,324` · `:333,335,337,339` · `:348,349,350` · `:423–426` · `:463,464,465` · `:476,477,478` · `:504,505,506` · `:516,517,518` ·
`chapter4.tex:358,359,360` · `:427,429,431,433` · `:493,495,497,499,501` (bold *sentences*, not labels) ·
`chapter5.tex:46–60` (8 Challenges items) · `:71–87` (9 Recommendations items).

### 3d. Explicitly EXCLUDED — bold for emphasis in running prose

`chapter4.tex:206` (`term dilution`) · `chapter4.tex:391` (full-sentence emphasis) · `chapter4.tex:683` (`retriever-specific query representation principle`) · `chapter5.tex:28` (the bolded 0.7137 headline). Plus every `\textbf{}` inside `tabular` headers and numeric cells (~120 occurrences) and inside `\caption{}` — all excluded by definition.

---

## 4. Runs (2+ parallel siblings = promotion candidates)

| Run | Location | Members | Current form | Target level | Cost (pt) | Cost (page) | ToC lines added |
|---|---|---|---|---|---|---|---|
| **R0** | §1.3 (`ch1:54–60`) | 4 | bold inline | — | — | — | — |
| **R1** | **§2.1.4** (`ch2:86,94,96,98`) | 4 | bold inline | `\subsubsection` 2.1.4.1–4 | 185 | **0.26** | **0** |
| **R2** | **§2.1.5** (`ch2:117,119,121,123`) | 4 | bold inline | `\subsubsection` 2.1.5.1–4 | 185 | **0.26** | **0** |
| **R3** | §2.3 (`ch2:264,266,268`) | 3 | bold inline | `\subsection` 2.3.1–3 | 155 | 0.22 | 3 (free) |
| **R4** | §3.6 (`ch3:362,372,382,385`) | 4 | `\paragraph` | `\subsection` 3.6.1–4 | 187 | 0.27 | 4 (free) |
| **R5** | §3.7 (`ch3:394,397,400`) | 3 | `\paragraph` | `\subsection` 3.7.1–3 | 140 | 0.20 | 3 (free) |
| **R6** | §3.8.1 (`ch3:445,454`) | 2 | `\paragraph` | `\subsubsection` 3.8.1.1–2 | 83 | 0.12 | 0 |
| **R7** | §3.9 (`ch3:497,500,509,512`) | 4 | `\paragraph` | `\subsection` 3.9.1–4 | 187 | 0.27 | 4 (free) |
| **R8** | §4.10.4 (`ch4:935,938,941`) | 3 | `\paragraph` | `\subsubsection` 4.10.4.1–3 | 124 | 0.18 | 0 |
| **R9** | **§5.1** (`ch5:14–36`) | **12** | bold inline | `\subsection` 5.1.1–12 | 619 | **0.88** | 12 (free) |
| | | | | **TOTAL if all promoted** | 1 865 | **≈ 2.7 → +3 in practice** | 26 (all free) |

**Isolated bold leads — NOT promotion candidates** (a lone `\subsubsection` under a parent that has no other child is a style defect, not an improvement): `chapter2.tex:378` (`\paragraph{Notation.}`, sole child of 2.4.3.2). No other genuine singletons exist in §3a/3b.

### Per-run recommendation

**R0 — §1.3 Thesis Layout (4 bold `Chapter~\ref{}` leads) → KEEP AS IS, and do not touch.**
Direct conflict with **task C4** (`TASKS.md:139`), which requires §1.3 to become *one single continuous paragraph*. C4 deletes these four leads outright. Promoting them would have to be undone by C4. Also, the four "headings" are cross-references, not titles — `\subsection{Chapter 2}` is meaningless. **Cost of not doing it: 0. Do C4 instead.**

**R1 — §2.1.4 QE Techniques → PROMOTE.** Supervisor's explicit ask (video 2, 06:10–07:20). A clean four-member taxonomy (`expansion / decomposition / disambiguation / abstraction`) that the §2.1.4 preamble already names as "four atomic operations… Each operation is described below". This is the textbook case for numbered sub-headings. `\subsubsection{}` at depth 3 → numbered `2.1.4.1`–`2.1.4.4`, no ToC change. **0.26 page.** One caveat (§5) and one orphan problem (§5).

**R2 — §2.1.5 Arabic Language Processing Challenges → PROMOTE.** Same directive. Four parallel linguistic phenomena; the leads already carry a terminal period inside the braces, i.e. they are already written as run-in headings. **Zero prose change required** — the cleanest promotion in the thesis. `\subsubsection{}` → `2.1.5.1`–`2.1.5.4`. **0.26 page.**

**R3 — §2.3 Evaluation Dataset Selection → PROMOTE-BUT-DEFER.**
Genuinely qualifies under "audit for any OTHER large section using bold-text pseudo-headings": 3 siblings, ~2 pages, no existing subsections. *But* it is a report-style rhetorical sequence (selection → alternatives → limitation), not a taxonomy, and the members are not parallel in weight (9 / 9 / 3 lines). The first title, `Selected benchmark: MIRACL (Arabic).`, reads awkwardly as `2.3.1`. Target level is `\subsection` (only depth-2 slot is free under §2.3), which is the *most* expensive kind of promotion. **Defer; revisit only if the page budget turns positive after D2/D5.** Cost if done: 0.22 page.

**R4 — §3.6 Query Repetition (4 `\paragraph`) → PROMOTE-BUT-DEFER.**
Strongest of the Ch.3 candidates: 4 parallel members, and §3.6 is currently the *only* Ch.3 section from 3.1–3.9 with no subsections at all despite being 2 pages long. Promoting to `\subsection` 3.6.1–3.6.4 would make it consistent with §3.1–3.5. However: these are already `\paragraph{}` — real sectioning commands producing real bold headings — so the supervisor's complaint ("bold *inline* pseudo-headings") is only half applicable. The observable defect is that they are *unnumbered and absent from the ToC*, which is a `secnumdepth`/`tocdepth` symptom, not a markup one. Cost 0.27 page + 4 free ToC lines.

**R5 — §3.7 Hybrid Retrieval Fusion (3 `\paragraph`) → KEEP AS IS.** Only 3 members, two of which (`RRF.`, `CC.`) are two-character labels; §3.7 is barely 1.5 pages. `3.7.1 RRF` / `3.7.2 CC` / `3.7.3 Setup` fragments a short section for no reader benefit. Cost avoided: 0.20 page.

**R6 — §3.8.1 (2 `\paragraph`) → KEEP AS IS.** Only 2 members, and they are asymmetric (a prompt listing + a rationale). Already sits under a numbered `\subsection` (3.8.1). Cost avoided: 0.12 page.

**R7 — §3.9 Per-Query Error Analysis (4 `\paragraph`) → PROMOTE-BUT-DEFER.** Same profile as R4: 4 parallel members, 3-page section with no subsections. Same argument and same verdict. Cost 0.27 page.

**R8 — §4.10.4 Regression Analysis (3 `\paragraph`) → KEEP AS IS.** `Type A` / `Type B` / `Implications.` is not a clean parallel series — the third member is a closer, not a third type. Promoting all three produces `4.10.4.3 Implications`, which mislabels it as a peer of Types A and B. (There is no Type C paragraph even though Table 4.25 lists one — see §7.) Cost avoided: 0.18 page.

**R9 — §5.1 Conclusions (12 bold leads) → KEEP AS IS. Strongest "do not do this" in the audit.**
It is the largest run in the thesis (12 members, 5 pages, `chapter5.tex:14–36`) and therefore the most likely thing a reader of C5's "audit for any OTHER large section" would land on. Four independent reasons not to:
1. **Cost.** 0.88 page — a third of the entire audit's cost, on a manuscript already 4 pages over.
2. **The "headings" are full sentences.** `5.1.8 Corpus-steered expansion validates the corpus grounding hypothesis` is a claim, not a title. Turning claims into headings is a different (and larger) editorial job than promoting labels.
3. **Over-fragmentation.** 12 numbered subsections for a 5-page Conclusions section, in a thesis whose other sections average 3–5 subsections.
4. **`\subsection` is the only free level** (§5.1 has no children), so all 12 *would* enter the ToC — 12 extra ToC lines is likely a 13th ToC page. Free against the 100-page core, but it makes the Contents look like an index.
Cost avoided: 0.88 page.

### Recommended C5 scope

| Do | Runs | Page cost |
|---|---|---|
| **Now (supervisor directive)** | R1 + R2 | **+0.53 → +0 or +1 page** |
| Defer to post-D2/D5 (only if budget allows) | R3, R4, R7 | +0.76 page |
| Never | R0 (C4 conflict), R5, R6, R8, R9 | — |

---

## 5. §2.1.4 and §2.1.5 — full detail

### 5.1 §2.1.4 QE Techniques — `chapter2.tex:81–110`, PDF pp. 12–13

**Today.** `\subsection{QE Techniques}` + `\label{sec:qe_techniques}`, then:
```
:84   preamble — names the "four atomic operations" and says "Each operation is described below"
:86   **Query Expansion** broadens …          <- bold lead #1
:88-92  itemize{ HyDE:, Query2Doc:, GRF: }    <- nested list under lead #1
:94   **Query Decomposition** breaks …        <- bold lead #2
:96   **Query Disambiguation** reformulates … <- bold lead #3
:98   **Query Abstraction** steps back …      <- bold lead #4
:100  "Among these four families, query expansion is adopted…"   <- SECTION-level closer
:102  "These QE techniques operate as modular layers…"           <- SECTION-level closer
:104-110  Table 2.1 (float [H])                                  <- SECTION-level float
```

**Proposed structure** (titles verbatim from the current bold text, no rewording):

| New number | Title (verbatim) | Source line |
|---|---|---|
| 2.1.4.1 | Query Expansion | `chapter2.tex:86` |
| 2.1.4.2 | Query Decomposition | `chapter2.tex:94` |
| 2.1.4.3 | Query Disambiguation | `chapter2.tex:96` |
| 2.1.4.4 | Query Abstraction | `chapter2.tex:98` |

Command: `\subsubsection{Query Expansion}` etc. — numbered (secnumdepth 3), no ToC entry (tocdepth 2), style identical to the existing `2.1.3.1 Sparse Retrieval` two subsections earlier.

**⚠ Flag 1 — the four leads are grammatically fused into their sentences.** Unlike §2.1.5, these bold runs have no terminal period and are the grammatical *subject*:
`\textbf{Query Expansion} broadens the scope of a query…` → pulling the label into a heading leaves `broadens the scope of a query…`, a fragment. All four (`:86`, `:94`, `:96`, `:98`) are affected. Each needs the subject restored (e.g. `Query expansion broadens…`). **This is a forced consequence of the structural change, not a wording proposal — but it means R1 is not a pure markup edit and must be reviewed for sense, whereas R2 is.**

**⚠ Flag 2 — two orphaned closing paragraphs + a table.** `:100`, `:102` and Table 2.1 belong to §2.1.4 *as a whole*, not to Query Abstraction. After promotion they fall under `2.1.4.4 Query Abstraction`, which is wrong. Three structural options, none of which requires new prose except (c):
- **(a) Accept it.** Cheapest; the misattribution is mild and common in published theses. This is what I would do given the page budget.
- **(b) Move `:100` and `:102` + Table 2.1 above the first `\subsubsection`.** Zero page cost, zero new prose — but `:100` opens "Among these four families…", so it cannot precede them without reordering the argument. **Not viable as-is.**
- **(c) Add a fifth `\subsubsection` to hold them.** Costs +46 pt and requires inventing a title — a prose decision, out of C5's structural scope. Flag to Elhaj/supervisor if (a) is unacceptable.

**⚠ Flag 3 — nested bullets stay put.** `HyDE:` / `Query2Doc:` / `GRF:` (`:89–91`) sit one level below Query Expansion. They must remain an `itemize`; promoting them would need `\paragraph` at depth 4, which is unnumbered and would look broken directly under a numbered `2.1.4.1`. **Do not promote.**

**⚠ Flag 4 — asymmetry.** 2.1.4.1 governs ~17 lines (para + 3 bullets); its three siblings govern 4–5 lines each. Structurally legal, visually lopsided. No action needed; noted for the supervisor.

### 5.2 §2.1.5 Arabic Language Processing Challenges — `chapter2.tex:112–125`, PDF pp. 14–15

**Today.** `\subsection{Arabic Language Processing Challenges}` + `\label{sec:arabic_challenges}`, then a 2-line preamble (`:115`), four bold-led paragraphs, and one closing paragraph (`:125`).

**Proposed structure** (titles verbatim, minus the terminal period which moves out of the heading):

| New number | Title (verbatim, period dropped) | Source line |
|---|---|---|
| 2.1.5.1 | Morphological Richness | `chapter2.tex:117` |
| 2.1.5.2 | Diglossia | `chapter2.tex:119` |
| 2.1.5.3 | Orthographic Variations | `chapter2.tex:121` |
| 2.1.5.4 | Diacritical Marks | `chapter2.tex:123` |

**✅ Zero prose change required.** All four leads are self-contained (`\textbf{Diglossia.} Arabic exhibits a diglossic situation…`) — deleting the bold run leaves a complete sentence. This is the one run in the whole thesis that promotes cleanly with a pure markup edit.

**⚠ Flag 5 — one orphaned closing paragraph.** `:125` ("These characteristics collectively create what may be termed a 'morphological gap'…") is a §2.1.5-level closer and would fall under `2.1.5.4 Diacritical Marks`. Same three options as Flag 2; **(a) accept** is the pragmatic call.

**⚠ Flag 6 — no bold item in either section fails to fit the series.** All eight are genuine parallel siblings. The only misfits are the *closers*, which were never bold in the first place.

### 5.3 Page-cost of R1 + R2, stated precisely

8 × 46.3 pt = **370 pt = 0.53 of a 700 pt text block ≈ 17 body lines.**
§2.1.4 currently ends mid-p. 13 with Table 2.1 floating to p. 14; §2.1.5 ends on p. 15 with §2.2 starting immediately below. Adding ~8.5 lines to each section will push Table 2.1 and the §2.2 heading down. Because `float [H]` forbids deferral, a table that no longer fits will end its page early and waste the remainder.

> **Realistic outcome: +1 page on Ch. 2 (104 → 105), with a genuine chance of +0 if the breaks fall kindly. Budget for +1.**
> ToC impact: **0 lines** — and even a nonzero ToC impact would be free, because the ToC is front matter and is excluded from the 100-page core count.

---

## 6. Side effects

**(a) Cross-references — no breakage.** Every `\ref` that touches an affected section points at the *parent* label, which stays attached to the parent's `\subsection`/`\section`. Adding children does not renumber a parent.

| Label | Refs | Referenced from |
|---|---|---|
| `sec:qe_techniques` (§2.1.4) | 2 | `chapter2.tex:500`, `chapter3.tex:169` |
| `sec:arabic_challenges` (§2.1.5) | 1 | `chapter2.tex:501` |
| `sec:dataset_selection` (§2.3) | 2 | `chapter2.tex:5,503` |
| `sec:meth_repetition` (§3.6) | 3 | `chapter2.tex:438`, `chapter3.tex:5`, `chapter4.tex:441` |
| `sec:meth_hybrid` (§3.7) | 2 | `chapter3.tex:5`, `chapter4.tex:523` |
| `sec:meth_error_csqe` (§3.9) | 3 | `chapter3.tex:5,126`, `chapter4.tex:784` |
| `sec:conclusions` (§5.1) | 0 | — |

**Label-placement check (the one real hazard):** `\label` immediately following a `\subsubsection` binds to the *subsubsection*, not the parent. Verified safe — `\label{sec:qe_techniques}` is at `chapter2.tex:82` and `\label{sec:arabic_challenges}` at `:113`, both on the line directly after their `\subsection` and before any body text or new heading. As long as the new `\subsubsection`s are inserted at `:86/:94/:96/:98` and `:117/:119/:121/:123` — i.e. *after* the existing labels — nothing rebinds. Same holds for `sec:dataset_selection` (`:240`), `sec:meth_repetition` (`:357`), `sec:meth_error_csqe` (`:492`), `sec:conclusions` (`chapter5.tex:9`).

**(b) ToC depth/appearance.**
- R1/R2/R6/R8 (`\subsubsection`, level 3) → **no ToC change whatsoever** (tocdepth 2), and no PDF bookmark (bookmarksdepth 2).
- R3/R4/R5/R7/R9 (`\subsection`, level 2) → **would** add ToC lines *and* PDF bookmarks. 26 lines if all were done; likely +1 ToC page. **Front matter — does not count toward the 100-page core.**
- If anyone later raises `tocdepth` to 3 to expose the new 2.1.4.x/2.1.5.x, it retroactively exposes **all 20 existing subsubsections plus 17 `\paragraph`s**, adding ~30 ToC lines at once. **Do not raise `tocdepth` as part of C5.**

**(c) Existing `\subsubsection` style — confirmed and matchable.** 20 in use (list in §1). Rendering verified in the PDF: `2.1.3.1 Sparse Retrieval`, `2.2.4.2 NDCG@k`, `2.4.3.1 mDPR`, `2.4.1.3 ALLaM-7B` all appear flush-left, bold, `\normalsize`, on their own line, with the number. **Numbered depth-4 headings already exist and work.** The new 2.1.4.x/2.1.5.x will be visually indistinguishable from them. Ch. 2 is where all of them live, so R1/R2 also improve intra-chapter consistency: §2.1.3, §2.2.4, §2.4.1, §2.4.2 and §2.4.3 all use numbered subsubsections while §2.1.4 and §2.1.5 alone use bold runs.

**(d) ⚠ The committed `1-main.pdf` is stale — do not use it to measure anything.** `git log` shows both `Chapters/chapter2.tex` and `1-main.pdf` last changed in `14533f2` ("revert out-of-scope final-round changes"), but the committed PDF was built *before* that commit's source reverts: it still contains the CSQE taxonomy bullet in §2.1.4 and the "generate or select" wording, both of which `14533f2` removed from `chapter2.tex`. Committed PDF = 131 pp / core 105; clean rebuild of current sources = 130 pp / core 104. **All numbers in this report come from the clean rebuild.**

---

## 7. OUT OF SCOPE — candidate new tasks

1. **Page count is 104, not 103.** `TASKS.md` D1 records 103 (Ch.5 p. 95, Bib p. 104). A clean rebuild of the current sources gives Ch.5 p. 96, Bib p. 105 → **core = 104, i.e. 4 over, not 3.** D2/D5 must free one more page than budgeted. Suggest updating the D1 entry.
2. **Committed `1-main.pdf` does not match committed sources** (§6d). Anyone measuring pages or checking layout from the repo PDF will be off by ~1 page and will see reverted text. Suggest a rebuild-and-commit, or drop the PDF from version control.
3. **`\paragraph{}` headings are silently unnumbered *and* invisible in the ToC.** 17 of them across Ch. 2–4. With `secnumdepth=3` they render as bold run-in labels with no number — the exact visual outcome the supervisor objected to for §2.1.4/§2.1.5. If she applies the same objection to Ch. 3, R4/R5/R7 come back into play. Worth pre-empting at the next meeting.
4. **Two singleton `\subsubsection`s.** `chapter4.tex:203` (`4.3.2.1 Term Dilution Analysis`, only child of §4.3.2) and `chapter4.tex:329` (`4.4.3.1 ALLaM-7B`, only child of §4.4.3). A 1-of-1 numbered subdivision is a style smell in both directions — either promote to `\subsection` or demote to plain prose. Cheap either way.
5. **§4.10.4 documents Type A and Type B but not Type C**, while Table 4.25 (`chapter4.tex:900–913`) reports Type C as 45 queries / 12%. The `\paragraph` run stops at Type B and jumps to `Implications.` Content gap, not a structural one.
6. **§3.9 and §4.10 share the identical title "Per-Query Error Analysis".** Deliberate under the zigzag methodology↔results structure, but two identically named sections in one ToC may draw a comment.
7. **`chapter4.tex:433` breaks its list's parallelism.** Items 1–3 of §4.5.5 are model profiles (`Strongest overall performance:` …); item 4 is `\textbf{Temperature 0.1} was found to be optimal…`, a hyperparameter finding. Not a heading issue — a list-hygiene one.
8. **`Chapters/chapter2_generated.tex` is dead weight.** Not `\include`d by `1-main.tex`, contains an older draft of §2.1.4/§2.1.5 with 20+ bold pseudo-headings. It matched several audit greps and will keep polluting future searches. Suggest deleting or moving it out of `Chapters/`.
