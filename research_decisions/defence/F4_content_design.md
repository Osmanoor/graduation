# F4 · Content design — continuing Mohammed & Osman's 2026-08-13 brainstorm

**Status:** Parts 1–2 are yours (tightened + timed). Parts 3–8 are new, written in the same voice.
**Budget:** 600 seconds. Every part below carries a time. They sum to 600 — check them as you write.
**Device:** one system diagram, held in a fixed position, one component expanded per slide.

---

## First: three corrections to Parts 1–2

### ① Do not say "vector database" — say "search the corpus"

Your Part 2 describes the general RAG figure as *"we find relevant passages in our vector database."*
**Change this.** It is the single most damaging sentence you could put in the opening.

Your final system applies the expansion to **BM25** — a lexical retriever with no vectors in it at all.
If the panel learns in minute 2 that "RAG = vector database", then in minute 8 your central finding
(*expand the sparse retriever, not the dense one*) has no vocabulary to land in, and you have to
retract your own setup mid-talk to explain it.

Say **"search the corpus"** or **"the retrieval step"** in the general figure. Introduce the two
kinds of search — lexical and semantic — when you specialise the figure. That is exactly where you
already planned to introduce BM25 and Dense, so it costs you nothing.

### ② Sharpen "we are not solving the Arabic problems"

The framing is right, but as worded it invites: *"then why did you spend a chapter on morphology?"*

Precise version: **the Arabic linguistic challenges are the cause of the failure we measured, not
the thing we repair.** We do not normalise orthography or strip morphology. We compensate one layer
up, at the query, by injecting vocabulary that already carries the right surface forms. That is
literally what corpus-steered expansion does — it copies attested wording out of the corpus rather
than trying to fix the language.

That version is defensible, and it also pre-loads the CSQE explanation seven slides early.

### ③ "Reproduce the paper's results" → be specific about which

As said, it invites *"which paper, and did your numbers match?"* State it precisely and it becomes
a strength instead:

> "Before changing anything, we reproduced the published MIRACL baselines for both retrievers, so
> that any improvement we measured later could be attributed to our intervention and not to a
> difference in setup."

That is a methodology answer, and it is the kind of sentence examiners are listening for.

### ④ On the error-analysis graph — your instinct is half right

You said you might skip the graph so the jury doesn't grill you on it. **Avoiding figures does not
avoid questions** — Dr. Tahani says explicitly they will ask *"اشرح لينا الـ figure الفلاني"*. The real
rule is: never show a figure you cannot explain.

But there *is* a trap in this particular one. The length–performance relationship is **not
monotonic**: 1–3 words = 0.345, 4–8 words = **0.511**, 9+ words = 0.476, and overall correlation is
$r \approx -0.01$. A box plot invites *"so longer queries are better?"* and the honest answer is no.

**So: put the numbers on the slide, not the figure.** Keep `fig_4_3_length_box_v1.png` as a backup
slide. You claim only *"the shortest queries are the weakest group"* — which is true, is enough, and
cannot be attacked. If they ask for the distribution, you have it one keypress away.

---

## The time problem — read this before writing any slides

Parts 1–2 as you brainstormed them are, spoken at a calm pace, about **six minutes** of material:

| Your beat | Realistic |
|---|---|
| AI booming → parametric memory → RAG → bounded by retrieval → QE in English → Arabic gap | 90s |
| Problem statement + research question | 30s |
| General RAG figure, explained component by component | 40s |
| Specialise it: MIRACL, why we chose it, BM25, Dense, embeddings, complementarity | 90s |
| Baseline experiment + error analysis | 45s |
| QE layer introduced + Query2Doc + prompt + 10 models | 75s |
| **Total** | **~370s (6:10)** |

That leaves **3:50 for CSQE, the placement finding, all results, and the conclusion** — i.e. your
entire contribution gets less time than your setup. This is precisely the failure Dr. Tahani warns
about in Note 9: *"تضيع الزمن كله في النظريات… وتكون انت ما عملت حاجة في الشرح."*

**Parts 1–2 must come down to ~3:35.** Concretely, cut these four things:

- **"Why we chose MIRACL"** — a justification, not a finding. Cut entirely → Q&A. *(−20s)*
- **Embeddings / vectorisation** — you already said you'd skip it. Hold that line. *(−15s)*
- **The general RAG figure narration** — let the diagram carry it. One sentence, not five. *(−20s)*
- **The Query2Doc prompt** — keep it *visible* on the slide (it pre-empts "what prompt?") but do
  not read it aloud. *(−20s)*

That gets you to ~295s. The remaining trim comes from tightening the opening chain, below.

