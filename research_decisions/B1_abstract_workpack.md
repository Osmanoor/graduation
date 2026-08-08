# B1 — English Abstract Work Pack

**Date:** 2026-08-01
**Purpose:** get a second independent draft (Gemini), compare with ours, merge into a final.
**Status:** nothing applied to `5-Abstract.tex` yet.

---

## 1. The rules (from Dr. Tahani, `TASKS.md` B1 + Q5)

| Rule | Value |
|---|---|
| Length | **250–350 words** (≈ 3/4 page) |
| Hard limit | never more than 1 page |
| Minimum | not less than half a page |
| Structure | Context/Area → Problem → Objectives → Methodology → Key Findings → Overall Conclusion |
| Format | Times New Roman 12, 1.5 spacing (already the template default) |

---

## 2. Prompt to paste into Gemini

Attach these files: `Chapters/chapter1.tex`, `Chapters/chapter3.tex`,
`Chapters/chapter4.tex`, `Chapters/chapter5.tex`.

> You are helping write the English abstract for a bachelor's thesis in Electrical
> and Electronic Engineering (University of Khartoum). The thesis is about Arabic
> information retrieval.
>
> I am attaching four chapters of the thesis. Write the abstract **only** from what
> is in them. Do not add any claim, number, or citation that is not in the attached
> text. If something you would normally include is missing, leave it out.
>
> **Required structure**, in this order, as flowing paragraphs (not headings, not bullets):
> 1. Context / research area
> 2. Problem
> 3. Objectives
> 4. Methodology
> 5. Key findings
> 6. Overall conclusion
>
> **Hard requirements**
> - **250–350 words. This is a strict limit — count them.**
> - British spelling: normalised, standardised, analyse, characterise.
> - The abstract is read on its own, so every abbreviation must be written in full
>   the first time it appears, e.g. "Retrieval-Augmented Generation (RAG)". After
>   that use the abbreviation only. Do this for RAG, LLM, QE, MIRACL, mDPR, BM25,
>   NDCG and CSQE.
> - Formal academic register, passive voice, past tense for what was done.
> - LaTeX conventions: `---` for an em dash, `\%` for percent, `--` for a number range.
> - No headings, no bullet points, no citations, no figures or tables.
>
> **The central research question is, verbatim:**
> "To what extent can LLM-based query enhancement---blind and corpus-steered---improve
> Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms?"
> The abstract must reflect this question and not a different one.
>
> **Things that must appear:**
> - The final result: 0.7137 NDCG@10, which is +54.5\% over the BM25 baseline and
>   +13.9\% over the best hybrid system without query enhancement.
> - CSQE (Corpus-Steered Query Expansion), named and explained in a few words.
> - The main finding: the expansion helps most when applied to the sparse retriever
>   **only**, not to both retrievers.
>
> **Things that must NOT appear:**
> - Any framing that the thesis is about "small open-source models" or about
>   "identifying which model characteristics determine effectiveness". That framing
>   was deliberately removed from the thesis.
> - Any claim that model size predicts performance. Chapter 5 states this only with
>   heavy qualification.
>
> Return only the abstract, then a word count on a separate line.

---

## 3. Fact-check list — apply to ANY draft, ours or Gemini's

These are the traps. Check every returned draft against this list before using it.

| # | Trap | Correct |
|---|---|---|
| T1 | **0.7137 vs 0.6936** | 0.7137 is the corpus-level pooled score. 0.6936 is a *different system* (both-expanded, RRF). There is also a per-query **mean** of 0.6936 for the best system — coincidentally the same number. Never present a per-query mean as the headline. |
| T2 | **Mixed fusion methods** | The placement comparison must use RRF for all three: 0.7137 (sparse-only) / 0.6936 (both) / 0.6474 (dense-only). Do not mix in the CC numbers (0.7088, 0.6959, 0.6588). |
| T3 | **Baseline for the +54.5\%** | BM25 alone = 0.4621. Not 0.5046 (that is the Aya blind BM25 n=1 baseline, used only for the per-query analysis). |
| T4 | **Baseline for the +13.9\%** | Hybrid RRF k=20 without QE = 0.6267. |
| T5 | **"nine models" vs "ten"** | Ten were evaluated, one (ALLaM-7B) was dropped. Say "ten evaluated" or "all nine viable models", never "nine evaluated". |
| T6 | **Query-length buckets** | If mentioned at all, the buckets are 1--3 / 4--8 / 9+ words. Never "<5 / >=10". |
| T7 | **Model-size claim** | Chapter 5 says parameter count is *confounded* with architecture and training data, and that the clean evidence is only within the Qwen family. Do not state a general correlation. |
| T8 | **Spelling** | British throughout: normalised, standardised, analyse. |
| T9 | **Acronyms** | Each expanded exactly once, on first use. |
| T10 | **Word count** | 250--350. Count it, do not estimate. |

