# F7 · Mohammed's half — final content (slides 1 → handover)

**Built from:** Mohammed's feedback recordings, 2026-08-14 / 15 (rev. 3).
**Script language:** Arabish — Arabic with English technical terms, as spoken.
**Rev 3:** slide 8 condensed to RQ only · objectives restored to full text · baseline block added
(slides 9–13) · deletions applied · BM25 comparison figure generated.

---

## The running example — threaded across the talk

> **«ما الشروط التي تسمح للطالب بتأجيل دراسته في جامعة الخرطوم؟»**

| Where | What happens |
|---|---|
| **Slide 3** | Ask an LLM → it answers confidently, and it is invented. |
| **Slide 5** | Put the regulations *into* a RAG system → retrieval returns the wrong passages. Still wrong. |
| **Slide 11–12** | Expand the query → the right passage comes back. Payoff. |

> ⚠️ **Never attach a score to it.** Narrative device, not a result. Say «تخيّلوا معاي» / «لو جربنا».
> The measured example is «الأسماء الخمسة» in Osman's half.

---

## Slide 1 · Title & greeting — 15s

> السلام عليكم ورحمة الله وبركاته. حضورنا الكرام، الدكاترة الأعزاء.
> أنا محمد الحاج، ومعاي زميلي عثمان بشير. أطروحتنا اليوم بعنوان: **تحسين جودة الـ Retrieval في
> أنظمة الـ RAG العربية باستخدام الـ LLM-based Query Enhancement** — بإشراف الدكتورة تهاني عبدالله.

**Visual:** left third, a short Arabic query alone in clean type. Right two-thirds, a dense field of
document cards receding into depth. One thin gradient beam runs from the query into the field and
lights exactly **two** cards; the rest stay pale.

---

## Slide 2 · Agenda — 10s
> Content deferred until all slides exist.

---

## Slide 3 · LLMs, their limitation, and our example — 30s

> الـ **Large Language Models** — زي ChatGPT و Claude و Gemini — بقت أدوات قوية جداً في توليد النصوص
> والإجابة على الأسئلة.
>
> لكن عندها **limitation** أساسي: الـ memory بتاعتها **parametric** — المعرفة كلها مخزّنة جوّه الـ
> weights ومجمّدة عند لحظة التدريب. ولو الداتا اتغيّرت أو كانت داتا خاصة، الـ **retraining** مكلف جداً.
>
> خلّونا نشوف مثال حيمشي معانا طول العرض:
> **«ما الشروط التي تسمح للطالب بتأجيل دراسته في جامعة الخرطوم؟»**
>
> لوائح الجامعة ما موجودة في البيانات اللي الموديل اتدرّب عليها. ومع ذلك — **ما بيقول ليك «ما عارف»**.
> بيجاوب، بثقة، وبغلط. ودي الـ **hallucination**.

**On slide:** `Parametric memory` · `Frozen at training time` · `Retraining is expensive` · `Hallucination`
**Visual:** a large soft circle labelled `TRAINING DATA`, filled with tiny document glyphs, model at
centre. The UofK question enters from the right and lands **outside** the circle, in white space. A
confident arrow shoots back out to answer it anyway, in the warning accent, ending in an answer card
marked ✗.

---

## Slide 4 · RAG and the librarian — 25s

> عشان كده ظهر الـ **RAG**. الفكرة: بدل ما نعيد تدريب الموديل، بندّي ليهو **external knowledge base**
> يقدر يفتّش فيها.
>
> خلّونا نتخيّل مكتبة. جاء زول وسأل. أمين المكتبة ما بيجاوب من ذاكرتو — بيمشي يختار الكتب المناسبة
> ويجيبها، والإجابة بتتكتب **من الكتب دي**.
>
> ودي بالظبط الـ RAG: الـ query بتجي، النظام بيسترجع الـ passages من الـ corpus، والـ LLM بيجاوب منها.

