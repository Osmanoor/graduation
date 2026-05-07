# pt3 Analysis Notes — 23.1.2026 Part 3

**Source:** `meetings/23.1_2026.pt3.md` (985 lines, but content from line ~363 onward is duplicated 5×; unique material is lines 1–362)
**Speakers:** Mohammed (driving), Osman
**Coverage:** Confirms decision on **3.3** from pt2; then **3.4 → 3.13**, **4.1 → 4.16**, and start of **Chapter 1 (item 1.1)** discussion (item 4.13 mostly absorbed into a joke).
**Notable:** Several honesty moments where they admit the AI fabricated rationales for their experimental choices (3.9 diminishing returns, 3.10 16x speedup).

---

## Per-Item Discussion & Decisions

### Item 3.3 (continued from pt2) — mDPR weak baseline framing

**Discussion:** Confirmed: drop the "intentionally weaker baseline for headroom" framing entirely. They chose mDPR because they had a working pipeline on it; "not fine-tuned on MIRACL" stays as a factual statement.

**Decision:** **REVISE** — drop the strategic framing. Keep only neutral facts about mDPR.

---

### Item 3.4 — BM25S achieves 96% of official Pyserini BM25 performance

**Discussion:** Brief — Osman confirmed it's documented. Implementation was easier and the gap is small.

**Decision:** **APPROVE.**

---

### Item 3.5 — Java 21/11 dependency conflict as the reason for choosing BM25S over Pyserini

**Discussion:** Confirmed — Java conflict was real, BM25S is more efficient and recent, decision was sound.

**Decision:** **APPROVE.**

---

### Item 3.6 — Error analysis thresholds: Failed (<0.3), Mediocre (0.3–0.7), Successful (≥0.7)

**Discussion (substantial — connects to 3.7):**
- Mohammed: the AI says "thresholds come from your error analysis documentation" but admits there's no clear *justification* for these specific cutoffs. Why 0.3 vs 0.4? Why 0.7 vs 0.6? Arbitrary.
- They opened the thesis and confirmed the numbers are mentioned in §3.3 but without rationale.
- Osman: candid admission — "we didn't really lean on this analysis heavily." It informed the decision to focus on Query2Doc, but post-experiment they have a much better understanding.
- They noticed the **Phase 4 error analysis (later, §3.9)** uses *different* thresholds (Failure < 0.1, Big Win Δ > 0.3, Regression Δ < −0.1). Two threshold systems exist in the thesis (the original Phase-1 absolute thresholds vs the Phase-4 paired-comparison deltas). This matches the issue flagged in **item P4.3.17.**

**Decision:** **REVISE** — re-do the original error analysis with better justified thresholds (and bucketing) to make the whole thesis "data-driven" coherent. This connects directly to 3.7 (recalculate query length buckets too). Mohammed will redo this and update §3.3 + downstream.

---

### Item 3.7 — Query length buckets: Short (1–3), Medium (4–8), Long (9+)

**Discussion (substantial):**
- They opened the relevant tables and noticed an **inconsistency**: the original error analysis (§3.3, table 4.6) buckets are 1–3, 4–8, 9+ in **tokens**, while the Phase 4 error analysis (§4.10, table 4.26) uses Short < 5 words, Medium 5–9 words, Long ≥ 10 words.
- The original buckets are probably too narrow ("1–3 tokens" is very short).
- They want consistency: re-do the original error analysis with the same word-based buckets the Phase 4 analysis uses. Files are saved in Drive, recalculation is easy. Documentation needs to be updated alongside.
- Osman's worry: "won't recalculation change the findings?" Mohammed's reply: probably not the headline findings (short queries benefit most from QE, long queries benefit too) but it might shift specific numbers.

**Decision:** **REVISE** — recalculate the original error analysis with:
1. Consistent word-based buckets matching the Phase 4 analysis (or vice versa — pick one and apply throughout).
2. Better-justified threshold rationale for 3.6.
3. Update §3.3 documentation and any downstream §4 sections that reference these numbers.
4. Reframe to emphasize "data-driven decisions": this analysis is what motivated the focus on Query2Doc, so make that linkage explicit.