---

# PART 1 · Opening + problem statement — 90s

*Slides 1–4. Mohammed.*

Your zigzag chain is right and it mirrors the Chapter 1 preamble, so it is defensible line by line.
Delivered tight, it is four beats and ninety seconds:

1. **AI is everywhere now, but its memory is parametric** — a model only knows what it was trained
   on, and it does not say "I don't know." It answers fluently and wrongly. *(20s)*
2. **RAG was the industry's answer** — don't retrain the model, give it the documents. Show the
   general figure here: a question, a search over the corpus, the passages, the answer. *(25s)*
   → **"search the corpus", not "vector database".**
3. **But RAG only moved the problem.** The answer can never be better than what the retrieval step
   found. Retrieval sets the ceiling. *(20s)*
4. **Query enhancement is the English literature's fix for that** — repair the query before it
   reaches the retriever. Validated on English, with proprietary 175B models. **Arabic is not
   covered**, and Arabic is not English: root-and-pattern morphology, orthographic variation,
   diglossia. *(25s)*

**Land the problem statement as one sentence**, and make it the research question:

> **To what extent do LLM-based query enhancement techniques transfer to Arabic, and how much do
> they actually improve retrieval?**

Then §① above: we are not repairing the Arabic language. We are compensating at the query.

---

# PART 2 · Objectives + the system + the baseline — 145s

*Slides 5–7. Mohammed.*

### 2a · Objectives — 30s

Nine objectives grouped into three. One line each:

- **Diagnose** — build both baselines, measure where and why Arabic retrieval fails *(obj. i–ii)*
- **Adapt** — make Query2Doc work in Arabic with small open models; compare ten of them *(obj. iii–vi)*
- **Ground & place** — ground the expansion in the corpus, and find where to apply it *(obj. vii–ix)*

Say these three words here, again on the conclusion slide. Repetition is what makes ten minutes
feel finished rather than cut off.

### 2b · The system, specialised — 60s

The device starts here. Same diagram, same position, now filled in:

- **Corpus** → MIRACL Arabic. 2,896 questions, 2.06M Wikipedia passages, **human** relevance
  judgements. State the numbers, skip why we chose it.
- **Retrieval** → two of them, built **separately**: **BM25S** matches the words, **mDPR** matches
  the meaning.
- **Metric** → NDCG@10. Did the right passage come back, and how near the top.

> **Say explicitly that they are separate for now:** *"We built these two independently first — we'll
> come back to combining them."* Otherwise the panel spends the next three minutes wondering whether
> the two boxes are one system or two, and you lose them.

Thirty seconds on lexical-vs-semantic is the load-bearing part — the whole contribution rests on
the distinction. Ten seconds on complementarity ("they fail on different queries"), which sets up
fusion later. Nothing on embeddings.

### 2c · Baseline + the finding that selected the technique — 55s

> "Before changing anything, we reproduced the published MIRACL baselines for both retrievers."

BM25S = 0.4621. mDPR = 0.4993. Then the error analysis, as three numbers on the slide, no figure:

- **34%** of queries failed outright
- for about **1 in 10**, no relevant passage appeared even in the top 100 — a recall ceiling that
  better ranking cannot lift
- the **shortest queries were the weakest group: 0.345**

> **This is the hinge of the whole talk.** The fault is not in the retriever and not in the index —
> it is in the query, which carries too little information to separate one passage from two million.
> So the fix goes in front of the retriever. Nothing downstream is touched, nothing is re-indexed.

Then the motion beat you wanted: **the query enhancement layer drops into the diagram.**

---

# PART 3 · Query2Doc, and what broke — 75s

*Slide 8. Mohammed closes here, or hand over before this — see note at the end.*

Expand the QE component.

- **The idea:** before searching, ask an LLM to write the answer it *thinks* is right. Nobody reads
  it. Glue it to the query and search with both. Four words becomes eighty — and many of those words
  are the ones the real document uses. That is the vocabulary gap, bridged.
- **Our constraint:** openly available models, **2–8B**, free Colab GPUs, no commercial API. We
  compared **ten** of them. *(← this one line discharges objective iv — do not drop it)*
- **On dense retrieval, it worked.** Every viable model improved. Best was **Aya Expanse 8B:
  0.4993 → 0.6164**, +23.5%.
- **On BM25, it broke.** Six of nine models got **worse**.
- **Why: term dilution.** BM25 scores by term overlap. Add eighty generated words to a four-word
  query and the four words that carried the meaning are now a rounding error in the score.