**On slide:** four labels only — `Query` · `Retrieve` · `Passages` · `Answer`
**Visual:** two aligned bands. Upper — four illustrated scenes (person asking · librarian at shelves ·
librarian carrying three books back · person reading the answer). Lower — the four boxes in the
gradient. Between them, four faint vertical dotted connectors linking each scene to the box directly
beneath. Same width, perfect alignment. The alignment does the teaching.

---

## Slide 5 · Retrieval is the bottleneck — 25s

> نرجع لسؤالنا. حطّينا لوائح الجامعة **جوّه** الـ RAG system — يعني الإجابة موجودة في الـ corpus حرفياً.
> ومع ذلك النظام رجع بـ passages غلط، لأنو الطريقة اللي الطالب بيسأل بيها مختلفة عن الطريقة اللي
> اللائحة مكتوبة بيها. فالإجابة لسّة غلط.
>
> **جودة الإجابة بتعتمد على الكتب اللي أمين المكتبة جابها.** جاب الصح — الإجابة صح. جاب غلط — الإجابة
> غلط والموديل بيهلوس.
>
> يعني الـ **bottleneck** هنا، في الـ Information Retrieval. ودي اللي دفعتنا ندرس الـ techniques اللي
> بتحسّنو.

**On slide:** `Answer quality ≤ retrieval quality`
**Visual:** one query splits into two tracks. Upper (teal) → correct documents → **LLM icon** →
`CORRECT ✓`. Lower (warning) → wrong documents → **LLM icon** → `WRONG · HALLUCINATION ✗`. Draw the
LLM icon **identically** on both, with a caption between them: `same model`. Behind it, ghost the
four-box pipeline with step 2 lit.

---

## Slide 6 · Query Enhancement — rich in English, empty in Arabic — 25s

> فمشينا للـ literature. ولقينا إنو في اللغة الإنجليزية ده مجال **غني جداً ومدروس كويس** — الـ
> **Query Enhancement**: نصلّح الـ query **قبل** ما توصل للـ retriever، من غير ما نلمس الـ retriever
> ومن غير ما نعيد فهرسة الـ corpus. عائلة كاملة من التقنيات — Query2Doc، HyDE، GRF.
>
> طيب — ومشينا نشوف الـ literature **العربي**... ولقيناهو **ضعيف جداً**. ما في حد أثبت هل التقنيات دي
> بتنتقل للعربي، ولا هل بتشتغل بموديلات صغيرة كفاية إنو مجموعة زينا تقدر تشغّلها.

**Visual:** split slide. Left ~60% — the QE taxonomy tree, redrawn from `fig_2_3_qe_taxonomy.png`,
deliberately **dense**: many leaves, many labels, small type, `Query2Doc` highlighted in the accent
and everything else neutral grey. Right ~40% — two identical bookshelves, left one **packed**, right
one **nearly bare**, labelled `English` / `Arabic`.

---

## Slide 7 · But Arabic is not English — 20s

> طيب — **هل العربي زي الإنجليزي؟** إحنا ما عارفين إذا الحاجات دي حتنطبق بنفس الصورة ولا لأ. لأنو
> العربي عندو تحدياتو الخاصة:
>
> الـ **morphology** — root-and-pattern، الجذر الواحد بيطلع منو عشرات الصيغ.
> والـ **orthography** — الهمزة والألف، التاء المربوطة والهاء.
> والـ **diglossia** — الناس بتسأل بالعامية، والمعرفة مكتوبة بالفصحى.

**Visual:** redraw `fig_2_5_arabic_challenges.png` in the new theme, three panels. Under each label
one real Arabic example, **large**: كتب · كاتب · مكتوب · كتاب — أ / ا / إ · ة / ه — a colloquial
phrasing above its MSA equivalent. The Arabic teaches this slide; the English labels are captions.

---

## Slide 8 · Research question — 20s

*(condensed to one — the problem statement is already delivered by slides 6 and 7)*