---

### Item 3.8 — System prompt for query expansion

**Discussion:** Brief — confirmed the prompt is the same across all model notebooks. Only the corpus-steered prompt is different.

**Decision:** **APPROVE.**

---

### Item 3.9 — Max tokens = 128 with claim "256 showed diminishing returns"

**Discussion (honesty moment):**
- Osman: "we initially tried 256, found it took too long, dropped to 128." That's it.
- Mohammed: "I don't think we ever computed any diminishing return." They never measured the 256 quality.
- "نجفناها أيوة" — "we just made it up." They acknowledge laughingly that the AI invented the diminishing-returns justification.
- **Plan:** they could actually test this — run 256 vs 128 on the main Aya experiment (pre-hybrid, pre-CSQE), check if results differ. If similar → 128 is justified. If different → may need to revise the choice.
- Realistic assessment: probably won't run the experiment ("not every point becomes a new experiment"). So tag as "noted, do if time permits."

**Decision:** **REVISE** — remove the "diminishing returns at 256" justification from the thesis since it's fabricated. Either:
- (a) State plainly: "128 was chosen for inference speed; we did not formally test 256 vs 128 quality."
- (b) Run the 256 vs 128 comparison on Aya (one experiment) if time allows, and update the justification with real data.

---

### Item 3.10 — "16x combined speedup" (8x batching × 2x token reduction)

**Discussion (honesty moment):**
- Mohammed read the AI's claim: "16x combined speedup from batch processing + reduced tokens + inference optimizations."
- Osman: "we made this up too." They never measured the multiplicative speedup.
- They reasoned it through: 8 hours sequential → 40 minutes after optimizations → that's roughly 12x, not 16x. The 16x is wrong arithmetic, the 12x might be defensible.
- The breakdown (8x batching × 2x tokens) is also fabricated math, not measured.
- The *individual* claims are real: batching, half precision, eval mode, 256→128 — each contributed. The *combined multiplier* is the made-up part.

**Decision:** **REVISE** — replace the "16x combined speedup" with what they actually observed:
- (a) State the wall-clock change: "from ~8 hours sequential to ~40 minutes" — that's a measurable real result.
- (b) List the optimizations that contributed (batching, half precision, eval mode, 128 tokens) without claiming a precise multiplier per optimization.
- (c) Don't claim 16x; if pressed, "approximately 12x wall-clock improvement."

---

### Item 3.11 — Temperature: SILMA tested at 0.7 vs 0.1 with 0.1 yielding +2.5%

**Discussion:**
- Mohammed flagged that the AI wrote "tested at 0.0 and 0.1" — the 0.0 is wrong. The actual temperature range was higher (Mohammed thinks it was 0.7 vs 0.1, possibly 0.8 vs 0.1).
- This needs a verification against the SILMA experiment notebook to get the right numbers.

**Decision:** **VERIFY then REVISE** — confirm the actual temperatures tested in the SILMA experiment and correct the text. Likely 0.7 vs 0.1, not 0.0 vs 0.1.

---

### Items 3.12, 3.13 — Work division and Table 3.2 model configs

**Discussion:** Not explicitly discussed in pt3. Implicitly accepted as factual.

**Decision:** **APPROVE (implicit)** — to verify in later transcripts if revisited.

---

### Item 4.1 — All numerical results

**Discussion:**
- Brief. Osman confirmed CLAUDE.md is the source of truth, he checks it after experiments and updates it.
- Mohammed asked about Gemini check: "yes, looked correct."

**Decision:** **APPROVE.**

---

### Item 4.2 — mDPR baseline "0.4993 reproduced with less than 0.1% difference vs published 0.499"

**Discussion (clarification):**
- Osman: the *real* situation is they reproduced the baseline **exactly** — both got 0.4993. The published paper just rounded to 0.499. There's no actual ~0.1% difference; it's a presentation/rounding artifact.
- Plan: round their own number to 0.499 to match the paper, or acknowledge they reproduced exactly.

