# F1 · Deliverable 4 — Defence narrative outline

**Status:** DRAFT v1, built from Elhaj's arc (2026-08-07 voice note). Order of ideas, not slides.
**Audience:** EEE professors, Arabic speakers, no retrieval background.
**Mode:** straight narration. No asking the room questions. No live demo.
**Budget:** ~25 min of talking. Times below are targets, not promises.

**The spine in one line:** everyone knows LLMs → LLMs are frozen → industry answer is RAG →
RAG is only as good as what it retrieves → Arabic retrieval fails a lot → the query is the
weak link → expand it → expansion can lie → ground it in the corpus → and put it in the right
place.

---

## Act 1 — LLMs (2 min) · *start where they already are*

Every person in the room has used ChatGPT. Start there, not at retrieval.

Three facts, fast, no literature review:
1. An LLM is frozen at its training data. It has a cut-off date and a fixed scope.
2. Ask outside that scope and it does not say "I don't know" — it produces something fluent and
   wrong. That is hallucination.
3. It cannot see your company's private data at all. It was never trained on it.

**Land this:** the failure mode is not silence. It is confident, well-written error.
That single idea gets reused three more times in this talk — it is the same failure that
blind expansion has in Act 7. Plant it here deliberately.

---

## Act 2 — RAG (3 min) · *the industry's answer*

> Don't retrain the model. Give it the documents.

The loop, in four steps, said plainly:
1. User asks a question.
2. **Search a library of documents** for the passages related to that question.
3. Paste those passages next to the question.
4. The LLM answers **from the text in front of it**, not from memory.

Why industry adopted it: no retraining cost, private data stays private, answers can be traced to
a source, and the knowledge updates when the documents update.

> ⚠️ **TRAP — do not say "vector database" here.** Say **"search the library."** Then add one
> sentence: *"and there are two ways to search a library — match the words, or match the meaning."*
> Those two ways cost you ten seconds now and they are the ONLY reason Act 9 is understandable
> later. If we teach the jury "RAG = vector database", our main contribution has nowhere to land
> and we have to retract the setup mid-talk.

---

## Act 3 — the problem, stated strictly (3 min) · *this is our thesis*

> "The whole system rests on step 2. So — what if step 2 brings back the wrong passages?"

Make the scale physical:
- Two million passages in our library.
- For a given question, maybe **one or two** of them contain the answer.
- Step 2 has to find those two.

Then the consequence, which is the sentence the entire defence hangs on:

> **The LLM can only answer from what it is given. If the right passage never arrives, no model —
> however large — can recover it. The retrieval stage sets the ceiling for everything after it.**

**This is also the prepared answer to "where is the generation in your project?"** It is not a
defensive answer. It is the reason the work exists. Deliver it here, on our terms, before anyone
asks it as a challenge.

> ⚠️ **TRAP — the medical example.** A medical assistant is a great way to make "wrong chunk =
> real harm" concrete, so use it — but start the sentence with **"Imagine."** We evaluated on
> Arabic Wikipedia (MIRACL), not medical data. If a slide implies otherwise, that is the one
> thing in the defence that could be called dishonest. One word prevents it.

Close the act by naming it: *this is the field of **information retrieval**, and it is the
problem this thesis works on.*

---

## Act 4 — why Arabic makes it worse (3 min) · *narrowing*

Now narrow from "retrieval is hard" to "Arabic retrieval is hard." Arabic examples, to Arabic
speakers — this act is free.

Three causes, one Arabic example each:
1. **Root-and-pattern morphology** — one root, dozens of surface forms. The question says one
   form, the document uses another. No word matches.
2. **Orthographic variation** — أ / ا / إ, ة / ه, ى / ي. Same word, different bytes, no match.
3. **Diglossia** — people ask in dialect; encyclopedias are written in MSA.

Then stop asserting and give **our own measurement**:

> We built a standard Arabic retrieval baseline and analysed every query.
> **34% of queries failed outright.** Another 33% were mediocre. Only 33% were successful.
> And even searching 100 passages deep, the right passage was missing entirely for **10%** of
> questions.