> فالـ **research question** بتاعنا: **إلى أي مدى الـ LLM-based Query Enhancement بتقدر تحسّن الـ
> Arabic Information Retrieval — عبر الـ sparse والـ dense والـ hybrid — باستخدام موديلات مفتوحة من
> 2 لـ 8 مليار باراميتر؟**
>
> وأبعد من الـ validation — وده الـ **contribution** الخاص بينا — دايرين نعرف: **كيف الـ retrievers
> المختلفة بتتفاعل مع الـ Query Enhancement؟**

**On slide:** the RQ large, and one line beneath it:
`Beyond validation — how do different retrievers interact with query enhancement?`

**Visual:** full-width gradient band carrying the RQ in white type, generous margins. The
contribution line sits below it in the accent colour, visually lighter but clearly attached. This is
the only slide in the deck that looks like this — the conclusion calls back to it.

---

## Slide 9 · Objectives — 20s

> وعشان نجاوب على السؤال ده، حدّدنا **تسعة objectives**.

Read them briskly. Detail lives in Q&A.

**On slide — full text, nine rows:**

1. Establish dense and sparse baselines on MIRACL Arabic and measure their complementarity
2. Run a systematic error analysis to identify the failure modes QE must address
3. Adapt Query2Doc for Arabic zero-shot application on freely available cloud GPUs
4. Compare ten openly available LLMs from 2 to 8 billion parameters as query generators
5. Analyse how LLM-generated expansions interact with sparse versus dense retrieval
6. Investigate query repetition as a remedy for term dilution in BM25
7. Establish a hybrid fusion baseline without QE — the ceiling any enhancement must exceed
8. Adapt and evaluate CSQE for Arabic, isolating its components through ablation
9. Determine the optimal placement of query expansion within the hybrid pipeline

**Visual:** nine numbered rows, tight leading, numbers in the gradient, text neutral dark. **No
illustration** — this slide has to be dense and a graphic would fight the text.

---

# The baseline block

## Slide 10 · The system we built — 40s

*(Figure 3.1 restyled, without the QE layer — one diagram, each component labelled with what we used)*

> وبدينا بأول objective: **نبني الـ baseline**.
>
> ودي المنظومة اللي بنيناها — **نفس الكومبوننتس** اللي شفناها في الأول، لكن هسي مليانة بالتفاصيل
> بتاعتنا.
>
> الـ **corpus** بتاعنا **MIRACL Arabic** — 2 مليون passage من ويكيبيديا العربية.
>
> والـ **retriever** — وهنا في نوعين. الـ **BM25**، وده sparse، بيشتغل بالـ exact term matching.
> والـ **Dense**، وعندنا mDPR، بيحوّل الـ query لـ vector وبيفهم المعنى حتى لو الكلمات مختلفة.
> **وكل واحد فيهم بيفشل في نوع مختلف من الأسئلة** — يعني هم complementary.
>
> والقياس بتاعنا **NDCG@10**.

**On slide — written, but not all spoken:**
`Corpus → MIRACL Arabic · 2M passages · 2,896 queries · human relevance judgments`
`Retriever → BM25 · Dense · Hybrid`
`Metric → NDCG@10`

> The queries count and the human-judgments line stay on the slide and out of your mouth, as you
> asked. The panel reads them while you talk about the retrievers.

**Visual:** redraw thesis Figure 3.1 with the **QE layer removed**. The retriever is **one single
box** labelled `Retriever`, with the three names listed underneath as plain text — `BM25` · `Dense` ·
`Hybrid`. **No parallel branches, no fusion box, no hybrid drawn.** Hybrid is only a word on a list
here; it becomes a decision later, in Osman's half, which is where it earns its reveal.

The two retrieval types get explained in the middle of this slide, briefly, as you wanted — not as a
separate theory beat before it.

---

## Slide 11 · Baseline results, and what they pointed at — 30s

*(deletions applied: "matched the official number exactly", "96% of the official", the 1-in-10 /
recall-ceiling sentence, and "كلمة لتلاتة كلمات" are all gone)*

