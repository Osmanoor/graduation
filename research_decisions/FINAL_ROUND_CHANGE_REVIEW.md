# Final-Round Change Review — for independent AI/human review

**Commit reviewed:** `31240f1` ("close all open review calls") — the diff `6ba4e80..31240f1`.
**Date:** 2026-07-29. **Scope:** 21 thesis edits + 2 bibliography entries + 5 CLAUDE.md corrections.
**Compile status after all changes:** clean — 0 errors, 0 undefined citations, 131 pages total, core manuscript 106 pages.

## How to use this document

Each change below has: the **exact before/after text**, the **justification**, the **evidence** (with source), a **risk rating**, and what happens **if the change is wrong**. A reviewer should focus on the 🔴 and 🟠 items — the 🟢 items are mechanical.

**Risk key:**
🔴 = changes a *claim about the world* (literature/novelty/licensing). Verify the evidence.
🟠 = changes *how a contribution is framed*. Judgment call — reasonable people could differ.
🟢 = terminology/accuracy fix with no claim content.

**Reverting:** every change is a self-contained text substitution. `git diff 6ba4e80..31240f1 -- <file>` shows the exact hunks.

**Provenance note (important for the reviewer):** the *evidence* below was gathered by three independent Opus agents that read primary sources (arXiv PDFs, ACL Anthology pages, in-repo experiment artefacts). The *decisions* about what to change were mine. Where I overrode an agent's recommendation, it is stated explicitly.

---

# PART 1 — 🔴 Changes to claims about the literature (verify these first)

These five changes alter what the thesis asserts about prior work. Each was made because the previous wording was **falsifiable by an examiner with a search engine**. All primary sources were read this session.

## 1.1 The italic gap statement — "in any language" was an overclaim

**Location:** `Chapters/chapter2.tex` §2.5.2, closing paragraph.

**Before:**
> However, a critical gap remains: *LLM-based QE has not been evaluated for monolingual Arabic retrieval, and the interaction between the generated expansion and the retrieval paradigm to which it is submitted has been left largely **unexamined in any language***.

**After:**
> However, a critical gap remains: *LLM-based QE has not been evaluated for monolingual Arabic retrieval, and the question of which retriever within a heterogeneous sparse--dense hybrid should receive the **query** expansion has not been addressed **for any language***. The closest analogue is found in the document-expansion literature, where the same asymmetry has been observed---text appended to documents benefits sparse matching but degrades dense representations, motivating separation at the index level [Doc2Query++]---but the corresponding question for query expansion at retrieval time remains open.

**Justification:** the old claim is contradicted by **four sources, one of which is the thesis's own next paragraph**:
- Query2Doc (`papers/2023_Query2doc.md:13-21`) reports both sparse and dense results and prescribes a *different* query construction per paradigm.
- GRF was extended to dense and learned-sparse retrieval (`chapter2.tex:425`, already in the thesis).
- MuGI's adaptive repetition *is* an expansion/sparse-retriever interaction study (`chapter2.tex:438`).
- **Lei et al. list "the advantages of BM25 over dense retrieval with query expansion from LLMs" as their third stated contribution** (`papers/arxiv_downloads/2402.18031.md:147`, §4.2).
- The very next sentence in the thesis credits Macmillan-Scott with finding that meta-text pollutes sparse retrieval — itself an interaction result.

**Why the new wording survives:** the *placement* question (which retriever in a heterogeneous hybrid receives the expansion) has no counter-example. Exp4Fuse — the nearest neighbour — is sparse-only (verified: *"using **only a single sparse retriever**"*, arXiv:2506.04760 full text).

**If wrong:** the gap claim would need narrowing further, but the thesis's novelty claim (asymmetric placement) does not depend on the deleted clause.

**⚠️ Reviewer should check:** whether citing Doc2Query++ is desirable. See §1.2.

## 1.2 🔴 NEW CITATION — Doc2Query++ (this is the single most consequential addition)

**Location:** `chapter2.tex` §2.5.2 and Gap 4; new `References.bib` entry `kuo_2025_doc2query_pp`.

**What was added:** two sentences citing Doc2Query++ (arXiv:2510.09557, Oct 2025) as the document-expansion analogue of this thesis's finding.

