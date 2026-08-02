# SILMA 2B BM25 n=1 Conflict — Resolution

**Date:** 2026-07-29
**Status:** RESOLVED — root cause identified in experiment artefacts
**Scope:** `chapter4.tex:311` (Table 4.7) vs `chapter4.tex:462` (Table 4.11). No `.tex` file was edited by this investigation.

---

## 1. Verdict (one line)

**Both numbers are real measurements of DIFFERENT pseudo-document sets.** `0.4277` is SILMA at **temperature 0.1**; `0.4194` is SILMA at **temperature 0.7**. The thesis's own declared protocol (Chapter 3, Table 3.2) says SILMA was run at **temperature 0.1**, so **0.4277 is the protocol-canonical value** — and the repetition sweep (Exp 011) is the artefact that deviates, because it loaded the wrong pickle.

This is **not** a transcription error and **not** a rounding difference. All four metrics differ.

---

## 2. Evidence

### 2.1 The two runs, side by side

| Source | Run | nDCG@10 | Recall@10 | Recall@100 | MRR |
|---|---|---|---|---|---|
| `arabic-rag-query-enhancement/docs/OSMAN_MODEL_COMPARISON_RESULTS.md:65` | Model comparison, **temp 0.1** | 0.4277 | 0.5550 | 0.8115 | 0.4485 |
| `arabic-rag-query-enhancement/experiments/exp_11_bm25_repetition/exp11_all_metrics.json` → `SILMA 2B` → `n=1` | Repetition sweep, **temp 0.7** | 0.41938 | 0.544661 | 0.816819 | 0.440023 |

Quoted rows:

`arabic-rag-query-enhancement/docs/OSMAN_MODEL_COMPARISON_RESULTS.md`, line 62–65 (section "Experiment 1: SILMA Kashif-2B (Temperature 0.1)"):

```
| Retriever | Recall@10 | Recall@100 | NDCG@10 | MRR | vs Baseline |
|-----------|-----------|------------|---------|-----|-------------|
| **Dense (mDPR)** | 0.6289 | 0.8353 | 0.5177 | 0.5508 | +3.7% |
| **BM25S** | 0.5550 | 0.8115 | 0.4277 | 0.4485 | -7.4% |
```

The same file, line 27–28, states the config explicitly:

```
### Temperature 0.1 (More Focused)
- **Dense NDCG@10:** 0.5177 (+3.7% vs baseline)
- **BM25 NDCG@10:** 0.4277 (-7.4% vs baseline)
```

`arabic-rag-query-enhancement/experiments/exp_11_bm25_repetition/exp11_all_metrics.json`, key `SILMA 2B` / `n=1`:

```json
{"recall_10": 0.544661, "recall_100": 0.816819, "ndcg_cut_10": 0.41938, "recip_rank": 0.440023, "num_queries": 2896}
```

`arabic-rag-query-enhancement/experiments/exp_11_bm25_repetition/exp11_ndcg10.csv`, row `SILMA 2B`, column `n=1`: `0.4193804754709807`.

### 2.2 Smoking gun — the repetition sweep loaded the temp-0.7 pickle

`arabic-rag-query-enhancement/experiments/phase4_quick_wins (1).ipynb`, code cell 7 (identical mapping in
`arabic-rag-query-enhancement/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb`, cell 6):

```python
PKL_FILES = {
    'Aya Expanse 8B':  'enhanced_queries_aya_expanse_8b.pkl',
    'Jais-2-8B':       'enhanced_queries_jais_2_8b_chat.pkl',
    'Qwen3-8B':        'enhanced_queries_qwen3_8b.pkl',
    'Qwen 2.5-7B':     'enhanced_queries_qwen25_7b.pkl',
    'Qwen3-4B':        'enhanced_queries_qwen3_4b.pkl',
    'Gemma 3 4B':      'enhanced_queries_gemma3_4b.pkl',
    'Qwen 2.5-3B':     'qwen25_3b_temp07.pkl',
    'Falcon-H1-3B':    'enhanced_queries_falcon_h1_3b_temp01.pkl',
    'SILMA 2B':        'silma_2b_temp07.pkl',      # <-- temp 0.7
}
```

