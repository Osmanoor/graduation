# Track A — Prompt for the chapter-editing chat

Paste this whole document as the first user message in the chat that owns
the thesis LaTeX edits (the chat that has been working on `Chapters/*.tex`).
It is self-contained and includes every file path, line target, and replacement
value the next session needs to act independently — no other context required.

---

## Mission

Apply the Track A thesis text edits that follow from Workstream 1's completion.
Data is settled, figures are rendered, decisions are made. The remaining work
is **pure LaTeX prose editing across `chapter3.tex`, `chapter4.tex`, and two
supporting MD docs**. Estimated effort: ~3 hours focused writing.

## Read these first (in order)

1. `research_decisions/STREAM_1_COMPLETION_REPORT.md` — §3 has the exact
   `file:line` targets and the new canonical numbers. **This is the
   source of truth.** If anything below disagrees, that doc wins.
2. `research_decisions/STREAM_1_KICKOFF.md` — has the ready-to-paste LaTeX
   signpost paragraph for Task 1.4 (Section 1.4 of the doc).
3. `thesis_figures/EMBEDDING_PLAN.md` — per-figure copy-paste LaTeX blocks +
   cross-reference suggestions. Use it whenever §4.2 / §4.10 references a
   figure.

## Edits to apply

### A. §4.2 numeric correctness fix (highest priority — current numbers are wrong)

The §4.2 baseline error analysis was sourced from a buggy nDCG-computation
file. The corrected values (recomputed from the canonical TREC run with
`pytrec_eval`, reproducing all four headline metrics exactly) are:

| Location | What | OLD (buggy) | **NEW (canonical)** |
|---|---|---|---|
| §4.2.1 (`chapter4.tex:44`) | Failure rate (nDCG@10 < 0.3) | 39.0% | **33.9%** |
| §4.2.1 | Mediocre (0.3–0.7) | 55.9% | **33.2%** |
| §4.2.1 | Successful (≥0.7) | 5.1% | **32.9%** |
| §4.2.2 (`chapter4.tex:78-85`) | Short 1–3 words nDCG@10 | 0.240 | **0.345** |
| §4.2.2 | Medium 4–8 words nDCG@10 | 0.367 | **0.511** |
| §4.2.2 | Long 9+ words nDCG@10 | 0.406 | **0.476** |
| §4.2.2 | "tokens" everywhere | tokens | **words** |
| §4.2.2 | Short-vs-long gap | 41% | **28%** (non-monotonic) |
| §4.2.2 | Length↔nDCG correlation | r = 0.125 (p<0.001) | **r ≈ -0.01 (no linear trend)** |
| §4.2.3 (`chapter4.tex:92-108`) | Coverage @10 | 93.4% | **74.6%** |
| §4.2.3 | Coverage @100 | 99.4% | **90.1%** |
| §3.3 | Queries with nDCG@10 = 0 | 192 | **736** |

**Narrative changes that flow from the numbers:**

- §4.2.2: drop the "performance rises with length" framing. The new story is
  "**short queries underperform** (0.345 mean); medium and long are similar
  (0.511 and 0.476)." No linear trend — Medium actually outscores Long.
- §4.2.3: reframe coverage. The OLD story was "finds-but-doesn't-rank";
  the NEW story is **"~10% recall ceiling even at depth 100"** — a real
  miss, not just a ranking gap. **This is a *stronger* motivation for hybrid
  + CSQE** because it speaks to recall, not just precision.
- §4.2.1: soften "failure cliff" language slightly — 34% is still a real
  cliff, but lower than the original 39%, and the successful tier roughly
  triples from 5% to 33%.

**Editorial call already settled:** lean into the §4.2.3 recall-ceiling
framing as motivation for the hybrid + CSQE direction. Don't keep it
minimal — the recall ceiling is the cleanest argument for the contribution.

### B. §3.3 token → word relabel + threshold signpost paragraph

1. **In `chapter3.tex:131-135`** — change the bucket scheme from
   "1–3 / 4–8 / 9+ tokens" to "**1–3 / 4–8 / 9+ words**". Apply to all prose
   that references the buckets. Boundaries unchanged.

2. **Insert at `chapter3.tex:109`** (before the Failed/Mediocre/Successful
   list, as a `\subsubsection*{}` or similar break) — the threshold signpost.
   Verbatim block from `STREAM_1_KICKOFF.md` Task 1.4:

   ```latex
   \subsubsection*{Note on threshold systems used in this thesis}
   Three threshold systems are used throughout this thesis to answer different
   questions. The \emph{absolute} system (this section) classifies each query's
   retrieval quality independently and is used to characterise dataset difficulty
   and to report overall failure rates. The \emph{pairwise} system (Section~3.9)
   compares the per-query nDCG@10 of two systems and is used in error-analysis
   tables that contrast CSQE with the blind baseline. A third \emph{hybrid}
   classification (Section~3.9, regression sub-typing) uses absolute BM25 score
   thresholds to label pairwise regressions by their root cause. The three
   systems are orthogonal: a single query can be classified as ``Mediocre'' on
   the absolute system, ``Big Win'' on the pairwise system, and ``Type~A
   regression'' on the hybrid system without contradiction, because each
   measures a distinct aspect of retrieval behaviour.
   ```

3. **§3.9 lines 458–472** — no numeric change. The signpost paragraph
   inserted above covers the relationship between §3.9 and §3.3.

### C. §4.10 rewrite (failure paragraph + Medium row fill + first-pass wording)

