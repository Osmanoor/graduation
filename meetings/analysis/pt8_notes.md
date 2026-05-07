# pt8 Analysis Notes — Part 8

**Source:** `meetings/pt8.md`
**Speakers:** Mohammed, Osman
**Coverage:** **P4.4.1 → P4.4.11** (BM25 repetition results, hybrid fusion results, Dense degradation in CSQE).
**Notable:** Several "we don't actually understand the mechanism" admissions (CC tie-breaking, Dense degradation specifics). Verification of the asymmetric Q2D gap from pt6 — confirmed they have *not* done blind Q2D in asymmetric hybrid configurations.

---

## Per-Item Discussion & Decisions

### Item P4.4.1 — Combined 8-column repetition table (n + β side-by-side)

**Discussion:**
- Both find the combined table understandable.
- Adaptive (β) clearly visible as better than fixed (n) at a glance — this is exactly the comparison they want readers to see immediately.

**Decision:** **APPROVE** — keep the combined table. The dense layout is intentional and works.

---

### Item P4.4.2 — Claim "query repetition recovers all 9 previously degraded BM25 models"

**Discussion (factual correction):**
- Mohammed corrected: at n=1, only **3/9 models were above the BM25 baseline; 6/9 were below**. The "all 9 degraded" framing is overstated. Correct framing: "the 6 originally degraded models all recovered above baseline with appropriate repetition; the 3 already above baseline improved further."
- Both want to add a **graph** to make the recovery visible — line per model, x-axis = n (and β), y-axis = nDCG@10, with the BM25-no-QE baseline drawn as a horizontal line. The recovery is dramatic visually: at n=1 most lines are below the baseline; at n=5–7 all lines are above.
- They confirmed this kind of graph already exists in their Colab notebook and slides — easy to extract.

**Decision:** **REVISE** — multi-part:
1. Correct the "all 9 degraded" claim to "6 of 9 were below baseline at n=1; all 9 reached or exceeded baseline at the appropriate repetition setting."
2. Add a recovery graph (line plot with baseline horizontal line). Tag this for the figure-plan workstream (item 4.15).

---

### Item P4.4.3 — Interpretation: "8B models converge at MuGI β=2; 3-4B models plateau at fixed n=5-7; SILMA peaks at n=5 because pseudo-documents are shorter"

**Discussion (REJECT — over-interpretation):**
- They opened the actual numbers and observed: the differences between (n=5, n=7, β=2) for any given model are **tiny — under 0.001 (6 in 10,000) in some cases**. This is not enough to support a model-size-based interpretation.
- All pseudo-documents had max_tokens=128, so the "smaller models produce shorter docs" claim is also unsupported — they all generated up to the same cap.

**Decision:** **REJECT** — drop the size-based interpretation entirely. The data isn't strong enough to support claims about model-size patterns in optimal repetition. Keep just the empirical observation that different models settle on different optimal configurations, without inventing a causal story.

---

### Item P4.4.4 — Claim "excessive repetition over-weights query tokens, suppresses expansion vocabulary"

**Discussion:**
- Mohammed confirmed the diminishing-returns trend: most models go up from n=1→3→5→7 but then **decrease at n=10** (the inverse term-dilution).
- The decrease is small but consistent across models — suggesting if they tested n=20, the decline would be more pronounced.
- Interpretation is plausible (inverse of term dilution) but unproven.

**Decision:** **APPROVE WITH FRAMING** — keep the explanation but explicitly tag it as discussion, not proven mechanism. Possibly mention that going to higher n (e.g., 20) would likely show the decline more clearly — useful future direction.

---

### Item P4.4.5 — Framing "query repetition — not a change of model — was the missing ingredient"

**Discussion:**
- Both like the substance of the finding (the fix was not about model selection but about applying repetition).
- They dislike the phrase "missing ingredient" — too informal/marketing-style for a thesis.

**Decision:** **REVISE** — keep the finding, change the phrasing to something more scientific. Suggested rewording: "demonstrating that for the originally underperforming systems, the deficiency was not in the model itself but in the absence of query repetition." Drop "missing ingredient."

---

### Item P4.4.6 — "+26.7% improvement for Aya β=2 (0.5855 vs 0.4621 baseline)"

**Discussion:**
- Mohammed joked: "if this number is wrong, we'll be paying for it forever."
- Verification: (0.5855 − 0.4621) / 0.4621 = 26.7% — confirmed correct.

**Decision:** **APPROVE.**

---

### Item P4.4.7 — RRF k=20 and CC α=0.5 "statistically indistinguishable"

**Discussion:**
- Both immediately agreed: they did **not run any statistical test** (no t-test, no permutation test). The wording "statistically indistinguishable" is technically false because no test was conducted.
- The values are 0.6267 vs 0.6266 — they differ at the 4th decimal place, practically identical.

**Decision:** **REVISE** — change "statistically indistinguishable" to "**numerically indistinguishable**" (or "essentially equivalent"). Avoid "statistically" unless they actually run a test.

---

### Item P4.4.8 — CC boundary interpretation (α=0.1 outperforms BM25 alone via "tie-breaking")

**Discussion (substantive — admission of unclear mechanism):**
- The brief's claim: at α=0.1, the result (0.5248) exceeds BM25 alone (0.4621), and the AI attributes this to "Dense's tie-breaking contribution."
- Mohammed and Osman struggled to understand the tie-breaking mechanism in convex combination. Specifically:
  - In CC, the score is (1−α)·BM25_norm + α·Dense_norm. If α=0.1, BM25 dominates but Dense still contributes.
  - Why would this *exceed* BM25 alone? Their hypothesis: maybe a tie-breaking rule built into the implementation prefers Dense over BM25 when scores are close, which happens to help in low-α settings.
  - They acknowledge they don't actually know what the implementation does for ties.