- **Fix: query repetition.** Repeat the original query inside the expanded one to restore its
  weight. **All nine models recovered.** Aya at β=2: 0.4621 → **0.5855**, +26.7%.

**Plant the finding, then move on:**

> *"So the two retrievers did not respond to the same technique the same way. One was helped, one
> was harmed. Hold onto that — it comes back at the end."*

Keep the prompt visible in a corner of this slide. Do not read it.

---

# PART 4 · The catch — 65s

*Slide 9. Osman.*

The strongest sixty seconds you have. Say this part in Arabic — the panel are Arabic speakers on a
video call and they will get it instantly, with no explanation from you.

- The question: **«ما هي الأسماء الخمسة في اللغة العربية؟»**
  *(Pause. Let them answer it silently — it is school grammar. Do not fill the silence.)*
- The question **states its own subject**: في اللغة العربية. The answer is أب، أخ، حم، فو، ذو.
- What our model actually generated, unedited: **«فئة خاصة من الأسماء الأكثر شيوعًا… ١. محمد ٢. آدم
  ٣. إبراهيم ٤. إسماعيل»** — the most popular boys' names in the Arab world.
- An 8B model, trained with Arabic as a priority, told explicitly that the subject is Arabic
  grammar. Fluent, structured, confident, completely wrong.
- **And nobody reads that text.** It goes straight into the search box. So the retriever is now
  hunting for an article about men named Muhammad and Adam. The grammar article contains none of
  those words. **Score: 0.000.**
- **Before we added anything**, the bare four-word query had already found the correct article at
  rank one. **Score: 1.000.**

> **"Our improvement took a question the system had already solved, and broke it."**

Volunteer the frequency **before** you are asked — it is what stops the example looking
cherry-picked: perfect reversals like this occur in **143 of 2,896** queries. It is not typical; it
is shown because it makes the mechanism visible.

**The lesson, one line:** *a confident wrong guess is worse than no guess at all.*

---

# PART 5 · CSQE — 75s

*Slide 10. Osman.*

Expand the QE component again — the device pays off here, because the audience now watches the same
box change contents rather than meeting a new diagram.

> "It answered from memory. It should have looked first."

Dr. Rashad's analogy, in his words: *a standard LLM is like a layperson — he answers from what he
remembers, and he sounds equally certain whether he is right or wrong. A mufti does one extra thing:
he takes the book off the shelf and quotes its wording before he rules. Not more intelligent — he
looks before he speaks.*

**Corpus-Steered Query Expansion, three steps:**

1. **Look.** Search once with the bare query, take the top 5. Not the answer — a cheap first glance.
2. **Read.** Extract from those 5 the sentences that genuinely match the query.
3. **Expand.** Use *those* sentences. Words **copied** from documents that are really in our corpus,
   not invented by a model.

Same question: the first glance returned the real grammar article, containing أب، أخ، حم، فو، ذو.
The expansion now carries the correct vocabulary — not because the model knew it, but because it was
copied from a document that had it. **0.000 → 1.000.**

**The difference in two lines** *(say this slowly and add nothing after it)*:

> **Blind expansion asks the model: what do you think this is?**
> **Corpus-steered expansion asks the corpus: what do you actually have?**

The corpus cannot hallucinate. It only contains what it contains.

**Result:** CSQE on BM25 = **0.6157**, against 0.5855 for blind expansion with repetition.

One precision to have ready *(say it only if time allows — otherwise it is your first Q&A answer)*:
CSQE does not throw the model away. Four samples: **two corpus-grounded, two still blind.** The
ablation says corpus-only 0.5381, blind-only 0.5752, mixed **0.6157** — the mix beats both halves.
Generation is not useless; it must be **anchored**.

---

# PART 6 · Fusion and placement — 80s

*Slide 11. Osman. This is the contribution — protect its time.*

Zoom back out to the whole system. Two retrievers, one expansion.

**First, fusion with no expansion at all.** Merge BM25 and mDPR with RRF: **0.6267**. Far above
either alone, because they fail on different queries. **That is the number we held ourselves to** —
not the weak baseline.

**Then the obvious move:** we have a technique that improves retrieval and two retrievers, so give
the expansion to both.

*(Beat. Deadpan.)* It made things worse.

| Expansion applied to | NDCG@10 |
|---|---|
| Nothing — fusion alone | 0.6267 |
| The meaning-matcher only | 0.6474 |
| **Both** | 0.6936 |
| **The word-matcher only** | **0.7137** |

Same technique, same fusion, same models. **The only variable is which retriever receives the
expansion**, and the spread is 0.0663.

