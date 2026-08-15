# F10 · Where to cut — getting each half from 6:00 to 5:00

**Measured:** Mohammed ~6:00, Osman ~6:00. **Target:** 5:00 each, ideally a little under.
**Needed:** about 60 seconds from each half.

Every cut below is chosen on one principle: **cut what the panel already knows, or what the
slide already shows. Never cut what only you can say.**

---

# MOHAMMED — find 60s

## The big one: slides 3–5 are 80 seconds of material the panel already has

You spend a minute and twenty seconds explaining what a language model is, what RAG is, and
that retrieval matters. This is an EEE faculty panel. Dr. Tahani's Note 9 warns about exactly
this — *"تضيع الزمن كله في النظريات… وتكون انت ما عملت حاجة في الشرح"*.

**Slide 3 — cut this clause entirely (−6s)**
> ~~ولو الداتا اتغيّرت، أو كانت داتا خاصة ما شافتها، الـ **retraining** عملية مكلفة جداً.~~

The parametric-memory point already lands. Retraining cost is a second reason for a conclusion
they have already accepted.

**Slide 4 — compress the librarian from four beats to one (−12s)**

Currently you walk the scene: someone asks, the librarian goes, he brings books, the answer is
written from them. The **slide already shows all four scenes**. Say it once:

> خلّونا نتخيّل مكتبة: أمين المكتبة ما بيجاوب من ذاكرتو — بيمشي يجيب الكتب، والإجابة بتتكتب منها.
> ودي بالظبط الـ RAG.

**Slide 5 — drop the restatement (−8s)**
> ~~**جودة الإجابة بتعتمد على الكتب اللي أمين المكتبة جابها.** جاب الصح — الإجابة صح. جاب غلط —
> الإجابة غلط والموديل بيهلوس.~~

The fork diagram *is* this sentence. Go straight from the UofK example to «يعني الـ bottleneck هنا».

**Subtotal: −26s**

## Slide 7 — name the four, don't read them (−10s)

Four cards now instead of three, and the Arabic examples are large on screen. **The panel are
Arabic speakers — the examples explain themselves.** Name the four categories and stop:

> العربي عندو تحدياتو الخاصة: الـ morphology، والـ orthography، والتشكيل، والـ diglossia. وزي ما
> شايفين في الأمثلة دي، كلها بتكسر المطابقة بين السؤال والدوكيومنت.

Do not read كتب / كاتب / مكتوب aloud. They read it faster than you can say it.

## Slide 11 — one clause, not two sentences (−10s)

> وأول حاجة، **أعدنا إنتاج النتائج المنشورة بالظبط** — عشان أي تحسّن بعد داك يكون بسببنا إحنا.
> الـ mDPR جاب **0.4993**، والـ BM25 **0.4621**.

Drops "عشان نتأكد إنو الـ pipeline بتاعنا صاح" and "مش بسبب اختلاف في الـ setup" — both restate
the same idea.

## Slide 13 — stop narrating the charts (−10s)

The two charts are side by side with a dashed baseline through them. Say the finding, not the
reading:

> على الـ Dense كل الموديلات التسعة اتحسّنت. على الـ BM25، ستة من تسعة بقى أداءها أسوأ.
> نفس التقنية، نفس النص المولّد — ونتيجتين في اتجاهين متعاكسين.

Cut «زي ما شايفين على اليسار» and «على اليمين» — they can see.

## Slide 14 — the sweep detail is Q&A, not talk (−12s)

> ~~وما وقفنا عند كده — عملنا **sweep** على معامل التكرار لكل موديل من التسعة. ولقينا إنو الـ
> optimum **بيختلف من موديل لموديل**: أقوى موديلين عربياً وصلوا لأحسن أداء بالـ adaptive
> repetition، والباقي بقيمة ثابتة بين خمسة وعشرة.~~

Replace with one clause: «وعملنا sweep على معامل التكرار لكل موديل — والـ optimum طلع بيختلف من
موديل لموديل.» The adaptive-vs-fixed detail is a perfect Q&A answer; it is wasted in the talk.

