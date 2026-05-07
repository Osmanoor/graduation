# pt4 Analysis Notes — 23.1.2026 Part 4

**Source:** `meetings/23.1_2026.pt4.md` (123 lines)
**Speakers:** Mohammed, Osman
**Coverage:** Phase-4 objectives discussion (P4.1.1, P4.1.3 implied), then **1.4, 1.5, 1.6, 1.7**, then **5.1, 5.4, 5.5, 5.6 → 5.9**. Ends with plan to continue tomorrow at 5am.
**Notable:** Significant honesty discussion about how research was done sequentially (not from a plan); long tangent about ALLaM (referred to as "LLaMA") that surfaces a real grievance.

---

## Per-Item Discussion & Decisions

### Items P4.1.1 / P4.1.3 (Phase-4 objectives 6–8) — opening discussion

**Discussion:**
- Osman openly: "our experience was all sequential — one thing led to the next. There was no strict plan; it was just one thing after another." He doesn't see another way the objectives could be written except by retrofitting them from the experiments.
- Mohammed acknowledges the risk: Dr. Tahani would interrupt them on this if presented as if the objectives were pre-planned. They both know.
- The reframing has been done and they feel it's "decent" — not perfect, but the best honest reconstruction available.

**Decision:** **APPROVE — with caveat that the objectives are honestly retrofit from the experiments.** They accept this reality and will defend it as such. No new wording change beyond what was already discussed in pt2 for item 2.7.

---

### Item 1.4 — Five objectives mapping to Ch.3 methodology

**Discussion:**
- Brief — they reaffirmed the original 5 objectives are accurate to the work. Phase 4 added objectives 6–8.
- They want the AI to flag any objective it suggests adding — open invitation for the AI to propose more if it sees coverage gaps.

**Decision:** **APPROVE** — keep the existing 5 + Phase 4 additions. AI invited to suggest additional objectives if applicable.

---

### Item 1.5 — Objective 4 says "ten" open-source LLMs (vs 11 attempted)

**Discussion (substantive):**
- Inconsistency identified: Objective 4 says "ten LLMs with 2–8B parameters" but the literature review (Ch.2) describes 11 models, and the research-gap section also says 11. Methodology and results say 10.
- Osman: GPT-OSS was a *fallback* that got dropped — when the original 10 ran into issues, GPT-OSS was added as an attempted replacement. So originally 10 was the goal.
- Mohammed wants to keep "10" in the objective since 10 were actually evaluated. The 11 in Ch.2 is because they did literature research on all 11.
- **Bigger discussion that branches:** Mohammed wants to **delete GPT-OSS from the entire thesis** because it didn't produce results. Osman wavers. They notice the AI added a sentence claiming the model was included to "evaluate whether English-dominant MoE can do Arabic QE" — both find this framing fabricated (Mohammed wanted that "English-dominant" claim verified back in pt1).
- Osman raises the wider issue: this framing makes the thesis read like a **systematic evaluation of 10 models** ("ablation study") which is NOT the contribution. The real contribution is the technique (QE for Arabic RAG); the 10-model evaluation was an extensive but secondary validation.
- Tension: Osman points out the model comparison "took the most time of any work-stream", so calling it secondary feels off. But Mohammed is firm — extensive ≠ central.

**Decision:** **REVISE — multi-part:**
1. Use **10** consistently (objectives, methodology, results, abstract).
2. Use **11** only in Ch.2 literature review where the broader research is being described — and label it that way ("we surveyed 11 candidate models, of which 10 were ultimately evaluated").
3. **Re-decide GPT-OSS retention later** when reviewing Ch.2/Ch.4 model description sections. Working preference: delete GPT-OSS entirely from the thesis if time permits; otherwise keep with honest "dropped due to MoE inefficiency" framing.
4. Anywhere the AI invented framing for *why* GPT-OSS was included (e.g., "English-dominant MoE evaluation"), remove that framing. Same applies to ALLaM if similar.
5. Reframe the model comparison so it's clearly an extensive validation step, not the central contribution. Avoid wording that reads like "systematic evaluation of 10 models was the goal."