**Land this:** this is not a claim from a paper. We measured it on 2,896 questions.

> ⚠️ **TRAP** — do NOT say "performance improves as queries get longer." Our corrected numbers
> are non-monotonic: 1–3 words 0.345, 4–8 words 0.511, 9+ words 0.476. Say only what is true:
> **short queries are the worst bucket.** A jury member with Table 4.4 open will catch the
> stronger claim.

---

## Act 5 — the query is the weak link (2 min) · *narrowing again*

> "So where exactly does it break? Look at what we actually hand the search engine."

A typical question is four words. Four words to separate one passage from two million. The
document that answers it is a paragraph of a hundred words, written by someone who never saw
the question and used different vocabulary.

> **The failure is not in the search engine. It is in the query. It is too poor to search with.**

Because the defect is in the query, the fix goes in front of the retriever — not inside it.
Nothing gets rebuilt, nothing gets re-indexed. That modularity is a selling point: say it.

---

## Act 6 — query expansion (2 min) · *the idea, from the literature*

> Before searching, ask an LLM to write the answer it *thinks* is right. Glue that text onto the
> question. Search with both. Four words becomes eighty — and many of the extra words are the
> ones the real document uses.

Name it: **Query2Doc**. Note it is not ours — it is established work, English, GPT-3 scale.
What is open: does it work for Arabic, with small open models, and where should it go in a
hybrid system.

Then show it works: our numbers, with the best generator.

---

## Act 7 — the catch (3 min) · *the pivot of the whole talk*

**Example A — expansion helping.** *(NOT YET BUILT — see open question at the bottom.)*

**Example B — expansion hurting.** Full script in
[`F1_csqe_example.md`](F1_csqe_example.md). Compressed:

- Query: «ما هي الأسماء الخمسة في اللغة العربية؟»
- The model wrote: محمد، آدم، إبراهيم، إسماعيل — the popular boys' names.
  It was **told** the subject was Arabic grammar and still got it wrong. Fluent, numbered,
  confident, wrong.
- That text went into the search box. Score **0.000**.
- **The twist:** the bare question, with no help at all, had already scored **1.000**.

> **We took a query the system had already solved, and broke it.**
> Act 1's failure mode, now inside our own pipeline: **a confident wrong guess is worse than no
> guess at all.**

> ⚠️ **Honesty guard — say this before anyone asks.** This is the loud version. Perfect flips
> like it are ~143 of 2,896 queries. It is here because it makes the mechanism *visible*, not
> because it is typical. The typical effect is quieter and bigger: **56.8% of queries improve.**
> Volunteering the frequency is what makes the example survive scrutiny instead of looking cherry-picked.

---

## Act 8 — CSQE (3 min) · *the fix, and the supervisor's analogy*

> "The model answered from memory. It should have looked first."

**The Mufti analogy** — from Rashad's consultation, and his own words fit exactly:
*"A standard LLM is like a layperson — it tries to answer generatively."*

> Ask a layperson a question of fiqh, and he answers from what he remembers. He sounds certain.
> He may be wrong.
>
> Ask a mufti, and he does something else. His general knowledge tells him roughly where the
> answer lives — but he pulls the book off the shelf and **quotes its actual wording** before he
> rules.
>
> Blind expansion is the layperson. CSQE is the mufti.

**The method, three steps:**
1. Search once with the bare question. Take the top five documents. Cheap first look, not the answer.
2. Extract the sentences in them that actually match the question.
3. Use *those* sentences as the expansion — words **copied** from our library, not invented.

Back to Act 7's query: the first pass returned «الأسماء الخمسة … (أب، أخ، حم، فو، ذو)».
The expansion now carries the real vocabulary. Score **1.000**.

> **Blind expansion asks the model: what do you think this is?**
> **CSQE asks the library: what do you actually have?**
> The library cannot hallucinate. It only contains what it contains.

> ⚠️ **TRAP — Rashad's original Mufti analogy was about knowing the *structure* of the corpus**
> (which chapter to open), which is metadata/clustering work we did **not** implement. Our use is
> the narrower "opens the book instead of answering from memory," which is faithful to CSQE. If
> Rashad or anyone from that meeting is present, say "we took one half of your analogy" rather
> than letting them notice the gap.

