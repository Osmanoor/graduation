# Handoff — B2: revise the English abstract, then write the Arabic one

**For:** a dedicated parallel Claude chat.
**Owner:** Elhaj · **Created:** 2026-08-06
**Scope:** TWO tasks, in this order. The English revision comes first and gates the translation.

---

## 1. The prompt (paste this into the new chat)

> I'm Mohammed (Elhaj), finishing my B.Sc. thesis at the University of Khartoum with Osman.
> This chat has two jobs, in order.
>
> **Job 1 — revise the English abstract.** It is factually correct but Osman and I both found it
> hard to read. Two specific complaints: it is stuffed with numbers, and the CSQE part is
> explained in a complicated way. I want fewer, clearer numbers — an obvious "before → after"
> with the impact — and CSQE explained so a non-specialist understands what it does.
>
> **Job 2 — write the Arabic abstract (المستخلص)** from the revised English one.
>
> Read these first, in order:
> 1. `research_decisions/handoffs/B2_ABSTRACT_HANDOFF.md` — this file, the full brief
> 2. `University_of_Khartoum__EEE_bachelor_s_thesis_template/5-Abstract.tex` — the current English abstract
> 3. `research_decisions/B1_abstract_workpack.md` — how it was built, and a 10-item fact-check list
> 4. `University_of_Khartoum__EEE_bachelor_s_thesis_template/6-ARAbstract.tex` — the current Arabic one, to be replaced
> 5. `CLAUDE.md` — project facts and canonical numbers
>
> **Do not change any number without checking it against §5 of the handoff.** Every figure in
> the abstract has a verified source. If you want to drop a number, drop it — but never restate
> one from memory.
>
> Show me the revised English abstract before you start the Arabic. I want to approve it first.
>
> **Working rules:** answer first, then explain. Keep replies short and in plain English — I'm a
> native Arabic speaker and long dense replies make the work harder. Ask me ONE question at a
> time. Show me the diff before applying any `.tex` edit.

---

## 2. Job 1 — revise the English abstract

### The current text — 315 words, one paragraph, `5-Abstract.tex`

It was rewritten on 2026-08-01 (task B1) and is **factually clean** — it passes all ten traps in
`B1_abstract_workpack.md` §3. This revision is about **readability, not correctness.**

### The two complaints, stated precisely

**(a) Too many numbers.** The abstract currently carries eleven: 175 billion, 2–8 billion,
2,896, 2.06 million, 34%, nine models, six models, 0.6267, 0.7137, 0.6936, 0.6474, 54.5%, 13.9%,
8 billion. A reader cannot hold that many. **What Elhaj wants instead: a clear old number, a
clear new number, and the impact.** The core story is:

> BM25 alone **0.4621** → final system **0.7137** = **+54.5%**

Everything else is supporting detail and most of it can go. The three placement numbers
(0.7137 / 0.6936 / 0.6474) are the evidence for the main finding — consider keeping the
comparison but expressing it in words rather than three decimals.

**(b) CSQE is explained in a complicated way.** Current text:

> *"Corpus-Steered Query Expansion (CSQE), which grounds the expansion in first-pass retrieved documents"*

That is accurate but abstract. A reader who does not already know the technique learns nothing.
**Iterate on this specifically.** The idea in plain terms: instead of asking the model to invent
an answer from memory, you first retrieve a few real documents from the corpus and let the model
build the expansion out of the words that actually appear in them. Find a phrasing that conveys
that in one clause without jargon.

### Hard constraints — do not break these

| Rule | Value | Source |
|---|---|---|
| Length | **250–350 words** | Dr. Tahani + faculty guidelines |
| Must fit | **one page**, never spill to a second | Dr. Tahani (firmest of her rules) |
| Minimum | not shorter than half a page | Dr. Tahani |
| Form | **ONE paragraph** — no multiple paragraphs | faculty guidelines, verbatim |
| Structure | Context → Problem → Objectives → Methodology → Key Findings → Conclusion, all six present | Dr. Tahani |
| Spelling | British — normalised, standardised, analyse | thesis convention |
| Acronyms | expanded exactly once, on first use, since the abstract is read standalone | task C3 |
| No | reference numbers, bullets, headings | faculty guidelines |

⚠️ **Verify the one-page fit by building**, not by word count. The current 315 words fill the
page almost exactly. If the revision runs longer it will spill, which breaks her firmest rule.

⚠️ **Acronyms currently expanded in the abstract:** RAG, LLM, QE, MIRACL, mDPR, BM25, NDCG, CSQE.
If you remove a term entirely that is fine. If you keep it, it must carry its expansion.

### Get a second opinion — two ways, both cheap

**Gemini** (`gemini-3.1-pro-preview`). A working script already exists at
`C:\Users\moham\AppData\Local\Temp\claude\...\scratchpad\gemini_abstract.py` — if it is gone,
it is a ~40-line `urllib` POST to
`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent`.
Set `maxOutputTokens` to **32768** — the model spends ~20k tokens thinking and truncates at 8192.

⚠️ **Key handling:** Elhaj will supply the API key. Pass it via an environment variable. **Never
write it into a file in the repo and never commit it.** The previous key was blocked by Google
for being leaked, so treat this seriously.

**ChatGPT** — give Elhaj a ready prompt to paste. It should include the same constraints as §2
above, the verified numbers from §5, and an instruction to return only the abstract plus a word
count.