**Decision:** **REVISE** — change the framing from "less than 0.1% difference" to either:
- (a) "reproduced exactly (the published paper reports 0.499; our measurement is 0.4993, identical when rounded to the same precision)"; or
- (b) round their own number to 0.499 for visual consistency.
- Sweep wherever this is mentioned in the thesis.

---

### Item 4.3 — Percentage improvements (e.g., +23.5% for Aya)

**Discussion:** Spot-checked — math is straightforward. Approved.

**Decision:** **APPROVE.**

---

### Item 4.4 — Attributed BM25 degradation to "term dilution" (Wang 2023)

**Discussion:** Confirmed — Wang's Query2Doc paper documents this phenomenon. Their experiment confirmed it (BM25 improved when they added query repetition). Solid grounding.

**Decision:** **APPROVE.**

---

### Item 4.5 — "Arabic benefits disproportionately from vocabulary expansion" hypothesis

**Discussion (significant — REJECT):**
- The AI used this hypothesis to explain why their 3B model improved BM25 by +8.9% while the original Wang 2023 paper (175B model, English) reported smaller improvements.
- Both Mohammed and Osman: **the comparison is invalid.** Different model, different dataset, different language, different baseline, different margins. There's no valid basis to say "Arabic helped us more than English helped them" because too many variables differ.
- Osman: "this interpretation should be removed."

**Decision:** **REJECT / REMOVE** — delete the "Arabic benefits disproportionately" hypothesis from §4 entirely. Same decision applies to **item 5.2** (where it reappears in conclusions).

---

### Item 4.6 — Model parameter count positively correlated with dense improvement

**Discussion:**
- The trend is real and visible — particularly clean within the Qwen family (Qwen 2.5-3B → Qwen3-4B → Qwen 2.5-7B → Qwen3-8B).
- AI noted no formal correlation coefficient was computed. Mohammed thinks they could compute it from the numbers they have.
- Caveat raised: cross-family comparison is harder (Qwen3-4B is newer architecture than Qwen 2.5-3B, so 4B vs 3B confounds size with generation). Restrict the correlation to the **Qwen family only** for cleanliness.

**Decision:** **REVISE** — add a real correlation coefficient (Pearson or Spearman) restricted to the **Qwen family** (4 data points: 2.5-3B, 3-4B, 2.5-7B, 3-8B). Also note the cross-generation confound for the broader claim. Don't compute correlation across all 10 models because too many other variables differ.

---

### Item 4.7 — "Arabic NLP benchmark scores do not directly predict QE quality"

