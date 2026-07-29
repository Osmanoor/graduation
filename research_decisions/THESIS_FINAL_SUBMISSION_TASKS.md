# Thesis Final Submission — Task List (July 2026)

**Created:** 2026-07-27, from the July review cycle.
**Sources:**
- `meetings/Thesis Review Report.md` — Dr. Tahani's answers to our 10 questions + her additional directives (recordings, arranged into this file).
- `meetings/video_1_text_July.md` + `meetings/video_2_text_July.md` — our two-part meeting discussing her feedback and remaining work.
- `research_decisions/THESIS_NEXT_STEPS_TASKS.md` — the previous task list (the 10 questions originated there; several of its supervisor-gated tasks are now unblocked).

**Team:** Elhaj (Mohammed Elhaj Sami) + Osman (Osman Bashir).

> **Note on assignments:** everything in the *task descriptions* is CONFIRMED (from the supervisor report or explicitly agreed in the meeting). The *owner column and phase ordering* are an **AI Suggestion** — the meeting did not assign owners; swap freely. Review this whole file per task G1.

---

## Supervisor questions — now ANSWERED (unblocks old tasks)

| Old open question | Dr. Tahani's answer | Old task now unblocked |
|---|---|---|
| Q1 — Chapter summaries? | Optional, **recommended to keep** | — (decision: keep) |
| Q2 — Problem statement general vs specific? | **Very specific**, funnel wide→narrow, single paragraph | 5.A.3 / 5.E.1 / 5.E.3 |
| Q3 — Technology-driven narrative OK? | **Yes, completely acceptable** | 5.E.1 / 5.E.3 |
| Q4 — Thesis Layout paragraphs or bullets? | **One single continuous paragraph** | 5.E.4 |
| Q5 — Abstract length? | **≈ 3/4 page** (250–350 words), never > 1 page | 5.F.1 / 5.F.4 |
| Q6 — "33 cross-reference labels"? | Not addressed in this round | covered anyway by old 4.16 (figure-gated) |

Still figure-gated from the old list: **4.16** (dead labels) + **5.C.5** (Ch.4 table audit) + **Fig 4.2/4.3/4.4 regeneration** (thesis text is ahead of these figures). Folded into Phase E below.

**Tags:** `[AI]` = task is designed to be run as its own Claude chat/prompt (our agreed approach: split tasks, one chat each). `[JOINT]` = both review the output. Effort: S < 1h, M = half-day, L = multi-day.

---

## Phase A — Core narrative rewrite (cross-cutting — DO FIRST)

> The meeting's key realization (video 2, 37:35): the problem statement still centers on "small open-source LLMs," but our actual contribution became CSQE + asymmetric hybrid fusion. Elhaj: *"دي ممكن تكون أكبر غلط حالياً في التزيس."* This is the **only cross-cutting task cluster** (video 2, 43:10) — everything it touches (Ch.1, abstract, conclusion) should stabilize before the abstract rewrite and the final conciseness pass.

- [x] **A1 — Rewrite the Problem Statement** — **Owner: Elhaj** `[AI]` (L) — **DONE 2026-07-29**
  One single continuous paragraph (even if long), highly specific, funnel from wide (Arabic IR/RAG recall challenges) to narrow (the exact problem: short-query information poverty / vocabulary mismatch), ending with the exact thesis problem. **Content reframe:** center it on query enhancement for Arabic retrieval with our final pipeline (CSQE + hybrid fusion) as the answer — drop "small open-source models" as the headline framing. *(Report §2, §3; video 1 §2/§5; video 2 37:35–43:10. Closes old 5.A.3.)*

- [x] **A2 — Fix the central research question** — **Owner: Elhaj** (S) — **DONE 2026-07-29**
  Remove *"and what model characteristics determine effectiveness"* — we explicitly de-scoped model-characteristics analysis. Refocus the RQ on how far LLM-based query enhancement (blind + corpus-steered) can improve Arabic retrieval. Any RQs elsewhere must map back to the single problem statement. *(Video 1 §6; Report §3.)*

- [x] **A3 — Introduction funnel structure** — **Owner: Elhaj** `[AI]` (M) — **DONE 2026-07-29**
  The whole Introduction section should follow the funnel: open broad, progressively narrow, arrive at the problem statement as its natural endpoint. *(Report §2; video 1 §4.)*