Both SILMA generations exist on disk:

```
arabic-rag-query-enhancement/results/enhanced_queries/silma_2b_temp01.pkl   804,707 bytes
arabic-rag-query-enhancement/results/enhanced_queries/silma_2b_temp07.pkl   788,216 bytes
```

`research_decisions/WS4_VERIFICATION_REPORT.md:53` independently confirmed this months ago:
"SILMA was actually run at **both 0.1 and 0.7** (two result files exist). The notebook's committed config is 0.1."

### 2.3 Proof that no other model is affected — every other model reproduces EXACTLY

The four models present in **both** the model comparison and the repetition sweep agree to 4 d.p. on
**both** nDCG@10 and Recall@10, because both runs consumed the identical pickle. Only SILMA diverges:

| Model | Osman nDCG / R@10 | Exp 011 n=1 nDCG / R@10 | Match? |
|---|---|---|---|
| Aya Expanse 8B | 0.5046 / 0.6284 | 0.5046 / 0.6284 | ✅ exact |
| Qwen 2.5-7B | 0.4682 / 0.6040 | 0.4682 / 0.6040 | ✅ exact |
| Qwen3-8B | 0.4459 / 0.5806 | 0.4459 / 0.5806 | ✅ exact |
| Gemma 3 4B | 0.3447 / 0.4532 | 0.3447 / 0.4532 | ✅ exact |
| **SILMA 2B** | **0.4277 / 0.5550** | **0.4194 / 0.5447** | ❌ **differs on all 4 metrics** |

Agreement to 4 d.p. across 2,896 queries is not coincidence — it proves the pipelines are identical
and that the *only* changed variable for SILMA is the input pseudo-document file.

### 2.4 Corroboration — the temperature story is internally consistent

| SILMA generation | Dense nDCG@10 | BM25 nDCG@10 (n=1) |
|---|---|---|
| temp 0.1 | 0.5177 | 0.4277 |
| temp 0.7 | 0.5052 | 0.4194 |