**Mohammed total: −68s → about 4:52**

---

# OSMAN — find 60s

## The cheapest 30 seconds in the whole deck: move slide 19 to backup

Slide 19 is the four-metric table. It exists to answer *"did you cherry-pick NDCG@10?"* — a
question **nobody may ask**. It costs 30 seconds of a 5-minute half to pre-empt a hypothetical.

**Move it behind the thank-you slide as a backup.** If it comes up, you flip to it and answer in
15 seconds with a table already built. Zero narrative loss.

**−30s, and it is the single best trade in this deck.**

## Slide 16 — name the three steps, don't explain them (−10s)

The CSQE figure now fills the slide and shows the whole pipeline. You are describing a diagram
the panel is looking at.

> فبنبني الكويري النهائية من تلاتة components: جمل متسخرجة من الـ corpus، واتنين blind expansions،
> والكويري الأصلية مكرّرة. والنتيجة: من **0.4621** لـ **0.6157**.

Cut the per-step captions ("Look / Read / Expand" narration) — they are on the figure.

## Slide 18 — you are repeating numbers already shown (−12s)

The progression figure is on screen and the three metric pills are beside it.

> ~~والسيستم النهائي بتاعنا — hybrid، بيدمج BM25 بالـ Corpus-Steered Expansion مع Dense بالكويري
> الأصلية — أدّانا **0.7137**: أحسن من الـ baseline بـ **54.5%**، وتفوّق على الـ hybrid اللي بدون
> query expansion بـ **13.9%**.~~

Those three numbers are printed on the slide. Keep the **loop methodology** — that is the part
only you can say, and it is what makes this a methodology slide rather than a scoreboard. Then:

> والأهم إنو الـ short queries — أول مشكلة واجهتنا — هي الأكتر استفادة.

## Slide 20 — the six conclusions go faster (−10s)

You are reading six statements that are printed on the slide in full. Take them at a brisk clip
with no elaboration between them — one breath, not six. The **contribution paragraph** and the
**paper in preparation** line are what matter here; protect those and speed up the list.

## Slide 17 — tighten the "why", protect everything else (−8s)

This is the contribution. Do not cut the four numbers or the principle. But:

> ~~لو الاتنين شالوا نفس الكويري الموسّعة، بيتقاربوا، وبيبدوا يرجّعوا نفس الدوكيومنتات ويغلطوا نفس
> الغلطات — و**الـ complementarity اللي دمجنا عشانها بتضيع**.~~

becomes:

> لو الاتنين شالوا نفس الكويري، بيتقاربوا — و**الـ complementarity اللي دمجنا عشانها بتضيع**.

**Osman total: −70s → about 4:50**

---

# What must NOT be cut

| Keep | Why |
|---|---|
| The **الأسماء الخمسة** example, slide 15, all 50s | Highest value-per-second in the deck. Real measured output, in Arabic, to an Arabic-speaking panel. |
| The **four placement numbers**, slide 17 | This is the contribution. Everything else is setup for it. |
| *"Retrieval sets the ceiling"*, slide 5 | Pre-empts the most likely hostile question before it is asked. |
| The **loop methodology**, slide 18 | The panel grades method as much as result, and this is the only slide that shows method. |
| The **contribution + paper** lines, slide 20 | The closing claim. |
| The **UofK example**, slides 3 and 12 | It is their own institution. It costs little and buys attention. |

---

# Summary

| | Now | Cut | After |
|---|---|---|---|
| Mohammed | ~6:00 | −68s | **~4:52** |
| Osman | ~6:00 | −70s | **~4:50** |
| **Total** | **~12:00** | **−2:18** | **~9:42** |

That leaves roughly 20 seconds of slack against a 10-minute slot — which you will need, because
live delivery always runs slower than rehearsal.

**If you can only make one cut in each half:** Mohammed compresses the librarian walk-through on
slide 4, and Osman moves slide 19 to backup. That alone is 42 seconds.
