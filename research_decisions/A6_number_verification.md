# A6 — Number Verification Before Conclusion Edits

**Date:** 2026-07-29
**Scope:** Task A6 preparation. No `.tex` file was edited; this document is a report only.
**Primary evidence:** `thesis_figures/data/raw/csqe_vs_blind_per_query.csv` (2,896 rows), `thesis_figures/data/raw/baseline_bm25_run.txt`, `thesis_figures/data/raw/miracl_qrels_dev.json`, `thesis_figures/data/raw/exp21_summary.csv`, `thesis_figures/data/computed/sec4_2_reconciliation.csv`, `thesis_figures/data/computed/sec4_2_mdpr_length_standard_ndcg.csv`, `thesis_figures/data/computed/sec4_10_length_buckets_1-3-4-8-9.csv`, `arabic-rag-query-enhancement/docs/experiments/exp_error_analysis_csqe.md`, `arabic-rag-query-enhancement/docs/experiments/exp_013cd_ablations.md`.

---

## Task 1 — The "1,061" collision

### Verdict: **GENUINE COINCIDENCE.** Both counts are independently correct; neither line is a transcription error.

Both sets were recomputed from the raw per-query artefacts rather than being read back out of the prose.

| Set | Definition | Recomputed count | Source of computation |
|---|---|---|---|
| First-pass relevant (`chapter4.tex:832`) | BM25 baseline top-1 document has qrel $\geq$ 1 | **1,061** (36.63 % of 2,896) | `thesis_figures/data/raw/baseline_bm25_run.txt` joined against `thesis_figures/data/raw/miracl_qrels_dev.json` |
| Big wins (`chapter4.tex:876`) | $\Delta$ = NDCG@10(CSQE+Hybrid) $-$ NDCG@10(Aya-blind BM25) $> 0.3$ | **1,061** | column `delta_ndcg10_csqe_vs_blind` of `thesis_figures/data/raw/csqe_vs_blind_per_query.csv` |

Supporting evidence that the two are distinct sets:

- The **overlap is only 389 queries**, not 1,061. Were one line a transcription of the other, the sets would be identical.
- The first-pass split is internally closed: 1,061 + 1,835 = 2,896 (`chapter4.tex:832-835`), and conditioning on that split reproduces the published means **exactly** — 0.8877 / 0.6684 for the relevant group and 0.5814 / 0.4100 for the remainder (`chapter4.tex:832-833`).
- The big-win count was independently reproduced during Workstream 1 and is recorded as validated in `research_decisions/STREAM_1_COMPLETION_REPORT.md:31` ("Big wins (Δ>0.3) | 1061 | 1061 ✓") and `research_decisions/THESIS_NEXT_STEPS_TASKS.md:381`.
- The same coincidence is already present, independently, in the source experiment document: `arabic-rag-query-enhancement/docs/experiments/exp_error_analysis_csqe.md:37` (big wins 1,061) and `:49` (first-pass relevant 1,061).

Neither number requires changing. **A6 may quote either.** Should the coincidence be judged distracting to a reader, the safest mitigation is wording rather than arithmetic — the first-pass figure can be cited as "36.6 % of queries" in Chapter 5 (as `chapter5.tex:28` already does) so the numeral 1,061 is used only once in the conclusion.

### Separate defect found on the same line — `chapter4.tex:876` (NOT a Chapter 5 issue, but it must not be quoted by A6)

The sentence "All 1,061 big-win queries ($\Delta > 0.3$) shared a single pattern: CSQE nDCG@10 = 1.000, Blind = 0.000" is **false**. Recomputed from `csqe_vs_blind_per_query.csv` over the 1,061 big-win rows:

| Condition | Count | Share of big wins |
|---|---|---|
| CSQE = 1.000 **and** blind = 0.000 | **143** | 13.5 % |
| CSQE $\geq$ 0.90 and blind $\leq$ 0.10 | 152 | 14.3 % |
| CSQE = 1.000 (any blind score) | 485 | 45.7 % |
| Blind = 0.000 (any CSQE score) | 463 | 43.6 % |
| Mean over big wins | CSQE 0.8029, blind 0.2477 | — |

The claim appears to have been generalised from the WS4 Task 4.12 candidate filter, which was explicitly a *subset* selector — `(blind_bm25 <= 0.10) & (csqe_bm25 >= 0.90) & definitional` — see `research_decisions/WS4_TASK_4.12_BIGWIN_EXAMPLES.md:180`. That filter was used to *find illustrative examples*, never to characterise the whole population. The inherited claim is also present in the source doc at `arabic-rag-query-enhancement/docs/experiments/exp_error_analysis_csqe.md:84` and in `thesis_update_brief.md:451`.

The caption of Table `tab:bigwin_examples` (`chapter4.tex:880`) is unaffected — it asserts the 1.000/0.000 pattern only for the three tabulated examples, which is correct.

**Suggested repair for `chapter4.tex:876`** (outside A6's edit scope; raised for the caller to schedule):

```latex
Among the 1,061 big-win queries ($\Delta > 0.3$), a recurring pattern was observed: in 463 the blind baseline scored 0.000 while CSQE recovered the query, and in 143 of these the recovery was complete (CSQE nDCG@10 = 1.000). In each such case, blind QE hallucinated a plausible but factually incorrect entity, while CSQE's first-pass corpus document anchored the expansion to the correct Wikipedia article. Table~\ref{tab:bigwin_examples} presents three representative examples.
```

**Consequence for A6:** the phrase "all 1,061 big-win queries" must not be carried into the conclusion. None of the three drafted paragraphs (P1--P3) relies on it, so no rewrite of the drafts is needed on this account.

---

## Task 2 — Canonical baseline error-analysis numbers

Canon is taken from `thesis_figures/data/computed/sec4_2_reconciliation.csv` (the WS1 corrected-run reconciliation) and the underlying `thesis_figures/data/computed/sec4_2_mdpr_length_standard_ndcg.csv`.

### `chapter5.tex:14` — the conclusion sentence under audit

| Claim (chapter5.tex:14) | Canon | Source | Verdict |
|---|---|---|---|
| mDPR NDCG@10 = 0.4993 | 0.4993462 | `thesis_figures/data/raw/exp12_summary.csv` | ✅ Match |
| BM25S Recall@100 = 0.8577 | 0.8577332 | `thesis_figures/data/raw/exp12_summary.csv` | ✅ Match |
| 34 % of queries failed (NDCG@10 < 0.3) | 33.9 % (982 / 2,896) | `sec4_2_reconciliation.csv`, row "Failed (<0.3)" | ✅ Match (correct rounding) |
| Shortest queries NDCG@10 = 0.345 | 0.3448 (Short 1--3, n = 147) | `sec4_2_mdpr_length_standard_ndcg.csv` | ✅ Match |
| Long queries NDCG@10 = 0.476 | 0.4764 (Long 9+, n = 254) | `sec4_2_mdpr_length_standard_ndcg.csv` | ✅ Match |
| "only 72 % of long-query performance" | 28 % gap = 72 % of long | `sec4_2_reconciliation.csv`, row "short-vs-long gap" | ✅ Match |
| Correlation $r \approx -0.01$ | $-0.01$ (no relationship) | `sec4_2_reconciliation.csv`, row "length~nDCG correlation r" | ✅ Match |
| "performance did not increase monotonically with length" | Medium 0.5108 > Long 0.4764 | `sec4_2_mdpr_length_standard_ndcg.csv` | ✅ Match |

**`chapter5.tex:14` is fully canonical. No edit is required.**

### `chapter4.tex` §4.2 (lines 47--146) — the source section

| Claim | Location | Canon | Verdict |
|---|---|---|---|
| Failed 982 / 33.9 % / avg 0.053 | `chapter4.tex:66` | 33.9 % (982) | ✅ Match |
| Mediocre 962 / 33.2 % / avg 0.511 | `chapter4.tex:67` | 33.2 % (962) | ✅ Match |
| Successful 952 / 32.9 % / avg 0.948 | `chapter4.tex:68` | 32.9 % (952) | ✅ Match |
| "34 % of queries (982 out of 2,896)" | `chapter4.tex:73` | 33.9 % (982) | ✅ Match |
| "736 retrieved no relevant passage at all" | `chapter4.tex:73` | 736 (`nDCG@10 == 0` queries) | ✅ Match |
| Short (1--3 words) 0.345, n = 147, 5.1 % | `chapter4.tex:95` | 0.3448 / 147 / 5.1 % | ✅ Match |
| Medium (4--8 words) 0.511, n = 2,495, 86.2 % | `chapter4.tex:96` | 0.5108 / 2,495 / 86.2 % | ✅ Match |
| Long (9+ words) 0.476, n = 254, 8.8 % | `chapter4.tex:97` | 0.4764 / 254 / 8.8 % | ✅ Match |
| "72 % ... a 28 % gap"; $r \approx -0.01$ | `chapter4.tex:102` | 28 % gap; $r = -0.01$ | ✅ Match |
| Coverage 74.6 / 80.8 / 86.9 / 90.1 % | `chapter4.tex:124-127` | 74.6 / 80.8 / 86.9 / 90.1 % | ✅ Match |
| "roughly 10 % ... (coverage 90.1 %)" and "$\sim$15 % ranked outside top-10" | `chapter4.tex:132` | 100 $-$ 90.1 = 9.9 %; 90.1 $-$ 74.6 = 15.5 % | ✅ Match |

**§4.2 is fully canonical throughout. No buggy-file residue was found in either chapter.** All fourteen quantities that the reconciliation table flagged as changed (0.240 → 0.345, 0.367 → 0.511, 0.406 → 0.476, 41 % → 28 %, +0.125 → $-$0.01, 39.0 % → 33.9 %, 55.9 % → 33.2 %, 5.1 % → 32.9 %, 93.4 % → 74.6 %, 96.7 % → 80.8 %, 98.8 % → 86.9 %, 99.4 % → 90.1 %, 192 → 736) are present in their **corrected** form.

### One unrelated rounding discrepancy noted in passing (not §4.2, not blocking)

Hybrid RRF $k=20$ Recall@100 is printed as **0.9467** at `chapter4.tex:546`, `:547`, `:561`, `:599` and `:669`. The canonical raw value is **0.94661684** (`thesis_figures/data/raw/exp12_summary.csv`, row "Hybrid RRF (k=20)"), which rounds to **0.9466** — the value recorded in `CLAUDE.md:117`. This is a one-in-the-fourth-decimal rounding slip affecting five call sites in Chapter 4 only; it does not appear in Chapter 5 and does not affect any A6 paragraph. It is raised for completeness.

---

## Task 3 — Verification of the three drafted conclusion paragraphs

### P1 — appended to the Query2Doc paragraph (`chapter5.tex:16`)

#### Per-figure verification

| Figure in draft | Source | Verdict |
|---|---|---|
| "batched generation" | `chapter3.tex:229` — "Multiple queries were tokenised with left-padding and processed simultaneously" | ✅ Correct |
| "a 128-token generation limit" | `chapter3.tex:230`; also `chapter3.tex:212`, `:221` | ✅ Correct |
| "4-bit quantisation where memory required it" | `chapter3.tex:345`, `:353` (NF4 via bitsandbytes; Jais-2-8B on T4, Aya Expanse 8B) | ⚠️ **Correct as fact, misplaced as cause.** Quantisation is a *memory* measure listed in §3.5.5, and it is explicitly **not** one of the three throughput optimisations that produce the forty-minute figure (`chapter3.tex:226-232`). 4-bit inference is slower, not faster. It must be stated as a separate enabling measure, not as a contributor to the runtime. |
| "a two-notebook workflow separating query generation from retrieval evaluation" | `chapter3.tex:58` | ⚠️ **Correct as fact, misattributed as a speed-up.** §3.1.3 credits it with *reuse of enhanced queries across retrieval configurations*, not with the forty minutes. It is nevertheless already framed this way at `chapter5.tex:42`, so retaining it is defensible provided the causal claim is loosened. |
| "reduced a **full-corpus experiment** to approximately forty minutes" | `chapter3.tex:234` — "reduced **full-set generation time** to approximately 40 minutes **per model on a T4 GPU**" | ❌ **FAILS VERIFICATION on two counts.** (a) "Full-corpus" is wrong: the forty minutes covers generation over the **2,896-query development set**, not the 2,061,414-document corpus. (b) It is the *generation stage*, not the whole experiment: `arabic-rag-query-enhancement/docs/experiments/exp_003_query2doc_dense.md:241-245` gives ~3 min model load + ~40 min generation + ~5 min retrieval = **~48 min total**; `exp_004_query2doc_bm25.md:224-227` gives ~45 min total. Corroborated at `arabic-rag-query-enhancement/docs/experiments/README.md:87,110`. |
| (baseline for the comparison, not in the draft) | `chapter3.tex:226` — naïve sequential processing ~10 s/query $\approx$ 8 hours for the full dev set | Available and worth including; it is what makes "forty minutes" meaningful. |

#### Final paste-ready LaTeX (P1)

```latex
Practical execution on freely available cloud GPUs was achieved through a set of engineering optimisations---batched generation with left-padding, a 128-token generation limit, and half-precision inference with gradient computation disabled---which reduced pseudo-document generation over the full 2,896-query development set from an estimated eight hours of naïve sequential processing to approximately forty minutes per model on a T4 GPU (Section~\ref{sec:meth_q2d_batch}). Models whose native-precision footprint exceeded the available VRAM were additionally quantised to 4-bit NF4 (Section~\ref{sec:meth_quantisation}), and a two-notebook workflow separating query generation from retrieval evaluation allowed each set of enhanced queries to be reused across both retrieval paradigms without regeneration (Section~\ref{sec:meth_pipeline}).
```

Label check: `sec:meth_q2d_batch` is defined at `chapter3.tex:224`, `sec:meth_quantisation` at `chapter3.tex:343`, `sec:meth_pipeline` at `chapter3.tex:47`. All three resolve.

Consistency note: `chapter5.tex:42` (Challenges, item 1) states "approximately 40 minutes per full experiment". Strictly this should read "per full generation run"; the totals in the experiment documents are 45--48 minutes. Should P1 be adopted with the corrected wording, `chapter5.tex:42` ought to be aligned in the same pass so the two statements do not disagree.

---

### P2 — new paragraph after the CSQE paragraph (`chapter5.tex:28`)

#### Per-figure verification

| Figure in draft | Source | Verdict |
|---|---|---|
| Corpus-only BM25 = 0.5381 | `chapter4.tex:620`; `arabic-rag-query-enhancement/docs/experiments/exp_013cd_ablations.md` (013c row); `CLAUDE.md:143` | ✅ Correct |
| Blind-only BM25 = 0.5752 | `chapter4.tex:621`; `CLAUDE.md:144` | ✅ Correct |
| Combined 2+2 BM25 = 0.6157 | `chapter4.tex:622`, `:594`; `thesis_figures/data/raw/exp21_summary.csv` row "BM25+CSQE (Exp 013)" | ✅ Correct |
| "+0.0405 over the stronger component" | 0.6157 $-$ 0.5752 = 0.0405; stated verbatim at `chapter4.tex:627` | ✅ Correct |
| Fused corpus-only = 0.6616 | `chapter4.tex:695`; `exp_013cd_ablations.md:53` | ✅ Correct |
| Fused blind-only = 0.7082 | `chapter4.tex:696`; `exp_013cd_ablations.md:54` | ✅ Correct |
| Fused combined = 0.7137 | `chapter4.tex:697`, `:678`, `:772`; `exp21_summary.csv` row "A: BM25+CSQE + Dense RRF (k=20)" | ✅ Correct |
| "corpus samples anchor to attested vocabulary while blind samples widen coverage" | `chapter4.tex:627` — "corpus samples contribute by anchoring the expansion to attested Wikipedia vocabulary, reducing entity misidentification; blind samples diversify answer-space coverage beyond the first-pass retrieval window" | ✅ Correct, and near-verbatim from Chapter 4 |
| (omitted from the draft, but material) | In fused form the combined margin over blind-only collapses to **+0.0055** (0.7137 $-$ 0.7082), explicitly discussed at `exp_013cd_ablations.md:85` | ⚠️ The draft quotes the fused triple without noting that complementarity is far weaker after fusion. Presenting 0.6616 / 0.7082 / 0.7137 as evidence of complementarity, immediately after a BM25-only margin of +0.0405, invites the reader to assume the same gap survives fusion. It does not; the gap is 7.4 times smaller. Stating the +0.0055 explicitly forestalls the objection. |

#### Final paste-ready LaTeX (P2)

```latex
\textbf{Corpus-grounded and blind expansion are complementary.} A component ablation isolated the two halves of the CSQE expansion. On BM25 alone, corpus-only expansion achieved 0.5381 NDCG@10 and blind-only expansion 0.5752, while the combined two-corpus-plus-two-blind configuration achieved 0.6157---an improvement of +0.0405 over the stronger single component, confirming that the two sources are not substitutes for one another (Section~\ref{sec:res_csqe_ablation}). The same ordering was preserved once the expanded BM25 run was fused with the original-query dense run (0.6616, 0.7082 and 0.7137 respectively), although the margin over blind-only narrowed to +0.0055, because the dense retriever supplies a semantic signal that does not depend on expansion quality and therefore absorbs much of the corpus component's marginal contribution (Section~\ref{sec:res_csqe_configs}). The mechanism is interpreted as follows: the corpus samples anchor the expansion to vocabulary attested in the target corpus, reducing entity misidentification, while the blind samples widen answer-space coverage beyond the first-pass retrieval window.
```

Label check: `sec:res_csqe_ablation` is defined at `chapter4.tex:607`, `sec:res_csqe_configs` at `chapter4.tex:657`. Both resolve.

---

### P3 — new paragraph after the retriever-specific paragraph (`chapter5.tex:30`)

#### Per-figure verification

| Figure in draft | Source | Verdict |
|---|---|---|
| Improved 56.8 % | `chapter4.tex:799`, `:808`; recomputed from `csqe_vs_blind_per_query.csv`: 1,646 / 2,896 = 56.83 % | ✅ Correct |
| Regressed 16.6 % | `chapter4.tex:801`; recomputed: 480 / 2,896 = 16.57 % | ✅ Correct |
| Mean +0.1890 NDCG@10 | `chapter4.tex:803`; recomputed mean $\Delta$ = 0.188984 | ✅ Correct |
| 1--3 words: +43.6 % proportional | `chapter4.tex:850`, `:857`; `sec4_10_length_buckets_1-3-4-8-9.csv`: 0.1609 / 0.3692 = 43.58 % | ✅ Correct |
| 4--8 words: +0.197 absolute | `chapter4.tex:851`, `:857`; computed file gives $\Delta$ = 0.1965 | ✅ Correct |
| 9+ words: +0.132 ($+23.3$ %) | `chapter4.tex:852`, `:857`; computed file gives $\Delta$ = 0.1317, 0.1317 / 0.5665 = 23.25 % | ✅ Correct |
| First-pass-relevant share 36.6 % | `chapter4.tex:857`; recomputed 1,061 / 2,896 = 36.63 % | ✅ Correct |
| 0.8877 vs 0.5814 | `chapter4.tex:832-833`; recomputed exactly by conditioning on BM25 top-1 qrel $\geq$ 1 | ✅ Correct |
| (implicit) the baseline being compared against | Aya blind BM25 $n=1$, 0.5046 (`chapter4.tex:793`, `:835`) | Correct, but unnamed in the draft — the deltas are meaningless without it |
| (implicit) "the final system" mean | The per-query mean of the analysed system is **0.6936**, not the corpus-level 0.7137 (`chapter4.tex:793` explains the distinction) | ⚠️ The draft never states a system mean, so no contradiction arises; the caveat is recorded so that no absolute figure is added later without the accompanying explanation |

**All nine figures in P3 verify.** The only defects are omissions of context (the identity of the comparison baseline) rather than incorrect arithmetic.

#### Final paste-ready LaTeX (P3)

```latex
\textbf{Per-query analysis localises where the gains arise.} Measured against the blind-QE baseline (Aya Expanse~8B, BM25, $n=1$; 0.5046 NDCG@10), the final system improved 56.8\% of the 2,896 development queries and regressed on 16.6\%, for a mean per-query gain of +0.1890 NDCG@10 (Section~\ref{sec:res_win_loss}). These gains were not distributed evenly. The shortest queries (1--3 words) gained the most in proportional terms (+43.6\%), medium-length queries (4--8 words) the most in absolute terms (+0.197), and the longest queries (9+ words) the least (+0.132, or +23.3\%)---confirming that the expansion compensates chiefly for the information poverty of underspecified queries, exactly the weakness identified in the baseline error analysis. First-pass retrieval quality was found to be the largest single modulator of that benefit: for the 36.6\% of queries whose BM25 first pass returned a relevant document at rank~1, the system achieved 0.8877 NDCG@10, against 0.5814 for the remainder (Section~\ref{sec:res_firstpass}).
```

Label check: `sec:res_win_loss` is defined at `chapter4.tex:787`, `sec:res_firstpass` at `chapter4.tex:820`. Both resolve.

---

## Summary of required actions

| # | Item | Location | Action |
|---|---|---|---|
| 1 | "1,061" collision | `chapter4.tex:832` and `:876` | **None.** Coincidence confirmed; both counts are correct. |
| 2 | "All 1,061 big-win queries shared a single pattern" | `chapter4.tex:876` | **Correction required** (only 143 of 1,061 match). Replacement sentence supplied above. Outside A6's scope; must not be quoted in the conclusion. |
| 3 | Baseline error-analysis figures | `chapter5.tex:14` and `chapter4.tex:47-146` | **None.** Fully canonical. |
| 4 | "full-corpus experiment ... forty minutes" | P1 draft | **Corrected** to "generation over the full 2,896-query development set ... forty minutes per model on a T4 GPU". |
| 5 | 4-bit quantisation and the two-notebook workflow presented as runtime optimisations | P1 draft | **Corrected**: reordered into separate clauses reflecting their actual roles per §3.1.3 and §3.5.5. |
| 6 | "40 minutes per full experiment" | `chapter5.tex:42` | Recommended alignment to "per full generation run" (totals are 45--48 min) in the same editing pass. |
| 7 | Fused-ablation margin left implicit | P2 draft | **Corrected**: the +0.0055 fused margin and its cause are now stated. |
| 8 | P3 figures | P3 draft | **All verified.** Baseline identity added for readability; no numeric change. |
| 9 | Recall@100 printed as 0.9467 | `chapter4.tex:546`, `:547`, `:561`, `:599`, `:669` | Rounding slip; canon is 0.9466. Chapter 4 only, not blocking A6. |