**Justification:** Doc2Query++ establishes **the identical sparse-benefits/dense-degrades asymmetry** — its "Dual-Index Fusion" keeps expansions out of the dense index because *"appending expansions degrades dense retrieval effectiveness due to semantic noise… which weakens the original document embedding"*, then fuses a sparse expanded index with an unexpanded dense index. This is structurally the same insight as the thesis's headline finding, published one year earlier, in English, for documents.

**The decision:** the verifying agent rated this a **Medium-likelihood examiner attack** if left uncited, and recommended citing it. I agreed and applied it. The argument: an examiner who knows this paper and sees it uncited concludes either ignorance of the literature or concealment. Citing it and drawing the distinction (document expansion at *index* time vs. query expansion at *retrieval* time; dual-*index* vs. dual-*retriever* fusion) demonstrates command of the field and makes the novelty claim more precise, not weaker.

**⚠️ THIS IS THE CHANGE MOST WORTH A SECOND OPINION.** Arguments to reconsider:
- It introduces a paper the authors have not read in full (only the abstract and key passages were fetched).
- It slightly narrows the perceived novelty by naming a close relative.
- Counter-argument: the relative exists whether or not it is cited.

**To revert:** delete the two "The closest analogue…" / "The analogous asymmetry…" sentences and the bib entry. The surrounding claims remain valid (the "query expansion" / "for any language" narrowing in §1.1 is independent and should be kept regardless).

## 1.3 🔴 "The query formulation stage remains uninvestigated" — missing qualifier

**Location:** `chapter2.tex` §2.5.3, final sentence.

**Before:** "The query formulation stage---specifically, whether LLM-based QE techniques developed for English transfer effectively to Arabic---remains uninvestigated."

**After:** same, with ***LLM-based*** italicised, plus a new sentence: "Automatic query expansion for Arabic has itself been studied for two decades using thesaurus-, ontology- and word-embedding-based methods [survey], but these approaches predate generative expansion and address a different mechanism: the addition of related *terms* rather than the generation of a pseudo-document."

**Justification:** this was **the only sentence in the thesis stating the gap in a form one search can falsify**. Arabic AQE is an active field: a dedicated survey (Al-Shawakfa et al., JISTaP 8(4), 2020) and a paper published *during* this thesis (Al-Lahham et al., *Scientific Reports*, 22 Jan 2026). Neither is LLM-based, so the thesis's actual gap claim is untouched — but "uninvestigated" without the qualifier is indefensible.

**Evidence:** an unfiltered search (six queries, English + Arabic terms — توسيع الاستعلام, استرجاع المعلومات العربي — including 2026) found **no LLM-based monolingual Arabic QE work**. The gap survives in its LLM-specific form. Bonus evidence: the 2025 QE survey (arXiv:2509.07794) never mentions Arabic or MIRACL.

**⚠️ Reviewer note:** one new citation added (`alshawakfa_2020_survey_aqe`). Its **author list was not verified at page level** — confirm before submission, or drop the citation and keep only the qualifier (which is the load-bearing part).

## 1.4 🔴 CSQE described as "synthesise" — conceded the paper's central claim

**Location:** `chapter2.tex` §2.5.2, CSQE description.

**Before:** "instructing it to **extract and synthesise** topically relevant vocabulary and context grounded in the actual corpus content."

**After:** "instructing it to identify which of them are relevant and to ***extract verbatim*** the key sentences that establish that relevance. Because the extracted text is copied from the corpus rather than generated---Lei et al. report that **830 of 1,000** extracted sentences were identical to sentences in the retrieved documents---the corpus-grounded component is structurally incapable of hallucination."

**Justification:** Lei et al. are emphatic that the operation is extraction, *not* synthesis — that is their entire anti-hallucination argument (*"these key sentences are usually identical to the existing texts in the corpus"*, with the 830/1000 footnote). Saying "synthesise" gives away the mechanism that justifies corpus steering, which is this thesis's central technique.

**Effect:** strengthens the thesis. The 830/1,000 figure is verified in the in-repo paper copy.

## 1.5 🟠 Paragraph opener mischaracterised five cited papers

**Before:** "Several additional studies have examined QE **with smaller and more efficient models**."
**After:** "Several further studies have extended LLM-based QE along complementary axes."