---

### Item 1.6 — No references in Chapter 1

**Discussion:** Brief. Confirmed Dr. Tahani's instruction.

**Decision:** **APPROVE.**

---

### Item 1.7 — Thesis Layout describing Ch.2–5 in one paragraph each

**Discussion:**
- Currently Ch.2 description is "written weirdly, all in one paragraph without sub-headings."
- Mohammed feels each chapter description should be a clear bullet point, not a flowing paragraph.
- Want to check with Dr. Tahani whether the current paragraph form is acceptable or whether bullets would be better.

**Decision:** **DEFER TO SUPERVISOR** — ask Dr. Tahani: paragraph form vs bullet points for the thesis layout section. Working preference: bullets for clarity. Add to the supervisor questions list.

---

### Item 5.1 — Six conclusion topics

**Discussion (positive, with substantive observations):**
- Both think the conclusions are excellent overall. Mohammed went through them one by one:
  - Baseline + error analysis: solid.
  - Query2Doc transfer: solid.
  - Comprehensive model comparison: solid.
  - Analytical findings on model characteristics: solid (this is the "secondary" finding line).
  - **"Dense retrieval responds differently to query enhancement"**: Mohammed praises this as a surprisingly clean finding.
  - **"Query repetition reports..."**: Mohammed praises — the fix works immediately and clearly.
  - **Hybrid is always better**: Mohammed observes this is a beautiful finding too. Hybrid-no-QE > non-hybrid-no-QE; Hybrid-with-QE > non-hybrid-with-QE.
  - **Corpus-steered + retriever-specific representation**: praised as the strongest finding.

**A new investigation idea raised mid-discussion (Mohammed):**
- Does the **retriever-specific representation principle apply to vanilla Query2Doc (blind QE) too**? The Phase 4 finding was for CSQE; if it also holds for blind Q2D, that would be a much stronger generalisation.
- Osman: "I think I almost tried that — Hybrid with both fusion approaches on the Q2D experiment." But neither of them remembers the exact configuration (alpha values, CC vs RRF). They're not sure if they tested asymmetric Q2D explicitly.
- This is a gap — the Hybrid + Q2D experiment was done but the asymmetric variant (Q2D applied only to BM25, not Dense) was not clearly tested.

**Decision:** **APPROVE conclusions as listed.** **NEW WORK ITEM:** investigate whether the retriever-specific representation principle generalises to vanilla Query2Doc. If it does, that's a much stronger conclusion. Add to the experimental backlog.

---

### Item 5.4 — Six challenges

**Discussion (per-challenge):**

1. **Resource constraints:** Mohammed initially joked "we never had resource constraints" but on reflection the thesis is right — they were forced to limit to 8B parameters and to engineer batching/optimization to fit T4/A100. The 40-minute-per-evaluation constraint is real.
   - **Decision:** **APPROVE.**

2. **BM25 term-dilution challenge:** Long debate.
   - Osman: "this isn't really a challenge — we just ignored a tip from the original paper and discovered the hard way."
   - Mohammed: "but the negative finding *was* in the original paper; what was new is that we validated it in Arabic with morphological richness."
   - Tension unresolved. Mohammed leaned toward keeping it as a challenge with the framing "we encountered the documented term-dilution effect; addressed it with query repetition (per Phase 4)."
   - **Decision:** **APPROVE WITH REWORDING** — keep as a challenge but acknowledge the precedent in the original paper and frame the resolution honestly.

