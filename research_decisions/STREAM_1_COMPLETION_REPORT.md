# Workstream 1 — Completion Report

**Date:** 2026-05-31 · **Owner:** Mohammed (sole owner of 1.1–1.4) · **Status:** all data/analysis for 1.1–1.4 complete and verified; only Mohammed-owned thesis-text edits remain.

> **Note for Osman:** nothing in this report is delegated to you. Every number is already researched and resolved (including the 0.364-vs-0.4993 item in §2 — that is *confirmed and closed*, not an open question). The remaining work is Mohammed editing the thesis text. The WS4/WS5 cross-references in §4 just record which of *your* existing items WS1 has now *answered for you* (so you can close them), not new tasks.

This report covers: (1) task results 1.1–1.4, (2) the exact thesis changes needed, (3) a newly-surfaced nDCG-computation issue, (4) cross-workstream touchpoints, (5) thesis-figures impact, (6) artifacts produced, (7) the open decision.

---

## 1. Task results

### Task 1.1 — Dataset integrity ✅ (claim REFUTED)
Direct corpus-membership check over the full **2,061,414-doc** MIRACL Arabic corpus (= canonical size → index complete, no preprocessing bug, no reindex).

- Of 258 failures (Config A RRF nDCG@10 < 0.1): **0 irretrievable / 258 genuine retrieval failures** — every one has ≥1 relevant doc in the corpus.
- 199 also miss on the BM25 baseline (present but un-retrieved by any method); **58 are retrieved by BM25 alone (43 with BM25 ≥ 0.3) but lost by the CSQE hybrid** = genuine regressions. qid 1060 (originally "the sole genuine failure") is just one of those 58.
- **What went wrong originally:** the notebook's scatter labelled "CSQE<0.1 AND blind<0.1" points as *"irretrievable"* — a retrieval statement — and the write-up escalated it to a never-tested *corpus-membership* claim ("passage absent from the dump"). No membership check was ever run.
- Verdict CSV: `thesis_figures/data/computed/task_1_1_failure_corpus_check.csv`. Script: `thesis_figures/notebooks/task_1_1_corpus_integrity.py`.

### Task 1.2 — Consistent length buckets ✅ data done · DECISION: Option A
- **Decision:** unify everything on **Short 1–3 / Medium 4–8 / Long 9+ words** (preserves the founding §4.2 short-query motivation). "tokens" in the text = whitespace words.
- **Thresholds:** KEEP the absolute Failed/Mediocre/Successful system (do not go distributional).
- **⚠ New issue (see §3 below):** the existing §4.2 numbers use a non-standard nDCG and must be recomputed.

### Task 1.3 — Per-query Config A analysis ✅ (CSV generated + fully validated)
`csqe_vs_blind_per_query.csv` (2,896 rows, in `thesis_figures/data/raw/`) reproduces **every** claimed aggregate exactly:

| Quantity | Re-derived | Claim |
|---|---|---|
| Big wins (Δ>0.3) | 1061 | 1061 ✓ |
| Regressions (Δ<−0.1) | 367 | 367 ✓ |
| Win/tie/loss | 1646 / 770 / 480 | 56.8 / 26.6 / 16.6% ✓ |
| Mean Δ / CSQE / blind | 0.1890 / 0.6936 / 0.5046 | same ✓ |
| First-pass dependence | 0.8877 / 0.5814 | same ✓ |

- **First-pass definition resolved:** "first-pass relevant" = **BM25 retrieves a relevant doc at rank 1 (top-1, qrel≥1)** → n=1061, CSQE=0.8877; not-relevant n=1835, CSQE=0.5814. (Note: CSQE *grounding* uses top-5, so §4.10 wording should say "top-1" precisely. This is also WS4 Task 4.8.)

### Task 1.4 — Threshold reconciliation ✅ verified (plan ready, pure text)
Three orthogonal systems confirmed: **absolute** (`chapter3.tex:109-113`), **pairwise** (`chapter3.tex:458-460`), **hybrid regression-subtyping** (`chapter3.tex:470-472`). Resolution: keep all three + one signposting paragraph before line 109. No data dependency.

