# F1 · Deliverable 1 — The CSQE example, worked through

**Status:** DRAFT v1, awaiting Elhaj sign-off. Nothing else in F1 starts until this is signed off.
**Audience:** EEE professors. Arabic speakers. Assume zero knowledge of retrieval.
**Runtime:** ~4 minutes spoken.
**Golden example:** qid 3034 — «ما هي الأسماء الخمسة في اللغة العربية؟»

---

## Part A — The script

Nothing here needs a definition the jury doesn't already have. No "RAG", no "embedding", no
"BM25", no "vector". Those words appear later in the defence, after this example has done its job.

---

### Beat 0 — the setup (40 seconds, before the example)

*This is the minimum the example needs to stand on. Items 1 and 2 of the narrative will replace
this with something better; for now it works.*

> "A search engine finds documents by matching words. If you type four words, it has four words
> to work with. That is not much when the library has two million passages.
>
> So we had an idea, and it is not our idea — it comes from the literature. Before searching,
> ask a language model to **write the answer it thinks is correct**. Then glue that text onto the
> question and search with both. Now instead of four words you have eighty, and many of them are
> the words the real document uses.
>
> It works. That is not in dispute. But watch what happens on this question."

---

### Beat 1 — the question *(ask the room, out loud)*

**On screen — Arabic only, large:**

> ## ما هي الأسماء الخمسة في اللغة العربية؟

> "This is a real question from our test set. Please answer it out loud."

*The room answers in about two seconds: **أب، أخ، حم، فو، ذو**. School grammar. Everyone knows it.*

> "Two seconds. Nobody hesitated."

⚠️ **If nobody answers** — that is equally good. Say: *"Some of you hesitated. Hold onto that
feeling, because that is exactly what happened to our machine."* The beat is robust either way.

---

### Beat 2 — what the machine wrote

**On screen, next to the question:**

> «فئة خاصة من الأسماء الأكثر شيوعًا واستخدامًا، ولها قواعد نحوية خاصة:
> ١. **محمد** ٢. **آدم** ٣. **إبراهيم** ٤. **إسماعيل** …»

> "That is what our language model produced. Word for word — I have not edited it.
>
> It is an 8-billion-parameter model, trained with Arabic as a priority. And notice: the question
> says **في اللغة العربية**. We told it the subject. It still listed the most popular boys' names
> in the Arab world.
>
> And it was not hesitant. It gave the category a definition and numbered the list."

**The line to land here:** *it was confidently, fluently, grammatically wrong.*

---

### Beat 3 — why that is not just a funny mistake

> "Now — we never show that text to a user. Nobody reads it. It goes straight into the search box,
> stuck onto the original question."

**On screen — one arrow:**

```
   ما هي الأسماء الخمسة في اللغة العربية؟
              +  محمد، آدم، إبراهيم، إسماعيل …
              ↓
        [ SEARCH — 2 million passages ]
```

> "So the search engine is now hunting for an article about famous men named Muhammad and Adam.
>
> The correct article — the grammar one — does not contain a single one of those words.
> It never comes back. Not at rank one, not anywhere in the top ten.
>
> Score: **zero**."

---

### Beat 4 — the twist ⭐ *(this is the whole example; do not rush it)*

> "Here is the part I want you to sit with.
>
> Before we added anything — the bare question, on its own, no model, no expansion —"

**On screen:**

| | score |
|---|---|
| Bare question, nothing added | **1.000** |
| Question + the model's help | **0.000** |

> "It already worked. Perfectly. Rank one.
>
> Our improvement took a query the system had already solved, and broke it.
>
> This is not a small model failing. This is a strong model, answering fluently, being helpful —
> and doing damage. **A confident wrong guess is worse than no guess at all.**"

*Pause. Let it sit. This is the moment the jury understands the problem is real.*

---

### Beat 5 — hand them the fix

> "So — what should it have done instead?"

*Ask it as a real question. Wait. Someone in the room will say: it should have looked it up first.*

> "Yes. Exactly that. Don't answer from memory. **Look first.**"

⚠️ **This is the transition.** The jury proposes the solution, we don't. Everything after this
point they experience as *confirming their own idea*, not as absorbing ours. Do not step on it by
answering your own question.

---

### Beat 6 — CSQE, in three steps

> "That is the entire method. Three steps.
>
> **One.** Send the bare question to the search engine first. Take the top five documents back.
> They are not necessarily right — this is a cheap first look, not the answer.
>
> **Two.** Read those five. Pull out the sentences that actually match the question.
>
> **Three.** Use *those* sentences as the expansion. Real words, from real documents, that are
> already in our own library."