Temperature 0.1 wins on **both** retrievers, by a similar margin (+0.0125 dense, +0.0083 sparse).
This is exactly what Chapter 3 §3.x claims ("Temperature 0.1 yielded a 2.5% improvement in NDCG@10
over 0.7"). The two conflicting numbers are the same model at the two temperatures Osman tested.

### 2.5 The thesis's own methodology chapter picks temp 0.1

`chapter3.tex:288` (Table 3.2, "Model configurations for the Query2Doc comparison experiments"):

```latex
SILMA 2B & 2B & FP16 & 0.1 & 16 & A100 \\
```

`chapter3.tex:324`: "For SILMA Kashif-2B, two temperature values were compared (0.7 and 0.1).
Temperature 0.1 yielded a 2.5% improvement in NDCG@10 over 0.7, leading to its adoption as the default…"

`thesis_figures/data/raw/table_3_2_gen_hyperparams.csv:2`:
`SILMA Kashif-2B,0.1,0.9,128,temp 0.1 chosen empirically over 0.7 (+2.5%)`

`chapter4.tex:267` (Table 4.6, dense leaderboard) uses SILMA = **0.5177**, which is the **temp 0.1**
dense number. `thesis_figures/output/pdf/table_4_2.tex` annotates that row: `temp 0.1 (chosen over 0.7)`.

**Conclusion:** Chapter 3, Table 4.6 and Table 4.7 are all on temp 0.1. Table 4.11/4.12 and
Figure 4.7 are on temp 0.7. The odd one out is the repetition sweep, not Table 4.7.

---

## 3. Answers to the five questions

**1. Canonical value.**
Protocol-canonical (matching Ch.3 Table 3.2 and Ch.4 Table 4.6) = **0.4277**, from
`arabic-rag-query-enhancement/docs/OSMAN_MODEL_COMPARISON_RESULTS.md:65`.
Latest-run value = 0.4194, from `exp_11_bm25_repetition/exp11_all_metrics.json` (`SILMA 2B` → `n=1`)
and `exp11_ndcg10.csv` row `SILMA 2B`, col `n=1` — but that run used the temp-0.7 pickle, i.e. a
configuration the thesis nowhere declares.

**2. Two different runs?** Yes — definitively. Differing variable: **generation temperature
(0.1 vs 0.7)**, i.e. two different pseudo-document sets (`silma_2b_temp01.pkl` vs `silma_2b_temp07.pkl`).
Everything else (retriever BM25S, 2,896 MIRACL-ar dev queries, max_new_tokens=128, top_p=0.9,
evaluation code) is identical. The temp-0.7 sweep is chronologically **later** (Exp 011, 2026-04-04)
but is **methodologically the deviant one**, because Ch.3 declares SILMA at temp 0.1.

**3. Do Table 4.7's other SILMA cells match?** Yes — Table 4.7's SILMA row is fully self-consistent
with the temp-0.1 source: 0.4277 / 0.5550 / 0.4485, and (0.4277 − 0.4621)/0.4621 = **−7.44% → −7.4%** ✅.
No correction is needed **if** temp 0.1 is kept. Note the sibling data file
`thesis_figures/data/raw/model_comparison_bm25.csv:3` mixes sources — it carries the temp-0.1 n=1
metrics but pairs them with the temp-0.7 `best_ndcg10` 0.4832, producing a **wrong** Δ of 0.0555.

**4. Any other model differing between Table 4.7 and Table 4.11?** **No.** Verified all nine,
`chapter4.tex:304–315` vs `chapter4.tex:453–462`:

| Model | Table 4.7 (line) | Table 4.11 n=1 (line) | Δ |
|---|---|---|---|
| Baseline (no QE) | 0.4621 (304) | 0.4621 (453) | — |
| Jais-2 8B | 0.5122 (306) | 0.5122 (455) | — |
| Aya Expanse 8B | 0.5046 (307) | 0.5046 (454) | — |
| Qwen 2.5 7B | 0.4682 (308) | 0.4682 (457) | — |
| Qwen3-8B | 0.4459 (310) | 0.4459 (456) | — |
| **SILMA 2B** | **0.4277 (311)** | **0.4194 (462)** | **0.0083** |
| Qwen3-4B | 0.4145 (312) | 0.4145 (458) | — |
| Qwen 2.5 3B | 0.4090 (313) | 0.4090 (460) | — |
| Falcon-H1 3B | 0.4038 (314) | 0.4038 (461) | — |
| Gemma 3 4B | 0.3447 (315) | 0.3447 (459) | — |

SILMA is the sole discrepancy. Table 4.7's Recall@10 and MRR columns likewise match `exp11` n=1
for all nine models **except** SILMA, confirming the whole leaderboard was assembled from the sweep
with SILMA's row alone pulled from the older temp-0.1 document.

**5. Recommended presentation.** See §5 below.

---

## 4. Corrected rows (LaTeX, matching surrounding format)

### Option A — RE-RUN (recommended, gold standard). Standardise everything on temp 0.1.

Table 4.7 (`chapter4.tex:311`) stays **unchanged**:

```latex
        5 & SILMA 2B & 2B & 0.4277 & 0.5550 & 0.4485 & $-$7.4\% \\
```

Table 4.11 (`chapter4.tex:462`) and Table 4.12 (`chapter4.tex:485`) are regenerated from a temp-0.1
sweep. Current temp-0.7 values to be replaced (new values unknown until the re-run):

```latex
        SILMA 2B & 0.4194 & 0.4783 & \textbf{0.4832} & 0.4829 & 0.4788 & 0.4494 & 0.4252 & 0.4203 \\
        SILMA 2B & $n=5$ & 0.4832 & 0.6216 & 0.8747 & 0.5048 & +0.0639 \\
```

Cost: BM25S is CPU-only; the full 72-run sweep took ~73 min, so 8 configs for one model is ~8 min.
Inputs already in-repo: `results/enhanced_queries/silma_2b_temp01.pkl` and
`experiments/phase4_quick_wins (1).ipynb` (change one dict value: `'SILMA 2B': 'silma_2b_temp01.pkl'`).

### Option B — NO RE-RUN. Keep 0.4277 in Table 4.7, footnote Table 4.11.

Table 4.7 unchanged (as above). Add to the Table 4.11 caption (`chapter4.tex:447`):

```latex
    \caption{BM25 nDCG@10 for nine models under query repetition. Columns $n \in \{1, 3, 5, 7, 10\}$ are fixed-count repetition (Query2Doc style); columns $\beta \in \{2, 4, 6\}$ are MuGI adaptive repetition where $n$ is computed per-query as $n = \max(1, \lfloor |d| / (|q| \cdot \beta) \rfloor)$. MIRACL Arabic dev (2,896 queries). Best value per model in bold. \emph{Note:} the SILMA 2B row was computed on the temperature-0.7 pseudo-documents rather than the temperature-0.1 set used in Table~\ref{tab:bm25_leaderboard}; its $n{=}1$ value is therefore 0.4194 rather than 0.4277. All eight SILMA configurations are internally consistent at temperature 0.7, so the $\Delta$ in Table~\ref{tab:bm25_best_config} is computed from 0.4194. No other model is affected.}
```

Table 4.12's `+0.0639` is then **correct as printed** and needs no change.

### Option C — NOT RECOMMENDED. Switch Table 4.7 to the temp-0.7 run.

```latex
        5 & SILMA 2B & 2B & 0.4194 & 0.5447 & 0.4400 & $-$9.2\% \\
```

(Rank 5 is preserved: 0.4459 > 0.4194 > 0.4145, so no re-ordering of Table 4.7 is required.)
Rejected because it would put SILMA's BM25 row at temp 0.7 while its **dense** row
(`chapter4.tex:267`, 0.5177) and Ch.3 Table 3.2 (`chapter3.tex:288`) remain at temp 0.1 — trading
one inconsistency for a worse, cross-chapter one.

---

## 5. Every derived figure that moves

### Under Option A or B (recommended) — thesis `.tex` changes

| Location | Current | Action |
|---|---|---|
| `chapter4.tex:311` (Table 4.7 SILMA row) | 0.4277 / 0.5550 / 0.4485 / −7.4% | **No change** |
| `chapter4.tex:410` (Table 4.10, "Avg improvement" BM25 = −5.5%) | −5.5% | **No change** (recomputes to −5.49% with 0.4277) |
| `chapter4.tex:447` (Table 4.11 caption) | — | Option B: add footnote. Option A: no change |
| `chapter4.tex:462` (Table 4.11 SILMA row) | 0.4194 … 0.4203 | Option A: regenerate. Option B: no change |
| `chapter4.tex:485` (Table 4.12 SILMA row, Δ +0.0639) | +0.0639 | Option A: regenerate. Option B: no change |
| `chapter4.tex:320`, `:358`, `chapter5.tex:18` | prose | **No change** — none cite SILMA's BM25 number |

### Under any option — repo data files that are already WRONG and must be fixed

| File | Line | Problem | Fix |
|---|---|---|---|
| `thesis_figures/data/raw/model_comparison_bm25.csv` | 3 | `SILMA 2B,2,0.4277,0.5550,0.8115,0.4485,n=5,0.4832,0.0555` — mixes temp-0.1 n=1 metrics with the temp-0.7 best config; Δ 0.0555 contradicts thesis Table 4.12's +0.0639 | Make both columns come from the same run |
| `thesis_figures/output/pdf/table_4_3.tex` | 6 | `SILMA 2B & 2.0000 & 0.4277 & … & 0.4832 & 0.0555 \\` — same mixed-source Δ | Regenerate after fixing the CSV |
| `arabic-rag-query-enhancement/experiments/phase4_quick_wins (1).ipynb` cell 7 | `'SILMA 2B': 'silma_2b_temp07.pkl'` | Contradicts Ch.3 Table 3.2 | Option A: switch to `silma_2b_temp01.pkl`. Option B: add a comment recording the deviation |

### Figures that currently disagree with each other in the same chapter

Traced via `thesis_figures/notebooks/03_model_comparison.ipynb` cell 2:

- `fig_4_7_repetition_v1/v2/v3` (`chapter4.tex:506`) reads `exp11_ndcg10.csv` → plots SILMA n=1 at **0.4194**.
- `fig_4_8_gains_v1/v2` (`chapter4.tex:513`) reads `model_comparison_bm25.csv` `n1_ndcg10` → plots SILMA at **0.4277**.

So Figures 4.7 and 4.8, three pages apart, already show two different SILMA n=1 points. Whichever
option is chosen, **both figures must be regenerated from the same source** so they agree.

### Values confirmed NOT affected

- Dense Table 4.6 (`chapter4.tex:267`), SILMA 0.5177 / 0.6289 / 0.5508 / +3.7% — temp 0.1 throughout ✅
- `chapter4.tex:358` "2–3B models: +3.7% to +8.9%" — dense figures ✅
- `chapter5.tex:18` "+3.7% (SILMA Kashif-2B)" — dense ✅
- Table 4.10 "Models improving 3/9", "Best +10.8%", "Worst −25.4%" — SILMA is neither ✅
- All hybrid / CSQE results — SILMA not involved ✅

If Option C were chosen instead, the BM25 "Avg improvement" in Table 4.10 (`chapter4.tex:410`) would
have to change **−5.5% → −5.7%** (mean over 9 models: −5.49% with 0.4277, −5.69% with 0.4194).

---

## 6. Recommendation

1. **Preferred — Option A.** Re-run the eight repetition configs for SILMA using
   `silma_2b_temp01.pkl` (~8 min, CPU, all inputs in-repo). This makes Ch.3, Table 4.6, Table 4.7,
   Table 4.11, Table 4.12, Fig. 4.7 and Fig. 4.8 all describe the single temperature-0.1
   configuration the thesis says it used. It also removes the need for any apologetic footnote.
   *Sanity check after the re-run:* confirm SILMA's best config still exceeds 0.4621 so the
   "all nine models beat the baseline" claim in §4 observation 1 (`chapter4.tex:494`) survives.
   This is very likely — temp-0.1 n=1 already starts 0.0083 above temp-0.7 n=1, and repetition
   added +0.0639 at temp 0.7.

2. **If time-constrained — Option B.** Keep 0.4277 everywhere it currently appears and add the
   Table 4.11 caption footnote in §4 above. This is fully honest, costs no compute, and keeps the
   thesis consistent with its own methodology chapter. An examiner comparing the two tables finds
   the explanation immediately.

3. **Do not** silently change either number without disclosure, and do not adopt Option C — the
   thesis must not report SILMA's dense result at temp 0.1 and its sparse result at temp 0.7
   without saying so.

4. **Regardless of option**, fix `thesis_figures/data/raw/model_comparison_bm25.csv:3` — its Δ of
   0.0555 is derived from two different runs and matches neither table in the thesis.

### Secondary observation (out of scope, flagged for completeness)

`chapter3.tex:290` lists **Jais-2 8B at temperature 0.1**, but
`thesis_figures/data/raw/table_3_2_gen_hyperparams.csv:8` records `Jais-2-8B,0.7,…`. That is a
separate documentation conflict in Table 3.2 and should be checked against
`experiments/Query_generator_jais2.ipynb` before submission. It does not affect any Chapter 4 number.