**Why — and this room will recognise the mechanism.** BM25 counts term hits: more terms, more
chances to match. The dense retriever compresses the entire input into *one* vector — a single
average meaning. Bolt eighty generated words onto a four-word query and the query no longer
dominates that average. It behaves like a **matched filter**: best when the reference is a clean
template of the signal. Padding the template with generated text is adding noise to it.

**And the deeper reason — the sentence to leave them with:**

> **Fusion only pays off while the two retrievers stay different.** Their entire value is that they
> fail on different queries. Feed the same eighty words into both and they converge — same
> documents, same mistakes — and the complementarity you were merging for disappears.

So the finding is not *expansion is good* or *expansion is bad*. It is that **expansion has a place,
and the place matters**: apply it to the sparse retriever, withhold it from the dense one,
specifically to protect the difference between them.

*(This is where the Part 3 plant pays off — say so: "this is the same asymmetry we saw with
Query2Doc. It was there from the start; we just didn't understand it yet.")*

---

# PART 7 · Results — 65s

*Slide 12. Osman.*

The whole thing in two numbers: standard Arabic keyword search, **0.4621**. Our final system,
**0.7137**. An improvement of **+54.5%** — and **+13.9%** over the strongest system we could build
with no expansion at all.

**What it cost is part of the result:** one openly available 8B model, free Colab GPUs, no
commercial API, no 175B model, no re-indexing of 2.06M passages, and no modification to either
retriever. The whole intervention sits in front of an existing system.

**Where the gains actually come from** — 56.8% of the 2,896 queries improved, 26.6% unchanged,
16.6% worse; mean **+0.189** per query. And they land exactly where the baseline was weakest: the
**shortest queries gained the most proportionally, +43.6%** — which is the weakness identified back
in Part 2c, closed.

> That closes the cherry-picking question for good: the dramatic example was the visible edge of
> something happening quietly across the majority of queries.

---

# PART 8 · Conclusion, challenges, future work — 55s

*Slide 13. Osman.*

**Answer the research question you asked in Part 1.** *Do English QE techniques transfer to Arabic?*

> **Yes — but not unmodified.** Applied off the shelf they failed. Three adaptations were required,
> and each came out of a failure we measured:
> **1 · query repetition** — expansion diluted sparse retrieval;
> **2 · corpus grounding** — blind generation hallucinated on Arabic-specific terms;
> **3 · asymmetric placement** — expanding both retrievers destroyed the complementarity fusion
> depends on.

Then tick the three objective groups with the number that proves each:

| | | |
|---|---|---|
| **Diagnose** | baselines + error analysis | 0.4621 / 0.4993 · 34% fail · 0.345 short |
| **Adapt** | Query2Doc in Arabic, ten models | 0.4993 → 0.6164 dense · all 9 recovered on BM25 |
| **Ground & place** | CSQE + asymmetric fusion | **0.7137**, +54.5% |

**Challenges — three, not eight:** MSA only, no dialect. Aya Expanse is CC-BY-NC, so research-only.
CSQE depends on first-pass quality — when the first glance is poisoned, the expansion is grounded in
the wrong thing (131 queries, 4.5%).

**Future work — one, not nine:** a **first-pass quality gate** — check lexical overlap between the
top-1 document and the query before grounding, and fall back to blind expansion when it is too low.
That is expected to recover most of those 131 regressions. It follows directly from the limitation,
which is what makes it a good answer.

> "Thank you. We're happy to take your questions."

---

## The split, and the handover

| | Parts | Slides | Time |
|---|---|---|---|
| **Mohammed** | 1, 2, 3 | 1–8 | 310s |
| **Osman** | 4, 5, 6, 7, 8 | 9–13 | 340s |

That is 650s against a 600s budget — **you are 50 seconds over before you start.** Take it out of
Parts 1–2 using the four cuts listed above; do not take it out of Parts 5–7.

**Handover after Part 3**, on the plant:

> "So expansion works, but the two retrievers don't agree about it. Osman will show you what
> happened when we looked at what the model was actually generating."

Same sentence every rehearsal. Note 10 makes the handover a graded moment — the panel is watching
for whether you look like one team.

---

## On the animation

You want the components to expand and shrink in motion. **Get the effect without real animation.**

Build it as a sequence of **static slides that hold the diagram in the exact same position**, with
one component enlarged or highlighted per slide. The slide transition supplies the motion. To the
audience it is identical to an animated zoom — and it cannot stutter, drop frames, or desync over a
shared Google Meet stream, which real animation frequently does. It is also perhaps a quarter of the
build time, which matters with a day and a half left.

The continuity you are after comes from **the diagram never moving**, not from the tweening.