Then compare all three drafts against `B1_abstract_workpack.md` §3's fact-check list before
merging. That is how the current version was built, and it caught real errors.

---

## 3. Job 2 — the Arabic abstract (المستخلص)

Start only after Elhaj approves the revised English.

### Current state
`6-ARAbstract.tex` — **~1.5 pages, derived from the OLD pre-B1 English abstract.** It carries the
framing Phase A removed. It must be **re-derived from the new English text**, not patched.

### Rules — Dr. Tahani, Report §9 and video 2 (08:08–09:20)

| Rule | Detail |
|---|---|
| Length | **≈ ¾ page**, same as the English |
| Arabisation | **Full Arabisation of technical terms where a standard Arabic equivalent exists** — e.g. الاسترجاع الكثيف (dense retrieval), التوليد المعزز بالاسترجاع (RAG) |
| First mention | Arabic term **first**, English acronym in parentheses after it |
| Numerals | **ASCII/Western digits** (0, 1, 2 …) throughout, matching the English side |
| Form | one paragraph, to match the English |

### What "a very accurate translation, not just a translation" means here

Elhaj's instruction: work hard on accuracy, not literal rendering. Specifically:

- **Do not transliterate what has a real Arabic term.** Use the established terminology.
- **Web search is allowed and encouraged** to confirm the standard Arabic rendering of technical
  terms — check how Arabic IR/NLP papers actually write them, not just a dictionary.
- Run the Gemini and ChatGPT drafts for Arabic too, then reconcile. Terminology is exactly the
  place where a second opinion catches a bad choice.
- ⚠️ **Both Elhaj and Osman must review the terminology** before it is final. Flag every term
  where you had to make a judgement call, in a short list at the end — do not bury the choices.

### Technical notes for the `.tex`

- The template uses `polyglossia` with `\setotherlanguage{arabic}` and Arial as the Arabic font
  (`1-main.tex:14-17`).
- `\<text>` is mapped to `\textarabic{text}` (`1-main.tex:99`).
- ⚠️ `6-ARAbstract.tex` was **deliberately excluded** from the C3 acronym sweep, so it has no
  first-mention obligations inherited from the English side — set them fresh.
- ⚠️ `\chapter*` sets no running head. If the Arabic abstract runs to two pages, its second page
  will have a blank header. Keeping it to ¾ page avoids the problem entirely.

---

## 4. Order of work

1. Revise the English abstract. Get Gemini + ChatGPT drafts. Fact-check all three.
2. **Show Elhaj the revised English. Wait for approval.**
3. Build and confirm it still fits one page.
4. Write the Arabic from the approved English. Get second opinions on terminology.
5. Build and confirm ≈¾ page.
6. Give Elhaj and Osman the list of terminology judgement calls to review.
7. Mark B2 done in `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`.

---

## 5. Verified numbers — the only source of truth

Do not restate any of these from memory. Sources in brackets.

| Figure | Value | Source |
|---|---|---|
| MIRACL Arabic dev set | 2,896 queries | `chapter3.tex:17` |
| Corpus | 2,061,414 passages → "2.06 million" | `chapter3.tex:17` |
| **BM25S baseline** | **0.4621** NDCG@10 | CLAUDE.md |
| mDPR baseline | 0.4993 NDCG@10 | CLAUDE.md |
| Baseline query failure rate | 34% | `chapter5.tex:14` |
| Dense gains across 9 models | +3.7% to +23.5% (avg +12.3%) | `chapter5.tex:18`, `chapter4.tex:410` |
| Models degrading BM25 | 6 of 9 | `chapter5.tex:22` |
| Hybrid RRF, no QE | 0.6267 | CLAUDE.md Exp 1.2 |
| CSQE on BM25 alone | 0.6157 | CLAUDE.md Exp 013 |
| **Final system (sparse-only CSQE + hybrid RRF)** | **0.7137** | CLAUDE.md Exp 2.1 |
| Both retrievers expanded | 0.6936 | same, RRF column |
| Dense-only expanded | 0.6474 | same, RRF column |
| Improvement over BM25 | **+54.5%** | 0.7137 / 0.4621 = 1.5445 ✅ |
| Improvement over hybrid | **+13.9%** | 0.7137 / 0.6267 = 1.1388 ✅ |
| Models evaluated | **ten**, of which **nine viable** (ALLaM-7B dropped) | `chapter5.tex:18` |
| Generator | Aya Expanse 8B, openly available, 8B params | `chapter5.tex:36` |

### Traps — full list in `B1_abstract_workpack.md` §3

- **0.6936 appears twice for different things.** It is the both-expanded RRF result, *and*
  coincidentally the per-query mean of the best system. Never present a per-query mean as the
  headline — the headline 0.7137 is corpus-level pooled.
- **All three placement numbers must be RRF** (0.7137 / 0.6936 / 0.6474). Do not mix in the CC
  numbers (0.7088 / 0.6959 / 0.6588) — that is a like-for-unlike comparison.
- **+54.5% is against 0.4621**, not 0.5046. The latter is the blind-QE baseline used only in the
  per-query analysis.
- **Never say "nine models were evaluated"** — ten were, nine were viable.
- **Do not claim model size predicts performance.** `chapter5.tex:20` states this only with
  heavy qualification; a flat claim would contradict the thesis.
