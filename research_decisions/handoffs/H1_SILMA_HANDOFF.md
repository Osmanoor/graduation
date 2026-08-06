# Handoff — H1: SILMA repetition sweep re-run

**For:** a dedicated parallel Claude chat.
**Owner:** Elhaj · **Created:** 2026-08-06
**Scope:** ONE task. Do not touch anything else in the thesis.

---

## 1. The prompt (paste this into the new chat)

> I'm Mohammed (Elhaj), finishing my B.Sc. thesis at the University of Khartoum. This chat has
> exactly one job: fix task **H1**, a data inconsistency in Chapter 4 of my thesis.
>
> Read these first, in order:
> 1. `research_decisions/handoffs/H1_SILMA_HANDOFF.md` — this file, the full brief
> 2. `research_decisions/SILMA_CONFLICT_RESOLUTION.md` — original root-cause analysis
> 3. `research_decisions/SILMA_TEMPERATURE_RATIONALE_CHECK.md` — the adjudication
> 4. `CLAUDE.md` — project facts and canonical numbers
>
> **The problem in one line:** the Exp 1.1 repetition sweep loaded SILMA's temperature-**0.7**
> expansions while every other model used temperature **0.1**, so Table 4.7 prints 0.4277 and
> Table 4.11 prints 0.4194 for the same configuration.
>
> **What to do:** re-run SILMA's 8 repetition configurations from the temp-0.1 expansions, then
> update Tables 4.11 and 4.12. Details, file paths, the sanity check and the fallback are all in
> the handoff file. Follow it exactly.
>
> **Working rules:** verify before asserting — check numbers against the raw data, not against
> memory. Show me the diff before applying any `.tex` edit. Do not touch figures — those belong
> to Osman. If anything is ambiguous, ask me rather than guessing.

---

## 2. The problem

`phase4_quick_wins (1).ipynb` cell 7 mapped `'SILMA 2B'` to `silma_2b_temp07.pkl`. Every other
model in the sweep loaded the same pickle as the model-comparison run. SILMA is the only
deviation, and it is the only model with both temperature variants on disk.

Consequence, both in the printed thesis right now:

| Location | Value | Temperature |
|---|---|---|
| `chapter4.tex:313` — Table 4.7, SILMA BM25 n=1 | **0.4277** | 0.1 ✅ canonical |
| `chapter4.tex:464` — Table 4.11, SILMA n=1 | **0.4194** | 0.7 ❌ deviant |

Same configuration, two numbers. **Table 4.7 is canonical** — it uses the same temp-0.1 pickle
as the dense results and as Ch.3 Table 3.2.

**The temperature *decision* is not in question.** SILMA at 0.1 was chosen deliberately and
empirically by Osman (+2.5% over 0.7). Only the sweep's file mapping was wrong.

---

## 3. Osman already fixed the notebook — the re-run has NOT happened

Commit `0d7bfe3` changed one line in
`arabic-rag-query-enhancement/experiments/phase4_quick_wins (1).ipynb`:

```
'SILMA 2B': 'silma_2b_temp07.pkl'   →   'SILMA 2B': 'silma_2b_temp01.pkl'
```

So the notebook is correct. **Nobody has executed it.** That is this task.

---

## 4. What to run

| | |
|---|---|
| Notebook | `arabic-rag-query-enhancement/experiments/phase4_quick_wins (1).ipynb` |
| Input | `results/enhanced_queries/silma_2b_temp01.pkl` (804,707 B, already on disk) |
| Configs | 8 total: `n ∈ {1, 3, 5, 7, 10}` and `β ∈ {2, 4, 6}` |
| Compute | **BM25S is CPU-only. ~8 minutes. No LLM inference** — the expansions already exist |
| Scope | **SILMA only.** The other 8 models are already correct; do not re-run them |

**Google Drive is connected to this chat** and holds the project files if they are not local.

### The sanity check — do this first