3. **Dropped models (LLaMA — they mean ALLaM):** Long discussion with substantive honesty issue.
   - Osman has lingering frustration with how ALLaM was treated in the experiment. He showed Mohammed: ALLaM was generating actual content but with dashes ("daash") instead of spaces between every word. Their evaluation pipeline counted the dash-injected output as garbage.
   - Osman: "with simple post-processing (just remove the dashes), ALLaM would have given good results. The score it received was unfair."
   - Mohammed: "but we have to be fair — we'd need to apply the same post-processing to all models."
   - Osman: "we could apply post-processing to all of them."
   - **Tension unresolved on whether to retroactively rerun ALLaM.** They acknowledge the methodology was uniform (no special treatment for any model) which is defensible. But Osman is uncomfortable that ALLaM was effectively penalised by a tokenizer artifact rather than by actual model quality.
   - **Decision:** **REVISE — open question:**
     - (a) Keep ALLaM result as-is, but in the "Dropped models" challenge section explicitly mention that ALLaM's poor result was likely due to a sentencepiece tokenizer artifact (`▁` leakage rendered as dashes), not a fundamental model issue.
     - (b) Re-run ALLaM with post-processing applied uniformly to all models, and update the leaderboard if results change materially.
     - **Working preference: (a)** — honest disclosure within the challenges section without re-running. Re-running uniformly across all 10 models is too expensive at this stage.

4. **"BM25 query repetition... implemented in Phase 4":** Mohammed flagged: "Phase 4" terminology must be removed (matches **P4.X.4**). The sentence itself is fine; just delete the "in Phase 4" phrasing.
   - **Decision:** **REVISE** — remove "Phase 4" terminology. Replace with "in subsequent experiments" or similar.

5. **Dataset scope:** They tied this to the missing Ch.2 dataset analysis section (item 2.1). Their original investigation evaluated multiple Arabic datasets (Mr.TyDi, SADIE, etc.) and chose MIRACL because it had the right combination of (1) MSA, (2) judged relevance, (3) sufficient size. **MIRACL lacks metadata** — this became a real challenge for the chunking-aware QE work-stream they wanted to do.
   - **Decision:** **APPROVE WITH ADDITION** — extend the dataset-scope challenge to mention MIRACL's lack of metadata which blocked the chunking-aware extension.

6. **Single QE technique / baseline retriever strength:** Not explicitly debated. Implicitly OK but matches the 5.5 / 3.3 weak-baseline issue.

---

### Item 5.5 — Weak baseline framed as deliberate

**Discussion:** Confirmed: same decision as item **3.3**. Drop the "intentional" framing. They acknowledged this is exactly the post-hoc rationalisation Dr. Tahani would challenge.

**Decision:** **REVISE** — soften or remove. Match exactly what's done in item 3.3 (whichever wording they choose there).

---

### Item 5.6 — Eight recommendations ordering

**Discussion:** Reviewed alongside the individual recommendations below.

**Decision:** Will be subsumed by the per-recommendation decisions below.

---

### Item 5.7 — Recommendation 1 (knowledge-base-aware / chunking-aware QE)

**Discussion:**
- They want to keep this and possibly elaborate. The MIRACL dataset has section headings but no real structured metadata they could exploit.
- Osman: this was in their **original plan but didn't happen** because of dataset constraints. Should be honest in the recommendation: "we wanted to do this; we couldn't because of dataset metadata gaps."
- Suggest: identify suitable datasets that *do* have metadata (hierarchical structure, section headings, article boundaries) before recommending this work to others.

**Decision:** **APPROVE WITH ADDITION** — keep Recommendation 1 prominently. Add: dataset selection criterion (suitable metadata for chunking-aware extension). Possibly mention this was an originally planned direction blocked by MIRACL's metadata gap.

---

### Recommendations 2 and 4 (BM25 query repetition; Hybrid retrieval with QE)

**Discussion:**
- Both **already implemented** in Phase 4. Mohammed: "should be deleted entirely from recommendations." Osman agrees.
- The brief had proposed converting them to a "now-implemented" note (item P4.5.7) — Mohammed and Osman are more aggressive: just delete them.

