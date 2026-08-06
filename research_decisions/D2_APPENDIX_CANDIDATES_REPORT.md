# D2 — Appendix-Candidates Analysis

**Task:** D2 (Phase D), `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`
**Owner:** Osman · **Run:** 2026-08-02 · **Status:** analysis only — no `.tex`, notebook, or figure was modified.
**REVIEWED AND DECIDED 2026-08-02 by Osman + Elhaj.** §0.5 below is the authoritative decision list and **overrides the recommendations in §2–§5 wherever they differ**. The original analysis is left intact as the record of why each call was on the table.
**✅ EXECUTED 2026-08-02.** All decisions have been applied to the thesis — appendices A/B/C created, main-text moves and stubs done, build verified (0 errors, 0 undefined refs). See the D3 entry in `THESIS_FINAL_SUBMISSION_TASKS.md`. **Deviations from §0.5, on Osman's instruction:** no `License` column was added to Table 2.3 (⚠️-A declined); Table 4.22 was already deleted by the team, so Table 4.28 moved to Appendix B without a replacement inline (TAB-4a's second half is moot — the progression is carried by Figure~4.11).
**Feeds:** D3 (build the code appendix), D5 (conciseness pass), D4 (clean repo), E3 (table audit).
**Consumes:** `research_decisions/E1_FIGURE_TABLE_DUPLICATION_REPORT.md` (its keep/drop verdicts are taken as settled and are **not** re-litigated here).

**Sources of truth used:** the committed `1-main.pdf` (**131 sheets**, created 2026-07-29 22:38, its own embedded ToC/LoT), rendered pages 14 / 78 / 81 / 93 / 96 / 97, `Chapters/chapter2–5.tex`, `1-main.tex`, `arabic-rag-query-enhancement/` (`src/`, `experiments/`).

> **Every item below is individually numbered so it can be approved or rejected on its own line.** Nothing here has been applied. The checklist in §6 is the sign-off sheet.

---

## 0. Headline findings

1. **The page count everyone is working from is wrong, in both directions.** The real core manuscript is **105 pages** — we are **5 OVER** the 100-page limit, not 3 over (D1's answer) and definitely not already under it (E1's answer). Full derivation and the explanation of how three numbers came to exist is in §1.
2. **Consequence:** D5 does *not* get to be gentle. E1's closing advice ("these cuts buy margin, they are not rescuing a violation") was based on a stale build and should be reversed. With a 5-page safety margin we need to free **≈10 pages**.
3. **The single biggest lever is not a table — it is §2.4's per-model prose** (≈4.5 pages of "exhaustive per-model listings" for 10 models). It is the purest instance of what Dr. Tahani described, and Phase A already de-scoped model characteristics as a contribution (task A2 removed *"and what model characteristics determine effectiveness"* from the RQ). Moving the detail cards to an appendix is both a page win and a narrative fix. **≈3.5 pages net.**
4. **Two live layout defects found while sizing tables** (§3.6): **Table 4.28 overflows the right text margin** — the `Status` column is clipped mid-word in the compiled PDF ("Baselin", "Droppe", "Best ove") — and it sits nearly alone on p.96 under half a page of whitespace. **Table 2.1's rules also run past the right margin** on p.14. Both are moot if the tables move, which is a further argument for moving them.
5. ~~**Code appendix: 8 snippets, ≈500 lines, ≈11–12 pages.**~~ → **DECIDED: 4 snippets, ≈165–255 lines, ≈4–6 pages** (§0.5). The team excluded fusion, evaluation, retrieval and first-pass code; Appendix C now covers the CSQE prompts, config and assembly logic only. Everything else — 11 near-identical generator notebooks, the plotting cells, the Colab plumbing, and ~520 lines of contrastive-HyDE code that **does not appear in the thesis at all** — stays repo-only.
6. ~~**One cross-report conflict to resolve before D3/D5 run**~~ → **RESOLVED: TAB-4a.** Table 4.28 moves to the appendix and **Table 4.22 stays inline**. ⚠️ **E1's action list contains `DELETE … tab:system_progression (Tab 4.22)` — that line must be SKIPPED when D5 executes it**, or Ch.4 loses the system-progression numbers entirely.
7. **`\appendix` will not work out of the box.** `1-main.tex:40-45` hardcodes the chapter label as `Chapter \thechapter`, so appendices will render **"Chapter A"**, and `\chaptermark` (line 32) will put "Chapter A - …" in every running header. `listings` is not loaded either. Concrete fixes for D3 in §2.4.

---

## 0.5 DECISIONS APPLIED — 2026-08-02 (authoritative)

Reviewed by both team members. This section supersedes §2–§5 where they differ.

### Appendix structure — REORDERED (narrative flow, not the order proposed in §5.1)

```
Appendix A — Model Details            Table 2.4 + §2.4.1-2.4.2 prose + §3.5.4      ≈ 6 pp
Appendix B — Extended Result Tables   Tables 4.12, 4.14 full sweep, 4.28, 4.26     ≈ 3 pp
Appendix C — Implementation Code      4 snippets, CSQE + prompts only              ≈ 4-6 pp
```

### Tables and main-text cuts