**Verified numbers** (source in brackets):

- 2,896 queries, 2,061,414 passages → "2.06 million" [`chapter3.tex:17`]
- BM25S baseline 0.4621 NDCG@10 [CLAUDE.md]
- mDPR baseline 0.4993 NDCG@10 [CLAUDE.md]
- 34\% query failure rate [`chapter5.tex:14`]
- Dense gains +3.7\% to +23.5\% across nine models [`chapter5.tex:18`]
- BM25 degraded for 6 of 9 models [`chapter5.tex:22`]
- Hybrid RRF without QE 0.6267 [CLAUDE.md Exp 1.2]
- CSQE on BM25 alone 0.6157 [CLAUDE.md Exp 013]
- CSQE + hybrid, sparse-only 0.7137 / both 0.6936 / dense-only 0.6474, all RRF [CLAUDE.md Exp 2.1]
- 0.7137 / 0.4621 = 1.5445 → +54.5\% ✅ recomputed
- 0.7137 / 0.6267 = 1.1388 → +13.9\% ✅ recomputed

---

## 4. Our draft — 350 words

```
Retrieval-Augmented Generation (RAG) systems depend on effective retrieval to ground Large Language Model (LLM) outputs in external knowledge, yet Arabic information retrieval fails on many queries because of morphological richness, orthographic variation, and vocabulary mismatch between short queries and documents. Query enhancement (QE)---the modification of a query before retrieval---offers a modular remedy, but its established techniques were developed for English using proprietary models of 175 billion or more parameters, and neither their transfer to Arabic nor their placement within a hybrid architecture has been established. This thesis investigates the extent to which LLM-based QE---generated blindly or steered by the target corpus---can improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms, using only openly available models of 2--8 billion parameters.

Experiments used the Arabic subset of the Multilingual Information Retrieval Across a Continuum of Languages (MIRACL) benchmark, comprising 2,896 queries over 2.06 million passages, with the Multilingual Dense Passage Retriever (mDPR) and BM25S, an implementation of Best Matching 25 (BM25), as the dense and sparse baselines. An error analysis identifying a 34\% query failure rate, concentrated in very short queries, motivated adapting Query2Doc for Arabic. Ten openly available LLMs were compared as expansion generators, followed by query repetition, hybrid sparse--dense fusion, and Corpus-Steered Query Expansion (CSQE).

QE improved dense retrieval for all nine viable models, with Normalised Discounted Cumulative Gain at rank 10 (NDCG@10) gains between +3.7\% and +23.5\%, but degraded sparse retrieval for six of the nine by diluting the original query terms---a degradation fully removed by query repetition. Hybrid fusion without QE reached 0.6267 NDCG@10. CSQE reached 0.6157 on BM25 alone, and its placement within the hybrid pipeline proved decisive: applied to the sparse retriever alone it achieved 0.7137 NDCG@10, against 0.6936 when both retrievers received the expansion and 0.6474 when only the dense retriever did.

The final system therefore exceeded the BM25 baseline by 54.5\% and the strongest unenhanced hybrid baseline by 13.9\%, using an openly available 8-billion-parameter generator and without proprietary APIs. LLM-based QE is effective across all three retrieval paradigms, provided that both the expansion's form and its placement are adapted to the retriever.
```

**What was cut from the old abstract to fit 350 words:**

| Cut | Words saved | Can go back? |
|---|---|---|
| Aya Expanse and Jais-2 named as best models | ~35 | Yes, if something else goes |
| "3B model beat GPT-3 175B" | ~30 | Yes, if something else goes |
| "model size correlates with improvement; training data matters more than Arabic benchmarks" | ~35 | **No** — Chapter 5 now states this with heavy qualification, so keeping it would contradict the thesis |