> ⚠️ CSQE is **not** purely corpus-based: four samples, **two** copied from the corpus, **two**
> still blind. Ablation: corpus-only 0.5381, blind-only 0.5752, the 2+2 mix **0.6157**. The mix
> beats both alone. Have this ready; do not hide it.

---

## Act 9 — placement: our actual contribution (3 min) · *hardest act, do not skip*

Cash in the ten seconds spent in Act 2.

> Two ways to search: **match the words**, and **match the meaning**. They fail on different
> questions, so running both and merging the results beats either alone — **0.6267**, our
> strongest baseline with no expansion at all.

> Then the obvious move: give the expansion to both. It made things **worse**.

Why, in their own language:
- The **word-matcher** counts term hits. More words = more chances to hit. Expansion helps it.
- The **meaning-matcher** compresses the whole text into one average meaning. Bolt eighty
  generated words onto a four-word question and the question's meaning is diluted. It is a
  **matched filter**: it works when the reference is a clean template of what you want. Padding
  the reference with generated text is adding noise to it, and the match degrades.

The deeper reason, and the one to say last:
> **Fusion only pays when the two retrievers stay different.** Expanding both makes them look
> alike, and the complementarity we were fusing for disappears.

The three numbers, all RRF, same fusion, only the placement changes:

| Expansion applied to | NDCG@10 |
|---|---|
| **Word-matcher only** | **0.7137** |
| Both | 0.6936 |
| Meaning-matcher only | 0.6474 |

> ⚠️ All three must be RRF. Do not mix in the CC numbers. And 0.6936 here means *both-expanded* —
> it is coincidentally also the per-query mean of the best system. Never say both meanings.

---

## Act 10 — results (2 min) · *few numbers, said slowly*

One line:
> Standard Arabic keyword search: **0.4621**. Our system: **0.7137**. **+54.5%.**
> Against the strongest baseline with no expansion at all — **0.6267** — we are **+13.9%**.

And what it cost: an **8-billion-parameter open model**, on free Colab GPUs. No API, no
175B model, no re-indexing.

---

## Act 11 — own the limits (1 min) · *strength, not weakness*

Do not wait to be asked:
- One benchmark, Arabic Wikipedia. Modern Standard Arabic only — no dialect.
- One retriever pair, one language.
- We measured retrieval, not final answer quality. Deliberate: retrieval is the ceiling.
- Our best generator, Aya Expanse, is **CC-BY-NC** — research use, not commercial deployment.
- CSQE costs an extra retrieval pass per query.
- It hurts when the first pass is poisoned: **131 queries**, 4.5% of the total.

---

## Running list of traps (one place)

| # | Trap | Fix |
|---|---|---|
| 1 | "Vector database" in Act 2 | say "two ways to search a library" — Act 9 depends on it |
| 2 | Medical data sounding like our dataset | start with "Imagine" |
| 3 | "Longer queries do better" | false, non-monotonic — say only "short is worst" |
| 4 | الأسماء الخمسة looking cherry-picked | volunteer the frequency (143/2,896) and the real number (56.8%) |
| 5 | Mufti analogy over-promising structure-awareness | we took half of it; say so |
| 6 | Mixing RRF and CC placement numbers | all three must be RRF |
| 7 | 0.6936 means two different things | in the defence it is both-expanded only |
| 8 | Model size predicts performance | `chapter5.tex:20` qualifies this heavily — do not simplify it |

---

## Open — blocks Act 7

**Example A does not exist yet.** Act 7 needs a query where blind expansion clearly *helped*,
so the jump to Act 8 is motivated ("expansion works — but look what it does here"). Without it,
Act 6 says expansion works and Act 7 immediately says it fails, and the jury cannot tell which
is true.

Per-query scores are not saved in the repo — only computed live in the Colab error-analysis
notebook (`WS4_TASK_4.12_BIGWIN_EXAMPLES.md` §5 has a self-contained miner cell that would find
one).
