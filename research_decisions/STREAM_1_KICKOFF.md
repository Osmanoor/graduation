# Workstream 1 Kickoff — Error Analysis

**Status:** Pivoting here. Plots work paused; will resume after WS1 lands. See `thesis_figures/PROGRESS_SNAPSHOT.html` for plot-side context.

**Owner:** Mohammed (sole owner; user-confirmed)
**Parallel work:** Osman is on Workstreams 4 (verifications) and 6 (literature lookups).

---

## What this doc adds

`THESIS_NEXT_STEPS_TASKS.md` is the **source of truth** for *what* to do in Tasks 1.1–1.4. This file adds the *operational* details (file paths, cell line numbers, expected I/O) that aren't in the master task list, so a fresh-chat agent can execute without re-discovering them.

**Read this AND `THESIS_NEXT_STEPS_TASKS.md` Workstream 1 section together.**

---

## Already known from the previous chat

### Central notebook for Tasks 1.2 + 1.3
`arabic-rag-query-enhancement/docs/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb` (1.1 MB local copy; canonical version is in Drive `Colab Notebooks/`).

Key cells (line numbers in the local `.ipynb` JSON, approximate):

| Line | Content |
|------|---------|
| ~11708 | `def per_query_ndcg10(run):` — the per-query helper |
| ~11718–11719 | `scores_csqe = per_query_ndcg10(config_a_run)` / `scores_blind = per_query_ndcg10(aya_blind_bm25_run)` |
| ~11725 | `bm25_scores = per_query_ndcg10(bm25_run)` (BM25 baseline) |
| ~11732 | `deltas = {qid: scores_csqe[qid] - scores_blind[qid] for qid in shared_qids}` |
| ~11772–11778 | `big_wins`, `regressions` lists (thresholds: Δ > 0.3, Δ < −0.1) |
| ~11815 | Failure analysis block (Config A nDCG@10 < 0.1) |
| ~11893–11894 | `delta_values = list(deltas.values())` → fed to `sns.histplot` (already drawn but never saved) |

**Critical observation:** This notebook computes everything Workstream 1 needs *in memory*, then plots from memory and never exports to CSV. The fix for Tasks 1.2 and 1.3 is mostly **adding `to_csv()` cells**, not new computation.

### Drive locations of the raw inputs
- `colab_data/results_phase4/exp_21_csqe_hybrid/`:
  - `bm25_csqe_run.txt` (12 MB) — Config A's BM25+CSQE TREC run
  - `dense_csqe_run.txt` (12 MB) — Dense baseline TREC run for Config A
  - `hybrid_csqe_rrf_k20.txt` (12 MB) — Config A RRF fused output (the headline)
- `colab_data/results/exp_013_csqe_aya_8b_results.pkl` (10 MB) — full CSQE results object
- `colab_data/results_phase4/exp_11_ablations/`:
  - `ablation_table.csv`, `alpha_ablation.csv`, `error_analysis_patterns.csv` (already pulled into `thesis_figures/data/raw/`)

### Already-aggregated numbers we're trying to validate / refine
From `exp_error_analysis_csqe.md` (uses Config A RRF):
- Total queries: 2,896
- CSQE > blind: 1,646 (56.8%)
- CSQE = blind tie: 770 (26.6%)
- CSQE < blind: 480 (16.6%)
- Mean Δ: +0.1890
- 1st-pass IS relevant (n=1061): CSQE+Hybrid = 0.8877
- 1st-pass NOT relevant (n=1835): CSQE+Hybrid = 0.5814
- Short queries (<5 words, n=865): Δ = +0.1990
- Long queries (≥10 words, n=131): Δ = +0.1053
- 258 failures (Config A nDCG@10 < 0.1), of which **claimed 257/258 are "universally irretrievable"** — this is the claim Task 1.1 verifies.

---

## Task 1.1 — Verify dataset integrity (BLOCKING; do first)

### What needs to happen
The 257-of-258 "irretrievable" claim asserts: for those 257 failure queries, their relevant qrel documents do not exist in the indexed Wikipedia corpus. Need to write and run a verification cell.