---

## 2. CONFIRMED — the §4.2 baseline error-analysis file is buggy (READ FIRST)

> **Status: RESOLVED in this WS1 session — no open question, nothing delegated.** Mohammed researched this and the analysis below proves it; the exact corrected numbers and edits are known (listed here + in §3). This is *not* a task for Osman or a WS4 verification. The only thing left is Mohammed applying the edits.

**Finding:** the entire §4.2 / §3.3 baseline error analysis is sourced from `exp_001_quantitative_analysis.json`, whose custom analysis code computed **multiple metrics incorrectly**. It disagrees with the canonical mDPR run on nDCG, coverage, zero-count, **and** correlation.

**Proof it's the file that's wrong (not my recomputation):** I recomputed all metrics directly from the canonical run `exp_001_baseline_dense.txt` (100 docs/query, complete) with `pytrec_eval`, and it reproduces **all four published headline numbers exactly** — nDCG@10 0.4993, Recall@10 0.6156, Recall@100 0.8407, MRR 0.5328. So my recomputation **is** the canonical baseline; the analysis file is the outlier.

| §4.2 / §3.3 quantity | thesis section | OLD (buggy file) | **CORRECTED (canonical run)** |
|---|---|---|---|
| Short 1–3 words nDCG@10 | §4.2.2 | 0.240 | **0.345** |
| Medium 4–8 words nDCG@10 | §4.2.2 | 0.367 | **0.511** |
| Long 9+ words nDCG@10 | §4.2.2 | 0.406 | **0.476** |
| short-vs-long gap | §4.2.2 | 41% | **28%** (non-monotonic: Medium > Long) |
| length↔nDCG correlation r | §4.2.2 | +0.125 (p<0.001) | **≈ −0.01 (no linear trend)** |
| Failed (<0.3) | §4.2.1 | 39.0% | **33.9%** |
| Mediocre (0.3–0.7) | §4.2.1 | 55.9% | **33.2%** |
| Successful (≥0.7) | §4.2.1 | 5.1% | **32.9%** |
| Coverage @10 / @100 | §4.2.3 | 93.4% / 99.4% | **74.6% / 90.1%** |
| nDCG@10 = 0 queries | §3.3 "failed" | 192 | **736** |

Full reconciliation: `thesis_figures/data/computed/sec4_2_reconciliation.csv`.

**Implications for the narrative:**
- **Motivation survives:** short queries are still clearly the weakest bucket (0.345 vs 0.48–0.51) → still motivates query expansion. But state it as "short queries underperform," NOT "performance rises with length" — the linear trend (r=0.125) is gone (r≈0) and Medium now outscores Long.
- **Coverage story changes:** the dense retriever misses the relevant passage entirely for ~10% of queries even at depth 100 (not 0.6%), and ranks it outside the top-10 for another ~15%. This is a *stronger* argument for hybrid/CSQE (a real recall ceiling, not just a ranking problem).
- **"Only 5% successful" reverses to ~33% successful** — the baseline is meaningfully better than §4.2 currently claims; the "failure cliff" is softer (34% vs 39%).
- This is a **correctness fix**: §4.2 (baseline) and §4.10 (CSQE) must use the same scorer; §4.10 already uses the correct `pytrec_eval`, so only §4.2/§3.3 move.
- **Scope caveat:** only the *dense baseline* error analysis is affected (only exp_001 has this custom file; exp_002/BM25 has no such file). Headline metrics, all CSQE/hybrid results, and §4.10 are unaffected.

---

## 3. Thesis changes needed (by location)