**Discussion:**
- They like this finding (it's a strong and publishable observation: a 3B model with a lower OALL score outperformed Falcon-H1-3B with a higher OALL).
- **Concern:** what specific benchmark are they invoking? The AI says "Arabic NLP benchmark" — is that OALL, AraGen, AMMLU, SILMA leaderboard, or something else? Mohammed isn't sure where this comes from.
- They need to clarify exactly which benchmark is being claimed not to predict QE — otherwise the claim is too vague to defend.

**Decision:** **REVISE** — keep the finding, but **specify which benchmark(s)** are being referenced (e.g., OALL specifically, or "Arabic LLM leaderboards generally"). Verify the comparison cited (Falcon-H1 vs Qwen 2.5 3B) is correct on that benchmark before printing.

---

### Item 4.8 — Jais-2 BM25 success attributed to 150K Arabic-centric vocabulary

**Discussion:**
- Mohammed and Osman both find this plausible. Larger Arabic vocabulary → generated pseudo-documents use richer Arabic terms → closer match to BM25 index vocabulary → better BM25 performance.
- Osman initially didn't follow the term-distribution argument but Mohammed re-explained it.
- **Cross-cutting note (Osman):** "BM25" vs "BM25S" usage in the thesis — is it consistent? They confirm it's all BM25S (with their specific config), but in the writing they sometimes say "BM25" generically. They want a notation convention upfront: when we say "BM25" we mean "BM25S with [X config]."

**Decision:** **APPROVE the hypothesis** as a hypothesis (not a proven mechanism — "may be due to"). **Cross-cutting REVISE:** add a notation note at the start (Ch.2 or Ch.3) clarifying that "BM25" in the thesis refers to BM25S with their specific configuration, like other papers use BM25 generically.

---

### Item 4.9 — Aya BM25 success attributed to purpose-built multilingual training

**Discussion:**
- Same shape as 4.8. Plausible but not isolated. Could be training data, alignment, instruction tuning — many factors.
- They acknowledge they can't truly know without controlled training experiments.

**Decision:** **APPROVE as hypothesis** — present as a possibility, not a proven mechanism. Same wording standard as 4.8.

---

### Item 4.10 — Qwen generational comparison (training data 36T vs 18T tokens)

**Discussion:** Not explicitly addressed in pt3 (covered indirectly under 4.6).

**Decision:** **APPROVE (implicit)** — flag for revisit.

---

### Item 4.11 — Dense "universally benefiting" while BM25 "divergent"

**Discussion:** Not explicitly addressed in pt3.

**Decision:** **APPROVE (implicit).**

---

### Item 4.12 — "Best Model Recommendations" section

**Discussion (touched lightly):**
- Mohammed acknowledged Aya is "the best model we found across our experiments" but Osman pushed back on framing this as a universal recommendation: "we found it good *for our use case*. Telling everyone to use Aya for any QE work is too strong."

**Decision:** **REVISE** — soften the "recommendation" framing. Phrase as "Aya was the strongest model in our experiments on MIRACL Arabic" rather than "use Aya for QE." Avoid universal recommendations.

---

### Item 4.13 — BM25 results for Osman's models

**Discussion:**
- Comic relief: Mohammed and Osman joked about the AI flagging "Osman's models — verify if they were actually run or projected" because Osman's documentation is terser than Mohammed's (one report vs ten reports).
- They affirm: yes, all of Osman's BM25 numbers are real measurements. The AI was fooled by Osman's lighter documentation style.

**Decision:** **APPROVE — no changes, no further verification needed.** All numbers are accurate.

---

### Item 4.14 — 12 tables total

**Discussion (substantive):**
- Three concerns:
  1. **Completeness:** the summary table is missing things ("ناقصة حاجات كتيرة").
  2. **Rendering:** some tables overflow the page width — formatting issue.
  3. **Tables vs figures:** they recall a guideline (Dr. Tahani or general academic) preferring figures over tables. Want fewer tables, more figures.

**Decision:** **REVISE** — task list:
- (a) Audit each table for completeness and accuracy.
- (b) Fix page-overflow rendering issues.
- (c) After Phase 4 figure plan is finalized (4.15), move data into figures where it works better, keeping tables where they're genuinely the right format.

---

### Item 4.15 — 2 placeholder figures

**Discussion (operational):**
- Both agree they need a comprehensive figure plan. The current 2 placeholders are not enough; the post-Phase-4 thesis has more material.
- **Process question:** who creates the figures? Options discussed:
  - (i) Gemini generates a figure-plan document (it has the full context).
  - (ii) Mohammed/Osman drafts the figure-plan document.
  - (iii) Both produce parallel proposals, then merge.
- After agreeing on the figure list and descriptions, Claude implements them in LaTeX.

**Decision:** **REVISE — two-phase plan:**
1. Generate a figure-plan document (Mohammed will draft it, possibly comparing with a Gemini-generated version).
2. Once figure descriptions are agreed, Claude inserts them into the LaTeX thesis.
This is a follow-up workstream, not just a revision.

---

### Item 4.16 — Experiment numbers in Table 4.10

**Discussion:**
- Both agree: **delete experiment numbers entirely** from the thesis. They're internal-only naming, not meaningful to readers.
- Mohammed: even *he* mis-uses the numbers ("I keep calling things 21 and I don't know why"). The internal numbering is unstable and not load-bearing.
- Refer to experiments by descriptive name instead ("Aya experiment", "initial experiments", "Query2Doc experiments", etc.).

**Decision:** **REVISE** — remove all experiment numbers from the thesis. Replace with descriptive names. When in a paragraph dedicated to one experiment, just say "this experiment."

---

### Item 1.1 — Four introductory paragraphs / funnel structure

**Discussion (significant — narrative honesty issue):**
- Inconsistency identified: Ch.1 narrative funnels Arabic → RAG → QE → gap, while Ch.2 related-work funnels QE → Arabic. Different ordering of the same elements.
- **Real problem (Osman):** the Ch.1 narrative is *problem-driven* (start from Arabic challenges, find QE solutions). But their actual research process was *technology-driven* (look at QE techniques, see what works on Arabic). The narrative misrepresents how they actually worked.
- Mohammed and Osman recall Dr. Tahani saying: "you're engineers, technology-driven approach suits you." But they're unsure whether she meant:
  - (a) "this approach suits you for the work" (an OK way to do research), or
  - (b) "this approach suits you for the narrative too" (an OK way to *write* the thesis).
- They want to ask Dr. Tahani directly: can the thesis be written as a technology-driven narrative honestly, or should they continue with the problem-driven funnel even though it's retrospective?

**Decision:** **DEFER TO SUPERVISOR** — explicit question for Dr. Tahani: is a technology-driven narrative acceptable for the thesis, or should we keep the problem-driven funnel? Working preference: switch to honest technology-driven narrative.
- Side decision: the funnel structure should only apply to **Related Work (§2.4)**, not to the Ch.1 narrative.
- Side decision: Ch.1 vs Ch.2 ordering inconsistency must be resolved either way.

---

## Cross-Cutting Insights & Action Items Raised in pt3

- **Fabricated-rationale pattern (third pattern identified, after pt2's decorative-citation and cited-but-unread):** the AI is observed inventing technical justifications that were never measured (3.9 diminishing returns, 3.10 16x speedup). They've now caught this pattern three times in two transcripts. **Whenever the AI offers a precise multiplier, threshold, or "X tested vs Y" claim, sanity-check before keeping.**
- **BM25 vs BM25S notation:** add a one-line convention upfront — "BM25 in this thesis refers to BM25S with [config]." Then use BM25 throughout.
- **Recalculation workstream:** error analysis must be re-run with consistent buckets/thresholds across Phase 1 and Phase 4 sections (items 3.6, 3.7).
- **Figures workstream:** figure-plan document must be drafted before LaTeX implementation (item 4.15).
- **Experiment numbering:** drop entirely (item 4.16).
- **Honesty-over-narrative principle confirmed again:** apply it to mDPR (3.3), to "Arabic benefits disproportionately" (4.5/5.2), to fabricated speedups (3.9/3.10), and to the Ch.1 narrative (1.1). The team is consistent in wanting to remove invented justifications.
- **Dr. Tahani questions accumulating** — keep a list of supervisor questions for the next meeting:
  - Q1: Chapter summary section yes/no? (item 2.3, from pt1)
  - Q2: Problem statement general vs specific? (item 2.7, from pt1)
  - Q3: Technology-driven narrative acceptable for Ch.1? (item 1.1, from pt3)

---

## Items Touched But Deferred

- **Item 5.2** — same decision as 4.5 (REJECT/REMOVE the Arabic-disproportionate hypothesis). Apply when reaching Ch.5.
- **Items 1.2, 1.3, 1.4** — connected to the Ch.1 narrative redesign (item 1.1). Will be revisited.
- **Items 5.5** — same decision as 3.3 about the weak-baseline framing. Apply when reaching Ch.5.

---

## Items Not Yet Discussed

Continues from Ch.5 (5.1, 5.3, 5.4, 5.6–5.9), abstract, cross-cutting (X.1–X.6), and all Phase 4 items in pt4 onward.