### Verification logic (pseudocode)
```python
# Inputs:
#   qrels: dict {qid: {docid: relevance}}
#   corpus_docids: set of docids actually present in the BM25S/FAISS index
#   failure_qids: list of 258 qids where Config A RRF nDCG@10 < 0.1

# For each failure_qid, check:
#   1. relevant_docids = [d for d, r in qrels[qid].items() if r > 0]
#   2. present = set(relevant_docids) & corpus_docids
#   3. classify: "irretrievable" (present == ∅) vs "genuine_failure" (present != ∅)

results = {qid: {
    "n_relevant": len(relevant),
    "n_present_in_corpus": len(present),
    "verdict": "irretrievable" if not present else "genuine_failure",
    "missing_docids": list(set(relevant) - set(corpus_docids))[:5],
} for qid in failure_qids}

# Tally
n_irretrievable = sum(1 for v in results.values() if v["verdict"] == "irretrievable")
n_genuine = sum(1 for v in results.values() if v["verdict"] == "genuine_failure")
print(f"Irretrievable: {n_irretrievable} / {len(failure_qids)}")
print(f"Genuine failures: {n_genuine}")
```

### Where to run it
Add as a new cell in `phase4_quick_wins_Ablation_erroranalysis.ipynb`, **after** the failure analysis block (~line 11815) where `failure_qids` is already defined.

### How to get `corpus_docids`
**Option A (cheap, recommended first):** the BM25S index pickle contains the corpus docid list. Path in Drive: `colab_data/corpus_ids.pkl` (24 MB). Load with `pickle.load()` and check.

**Option B (sanity check):** use the FAISS index — same set of docids since both retrievers ran on the same MIRACL corpus dump.

### Outcome branches
- **n_irretrievable ≈ 257** → claim holds. Update §4.10 wording with the verified number. Continue to 1.2/1.3.
- **n_irretrievable << 257** → claim is wrong. The failures are real retrieval failures. Rewrite §4.10 narrative. Re-think recovery-rate framing. Continue to 1.2/1.3 but with corrected baseline counts.
- **n_irretrievable wildly different from anything** → there's an indexing/preprocessing bug. **STOP. Consult before reindexing** — could blast back through all baselines.

### Estimated effort
30 minutes to write + run + interpret. Single Colab cell.

---

## Task 1.2 — Re-run error analysis with word-based buckets

### ✅ DECISION (2026-05-31): Option A — unify everything on the original 1–3 / 4–8 / 9+ word boundaries

Both error analyses use **Short 1–3 / Medium 4–8 / Long 9+ words** (these are whitespace word counts; the thesis word "tokens" = words — confirmed against the per-query JSON, min 3 / max 17 / mean 5.74). We unify the *second* analysis (§4.10 CSQE, currently <5/5–9/≥10) onto the *first's* boundaries, NOT the other way around.

**Rationale:**
- Preserves the project's founding motivation — §4.2's short-query gap (0.240 vs 0.406, 41%) — the assumption the whole project is built on. Re-bucketing to <5 would have shrunk it to ~17%.
- One consistent scheme everywhere; no signposting hack.
- The "cost" reframes as a strength: CSQE improves **all** query lengths substantially (vs mDPR baseline: short +0.291, medium +0.336, long +0.293) — a *general* method, not a short-query patch. And in **relative** terms short still benefits most (+121% vs +72% for long), so "short queries helped most" survives when stated as % improvement.