---

## 5. Where our draft is weakest

Honest assessment, so the comparison is fair:

1. **No named models.** Objective 4 is about identifying the best generator per paradigm.
   The abstract now says "ten were compared" but never says who won. A reader finishes the
   abstract not knowing Aya Expanse 8B is the answer.
2. **Objectives are compressed into the research question.** Six of the nine objectives are
   not visible. This is normal for an abstract, but Dr. Tahani asked for an explicit
   Objectives element in the structure.
3. **The error analysis is one clause.** Objectives 2 and 9 (error analysis, per-query
   analysis) are barely represented.
4. **`chapter4.tex` was not read in full** when drafting. Numbers came from `CLAUDE.md` and
   Chapter 5. A finding unique to Chapter 4 could be missing.

These are the four things the Gemini draft should be checked against — if it covers any of
them within 350 words, take that part.

---

## 6. Merge procedure

1. Run the §2 prompt in Gemini with the four chapters attached.
2. Paste its output into §7 below.
3. Run **both** drafts through the §3 fact-check list. Reject any sentence that fails.
4. Build the final from whichever draft handles each of the six structural elements best.
5. Recount words. Must land 250--350.
6. Apply to `5-Abstract.tex`, rebuild, confirm it fits under one page.

---

## 7. Gemini draft

**Model:** `gemini-3.1-pro-preview`, temperature 0.4.
**Input:** the §2 prompt + full text of `chapter1.tex`, `chapter3.tex`, `chapter4.tex`,
`chapter5.tex` (41,567 prompt tokens).
**Output:** 348 words.

```
Retrieval-Augmented Generation (RAG) relies on accurate retrieval to ground Large Language Model (LLM) outputs. However, Arabic retrieval faces severe vocabulary mismatch and orthographic variation. Query enhancement (QE) offers a pre-retrieval intervention to bridge this gap, yet research remains predominantly English-centric.

Arabic RAG systems frequently fail on short, information-poor queries. It remains unknown how expansions interact with different retrieval paradigms, and whether grounding them in retrieved evidence outperforms blind generation. Consequently, the central research question is: To what extent can LLM-based query enhancement---blind and corpus-steered---improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms?

The research aimed to establish baselines on the Arabic subset of the Multilingual Information Retrieval Across a Continuum of Languages (MIRACL) benchmark, adapt generative QE techniques, and evaluate their impact. It also sought to determine the optimal placement of expansions within a hybrid sparse--dense architecture.

A systematic evaluation was conducted using Multilingual Dense Passage Retriever (mDPR) and Best Matching 25 (BM25) baselines. Blind QE was implemented by generating pseudo-documents to expand queries. Subsequently, Corpus-Steered Query Expansion (CSQE)---a technique grounding LLM-generated expansions in first-pass retrieved documents---was adapted for Arabic. Expansions were evaluated independently on sparse and dense retrievers, followed by an investigation into hybrid fusion. Normalised Discounted Cumulative Gain (NDCG) served as the primary evaluation metric.

Experiments revealed that dense and sparse retrievers responded differently to QE. While blind expansion improved dense retrieval, it initially degraded BM25 performance due to term dilution, which was resolved through query repetition. Implementing CSQE demonstrated that corpus-grounded and blind expansions were complementary. Crucially, the main finding established that the expansion helped most when applied to the sparse retriever only, not to both retrievers. This asymmetric application preserved the independent semantic signal of the dense retriever, maximising list divergence for hybrid fusion. The final system achieved 0.7137 NDCG@10, an improvement of +54.5\% over the BM25 baseline and +13.9\% over the best hybrid system without query enhancement.

It was concluded that LLM-based QE substantially improves Arabic information retrieval when tailored to the retrieval paradigm. Asymmetric application of CSQE within a hybrid pipeline provides an effective architecture for mitigating Arabic vocabulary mismatch.
```

---

## 8. Comparison

### 8.1 Fact-check (§3 list) — both drafts