**On screen — the same first pass, what it returned:**

> «الأسماء الخمسة المعروفة في اللغة العربية هي **(أب، أخ، حم، فو، ذو)**، ويختلف النحاة في
> عدّ سادس هو **(هن)** لقلة استعماله.»

> "Now the expansion carries أب، أخ، حم، فو، ذو — and إعراب، and مضاف. The right vocabulary,
> because it was **copied**, not invented.
>
> Score: **1.000**. Correct article, rank one."

---

### Beat 7 — the sentence they leave with

> "Blind expansion asks the model: **what do you think this is?**
>
> Corpus-steered expansion asks the library: **what do you actually have?**
>
> The library cannot hallucinate. It only contains what it contains."

---

## Part B — The 20-second version, for their own field

*Optional. Use only if the room is warm and the control framing feels natural. Needs testing.*

> "In your language: the blind method is **open loop**. We compute a correction from an internal
> model of the world and apply it without ever measuring anything.
>
> CSQE closes the loop. The first-pass retrieval is the **sensor** — we take one measurement from
> the corpus before we act.
>
> And it has the failure mode you would predict: when the sensor is wrong, the loop drives the
> wrong way. We measured that. It is 131 queries out of 2,896."

⚠️ Owning that failure mode is what makes the analogy survive a follow-up. Don't use the framing
without the last line.

---

## Part C — Pushback, prepared

**"So you just run a search before the search? Isn't that circular?"**
> Yes — deliberately. The first pass only has to be right *sometimes*. It is right 36.6% of the
> time, and on those queries the final system reaches 0.8877. When it is wrong, we still keep two
> blind samples and the original query, so the query never ends up worse than where it started.

**"What if the first-pass documents are wrong?"**
> Then it hurts, and we counted it: 131 queries, 36% of our regressions, 4.5% of all queries.
> Net effect is still strongly positive — 56.8% of queries improve, 16.6% regress.

**"Why not just show the user the model's answer? It was fluent."**
> Because it was wrong. Fluency was the problem, not the solution. Our job is to put the correct
> document in front of the generator; a fluent wrong answer is exactly what we are trying to stop.

**"Is CSQE purely corpus-based then?"**
> No, and we should say so before they ask. Four expansion samples: **two** copied from the
> corpus, **two** still generated blind. The ablation is in the thesis — corpus-only scores
> 0.5381, blind-only 0.5752, the 2+2 mix 0.6157. The mix beats both. We are not claiming
> generation is useless; we are claiming it must be anchored.

---

## Part D — Provenance (every claim above is checkable)

| Claim in the script | Source |
|---|---|
| Query text, qid 3034 | `WS4_TASK_4.12_BIGWIN_EXAMPLES.md:37` |
| The model's actual blind output (محمد، آدم، إبراهيم…) | same, line 38 — quoted from `enhanced_queries_aya_expanse_8b.pkl` |
| The corpus-grounded text (أب، أخ، حم، فو، ذو + هن) | same, line 39 — from `exp_013_csqe_aya_8b.pkl` |
| blind 0.000 → CSQE 1.000 | `chapter4.tex` Table 4.26; verified per-query 2026-05-31 |
| Bare query already scored 1.000 | `WS4_TASK_4.12_BIGWIN_EXAMPLES.md:20,24-26`; `chapter4.tex:901` |
| First pass = top-5, 2 corpus + 2 blind, α=4 | `CLAUDE.md`, CSQE config |
| 36.6% / 0.8877 · 131 regressions · 56.8% / 16.6% | `CLAUDE.md`, error analysis block |
| Ablation 0.5381 / 0.5752 / 0.6157 | `CLAUDE.md`, exp 013c/013d table |
| Aya = 8B, Arabic-priority | `CLAUDE.md` |

**One discrepancy to note:** Table 4.26 in `chapter4.tex` prints the query as
«ما هي الأسماء الخمسة؟», dropping «في اللغة العربية». The real query has it. The defence should
use the **full** query — it is strictly stronger, because the model was told the domain and still
failed. Worth deciding whether to fix the thesis table too.

---

## Part E — Open for Elhaj

1. Does Beat 4 (the twist) land, or does it feel like admitting failure?
2. Keep Part B (open-loop / closed-loop), or drop it?
3. Is 4 minutes too long for one example?