**Threshold systems (sub-decision 1 below): KEEP the absolute Failed<0.3 / Mediocre / Successful thresholds.** The "39% of queries fail at baseline" statistic is strong motivation; arbitrary-but-conventional cutoffs are a minor, common thing in IR. Do NOT switch to distributional (that earlier recommendation was the prior chat's; reassessed and reversed).

**Execution:** §4.2 (mDPR) numbers recomputed locally already (`thesis_figures/data/computed/`). §4.10 numbers (CSQE vs Aya-blind Δ) come from the per-query CSV produced by the Task 1.3 cell, rebucketed locally to 1–3/4–8/9+ — no extra notebook runs. The blind per-query run is NOT saved in Drive, so the 1.3 cell must run once to produce it.

### Current state in the thesis (grounded grep)
The thesis already contains BOTH bucket schemes — they're inconsistent and need unifying:

| Section | File:line | Scheme | Values |
|---------|-----------|--------|--------|
| §3.3 — Short Query Performance Gap | `Chapters/chapter3.tex:78-80` | **token-based** | Short 1–3 / Medium 4–8 / Long 9+ tokens → 0.240 / 0.367 / 0.406 |
| §4.10 — performance by length | `Chapters/chapter4.tex:867-880` | **word-based** | Short <5 / Medium 5–9 / Long ≥10 → 0.4793 / **---** / 0.6003 |

The **Medium row in §4.10 is literally `---`** (line 874) — that's Task 5.C.20's "drop or populate" trigger, and the simplest fix is to populate it from the recomputation.

The supporting analysis doc (`research_decisions/error_analysis_phase1_quantitative.md`) uses token-based throughout — needs synchronizing once thesis is updated.

### What 1.2 produces
A single per-query dataframe and a Short/Medium/Long table that replaces the §3.3 token-based table and fills in the §4.10 Medium row. Same scheme used everywhere in the thesis afterwards.

### Sub-decisions
1. **Failed/Mediocre/Successful absolute thresholds (§3.3 lines 110-112).** Currently <0.3 / 0.3–0.7 / ≥0.7. The "<0.3 = failed" cutoff has no published justification. Options:
   - (a) Keep but justify — quartile cutoffs from the empirical distribution.
   - (b) Drop fixed thresholds; present distributionally (CDF + a single summary stat like 'median 0.49').
   - **Recommended:** (b). Decouples §3.3 from arbitrary thresholds; pairs cleanly with Fig 4.2 v1 (which already shows the CDF).
2. **Stay with mDPR baseline.** §3.3 documents the baseline retriever's error pattern; the rerun is on the same per-query mDPR data, just rebucketed.

### Files / cells involved
- **Per-query mDPR NDCG@10:** `arabic-rag-query-enhancement/results/baseline_dense/exp_001_quantitative_analysis.json` (also copied at `thesis_figures/data/raw/baseline_dense_per_query.json`).
- **Topics for word counts:** `arabic-rag-query-enhancement/data/processed/exp001_topics.json` (also at `thesis_figures/data/raw/miracl_topics_dev.json`).
- **No Colab needed.** Pure pandas, runs locally.

### Executable snippet
Paste into a Python REPL or a fresh local notebook. Works from anywhere; uses relative path to the repo root.

```python
import json
import pandas as pd
from pathlib import Path

ROOT = Path('c:/Users/moham/Desktop/graduation')

# 1) Load per-query mDPR NDCG@10
pq = json.loads((ROOT / 'arabic-rag-query-enhancement/results/baseline_dense/exp_001_quantitative_analysis.json').read_text(encoding='utf-8'))
df = pd.DataFrame([
    {'qid': qid, 'ndcg10': v['ndcg_10'], 'recall10': v['recall_10'], 'mrr': v['mrr']}
    for qid, v in pq['per_query_metrics'].items()
])

# 2) Load topics, compute word count per qid
topics = json.loads((ROOT / 'arabic-rag-query-enhancement/data/processed/exp001_topics.json').read_text(encoding='utf-8'))
def get_text(v):
    return v if isinstance(v, str) else v.get('query', v.get('text', ''))
words = pd.DataFrame([
    {'qid': str(qid), 'query': get_text(v), 'word_count': len(get_text(v).split())}
    for qid, v in topics.items()
])

# 3) Merge + bucket (word-based, matches §4.10 scheme)
df['qid'] = df['qid'].astype(str)
m = df.merge(words, on='qid')
def bin3(n):
    if n < 5: return 'Short (<5 words)'
    if n < 10: return 'Medium (5–9 words)'
    return 'Long (≥10 words)'
m['bucket'] = m['word_count'].apply(bin3)

# 4) Summary table for §3.3 + §4.10
bucket_order = ['Short (<5 words)', 'Medium (5–9 words)', 'Long (≥10 words)']
summary = (m.groupby('bucket')
            .agg(n=('ndcg10', 'size'),
                 mean_ndcg10=('ndcg10', 'mean'),
                 median_ndcg10=('ndcg10', 'median'))
            .reindex(bucket_order))
summary['pct'] = (summary['n'] / summary['n'].sum() * 100).round(1)
print(summary)

# 5) Save for downstream use
out_dir = ROOT / 'thesis_figures/data/computed'
out_dir.mkdir(parents=True, exist_ok=True)
m[['qid','ndcg10','recall10','mrr','word_count','bucket']].to_csv(
    out_dir / 'baseline_dense_per_query_with_length.csv', index=False)
summary.to_csv(out_dir / 'length_bucket_summary.csv')
```

### Expected outputs (numbers you'll quote)
- `thesis_figures/data/computed/baseline_dense_per_query_with_length.csv` — full per-query dataframe.
- `thesis_figures/data/computed/length_bucket_summary.csv` — the table you paste into §3.3 and use to fill §4.10's `---` row.
- Three numbers to validate against the existing §4.10 Short (0.4793) and Long (0.6003) — those are CSQE+Hybrid values, NOT mDPR baseline. **Don't confuse them.** The mDPR-baseline numbers from 1.2 will be lower (mDPR alone is 0.4993 average).

### Thesis edits after the snippet runs
- **`chapter3.tex` lines 76–82**: replace the token-based table with the word-based one. Rewrite the surrounding paragraph (currently quotes "0.240 vs 0.406" → 59% gap) with the new mDPR word-based numbers.
- **`chapter4.tex` line 874**: fill the Medium row from `csqe_error_patterns.csv` Medium values once Task 1.3's per-query CSV exists (Task 1.3 produces the CSQE side; this task produces the mDPR side). Note: §4.10 reports CSQE+Hybrid per-bucket, so the Medium fill needs the CSQE per-query data, not just 1.2's output.
- **`research_decisions/error_analysis_phase1_quantitative.md`**: update lines 29–35 (Performance by Length Bucket table) and lines 99–105 (Length Distribution of Failed Queries) with word-based buckets. This doc is the supporting analysis — keep it in sync.

### Estimated effort
- Snippet run + verify: 15 min.
- Thesis text update in §3.3: 30 min (table swap + paragraph rewrite).
- §4.10 Medium row fill: 15 min (one-cell change once 1.3 lands).
- Supporting doc sync: 15 min.
- Total: ~75 min (independent of 1.1 except for the 258-query interpretation in §4.10 Medium row).

---

## Task 1.3 — Re-run per-query analysis for Config A

### What needs to happen
This is the **same Colab patch** I mentioned in the plot context, but framed as a thesis task rather than a figure fix. Two effects:
- (a) Produces the per-query CSV that unblocks Fig 4.12.
- (b) Replaces every Config-C reference in §4.10 with verified Config-A numbers (recovery rate, first-pass dependence, big-win counts, etc.).

### The Colab patch (add right after line 11732)
```python
import pandas as pd
out = pd.DataFrame([
    {
        "qid": q,
        "ndcg10_csqe_hybrid": scores_csqe[q],         # Config A RRF
        "ndcg10_aya_blind_bm25": scores_blind[q],      # Aya blind baseline
        "ndcg10_bm25_baseline": bm25_scores[q],        # BM25 no QE
        "delta_csqe_vs_blind": deltas[q],
    }
    for q in shared_qids
])
out.to_csv("results/csqe_vs_blind_per_query.csv", index=False)

# In Colab, also push the CSV to Drive so it persists:
import shutil
shutil.copy("results/csqe_vs_blind_per_query.csv",
            "/content/drive/MyDrive/graduation project/colab_data/results_phase4/csqe_vs_blind_per_query.csv")

# Optional: trigger download
try:
    from google.colab import files
    files.download("results/csqe_vs_blind_per_query.csv")
except ImportError:
    pass

print("Saved:", len(out), "rows")
```

### Verification (do before trusting the CSV)
After the patch runs, manually check:
- Row count = 2,896 (matches Aya blind + Config A intersection)
- Mean `delta_csqe_vs_blind` ≈ +0.1890 (sanity check against `exp_error_analysis_csqe.md`)
- 56.8% of rows have `delta > 0`
- Spot-check 3–5 qids against the existing aggregate tables

### Re-derivation pass after CSV is in hand
With the CSV local in `thesis_figures/data/raw/csqe_vs_blind_per_query.csv`, re-derive (locally, no Colab needed):
- Big wins: `(delta > 0.3).sum()` — currently claimed 1,061
- Regressions: `(delta < -0.1).sum()` — currently claimed 367
- Type-A/B/C regression breakdown (52% / 36% / 12%) — needs per-query inspection of regressions; this is where Mohammed personally vets each step per the task description
- First-pass dependence split: needs the additional column `first_pass_relevant` (0/1) → has to come from the Colab notebook too. Either add another export or compute downstream by intersecting per-query BM25 top-1 with qrels.

### Where the Config-C → Config-A swap matters in the thesis
§4.10 currently uses Config C numbers in places. After 1.3, every numeric reference in §4.10 should pull from this CSV. Watch for:
- "56.8% recovery rate" — should match new value
- "0.8877 vs 0.5814 first-pass dependence" — verify (these were Config A; should be unchanged but confirm)
- Recovery rate definition — pairwise (CSQE − blind > 0) vs absolute (CSQE > some threshold)

### Estimated effort
- Colab cell + run: 15 min
- Download + local re-derive: 30 min
- Thesis text update §4.10: 1–2 hours (this is the real time sink)

### Dependencies
**Hard dependency on 1.1.** If 1.1 reveals a corpus indexing bug, the entire Config A run may need to be regenerated. Don't start 1.3 until 1.1 is green.

---

## Task 1.4 — Threshold-system reconciliation

### Current state in the thesis (grounded grep)
The thesis has **three** threshold definitions, not two — and they actually mix inside the regression-type classification. Catalogue:

| System | File:line | Question it answers | Thresholds |
|--------|-----------|--------------------|--------|
| **Absolute** | `chapter3.tex:110-112` | How well-served is this query by the retriever? | Failed <0.3 / Mediocre 0.3–0.7 / Successful ≥0.7 |
| **Pairwise** | `chapter3.tex:458-460` | How does CSQE compare to blind per query? | Failure <0.1 / Big Win >0.3 / Regression <-0.1 |
| **Hybrid (regression sub-typing)** | `chapter3.tex:470-472` | What kind of regression is this? | Type A: BM25 ≥0.3 / Type B: BM25 <0.1 / Type C: 0.1–0.3 |

The **hybrid case uses absolute BM25 score thresholds (lines 470–472) to classify pairwise comparisons** — that's not wrong, but it's where most readers will get confused because the same number (0.3) means different things in §3.3 ("Mediocre boundary") and §3.9 ("Type A boundary"). Reconciliation is mostly signposting + caption alignment, not a numeric change.

Also: `chapter4.tex:43-58` uses absolute thresholds (Failed/Mediocre/Successful) for the overall failure rate; `chapter4.tex:829` uses the pairwise <0.1 for the 258 failure queries. Both are correct given their context but the reader has to track which is which.

### Recommended resolution
**Keep all three; signpost explicitly.** Add one paragraph at the start of §3.3 (right before the Failed/Mediocre/Successful list) introducing the three systems with an example of orthogonality. Then leave existing thresholds alone.

#### Exact paragraph to insert (`chapter3.tex`, before line 110)
```latex
\subsubsection*{Note on threshold systems used in this thesis}
Three threshold systems are used throughout this thesis to answer different
questions. The \emph{absolute} system (this section) classifies each query's
retrieval quality independently and is used to characterise dataset difficulty
and to report overall failure rates. The \emph{pairwise} system (Section~3.9)
compares the per-query nDCG@10 of two systems and is used in error-analysis
tables that contrast CSQE with the blind baseline. A third \emph{hybrid}
classification (Section~3.9, regression sub-typing) uses absolute BM25 score
thresholds to label pairwise regressions by their root cause. The three systems
are orthogonal: a single query can be classified as ``Mediocre'' on the
absolute system, ``Big Win'' on the pairwise system, and ``Type~A regression''
on the hybrid system without contradiction, because each measures a distinct
aspect of retrieval behaviour.
```

### Sweep — where threshold references live
To check no caption or paragraph in Chapter 4 cites the wrong system, the agent should grep both chapters for the numeric thresholds and verify each match cites the right section:

```bash
# threshold-numeric mentions, with context
grep -n "0\.3\|0\.1\|0\.7\|Failed\|Mediocre\|Successful\|Big Win\|Big win\|Regression\|Failure\|Type A\|Type B\|Type C" chapter3.tex chapter4.tex
```

Each hit should be classifiable as: absolute-system, pairwise-system, hybrid-system, or unrelated (e.g. temperature 0.1, model name "Type A"). For each, verify the surrounding text cites the right §.

### Known caption alignments after this task
- **Fig 4.2** (failure cliff at NDCG@10 < 0.3): cite absolute system (§3.3). Already correct in my notebook.
- **Fig 4.12** (per-query Δ histogram, shaded bands at ±0.1 regression, +0.3 big win): cite pairwise system (§3.9). My notebook 05 already uses these bands.
- **Fig 4.15** (regression type breakdown 52/36/12%): cite hybrid system (§3.9 lines 470-472). My notebook 05 already uses these percentages from `csqe_error_patterns.csv`.

### Estimated effort
- Sweep + alignment check: 30 min.
- Insert signposting paragraph: 5 min.
- Caption text updates in any §4 mentions that cite the wrong system: 20 min.
- Total: ~55 min. Pure-text task, no data dependency, can run in parallel with 1.2 and 1.3.

---

## Recommended execution order

1. **Task 1.1** (~30 min) — gate. Verification cell + outcome interpretation. If green, continue. If red, stop and consult before reindexing.
2. **Task 1.2** (~75 min) and **Task 1.4** (~55 min) — both run locally, no Colab. 1.2 is data work (pandas + thesis text); 1.4 is pure text. Can interleave.
3. **Task 1.3** (~15 min Colab + ~30 min local re-derive + 1–2 hours thesis text update for §4.10) — starts after 1.1 is green. Provides the per-query CSV that fills 1.2's §4.10 Medium row.

**Total estimated effort for Workstream 1:** half a day of focused work. The data side (1.1 + 1.2 snippet + 1.3 Colab cell) is ~90 min. The thesis text rewrites (§3.3 + §4.10 + signposting + supporting docs) is the rest.

---

## Open questions for Mohammed before / during the next chat

1. **Distributional vs absolute thresholds in §3.3** (Task 1.2 sub-decision 1) — your call. My recommendation is distributional, but if §3.3 has a structural reliance on the Failed/Mediocre/Successful labels, going distributional means rewriting more of the section.
2. **Should Aya blind per-query also include the Aya-blind Recall@10 and MRR**, or is per-query NDCG@10 enough for §4.10? Including more metrics means adding columns to the Colab patch. Cheap to add now, expensive to add later.
3. **§4.10 narrative direction after 1.1** — depends on outcome:
   - If "irretrievable" claim holds: minor wording tweak, §4.10 stays as-is.
   - If claim fails: §4.10 needs a partial rewrite. Decide between two narratives:
     - (a) "Failures are genuine retrieval limitations" — straightforward.
     - (b) "Failures are predominantly indexing-pipeline artefacts that need separate study" — only if 1.1 reveals a specific pipeline bug.

---

## How to start the next chat

Recommended opening message:

> Continuing Workstream 1 from `research_decisions/STREAM_1_KICKOFF.md` and `THESIS_NEXT_STEPS_TASKS.md`. Mohammed owns 1.1–1.4. Today's goal is Task 1.1 + start 1.3. Plots work paused (see `thesis_figures/PROGRESS_SNAPSHOT.html` for what's blocked on this).