| Trap | Ours | Gemini |
|---|---|---|
| T1 — 0.7137 vs 0.6936 confusion | ✅ pass | ✅ pass (does not mention 0.6936) |
| T2 — mixed fusion methods | ✅ pass (all three RRF) | ✅ pass (gives no comparison) |
| T3 — baseline for +54.5\% | ✅ BM25 | ✅ BM25 |
| T4 — baseline for +13.9\% | ✅ hybrid without QE | ✅ hybrid without QE |
| T5 — nine vs ten models | ✅ "Ten … all nine viable" | ⚠️ never states how many |
| T6 — query-length buckets | ✅ not mentioned | ✅ not mentioned |
| T7 — model-size claim | ✅ absent | ✅ absent |
| T8 — British spelling | ✅ | ✅ |
| T9 — acronyms expanded once | ✅ | ⚠️ expands NDCG, then uses NDCG@10 without introducing `@10` |
| T10 — 250--350 words | ✅ 350 | ✅ 348 |

**Neither draft contains a factual error.** Both are safe to use.

### 8.2 Where each one wins

| | Ours | Gemini |
|---|---|---|
| Words | 350 | 348 |
| Paragraphs | 4 | **6** — more vertical space for the same word count |
| Numbers reported | **10** | 3 |
| Explains what CSQE *is* | ❌ names it only | ✅ "grounding LLM-generated expansions in first-pass retrieved documents" |
| Explicit Objectives element | ❌ folded into the RQ | ✅ own paragraph |
| RQ stated verbatim | ✅ (paraphrased into the sentence) | ✅ quoted as a question |
| Evidence for the main finding | ✅ 0.7137 / 0.6936 / 0.6474 | ❌ asserted, not shown |
| Explains *why* sparse-only wins | ❌ | ✅ "preserved the independent semantic signal of the dense retriever" |
| Dataset size stated | ✅ 2,896 queries / 2.06 M passages | ❌ |
| Model comparison visible (Obj. 4) | ✅ ten compared, Arabic vs multilingual finding | ❌ invisible |
| "openly available, no proprietary APIs" | ✅ | ❌ |

### 8.3 Verdict

**Ours is the better base.** It carries the evidence; Gemini's asserts conclusions an examiner
cannot check. But Gemini beats us on three specific things that are worth importing:

1. **It explains what CSQE is.** Ours names CSQE and never says what it does. That is a real
   defect in an abstract read on its own — fix regardless of which draft wins.
2. **It explains *why* sparse-only placement wins.** Ours gives three numbers and no mechanism.
   The mechanism is the contribution; the numbers are the proof.
3. **It has an explicit Objectives paragraph.** Dr. Tahani named Objectives as one of the six
   required elements. Ours folds them into the research question, which is defensible but
   less obviously compliant.

**Caution on paragraph count:** Gemini used 6 paragraphs for the same word count. Each break
costs 12 pt of `\parskip`. Six paragraphs may push the abstract past 3/4 page even at 348 words.
Prefer 4, at most 5.

---

## 9. Final abstract — APPLIED to `5-Abstract.tex` 2026-08-01

**350 words** by plain word count; 355 if em dashes are counted as word separators.
Five paragraphs. All six required structural elements present.

Built as: our draft as the base (it carries the evidence), plus the three things
Gemini did better — the CSQE gloss, the mechanism behind the placement finding, and an
explicit Objectives sentence.

**Element map:**

| Element | Where |
|---|---|
| Context / area | ¶1 sentence 1 |
| Problem | ¶1 sentence 2 |
| Objectives | ¶2 (research question + four objectives) |
| Methodology | ¶3 |
| Key findings | ¶4 |
| Overall conclusion | ¶5 |

**Trade-off made to stay under the limit:** two things were dropped from the 350-word
version that preceded this one —
- the dense-gain figure ("+12.3\% average"), the least load-bearing number present;
- the Arabic-specialised vs. multilingual finding (`chapter4.tex:389`).

Both were cut to buy room for the explicit Objectives sentence, which is a supervisor
requirement and therefore outranks them. Either can be restored if something else goes.

**Fact-check:** passes all ten traps in §3. Every number verified — see §3's verified list.

