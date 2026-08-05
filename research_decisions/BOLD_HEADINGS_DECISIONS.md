# Bold Pseudo-Headings — Complete Inventory and Decision

**Date:** 2026-08-04
**Supersedes:** task **J8** (Elhaj 2026-08-04: *do not ask Dr. Tahani; decide it ourselves*)
and widens **C5** from 8 headings to the whole thesis.
**Status:** DECISION PROPOSAL. Nothing applied.

---

## 1. What was found

Automated pass over `chapter1.tex` … `chapter5.tex`, excluding anything inside
`tabular`, `figure`, `caption`, `verbatim` or `equation`.

| Kind | Count | What it is |
|---|---|---|
| `BOLD-LEAD` | **27** | `\textbf{...}` at the start of a paragraph |
| `PARAGRAPH` | **17** | `\paragraph{...}` — a real command, but renders with **no number and no ToC line** at our settings |
| `LIST-ITEM` | **94** | `\item \textbf{...}` inside `itemize`/`enumerate` |
| | **138** | |

`BOLD-LEAD` and `PARAGRAPH` look **identical on the printed page**: bold text,
no number, absent from the Contents. Those 44 are the ones in question.

---

## 2. The rule used to decide

Dr. Tahani's objection is that **bold text is being used to fake a heading**. So:

- **PROMOTE** where the label really is a heading — a short noun phrase naming a
  block of parallel content that a reader would want to find in the structure.
- **DE-BOLD** where it is not a heading — a full sentence, a one-off signpost, a
  closer, or a label that merely repeats the first words of its own paragraph.
- **LEAVE** list items. A bold lead inside `\item` is a definition list, not a fake
  heading. It is standard academic style, she never objected to it, and promoting
  or de-bolding would damage the lists.

Second test: **a heading is never a full sentence.** Anything ending in a period
that is a complete sentence gets de-bolded, not promoted.

---

## 3. Decision table — the 44

### PROMOTE → 19 headings

| § | Lines | Items | New level | Why |
|---|---|---|---|---|
| **2.1.4** QE Techniques | `ch2:86,94,96,98` | Query Expansion · Decomposition · Disambiguation · Abstraction | `\subsubsection` **2.1.4.1–4** | Supervisor's explicit ask. A genuine 4-part taxonomy the section preamble already announces as "four atomic operations". |
| **2.1.5** Arabic Challenges | `ch2:117,119,121,123` | Morphological Richness · Diglossia · Orthographic Variations · Diacritical Marks | `\subsubsection` **2.1.5.1–4** | Supervisor's explicit ask (Report §7: *"maintain clear sub-headings"*). Four parallel linguistic phenomena. |
| **2.3** Dataset Selection | `ch2:264,266,268` | Selected benchmark: MIRACL (Arabic) · Alternatives considered · Limitation | `\subsection` **2.3.1–3** | ~2 pages with no subsections at all. All three read naturally as headings. |
| **3.6** Query Repetition | `ch3:362,372,382,385` | Fixed Repetition · Adaptive Repetition · Motivation for the Adaptive Variant · Sweep Design | `\subsection` **3.6.1–4** | 2 pages, **the only §3.x from 3.1–3.9 with no subsections**. Four parallel method steps. |
| **3.9** Per-Query Error Analysis | `ch3:497,500,509,512` | Per-Query Metric Computation · Classification Thresholds · First-Pass Quality Split · Regression Classification | `\subsection` **3.9.1–4** | 3 pages, no subsections. Four parallel method steps. |

### DE-BOLD → 25 items

| § | Lines | Items | Why not a heading |
|---|---|---|---|
| **5.1** Conclusions | `ch5:14–36` (12) | "Corpus-steered expansion validates the corpus grounding hypothesis." etc. | **They are complete sentences, not titles.** They already work as topic sentences — removing the bold changes nothing except that they stop pretending to be headings. Promoting would mean 12 subsections in a 5-page section, +0.88 page, and 12 ToC lines. |
| **3.7** Hybrid Fusion | `ch3:394,397,400` (3) | RRF. · CC. · Setup. | Each label **repeats the first word of its own sentence** — `\paragraph{RRF.}` followed by *"RRF (Equation…) combines ranked lists…"*. Pure redundancy. "Setup" is a closer, not a peer. |
| **3.8.1** CSQE Pipeline | `ch3:445,454` (2) | CSQE System Prompt. · Rationale for Combining Corpus and Blind Samples. | Only two, and asymmetric — a prompt listing plus a rationale. Already sits under a numbered `\subsection`. |
| **4.10.4** Regression Analysis | `ch4:935,938,941` (3) | Type A… · Type B… · Implications. | ⚠️ **Decisive reason:** Table 4.25 reports **three** types, but only A and B have paragraphs. Numbering them `4.10.4.1 Type A` / `4.10.4.2 Type B` makes the **missing Type C a visible gap in the numbering**. De-bolding hides nothing and creates no gap. Also "Implications" is a closer, not a third type. *(See J6.)* |
| **2.4.3.2** BM25S | `ch2:378` (1) | Notation. | A lone `\paragraph` under a parent with no other child. Deleting it leaves a complete sentence: *"Throughout the remainder of this thesis, the term 'BM25' refers to…"*. |

### HANDLED ELSEWHERE → 4

| § | Lines | Disposition |
|---|---|---|
| **1.3** Thesis Layout | `ch1:54,56,58,60` | **C4** deletes these outright when §1.3 becomes one paragraph. Do not promote — it would have to be undone. |

### LEAVE → 94 list items

All 94 `\item \textbf{...}` stay exactly as they are. Two are worth flagging as
*list-hygiene* issues, not heading issues:

- ⚠️ `chapter4.tex:493–501` — five items whose bold text is a **full sentence**
  ("Query repetition brought all nine models above the BM25 baseline."), not a label.
  Inconsistent with every other list in the thesis. **Log, do not fix here.**
- ⚠️ `chapter4.tex:433` — items 1–3 of §4.5.5 are model profiles ("Strongest overall
  performance:"); item 4 is `\textbf{Temperature 0.1} was found to be optimal…`, a
  hyperparameter finding. Breaks the list's parallelism. **Log, do not fix here.**

---

## 4. Page impact

Text block 452 pt wide, ~700 pt tall. Costs derived from `report.cls` `\@startsection`.

| Action | Count | Unit | Total |
|---|---|---|---|
| Promote to `\subsubsection` (2.1.4, 2.1.5) | 8 | +46.3 pt | +370 pt |
| Promote to `\subsection` (2.3, 3.6, 3.9) | 11 | +51.6 / +46.8 pt | +529 pt |
| De-bold a `\paragraph` (removes its 3.25ex before-skip) | 9 | −17 pt | −153 pt |
| De-bold an inline `\textbf` lead (§5.1, §2.3 n/a) | 12 | ~0 | 0 |
| | | **net** | **+746 pt ≈ +1.07 page** |

**ToC lines added: 11** (the `\subsection` promotions only — `\subsubsection` is
invisible at `tocdepth=2`). **ToC is front matter and does not count** toward the
100-page core.

> **Budget:** the core is at **exactly 100**. This costs **+1**. **J2** (heading sizes,
> −1 to −2) must be applied **first** to pay for it. If the budget still bites, the
> first thing to drop is the **§2.3 promotion** (−0.22 page, and it is the weakest of
> the five — a rhetorical sequence rather than a taxonomy).

---

## 5. Why this is defensible without asking Dr. Tahani

1. **Everything she explicitly named is promoted** — §2.1.4 and §2.1.5, exactly as
   directed (Report §7, video 2 06:10–07:20).
2. **The rule is the one she stated**, not one we invented: the faculty guidelines say
   *"Use headings and subheadings to describe briefly the material in the section that
   follows"* and *"Second-level and subsequent subheadings may be included."* Both
   promotions and de-bolds follow from that.
3. **Nothing bold-and-fake is left standing.** After this, no `\textbf` or `\paragraph`
   in the thesis acts as a heading. The complaint cannot recur anywhere else.
4. **Numbered depth-4 headings already exist** — 20 of them, all in Ch.2 (2.1.3.1,
   2.2.4.2, 2.4.3.1 …). The promotions match established style rather than introducing one.
5. **The de-bolds are all pure markup**, except §2.3 which is promoted instead. No
   sentence changes meaning.

---

## 6. Prose repairs forced by this (the only writing involved)

**§2.1.4 — four sentences.** Its leads are the grammatical *subject*:

```
\textbf{Query Expansion} broadens the scope of a query…
```

Promotion leaves `broadens the scope of a query…`, a fragment. Each needs its subject
restored:

| Line | After promotion, the body must start |
|---|---|
| `ch2:86` | Query expansion broadens the scope of a query… |
| `ch2:94` | Query decomposition breaks… |
| `ch2:96` | Query disambiguation reformulates… |
| `ch2:98` | Query abstraction steps back… |

**§2.3 — three labels.** `\textbf{Selected benchmark: MIRACL (Arabic).}` is followed by
*"MIRACL was selected as the primary evaluation benchmark."* — promoting the label to a
heading leaves the body repeating it. The body sentence needs its opening trimmed, or
the heading shortened to `Selected Benchmark`. **Recommendation: heading =
`Selected Benchmark`, body unchanged.**

**Everything else — zero prose change.** §2.1.5's leads already end with a period
inside the braces; §5.1's, §3.7's, §3.8.1's, §4.10.4's and §2.4.3.2's bodies are all
complete sentences without their labels.

---

## 7. Orphaned closers (unchanged from the C5 audit)

After promotion, section-level closing paragraphs fall under the *last* child:
`chapter2.tex:100`, `:102` + Table 2.1 (§2.1.4) and `:125` (§2.1.5).

**Accept it.** Moving them is not viable — `:100` opens *"Among these four families…"*
so it cannot precede them — and adding a holder subsubsection costs a heading plus an
invented title. The misattribution is mild and common in published theses.

---

## 8. After this is applied — what to review

1. ⚠️ **Insert new `\subsubsection`s *after* the existing `\label`s.**
   `\label{sec:qe_techniques}` (`ch2:82`) and `\label{sec:arabic_challenges}` (`ch2:113`)
   sit directly under their `\subsection`. A `\label` immediately following a heading
   binds to *that* heading — inserting above them rebinds 3 cross-references
   (`ch2:500,501`, `ch3:169`). Same hazard for `sec:dataset_selection` (`ch2:240`),
   `sec:meth_repetition` (`ch3:357`), `sec:meth_error_csqe` (`ch3:492`).
2. **Confirm 0 undefined references** in the log.
3. **Confirm the ToC gained exactly 11 lines** and no subsubsections appeared —
   that proves `tocdepth` behaved as measured.
4. ⚠️ **Do NOT raise `tocdepth`.** It would expose all 20 existing subsubsections plus
   the remaining `\paragraph`s at once, ~30 new ToC lines.
5. **Re-measure the core page count** and update `SESSION_HANDOFF.md` §0.
6. **J6 interacts with §4.10.4** — de-bolding there is the right move *because* Type C
   is missing. If J6 later adds a Type C paragraph, revisit whether promotion becomes
   viable.
7. **Two list-hygiene items logged** (`ch4:493–501`, `ch4:433`) — not fixed here.