| Section | File:line | Change | Depends on |
|---|---|---|---|
| §4.2.2 length table + "41%/59%" prose | `chapter4.tex:78-85` | Canonical numbers (0.345/0.511/0.476); "tokens"→"words"; 28% gap; short still weakest but non-monotonic | §2 (confirmed) |
| §4.2.2 correlation claim | `chapter4.tex:85` | r=0.125 "weak positive" → r≈0 (no linear length↔nDCG trend); reframe as "short queries specifically underperform" | §2 (confirmed) |
| §4.2.1 failure rate | `chapter4.tex:44`+ | 39%→34% failed; **5%→33% successful**; soften "failure cliff" | §2 (confirmed) |
| §4.2.3 coverage table+prose | `chapter4.tex:92-108` | 93.4/96.7/98.8/99.4 → **74.6/80.8/86.9/90.1**; reframe "finds-but-doesn't-rank" as recall ceiling (~10% missed even @100) → stronger hybrid motivation | §2 (confirmed) |
| §3.3 bucket defs | `chapter3.tex:131-135` | "1–3/4–8/9+ tokens"→"words"; keep boundaries | 1.2 |
| §3.3 thresholds | `chapter3.tex:109-113` | Keep absolute; add 1.4 signpost paragraph before line 109 | 1.4 |
| §4.10 failure paragraph | `chapter4.tex:829` | Rewrite: genuine retrieval failures (0 irretrievable), 199 missed-by-all + 58 BM25-retrievable-but-lost; drop "dataset ceiling" | 1.1 |
| §4.10 length table (fill Medium `---`) | `chapter4.tex:~867-880` | Scheme A (1–3/4–8/9+) CSQE-vs-blind; "general method, all lengths gain; short gains most proportionally (+43.6%)" | 1.3 (done) |
| §4.10 first-pass wording | §4.10 / 5.C.18 | "dominant predictor"→"largest modulator"; define first-pass = top-1 | 1.3 (done) |
| §3.9 regression sub-typing | `chapter3.tex:458-472` | Numbers unchanged; covered by 1.4 signpost | 1.4 |
| Supporting docs | `error_analysis_phase1_quantitative.md`, `exp_error_analysis_csqe.md` | Sync to word buckets + standard nDCG; the CSQE doc already has a Task-1.1 correction banner | 1.1/1.2 |

### §4.10 length table to drop in (Scheme A, CSQE+Hybrid vs Aya-blind, standard nDCG)
| Bucket | n | Aya-blind | CSQE+Hybrid | Δ abs | Δ rel |
|---|---|---|---|---|---|
| Short 1–3 | 147 | 0.369 | 0.530 | +0.161 | **+43.6%** |
| Medium 4–8 | 2495 | 0.506 | 0.703 | +0.197 | +38.8% |
| Long 9+ | 254 | 0.566 | 0.698 | +0.132 | +23.3% |

Framing: CSQE improves **all** query lengths substantially (general method); the shortest queries see the **largest proportional gain (+43.6%)**, consistent with §4.2 (they start weakest). Use "largest *proportional* gain" — the largest *absolute* Δ is Medium.

---

## 4. Cross-workstream touchpoints

- **WS4 Task 4.8** (first-pass definition): **answered** → BM25 top-1, qrel≥1.
- **WS4 Task 4.11** (258 inspection exhaustive or sampled): **answered** → exhaustive (all 258); refutes "irretrievable".
- **WS4 Task 4.12 / WS5.C.17** (big-win examples): the *count* (1061) is validated; the specific example *texts* (الرباط المنصوري, John Dewey, Nicolas Boileau) still need qualitative verification — not derivable from the CSV.
- **WS4 Task 4.14 / WS5.C.18** (0.3 "BM25 well-handled" threshold): covered by 1.4 (keep + signpost); soften "first-pass is dominant predictor" → "largest modulator."
- **§2 nDCG/coverage discrepancy — ALREADY RESOLVED, not a task for anyone.** This is *not* an open WS4 verification. It was fully investigated and proven in this WS1 session (the canonical run reproduces all four headline metrics); the corrected numbers are known and listed in §2. The only remaining action is Mohammed applying the §4.2/§3.3 edits — no further research or fact-check by Osman is needed.
- **WS5.B.2:** §3.3/§3.9 edits = Tasks 1.2 + 1.4 (this report).
- **WS5.C.15:** §4.10 redo = Tasks 1.1 + 1.3 (this report).
- **WS5.C.16** (demote meta-description failure mode): aligns with 1.1 — the "1 genuine failure = meta-description" framing is gone; it's 58 regressions.
- **WS5.C.20** (Medium length row "—"): now **fillable** (Scheme A Medium = CSQE 0.703 / blind 0.506).
- **WS2.1** ("Phase 4" purge): the bucket decision moved off the "<5 Phase-4 framework", so no naming conflict.
- **WS2.4** (Config A/B/C → descriptive): §4.10 text still says "Config A"; align to the descriptive name during the §4.10 rewrite.

