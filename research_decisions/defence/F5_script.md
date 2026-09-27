# F5 · Defence script — word for word

**Budget:** 600s total. **Mohammed 300s · Osman 300s.**
**Convention:** plain text = say it. *[italics in brackets]* = stage direction, do not read aloud.
**Pace assumption:** ~122 words/minute. Calm, not rushed. Mohammed's half below is **608 words**.

> Corrects the timing table in [F4_content_design.md](F4_content_design.md), which summed to 685s.
> The budget below closes at exactly 600 and splits 300/300.

| | Slide | Beat | s |
|---|---|---|---|
| **M** | 1 | Cover | 10 |
| **M** | 2 | Agenda | 20 |
| **M** | 3 | Frozen model → RAG | 40 |
| **M** | 4 | Retrieval sets the ceiling → the gap | 35 |
| **M** | 5 | Objectives | 30 |
| **M** | 6 | The system, specialised | 50 |
| **M** | 7 | Baseline + the finding | 45 |
| **M** | 8 | Query2Doc, and what broke | 70 |
| **O** | 9 | The catch — الأسماء الخمسة | 60 |
| **O** | 10 | CSQE | 70 |
| **O** | 11 | Placement — the contribution | 75 |
| **O** | 12 | Results | 50 |
| **O** | 13 | Conclusion, challenges, future work | 45 |

---

# MOHAMMED — 300 seconds

## Slide 1 · Cover — 10s

Good morning. I'm Mohammed, this is Osman, and our project is Corpus-Steered Query Expansion for
Arabic Retrieval, supervised by Dr. Tahani.

*[Do not read the title slowly. Names, then move.]*

## Slide 2 · Agenda — 20s

Here is what we'll cover. The problem we set out to solve. Our objectives. Then the methodology —
what we actually built. Then our results, and our conclusions. Osman takes over halfway through.

## Slide 3 · A frozen model, and RAG — 40s

*[Slide: the general RAG loop. Four boxes.]*

Everyone here has used ChatGPT. A language model is trained once and then frozen — everything it
knows sits in its weights, and it is not looking anything up. Ask it something outside its training
and it does not say "I don't know." It answers fluently, confidently, and wrongly.

RAG is the industry's answer. Don't retrain the model — give it the documents. The user asks a
question, we **search the corpus**, we put the passages we find next to the question, and the model
answers from that text instead of from memory.

*[⚠ Say "search the corpus". Never "vector database" — your final finding is about BM25, which has
no vectors in it, and that word here will cost you slide 11.]*

## Slide 4 · Retrieval sets the ceiling — 35s

But RAG only moved the problem. The answer can never be better than what the search returned.
**Retrieval sets the ceiling.**

The English literature fixes this with query enhancement — repairing the question before it reaches
the retriever. But it was built on English, using proprietary models of 175 billion parameters.
Arabic is barely covered. And Arabic is not English: morphology, spelling variation and diglossia
all break the match between a question and the document that answers it.

We are not repairing the Arabic language. Those challenges are the *cause* of the failure. We
compensate one layer up — at the query.

## Slide 5 · Objectives — 30s

We set nine objectives, and they group into three.

**Diagnose** — build both retrieval baselines, and measure where Arabic retrieval fails and why.

**Adapt** — make query enhancement work in Arabic using small, openly available models.

**Ground and place** — ground the expansion in the corpus itself, and find where in the pipeline to
apply it.

## Slide 6 · The system, specialised — 50s

*[Same diagram, same position, now filled in.]*

Our corpus is MIRACL Arabic: 2,896 questions over 2.06 million Wikipedia passages, with **human**
relevance judgements.

For the retrieval step we built two, separately. **BM25 matches the words** — it counts how many of
the query's terms appear in a passage. **mDPR matches the meaning** — it maps text to a vector, so
a passage lands close to a question that means the same thing, even with no shared words.

We built these two independently first. We'll come back to combining them.

And they fail on **different** questions. Remember that.

We score with NDCG@10 — did the right passage come back, and how near the top.

## Slide 7 · Baseline, and the finding that chose our technique — 45s

Before changing anything, we reproduced the published MIRACL baselines, so that any improvement
later could be attributed to our intervention and not to our setup. BM25 scored **0.4621**, mDPR
**0.4993**.

Then we analysed all 2,896 queries. **Thirty-four percent failed outright.** For one query in ten,
no relevant passage appeared even in the top hundred — a ceiling that better ranking cannot lift.
And the **shortest queries were the weakest group, at 0.345**.

So the fault is not the retriever, and not the index. It is the question — too few words to separate
one passage from two million. That is why our fix goes **in front of** the retriever.

*[No figure here. Numbers only. `fig_4_3_length_box_v1.png` is a backup slide — the length curve is
not monotonic and a box plot invites "so longer is better?", which is not what the data says.]*

## Slide 8 · Query2Doc, and what broke — 70s

*[The query enhancement layer drops into the diagram. Then expand it.]*

So we add a layer in front. The idea comes from the literature — it is not ours.

Before searching, ask a language model to write the answer it *thinks* is correct. Nobody ever reads
that text. Glue it onto the question, and search with both. Four words becomes eighty — and many of
those words are the ones the real document uses.

This is **Query2Doc**. We tested it with **ten open models**, two to eight billion parameters, on
free Colab GPUs. Aya Expanse 8B was best overall.

On dense retrieval it worked. Every viable model improved — Aya took us from 0.4993 to **0.6164**.

On BM25 it broke. Six of the nine models made it **worse**. The cause is **term dilution**: BM25
scores by term overlap, so eighty generated words drown the four that carried the meaning. We fixed
it by repeating the original question inside the expansion. All nine recovered — Aya reached 0.5855.

So the two retrievers did not respond to the same technique the same way. One was helped, one was
harmed. **Hold onto that.**

### Handover

Osman will show you what happened when we looked at what the model was actually generating.

*[Same sentence every rehearsal. Note 10 makes this a graded moment — the panel is watching whether
you look like one team.]*

---

# OSMAN — 300 seconds

*[Coming next — Parts 4–8 of F4 converted to script at 60/70/75/50/45s.]*

---

## Timing notes for Mohammed

- **608 words.** At 122 wpm that is 299 seconds. You have no slack, so read it as written.
- **Read it aloud with a stopwatch before you touch Canva.** If your first run is 5:30, that is
  normal — it means your natural pace is ~110 wpm and we cut 60 more words, not that you speed up.
  A rushed delivery is audible and it costs marks.
- **Three sentences must not be cut, whatever else goes:** *"Retrieval sets the ceiling."* ·
  *"They fail on different questions — remember that."* · *"One was helped, one was harmed."*
  The first pre-empts the most likely hostile question; the other two are the setup for slide 11,
  which is your actual contribution.
- **If you must trim**, take it from slide 3 (the RAG explanation — the diagram carries it) and
  slide 6 (drop "it counts how many of the query's terms appear in a passage"). Never from slide 7
  or 8.