- [x] **A4 — Rewrite the Objectives** — **Owner: Elhaj** `[AI]` (M) — **DONE 2026-07-29** (9 objectives, 1:1 with experiments; hybrid baseline + per-query error analysis now anchored)
  Clear, explicit, **measurable** goals — one per thing we actually experimented on (we counted ~8: model comparison for QE, BM25 query repetition, hybrid fusion, CSQE, asymmetric fusion configs, error analysis, …). Exploratory origin is fine (confirmed), but each written objective must state what was tested/evaluated/achieved so it can be **checked off in the conclusion**. *(Report §5; video 2 01:45–03:37.)*

- [x] **A5 — Small-models de-emphasis sweep** — **Owner: Elhaj** `[AI]` (M) — **DONE 2026-07-29** (Opus agent sweep: 55 occurrences, 41 KEEP / 14 FIX, all 14 applied; full audit + borderline calls in `research_decisions/A5_small_models_sweep_report.md`)
  Review the whole thesis (Ch.1 and Ch.5 especially) for leftover framing that presents small models as *the* contribution; align with the new statement/objectives. *(Video 2 38:25 — "محتاجين نعمل Review للبحث كله".)*

- [ ] **A6 — Cascade check: Conclusion** — **Owner: Elhaj** (S) — *prep ready: A5 report §(d) has the Ch.5↔9-objectives mapping + 3 drafted paragraphs (Obj 3 engineering, Obj 8 ablation, Obj 9 per-query analysis); verify the 1,061 count collision (ch4 L832 vs L876) and the §4.2 canonical error-analysis numbers before applying*
  After A1–A4, verify the Conclusion (and anywhere echoing the old statement) answers the *new* problem statement. Methodology/Results are expected to be unaffected (video 1 §5) — confirm rather than assume.

