# Osman — Wave 2 Agent Prompts

**Created:** 2026-07-30. Prompts for Osman's Wave-2 tasks from `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`.
**Covered:** E1 (Prompt 1), D2 (Prompt 2), D4 (Prompt 3).
**Skipped for now:** B2 (Arabic abstract) — blocked until Elhaj finishes B1 (English abstract); it re-derives from B1's output.

## How to use

- Run **one prompt per fresh agent/chat**, from the repo root. Review + commit between prompts.
- **Order matters this time:** run **Prompt 1 (E1) before Prompt 2 (D2)** — D2 reads E1's report to fold figure/table appendix candidates into one recommendation. Prompt 3 (D4) is independent — run it anytime.
- E1 and D2 are **analysis tasks**: their only output is a report file (no thesis edits). D4 has two stages with your approval between them.
- Every prompt ends with the same **approval gate**: the agent reports, waits for your explicit approval in that chat, and only then marks the task done in `THESIS_FINAL_SUBMISSION_TASKS.md`.

---

## Prompt 1 — E1: Figure ↔ table duplication analysis

```
You are working in the Arabic RAG thesis repo (graduation project, University of
Khartoum). The thesis LaTeX source is in
`University_of_Khartoum__EEE_bachelor_s_thesis_template/` (main file `1-main.tex`,
chapters in `Chapters/chapter1.tex`…`chapter5.tex`, compiled PDF `1-main.pdf`).
The figures are produced by a pipeline in `thesis_figures/` (matplotlib notebooks
in `thesis_figures/notebooks/`, rendered PDFs in `thesis_figures/output/pdf/`,
TikZ system diagrams in `thesis_figures/system_diagrams/`, source data in
`thesis_figures/data/`).

THIS IS AN ANALYSIS-ONLY TASK. Do NOT edit any thesis .tex file, any figure, or
any notebook. Your only output is a report file.

CONTEXT: Our supervisor (Dr. Tahani) directed us not to confuse tables and
figures, and to keep the manuscript concise (core chapters ≤ 100 pages; current
build is ~122). In our team meeting we noticed that several figures appear to be
pure re-plots of an adjacent table — e.g. Figure 4.1 is a bar chart of the same
nDCG@10 numbers shown in Table 4.1 directly above it. We need a systematic
analysis before deciding what to cut or move. A previous audit counted roughly
34 tables and 24 figures across the thesis; most data figures are in Chapter 4
(Fig 4.1–4.15 area), while Chapters 2–3 contain ~7 TikZ system diagrams (those
are genuine diagrams, not table re-plots — include them in the inventory but
they are not duplication suspects).

TASK:
1. Build a complete inventory of every figure and every table in Chapters 1–5:
   number, caption, file (for figures: which PDF in thesis_figures/output/pdf/
   and which generating notebook), what data it shows, and its physical size on
   the page (approximate fraction of a page, from the compiled PDF).
2. For each FIGURE, classify its relationship to nearby tables:
   - DUPLICATE: shows the same numbers as a table (reader needs neither to
     understand the other) — name the table;
   - PARTIAL OVERLAP: visualizes a subset/aspect of a table but adds real
     information (trend, distribution, comparison shape) — explain what it adds;
   - ORIGINAL: not derivable from any table (diagrams, per-query distributions,
     curves over data not tabulated).
3. For every DUPLICATE / PARTIAL OVERLAP pair, recommend exactly one of:
   keep both (justify) / drop the figure / drop the table / move one of them to
   an appendix. Consider: which of the two communicates the result faster in a
   defense-reading scenario; supervisor preference for concise main text;
   estimated page savings of each option. Attach a confidence level
   (high/medium/low) to each recommendation.
4. Answer the strategic question from our meeting: given our results, could we
   produce additional GENUINE figures (not table re-plots) that would strengthen
   the thesis — e.g. score-distribution plots, per-query delta histograms,
   funnel/pipeline illustrations? List concrete opportunities with the data
   source each would use (check what exists in thesis_figures/data/), but do NOT
   create them.
5. Summarize: total estimated page savings if all high-confidence
   recommendations are applied.

DELIVERABLE: write the report to
`research_decisions/E1_FIGURE_TABLE_DUPLICATION_REPORT.md` — structured, with
the inventory table, per-pair verdicts + confidence, the genuine-figure
opportunities, and the page-savings summary. This report feeds two downstream
tasks (D2 appendix analysis and D5 conciseness pass), so make verdicts
copy-paste actionable.

FINAL STEP — APPROVAL GATE (do not skip):
After delivering the report, present a short summary in chat and STOP. Wait for
Osman's explicit approval in this chat. Do not edit the task list before he
approves.
- If Osman approves: open `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`,
  find the E1 entry ("- [ ] **E1 — Figure↔table duplication analysis**"), flip
  it to "- [x]" and append " — **DONE <today's date>**" to its title line, then
  add a brief "**Done:**" note (2–4 lines: headline verdicts count, page-savings
  estimate, pointer to the report file) and "⚠️" lines for anything needing a
  team/supervisor decision. Match the formatting style of the completed C1/C2/C6
  entries in that file.
- If Osman approves with modifications: update the report first, then mark done
  noting the modifications.
- If Osman rejects or asks for changes: revise and re-present; do not mark done.
```