**Decision:** **REVISE** — DELETE Recommendations 2 and 4 from §5.3 entirely. Optionally add a one-sentence note in the conclusion that these directions, listed at the proposal stage, were addressed during the project.

---

### Item 5.8 — Recommendation 5 (dialectal Arabic)

**Discussion:**
- Mohammed initially wanted to remove because it's too speculative (the AI flagged this).
- Then reconsidered: there's a real underlying intuition. LLM-based QE could plausibly help bridge MSA↔dialect gaps by generating MSA pseudo-documents from dialect queries — that's testable future work, not pure hand-waving.
- Decision tentatively to keep with softer framing.

**Decision:** **APPROVE** — keep Recommendation 5 but soften the speculation. State it as "may help bridge MSA-dialect retrieval gaps; this requires evaluation on dialect-aware datasets."

---

### Item 5.9 — Recommendation 8 (publication)

**Discussion:**
- Mohammed: "this gets deleted immediately." It's presumptuous for the AI to claim the results are publication-ready.
- This is a discussion the supervisor would have, not a self-claim.

**Decision:** **REJECT / DELETE** — remove Recommendation 8 entirely from §5.3.

---

### Phase-4 Recommendations (P4.5.8 — first-pass quality gate, asymmetric expansion, stronger retrievers)

**Discussion:**
- First-pass quality gate: Mohammed praised — directly addresses Type B regressions.
- Asymmetric expansion weighting: ties to the broader new-investigation question (does asymmetric Q2D work?).
- Stronger embedding models (BGE-M3, mE5-large): Mohammed: "this is beautiful." Keep.
- The recommendation about future work that's already done — Mohammed wants those deleted (matches Recommendations 2/4 above and the existing items P4.5.7).

**Decision:** **APPROVE the three new Phase 4 recommendations** (first-pass quality gate, asymmetric expansion, stronger retrievers). **DELETE** any "implemented in Phase 4" placeholder recommendations from the original list.

---

## Cross-Cutting Insights & Action Items Raised in pt4

- **"Phase 4" terminology purge:** confirmed multiple instances need removal (matches P4.X.4). Add to the global find-and-replace task.
- **GPT-OSS retention question:** working preference is to delete from the thesis entirely. Final decision deferred to when the team revisits the model description sections.
- **ALLaM (referred to as "LLaMA") fairness question:** unresolved tension between methodological purity (no per-model post-processing) and acknowledging the unfair tokenizer-artifact penalty. Working preference: keep result, but disclose the artifact in the dropped-models challenge section honestly.
- **Asymmetric Q2D investigation:** new experimental question raised — does the retriever-specific representation principle apply to vanilla Query2Doc, not just CSQE? If yes, it's a much stronger conclusion. Add to the post-thesis experimental backlog (or do before submission if time).
- **Dataset analysis section task** (already from pt1/2): explicit linkage now to challenges section — MIRACL's metadata gap blocked chunking-aware extension and this needs to be in both the Ch.2 dataset section and the Ch.5 challenges/recommendations.
- **Supervisor questions list grows:**
  - Q1 (chapter summary section yes/no, item 2.3) — pt1
  - Q2 (general vs specific problem statement, item 2.7) — pt1
  - Q3 (technology-driven narrative for Ch.1, item 1.1) — pt3
  - Q4 (paragraph vs bullets in thesis layout section, item 1.7) — pt4

---

## Items Touched But Deferred

- **Item 4.16 / 1.5** (10 vs 11 model count consistency): cross-cutting global edit needed wherever the count appears.
- **Items P4.5.x** (Phase 4 conclusion paragraphs): mostly approved but ordering decision (item P4.5.1 — where the "Overall" paragraph sits relative to Phase 4 conclusions) not finalized.

---

## Items Not Yet Discussed

Continues with abstract items (A.1–A.5), cross-cutting (X.1–X.6), and Phase 4 details from item P4.2.x onward in pt5.
