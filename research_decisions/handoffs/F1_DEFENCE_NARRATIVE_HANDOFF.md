# Handoff — F1: explaining the project simply, and the defence narrative

**For:** a dedicated parallel Claude chat.
**Owner:** JOINT (Elhaj + Osman) · **Created:** 2026-08-06
**Why it matters:** this is the only task the jury actually experiences. Everything else is a
document they skim; this is the hour they judge.

---

## 1. The prompt (paste this into the new chat)

> I'm Mohammed (Elhaj). Osman and I are defending our B.Sc. thesis at the University of Khartoum.
> This chat has one job: **make our project explainable to a jury that knows nothing about
> information retrieval.**
>
> We have a real problem. When we explain the project, it does not land. It sounds like
> "half a RAG system" and people do not see why it matters. I want to fix that before we build
> a single slide.
>
> Read these first, in order:
> 1. `research_decisions/handoffs/F1_DEFENCE_NARRATIVE_HANDOFF.md` — this file, the full brief
> 2. `University_of_Khartoum__EEE_bachelor_s_thesis_template/5-Abstract.tex` — what the thesis claims
> 3. `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter1.tex` §1.1–1.2 — the problem statement
> 4. `CLAUDE.md` — verified facts and canonical numbers
>
> **Start with one thing only: the CSQE example.** Section 5 of the handoff has three real
> queries from our results. Make one of them into an explanation a non-specialist follows
> completely and finds convincing. Do not move on to slides or structure until that single
> example works.
>
> **Working rules:** answer first, then explain. Short replies, plain English — I'm a native
> Arabic speaker and long dense replies make this harder, not easier. Ask me ONE question at a
> time and wait. If something I say is unclear, that's your problem to fix, not mine.

---

## 2. The jury — the single most important constraint

**General Electrical and Electronic Engineering staff.** Confirmed by Elhaj, 2026-08-06:

- They know **signals and control**. Assume that fluently.
- They may have **some software / AI background**, but **assume very low knowledge of this
  domain** — retrieval, search, embeddings, RAG.
- They are **Arabic speakers**. Arabic examples will land instantly. Use that.

**What this rules out.** Do not open with RAG, embeddings, vector spaces, BM25, or "retrieval
augmented generation". Every one of those needs its own explanation first, and you do not have
the budget. If a sentence requires a prior definition, it is too early in the narrative.

**What this opens up.** Signals and control people have strong intuitions about **matched
filters, noise, signal-to-noise ratio, and feedback loops.** Two of those map onto this project
almost exactly — see §7. Test whether that framing helps or whether it is a distraction.

---

## 3. The actual problem to solve

From the meeting record (video 2, 18:45–21:00): *we still struggle to explain the project
simply — it reads as "half a RAG" (retrieval-only).*

Two distinct failures, and they need different fixes:

**(a) "Where is the generation?"** The jury hears "RAG" and expects a chatbot. We only improved
retrieval. The honest answer is strong but has to be *prepared*: a RAG system's final answer is
bounded by what it retrieves — if the right passage never comes back, no amount of language
model quality recovers it. We attacked the bottleneck, not the visible part. **This answer must
be one sentence, ready, not improvised.**

**(b) "Why is this hard? It's just search."** Arabic search failing is not obvious to someone
who has never thought about it. It needs a concrete demonstration, not an assertion.

---

## 4. What has to be explained, in order

The chat should build these **in sequence**, and each one must land before the next:

| # | Idea | Status |
|---|---|---|
| 1 | Why Arabic retrieval fails — concretely, not as a claim | needs building |
| 2 | Why a short query is the root cause | needs building |
| 3 | The blind-expansion idea (Query2Doc / HyDE) | **already lands well** — Elhaj reports this one works when explained |
| 4 | **Why blind expansion is dangerous** — the setup for CSQE | needs building |
| 5 | **CSQE** — grounding the expansion in real documents | **not yet crafted. This is the priority.** |
| 6 | Why two retrievers, and why expansion goes to only one | hardest; needs building |

⚠️ **Item 6 is the thesis's actual contribution and the hardest to explain.** Do not skip it
because it is difficult — a jury that does not understand it will not credit it.

---

## 5. The raw material — three real examples from our results

All three are from `chapter4.tex:894-896`, Table 4.26. In every case the blind baseline scored
**0.000** and CSQE scored **1.000**. These are real, verified, in the thesis.

### ⭐ Example 1 — the one to build the explanation around

> **Query:** «ما هي الأسماء الخمسة؟» — *"What are the Five Nouns?"*
>
> **Blind expansion guesses:** a list of popular given names — Muhammad, Adam, Ibrahim…
>
> **What it actually means:** the Arabic grammatical category *الأسماء الخمسة* — أب، أخ، حم، فو، ذو
>
> **CSQE:** looks at real documents from the corpus first, sees the grammar article, builds the
> expansion from *its* words. **0.000 → 1.000.**