```
Retrieval-Augmented Generation (RAG) grounds Large Language Model (LLM) outputs in external knowledge, but Arabic information retrieval fails on many queries because of morphological richness, orthographic variation, and vocabulary mismatch. Query enhancement (QE)---modifying a query before retrieval---offers a modular remedy, but its established techniques were developed for English with proprietary 175-billion-parameter models, and neither their transfer to Arabic nor their placement within a hybrid architecture has been established.

This thesis therefore asks to what extent LLM-based QE---generated blindly or steered by the target corpus---can improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms, using only openly available models of 2--8 billion parameters. Its objectives were to establish sparse and dense baselines, adapt generative QE for Arabic, compare candidate generators, and locate the expansion within a hybrid pipeline.

Experiments used the Arabic subset of the Multilingual Information Retrieval Across a Continuum of Languages (MIRACL) benchmark (2,896 queries, 2.06 million passages), with the Multilingual Dense Passage Retriever (mDPR) and BM25S, an implementation of Best Matching 25 (BM25), as baselines. An error analysis identifying a 34\% query failure rate motivated adapting Query2Doc for Arabic. Ten openly available LLMs were compared as generators, followed by query repetition, hybrid fusion, and Corpus-Steered Query Expansion (CSQE), which grounds the expansion in first-pass retrieved documents rather than model knowledge.

QE improved dense retrieval for all nine viable models but degraded sparse retrieval for six of them through term dilution, an effect fully removed by query repetition. Hybrid fusion without QE reached 0.6267 in Normalised Discounted Cumulative Gain at rank 10 (NDCG@10). Expansion placement then proved decisive: applying CSQE to the sparse retriever alone achieved 0.7137 NDCG@10, against 0.6936 when both retrievers received it and 0.6474 when only the dense retriever did, because withholding it from the dense retriever preserved the complementarity on which fusion depends.

The final system exceeded the BM25 baseline by 54.5\% and the best unenhanced hybrid by 13.9\%, using an openly available 8-billion-parameter generator without proprietary APIs. LLM-based QE is therefore effective across all three retrieval paradigms, provided that both the form of the expansion and its placement are adapted to the retriever.
```

**Still to verify:** rebuild the PDF and confirm the abstract occupies about 3/4 page and
does not spill past one page. Five paragraphs cost four `\parskip` breaks; if it runs long,
merge ¶1 and ¶2.

**Feeds B2:** Osman's Arabic abstract must be re-derived from this text, not from the old one.

---

## 10. SUPERSEDED 2026-08-08 by task B2

The §9 text above is **no longer what is in `5-Abstract.tex`.** It was factually clean but Elhaj
and Osman both found it hard to read: too many numbers, and CSQE explained in a way that taught a
non-specialist nothing. B2 revised it for readability only — no fact changed, and it still passes
all ten traps in §3.

| | §9 version | Current (B2) |
|---|---|---|
| Words | 315 (one paragraph, after the 5-paragraph version was merged) | **327** |
| Numbers | 15 | **9** |
| Headline | 0.7137 + two percentages, no starting point | **0.4621 → 0.7137 = +54.5%**, one sentence |
| Placement evidence | 0.6267 / 0.6936 / 0.6474 as decimals | same comparison, expressed in words |
| CSQE | "grounds the expansion in first-pass retrieved documents" | "first retrieves a few documents from the collection and builds the expansion from the wording found in them, not from the model's own memory" |
| Model counts | "all nine viable models … six of them" | "Ten … of which nine proved viable" |

**Dropped:** 175-billion, 2–8 billion, the three placement decimals, 0.6267.
**Added:** 0.4621, the missing "before" number.

Second opinions were re-run for this revision (Gemini 3.1 Pro, 319 words; GPT-5.5, 322 words),
each given the same brief without seeing the others. All three passed the §3 fact-check. **All
three independently wrote the CSQE gloss the same way** — retrieve real passages first, build the
expansion from their wording — which is the main evidence that the new phrasing is right. Gemini's
draft was not used as the base because it kept 175-billion and 2–8 billion, failing the very
complaint that prompted the revision; both external drafts also dropped the placement evidence and
the +13.9% comparison, which were kept deliberately.

**One-page fit re-verified** by building the real front matter, not by word count: `1-main.pdf`
p5, one page, followed by المستخلص on p6.
