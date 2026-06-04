# Figures Track — Pending Tasks & Iteration Plan

**Date:** 2026-06-01

---

## The figures full loop — DONE

The figure pipeline now has every link in the chain in place:

1. **Data** — raw CSVs + JSONs committed; large TREC/PKL inputs manifest-tracked.
2. **Per-query metrics** — `01_compute_per_query.ipynb` builds canonical per-query CSVs.
3. **Plotting notebooks** — `02`–`05` produce 28 matplotlib figure variations.
4. **System diagrams** — 7 TikZ standalones (12 originally, 5 archived/restored split) using a shared style file with semantic colours + FontAwesome icons.
5. **Tables** — 12 tables: 5 hand-compiled (Tables 2.1, 2.2, 3.1, 3.2, 4.6) + 7 notebook-produced (Tables 4.1, 4.2, 4.3, 4.4, 4.5, 4.7).
6. **Visual upgrade** — accent palette, per-model colour mapping shared across Fig 4.5 / Fig 4.7.
7. **Embedding mechanics** — `graphicspath` in `1-main.tex`; ready-to-paste LaTeX blocks in `EMBEDDING_PLAN.md`.
8. **Preview compile** — `preview_all_figures.tex` produces a 39-page PDF showing every figure + table at thesis text width with the exact caption + label that will appear in the final thesis. Compile with `xelatex preview_all_figures.tex`.
9. **Joint review surface** — `REVIEW.html` for click-through inspection; `FIGURE_NOTES_MOHAMMED.md` carries Osman's review feedback as tracked items.

**Net:** anyone can now pick up the pipeline, change source data, re-run a notebook, and the new PDF lands in `output/pdf/` ready for the thesis to `\includegraphics`.

---

## What we will iterate on (open figure-side decisions)

These are not blockers — the figures as-is are submission-eligible. They're refinements that will improve the thesis if we have time.

### Iteration 1 — Joint figure-cut decision (Mohammed + Osman, ~30 min sync)

Osman flagged these in `FIGURE_NOTES_MOHAMMED.md` §3 for "do we actually need this?" discussion. I kept them; we need a joint call.

| Figure | Current judgement | Counter-argument | Decision needed |
|--------|--------------------|-------------------|------------------|
| Fig 3.3 (BM25S indexing) | Keep — specific k₁=0.9 b=0.4 + Arabic stemmer + 245-word stoplist are awkward in prose | Could replace with one prose paragraph + the parameters as bullet points | Joint call |
| Fig 3.4 (mDPR encoding) | Keep — encoder name, batch size, FAISS index size, GPU details | Same: could be a methodology bullet list | Joint call |
| Fig 3.7 (Hybrid CC + RRF) | Keep — has CC and RRF equations side-by-side, replacing it with prose loses the comparison | Could keep the equations inline in §3.7 prose and drop the boxes | Joint call |
| Fig 4.1 vs Fig 4.2 | Both kept (one histogram, one CDF) | Osman: feels redundant | Joint call — my pick: keep both, they answer different questions; if forced to cut, drop Fig 4.1 v2 (CDF) and keep v1 hist + Fig 4.2 v1 |

### Iteration 2 — Osman's variation overrides (mechanical, ~10 min)

Osman wants different ★★★ picks for three figures. The variations are already rendered; only the embedding choice changes.

- **Fig 4.3** — use **v2 violin** (not v1 boxplot). `EMBEDDING_PLAN.md` already reflects this.
- **Fig 4.5** — embed **both v1 vertical AND v3 grouped** (not just one). `EMBEDDING_PLAN.md` shows both blocks.
- **Fig 4.9** — use **v2 all-4-metrics** (not v1 NDCG-only). `EMBEDDING_PLAN.md` already reflects this.

### Iteration 3 — New companion figure for Fig 2.1 (Osman §1)

Add a sibling figure to Fig 2.1 showing where the QE layer sits inside the RAG pipeline. The plan: design after §2.1 prose is settled (the figure should follow the claim it supports). Same visual style as Fig 2.1 (`fig_2_1_rag_arch.tex`); add a `Query` → **`QE layer`** → `Retriever` → … arrow with the QE layer highlighted in the thesis accent teal.

Estimated effort: ~15 minutes once the §2.1 framing is clear.

### Iteration 4 — Fig 3.8 readability pass (Osman §2)

Osman flagged Fig 3.8 (CSQE pipeline) as messy *before* the colour upgrade landed. The current colourised version is significantly cleaner, but he hasn't re-reviewed. Two options:

- **(a) Stop here.** The colour upgrade may have addressed his concern. Ask Osman to re-review the new version; only iterate if he still objects.
- **(b) Iterate now.** Possible simplifications: drop the bidirectional arrow between "Extract corpus context" and "Aya LLM"; collapse Stage 1 + Stage 2 entry points; widen the canvas so labels don't crowd.

My recommendation: **(a)** — show him the new version first.

### Iteration 5 — Visual polish: AI-illustrated conceptual figures (long shot, low priority)