**Justification:** of the five papers in that paragraph, **only AQE fits the "smaller/efficient" framing**. KAR augments an LLM with a knowledge graph; ThinkQE is a test-time reasoning framework benchmarked against *training-intensive* systems; PBR is personalisation. The five individual descriptions were each verified accurate — only the framing sentence was wrong.

**Also verified this round:** all five `.bib` entries (ThinkQE, KAR, AQE, PBR, Yoon) are correct — authors, venues, years — and all five one-sentence descriptions are accurate. No mis-citations found.

---

# PART 2 — 🟠 Framing decisions (judgment calls — reasonable people could differ)

## 2.1 🟠 §1.1 no longer pre-announces the asymmetric finding

**Before:** "…a pipeline that couples corpus-steered query expansion with **asymmetric** hybrid sparse--dense fusion, **in which the expansion is applied to the sparse retriever only**."
**After:** "…a pipeline that couples corpus-steered query expansion with hybrid sparse--dense fusion, **and determines empirically at which point in that pipeline the expansion should be applied**."

**Justification:** four of the thesis's own framing sites hold the placement question **open** — Objective 9 ("to determine the optimal placement… expanding the sparse retriever, the dense retriever, or both"), Ch.2 Gap 4 ("is therefore an open question"), Ch.2 Q7, and §3.8.3 ("was left as an empirical question"). Exactly one sentence — the problem statement — closed it. An examiner reading §1.1 → §1.2 meets the *answer* before the *question*, which reads as post-hoc objective-writing: the most common committee criticism of the Problem↔Objectives chain.

**Counter-argument (why you might revert):** Dr. Tahani explicitly sanctioned a technology-driven narrative, and task A1 asked for "our final pipeline as the answer". If you read A1 as requiring the *finding* (not just the artefact) in §1.1, revert this.

**My assessment:** naming the pipeline satisfies A1; naming the result is what creates the contradiction. The rephrase arguably reads stronger — "determines empirically" flags a contribution rather than an assumption.

## 2.2 🟠 The word "small" — decided NOT to reinstate in objectives; removed from Ch.3 instead

**Decision:** "small" stays out of all 9 objectives. Two self-descriptive uses in Ch.3 were removed instead:
- `chapter3.tex:186`: "**Small open-source models:**" → "**Openly available models of 2--8 billion parameters:**"
- `chapter3.tex:265`: "Ten **open-source** models" → "Ten **openly available** models"

**Justification:**
1. **No inconsistency is created by the absence** — Ch.5 ¶2 already carries the claim in evidence-backed form: "adapted for Arabic zero-shot application using models **as small as 3 billion parameters**", tied to the Qwen 2.5 3B result.
2. The number is uncontestable; the adjective is not. A committee member can dispute whether 8B is "small" in 2026, but not that it is 8 billion parameters.
3. Reinstating it in the objectives — the most load-bearing list in the thesis — would partially undo Phase A's entire purpose at the highest-visibility point.
4. All remaining "small" in Ch.2 refers to the *literature*, not this thesis's models, and was correctly kept.

**If you disagree:** the least damaging single site is **Objective 3** (the Query2Doc-transfer objective, where the 175B→3B contrast is the actual point), *not* Objective 4. Wording: "…for Arabic zero-shot application using small, openly available LLMs…"

## 2.3 🟠 Licence caveat split between Overall and Challenges

**Before (in the Overall paragraph):** "…Apache-2.0 alternatives such as Jais-2-8B **follow at a small cost in effectiveness**."

**After (Overall):** "…whereas Apache-2.0 alternatives are available, the strongest of which---Jais-2-8B---**was within 2.4 per cent of Aya Expanse in the model comparison**."

**Plus a new Challenges item 8** stating that CSQE and fusion were run with Aya alone, so the substitution cost "was not measured directly", **and a new Recommendation** to repeat the pipeline with an Apache-2.0 generator.

**Justification — this fixed a real overclaim.** The previous sentence was attached to the **0.7137 CSQE headline**, but:
- **No Jais-2 CSQE run exists** anywhere in the thesis or the experiment logs. The claim extrapolated blind-QE leaderboard numbers to a pipeline Jais-2 was never run through.
- It was **directionally wrong for one comparison**: Jais-2 (0.5122) actually *beats* Aya (0.5046) on BM25 at n=1 (`chapter4.tex:306-307`).