> وأول حاجة عملناها: **أعدنا إنتاج النتائج المنشورة بالظبط** — عشان نتأكد إنو الـ pipeline بتاعنا
> صاح، وإنو أي تحسّن بعد داك يكون بسببنا إحنا، مش بسبب اختلاف في الـ setup. الـ **mDPR** جاب
> **0.4993**، والـ **BM25** جاب **0.4621**.
>
> وقبل ما نختار تقنية، عملنا **error analysis** على الـ baseline. لقينا **34%** من الكويريز فاشلة
> تماماً. والأهم: **الكويريز القصيرة أداءها أضعف بشكل واضح — 0.345**.
>
> والسبب هو الـ **information poverty**: كلمتين ما بيدّوا الـ retriever معلومات كافية وسط 2 مليون
> passage. يعني **العطل في الـ query ذاتها**.
>
> والتشخيص ده هو اللي حدّد لينا التقنية. لو المشكلة إنو السؤال فقير في المعلومات، فالحل لازم
> **يزوّد** السؤال معلومات — قبل ما يوصل للـ retriever. وعشان كده اخترنا الـ **Query Expansion** كـ
> QE technique بتاعتنا: من كل العائلة اللي شفناها في الـ taxonomy، دي هي اللي بتعالج المشكلة اللي
> قسناها بالظبط.

**On slide:** `Reproduced the published baselines` · `mDPR 0.4993` · `BM25S 0.4621` ·
`34% of queries fail` · `Short queries: 0.345`
**Visual:** stat tiles, with the `0.345` tile in the warning accent and visually largest — it is the
number that selected the technique. No chart. `fig_4_3_length_box_v1.png` goes on a backup slide.

> **The reproduction claim is back in, as you asked** — and it does real work here: it is the answer
> to *"how do we know your implementation is correct?"*, delivered before anyone asks it. Keep the
> precise figures on your Q&A sheet: mDPR matched the published MIRACL value exactly, BM25S reached
> 96% of Pyserini, the 4% gap being BM25S vs Pyserini's Java implementation.

---

## Slide 12 · Query2Doc — the technique — 30s

*(the QE layer enters the diagram · constraint sentence deleted)*

> بناءً على التحليل ده، دخلنا في السستم **layer** جديدة: الـ **Query Enhancement**، وركّزنا على تقنية
> **Query2Doc**.
>
> وهنا في نقطة جميلة: كلنا عارفين إنو الـ LLMs بتعاني من الهلوسة — لكن في التقنية دي، **الهلوسة ما
> مشكلة، هي ذاتها الحل**. بنطلب من الموديل يولّد **hypothetical document**. المعلومات فيهو ممكن تكون
> غلط، لكن الستايل والـ vocabulary قريبة من الدوكيومنتات الحقيقية — فبتقرّب المسافة اللغوية.
>
> ونرجع لمثالنا: الكويري بقت تحمل الـ vocabulary بتاع اللائحة نفسها — فالـ passage الصح رجع.

**On slide:** `Query → LLM writes a hypothetical answer → Query + pseudo-doc → Retriever`
Prompt visible in a corner, **not read aloud**.

**Visual — two parts.** Upper strip: the same pipeline, QE layer now **solid** and enlarged,
everything else shrunk and faded. That is the expand-one-component beat from your Part 2 draft.

Lower two-thirds: **the structural argument, made visible** — three text cards, and the shapes carry
the meaning.

| Card | Content | Styling |
|---|---|---|
| **1 · الـ query** | «ما الشروط التي تسمح للطالب بـ**تأجيل دراسته** في جامعة الخرطوم؟» | narrow, short, question mark, **different shape and colour** from the others |
| **2 · النص في الـ corpus** | «يجوز للطالب المقيّد التقدّم بطلب **إيقاف القيد** وفق الشروط الواردة في اللائحة…» | wide paragraph block, administrative register |
| **3 · الـ pseudo-document** | «يجوز للطالب التقدّم بطلب **إيقاف القيد** أو **تأجيل الدراسة** وفق شروط تحدّدها اللوائح…» | **identical shape and colour to card 2** |

Then highlight the two key terms in two different colours across all three cards:

- **«تأجيل الدراسة»** appears in card 1 and card 3 — **not** in card 2
- **«إيقاف القيد»** appears in card 2 and card 3 — **not** in card 1

So card 1 and card 2 share **no** highlighted term — that is why retrieval failed on slide 5. Card 3
carries **both** — that is the bridge. And card 3 is drawn the same shape as card 2 because the
pseudo-document imitates the register of the corpus, which is exactly the mechanism.

Draw a faint connector from card 1 to card 2 marked ✗, and from card 3 to card 2 marked ✓.

> ⚠️ The regulation wording above is **plausible administrative Arabic that I wrote**, not quoted from
> the real UofK regulations. Either check it against the actual text or keep it generic — and assert
> no durations, numbers, or conditions. «إيقاف القيد» vs «تأجيل الدراسة» is the right kind of
> mismatch for this panel, but do not present the sentence as a real quotation.

---

## Slide 13 · The impact — dense vs BM25 — 35s

> وعشان نتأكد إنو التقنية دي **بتعمّم** — يعني مش مرتبطة بموديل واحد بعينو — عملنا **comparison** بين
> عشرة موديلات، من 2B لـ 8B، بنفس البرومبت ونفس الـ pipeline.
>
> على الـ **Dense** — زي ما شايفين على اليسار — كل الموديلات التسعة اتحسّنت فوق الـ baseline. أحسنها
> **Aya Expanse** بـ **+23.5%**.
>
> لكن على الـ **BM25** — على اليمين — **ستة من تسعة** بقى أداءها **أسوأ** من الـ baseline ذاتو.
>
> نفس التقنية، نفس النص المولّد، **retriever اتنين — ونتيجتين في اتجاهين متعاكسين**.

**On slide:** two charts side by side, one caption: `Same expansion. Opposite effect.`
**Visual — use the real rendered charts, do not redraw:**
- Left: `thesis_figures/output/png/fig_4_5_models_bar_v1.png` (thesis Figure 4.3, dense)
- Right: `thesis_figures/output/png/fig_4_5b_models_bar_bm25_v1.png` — **newly generated**, same
  script style, same per-model colours, same dashed-baseline design