---

## Prompt 2 — D2: Appendix-candidates analysis (code + large tables)

```
You are working in the Arabic RAG thesis repo (graduation project, University of
Khartoum). Layout:
- Thesis LaTeX: `University_of_Khartoum__EEE_bachelor_s_thesis_template/`
  (main `1-main.tex`, chapters in `Chapters/`, compiled `1-main.pdf`, ~122 pages).
- Experiment code: `arabic-rag-query-enhancement/` — reusable modules in `src/`
  (subpackages: enhancers, retrievers, evaluation, analysis, utils) and the
  actual experiment notebooks in `experiments/` (e.g.
  `exp_013_csqe_aya_8b.ipynb` = the CSQE implementation,
  `exp_12_hybrid_baseline/` = hybrid RRF/CC fusion, `exp_11_bm25_repetition/`,
  `exp_001_baseline_dense.ipynb`, `exp_002_baseline_bm25.ipynb`, the
  `Query_generator_*.ipynb` family = per-model query enhancement).
- Figure pipeline: `thesis_figures/`.

THIS IS AN ANALYSIS-ONLY TASK. Do NOT edit the thesis, do NOT build the appendix
(that is a separate later task, D3). Your only output is a recommendation report.

CONTEXT: Supervisor directives (Dr. Tahani): the core manuscript (Ch.1–5) must
stay ≤ 100 pages ("ما قلّ ودل"); large code snippets, detailed proofs, and raw
extra data tables MUST move to appendices; appendix pages do NOT count toward
the limit; code must be included as an appendix. Team decisions from our
meeting: the appendix gets KEY code snippets (not everything) — specifically the
CSQE implementation and the retrieval/fusion pipeline were named — plus a link
to a cleaned GitHub repo (being prepared separately). Explicit open question we
want you to answer: WHICH exact code belongs in the appendix vs. stays only in
the repo. Also named as appendix candidates: the full model-comparison table and
the long qualitative query-examples table (referred to as "Table 4.26" in the
meeting — locate the actual long Arabic query-examples table in Ch.4).
If `research_decisions/E1_FIGURE_TABLE_DUPLICATION_REPORT.md` exists, read it
and fold its move-to-appendix verdicts into your recommendation (do not
re-litigate its keep/drop calls).

TASK:
1. Page budget math. From the compiled PDF / .toc, compute: where Ch.1 starts,
   where Ch.5 ends → the real current core page count, and the gap to 100 pages
   (with the margin we'd want, say ~5 pages). This frames how aggressive the
   moves must be.
2. CODE appendix plan. Inspect the notebooks/src named above and propose the
   exact snippets for a code appendix:
   - For each proposed snippet: source (file/notebook + cell), what it shows,
     approximate length in lines, and WHY it earns appendix space (reproducibility
     of a headline claim: CSQE prompt+generation, first-pass retrieval + corpus
     sampling, RRF/CC fusion, query repetition assembly, the pytrec_eval
     evaluation harness).
   - Everything else stays repo-only — list the notable exclusions with one-line
     reasons.
   - Recommend the LaTeX mechanism (e.g. `listings` with a minimal style — note
     the doc compiles with XeLaTeX) and estimate total appendix pages.
3. TABLE moves. Identify every table in Ch.1–5 that is a candidate to move to an
   appendix: the two named above + any table longer than ~half a page that is
   referenced but not essential inline. For each: table number, current size,
   what a 2–3-row inline summary version would look like (if a stub should
   remain), and estimated main-text page savings.
4. Anything else oversized. Flag any other main-text material that fits Dr.
   Tahani's "raw extra data" description (long qualitative example blocks,
   exhaustive per-model listings) with the same treatment.
5. Produce the final recommendation: proposed appendix structure (Appendix A:
   code — with sections; Appendix B: extended tables; …), total estimated core
   page count after all moves, and a prioritized "do these first" list if we
   only want the minimum to get safely under 100.

DELIVERABLE: write the report to
`research_decisions/D2_APPENDIX_CANDIDATES_REPORT.md`. Both team members must
approve it before anything is moved (the moves themselves are task D3 + the
conciseness pass D5) — write it so each item can be approved/rejected line by
line.

FINAL STEP — APPROVAL GATE (do not skip):
After delivering the report, present a short summary in chat and STOP. Wait for
Osman's explicit approval in this chat. Do not edit the task list before he
approves.
- If Osman approves: open `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`,
  find the D2 entry ("- [ ] **D2 — Appendix-candidates analysis**"), flip it to
  "- [x]" and append " — **DONE <today's date>**" to its title line, then add a
  brief "**Done:**" note (2–4 lines: headline numbers — current core page count,
  projected count after moves, pointer to the report) and "⚠️" lines for items
  needing Elhaj's or the supervisor's decision (note in the ⚠️ that Elhaj must
  also approve the report before D3 executes it). Match the formatting style of
  the completed C1/C2/C6 entries in that file.
- If Osman approves with modifications: update the report first, then mark done
  noting the modifications.
- If Osman rejects or asks for changes: revise and re-present; do not mark done.
```