**Licence facts verified** against the Ch.2 model table: Aya Expanse 8B = **CC-BY-NC** (`chapter2.tex:406`, `:363`); Jais-2-8B = Apache 2.0 (gated access); gaps −2.4% dense, −2.1% sparse-with-repetition.

**Why split rather than move:** the caveat must stay in the Overall paragraph because that is where the vulnerable claim ("practical for deployments") lives — a caveat in a later section doesn't defend it. But the *evidential weakness* (untested substitution) belongs in Challenges, where items 4–6 already establish the "magnitude may differ under X" pattern.

**⚠️ Reviewer decision:** whether the Overall paragraph — the thesis's strongest rhetorical moment — should carry a licence caveat at all. Alternative: move it entirely to Challenges and let Overall end on the result.

---

# PART 3 — 🟢 Accuracy and consistency fixes (low risk)

## 3.1 🔴→🟢 Factually false claim removed from Ch.3 (rated 🔴 for importance, 🟢 for risk of the fix)

**Before:** "…zero-shot prompting was adopted **exclusively**. This decision was driven by resource constraints (**small open-source models have limited context windows for few-shot examples**)…"

**After:** "…pseudo-document generation was performed zero-shot. The demonstrations of the original method are English query--passage pairs, and no curated set of Arabic demonstrations was available; constructing one would have introduced a design variable absent from the original method, and it is therefore left as a direction for future work (§5.3). Zero-shot prompting also keeps every prompt short, which matters when generation is batched over 2,896 queries for each of ten models within the available GPU budget (§3.4.4), and it allows each model's Arabic expansion capability to be assessed without task-specific demonstrations."

**Justification — the old claim is false on the thesis's own evidence:**

| Model | Context window | Source |
|---|---|---|
| Falcon-H1-Arabic-3B | 128K tokens | `chapter2.tex:293` |
| Gemma 3 4B-IT | 128K tokens | `chapter2.tex:354` |
| SILMA Kashif-2B | 12K tokens (smallest anywhere) | `chapter2.tex:320` |

Four Query2Doc demonstrations are a few hundred tokens. Even the 12K floor leaves ~11.7K spare. **No model in Table 2.4 has a context window that constrains few-shot prompting.**

**Second defect fixed:** "adopted **exclusively**" was contradicted by the thesis's own CSQE prompt, which is **one-shot** (`chapter3.tex:452`). The claim is now scoped to "pseudo-document generation", and §3.8.1 explicitly notes the one-shot demonstration is "the sole exception to the zero-shot protocol".

**Note:** the replacement reasons are all honest and already present elsewhere in the thesis (the Arabic-demonstrations argument is Recommendation 4 in §5.3).

## 3.2 🟢 CSQE added to the Ch.2 technique taxonomy

**What:** a fourth `\item` after GRF in §2.1.4, plus the lead-in changed from "generate expansion content" → "generate **or select** expansion content".

**Justification:** CSQE — the thesis's central technique — was **absent from the taxonomy section whose stated job (per §1.3) is to introduce QE techniques**, appearing first only in Related Work. A reader meeting "CSQE" in Objective 8 and turning to the taxonomy found nothing.

**Content check:** the new item is *taxonomic only* (what class of thing CSQE is), deliberately not duplicating §2.5.2's mechanism/results description. It pays off the RM3 sentence already at `chapter2.tex:86`, which sets up first-pass expansion but never returns to it. Survives task C5's bold→numbered-subsection conversion unchanged (an `\item` inside an itemize is unaffected).

## 3.3 🟢 Terminology standardisation

