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

- [x] **A6 — Cascade check: Conclusion** — **Owner: Elhaj** (S) — **DONE 2026-07-29** (all 9 objectives now have conclusion coverage: 3 paragraphs added after full number verification — see `research_decisions/A6_number_verification.md`; 1,061 collision = genuine coincidence; §4.2 numbers fully canonical; false "all 1,061 big-wins" claim fixed at ch4 §4.9.3; A5 edits fact-checked, 11 corrections applied — see `research_decisions/A5_edit_verification.md`)
  After A1–A4, verify the Conclusion (and anywhere echoing the old statement) answers the *new* problem statement. Methodology/Results are expected to be unaffected (video 1 §5) — confirm rather than assume.

> **Phase A review flags (2026-07-29, from the A1–A4 session — decide at Elhaj's read-through):**
> 1. **§1.1 closing sentence detail** — it currently pre-announces the empirical finding ("asymmetric hybrid sparse–dense fusion, expansion applied to the sparse retriever only"). AI recommendation: keep the pipeline announcement (technology-driven framing is sanctioned) but drop the "asymmetric / sparse-side-only" specificity — that is a Chapter 4 *result*, and Objective 9 already poses it honestly as an open question.
> 2. **The word "small" in the objectives** — removed in A4; scope is now carried numerically ("openly available LLMs spanning 2–8 billion parameters"). Optional: reinstate once, e.g. Objective 4 → "small, openly available LLMs (2–8 billion parameters)". Numeric range carries the content; the word adds emphasis only. Safe anywhere except the RQ and the problem-statement endpoint.
> 3. **First-mention re-audit (Ch.2/Ch.3)** — acronym definitions moved into Ch.1 during the merge of the C3 sweep with the A1–A4 rewrite; later chapters may hold duplicates/orphans. Fold into E3/A7.
> 4. **Osman to review the 9-objective structure** (was ~8 in the meeting count) — per G1.
> 5. **Pre-submission literature re-verification** (from A5 fact-check §7, `A5_edit_verification.md`): (a) the claim "LLM-based QE has not been evaluated for monolingual Arabic retrieval" was only ever *searched* at sub-7B scope (WS6) — re-run the search without the size filter; (b) obtain Macmillan-Scott et al. 2025 (arXiv 2511.19325) — WS6 notes say it evaluates MuGI and Exp4Fuse across eight languages *including Arabic* (cross-lingual) — confirm our gap claims survive contact with the actual paper; (c) MuGI and Exp4Fuse have no summaries in `papers/` — their characterisations rest on second-hand notes.
> **2026-07-29 — SCOPE DECISION (Elhaj):** the final-round revision commit (`31240f1`) went beyond this task list. Everything not required to remove a *false or self-contradicting* statement was **reverted** to the end-of-Phase-A text (`6ba4e80`) in commit `f0e0fb9`. Reverted: Doc2Query++ and Arabic-AQE-survey citations (both unverified, no copy in `papers/`, and the first conceded novelty), the CSQE taxonomy bullet, the CSQE 830/1,000 description rewrite, the §1.1 closing rephrase, the expanded Overall licence sentence. Kept (each removes a defect): Ch.3 zero-shot justification (old text claimed small models have limited context windows — false, they have 12K–128K), Ch.3 CSQE one-shot disclosure (thesis claimed zero-shot throughout while CSQE uses a one-shot English example), Ch.2/Ch.3 licence criterion (old text said "permissive licences" — Aya is CC-BY-NC), Ch.2 §2.5.2 topic sentence (old text described KAR/AQE/ThinkQE/PBR as small-model studies — they are not), Ch.5 Challenges item 8 + matching recommendation, and terminology consistency. **Rule for the rest of the project: no thesis edit without a task-list entry.**
>
> 6. **Aya licence caveat now in Ch.5 Overall** — Aya Expanse 8B is CC-BY-NC (per Table in Ch.2); the conclusion now says "practical … subject to the licence of the chosen generator". Review whether to keep, soften, or move to Limitations.

- [x] **A7 — AI audit of the 1-to-1 mapping** — **Owner: JOINT** `[AI]` (S) — **DONE 2026-07-29** (Opus audit: chain sound — 9/9 objectives have Ch.3+Ch.4+Ch.5 anchors, 0 orphan conclusion paragraphs; 6 blockers + 13 minors + 4 acronym violations found and fixed, except B5 = stale abstract, deferred to B1. Full audit: `research_decisions/A7_mapping_audit.md`. Deferred minors: M12 full open-source→openly-available sweep (Ch.2/3 factual contexts), M14 SILMA naming — both folded into D5/terminology pass.)
  Committee evaluates on strict mapping: Problem ↔ Objectives ↔ Methodology & Results ↔ Conclusions. Run a dedicated Claude check that every objective is addressed in methodology/results and checked off in the conclusion; fix gaps. *(Report §5; video 2 03:07 — "نستصحبها معانا مع الـ AI".)*

---

## Phase A-bis — Data corrections found during verification (NEW, 2026-07-29)

- [x] **A8 — Close the Objective 2 mapping gap in the Conclusion** — **Owner: Elhaj** (S) — **DONE 2026-07-29**
  A7's own blocker-B1 fix added "characterising the linguistic failure patterns arising from Arabic morphological, orthographic and lexical variation" to Objective 2, but A7 was never re-run afterwards, so no conclusion sentence was added. Methodology (§3.3.3 Failed Query Inspection) and results (§4.2.4, three named patterns with Arabic examples) both exist; only the Ch.5 check-off was missing. **Fix applied:** one sentence appended to Ch.5 §5.1 ¶1, citing `sec:res_error_rationale`. Verified against ch4:144 — the three patterns are vocabulary mismatch (\<آزوت>/\<نيتروجين>), named-entity variation (\<إبن الهيثم>/\<ابن الهيثم>), diacritic sensitivity (\<المَثَانةُ>/\<المثانة>).

- [ ] **H2 — Jais-2-8B temperature is wrong in Ch.3 Table 3.2** — **Owner: Osman** (S) — **CONFIRMED 2026-07-29, not yet fixed**
  `chapter3.tex:294` prints Jais-2 8B at temperature **0.1**, but its own feeder file `thesis_figures/data/raw/table_3_2_gen_hyperparams.csv:8` says **0.7** (and the generation notebook sets 0.7). The `.tex` cell is the outlier — the CSV is canonical. **No Ch.4/Ch.5 number changes**; this is a single table cell. Fix = change `0.1` to `0.7` in that row. *(Found by the SILMA temperature investigation; see `research_decisions/SILMA_TEMPERATURE_RATIONALE_CHECK.md`.)*

- [ ] **H3 — Table 3.2 caption may misstate top_p for Qwen3-4B** — **Owner: Osman** (S) — **UNRESOLVED, needs notebook check**
  The caption says "top_p = 0.9 unless otherwise noted". The investigating agent reports Qwen3-4B actually used `top_p=0.8, top_k=20` (the Qwen3 developer-recommended sampling settings), but the feeder CSV records `0.9` for Qwen3-4B. **Agent and CSV disagree** — resolve by reading `Query_generator_qwen3_4B.ipynb` before changing anything. If the agent is right, both the CSV and the caption need correcting. Low impact: sampling detail only, no metric changes.

- [ ] **H1 — SILMA temperature mix-up in the repetition sweep** — **Owner: Osman** (S) — **HANDED TO OSMAN 2026-07-29 by Elhaj**

  > **Handover note (Elhaj → Osman).** Two separate things are involved here; please keep them apart when you look at it:
  > 1. **The temperature *decision* for SILMA.** Elhaj's position is that this was made deliberately and is correct — and the evidence agrees with him: your `Query_generator_silma_2B.ipynb:510` hard-codes `TEMPERATURE = 0.1`, and `OSMAN_MODEL_COMPARISON_RESULTS.md:18-31` records "Decision: Use temperature 0.1 for all subsequent experiments". `thesis_figures/data/raw/table_3_2_gen_hyperparams.csv:2` carries your own note: *"temp 0.1 chosen empirically over 0.7 (+2.5%)"*. **Nothing here is being questioned.**
  > 2. **Which pickle the Exp 1.1 repetition sweep actually loaded.** This is the only issue: `phase4_quick_wins (1).ipynb` cell 7 maps `'SILMA 2B': 'silma_2b_temp07.pkl'`. Both facts can be true at once — the decision was 0.1, the sweep read the older 0.7 file.
  >
  > **Open question for you:** was loading `silma_2b_temp07.pkl` in the sweep intentional for some reason we have not found, or is it a leftover from the earlier default-config run? If intentional, say why and we will document it instead of re-running.
  >
  > **What was checked, so you do not repeat it:** a repo-wide search found developer-recommended-temperature statements for Falcon-H1 (0.1), Qwen3 (0.7 / top_p 0.8 / top_k 20) and ALLaM (card says 0.6, we deliberately used 0.7 for comparability) — **and none for SILMA**. Only SILMA has both `.pkl` variants on disk; the other 8 sweep rows load the same pickle as the model-comparison run, so nothing else is affected. `exp_011_bm25_repetition.md` records no temperature choice at all.
  >
  > **Sources:** `research_decisions/SILMA_TEMPERATURE_RATIONALE_CHECK.md` (this investigation) · `research_decisions/SILMA_CONFLICT_RESOLUTION.md` (original root-cause analysis) · `thesis_figures/data/raw/table_3_2_gen_hyperparams.csv` (canonical per-model hyperparameters).
  >
  > **Related and also yours now:** H2 and H3 below — both are Table 3.2 hyperparameter cells and depend on the same knowledge.

  Root cause proven: `phase4_quick_wins (1).ipynb` cell 7 maps `'SILMA 2B': 'silma_2b_temp07.pkl'` — the Exp 1.1 repetition sweep loaded SILMA's **temperature-0.7** expansions while every other model (and Ch.3 Table 3.2, and the dense Table 4.6) uses **temperature 0.1**. Hence Table 4.7 says 0.4277 and Table 4.11 says 0.4194 for the same configuration. **Table 4.7 (0.4277) is canonical**; the sweep is the deviant. Only SILMA is affected — the other 8 models match to 4 d.p. across both tables.
  - **Option A (recommended):** re-run SILMA's 8 repetition configs with `silma_2b_temp01.pkl` (~8 min, CPU-only, all inputs in-repo), then update Tables 4.11/4.12 + regenerate Figs 4.7/4.8.
  - **Option B (no re-run):** keep 0.4277 in Table 4.7, footnote Table 4.11 that SILMA's sweep used temp 0.7. Table 4.12's Δ=+0.0639 stays correct as printed.
  - **Rejected:** changing Table 4.7 to 0.4194 — it would split SILMA's dense/sparse rows across two temperatures.
  - **Independent of the choice:** `thesis_figures/data/raw/model_comparison_bm25.csv:3` and `thesis_figures/output/pdf/table_4_3.tex:6` pair temp-0.1 n=1 metrics with the temp-0.7 best config (Δ=0.0555, matching neither table); **Figs 4.7 and 4.8 currently plot different SILMA values** because they read different CSVs. Both need regenerating from one source regardless.
  - Full evidence: `research_decisions/SILMA_CONFLICT_RESOLUTION.md`.

---

## Phase B — Abstracts (after Phase A)

- [ ] **B1 — Rewrite the English abstract** — **Owner: Elhaj** `[AI]` (M) — *A7 blocker B5 lands here: the abstract still carries the pre-A1 framing (old RQ, no CSQE, no asymmetric-placement finding). Starter sentences proposed in `A7_mapping_audit.md` §(g) B5.*
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
  **Done:** `7-ListofAbbreviations.tex` rewritten — the two template placeholders ("Test Example"/"Another Example") removed, **60 entries** added, sorted A→Z, in the template's `\acro` bold-initials style (plain text where bolding is awkward: BF16, FP16, NF4, BM25S). `[LONGEST]` set to `[MS MARCO]` so the label column aligns. `MS~MARCO` and `TyDi~QA` use the `\acro{key}[short]{long}` form to keep spaces out of the internal key. Renders on pp. xvi–xviii.
  Also fixed two defects the filled list exposed: (a) the running header read **LIST OF TABLES** on the abbreviation pages (`\chapter*` never resets `\leftmark`) — added `\markboth{\MakeUppercase{List of Abbreviations}}{}`; (b) a **blank page xix** — the 64 entries filled p. xviii exactly, TeX broke at the list's closing negative penalty (`\@endparpenalty`), and `\clearpage`'s `\hbox{}` fallback then materialised the empty page. Fixed with `\itemsep`/`\parsep` `=0pt` inside the environment, which gives the list slack. Thesis is now **122 pages**, compiles clean (0 errors).
  **Removed on Osman's instruction (2026-07-28):** BM25S, ICLR, MBZUAI, SDAIA (64 → 60 entries). All four remain expanded inline at first mention in the text, so the first-mention rule is unaffected; they are simply not listed.
  ⚠️ **NOT included, expansions unverifiable:** ACQAD, 3C3H, Arabic-SQuAD (single mentions; I did not invent expansions — confirm before adding). Excluded by design: pure model/product names (Qwen, Jais, Aya, SILMA, Gemma, Falcon-H1, ALLaM, BGE-M3, E5, T4, A100…) and one-off cited-system names (GaQR, ThinkQE, QE-RAG, Exp4Fuse).
  ⚠️ **If entries are added later:** ~15+ more could refill p. xviii exactly and bring the blank page back; same two lengths (or trimming an entry) will clear it.

- [x] **C3 — First-mention rule sweep** — **Owner: Osman** `[AI]` (M) — **DONE 2026-07-28**
  Thesis-wide: first mention = full phrase + (ABBR); later mentions = abbreviation only. E.g. "Retrieval-Augmented Generation (RAG)". Audit + fix every acronym. *(Report Part 2B; video 2 34:20.)*
  **Done in two passes.** Pass 1 — added the missing first-mention expansions (~28 edits): HyDE, GRF, GPT-3, APIs, GPUs, BM25, MIRACL, mDPR (Ch.1); FAISS, QA, DCG, VRAM, SwiGLU, FP16, Squared-ReLU, BF16, AI, RMSNorm, SiLU, NF4, MAP (Ch.2); QLoRA, MS MARCO, NLTK (Ch.3); NLP, MTEB/MMTEB/STS (Ch.5). **`QE` was never defined anywhere in the thesis** — now defined at `chapter1.tex:9`. Also normalised `mAP`→`MAP`.
  Pass 2 — **strict enforcement per Osman's instruction (2026-07-28): each expansion appears exactly once, even where it costs readability.** 89 occurrences of "query enhancement" → `QE` across Ch.1–5, plus every repeated re-definition stripped to the bare abbreviation (LLM, RAG, MSA, HyDE, GRF, BM25, CSQE, MIRACL, mDPR, RRF, CC, SFT, OALL, NF4, QA). **Section headings and the ToC are included** — Osman's explicit call when asked. ToC now reads: `2.1.1 LLMs and the Transformer Architecture`, `2.1.2 RAG`, `2.1.4 QE Techniques`, `2.2.4.2 NDCG@k`, `2.2.4.3 MRR`, `2.4.3.1 mDPR`, `3.8 CSQE`, `4.8 CSQE Results`, `4.5.4 Dense vs. BM25 Behaviour with QE`.
  Verified by script: every expansion now occurs exactly once in Ch.1–5 and once in the standalone abstract (the abstract is read independently, so it carries its own first mentions). Untouched as scoped: `6-ARAbstract.tex` (task B2), the Ch.3 verbatim LLM prompt blocks, and generated files.
  ⚠️ **Side effect of including headings:** `NDCG` and `MRR` were previously defined *in* their §2.2.4.2/§2.2.4.3 headings. Those headings are now bare, so the definitions moved into the first body sentence below them — the only two places where an abbreviation precedes its own expansion. Reversible in one edit each if Dr. Tahani objects.
  ✅ **`nDCG` vs `NDCG` casing — RESOLVED 2026-07-28** (Osman's instruction). Unified on **`NDCG`** everywhere: 49 replacements — `chapter3.tex` (2, both figure captions), `chapter4.tex` (46, prose + table cells + captions), and `thesis_figures/output/pdf/table_2_1.tex` (1, `\input` into Ch.2). Rendered PDF now contains **167 × NDCG, 0 × nDCG**. Verified no occurrence sat inside a `\label`/`\ref`/filename/`\cite` before replacing, and file line endings were preserved. `table_2_1.tex` lives in the generated output folder but **no script regenerates it**, so the fix will not be overwritten.
  **Figures needed no change:** rendered `fig_4_1`, `fig_4_7` and `fig_4_11` to image and confirmed their axis labels already read `NDCG@10`. The 32 `nDCG` strings in `thesis_figures/*.py` are comments, `print` statements and AI-image prompts — not matplotlib labels — so E2 regeneration will not reintroduce lowercase.
  ⚠️ **Build noise (pre-existing, not from these tasks):** ~128 `Hyper reference 'acro:X' undefined` warnings — `acronym`+`hyperref` link list entries to targets only `\ac{}` creates, and the thesis never uses `\ac{}`. Verified the original placeholder file produced the same warning. One-line fix if wanted: `\usepackage[nohyperlinks]{acronym}` (`1-main.tex:78`).
  ℹ️ **Related but much milder — abstract running head.** `\chapter*` never sets a running head, so the English abstract's *continuation* page (currently p. v) shows a **blank** left header instead of "ABSTRACT". Unlike C2's case this is not a *wrong* header, just a missing one — the first page of any `\chapter*` uses `\thispagestyle{plain}` and correctly shows no header at all. **Left alone deliberately:** B1 shrinks the abstract to ≈3/4 page, which removes the continuation page and the issue with it. Only worth a `\markboth` if the abstract still runs to 2 pages after B1.

- [ ] **C4 — Thesis Layout §1.3 → one single paragraph** — **Owner: Elhaj** (S)
  Currently one paragraph *per chapter*; must become **one single continuous paragraph** ("Chapter 2 establishes… Chapter 3 details… Chapter 4 reports…"). *(Report §6; video 2 03:37–04:20. Closes old 5.E.4.)*

- [ ] **C5 — Promote bold inline headings to numbered sub-headings** — **Owner: Elhaj** (M)
  Agreed in video 2 (06:10–07:20): §2.1.4 Query Enhancement Techniques → 2.1.4.1, 2.1.4.2, … (p.28) and §2.1.5 Arabic Language Processing Challenges → 2.1.5.1, 2.1.5.2, … (p.30). While there, audit for any other large section using bold-text pseudo-headings and apply the same. *(Report §7.)*

- [x] **C6 — Citations: IEEE order-of-appearance + web access dates** — **Owner: Osman** `[AI]` (M) — **DONE 2026-07-29**
  (a) Verify the bibliography style numbers references strictly in order of first appearance ([1], [2], [3]…) — Elhaj was unsure the LaTeX setup does this; check the .bst/biblatex config and the rendered PDF. (b) Every web reference must have full URL + explicit access date ("[Online]. Available: … [Accessed: …]"). *(Report Part 2C; video 2 34:20–35:30.)*
  **(a) PASS — no changes needed.** Compared first-appearance order (from the per-chapter `.aux` files) against `\bibitem` order in `1-main.bbl`: **48/48, zero mismatches.** `IEEEtran.bst` is unsorted, so it emits in citation order. Multi-key `\cite`s all ascend too. `References.bib` entry order untouched — irrelevant to IEEEtran.
  **(b) 4 entries stamped, all 5 web URLs alive (HTTP 200).** `silma_2024`, `bm25s_2024`, `louis_2024_query`, `bari2025allam`. Mechanism: IEEEtran **already auto-prints `url`** as `[Online]. Available: …`, so `note` carries only the date (it renders just before `[Online]` — exactly where IEEE puts `Accessed:`); brace-protected as `{A}ccessed` because IEEEtran lowercases a note's first char. arXiv / DOI'd / ACL-venue entries left alone by design.
  **Verified by local compile** (`xelatex → bibtex → xelatex ×2`): 0 errors, 0 undefined citations, 122 pages. No Overleaf check needed.
  ⚠️ **`bari2025allam` is a borderline stamp** — it has ICLR venue metadata (argues against a date) but no DOI/arXiv ID and OpenReview pages are mutable. Revert is one line. Its missing arXiv ID (2407.15390) flagged, not edited.
  ⚠️ **~35 arXiv entries render `[Online]. Available: …` with no access date.** Correct IEEE, but a literal reading of the directive may query it. Same one-line fix each if uniformity is wanted.
  ⚠️ **`perin_2025_investigating`** — uncited orphan, no `booktitle`; renders nowhere. Kept per no-delete decision; needs venue + date if ever cited.
  ⚠️ **Committed `1-main.pdf` was six weeks stale** (June 19, 121 pp — predated C1/C2/C3 and A1–A4). Verification rebuild → 122 pp, so its diff is mostly pre-existing source changes, not this task's.

- [x] **C7 — Verify caption placement** — **Owner: Osman** (S) — **DONE 2026-07-29 (verdict: no change needed)**
  Table captions ABOVE tables; figure captions BELOW figures. We believe this is already correct — verify every table/figure rather than assume. *(Report §10; video 2 25:28.)*
  **Verdict: zero violations, zero edits.** Audited all **58 float environments** (34 tables, 24 figures) across `1-main.tex`, front matter, Ch.1–5, and the generated `.tex` fragments. Every table caption is above its `tabular`, every figure caption below its `\includegraphics`, and `\label` sits immediately after `\caption` throughout. Numbering verified unchanged (per-chapter, separate per entity type). Local compile clean: 0 errors, 0 undefined `\ref`, 0 `??` in the PDF, 122 pages.

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

> **2026-07-30:** Agent prompts for Osman's Wave-2 tasks (E1, D2, D4) are ready in `research_decisions/OSMAN_WAVE2_PROMPTS.md` — run E1 before D2 (D2 consumes E1's report). B2 waits on B1. Each prompt now ends with an approval gate: agent reports → Osman approves → agent marks the task done here.

- [x] **D1 — Pin down the page count** — **Owner: Elhaj** (S) — **ANSWERED 2026-07-29** from a clean local xelatex build (post-Phase-A, post-Osman-C1/C2/C3):
  > **Core manuscript (Ch.1–5) = 103 pages — 3 OVER the 100-page limit.**
  > Ch.1 p.1 · Ch.2 p.7 · Ch.3 p.36 · Ch.4 p.60 · Ch.5 p.95 · Bibliography starts p.104 (ends p.128). Front matter is roman (i–xvi+). **No appendices exist yet**, so D3's code appendix adds nothing to the count.
  > Implication: D2 (move large tables to appendices) + D5 (conciseness) must free ≥3 pages just to reach the limit, and more for a comfortable margin. The biggest single lever is Ch.4 (60→94, i.e. 35 pages of results/tables).

- [x] **D1-orig — Pin down the page count** — *(superseded by the measurement above)* — **Owner: Elhaj** (S)
  Rule: core manuscript (Ch.1–5) ≤ **100 pages**; references + appendices + front matter don't count. Our reading in the meeting: whole PDF 121, ~104 without refs, ~99 without appendices — borderline. Compute the real Ch.1–5 count and record the number; this decides how aggressive D2/D5 must be. *(Report §10; video 2 09:20–13:30.)*

- [x] **D2 — Appendix-candidates analysis** — **Owner: Osman** `[AI]` (M) — **DONE 2026-08-02**
  Ask Claude to analyze what should move to appendices (appendix pages don't count toward the limit):
  - **Key code snippets** — CSQE implementation, retrieval/fusion pipeline (which exact code belongs in an appendix vs. stays out — this was an explicit open question, video 2 18:00).
  - **Large tables** — e.g. the full model-comparison table; the long qualitative query-examples table (Table 4.26 area).
  Output: a recommendation report we both approve before moving anything. *(Report §10; video 2 15:08–18:45 + 25:28.)*
  **Done:** full report at `research_decisions/D2_APPENDIX_CANDIDATES_REPORT.md`, written as a line-by-line sign-off sheet (CODE-1…9, TAB-1…5, MISC-1…2, each with Osman/Elhaj checkboxes).
  **Core manuscript is 105 pages — 5 OVER the limit** (Ch.1 p.1 · Ch.2 p.7 · Ch.3 p.37 · Ch.4 p.62 · Ch.5 p.97–105 · Bibliography p.106). With a ~5-page margin we must free **≈10 pages**. Proposed: **Appendix A** = 8 code snippets (~525 lines, ≈12 pp), **Appendix B** = 4 extended tables (4.12, 4.14 sweep, 4.26, 4.28), **Appendix C** = §2.4 per-model prose + §3.5.4. **Projected core ≈96 pages after D2 + E1, before D5 does anything.** A 5-action minimum set reaches ≈97.3.
  ⚠️ **THE PAGE COUNT IN THIS FILE IS WRONG IN TWO PLACES.** D1 records 103 and E1 records 97; the real number is **105**. E1 measured from `1-main.toc`/`.lof`/`.lot`, which are artefacts of a **20:34 build (122 pp)**, while the `1-main.pdf` committed beside them is from a **22:38 build (131 pp)**. Verified three ways: the PDF's own embedded ToC (`Bibliography … 106`), rendered chapter-opening pages (sheet 20 → footer "1"; sheet 116 → "Chapter 5", footer "97"), and 131 − 19 front-matter sheets = 112 = 105 core + 7 bibliography. **Rule going forward: measure page counts from the compiled PDF, never from `.toc`.** A local rebuild is not a valid check unless the machine renders Arabic — this one does not (XeLaTeX silently drops every Arabic glyph and shortens the document). **Consequence: E1's "these cuts buy margin, they are not rescuing a violation" is reversed — D5 does need to be aggressive.**
  ⚠️ **ELHAJ MUST APPROVE THE REPORT BEFORE D3 EXECUTES IT.** Osman approved 2026-08-02; the sign-off sheet has a second column deliberately left blank.
  ⚠️ **DECISION 1 (Elhaj) — what did "the full model-comparison table" mean in the meeting?** The report reads it as **Table 4.12** (full 9×8 repetition sweep) and keeps Tables 4.8/4.9 inline, because E1 deletes Figs 4.5/4.6 *precisely because* Table 4.8 is the better artefact — moving 4.8 out would leave §4.4.1 with nothing.
  ⚠️ **DECISION 2 (Elhaj) — conflict with E1 over Tables 4.22 / 4.28.** E1's action list drops Table 4.22 as redundant with 4.28; D2 proposes moving 4.28 to the appendix. **Doing both would strip the system-progression numbers from Ch.4 entirely.** Net page difference is 0.2 — decide on narrative grounds. Recommendation: **TAB-4a** (move 4.28, keep 4.22 inline).
  ⚠️ **DECISION 3 (Dr. Tahani) — MISC-1, the largest single saving (≈3.5 pp).** Moving §2.4.1–2.4.2's per-model descriptions (1,499 words, 10 models) to an appendix moves *prose*, not data; her directive named code, proofs and raw data tables. It is also 35% of the total saving and fixes a Phase-A framing remnant (A2 de-scoped model characteristics). Suggested question: *"do the per-model description sections in the background chapter count as appendix material?"* **If she says no, D5 must absorb ≈3 pages of prose cuts instead** — the remaining table moves total only ≈1.9 pages against a 5-page deficit.
  ⚠️ **Two margin-overflow defects found while sizing (→ E3, not D2's to fix):** **Table 4.28**'s `Status` column runs past the right text margin in the compiled PDF (clipped mid-word: "Baselin", "Droppe", "Best ove") and the table sits nearly alone on p.96 under ~40% of a page of whitespace; **Table 2.1** (p.14) has rules extending past the text block. Moving 4.28 resolves the first. Possible third, unverified: the Arabic root letters in §2.1.5's `k-t-b` morphology example appear blank on p.14 while Arabic renders fine elsewhere (p.93).
  ⚠️ **Finding for D4:** `src/enhancers/contrastive_hyde.py` + `src/retrievers/contrastive_dense.py` (517 lines) implement a line of work that **appears nowhere in Ch.1–5** — grep finds only generic "contrastive learning" (ch2:72) and HyDE's encoder (ch2:89). Excluded from the appendix; consider excluding from the clean repo too.

- [ ] **D3 — Build the code appendix** — **Owner: Elhaj** `[AI]` (M)
  After D2 approval: add Appendix with the key code snippets (CSQE, pipeline) + the GitHub repo link. Dr. Tahani's directive: code must be included as appendix. *(Video 2 15:08.)*

- [x] **D4 — New clean GitHub repo** — **Owner: Osman** (M) — **DONE 2026-08-04**
  Create a **fresh repo** (no history needed — agreed): code + notebooks only. Remove/exclude MD research files, Claude artifacts, papers/PDFs. Organize by experiment, include the key notebooks, write a clean README. Link goes into the thesis (D3). *(Video 2 17:10–18:00.)*
  **Done:** **https://github.com/Osmanoor/arabic-rag-query-enhancement** — public, MIT, fresh history, single commit, **102 files / 136 MB**. Assembled outside this repo at `d:\Projects\Graduation\arabic-rag-query-enhancement\` so nothing is nested inside `graduation-1`.
  **Included** (Osman's call 2026-08-04 — maximally inclusive): 25 notebooks grouped by experiment (`01_baselines/` incl. `pyserini_superseded/`, `02_query2doc/`, `03_model_comparison/` = 11 generators, `04_csqe/`, `05_repetition_fusion_error_analysis/` with all four phase-4 duplicates — canonical at top level, the other three under `variants/` with a README explaining which is which), all 15 `src/` modules, 2 scripts, **all** results (36 files: every `.pkl`, every TREC run, sweep CSV/JSON, plots), MIRACL dev topics+qrels, and all 12 experiment write-ups under `docs/`.
  **Excluded:** Contrastive HyDE (6 files — Osman's decision, matching the D2 finding that it appears nowhere in Ch.1–5), three 0-byte files, and `SCIENTIFIC_REVIEW_ERROR_ANALYSIS.md` (AI-bylined "Antigravity (Agentic AI)" + carries the superseded 39% failure rate; thesis says 34%).
  **Notebook-output policy: outputs KEPT everywhere** (3.1 MB of notebooks; the 12 embedded charts in the phase-4 notebook are the strongest artefact an examiner sees). Only exception: Falcon-H1's OOM error tracebacks cleared.
  **Scrubs applied and verified:** 25 × old repo URL → new; 88 × `/content/graduation/...` and `%cd graduation/...` paths; HF-token cell → Colab secrets manager (`userdata.get('HF_TOKEN')`); 17 dangling `research_decisions/*.md` references; 2 `CLAUDE.md`/`TASKS.md` comment lines; **17 Colab `?usp=sharing` share links replaced with in-repo notebook paths** so the team's Drive stays unlisted. Leak scan run against the *published* remote tree: zero hits for `CLAUDE`, `.claude`, `research_decisions`, `meetings`, `papers/`, `contrastive`, `SCIENTIFIC_REVIEW`. Secret scan (`hf_*`/`sk-*`/`ghp_*`): zero hits. All 25 notebooks re-validated as parseable `.ipynb` after scrubbing.
  ⚠️ **THE URL MUST GO INTO THE THESIS CODE APPENDIX — task D3 (Elhaj).** Dr. Tahani's directive is that the code appears as an appendix; D3 adds the snippets *and* this link. Nothing in the thesis cites the repo yet.
  ⚠️ **Repo may be renamed later** (Osman, 2026-08-04 — name `arabic-rag-query-enhancement` chosen "for now"). GitHub keeps redirects on rename, but the notebooks hard-code the clone URL and `%cd` path in **88 places** — one find/replace + recommit. **Rename before D3 cites it**, or D3 will cite a redirect.
  ⚠️ **Cosmetic, not fixed:** three pickles (`allam_7b`, `jais_2_8b_chat`, `qwen3_4b`) carry a `'research_doc': 'research_decisions/…'` string inside their metadata dict. Left alone — rewriting binary pickles risks corrupting the query arrays.

- [ ] **D5 — Conciseness / redundancy pass — DO LAST** — **Owner: Elhaj drives, JOINT review** `[AI]` (L)
  Explicitly agreed to be the **last content task** (video 2 25:28), after all other edits settle. Method agreed (video 2 21:00–24:25): ask Claude for a redundancy/verbosity analysis of the full thesis — for each flagged passage: current text → proposed shorter text + a **confidence score**. High-confidence trims get batch-approved; low-confidence ones we review one by one. Goal: shorten without cancelling content ("بدل ما إسهب الحاجة في نص صفحة، إسهبها في ثلاث أسطر"). Target: comfortable margin under 100 pages.

---

## Phase E — Figures & tables

- [x] **E1 — Figure↔table duplication analysis** — **Owner: Osman** `[AI]` (M) — **DONE 2026-08-02**
  Agreed open question (video 2 26:30–33:45): several figures are pure re-plots of adjacent tables (e.g. Fig 4.1 vs Table 4.1 — same nDCG numbers). Run a Claude analysis: (a) which figures merely duplicate tables; (b) for each — keep both / drop one / move one to appendix; (c) can we produce *genuine* figures not derived from tables (diagrams, distributions)? Feed conclusions into D2/D5.
  **Done:** full report at `research_decisions/E1_FIGURE_TABLE_DUPLICATION_REPORT.md`. Inventoried all **23 figures + 34 tables** (Ch.1 and Ch.5 have zero floats; Ch.2–3's 8 diagrams are all ORIGINAL — no suspects). Verdicts: **6 DUPLICATE** (Fig 4.2, 4.5, 4.6, 4.13, 4.14, 4.15 — drop all six, HIGH confidence), **5 PARTIAL OVERLAP** (4.3, 4.4, 4.8, 4.10, 4.11 — in 4 of 5 the *table* is what should be trimmed or moved, not the figure), **12 ORIGINAL**. **Page savings ≈ 3.2 pages** high-confidence, **≈ 4.5** with the medium-confidence appendix moves. §7 of the report has a copy-paste delete list for D5 and an appendix-candidate list for D2; 6 genuine (non-re-plot) figure opportunities are specced in §4 with their data sources.
  **Correction to the meeting's premise:** Fig 4.1 is **not** a re-plot of Table 4.1 — it is a genuine per-query distribution over 2,896 queries, Table 4.1 is 3 rows of aggregates. **Keep both.** The real case is one section later: **Fig 4.5 is a bar chart of Table 4.8's NDCG@10 column printed on the same page directly beneath it** (p. 66), and Fig 4.6 re-plots three more of its columns (p. 67). Verified by rendering the actual pages.
  **Input to D1:** core manuscript measured at **97 pages** (Ch.1 p.1 → Ch.5 ends p.97; Bibliography starts p.98) — **already under the 100 limit.** These cuts buy margin and answer Dr. Tahani's tables-vs-figures directive; they are not rescuing a violation. D5 does not need to be aggressive.
  ⚠️ **Three live defects found in figures now in the thesis** (→ E2): (a) **Fig 4.9's axis labels are mojibake** — `Î"` instead of `Δ`, both axes, verified on p. 75 of the compiled PDF; the notebook source is correct (U+0394), so re-running `03_model_comparison.ipynb` fixes it (also affects `fig_4_8_gains_v2_slope`). (b) **Fig 4.5/4.6 contain an `Aya 8B CSQE` bar** that is absent from Table 4.8 and does not belong in a Query2Doc chart; both also omit ALLaM, which the table includes — moot if the drops are accepted. (c) **Fig 4.15's percentage labels are clipped** by the donut ring ("12%" renders as "%") — moot if dropped.
  ⚠️ **Fig 3.6 (CSQE pipeline) is an AI-generated JPEG** mis-named `.png` (PaperBanana/Gemini, 2752×1536) — a raster in an otherwise all-vector thesis, illustrating **our own contribution**. A TikZ version already exists (`system_diagrams/fig_3_8_csqe.tex`). **Recommend raising with Dr. Tahani** — a committee may ask how the figure was produced.
  ⚠️ **Two items need a team decision:** (a) **Fig 4.3** — drop it, or replace it with the proposed query-length histogram (G3)? Dropping removes the only view of within-bucket spread; medium confidence either way. (b) **Build G1 (per-query win/loss scatter) and/or G2 (recall funnel)?** Both are genuine figures rather than re-plots — exactly what Dr. Tahani asked for. G2 is cheap and doubles as F1 defense material.
  ⚠️ **Bonus finding for D2/D5 — table↔table duplication:** **Table 2.3 (p.19) and Table 2.4 (p.26)** list the same 10 models with overlapping columns, 7 pages apart in the same chapter. One should go. (Table 4.22 ↔ 4.28 is already covered by the Fig 4.11 verdict.)
  ⚠️ **Dead code for E3:** `\iffalse` figure block `fig:regression_pie_old` at `chapter4.tex:922-933`.

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