1. **Failure paragraph at `chapter4.tex:829`** — replace the
   "irretrievable / dataset ceiling" framing with the WS1-verified facts:

   - 258 queries with CSQE+Hybrid nDCG@10 < 0.1 are **genuine retrieval
     failures**, not dataset artefacts (0 of 258 are irretrievable).
   - Of these, **199 also miss on the BM25 baseline** (passages present in
     the corpus but not surfaced by any method tested).
   - The remaining **58 are retrievable by BM25 alone (43 with BM25 ≥ 0.3)
     but lost by the CSQE hybrid** — these are real regressions caused by
     expansion, not ceiling effects.

2. **Length-bucket table — fill the Medium row** (currently `---` at
   `chapter4.tex:~867-880`) using the Scheme A numbers:

   | Bucket | n | Aya-blind | CSQE+Hybrid | Δ abs | Δ rel |
   |---|---|---|---|---|---|
   | Short 1–3 | 147 | 0.369 | 0.530 | +0.161 | +43.6% |
   | Medium 4–8 | 2495 | 0.506 | 0.703 | +0.197 | +38.8% |
   | Long 9+ | 254 | 0.566 | 0.698 | +0.132 | +23.3% |

   Framing: **"CSQE improves all query lengths substantially (general method);
   the shortest queries see the largest *proportional* gain (+43.6%),
   consistent with §4.2.2 (they start weakest). Medium queries see the
   largest *absolute* gain (+0.197)."**

3. **First-pass wording (§4.10)** — soften "dominant predictor" to
   **"largest modulator"**. Define "first-pass relevant" precisely as
   **"BM25 retrieves a relevant document (qrel ≥ 1) at rank 1"** — i.e.
   top-1, not top-5. The numbers 0.8877 (relevant first pass, n=1,061) vs
   0.5814 (not relevant, n=1,835) are correct and unchanged.

### D. Sync supporting MD docs

1. **`research_decisions/error_analysis_phase1_quantitative.md`** — add a
   correction banner at the top noting the §2 reconciliation. Update the
   Performance-by-Length-Bucket table (lines 29–35) and the Length-Distribution
   table (lines 99–105) to the corrected canonical numbers + word-based buckets.

2. **`arabic-rag-query-enhancement/docs/experiments/exp_error_analysis_csqe.md`**
   — already has a correction banner from WS1. Verify it's still accurate
   after the rewrites in C.

### E. Figure + table embedding (optional in this session)

Once the prose edits are in place, embed the figures and tables in their
target sections. Use `thesis_figures/EMBEDDING_PLAN.md` — every figure has
a ready-to-paste LaTeX block, target section, and example cross-reference
sentence. Compile `thesis_figures/preview_all_figures.tex` separately to
preview every figure + caption at thesis text width before embedding.

`graphicspath` is already configured in `1-main.tex` so filenames resolve
without a path prefix. Embedding does not require any change to those paths.

## Decisions already settled (don't re-debate)

- **Length bins: 1–3 / 4–8 / 9+ words** (preserves §4.2 short-query motivation).
  No 3-vs-2-bucket discussion remains.
- **Keep absolute Failed/Mediocre/Successful thresholds** (do not switch to
  distributional). The 33.9% failure number is a clean motivator.
- **§4.2.3 recall-ceiling framing — lean in**, do not minimise.
- **§4.10 narrative: "genuine retrieval failures"** not "dataset ceiling".
- **First-pass definition: BM25 top-1, qrel ≥ 1**.
- **Config A/B/C → BM25-only-expanded / Dense-only-expanded / Both-expanded**
  already applied thesis-wide in earlier batches; figure labels in
  `thesis_figures/` are now consistent. No further rename needed.
- **Numeric rounding: 3 decimals** in tables (mDPR 0.499; R@100 0.947). All
  generated tables already follow this.

## What is NOT in scope for Track A

- WS6.4 citation fixes (10 fabricated BibTeX entries) — separate task; needs
  Mohammed-Osman alignment on Osman's WS6 report first.
- WS3.1–3.3 AI-pattern audits — can be folded in opportunistically while
  reading each chapter, but not required for this Track A pass.
- Ch 1 (introduction) / Ch 5 (conclusion) / abstract — blocked on
  supervisor Q2/Q3.
- New figures (e.g. Fig 2.1 QE-layer companion) — Osman's punch-list, separate.

## Verification checklist before declaring Track A done

- [ ] All numeric values in §4.2.1, §4.2.2, §4.2.3 match the table in section
      A above (no stale 39% / 0.240 / 99.4% anywhere).
- [ ] "tokens" replaced with "words" in §3.3 and §4.2 bucket prose.
- [ ] §3.3 signpost paragraph inserted at line 109.
- [ ] §4.10 failure paragraph no longer says "irretrievable" or "dataset
      ceiling" anywhere.
- [ ] §4.10 length-bucket table has Medium row populated; framing emphasises
      proportional gain on Short and absolute gain on Medium.
- [ ] §4.10 first-pass definition explicit ("BM25 top-1, qrel ≥ 1") and
      "dominant predictor" softened to "largest modulator".
- [ ] `error_analysis_phase1_quantitative.md` updated with banner + canonical
      numbers.
- [ ] (If figures embedded:) compiles cleanly via `xelatex 1-main.tex`; every
      figure has a `\caption` + `\label` + at least one `\ref` in body text.

## Reporting back

When done, drop a brief completion note in
`research_decisions/STREAM_1_COMPLETION_REPORT.md` under a new "Track A
applied" section, listing which checklist items are done and any deviations
from the spec above.