> **Phase A review flags (2026-07-29, from the A1–A4 session — decide at Elhaj's read-through):**
> 1. **§1.1 closing sentence detail** — it currently pre-announces the empirical finding ("asymmetric hybrid sparse–dense fusion, expansion applied to the sparse retriever only"). AI recommendation: keep the pipeline announcement (technology-driven framing is sanctioned) but drop the "asymmetric / sparse-side-only" specificity — that is a Chapter 4 *result*, and Objective 9 already poses it honestly as an open question.
> 2. **The word "small" in the objectives** — removed in A4; scope is now carried numerically ("openly available LLMs spanning 2–8 billion parameters"). Optional: reinstate once, e.g. Objective 4 → "small, openly available LLMs (2–8 billion parameters)". Numeric range carries the content; the word adds emphasis only. Safe anywhere except the RQ and the problem-statement endpoint.
> 3. **First-mention re-audit (Ch.2/Ch.3)** — acronym definitions moved into Ch.1 during the merge of the C3 sweep with the A1–A4 rewrite; later chapters may hold duplicates/orphans. Fold into E3/A7.
> 4. **Osman to review the 9-objective structure** (was ~8 in the meeting count) — per G1.

- [ ] **A7 — AI audit of the 1-to-1 mapping** — **Owner: JOINT** `[AI]` (S)
  Committee evaluates on strict mapping: Problem ↔ Objectives ↔ Methodology & Results ↔ Conclusions. Run a dedicated Claude check that every objective is addressed in methodology/results and checked off in the conclusion; fix gaps. *(Report §5; video 2 03:07 — "نستصحبها معانا مع الـ AI".)*

---

## Phase B — Abstracts (after Phase A)

- [ ] **B1 — Rewrite the English abstract** — **Owner: Elhaj** `[AI]` (M)
  Target ≈ 3/4 page (250–350 words); must fit one page; not shorter than half a page; Times New Roman 12, 1.5 spacing. Structure (use this as the AI prompt, as agreed): **Context/Area → Problem → Objectives → Methodology → Key Findings → Overall Conclusion.** Built on the new A1/A4 text. *(Report §8; video 2 07:20 + 36:30. Closes old 5.F.1.)*

- [ ] **B2 — Arabic abstract (المستخلص): shrink + Arabize** — **Owner: Osman** `[AI]` (M)
  Currently **1.5 pages → must become ≈ 3/4 page**. Re-derive from the new English abstract. Full Arabization of technical terms where standard equivalents exist (الاسترجاع الكثيف, التوليد المعزز بالاسترجاع (RAG)); Arabic term first + English acronym in parentheses at first mention; keep ASCII/Western numerals (0, 1, 2…). Self-review by both of us for terminology. *(Report §9; video 2 08:08–09:20. Closes old 5.F.4.)*

---

## Phase C — Structural & formatting fixes (independent — run in parallel with A)

> **2026-07-28:** Agent prompts for Osman's Wave-1 tasks (C1+C8, C2+C3, C6, C7) are ready in `research_decisions/OSMAN_WAVE1_PROMPTS.md`.

- [x] **C1 — Reorder front matter** — **Owner: Osman** (S) — **DONE 2026-07-28**
  Exact order: Title → Declaration of Authorship → Dedication → Acknowledgments → English Abstract → Arabic Abstract → Table of Contents → **List of Figures → List of Tables** → List of Abbreviations. *(Report Part 2A; video 2 33:45.)*
  **Done:** `1-main.tex:120-125` reordered to `\tableofcontents → \listoffigures → \listoftables → \include{7-ListofAbbreviations}`. Rebuilt PDF renders ToC viii → LoF xii → LoT xiii → Abbreviations xvi; compiles clean (0 errors).
  ⚠️ **CONFIRM WITH SUPERVISOR:** Dr. Tahani's order puts **List of Figures before List of Tables**, but the faculty `thesis Guidelines .pdf` (2018, "Preliminary Pages") lists **List of Tables before List of Figures**. We followed Dr. Tahani — confirm she is knowingly overriding the written guideline.

- [x] **C2 — Fill the List of Abbreviations** — **Owner: Osman** `[AI]` (S) — **DONE 2026-07-28**
  It is currently **empty** ("فاضية، ما اتملت"). Extract all abbreviations used in the thesis, sort **A→Z**. *(Report Part 2B; video 2 34:20.)*
  **Done:** `7-ListofAbbreviations.tex` rewritten — the two template placeholders ("Test Example"/"Another Example") removed, **64 entries** added, sorted A→Z, in the template's `\acro` bold-initials style (plain text where bolding is awkward: BF16, FP16, NF4, BM25S). `[LONGEST]` set to `[MS MARCO]` so the label column aligns. `MS~MARCO` and `TyDi~QA` use the `\acro{key}[short]{long}` form to keep spaces out of the internal key. Renders on pp. xvi–xviii.
  Also fixed two defects the filled list exposed: (a) the running header read **LIST OF TABLES** on the abbreviation pages (`\chapter*` never resets `\leftmark`) — added `\markboth{\MakeUppercase{List of Abbreviations}}{}`; (b) a **blank page xix** — the 64 entries filled p. xviii exactly, TeX broke at the list's closing negative penalty (`\@endparpenalty`), and `\clearpage`'s `\hbox{}` fallback then materialised the empty page. Fixed with `\itemsep`/`\parsep` `=0pt` inside the environment, which gives the list slack. Thesis is now **122 pages**, compiles clean (0 errors).
  ⚠️ **NOT included, expansions unverifiable:** ACQAD, 3C3H, Arabic-SQuAD (single mentions; I did not invent expansions — confirm before adding). Excluded by design: pure model/product names (Qwen, Jais, Aya, SILMA, Gemma, Falcon-H1, ALLaM, BGE-M3, E5, T4, A100…) and one-off cited-system names (GaQR, ThinkQE, QE-RAG, Exp4Fuse).
  ⚠️ **If entries are added later:** ~15+ more could refill p. xviii exactly and bring the blank page back; same two lengths (or trimming an entry) will clear it.

- [x] **C3 — First-mention rule sweep** — **Owner: Osman** `[AI]` (M) — **DONE 2026-07-28**
  Thesis-wide: first mention = full phrase + (ABBR); later mentions = abbreviation only. E.g. "Retrieval-Augmented Generation (RAG)". Audit + fix every acronym. *(Report Part 2B; video 2 34:20.)*
  **Done in two passes.** Pass 1 — added the missing first-mention expansions (~28 edits): HyDE, GRF, GPT-3, APIs, GPUs, BM25, MIRACL, mDPR (Ch.1); FAISS, QA, DCG, VRAM, SwiGLU, FP16, Squared-ReLU, BF16, AI, RMSNorm, SiLU, NF4, MAP (Ch.2); QLoRA, MS MARCO, NLTK (Ch.3); NLP, MTEB/MMTEB/STS (Ch.5). **`QE` was never defined anywhere in the thesis** — now defined at `chapter1.tex:9`. Also normalised `mAP`→`MAP`.
  Pass 2 — **strict enforcement per Osman's instruction (2026-07-28): each expansion appears exactly once, even where it costs readability.** 89 occurrences of "query enhancement" → `QE` across Ch.1–5, plus every repeated re-definition stripped to the bare abbreviation (LLM, RAG, MSA, HyDE, GRF, BM25, CSQE, MIRACL, mDPR, RRF, CC, SFT, OALL, NF4, QA). **Section headings and the ToC are included** — Osman's explicit call when asked. ToC now reads: `2.1.1 LLMs and the Transformer Architecture`, `2.1.2 RAG`, `2.1.4 QE Techniques`, `2.2.4.2 NDCG@k`, `2.2.4.3 MRR`, `2.4.3.1 mDPR`, `3.8 CSQE`, `4.8 CSQE Results`, `4.5.4 Dense vs. BM25 Behaviour with QE`.
  Verified by script: every expansion now occurs exactly once in Ch.1–5 and once in the standalone abstract (the abstract is read independently, so it carries its own first mentions). Untouched as scoped: `6-ARAbstract.tex` (task B2), the Ch.3 verbatim LLM prompt blocks, and generated files.
  ⚠️ **Side effect of including headings:** `NDCG` and `MRR` were previously defined *in* their §2.2.4.2/§2.2.4.3 headings. Those headings are now bare, so the definitions moved into the first body sentence below them — the only two places where an abbreviation precedes its own expansion. Reversible in one edit each if Dr. Tahani objects.
  ⚠️ **STILL OPEN — `nDCG` vs `NDCG` casing:** the thesis mixes 81 × `NDCG@10` with 46 × `nDCG@10` (Ch.3–5, incl. table/figure captions). The abbreviation list asserts one canonical form (`NDCG`), so this now reads as an inconsistency. **Not fixed** — it is a mass rewrite across captions and tables. Pick one form and sweep, ideally alongside E3.
  ⚠️ **Build noise (pre-existing, not from these tasks):** ~128 `Hyper reference 'acro:X' undefined` warnings — `acronym`+`hyperref` link list entries to targets only `\ac{}` creates, and the thesis never uses `\ac{}`. Verified the original placeholder file produced the same warning. One-line fix if wanted: `\usepackage[nohyperlinks]{acronym}` (`1-main.tex:78`).
  ⚠️ **Same header bug as C2 affects the abstract pages** (`\chapter*` again) — not fixed, one-line `\markboth` each.

- [ ] **C4 — Thesis Layout §1.3 → one single paragraph** — **Owner: Elhaj** (S)
  Currently one paragraph *per chapter*; must become **one single continuous paragraph** ("Chapter 2 establishes… Chapter 3 details… Chapter 4 reports…"). *(Report §6; video 2 03:37–04:20. Closes old 5.E.4.)*

- [ ] **C5 — Promote bold inline headings to numbered sub-headings** — **Owner: Elhaj** (M)
  Agreed in video 2 (06:10–07:20): §2.1.4 Query Enhancement Techniques → 2.1.4.1, 2.1.4.2, … (p.28) and §2.1.5 Arabic Language Processing Challenges → 2.1.5.1, 2.1.5.2, … (p.30). While there, audit for any other large section using bold-text pseudo-headings and apply the same. *(Report §7.)*

- [ ] **C6 — Citations: IEEE order-of-appearance + web access dates** — **Owner: Osman** `[AI]` (M)
  (a) Verify the bibliography style numbers references strictly in order of first appearance ([1], [2], [3]…) — Elhaj was unsure the LaTeX setup does this; check the .bst/biblatex config and the rendered PDF. (b) Every web reference must have full URL + explicit access date ("[Online]. Available: … [Accessed: …]"). *(Report Part 2C; video 2 34:20–35:30.)*

- [ ] **C7 — Verify caption placement** — **Owner: Osman** (S)
  Table captions ABOVE tables; figure captions BELOW figures. We believe this is already correct — verify every table/figure rather than assume. *(Report §10; video 2 25:28.)*

- [x] **C8 — Page-number placement consistency** — **Owner: Osman** (S) — **DONE 2026-07-28 (verdict: no change needed)**
  Video 2 (14:10): numbers appear top-of-page generally but bottom on chapter-start pages (and front-matter roman numerals looked odd on screen). This is standard LaTeX book behavior — confirm the template is consistent and matches faculty conventions; fix only if genuinely inconsistent.
  **Verdict:** the faculty `thesis Guidelines .pdf` "Pagination" section specifies only the numbering *scheme* (title page = page one but number not printed; lowercase roman before the body; arabic from Ch.1 p.1) — it says **nothing** about placement on the page. Top-right on normal pages / bottom-centre on chapter-start pages is standard `report`-class + `fancyhdr` behaviour and is compliant. **Nothing was changed.**
  ⚠️ **CONFIRM WITH SUPERVISOR:** one real gap vs. the written guideline — it says *"The Title page is considered to be page one… Roman numerals begin with the title"*, but `\pagenumbering{roman}` currently sits **after** the titlepage (`1-main.tex:114`), so the Declaration page becomes **i** instead of **ii**. One-line fix (move it above `\begin{titlepage}`), but it shifts every front-matter roman numeral. **Not applied** — ask whether she wants it.

- [ ] **C9 — Write the Dedication — DEFERRED to the very end** (Osman, 2026-07-28) — **Owner: Osman** (S)
  Currently needed for the front-matter order. Osman has prior poetic form (video 2 36:30 😄). Also confirm Declaration of Authorship + Acknowledgments pages exist for the C1 ordering.

- [ ] **C10 — Chapter summaries: keep (decision, verify) — DEFERRED until content edits settle** (Osman, 2026-07-28: summaries depend on Phase A/D edits; doing them now means redoing them) — **Owner: Elhaj** (S)
  Dr. Tahani: optional but keeping them is "ممتاز". **Decision: keep.** Just verify every chapter actually has one and the style is consistent. *(Report §1; video 1 §1.)*

---

## Phase D — Page budget, appendices, repo

- [ ] **D1 — Pin down the page count** — **Owner: Elhaj** (S)
  Rule: core manuscript (Ch.1–5) ≤ **100 pages**; references + appendices + front matter don't count. Our reading in the meeting: whole PDF 121, ~104 without refs, ~99 without appendices — borderline. Compute the real Ch.1–5 count and record the number; this decides how aggressive D2/D5 must be. *(Report §10; video 2 09:20–13:30.)*

- [ ] **D2 — Appendix-candidates analysis** — **Owner: Osman** `[AI]` (M)
  Ask Claude to analyze what should move to appendices (appendix pages don't count toward the limit):
  - **Key code snippets** — CSQE implementation, retrieval/fusion pipeline (which exact code belongs in an appendix vs. stays out — this was an explicit open question, video 2 18:00).
  - **Large tables** — e.g. the full model-comparison table; the long qualitative query-examples table (Table 4.26 area).
  Output: a recommendation report we both approve before moving anything. *(Report §10; video 2 15:08–18:45 + 25:28.)*

- [ ] **D3 — Build the code appendix** — **Owner: Elhaj** `[AI]` (M)
  After D2 approval: add Appendix with the key code snippets (CSQE, pipeline) + the GitHub repo link. Dr. Tahani's directive: code must be included as appendix. *(Video 2 15:08.)*

- [ ] **D4 — New clean GitHub repo** — **Owner: Osman** (M)
  Create a **fresh repo** (no history needed — agreed): code + notebooks only. Remove/exclude MD research files, Claude artifacts, papers/PDFs. Organize by experiment, include the key notebooks, write a clean README. Link goes into the thesis (D3). *(Video 2 17:10–18:00.)*

- [ ] **D5 — Conciseness / redundancy pass — DO LAST** — **Owner: Elhaj drives, JOINT review** `[AI]` (L)
  Explicitly agreed to be the **last content task** (video 2 25:28), after all other edits settle. Method agreed (video 2 21:00–24:25): ask Claude for a redundancy/verbosity analysis of the full thesis — for each flagged passage: current text → proposed shorter text + a **confidence score**. High-confidence trims get batch-approved; low-confidence ones we review one by one. Goal: shorten without cancelling content ("بدل ما إسهب الحاجة في نص صفحة، إسهبها في ثلاث أسطر"). Target: comfortable margin under 100 pages.

---

## Phase E — Figures & tables

- [ ] **E1 — Figure↔table duplication analysis** — **Owner: Osman** `[AI]` (M)
  Agreed open question (video 2 26:30–33:45): several figures are pure re-plots of adjacent tables (e.g. Fig 4.1 vs Table 4.1 — same nDCG numbers). Run a Claude analysis: (a) which figures merely duplicate tables; (b) for each — keep both / drop one / move one to appendix; (c) can we produce *genuine* figures not derived from tables (diagrams, distributions)? Feed conclusions into D2/D5.

- [ ] **E2 — Figures review + §4.2 regeneration (carry-over)** — **Owner: Elhaj** (M)
  Meeting: "في حاجات محتاجة مراجعة الـ Graphs دي" (video 2 14:10). Combine with the known carry-over from the old list: **Fig 4.2 / 4.3 / 4.4 must be regenerated from the canonical post-WS1 data** (text is ahead of them: 34% failure rate, word buckets 0.345/0.511/0.476, coverage 90.1%@100). Then verify every referenced `fig_*` PDF is the current version.

- [ ] **E3 — Dead labels + Ch.4 table audit (carry-over, figure-gated)** — **Owner: Elhaj** `[AI]` (S)
  Old tasks 4.16 + 5.C.5: once figures/tables are final (after E1/E2/D2 moves), check every table/figure label is referenced and every Ch.4 table is accurate and doesn't overflow pages.

---

## Phase F — Presentation prep (parallel track, not thesis-blocking)

- [ ] **F1 — Intuitive project explanation** — **Owner: JOINT** `[AI]` (M)
  Flagged as "critical, especially for the presentation" (video 2 18:45–21:00): we still struggle to explain the project simply (it reads as "half a RAG" — retrieval-only). Build with Claude: a simple narrative + analogy for (a) the retrieval-recall problem, (b) HyDE/Query2Doc intuition (already lands well), (c) **CSQE intuition** (not yet crafted), (d) why hybrid + asymmetric expansion. Output feeds the defense slides.

---

## Phase G — Process / wrap-up

- [ ] **G1 — Review this task list** — **Owner: JOINT** (S)
  Agreed in video 2 (44:15): after tasks are extracted, both review and check nothing from the meeting/report is missing.

- [ ] **G2 — Final joint read-through** — **Owner: JOINT** (L)
  Agreed in video 1 (§5): do the straightforward edits first, then read the whole thesis together as a final pass ("قراءة نهائية") before submission. Last step after D5.

---

## Suggested execution order — **AI Suggestion**

The meeting established: tasks are independent **except** the problem-statement cluster (cross-cutting) and the conciseness pass (last). Building on that:

```
Wave 1 (parallel):
  Elhaj:  A1 → A2 → A3 → A4 → A5 → A6   (core narrative — the big one)
  Osman:  C1, C2, C3, C6, C7, C8, C9     (mechanical/formatting, all independent)
  Both:   F1 can start anytime

Wave 2 (after A done):
  Elhaj:  B1 (EN abstract) → C4, C5, C10, D1
  Osman:  B2 (AR abstract, after B1) → E1, D2 analysis, D4 repo

Wave 3 (after B + D2 approved):
  Elhaj:  D3 (code appendix), E2 (figures regen/review)
  Both:   A7 (mapping audit)

Wave 4 (content frozen):
  Elhaj+Osman: D5 (conciseness pass) → E3 (labels/tables) → G2 (final read-through)
```

Rationale: A blocks B (abstract summarizes the new problem/objectives) and shapes A7/D5; D2 blocks D3 and informs D5; E1/E2 must precede E3; D5 and G2 are terminal by explicit agreement.

## Assignment balance — **AI Suggestion**

| | Elhaj | Osman | Joint |
|---|---|---|---|
| Content/writing | A1–A6, B1, C4, C5, C10 | B2, C9 | — |
| Formatting/mechanical | D1 | C1, C2, C3, C6, C7, C8 | — |
| Analysis prompts + infra | D3, E2, E3 | D2, E1, D4 | A7, D5, F1, G1, G2 |

Logic: Elhaj has driven the LaTeX/Overleaf editing and the figures track, so the narrative rewrite and figure work sit with him; Osman takes the independent mechanical sweeps, the Arabic abstract, and the repo/analysis prompts — roughly balanced. Swap anything.