The agent should:
1. Read this file and the Workstream 1 section of `THESIS_NEXT_STEPS_TASKS.md`.
2. Confirm with Mohammed which sub-decisions (open questions above) are settled.
3. Start with Task 1.1: write the verification cell (using the Drive notebook for execution), run it, interpret outcome, route to 1.2/1.3 or escalate.

**Files the next agent should read in order:**
1. `research_decisions/STREAM_1_KICKOFF.md` (this file)
2. `research_decisions/THESIS_NEXT_STEPS_TASKS.md` Workstream 1 section
3. `arabic-rag-query-enhancement/docs/experiments/exp_error_analysis_csqe.md` (the existing aggregated results)
4. `research_decisions/error_analysis_phase1_quantitative.md` (the original error analysis being rerun in 1.2)

---

## Returning to plots after Workstream 1 finishes

After 1.1–1.4 land:
- The per-query CSV from 1.3 unblocks Fig 4.12.
- The 3-bin length scheme from 1.2 closes Decision D1 in the plot snapshot.
- Threshold decision from 1.4 closes D2.
- Then a single render session: mechanical alignment edits (D3, D4), execute notebooks 02–05, compile TikZ, polish Excalidraw. Estimated ~3 hours focused work, no decisions needed because everything is settled.

See `thesis_figures/PROGRESS_SNAPSHOT.html` for the full plot-side picture.
