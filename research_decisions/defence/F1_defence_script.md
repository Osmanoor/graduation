# F1 · Defence script — word for word

**Status:** DRAFT v1 · built from [`F1_narrative_outline.md`](F1_narrative_outline.md)
**Length:** ~3,300 spoken words ≈ **25 minutes** at a calm pace.
**Mode:** straight narration. No questions to the room. No live demo.
**Convention:** plain text = say it. *[italics in brackets]* = stage direction, do not read aloud.

> Every number in this script is traceable to `CLAUDE.md` or the thesis. Do not add numbers while
> speaking. If you cannot remember one, skip it — the argument works without it.

---

# ACT 1 — LLMs · ~2 min

*[Slide: a ChatGPT-style chat window. Nothing else.]*

Everyone in this room has used a system like this. ChatGPT, Claude, Gemini. So let me start
from something you already know, and I will build from there.

A large language model is trained once, on a fixed set of text, up to a fixed date. After that,
it is frozen. Everything it knows, it learned during that training, and it carries that knowledge
in its weights — not in a database it can look things up in.

That creates one specific problem, and I want to be precise about it.

If you ask it something outside what it was trained on, it does not stop and say "I don't know."
It produces an answer. A fluent answer. Well-written, confident, correctly structured — and wrong.
We call this hallucination.

*[Pause here. This sentence is doing work later.]*

I want you to hold onto that shape, because you will see it three more times in this
presentation: **the failure is not silence. The failure is confident, well-formed error.**

And there is a second limit. The model has never seen your organisation's private documents. Your
hospital records, your internal reports, your archives. It was not trained on them, so it cannot
use them. Retraining it on your data every time your data changes is not practical — it costs
millions and takes weeks.

So the industry needed a way to give a frozen model access to knowledge it was never trained on.

---

# ACT 2 — RAG · ~3 min

*[Slide: the four-box RAG loop. Question → Search → Passages → Answer.]*

The answer the industry converged on is called Retrieval-Augmented Generation. RAG.

The idea is simple, and I can state it in one sentence: **do not retrain the model — give it the
documents.**

Concretely, four steps.

One. The user asks a question.

Two. We take that question and we **search a library of documents** for the passages that relate
to it.

Three. We take those passages and we paste them next to the question, as context.

Four. The model answers from the text in front of it, instead of from memory.

*[Slide: highlight step 2, then add a small caption under it: "match the words | match the meaning"]*

One detail about step two that will matter later, so let me plant it now. There are two different
ways to search a library. You can **match the words** — find documents that contain the same terms
as the question. Or you can **match the meaning** — represent the question and the documents as
mathematical objects and find the ones that are close together, even if they share no words at all.

Both are used in practice. Remember that there are two. I will come back to it.

That is RAG. And you can see immediately why industry adopted it: no retraining cost, the private
data never leaves your control, every answer can be traced back to a source document, and when the
documents change, the system's knowledge changes with them. Nothing is retrained.

---

# ACT 3 — the problem · ~3 min

*[Slide: same four boxes, but step 2 is now red.]*

Now. Notice what this architecture has done. It has moved the burden.

The whole system rests on step two. So the question we should ask is: **what happens if step two
brings back the wrong passages?**

Let me make the scale physical.

In our work, the library holds **two million passages**. For any given question, perhaps **one or
two** of them contain the answer. Step two has to find those two, out of two million, in a fraction
of a second.

*[Slide: "Imagine: a medical assistant." — the word Imagine must be visible.]*

Imagine a clinical assistant built this way. A doctor asks about a drug interaction. If step two
returns two million-to-one wrong — if it fetches a passage about a different drug — then the model
does what it always does. It reads what is in front of it and writes a fluent, confident,
well-structured answer. Based on the wrong passage.

The model has no way to know. It cannot detect that it was handed the wrong document.

*[Slow down. This is the load-bearing sentence of the entire defence.]*

Which brings me to the sentence this whole thesis rests on:

**A RAG system's answer can never be better than what its retrieval stage found. If the right
passage never arrives, no model — however large, however capable — can recover it. Retrieval sets
the ceiling for everything that comes after it.**