The re-run's **n=1 value must come out as 0.4277**. That is the same computation that produced
Table 4.7, so it doubles as proof the pipeline is wired correctly.

**If n=1 is not 0.4277, stop and report.** Something else is wrong and the other seven numbers
cannot be trusted.

---

## 5. What to update after a successful re-run

### Table 4.11 — `chapter4.tex:464`
```
SILMA 2B & 0.4194 & 0.4783 & 0.4832 & 0.4829 & 0.4788 & 0.4494 & 0.4252 & 0.4203 \\
```
Columns: `n=1, n=3, n=5, n=7, n=10, β=2, β=4, β=6`. All eight become the new values.
⚠️ The **bold** marks the row's best config — currently `n=5` at 0.4832. If the new best is a
different column, the bold moves.

### Table 4.12 — `chapter4.tex:487`
```
SILMA 2B & $n=5$ & 0.4832 & 0.6216 & 0.8747 & 0.5048 & +0.0639 \\
```
Columns: best config, NDCG@10, Recall@10, Recall@100, MRR, Δ vs n=1.
⚠️ **Δ is computed against the n=1 value in the same run**, so it changes even if the best
config stays `n=5`.

### Two claims to re-verify after the numbers change

1. **`chapter4.tex:494`** states all nine models beat the BM25 baseline of **0.4621**. SILMA's
   new best must still exceed it. Very likely — temp-0.1 n=1 starts 0.0083 above temp-0.7 n=1,
   and repetition added +0.0639 at temp 0.7.
2. **`chapter4.tex:495`** describes which models peak at adaptive β vs fixed n. If SILMA's
   optimum moves from `n=5` to a β column, that sentence needs checking.
3. **`CLAUDE.md`** "Reference Baselines — BM25 with Query Repetition" table has a SILMA row
   (`0.4194 | n=5 | 0.4832 | +0.0639`). Update it too.

---

## 6. If the re-run cannot be done

**Do NOT edit Table 4.11's n=1 cell to 0.4277 on its own.** That cell would then be a temp-0.1
number sitting beside seven temp-0.7 numbers in the same row — internally inconsistent, and
harder to defend than the current state. It also asserts a result that was never computed.

**Use Option B instead** (already recorded as legitimate in the task file):

- Keep **0.4277** in Table 4.7 — unchanged.
- Add a footnote to Table 4.11: *"SILMA's repetition sweep was executed using the
  temperature-0.7 expansions; all other models used their temperature-0.1 expansions
  (Table 3.2)."*
- Table 4.12's Δ = +0.0639 **stays correct as printed** — it is an internally consistent
  temp-0.7 delta.
- Report to Elhaj that Option B was taken and why.

**Rejected outright:** changing Table 4.7 to 0.4194. That would split SILMA's dense and sparse
rows across two different temperatures.

---

## 7. Out of scope — do not touch

- **Figures 4.7 and 4.8.** They currently plot different SILMA values because they read
  different CSVs. They need regenerating from one source regardless of this task's outcome —
  **that is Osman's**, under the figures/tables split.
- `thesis_figures/data/raw/model_comparison_bm25.csv:3` and
  `thesis_figures/output/pdf/table_4_3.tex:6` pair temp-0.1 n=1 metrics with the temp-0.7 best
  config (Δ=0.0555, matching neither table). **Flag it; do not fix it** — also Osman's.
- Any other chapter, table, or task.

---

## 8. Definition of done

- [ ] Sanity check passed: re-run n=1 = 0.4277
- [ ] Tables 4.11 and 4.12 updated, bold moved if the optimum changed
- [ ] `chapter4.tex:494` and `:495` re-verified against the new numbers
- [ ] `CLAUDE.md` SILMA row updated
- [ ] Thesis rebuilt: 0 errors, 0 undefined references
- [ ] Figures 4.7/4.8 flagged for Osman, not touched
- [ ] Task H1 marked done in `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md` with the
      new numbers recorded