| Change | Location | Reason |
|---|---|---|
| "without **query enhancement**" → "without **QE**" | Objective 7 | QE is defined at `chapter1.tex:9`; this was the last re-expansion in Ch.1–5 |
| "should receive **it**" → "should receive **the query expansion**" | `chapter1.tex:11` | Matches the §2.5.2 narrowing (1.1) |
| "asymmetric **assignment of expansion**" → "asymmetric **placement of query expansion**" | Ch.2 Gap 4 | "Placement" standardised as the reader-facing noun across all three lists |
| "blind **generation**" → "blind **expansion**" | Ch.2 Q6 | Five surface forms existed for one concept |
| "blind-**QE** baseline" → "blind-**expansion** baseline" | Ch.5 ¶11 | Same |
| "the **Dense** retriever's" → "the **dense** retriever's" | Ch.5 ¶10 | Capitals reserved for configuration labels ("Dense+CSQE") |
| "Jais-2 8B" → "Jais-2-8B" (2×) | Ch.5 ¶3, ¶6 | Matches the Ch.2 §2.4.1.2 heading and developer naming |
| criterion 3: "permissive licensing" → "a licence permitting research use, whether permissive or non-commercial" | `chapter3.tex:270` | Aya is CC-BY-NC; the old text was inaccurate |

---

# PART 4 — CLAUDE.md corrections (not thesis text; affects future AI sessions)

| # | Change | Why |
|---|---|---|
| 1 | Query-length buckets `<5 / ≥10 words` (n=865/n=131) → canonical **1–3 / 4–8 / 9+** with values 0.345/0.511/0.476 and gains +0.161/+0.197/+0.132 | The old buckets correspond to **no table in the thesis** — a dead bucketing that would propagate into future work |
| 2 | Exp 2.1 table gained the missing **RRF rows** (0.6474, 0.6936) | The old table listed Dense-expanded and Both-expanded only in **CC** form — anyone quoting it would reproduce the exact CC/RRF mixing defect just fixed in Ch.5 ¶10 |
| 3 | Added: **per-query mean is 0.6936, NOT 0.7137** (corpus-level pooled); per-query baseline = 0.5046 | A live trap — the two are routinely confused |
| 4 | Added SILMA warning: canon is **0.4277** (temp 0.1); 0.4194 is a temp-0.7 artefact | See Part 5 |
| 5 | "What's NOT Decided" block (embedding model, technique, LLM) → "Settled / Still open" | All were settled by experiment months ago; the stale block actively misleads |

---

# PART 5 — ⚠️ NOT changed: the SILMA data conflict (task H1 — needs your decision)

**Finding:** `chapter4.tex:311` (Table 4.7) says SILMA BM25 n=1 = **0.4277**; `chapter4.tex:462` (Table 4.11) says **0.4194**. Same configuration, two numbers.

**Root cause — proven, not inferred:** `arabic-rag-query-enhancement/experiments/phase4_quick_wins (1).ipynb` cell 7 maps `'SILMA 2B': 'silma_2b_temp07.pkl'`. **The repetition sweep loaded SILMA's temperature-0.7 expansions** while every other model, Ch.3 Table 3.2, and the dense results use temperature 0.1. Both pickles exist on disk. All four metrics differ (R@10 0.5550 vs 0.5447; MRR 0.4485 vs 0.4400) — not rounding.

**Canonical value: 0.4277** (Table 4.7 is correct; the sweep is the deviant artefact).

**Verified:** only SILMA is affected — the other models match to 4 d.p. across both tables (identical pickles reused).

**Options:**
- **A (recommended):** re-run SILMA's 8 repetition configs with `silma_2b_temp01.pkl` (~8 min, CPU-only, all inputs in-repo), update Tables 4.11/4.12, regenerate Figs 4.7/4.8.
- **B:** keep 0.4277, footnote Table 4.11. Table 4.12's Δ=+0.0639 remains correct as printed.
- **Rejected:** changing Table 4.7 to 0.4194 — would split SILMA's dense/sparse rows across two temperatures.

**Independent of the choice:** `thesis_figures/data/raw/model_comparison_bm25.csv:3` and `thesis_figures/output/pdf/table_4_3.tex:6` pair temp-0.1 n=1 metrics with the temp-0.7 best config (Δ=0.0555, matching neither table). **Figures 4.7 and 4.8 currently plot different SILMA values** because they read different CSVs. Both need regenerating from one source.

---

# PART 6 — What was verified and found CORRECT (no change needed)

Recorded so the reviewer knows these were checked, not overlooked:

| Claim | Verdict | Evidence |
|---|---|---|
| **Lei et al. never ran a corpus-only ablation** → exp 013c is first in any language | ✅ VERIFIED | Exhaustive read incl. all appendices. "BM25+KEQE" (blind-only) appears in Tables 3,4,6,7,10; **no corpus-only condition anywhere**. CSQE is defined as inseparable: "we expand the query by concatenating q, all sentences in S, **and the generations from KEQE**" |
| **Exp4Fuse is sparse-only** → placement gap holds | ✅ VERIFIED | *"using **only a single sparse retriever**"*; dense retrievers appear only as baselines, never fused |
| **Macmillan-Scott is cross-lingual only** | ✅ VERIFIED | Hit@10 heatmaps (Figs 3,4) have **blank diagonals** — no query-language = doc-language cell evaluated |
| **MuGI repetition is length-adaptive** | ✅ VERIFIED | λ = ⌊Σlen(rᵢ)/(len(q)·β)⌋ |
| **Ch.3's β matches MuGI's β semantics** | ✅ VERIFIED — was flagged Medium risk | Ch.3 `n = max(1,⌊\|d\|/(\|q\|·β)⌋)`; both use β as the **divisor**. No silent redefinition |
| **"30% MAP over BM25 at 7B"** | ✅ EXACT | 39.1 vs 30.1 = +29.9% |
| **All five previously unverified citations** (ThinkQE, KAR, AQE, PBR, Yoon) | ✅ VERIFIED | `.bib` entries and descriptions all correct |
| **No LLM-based monolingual Arabic QE exists** | ✅ VERIFIED (unfiltered search) | Six searches, English + Arabic terms, incl. 2026. All Arabic QE found is pre-LLM |

---

# PART 7 — Residual risks the reviewer should weigh

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| R1 | **Macmillan-Scott's paper contains the phrase "monolingual subsets for Arabic"** (§3.3). An examiner grepping the PDF may claim we mischaracterise it. | **Medium — highest single risk** | Rebuttal is solid and should be prepared: those subsets are *fine-tuning data*; the *retrieval evaluation* is cross-lingual without exception (blank diagonals). Consider a footnote showing this was considered. |
| R2 | Doc2Query++ citation is a judgment call (see 1.2) | Medium | Reviewer decides |
| R3 | "Has not been studied" is an unprovable universal | Low impact, unavoidable | Already narrowed by *monolingual*, *Arabic*, *heterogeneous hybrid*, *query* |
| R4 | `alshawakfa_2020_survey_aqe` author list not verified at page level | Low | Verify or drop the citation (keep the qualifier) |
| R5 | Yoon et al. cited as `@misc`/arXiv but published in ACL 2025 Findings | Low | Upgrade to `@inproceedings` |
| R6 | ThinkQE (same first author as CSQE) uses a "corpus-interaction strategy" — the most likely place a corpus-only ablation might exist | Low | One targeted read of ThinkQE's ablation section before submission |
| R7 | **WS6_RESEARCH_REPORT.md is wrong** — it says Macmillan-Scott evaluates MuGI/Exp4Fuse across 8 languages. It evaluates **four prompting strategies** (zero-shot/CoT/RaR/few-shot). | — | **Do not reuse that phrasing.** Not repeated in the thesis. |

---

# Appendix — full file inventory for this commit

| File | Changes |
|---|---|
| `Chapters/chapter1.tex` | 3 edits (§1.1 closing, l.11 "query expansion", Objective 7 "QE") |
| `Chapters/chapter2.tex` | 10 edits (6 literature claims, CSQE taxonomy item + lead-in, Q6 wording, criterion alignment) |
| `Chapters/chapter3.tex` | 4 edits (zero-shot justification, one-shot exception note, 2× de-"small") |
| `Chapters/chapter5.tex` | 6 edits (licence clause, +Challenges item 8, +Recommendation 9, 3× terminology) |
| `References.bib` | +2 entries (`kuo_2025_doc2query_pp`, `alshawakfa_2020_survey_aqe`) |
| `CLAUDE.md` | 5 corrections |
| `research_decisions/` | +3 reports (LITERATURE_VERIFICATION_FINAL, OPEN_CALLS_RESOLUTION, SILMA_CONFLICT_RESOLUTION), +task H1 |

**Chapter 4 was not modified in this round.**