The BM25 chart did not exist — Chapter 4 reports that sweep as Table 4.6 only. Generated from
`model_comparison_bm25.csv` via `thesis_figures/gen_fig_bm25_bar.py`, column `n1_ndcg10` (no
repetition — the repetition fix is the next slide's story). Verified: 3 above baseline, 6 below,
matching Table 4.6.

Side by side, the dashed line sits **below every bar** on the left and **cuts through the bars** on
the right. That is the entire finding, and it needs no words.

> ⚠️ **Do not let the image model draw these charts.** It will invent bar heights that look plausible
> and are wrong. Composite the two real PNGs into the generated slide, or generate the slide with
> empty chart areas and drop the PNGs in afterwards.

---

## Slide 14 · Query repetition, and the finding — 30s

> ولما فتّشنا في السبب لقيناهو الـ **term dilution**: الـ BM25 بيحسب بالـ term overlap، فلما تضيف
> تمانين كلمة مولّدة على سؤال من أربع كلمات، الكلمات الأصلية — اللي حاملة المعنى — وزنها بيضيع.
>
> فمعالجتنا للمشكلة دي كانت الـ **query repetition**: نكرّر السؤال الأصلي جوّه الكويري الموسّعة عشان
> نرجّع ليهو وزنو في المعادلة.
>
> وما وقفنا عند كده — عملنا **sweep** على معامل التكرار لكل موديل من التسعة. ولقينا إنو الـ optimum
> **بيختلف من موديل لموديل**: أقوى موديلين عربياً وصلوا لأحسن أداء بالـ **adaptive repetition**،
> والباقي بقيمة **ثابتة** بين خمسة وعشرة.
>
> والنتيجة: **كل الموديلات التسعة بقت فوق الـ baseline**. وأحسن نتيجة **Aya بـ 0.5855**.

**On slide:** `Term dilution → query repetition` · `Optimum is model-dependent` · `9/9 above baseline` ·
`Aya 0.5855`
**Visual:** `fig_4_7_repetition_v1.png` from the thesis, restyled. Same warning as slide 13 — real
chart, not AI-drawn.

> **"الحل كان بسيط" is gone**, and the repetition sweep is in instead. That sweep *is* objective 6 —
> nine models, each with its own optimum, adaptive vs fixed — and stating it is the difference
> between a trick you tried and a result you established. Never describe your own finding as simple;
> the panel will take the description at face value.

### Handover
> وهنا أسلّم الكلام لزميلي عثمان. اتفضل يا عثمان.

---

## One thing Osman needs to know

Deleting the closing lines of slide 14 removed the **plant** — *"same technique, two retrievers, one
helped and one harmed, this comes back at the end"*. That is fine, because slide 13 already states
the split out loud and repeating it a minute later was redundant.

But the payoff still needs its setup. **Osman's placement slide must point back explicitly**, e.g.
*"ودي نفس الـ asymmetry اللي شفناها في الـ Query2Doc — كانت موجودة من البداية، بس ما كنا فاهمينها."*
Without that callback the placement finding arrives as a new fact rather than a resolved thread.

---

## Two things I dropped, and why

**The single-model beat** — *"طبقنا الفكرة أول مرة بموديل واحد، ولقينا تحسن واضح"*. It is factually
wrong (Qwen 2.5 3B was dense **+8.9%** but BM25 **−11.5%**, Tables 4.3 and 4.4), and now that
slide 13 shows all nine models on both retrievers it is also redundant. Gone rather than corrected.

**The constraint sentence** — deleted as you asked. Note that objective 3 on slide 9 still carries
"freely available cloud GPUs", so the constraint is on the record without costing you the seconds.

---

## Timing

| # | Slide | s | Cum. |
|---|---|---|---|
| 1 | Title | 15 | 0:15 |
| 2 | Agenda | 10 | 0:25 |
| 3 | LLMs + example | 30 | 0:55 |
| 4 | RAG & librarian | 25 | 1:20 |
| 5 | Bottleneck | 25 | 1:45 |
| 6 | QE rich / Arabic empty | 25 | 2:10 |
| 7 | Arabic challenges | 20 | 2:30 |
| 8 | Research question | 20 | 2:50 |
| 9 | Objectives | 20 | 3:10 |
| 10 | The system we built | 40 | 3:50 |
| 11 | Baseline results | 40 | 4:30 |
| 12 | Query2Doc + the example | 35 | 5:05 |
| 13 | Dense vs BM25 | 35 | 5:40 |
| 14 | Repetition + the sweep | 35 | **6:15** |

**Mohammed: 6:15.** Osman's half as currently scoped is ~4:40 (الأسماء الخمسة 60 · CSQE 65 ·
placement 70 · results 45 · conclusion 40).

### ⚠️ Total ≈ 10:55 against a 10:00 slot — and it grew this round

Rev 3 added ~20s: the reproduction claim, the expanded technique justification, the generalisation
line, and the repetition sweep. Every one of them was the right call — they are all substance, and
three of them defend against likely questions. But they are not free.

**You are now ~55 seconds over, and the split is 6:15 / 4:40.**

Two ways out, and they solve different problems:

1. **Hand over after slide 12.** You end at 5:05, Osman runs 5:50. Fixes the balance, not the total.
2. **Take 55s out of the intro block (slides 3–9, currently 3:10).** That block is 30% of the talk
   and it is all setup. Slides 4 and 5 at 25s each can go to 20; slide 6 to 20; slide 3 to 25.
   That is −25s. The rest has to come from Osman's half.

**My call: do both — hand over after 12, and trim slides 3–6 by 25s.** That lands you at ~4:40 and
Osman at ~5:50, total ~10:30, with the intro no longer eating a third of the slot. Dr. Tahani's
warning in Note 9 is specifically about this: the setup expanding until the results get rushed.