*[Beat.]*

I want to be direct about something, because it is the first thing people ask us. Our project does
not build a chatbot. We did not work on the answer-writing part. We worked on step two — the
retrieval. That is a deliberate choice, and it is exactly the reason I just gave you: step two is
the ceiling. Improving the part above the ceiling changes nothing. Raising the ceiling changes
everything above it.

This field has a name: **information retrieval**. Given a user's question, return the passages that
actually answer it. That is the problem this thesis addresses.

---

# ACT 4 — why Arabic makes it worse · ~3 min

*[Slide: three Arabic examples, large.]*

Now let me narrow. Retrieval is hard in general. In Arabic it is harder, for three reasons that
are specific to the language.

**First, morphology.** Arabic is built on roots and patterns. One root generates dozens of surface
forms. The user writes one form in the question. The document uses a different form of the same
root. To a system matching words, those are two unrelated strings. Nothing matches.

**Second, orthography.** أ and ا and إ. ة and ه. ى and ي. The same word, written two acceptable
ways, is two different sequences of bytes. Again, no match.

**Third, diglossia.** People ask questions the way they speak — in dialect. Encyclopedias and
formal documents are written in Modern Standard Arabic. There is a systematic gap between how
questions are asked and how knowledge is written down.

*[Slide: 34% / 33% / 33%]*

Now, I could simply assert that this makes Arabic retrieval fail. Instead we measured it.

We built a standard Arabic retrieval system — the established, published baseline — and we ran it
over **2,896 real questions**. Then we analysed the result of every single one.

**34% of questions failed outright.** The system returned nothing useful.
Another 33% were mediocre.
Only **33%** were successful.

And one more finding that I find more troubling than the first. Even when we let the system return
its **top hundred** passages — a hundred, not ten — for about **10% of questions the correct passage
was not in there at all.** Not ranked badly. Absent.

*[Slide: 1–3 words → 0.345]*

We also broke the results down by how long the question was. The weakest group was the shortest
questions — one to three words. They scored **0.345**, well below the rest.

So: a third of questions fail, and the shortest questions fail worst.

---

# ACT 5 — the query is the weak link · ~2 min

*[Slide: a four-word Arabic question, alone in the middle of the slide. Then a hundred-word paragraph appears beside it.]*

That last finding pointed us at where the problem actually lives, so let me show you what we are
really asking the system to do.

Here is a typical question. Four words.

Four words, to distinguish one passage from two million.

And here is the passage that answers it. A hundred words, written by somebody who never saw the
question, using their own vocabulary, for their own purposes.

*[Beat.]*

**The failure is not in the search engine. It is in the question.** The question is too poor to
search with. It carries too little information to separate what we want from everything else — and
in Arabic, the few words it does carry may not even match, for the three reasons I just gave.

And that observation determines where the fix has to go. If the defect is in the question, then we
should repair the question — before it reaches the search engine. Not rebuild the search engine.
Not re-index two million passages.

This matters practically. It means the fix is a module you place in front of an existing system.
Nothing downstream is touched. Nothing is retrained. Nothing is re-indexed.

---

# ACT 6 — query expansion · ~3 min

*[Slide: query → LLM → pseudo-document → query + pseudo-document → search]*

So: how do you repair a question that is too short?

The idea comes from the literature, and it is elegant. **Before searching, ask a language model to
write the answer it thinks is correct.** Not to show anyone — nobody reads it. Then glue that
generated text onto the original question, and search with both together.

Four words becomes eighty. And critically, many of those extra words are the words the real
document actually uses. The gap between how the question is phrased and how the document is written
gets bridged — by the model's own vocabulary.

The technique is called **Query2Doc**. It is not our invention. But it was developed for English,
validated on English benchmarks, using proprietary models of a hundred and seventy-five billion
parameters or more.

So the open questions were: does it transfer to Arabic? Does it still work with small, openly
available models that a student can actually run? We tested **ten open models, between two and
eight billion parameters**, on free cloud GPUs.