If Mohammed wants the thesis to look "more designed" than functional, the highest-return target is Fig 2.1 (RAG architecture) and the new companion. AI image generators (DALL-E / SDXL) could produce stylised illustrations matching the thesis colour palette. **Skip unless Dr. Tahani specifically requests** — the current TikZ versions are submission-ready and read clean.

---

## Pending tasks across the whole thesis (not just figures)

Cross-reference with `research_decisions/THESIS_NEXT_STEPS_TASKS.md` Progress Log. Bold items below are critical-path for Dr. Tahani review.

### Owned by Mohammed

- **Track A — thesis text edits** (~3 h focused writing). Brief at `research_decisions/TRACK_A_PROMPT.md`. Numbers in `STREAM_1_COMPLETION_REPORT.md` §3.
- **Embed figures + tables into chapter `.tex` files**. Use `EMBEDDING_PLAN.md` — ready-to-paste blocks. Compile cleanly verified via `preview_all_figures.tex`.
- **WS6.4 citation fixes** — 10 fabricated BibTeX entries. Corrected entries in `WS6_RESEARCH_REPORT.md` Appendix. Cross-check the §2.4 sentences that cite them (some misstate findings — especially `yoon_2025_llm_retrieval`).
- **Joint figure decisions with Osman** — Iteration 1 above.
- **Fig 2.1 companion** — Iteration 3 above, after §2.1 prose settles.
- **WS5.C.2** — small Pearson/Spearman computation on Qwen family (4 data points, one-line pandas).
- **WS5.D.1** — Ch.5 deep dive (was interrupted recording).
- **WS3.1–3.3** AI-pattern audits — combine with the chapter walks during Track A and the WS6 citation fixes.
- **Ch 1 (introduction)**, **Ch 5 conclusion**, **Abstract (English) + المستخلص** — blocked on supervisor Q2/Q3.
- **Front matter** — cover page, declaration, lists of figures/tables/abbreviations, Roman-numeral pagination.
- **Appendix A — code listings**.

### Owned by Osman

- WS4 ✅ (verifications) and WS6 ✅ (research lookups) — both reports committed.
- **Re-review Fig 3.8** after colour upgrade — confirm whether redesign is still needed.
- **Joint figure decisions** for Iteration 1 (input from Osman needed).
- Sync with Mohammed on the WS6 findings before Track A integrates them.

### Joint / supervisor-gated

- **Supervisor meeting** — Q2 (problem statement framing) and Q3 (Ch 1 narrative direction) gate WS5.A / 5.E / 5.F.
- **Review meeting with Osman** on his WS6 report (Mohammed's feedback owed).

---

## Recommended order for the next 1–2 weeks

1. **Mohammed Track A** in the chapter-editing chat → ~3 h. Use `TRACK_A_PROMPT.md`.
2. **Joint Osman+Mohammed sync** on Iteration 1 figure decisions + WS6 → ~30–45 min.
3. **Embed figures + tables** into chapters using `EMBEDDING_PLAN.md` → ~1.5 h.
4. **WS6.4 BibTeX fixes** + re-verify §2.4 prose → ~2 h.
5. **Hand-compile remaining metadata content** for any tables/sections that need more text → as needed during Track A.
6. **WS3.1–3.3 sweep + WS5.C.2 + WS5.D.1** → ~3 h.
7. **Schedule supervisor meeting** with Q2/Q3 on the agenda. Once answered, unblock Ch.2 reframe → Ch.1 → Abstract.
8. **Finalisation** — front matter, references cleanup, appendix, submission compile.

Realistic timeline to "Dr. Tahani review-ready first draft": ~2–3 focused working weeks with concurrent supervisor scheduling.

---

## How this folder will evolve from here

- `thesis_figures/` source files (notebooks, TikZ, style) are now *stable*. We touch them only for the four iteration items above.
- `output/pdf/` is the read-only contract: chapter `.tex` files `\includegraphics` from here. Don't hand-edit; regenerate from the notebook.
- `archive/system_diagrams_dropped/` may grow (or shrink — if Iteration 1 cuts another figure, we move it there; if Iteration 1 restores any, we move it back to `system_diagrams/`).
- `preview_all_figures.pdf` is a convenience artefact. Don't read it as canonical — the canonical visuals are the per-figure PDFs in `output/pdf/`.

---

## Reference

- **Track A prompt:** `research_decisions/TRACK_A_PROMPT.md`
- **WS1 outcomes (data + canonical numbers):** `research_decisions/STREAM_1_COMPLETION_REPORT.md`
- **WS6 outcomes (citations + literature):** `research_decisions/WS6_RESEARCH_REPORT.md`
- **WS4 verifications:** `research_decisions/WS4_VERIFICATION_REPORT.md`
- **Big-win examples:** `research_decisions/WS4_TASK_4.12_BIGWIN_EXAMPLES.md`
- **Master task list:** `research_decisions/THESIS_NEXT_STEPS_TASKS.md`
- **Per-figure embedding spec:** `thesis_figures/EMBEDDING_PLAN.md`
- **Figure registry + visual feedback:** `thesis_figures/README.md`
- **Visual sign-off page:** `thesis_figures/REVIEW.html`
- **Osman's figure review:** `thesis_figures/FIGURE_NOTES_MOHAMMED.md` (filename misleading — content is Osman's notes)