| ID | Decision | vs. report |
|---|---|---|
| **TAB-1** | Table 4.26 → **Appendix B**. Replace inline with a 1–2 sentence stub using the al-Ribat al-Mansuri example. | as recommended ✔ |
| **TAB-2** | Table 4.12 → **Appendix B**. Fig 4.8 + Table 4.13 stay inline and carry §4.6. | as recommended ✔ |
| **TAB-3** | Table 4.14 → 5-row inline stub (2 baselines, best CC α=0.5, RRF k=20, RRF k=60); full 13-row sweep → **Appendix B**. | as recommended ✔ |
| **TAB-4a** | Table 4.28 → **Appendix B**; **Table 4.22 stays inline** in §4.9.2 so Ch.4 keeps the 0.4621 → 0.7137 progression. **Overrides E1's delete of Table 4.22.** | as recommended ✔ |
| **TAB-5** | **REVERSED.** **Keep Table 2.3 inline**; move **Table 2.4** (full summary, licences, architecture) → **Appendix A**. | report recommended the opposite ✖ |
| **MISC-1** | §2.4.1–2.4.2 per-model prose (~4.5 pp) → **Appendix A**. Leave a concise selection-criteria paragraph inline beside Table 2.3. | approved ✔ |
| **MISC-2** | §3.5.4 model-specific technical issues → **Appendix A**. Leave a 2-sentence pointer inline. | approved ✔ |
| **MISC-3** | §3.5.5 Quantisation Strategy **stays inline**. | as recommended ✔ |

### Code appendix — REDUCED to four items

**Included in Appendix C:**

| ID | Item | Lines |
|---|---|---|
| **CODE-1** | CSQE system prompt + one-shot construction (`exp_013` cell 10) | ~62 |
| **CODE-P** | **NEW** — Query2Doc/QE system prompt, *moved out of Ch.3* (see below) | ~15 |
| **CODE-2** | CSQE core query-repetition and assembly logic (`exp_013` cell 12) | ~150, or ~60 trimmed — see ⚠️-C |
| **CODE-3** | CSQE configuration and hyperparameters (`exp_013` cell 5) | ~28 |
| | **Total** | **~255** (or ~165 trimmed) |

**Now excluded** (were CODE-4 … CODE-9 in §2.1): first-pass retrieval + truncation, **hybrid fusion RRF/CC**, query-repetition helpers, the pytrec_eval evaluation harness, the BM25S/mDPR `search()` methods, and batched pseudo-document generation. Fusion was excluded by explicit decision.

### New main-text cut (not in the original report)

**CUT-P · Remove the system-prompt quote blocks from Chapter 3** → their content lives in Appendix C instead.
- Two blocks exist, both `\begin{quote}`: **`chapter3.tex:198–200`** (§3.4.3 LLM Configuration — the Query2Doc prompt, *"You are asked to write a passage that answers the given query…"*) and **`chapter3.tex:444–446`** (§3.8.1 — the CSQE prompt, *"You are an information retrieval assistant…"*).
- **Honest sizing: this saves ≈0.15 page, not more.** Each block is ~3 rendered lines plus float spacing. Its value is consolidating the prompts into Appendix C, not page budget. Recorded so nobody expects a page from it.
- ⚠️ Keep at least a one-clause description of each prompt's *intent* inline — §3.8.1's surrounding argument (extract vs. generate freely) and the one-shot disclosure at `chapter3.tex:452` both depend on the reader knowing what the prompt asked for.

### Verification outcomes

- **Table 4.28 right-margin overflow** — resolved by the move to Appendix B, with width/formatting set appropriately there. (E3 need not fix it inline.)
- **Table 2.1 (p. 14) overflow** — **confirmed**. Must be fixed inline with `tabularx` or a font-size reduction. → E3.
- **Arabic `k-t-b` morphology rendering (§2.1.5)** — **checked in `1-main.pdf`: renders correctly** (`ك-ت-ب`). ⚠️-6 in §7 was a **false alarm from the page-image extraction, not a defect**. No fix needed. Struck below.

### ⚠️ Three consequences of these decisions that D3 must handle

**⚠️-A · Chapter 2 will assert a licence criterion with no licence evidence left inline.**
`chapter2.tex:286` states models were selected partly on *"open weights under a licence permitting research use, whether permissive or non-commercial"*, and `chapter5.tex:51` raises Aya's CC-BY-NC as a named Challenge. **Table 2.4 is the only table carrying a License column** — and TAB-5 moves it to Appendix A. The per-model prose that states individual licences (`ch2:315` Apache 2.0, `ch2:324`, `ch2:341` Qwen Research License) is moved by MISC-1 in the same pass. After both, nothing inline supports either claim.
**Cheapest fix: add a `License` column to Table 2.3** (which stays inline) when D3 executes TAB-5. One column, no page cost.