*[Slide: 0.4993 → 0.6164]*

And it works. On the meaning-matching retriever, our best generator took the score from **0.4993**
to **0.6164**. A large improvement, from an eight-billion-parameter open model, at no API cost.

*[Slide: split — a green arrow up, a red arrow down.]*

But we found something in that experiment that I want to flag now, because it comes back at the end.

The improvement was not uniform. Expansion helped the **meaning-matcher** for every viable model.
But for the **word-matcher**, it made things **worse** for six of the nine models. The reason turned
out to be dilution: when you add eighty generated words to a four-word question, the original four
words — the ones that actually mattered — lose their weight in the scoring.

We fixed that, by repeating the original question several times inside the expanded query to restore
its weight. That worked; it recovered every model.

But hold onto the finding itself: **the two ways of searching did not respond to expansion the same
way.** That is the first sign of something, and I will return to it in a few minutes.

---

# ACT 7 — the catch · ~3 min

*[Slide: the Arabic query, alone, very large.]*

So far this is a good story. Expansion works.

Now I want to show you a single question from our test set, because it changed how we thought about
the whole approach.

The question is: **«ما هي الأسماء الخمسة في اللغة العربية؟»**

*[Beat. Let them read it. Most of the room will silently answer it — it is school grammar.]*

Notice the question says **في اللغة العربية**. The subject is stated. This is a question about
Arabic grammar, and the answer is أب، أخ، حم، فو، ذو.

