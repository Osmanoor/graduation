# Phase A Completion Report — Core Narrative Rewrite

**Completed:** 2026-07-29 (single working session, Elhaj + Claude)
**Commits:** `3632926` (A1–A4) → `2256f44` (merge with Osman's C3 sweep) → `fb61ade` (A5) → `0e18539` (A6 + fact-check) → final A7 commit.
**Verification trail:** `A5_small_models_sweep_report.md` · `A5_edit_verification.md` · `A6_number_verification.md` · `A7_mapping_audit.md`

## What changed, per task

| Task | Outcome |
|---|---|
| **A1** Problem statement | §1.1 is now **one continuous funnel paragraph** (retrieval failures → short-query information poverty + Arabic vocabulary mismatch → pre-retrieval intervention → exact problem: how expansions are *generated* (blind/corpus-steered) and *where applied* in a hybrid), ending in the RQ. Three-gap structure and "small models" headline removed; resource angle kept as one clause. |
| **A2** Research question | New RQ: *"To what extent can LLM-based QE---blind and corpus-steered---improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms?"* De-scoped "model characteristics determine effectiveness" clause deleted everywhere (RQ, Ch.2 questions, Ch.5 lead-in). |
| **A3** Introduction funnel | Gap paragraph re-landed on QE-for-Arabic + retriever-placement + corpus-grounding gaps; accuracy-fixed twice after verification (see below). |
| **A4** Objectives | **9 measurable objectives** (was 8), 1:1 with experiments and Ch.5 paragraphs. Old obj 4+5 merged (comparison/selection, no "predict", no "ten"); interaction analysis promoted to its own objective; hybrid no-QE baseline and per-query error analysis now anchored. |
| **A5** De-emphasis sweep | Opus agent audited 55 occurrences (Ch.2–5): 41 kept as legitimate facts, 14 framing fixes applied. Ch.2 Research Gap rebuilt as **4 gaps** (language / retriever interaction / corpus grounding / hybrid placement) + 7 questions mirroring the objectives. Ch.5 opening, "model characteristics" lead-in, and Overall paragraph re-centred on CSQE + asymmetric fusion (small-model strength kept as closing point). |
| **A6** Conclusion cascade | 3 paragraphs added so all 9 objectives are checked off: Query2Doc engineering, **corpus/blind complementarity** (0.5381 / 0.5752 / 0.6157; fused margin honestly stated as +0.0055), **per-query gains localisation** (56.8% improved, buckets, first-pass 0.8877 vs 0.5814). Every figure verified against raw CSVs. |
| **A7** Mapping audit | Chain verified sound: 9/9 objectives have Ch.3 + Ch.4 + Ch.5 anchors; 0 orphan conclusion paragraphs; all 7 Ch.2 questions map. 6 blockers fixed (see below); B5 (stale abstract) deferred to B1. |

## Errors caught by verification (would have been examiner ammunition)

1. **False population claim** (ch4 §4.9.3): "all 1,061 big-wins = CSQE 1.000/Blind 0.000" — true for only 143/1,061; over-generalised from an example-finding filter. Corrected. (The 1,061 = 1,061 first-pass/big-win collision itself is a verified coincidence — overlap only 389.)
2. **Self-contradicting "black box" claim** (Ch.1 + Ch.2, introduced during A5): Query2Doc *does* construct queries per-paradigm; rewritten as "adapts only the surface form … no study establishes which retriever in a hybrid should receive it."
3. **"Unexamined in any language" overclaim**: expansion↔paradigm interaction was studied for English (Query2Doc, MuGI, GRF-dense, CSQE §4.2); gap rescoped to **hybrid placement**, which truly is unstudied anywhere.
4. **Understated novelty**: Lei et al. never ran a corpus-only ablation — exp 013c is the first in any language. Ch.2 now says so.
5. **Literature-axis distortion** (caught by Mohammed): modern QE era is defined by *scale* (175B→7–8B), not proprietary→open. Corrected; rule saved to memory.
6. **Runtime misattribution**: "40 min" = generation stage over 2,896 queries (not "full-corpus experiment", which is 45–48 min); quantisation/two-notebook are enablers, not speed-ups.
7. **"Optimal β" misstatement**: only Aya + Jais-2 peak at adaptive β=2; seven models peak at fixed n=5–10. Corrected with ch.4's own attribution (pseudo-document length).
8. **Licence honesty**: headline 0.7137 comes from Aya Expanse 8B (CC-BY-NC); "practical for real-world deployments" now reads "subject to the licence of the chosen generator", with Apache-2.0 alternatives noted. §3.5.1 criterion 3 aligned.
9. Minor: Recall@100 rounding 0.9467→0.9466 (5 sites); NDCG/MRR/HyDE/GRF duplicate definitions removed; "Normalized"→"Normalised" (3 files).

## Open items (decisions for Elhaj/Osman — full list in task-file "Phase A review flags")

1. §1.1 closing sentence still names the asymmetric/sparse-only finding — recommendation: keep pipeline, drop the finding detail.
2. Optional: reinstate the word "small" once in Objective 4.
3. **Pre-submission literature re-verification**: monolingual-Arabic gap claim only searched at sub-7B scope; obtain Macmillan-Scott 2025 (evaluates MuGI/Exp4Fuse incl. Arabic, cross-lingual); MuGI/Exp4Fuse have no first-hand summaries.
4. Aya licence caveat placement (Overall vs Limitations).
5. Osman: review 9-objective structure (G1) + LoF/LoT order vs faculty guideline (C1 flag).
6. Deferred to later passes: full "open-source"→"openly available" sweep + SILMA naming (D5); abstract rewrite carries A7 blocker B5 (B1).

## Not yet done

- **Push**: all Phase A commits are local-only pending Elhaj's go.
- **Compile check**: prose-only edits, but a full xelatex run is due before the next editing round.
- **Phase B** (abstracts) is now unblocked.