- Mohammed: "we don't fully understand the concept of tie-break here. Once we have time, we'll let the AI explain it. For now, accept the AI's caveat that we should present this as possibility, not established mechanism."

**Decision:** **REVISE** — present the tie-breaking explanation as a hypothesis ("a possible explanation is …") not a mechanism. Add this to the verification queue: investigate the actual tie-breaking behaviour of the CC implementation (and min-max normalization effect) before committing to either explanation in print.

---

### Item P4.4.9 — Framing "0.6267 nDCG@10 hybrid baseline is the target all subsequent QE methods must surpass"

**Discussion:**
- Mohammed accepts the declarative framing. The hybrid baseline is genuinely the strongest non-QE system.
- Side question: should the hybrid baseline now be added to the **baselines section** alongside BM25 alone and mDPR alone? Yes — the hybrid is no longer a "result" but the strongest baseline reference.

**Decision:** **APPROVE the framing.** **REVISE the structure:** add the hybrid (no QE) result to the baselines section so it sits alongside BM25-alone and mDPR-alone as a reference baseline. All subsequent QE results then compare against it as the strongest baseline.

---

### Item P4.4.10 — Recall@100: 0.9466 vs 0.9467 inconsistency

**Discussion:**
- Mohammed: "this is destruction" (joking about the typo). They checked the file — confirmed which value is correct.
- They want global consistency: pick one and apply thesis-wide.

**Decision:** **REVISE** — pick **0.9467** (the value from the source exp_012 doc, per the brief's recommendation), apply consistently across all tables, abstract, and downstream references.

---

### Item P4.4.11 (revisited from pt7) — Dense degradation in CSQE

**Discussion (substantial — they verify the data and identify a missing experiment):**
- Mohammed pulled up the actual numbers:
  - Aya CSQE Dense: **0.5915**
  - Aya blind Q2D Dense: **0.6164**
- This **confirms** dense degradation is real when comparing blind Q2D to CSQE on Dense alone.
- The two specific descriptive claims (1500 chars expansion length, mDPR trained on short queries) remain unverified — they reaffirm pt7's decision to verify or remove these specifics.
- **NEW INVESTIGATION (CRITICAL — connects to pt6 P4.2.5):** Mohammed proposes:
  - Run a **blind+blind hybrid**: apply vanilla blind Q2D to BOTH BM25 and Dense, then RRF/CC fuse them. Compare against:
    - Hybrid no QE (0.6267)
    - Config A (BM25-CSQE + Dense-blind / Dense-raw)
    - Config B (BM25-blind / BM25-raw + Dense-CSQE)
    - Config C (BM25-CSQE + Dense-CSQE)
  - If blind+blind hybrid > Config A, that proves the retriever-specific representation principle generalises beyond CSQE — even more powerful finding.
- Osman confirms: "I did NOT do this experiment. I did repetition for all models. I did hybrid for the original blind tests but not systematically asymmetric." So the gap is real.
- Mohammed: "if we find time, this is doable — it's not a complex experiment."

**Decision:**
- **APPROVE the dense degradation finding** with verification of the descriptive claims pending (per pt7).
- **NEW EXPERIMENTAL TASK:** run blind+blind hybrid (and possibly blind-asymmetric configurations parallel to Config A/B/C). This is the missing experiment that completes the retriever-specific representation argument. Add to the experimental backlog with HIGH PRIORITY if time allows.

---

## Cross-Cutting Insights & Action Items Raised in pt8

- **Recovery graph** for BM25 repetition (item P4.4.2) — task for the figure-plan workstream.
- **Statistical-test discipline (P4.4.7):** sweep the thesis for any "statistically X" claim; replace with "numerically X" wherever no statistical test was actually run. This is an honesty pattern they're enforcing.
- **Mechanism-vs-hypothesis discipline (P4.4.8, P4.4.11):** anywhere the AI states a mechanism that the team doesn't actually understand or hasn't measured, soften to "a possible explanation is …". Apply consistently.
- **Hybrid-baseline restructuring (P4.4.9):** elevate the hybrid no-QE result to the baselines section alongside BM25-alone and mDPR-alone, so it's positioned as a reference target.
- **Asymmetric blind Q2D experiment (P4.4.11 + P4.2.5):** new high-priority experiment to validate the generalisation of the retriever-specific representation finding beyond CSQE.
- **Number verification queue grows:**
  - Recall@100: 0.9466 vs 0.9467 → use 0.9467 thesis-wide (P4.4.10).
  - +26.7% Aya β=2 BM25 → confirmed correct (P4.4.6).
  - CSQE expansion ≈1500 chars → still pending verification.
  - mDPR short-query training → still pending citation verification.

---

## Items Touched But Deferred

- The CC tie-breaking mechanism (P4.4.8) — investigate when there's time; for now soften the wording.

---

## Items Not Yet Discussed

Continues with P4.4.12 (already covered in pt7 in some depth, but worth re-checking), P4.4.13 onward (complementarity claim, etc.), P4.4.15+ (Config A framing), P4.4.18 (key finding ranking — partially covered in pt7), P4.4.20 (per-query error analysis Config C/A — covered in pt5), P4.4.23–28 (representative examples, predictor language, recommendations placement, table layout), and all P4.5.x, P4.A.x, P4.X.x.