*[Slide: the model's real output appears underneath.]*

Here is what our language model generated for it. This is its real output, word for word, I have
not edited it:

**«فئة خاصة من الأسماء الأكثر شيوعًا واستخدامًا … ١. محمد ٢. آدم ٣. إبراهيم ٤. إسماعيل»**

It listed the most popular boys' names in the Arab world.

*[Beat.]*

An eight-billion-parameter model, trained with Arabic as a priority, told explicitly that the
subject is Arabic grammar. And it produced a numbered list of first names. It even gave the
category a definition. It was fluent, it was structured, it was confident, and it was completely
wrong.

*[This is Act 1's shape returning. Name it.]*

That is the failure I asked you to hold onto at the start. Not silence — confident, well-formed
error. Except now it is inside our own system.

*[Slide: the arrow into the search box.]*

And remember what happens to that text. Nobody reads it. It goes straight into the search box,
attached to the original question. So the search engine is now hunting for an article about famous
men named Muhammad and Adam. The correct article — the grammar one — contains none of those words.

It never comes back. Not at rank one. Not anywhere in the top ten. **Score: zero.**

*[Slide: the two-row table.]*

And here is the part that stopped us.

Before we added anything at all — the bare four-word question, no model, no expansion — the system
had already found the correct article. Rank one. **Score: one point zero.**

*[Slow.]*

**Our improvement took a question the system had already solved, and broke it.**

*[Beat.]*

Now — I want to be honest about how common this is, because it is the fair question to ask. Perfect
reversals like this one, from a full score to zero, occur in about **143 of our 2,896 questions**.
I am not showing it to you because it is typical. I am showing it because it makes the mechanism
**visible**. The quieter version of the same effect is much more widespread — and I will give you
that number shortly.

The lesson generalises, and it is this: **a confident wrong guess is worse than no guess at all.**

---

# ACT 8 — CSQE · ~3 min

*[Slide: blank, or just the word "الفتوى".]*

So what should the system have done instead?

It answered from memory. It should have **looked first**.

Our supervisor gave us an analogy for this, and it fits so exactly that I want to use his words.
He said: *a standard language model is like a layperson — it tries to answer from what it knows.*

*[Slide: two figures — a man answering from memory, a scholar with an open book.]*

Ask a layperson a question of fiqh, and he answers from what he remembers. He sounds certain. He
may be right. He may be badly wrong, and he will sound the same either way.

Ask a mufti the same question, and he does something different. His general knowledge tells him
roughly where the answer lives — but he does not rule from memory. He takes the book off the shelf,
he finds the passage, and he **quotes its actual wording** before he gives the ruling.

He is not more intelligent than the layperson. He has one extra step: **he looks before he speaks.**

*[Slide: three numbered steps.]*

That extra step is the entire method, and it is called **Corpus-Steered Query Expansion** — CSQE.
Three steps.

**One.** Search once with the bare question, and take back the top five documents. These are not
the answer. This is a cheap first look — some of them will be wrong.

**Two.** Read those five, and extract the sentences that genuinely match the question.

**Three.** Use *those sentences* as the expansion. Words **copied** from documents that are actually
in our library — not words invented by a model.

*[Slide: the first-pass document appears, with أب أخ حم فو ذو highlighted.]*

Go back to our question. The first look returned the grammar article — the real one, from our
corpus — containing **أب، أخ، حم، فو، ذو**.

So now the expansion carries the correct vocabulary. Not because the model knew it. Because it was
copied from a document that had it.

**Score: one point zero.** Correct article, rank one.

*[Slide: two lines only.]*

Which gives the difference in one line:

**Blind expansion asks the model: what do you think this is?**
**Corpus-steered expansion asks the library: what do you actually have?**

The library cannot hallucinate. It only contains what it contains.

*[Only if asked, or if you have time:]*
One point of precision, so I am not overstating it. CSQE does not throw the model away. We generate
four expansion samples: two copied from the corpus, two still generated blind. We tested all three
combinations. Corpus-only scored 0.5381. Blind-only scored 0.5752. The mixture scored **0.6157** —
better than either alone. So the claim is not that generation is useless. It is that generation must
be **anchored**.

---

# ACT 9 — placement · ~3 min

*[Slide: two boxes side by side — "match the words" | "match the meaning"]*

Now I come to what I think is our main contribution, and it goes back to the detail I planted at
the beginning.

Two ways to search. Match the words. Match the meaning.

They fail on **different questions**. When the question and the document share vocabulary, word
matching is excellent. When they share meaning but no vocabulary — which in Arabic is constant —
meaning matching wins. So the natural move is to run both and merge the results.

*[Slide: 0.6267]*

We did that. Merging the two, with no expansion at all, scored **0.6267**. That is a strong system.
It became the number we had to beat.

Then we did the obvious thing. We had a technique that improves retrieval, and two retrievers. So we
gave the expansion to both.

*[Beat.]*

It made things worse.

*[Slide: three-row table, revealed one row at a time.]*

| Expansion applied to | Score |
|---|---|
| Both retrievers | 0.6936 |
| The meaning-matcher only | 0.6474 |
| **The word-matcher only** | **0.7137** |

Same technique. Same fusion. Same everything. The only variable is **which retriever receives the
expansion** — and the spread is large.

*[Slide: a matched filter diagram, or just the words "matched filter".]*

Here is why, and I think this room will recognise the mechanism faster than most.

The **word-matcher** works by counting term hits. Give it more terms, and you give it more chances
to match. Expansion is straightforwardly good for it.

The **meaning-matcher** does something else entirely. It compresses the whole input into a single
representation — one average meaning for the entire text. Now bolt eighty generated words onto a
four-word question. The question's meaning is no longer what dominates that average. It is diluted.

It behaves like a **matched filter**. A matched filter performs best when the reference is a clean
template of the signal you are looking for. Padding that reference with generated text is adding
noise to the template. The match degrades. That is exactly what we measured — and it is the same
asymmetry that appeared back in Act 6, when expansion helped one retriever and hurt the other.

*[Slide: one sentence, alone.]*

But there is a deeper reason, and it is the one I would like to leave with you.

**Fusion only pays off while the two retrievers remain different.** Their value is that they fail on
different questions. Feed the same eighty generated words into both, and they start to look alike —
they begin retrieving the same documents and making the same mistakes. The complementarity we were
merging for disappears.

So the finding is not "expansion is good" or "expansion is bad." It is: **expansion has a place, and
the place matters.** Apply it to the sparse retriever, and withhold it from the dense one — precisely
to protect the difference between them.

---

# ACT 10 — results · ~2 min

*[Slide: two numbers. Nothing else.]*

Let me put the whole thing in two numbers.

Standard Arabic keyword search — the established baseline — scores **0.4621**.

Our final system scores **0.7137**.

That is an improvement of **54.5%**.

*[Beat.]*

And against the harder comparison — the strongest system we could build with no query expansion at
all, the merged retriever at 0.6267 — we are **13.9%** ahead.

*[Slide: the constraint list.]*

What it cost is, I think, part of the result. One openly available eight-billion-parameter model.
Free cloud GPUs. No commercial API. No hundred-and-seventy-five-billion-parameter model. No
re-indexing of the corpus, and no modification to the retrievers. The whole intervention sits in
front of an existing system.

*[Slide: 56.8% / 26.6% / 16.6%]*

And this is the number I promised you earlier. Across all 2,896 questions, our final method improved
**56.8%** of them, left **26.6%** unchanged, and made **16.6%** worse. Average gain, per question,
**+0.189**.

So the dramatic example I showed you is the visible edge of something that is happening, more
quietly, on the majority of questions.

---

# ACT 11 — limits · ~1 min

*[Slide: the limitations, plainly listed. Do not rush this — read them.]*

Finally, I want to state the limits of this work myself, rather than leave them to be found.

We evaluated on one benchmark — Arabic Wikipedia — in **Modern Standard Arabic only**. We did not
test dialect, and given that diglossia was one of the three problems I identified at the start, that
is a real gap.

We used one pair of retrievers and one language. We have not shown these findings transfer.

We measured **retrieval quality, not final answer quality**. That was deliberate — retrieval is the
ceiling — but it does mean we have not demonstrated the downstream improvement directly.

Our best generator, Aya Expanse, is licensed **CC-BY-NC**. That is fine for research. It rules out
commercial deployment without a different model.

CSQE costs an extra retrieval pass for every query. It is not free.

And it has a failure mode we can name precisely: when the first look returns poisoned documents, the
expansion is grounded in the wrong thing, and the query gets worse. That happened to **131 questions**
— about 4.5% of the total. We measured it, and it is the clearest direction for future work.

*[Beat.]*

Thank you. I am happy to take questions.

---

# APPENDIX — prepared answers

**"Where is the generation? This is only half a RAG system."**
> A RAG system's answer is bounded by what it retrieves. If the right passage never comes back, no
> generator can recover it. We worked on the ceiling, not the part below it. *(Already delivered in
> Act 3 — this is the fallback if it is asked again.)*

**"Why didn't you evaluate final answer quality?"**
> Because it would measure the generator, not our contribution. Answer quality depends on the model,
> the prompt, and the judge. Retrieval metrics isolate what we actually changed. Our supervisor's
> guidance was explicit on this: get retrieval right and generation follows.

**"Why only Modern Standard Arabic?"**
> The benchmark we needed — with human relevance judgements at this scale — exists only in MSA.
> MIRACL gave us 2,896 judged questions over 2.06 million passages. No dialect equivalent exists.
> Building one is future work, and we say so.

**"Isn't this just prompt engineering?"**
> The prompt is one component. The findings are not about prompts: that expansion dilutes sparse
> retrieval and repetition repairs it; that grounding beats generation; and that placement within a
> hybrid pipeline changes the result by 0.066. None of those is a prompt choice. They hold across ten
> different models.

**"Why is the licence a problem?"**
> Aya Expanse is CC-BY-NC — non-commercial. Our results stand as research. A commercial deployment
> would need a permissively licensed generator, and we did not measure that trade-off. It is listed
> as a limitation.

**"How do you know the example wasn't cherry-picked?"**
> It was chosen to be clear, and I said so when I showed it. The claim rests on the aggregate:
> 56.8% of 2,896 questions improved, mean +0.189. The example illustrates the mechanism; the
> distribution carries the argument.

**"Does a bigger model always do better?"**
> No, and our data says otherwise. Be careful here — the thesis qualifies this heavily. Do not
> claim a clean relationship in either direction.