**⚠️-B · Appendix C no longer contains the retrieval or fusion pipeline.**
The meeting named *"the CSQE implementation **and the retrieval/fusion pipeline**"* as the code for the appendix; excluding fusion reverses that half. The resulting appendix documents how the expanded query is *built* but not how it is *scored or fused* — and RRF *k*=20 is what turns 0.6157 into the 0.7137 headline. Flagging once, not re-litigating: **the decision is applied as given.** If a committee member asks "where is the fusion code", the answer is the D4 repo link (Appendix C's closing section), which makes that link load-bearing rather than decorative.

**⚠️-C · CODE-2's scope needs one word from you.** The decision names it *"Core Query Repetition & Assembly Logic"*, which is narrower than the §2.1 proposal (the whole `CSQEEnhancer` batch path, ~150 lines). Two readings:
- **Narrow (~60 lines):** `batch_enhance()` only — prompt assembly, the four generation calls, and the `(query + ' ') * alpha + ' '.join(all_exps)` line. Matches the wording and keeps Appendix C tight.
- **Full (~150 lines):** adds `get_retrieved_docs()` and `batch_generate()` — the batching/padding machinery.
**Recommendation: narrow.** It contains the α=4 assembly that is the actual claim; the batching is engineering. D3 defaults to narrow unless told otherwise.

---

## 1. Page budget math

### 1.1 The measurement

Taken from the committed `1-main.pdf`'s **own embedded table of contents** (PDF sheets 9–12), cross-checked by rendering the chapter-opening pages. Printed page = PDF sheet − 19 throughout.

| Chapter | Starts (printed) | Ends | Pages |
|---|---|---|---|
| 1 Introduction | 1 | 6 | 6 |
| 2 Theoretical Background and Literature Review | 7 | 36 | 30 |
| 3 Methodology | 37 | 61 | 25 |
| 4 Results and Discussion | 62 | 96 | **35** |
| 5 Conclusion and Recommendations | 97 | 105 | 9 |
| **Core (Ch. 1–5)** | **1** | **105** | **105** |
| Bibliography | 106 | 112 | 7 (does not count) |

**Verification performed** (because three different numbers were in circulation):
- Rendered PDF sheet 20 → prints "Chapter 1 / Introduction", footer **1**. ✔
- Rendered PDF sheet 116 → prints "Chapter 5 / Conclusion and Recommendations", footer **97**. ✔
- The PDF's embedded ToC line reads `Bibliography …… 106`. ✔
- `pdfinfo` reports **131 pages**; 131 − 19 front-matter sheets = 112 arabic pages = 105 core + 7 bibliography. ✔ Internally consistent.

### 1.2 Why three numbers exist (so this does not happen again)

| Source | Says | Why it is wrong |
|---|---|---|
| **E1** (2026-07-30) | 97 core | Read `1-main.toc`, `.lof`, `.lot` — build artefacts from a **20:34 run (122 pages)**. The PDF committed alongside them is from a **22:38 run (131 pages)**. The `.toc` is ~5 pages stale and still carries the pre-rename section title "4.5 Key Findings and Analysis" where the PDF reads "4.5 Cross-Cutting Findings from the Model Comparison". |
| **D1** (2026-07-29) | 103 core | Right method, slightly earlier build; its chapter starts (2→7, 3→36, 4→60, 5→95) track the PDF's (7, 37, 62, 97) with a 0–2 page drift. Closest of the three. |
| **This report** | **105 core** | The committed PDF's own ToC, plus rendered pages. |

> **Process note for the team:** `1-main.toc`/`.lof`/`.lot` are committed but are **not** guaranteed to match the committed `1-main.pdf`. Measure page counts from the PDF, never from the `.toc`.
>
> A local rebuild was attempted as an independent check and **discarded as unusable**: this machine has no Arabic shaping available to XeLaTeX, so every Arabic character is dropped (`Missing character: There is no ك in font [lmroman12-regular]`), producing a shorter, invalid document. Any future page-count check must be run on a machine (or Overleaf) that renders Arabic.

### 1.3 The gap

| | Pages |
|---|---|
| Current core | **105** |
| Limit | 100 |
| **Over by** | **5** |
| Target with ~5-page margin | ≤ 95 |
| **Must free** | **≈ 10 pages** |

E1's already-approved high-confidence figure drops supply **≈3.2**. This report must find **≈7 more**. §5 shows it adds up to ≈10.6 without touching a single result.

---

## 2. CODE appendix plan

### 2.1 Recommended snippets

> **SUPERSEDED — see §0.5.** Only **CODE-1, CODE-2 (narrow), CODE-3** survived review, plus the new CODE-P. CODE-4 through CODE-9 were excluded and are repo-only. The table is kept as the record of what was considered and why.

Ordered as they should appear (pipeline order). "Lines" = source lines now → estimated lines after stripping `print()` diagnostics, Colab paths, and banner comments.

| ID | Source | What it shows | Lines | Why it earns appendix space |
|---|---|---|---|---|
| **CODE-1** | `experiments/exp_013_csqe_aya_8b.ipynb` **cell 10** | `BLIND_SYSTEM`, `CSQE_SYSTEM`, `CSQE_ONE_SHOT`, `build_csqe_prompt()`, `build_blind_prompt()` | 73 → **~62** | The literal implementation of §3.8.1's "CSQE System Prompt" paragraph **and** of the one-shot disclosure at `chapter3.tex:452`. The thesis states it is zero-shot everywhere *except* CSQE, which uses one English worked example — this is the only place a reader can check that claim. Highest-value snippet in the appendix. |
| **CODE-2** | same notebook, **cell 12** (`class CSQEEnhancer`) | `get_retrieved_docs`, `batch_generate`, `batch_enhance` | 233 → **~150** | Contains the headline claim in one line: `final = (queries[i] + ' ') * alpha + ' '.join(all_exps)` — the α=4 repetition + 2c+2b concatenation that produces 0.7137. Recommend **dropping the sequential `generate_samples`/`enhance` path** (~60 lines): it exists only for the 5-query sanity check and produced none of the reported numbers. |
| **CODE-3** | same notebook, **cell 5** (`CONFIG`) | k=5 first-pass, 128-token doc truncation, temp 1.0, top_p 0.9, 2 corpus + 2 blind, α=4, batch sizes | 42 → **~28** | Every hyperparameter §3.8.1 asserts, in one auditable block. This is what a committee member checks first when asked "what exactly did you run?". |
| **CODE-4** | same notebook, **cells 8 + 9** | first-pass loading, `parse_docid()`, `truncate_to_tokens()` | 57 → **~40** | Stage 1 of the pipeline + the 128-token truncation the caption of Fig 3.6 quotes. ⚠️ **Honest caveat for D3:** cell 8 as written *loads a cached pickle* of the first pass, it does not run BM25. Printed alone it would misrepresent the method. Pair it with the `search()` method from CODE-8, or add a one-line comment saying the cache was produced by that call. |
| **CODE-5** | `experiments/phase4_quick_wins (1).ipynb` **cell 8** | `normalize_scores_minmax()`, `fuse_cc()`, `fuse_rrf()`, `truncate_top_k()` | ~70 | The two fusion equations of §2.2.3 as executed. RRF *k*=20 on these ~40 lines is the best system in the thesis. Explicitly named in the meeting as appendix material. |
| **CODE-6** | same cell | `build_repeated_queries()`, `build_adaptive_queries()` | ~25 | The MuGI adaptive formula printed in Table 4.12's caption, `n = max(1, ⌊\|d\|/(\|q\|·β)⌋)`, verbatim. Cheap, and it makes Table 4.12 (which TAB-2 moves to the appendix) self-contained beside it. |
| **CODE-7** | `src/evaluation/metrics.py` L11–98 + L101–122 | `RetrievalEvaluator` (`evaluate`, `evaluate_per_query`), `save_results` | ~90 → **~70** | Every number in Chapter 4 came through this class. It also settles the caveat in Table 4.23's caption: `evaluate()` returns a **mean over per-query scores**, `evaluate_per_query()` does not aggregate — which is precisely the 0.6936-vs-0.7137 distinction the caption has to explain in four lines of prose. Include the exact metric strings (`ndcg_cut_10`, `recall_10`, `recall_100`, `recip_rank`). |
| **CODE-8** | `src/retrievers/bm25.py` L82–132 + `src/retrievers/dense.py` L58–133 | `BM25SRetriever.search()`, `DenseRetriever.encode_queries()` / `.search()` | ~100 → **~80** | Reproduces §3.2.1/§3.2.2: query batch size 64, top-100, FAISS, Arabic stemmer + stopword list. Both baselines and every experiment sit on these two methods. |
| | | **Total** | **≈ 525** | |

**Optional, recommended if space allows:**

| ID | Source | Lines | Rationale |
|---|---|---|---|
| **CODE-9** | `src/enhancers/query2doc.py` — `enhance_batch_parallel()` only (L129–194) | ~65 | §3.4.4 and the Chapter 5 conclusion both claim batching cut generation from "an estimated eight hours to approximately forty minutes per model". That is a stated efficiency result with no evidence anywhere else in the document. Include the method only, not the whole 245-line class. |

### 2.2 Notable exclusions — repo-only

| Excluded | Size | One-line reason |
|---|---|---|
| `src/enhancers/contrastive_hyde.py` + `src/retrievers/contrastive_dense.py` | 517 lines | **Contrastive HyDE is not in the thesis.** Grep of Ch.1–5 finds only generic "contrastive learning" (ch2:72) and HyDE's encoder (ch2:89) — our exp_005 contrastive line of work is never reported. Printing it would raise a question the thesis does not answer. *(Also a flag for D4: consider excluding from the clean repo.)* |
| 11 × `Query_generator_*.ipynb` | ~11 notebooks | Near-identical per model; the only differences (temperature, dtype, `token_type_ids`, `enable_thinking`) are already stated in Table 3.2 and §3.5.4. Printing 11 variants of one loop is exactly the bloat Dr. Tahani is trying to remove. |
| `src/analysis/analyze_exp001_quantitative.py` | 467 lines | Longest file in the repo; produces §4.2's descriptive statistics. Mechanical, and every output number is already tabulated. |
| Plotting cells (`phase4_*` cells 34–38, 68–75; `thesis_figures/` notebooks) | ~400 lines | matplotlib boilerplate. The figures *are* the output; the code adds nothing a reader can check. |
| Colab plumbing — `git clone`, `drive.mount`, `huggingface_hub.login` (cells 1–4 of every notebook) | ~70 lines each | Environment setup, not method. Belongs in the repo README. |
| `src/utils/data_loader*.py`, `extract_query.py`, `test_analysis.py` | ~230 lines | Dataset I/O and scratch scripts. |
| `exp_013_ablations.ipynb` cells 14–22 (`CONFIG_C`, `CONFIG_D`) | ~120 lines | The 4c+0b / 0c+4b ablations are two config dicts differing from CODE-3 by two integers. Cover in one sentence of the appendix text instead. |

### 2.3 Recommended LaTeX mechanism

**Use `listings`, not `minted`.** `minted` needs `-shell-escape` and a Pygments install — an extra failure mode on a document that already only builds correctly on some machines. `listings` is pure TeX and works fine under XeLaTeX.

Minimal setup for `1-main.tex` (goes **before** `hyperref`):

```latex
\usepackage{listings}
\lstdefinestyle{thesiscode}{
  language=Python,
  basicstyle=\footnotesize\ttfamily,
  keywordstyle=\bfseries,
  commentstyle=\itshape,
  numbers=left, numberstyle=\tiny, numbersep=6pt,
  breaklines=true, breakatwhitespace=true,
  showstringspaces=false,
  frame=single, framerule=0.3pt,
  aboveskip=1em, belowskip=1em,
  columns=fullflexible, upquote=true,
}
\lstset{style=thesiscode}
```

**Four gotchas D3 must handle — all verified against this document, not generic advice:**

1. **`\setstretch{1.5}` is global** (`1-main.tex:18`). Listings inherit it and code will double-space, inflating the appendix by ~50%. Wrap each listing in `\begin{spacing}{1}…\end{spacing}` (the `setspace` package is already loaded).
2. **Non-ASCII characters in the source will break the build.** The proposed cells contain box-drawing banners (`── Helper functions ──`), `×`, `α`, `→`, and em-dashes inside comments. `listings` under XeLaTeX chokes on these unless mapped. **Simplest fix: sanitise the comments to ASCII when extracting** — these are decorative separators, nothing is lost. Do not rely on `extendedchars`/`literate` for a one-off.
3. **`\appendix` will print "Chapter A".** `1-main.tex:40-45` hardcodes the label: `\titleformat{\chapter}[block]{…}{Chapter \thechapter}{0pt}{…}`. After `\appendix`, `\thechapter` becomes `A`. D3 must re-issue `\titleformat` with `Appendix \thechapter` after the `\appendix` command, **and** redefine `\chaptermark` (line 32, currently `Chapter \thechapter\ - #1`) or every appendix running header will read "Chapter A - …".
4. **Long lines exceed the 1-inch-margin text block.** `breaklines=true` is not optional here — `CONFIG` values and the `CSQE_ONE_SHOT` string both run long.

### 2.4 Appendix page estimate

> **SUPERSEDED — see §0.5.** With only four snippets the code appendix is **≈4 pp (narrow CODE-2) or ≈6 pp (full)**, not 12. It is now **Appendix C**, not A. The line-per-page calibration below still holds and is what those figures are derived from.

Text block is 700.5 pt tall. At `\footnotesize` (10 pt on a 12 pt baseline) with single spacing that is ~58 lines/page; allow ~50 after frames, section headings and the one-paragraph intro each snippet needs.

| | |
|---|---|
| Code lines (CODE-1…8) | ≈ 525 |
| + CODE-9 if accepted | ≈ 590 |
| Pages of code @ ~50 lines/page | ≈ 10.5 (11.8 with CODE-9) |
| + section headings, intros, repo link | ≈ 1.5 |
| **Appendix A total** | **≈ 12 pages** (≈ 13 with CODE-9) |

Appendix pages do not count toward the 100. This is free space — but it is not free *reader attention*, which is the argument for the exclusions in §2.2.

---

## 3. TABLE moves

Page numbers below are from the committed PDF and **supersede E1's** (which run ~5 pages early for the reason in §1.2). E1's *size fractions* were computed geometrically and remain valid; only the locations shifted.

### 3.1 The two tables named in the meeting

**TAB-1 · Table 4.26 — Big-win Arabic query examples** (p. 93) → **Appendix B**
- **Current size:** measured by rendering p. 93 — **≈55% of the page** (E1 estimated 38%; the render shows more, because the three Arabic/English/Arabic cells wrap to 5–7 lines each in `p{3.4cm}` columns).
- **Content:** 3 rows × 4 columns. Arabic query + gloss, what blind QE hallucinated, what CSQE grounded to, score 1.000.
- **This is the "Table 4.26" from the meeting** — confirmed, the label is `tab:bigwin_examples` and the LoT caption reads "Representative big-win queries illustrating the corpus grounding effect".
- **Inline stub recommended:** keep **one** example, in prose, not a table. §4.10.3's surrounding paragraph already narrates the al-Ribat al-Mansuri case in full ("the corpus anchor supplied the correct Arabic vocabulary … rather than the surgical terms"). One sentence + a pointer to Appendix B loses nothing.
- **Saving: ≈0.40 page net** (0.55 out, ~0.15 for the stub sentence).

**TAB-2 · "The full model-comparison table"** → **needs disambiguation, see ⚠️-1**
The meeting phrase maps to three different tables. Recommendation per candidate:

| Candidate | Where | Size | Verdict |
|---|---|---|---|
| **Table 4.12** — BM25 repetition, full 9×8 grid | p. 78 | ≈0.42 pg | **MOVE to Appendix B.** Reference data, not argument. Fig 4.8 carries the shape and Table 4.13 carries each model's best config with all four metrics. Already E1's `APPENDIX-CANDIDATE`. **Saving ≈0.42.** |
| **Tables 4.8 + 4.9** — dense / BM25 leaderboards | pp. 71, 72 | ≈0.28 + 0.27 | **KEEP inline.** These *are* the model-comparison result, and E1's plan already deletes Figs 4.5/4.6 on the grounds that Table 4.8 is the better artefact — moving 4.8 out would leave §4.4.1 with neither. |
| **Table 4.28** — Summary of all experiments | p. 96 | ≈0.50 pg **+ a page of whitespace** | **MOVE — see TAB-4, it is the strongest single case.** |

**Recommendation:** read "the full model-comparison table" as **Table 4.12**, and move Table 4.28 as well on independent grounds. Confirm with Elhaj.

### 3.2 Other tables over ~half a page, referenced but not essential inline

**TAB-3 · Table 4.14 — Hybrid fusion, full CC α-sweep** (p. 81) → **shrink; sweep rows to Appendix B**
- **Current:** 13 rows (2 baselines + 9 CC α values + 2 RRF), ≈0.42 page (rendered).
- Fig 4.10 already plots all four metrics across all nine α values, and E1 keeps that figure. The nine sweep rows are the figure in numeric form.
- **Inline stub (5 rows):**

  | Method | nDCG@10 | Recall@10 | Recall@100 | MRR |
  |---|---|---|---|---|
  | BM25S alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
  | mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
  | **Hybrid CC α = 0.5** (best CC) | **0.6266** | 0.7478 | 0.9458 | **0.6577** |
  | **Hybrid RRF k = 20** | **0.6267** | **0.7597** | **0.9466** | 0.6517 |
  | Hybrid RRF k = 60 | 0.6230 | 0.7553 | 0.9466 | 0.6490 |

  This preserves every number §4.7's five observations actually cite (the +35.6%/+25.5% deltas, the RRF-vs-CC tie, the k=20/k=60 comparison). Observation (c) — "smooth and unimodal, peaking at α=0.5, degrading symmetrically", with the α=0.9 and α=0.1 endpoints — must then cite Fig 4.10 and Appendix B instead of the table.
- **Saving ≈0.24 page.** (E1 estimated 0.20; same call.)

**TAB-4 · Table 4.28 — Summary of all experiments** (p. 96) → **Appendix B** ⚠️ *conflicts with E1, see below*
- **Current:** 17 data rows + 3 group rows, ≈0.50 page — **and it is the only float on p. 96**, sitting under ~40% of a page of whitespace because `[htbp]` pushed it down. The section's closing paragraph is the only other content. Removing it substantially empties the page.
- **It is also broken:** the `Status` column runs past the right text margin in the compiled PDF — "Baselin", "Best no-C", "Droppe", "Best BM25", "Best ove" are clipped mid-word. A `tabularx`/`\small` fix is needed *anyway*; doing it in an appendix (where a landscape or full-width layout is acceptable) is easier than in the main text.
- **The conflict:** E1's action list has `DELETE tab:system_progression (Tab 4.22)` on the grounds that all its rows recur in Table 4.28. If Table 4.28 also leaves the main text, the progression numbers vanish from Ch. 4 entirely.
- **Proposed resolution — pick one, do not do both blindly:**
  - **(a) Recommended.** Move Table 4.28 → Appendix B; **keep Table 4.22 inline** (7 rows, ≈0.30 page — it is the progression narrative §4.9.2 needs). Net saving **0.50**, and Fig 4.11 + Table 4.22 keep telling the 0.462 → 0.714 story inline. E1's saving of 0.30 from dropping 4.22 is forgone.
  - **(b)** Keep E1 as written (drop 4.22, keep 4.28 inline) and fix the overflow in place. Saving 0.30, and §4.11 stays as a real chapter-closing section.
  - Net difference is only 0.2 page — **decide on narrative grounds, not page grounds.** (a) reads better: a "Summary of all experiments" is a reference artefact, which is what an appendix is for.

**TAB-5 · Table 2.3 vs Table 2.4 — near-duplicate model tables** (pp. 21 and 27) → **merge, one goes**
- Inherited from E1 §5.6 as a hand-off, not a verdict. Both list the same 10 models 6 pages apart in the same chapter; overlapping columns (params, Arabic focus, multilingual coverage). Table 2.4 additionally carries Developer, Architecture and Licence — including the CC-BY-NC flag that Ch. 5's licence caveat depends on.
- ~~**Recommendation: keep Table 2.4** (the superset, and the licence column is load-bearing), **drop Table 2.3**~~
- 🔄 **DECIDED — REVERSED (2026-08-02): keep Table 2.3 inline, move Table 2.4 → Appendix A.1.** Saving **≈0.35 page** (slightly more than the original recommendation, since Table 2.4 is the larger of the two).
- ⚠️ **The licence column goes with it — see ⚠️-A in §0.5.** `chapter2.tex:286` asserts a licence selection criterion and `chapter5.tex:51` raises Aya's CC-BY-NC as a named Challenge; Table 2.4 is the only table carrying a `License` column, and MISC-1 simultaneously moves the per-model prose that states individual licences. **D3 must add a `License` column to Table 2.3** in the same edit. `\ref{tab:model_comparison}` (`chapter2.tex:394`) must be repointed at Appendix A.1; `\ref{tab:models_used}` is unaffected.
- ⚠️ Table 2.1 (p. 14, QE papers reviewed) **also overflows the right margin** — its rules extend past the text block. Not an appendix candidate (13 rows of literature at `\scriptsize`, ≈0.45 page, and it is the evidence for §2.5's gap claim) — but it needs a width fix in E3.

### 3.3 Tables explicitly NOT recommended for the appendix

| Table | Why it stays |
|---|---|
| 4.8, 4.9 (leaderboards) | The model-comparison result itself; E1 deletes Figs 4.5/4.6 *because* these tables are better. |
| 4.13 (best repetition config) | The payoff row-set of §4.6; 4.12 moves, 4.13 stays. |
| 4.15, 4.16, 4.17 (CSQE main + ablations) | The contribution. Small (0.17–0.24 pg each). |
| 4.18, 4.19, 4.20 (fusion strategies) | The asymmetric-placement finding — the thesis's most novel claim. |
| 4.23–4.27 (error analysis) | Each ≈0.22 pg and each is the sole source of its numbers. (4.26 excepted — TAB-1.) |
| 3.1, 3.2 (generation params) | Method disclosure; a committee expects these inline. *(Note: H1/H2/H3 corrections to Table 3.2 are still open and unrelated to D2.)* |

---

## 4. Other oversized main-text material

**MISC-1 · §2.4.1–2.4.2 per-model descriptions → Appendix C** ⭐ *biggest single lever*
- **What:** ten `\subsubsection` blocks, one per LLM (`chapter2.tex:288–364`), **1,499 words** — Falcon-H1 187, Jais-2 181, ALLaM 181, Qwen3-4B 157, Qwen 2.5 3B 124, Aya 112, SILMA 103, Gemma 103, Qwen 2.5 7B 78, Qwen3-8B 66. At this document's density (12 pt, 1.5 spacing, ≈330 words/full page) that is **≈4.5 pages**; §2.4 as a whole spans pp. 20–27 = 8 pages.
- **Why it qualifies:** this is the literal definition of an "exhaustive per-model listing". It is also *narratively* stale — task A2 removed model-characteristics analysis from the research question, and A5 swept the thesis for framing that presents small models as the contribution. Eight pages of model biographies in Chapter 2 is the largest surviving remnant of the old framing.
- **Proposed replacement inline:** keep Table 2.4 (the 10-model summary with params/architecture/Arabic focus/licence) + **one short paragraph per group** (Arabic-specialised / multilingual) stating the selection logic and naming the models — ≈1 page. Keep §2.4.3 (mDPR, BM25S — 207 words) inline: those are the retrievers, not candidates.
- **Saving ≈3.5 pages net.**
- ⚠️ This is the most intrusive item in the report and the one most likely to need Dr. Tahani's blessing, because it moves *prose* rather than data. Her directive named "large code snippets, detailed proofs, and raw extra data tables". Per-model spec sheets are arguably "raw extra data"; they are arguably background prose. **Recommend asking her directly** — the payoff (3.5 of the 10 pages we need) justifies one question.

**MISC-2 · §3.5.4 Model-Specific Technical Issues → Appendix C** (pp. 51–52)
- Five per-model engineering bugs — Falcon-H1's attention-mask batching bug, Jais-2's BF16/Squared-ReLU and `token_type_ids`, Qwen3's `enable_thinking=False`, ALLaM's sentencepiece `▁` leak. ≈1 page.
- Genuinely valuable (it is hard-won and reviewers like it) but it is engineering trivia about models the thesis no longer claims as its contribution. ALLaM's tokenizer bug must stay reachable because §4.4.3 explains the −48.9% collapse with it — an appendix cross-reference is enough.
- **Saving ≈0.8 page net** (leave a two-sentence pointer).

**MISC-3 · §3.5.5 Quantisation Strategy — NOT recommended for moving**
- Three bullets + a paragraph, ≈0.4 page. Small, and it carries the defensible claim that 4-bit Aya still won. Flagged only to record that it was considered.

**MISC-4 · Nothing else qualifies.** Ch. 1 and Ch. 5 contain zero floats (E1) and no oversized blocks. Ch. 4's §4.5 cross-cutting findings (pp. 74–78) are prose-heavy and a plausible D5 trim target, but they are *analysis*, not raw data — **out of D2's remit, handed to D5.**

---

## 5. Final recommendation

### 5.1 Appendix structure — AS DECIDED

```
Appendix A — Model Details                                        ≈ 6 pp
  A.1  Summary of language models        (Table 2.4)      [TAB-5, reversed]
  A.2  Per-model descriptions            (§2.4.1-2.4.2)   [MISC-1]
  A.3  Model-specific technical issues   (§3.5.4)         [MISC-2]

Appendix B — Extended Result Tables                               ≈ 3 pp
  B.1  BM25 query repetition: full 9 x 8 sweep       (Table 4.12)  [TAB-2]
  B.2  Hybrid fusion: full CC alpha-sweep            (Table 4.14)  [TAB-3]
  B.3  Summary of all experiments                    (Table 4.28)  [TAB-4a]
  B.4  Representative big-win queries                (Table 4.26)  [TAB-1]

Appendix C — Implementation Code                                  ≈ 4-6 pp
  C.1  CSQE system prompt and one-shot construction   CODE-1   ~62 L
  C.2  Query expansion system prompt                  CODE-P   ~15 L   [CUT-P]
  C.3  CSQE query repetition and assembly logic       CODE-2   ~60 L (narrow)
  C.4  CSQE configuration and hyperparameters         CODE-3   ~28 L
  C.5  Source code repository                         -> D4 link  [load-bearing, see WARN-B]
```

*Appendix C at ~165 lines (narrow CODE-2) ≈ 4 pp; at ~255 lines (full CODE-2) ≈ 6 pp.*

### 5.2 Projected core page count — AS DECIDED

| Stage | Δ | Core |
|---|---|---|
| **Now** | | **105.0** |
| E1 high-confidence figure drops — **minus the Table 4.22 delete, which TAB-4a cancels** | −2.90 | 102.1 |
| TAB-1 Table 4.26 → B.4 | −0.40 | 101.7 |
| TAB-2 Table 4.12 → B.1 | −0.42 | 101.3 |
| TAB-3 Table 4.14 shrink → B.2 | −0.24 | 101.0 |
| TAB-4a Table 4.28 → B.3 (Table 4.22 kept inline) | −0.50 | 100.5 |
| **TAB-5 (reversed)** Table 2.4 → A.1, Table 2.3 kept inline | −0.35 | 100.2 |
| MISC-1 §2.4 per-model prose → A.2 | −3.50 | 96.7 |
| MISC-2 §3.5.4 → A.3 | −0.80 | 95.9 |
| **CUT-P** prompt quote blocks → C.1/C.2 | −0.15 | **95.7** |
| E1 medium-confidence set (Fig 4.3; Table 4.4 → prose) | −0.66 | **95.1** |
| **D5 conciseness pass** | not estimated here | **< 95** |

**≈ 95.7 pages after D2 + E1 — 4.3 under the limit before D5 does any work.** With D5, a 6–8 page margin is realistic.

*Arithmetic note: TAB-5's reversal is worth slightly more than the original recommendation (Table 2.4 ≈0.35 page vs Table 2.3 ≈0.30), so the projection improved from 96.0 to 95.7 despite nothing else changing. E1's medium set is counted as 0.66, not its stated 1.3 — its other two items (Tables 4.12 and 4.14) are already counted as TAB-2/TAB-3 and must not be double-counted.*

### 5.3 Execution order for D3

All items are approved, so this is a sequencing aid rather than a triage list. Front-loaded by payoff and by how many other edits each one touches:

| # | Item | Δ | Running | Note |
|---|---|---|---|---|
| 1 | **E1 high-confidence figure drops** | −2.90 | 102.1 | Already analysed; **skip E1's Table 4.22 delete** — TAB-4a keeps it |
| 2 | **MISC-1** §2.4 prose → A.2 | −3.50 | 98.6 | Biggest single move; do with TAB-5 (same section) |
| 3 | **TAB-5** Table 2.4 → A.1 | −0.35 | 98.3 | **Add a License column to Table 2.3 in the same edit** (⚠️-A) |
| 4 | **TAB-4a** Table 4.28 → B.3 | −0.50 | 97.8 | Fix the width when placing it in the appendix |
| 5 | **TAB-2** Table 4.12 → B.1 | −0.42 | 97.3 | |
| 6 | **TAB-1** Table 4.26 → B.4 | −0.40 | 96.9 | Write the al-Ribat al-Mansuri stub |
| 7 | **MISC-2** §3.5.4 → A.3 | −0.80 | 96.1 | Leave the ALLaM pointer — §4.4.3 depends on it |
| 8 | **TAB-3** Table 4.14 → 5-row stub | −0.24 | 95.9 | Repoint §4.7 observation (c) at Fig 4.10 + B.2 |
| 9 | **CUT-P** prompt blocks → C.1/C.2 | −0.15 | **95.7** | Keep a one-clause description of each prompt's intent |

**We are under 100 after step 2.** Steps 3–9 are margin.

---

## 6. Sign-off sheet — CLOSED 2026-08-02

All items reviewed by Osman + Elhaj. ✅ = approved as proposed · 🔄 = approved with modification · ❌ = rejected.

**Code appendix (→ D3)**

| ID | Item | Outcome |
|---|---|---|
| CODE-1 | CSQE prompts + one-shot example (~62 L) | ✅ → C.1 |
| CODE-P | **NEW** Query expansion system prompt, moved out of Ch.3 (~15 L) | ✅ → C.2 |
| CODE-2 | CSQE query repetition + assembly logic | 🔄 → C.3 — **narrow reading (~60 L)**, see ⚠️-C |
| CODE-3 | CSQE `CONFIG` block (~28 L) | ✅ → C.4 |
| CODE-4 | First-pass + truncation | ❌ repo-only |
| CODE-5 | RRF + CC fusion | ❌ repo-only — **reverses the meeting's "retrieval/fusion pipeline", see ⚠️-B** |
| CODE-6 | Query repetition helpers | ❌ repo-only |
| CODE-7 | `RetrievalEvaluator` / pytrec_eval | ❌ repo-only |
| CODE-8 | BM25S + mDPR `search()` | ❌ repo-only |
| CODE-9 | `enhance_batch_parallel()` | ❌ repo-only |
| CODE-X | Exclusion list in §2.2 | ✅ (now larger — CODE-4…9 join it) |
| CODE-L | `listings` + the four fixes in §2.3 | ✅ — all four still apply |

**Table moves (→ D3 / D5)**

| ID | Item | Δ pg | Outcome |
|---|---|---|---|
| TAB-1 | Table 4.26 → B.4, stub example kept in prose | −0.40 | ✅ |
| TAB-2 | Table 4.12 → B.1 | −0.42 | ✅ |
| TAB-3 | Table 4.14 → 5-row stub, sweep to B.2 | −0.24 | ✅ |
| TAB-4a | Table 4.28 → B.3, **keep Table 4.22 inline** *(overrides E1)* | −0.50 | ✅ **adopted** |
| TAB-4b | *Alternative:* keep E1 as written | −0.30 | ❌ not taken |
| TAB-5 | ~~Drop Table 2.3, keep Table 2.4~~ | −0.35 | 🔄 **REVERSED — keep Table 2.3 inline, move Table 2.4 → A.1.** See ⚠️-A |
| CUT-P | **NEW** — prompt quote blocks out of Ch.3 → C.1/C.2 | −0.15 | ✅ |

**Other material (→ D3 / D5)**

| ID | Item | Δ pg | Outcome |
|---|---|---|---|
| MISC-1 | §2.4.1–2.4.2 per-model prose → A.2 | −3.50 | ✅ |
| MISC-2 | §3.5.4 → A.3, pointer left inline | −0.80 | ✅ |
| MISC-3 | §3.5.5 Quantisation Strategy | — | ✅ stays inline |

---

## 7. Open questions — RESOLVED 2026-08-02

1. ~~**What did "the full model-comparison table" mean?**~~ **RESOLVED.** Read as **Table 4.12**; Tables 4.8/4.9 stay inline. Table 4.28 moves on independent grounds (TAB-4a).
2. ~~**TAB-4a vs TAB-4b**~~ **RESOLVED: TAB-4a.** Table 4.28 → Appendix B, Table 4.22 stays inline in §4.9.2 so Ch.4 keeps the 0.4621 → 0.7137 progression. **E1's `DELETE tab:system_progression` line must be skipped when D5 runs its action list.**
3. ~~**MISC-1 needs Dr. Tahani**~~ **RESOLVED by team decision** — the per-model prose moves to Appendix A. *Recorded for transparency: this was flagged as a question for the supervisor because it moves background prose rather than code/proofs/data tables; the team took the call. Worth a one-line mention at the next supervision rather than a separate approval request.*
4. **The page-count record must be corrected — STILL OPEN.** D1's task entry states 103 and E1's states 97; the real number is **105**. Both entries should be annotated so nobody plans against a stale figure, and the rule "measure from the compiled PDF, never from `.toc`" recorded. *(Noted in D2's task entry; the D1 and E1 entries themselves are untouched.)*
5. **Margin overflows → E3.** **Table 4.28** — resolved by the move to Appendix B (set the width there). **Table 2.1 (p. 14)** — **confirmed overflow, still needs an inline `tabularx` or font-size fix.**
6. ~~**Possible third defect: Arabic `k-t-b` renders blank on p. 14**~~ — **FALSE ALARM, closed.** Verified in `1-main.pdf` §2.1.5: the root letters render correctly (`ك-ت-ب`). The blanks were an artefact of the page-image extraction used for sizing, not a defect in the thesis. **No fix needed.**

### Carried forward to D3

- **⚠️-A** — add a `License` column to Table 2.3 when TAB-5 is executed, or Ch.2/Ch.5's licence claims lose their inline evidence.
- **⚠️-B** — Appendix C's repo link (C.5) is now the only route to the retrieval/fusion code. It must be a real, working URL before submission (depends on **D4**).
- **⚠️-C** — CODE-2 defaults to the narrow (~60-line) reading unless Elhaj says otherwise.
- **CUT-P** — keep a one-clause statement of each prompt's intent inline; §3.8.1's extract-vs-generate argument and the one-shot disclosure at `chapter3.tex:452` depend on it.