---

## Prompt 3 — D4: New clean GitHub repo (two stages, approval between)

```
You are working in the Arabic RAG thesis repo (graduation project). The
experiment code lives in `arabic-rag-query-enhancement/` inside this repo:
reusable modules in `src/` (enhancers, retrievers, evaluation, analysis, utils),
experiment notebooks in `experiments/` (baselines, `Query_generator_*.ipynb`
per-model family, `exp_013_csqe_aya_8b.ipynb` CSQE, `exp_12_hybrid_baseline/`,
`exp_11_bm25_repetition/`, ablations), plus `configs/`, `requirements.txt`,
`results/`, `docs/`, and assorted working files.

GOAL (team decision from our meeting): create a FRESH, clean, public-facing
GitHub repository for the graduation project — code + notebooks only. Fresh
history (no need to preserve commits — explicitly agreed). Excluded by
agreement: research/working MD files, papers/PDFs, AI-session artifacts
(CLAUDE.md, .claude/, prompts, reports, meeting notes), and anything
private/half-finished. The repo link will be cited in the thesis appendix, so it
must look organized and professional to an examiner who clicks it.

STAGE 1 — PLAN (no side effects). Produce a plan containing:
1. Inventory of `arabic-rag-query-enhancement/`: what exists, what qualifies for
   the clean repo, what gets excluded (call out duplicates like the
   "(1).ipynb" copies and the stray nested `arabic-rag-query-enhancement/
   arabic-rag-query-enhancement/` folder — the clean repo takes exactly one
   canonical copy of each notebook; identify which copy is canonical by content,
   not filename).
2. Data policy: large datasets/indexes do NOT go in the repo (MIRACL is public —
   link it in the README); recommend what small result CSVs (if any) are worth
   including for reproducibility.
3. Notebook hygiene policy: recommend per notebook whether to keep outputs
   (small, informative) or strip them (huge dumps); flag any notebook containing
   API keys, tokens, or personal paths — these MUST be scrubbed.
4. Proposed repo structure (folders, naming — organized by experiment, matching
   how the thesis describes them), proposed repo name (suggest 2–3 options), and
   a drafted README.md: project one-liner, pipeline overview, headline results
   table (take numbers ONLY from this repo's documented results — e.g.
   `CLAUDE.md` reference tables / `docs/experiments/` — do not invent), setup +
   how-to-run, structure guide, license suggestion, and team credits (Mohammed
   Elhaj Sami & Osman Bashir, University of Khartoum, supervised by Dr. Tahani).
5. Staging location: the clean tree will be assembled OUTSIDE this repo (e.g.
   `d:\Projects\Graduation\<repo-name>\`) so we never nest a git repo inside
   graduation-1.
Present the plan in chat and STOP — wait for Osman's approval of: the
include/exclude list, the structure, the name, and the README draft.

STAGE 2 — EXECUTE (only after Osman approves Stage 1, with any corrections he
gives):
1. Assemble the staging folder exactly per the approved plan (copy files, apply
   the approved notebook-output policy, scrub anything flagged, write README.md,
   add a suitable .gitignore and the approved license file).
2. `git init` + a single initial commit in the staging folder.
3. Ask Osman explicitly: create the GitHub repo now or hand off? If he says
   create: use the `gh` CLI (`gh repo create <name> --public --source . --push`
   or private — HIS CALL, ask; if `gh` is not authenticated, give him the exact
   commands to run himself). NEVER push without his explicit go-ahead in this
   chat — pushing publishes.
4. Verify: repo tree matches the plan, README renders, no excluded file leaked
   (grep the staged tree for CLAUDE, .claude, meeting, papers/ remnants, API
   keys).
5. Report the final URL (or the handoff commands) + anything skipped.

FINAL STEP — APPROVAL GATE (do not skip):
After Stage 2's report, wait for Osman's confirmation that the result is
accepted. Then open `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`, find
the D4 entry ("- [ ] **D4 — New clean GitHub repo**"), flip it to "- [x]" and
append " — **DONE <today's date>**" to its title line, then add a brief
"**Done:**" note (2–4 lines: repo name/URL, what was included/excluded in one
phrase, notebook-output policy) and a "⚠️" line reminding that the URL must go
into the thesis code appendix (task D3 — Elhaj). Match the formatting style of
the completed C1/C2/C6 entries in that file. If Osman stops at Stage 1 or the
push is deferred, do NOT mark done — record the state in chat instead.
```