**Why this one is the best:** every Arabic speaker in the room instantly feels the ambiguity.
Nobody needs a definition of anything. The failure is obvious, the fix is obvious, and the
jury reaches the conclusion themselves before you state it. **That is what makes it convincing
rather than merely clear.**

### Example 2 — good backup, same shape
> «ما هو الرباط المنصوري؟» — blind guesses a **surgical suture**; it is actually a **Mamluk-era
> Sufi lodge** endowed by Sultan al-Mansur Qalawun. The corpus supplied the right words:
> رباط، مملوكي، قلاوون.

### Example 3
> «ما هو الفن الجزيري؟» — blind guesses **modern environmental/land art**; it is **Insular
> (Hiberno-Saxon) art**.

### ⚠️ The detail that makes the story honest — do not omit it

`chapter4.tex:901`: for all three of these, **the bare query with no expansion at all already
found the right article.** Blind expansion actively *poisoned* a query the system had already
solved. CSQE stayed on target and kept the hit.

That is a stronger and more interesting story than "expansion helps": it says **a confident
wrong guess is worse than no guess**, and grounding is what prevents it. Build the narrative
around that, not around "we added more words".

---

## 6. The numbers to use — and the discipline about them

The defence should carry **very few numbers**. Suggested spine:

> BM25 alone: **0.4621** → our system: **0.7137**. That is **+54.5%**.

Optionally one more, for the placement finding:

> Expansion on the word-matcher only: **0.7137**. On both retrievers: **0.6936**. On the
> meaning-matcher only: **0.6474**.

⚠️ **Every number must be checkable against `CLAUDE.md`.** Do not invent, round loosely, or
restate from memory. Two traps:
- **0.6936 means two different things** — it is the both-expanded result *and*, coincidentally,
  the per-query mean of the best system. In the defence it means the both-expanded result.
- **The three placement numbers must all be RRF.** Do not mix in the CC values.

---

## 7. Angles worth testing — none of these are decided

The chat should try these and keep what works. **Test them on Elhaj; he is the judge.**

**For the jury's own background (signals and control):**
- The dense retriever behaves like a **matched filter** — it works best when the query is a
  clean template of what you want. Padding it with a long generated description is like adding
  noise to the reference signal: the match degrades. BM25 counts term hits, so more terms means
  more chances to score. **That single asymmetry is why the expansion goes to one retriever and
  not the other** — and it may be the most natural possible framing for this specific jury.
- Blind expansion is **open-loop**; CSQE closes the loop by taking a measurement from the corpus
  before acting. First-pass retrieval is the sensor. When the sensor is wrong, the loop drives
  the wrong way — which is exactly our Type B regression (131 queries).

**General analogies to try:**
- The librarian who only matches words on book spines.
- Asking someone to fetch a book by describing it from memory, versus letting them glance at the
  shelf first.

⚠️ **Analogies must survive the follow-up question.** An analogy that collapses when a jury
member pushes on it is worse than none. Stress-test each one before adopting it.

---

## 8. What NOT to do

- **Do not open with RAG.** It needs its own explanation and invites the "where's the chatbot?"
  question before you are ready for it.
- **Do not lead with architecture diagrams.** Pipeline boxes explain *what* the system does, not
  *why* it was needed. The why comes first.
- **Do not claim model size predicts performance.** `chapter5.tex:20` states this only with heavy
  qualification, and a sharp jury member reading the thesis will catch a stronger claim on a slide.
- **Do not oversell.** We improved retrieval on one Arabic benchmark, MSA only, with one
  retriever pair. The limitations are in `chapter5.tex` §5.2 and should be owned, not hidden —
  a prepared limitation is a strength in a defence.
- **Do not build slides yet.** Narrative first. Slides are a later task and will be wasted work
  if the story changes.

---

## 9. Deliverables, in order

1. **The CSQE explanation.** One example, worked through completely, that a non-specialist
   follows and finds convincing. **Nothing else starts until Elhaj signs this off.**
2. The other five items from §4, each in the same style.
3. The one-sentence answer to "where is the generation?"
4. A defence narrative outline — the order of ideas, not slides.
5. Anticipated questions with prepared answers, especially:
   - "Why didn't you evaluate the final answer quality?"
   - "Why only Modern Standard Arabic?"
   - "Why is Aya's licence a problem?" *(CC-BY-NC — `chapter5.tex:60`)*
   - "Isn't this just prompt engineering?"
6. Only then: slide structure.

---

## 10. Context files worth reading if the chat needs depth

| File | For |
|---|---|
| `chapter4.tex` §4.10 | per-query error analysis — where gains and losses come from |
| `chapter5.tex` §5.1 | the twelve conclusions, in order |
| `chapter5.tex` §5.2 | the eight limitations — defence ammunition |
| `research_decisions/B1_abstract_workpack.md` | the tightest existing summary of the whole project |
| `meetings/video_2_text_July.md` 18:45–21:00 | the original discussion of this exact problem |