---

## 5. Thesis-figures impact (WS7.1 / PROGRESS_SNAPSHOT.html)

- **Fig 4.12** (per-query Δ histogram) — **UNBLOCKED.** The only hard blocker is cleared: `csqe_vs_blind_per_query.csv` is now in `thesis_figures/data/raw/`. The "5-line Colab patch" note in the snapshot is obsolete (data exists + validated).
- **Decision D1** (length bins) — **settled → 1–3 / 4–8 / 9+** (NOT the 3-bin `<5/5–9/≥10` the snapshot assumed). Update `_helpers.py` `length_bin()` accordingly. Affects Fig 4.3 and Fig 4.14.
- **Decision D2** (threshold system) — **settled → keep absolute** (Failed<0.3 …); Fig 4.12 pairwise bands (±0.1 / +0.3) unchanged.
- **Fig 4.2** (failure cliff) — annotation **39% → 34%** (§2 confirmed). The cliff is also based on the buggy per-query nDCG, so the underlying distribution shifts; the figure must be regenerated from the canonical run, not just relabelled.
- **Fig 4.3 / 4.14** (by length) — use 1–3/4–8/9+; numbers from the new computed CSVs.
- **Fig 4.13** (first-pass) — top-1 definition; 0.8877 / 0.5814 validated.
- **Fig 4.15** (regression types 52/36/12%) — unaffected.
- **D3** (Config A/B/C → descriptive labels) and **D4** (numeric rounding) — unchanged, still mechanical.

---

## 6. Artifacts produced this session

- `thesis_figures/notebooks/task_1_1_corpus_integrity.py` + `data/computed/task_1_1_failure_corpus_check.csv`
- Self-contained Task 1.3 export cell added to `experiments/phase4_quick_wins_Ablation_erroranalysis (1).ipynb` (after Section 12b)
- `thesis_figures/data/raw/csqe_vs_blind_per_query.csv` (validated)
- `thesis_figures/data/computed/`: `baseline_dense_per_query_with_length.csv`, `length_bucket_summary_mdpr.csv`, `sec4_10_length_buckets_1-3-4-8-9.csv`, `sec4_2_mdpr_length_standard_ndcg.csv`, `sec4_2_reconciliation.csv`
- Correction banner on `exp_error_analysis_csqe.md`; decision recorded in `STREAM_1_KICKOFF.md`; progress logged in `THESIS_NEXT_STEPS_TASKS.md`

---

## 7. Status & next step

The §4.2 buggy-file finding (§2) is **confirmed by proof** (canonical run reproduces all 4 headline metrics), so it is no longer a decision — those numbers are simply wrong and the corrected values are authoritative. There is **no remaining data decision**; everything for 1.1–1.4 is computed and reconciled.

**Remaining work is purely thesis text**, all ready to apply:
- Mechanical / low-risk: §3.3 bucket relabel (tokens→words), §3.3 threshold signpost (1.4), §3.9 signpost.
- Numeric corrections (§2): §4.2.1 failure rate, §4.2.2 length table + correlation, §4.2.3 coverage — replace with the canonical-run values.
- Review-first drafts (you vet): §4.10 failure paragraph (1.1), §4.10 length table + framing (1.3), §4.10 first-pass wording.
- Sync: `error_analysis_phase1_quantitative.md` (shares the buggy numbers — needs a correction banner), Fig 4.2 regenerated from the canonical run.

**One editorial call for you** (not data): §4.2.3 coverage now shows a real recall ceiling (~10% missed even @100). Frame it as a *strength* of the hybrid/CSQE direction (recall problem, not just ranking), or keep it minimal? My rec: lean into it — it motivates hybrid retrieval.
