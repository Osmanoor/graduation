# F8 · Osman's half — content (slides 15 → 22)

**Built from:** Osman's draft + Mohammed's change list, 2026-08-15.
**Script language:** Arabish, matching Mohammed's half in [F7](F7_intro_content_final.md).
**Applied:** no "term dilution" on the الأسماء الخمسة slide · ablation dropped from the talk ·
hybrid framing softened · new progression script · four-metric table added · conclusions on their own
slide · limitations dropped · thanks slide added.

---

## Slide 15 · Where blind expansion breaks — 50s

> شكراً محمد. طيب عشان نشوف الـ **expansion** بيفشل وين، خدوا معاي المثال ده:
> **«ما هي الأسماء الخمسة في اللغة العربية؟»** — دي قاعدة نحوية مشهورة، والإجابة **أب، أخ، حم، فو، ذو**.
>
> والـ BM25 العادي، بالكويري الأصلية، لقى المقال الصح في **المرتبة الأولى** — بنتيجة **1.000**.
>
> لكن لما ودّينا للموديل يعمل **expansion**، قال ليك بثقة: «فئة خاصة من الأسماء الأكثر شيوعاً:
> **محمد، آدم، إبراهيم، إسماعيل**» — أسماء أشخاص!
>
> فالأسماء المهلوسة دي اشتغلت كـ **noise** — ودّت البحث في اتجاه غلط تماماً، ناحية مقالات عن رجال
> اسمهم محمد وآدم. والمقال الصح، بتاع النحو، ما فيهو ولا واحدة من الكلمات دي.
>
> النتيجة نزلت من **1.000** لـ **0.000**.
>
> ودي وصّلتنا للفكرة المفتاحية: الـ expansion **ما المفروض تعتمد على ذاكرة الموديل** — لازم تكون
> **grounded** في الـ corpus ذاتو.

**On slide:** the Arabic query · the model's real output · `1.000 → 0.000`
**Visual:** query at the top, large. Beneath it two cards side by side — left, the generated names in
the warning accent with an ✗; right, the correct grammar article greyed out with a caption
«ما رجع أبداً». The `1.000 → 0.000` transition set large at the bottom.

> **"Term dilution" is gone**, as you asked — you already told the panel you solved that with query
> repetition, so re-raising it here would read as the fix not working. **Noise pulling the search in
> the wrong direction** is the right description and it is a different mechanism: dilution is about
> the original terms losing *weight*, this is about generated terms actively pointing *elsewhere*.
>
> **"Blind" is gone too**, and the closing line now reads *"expansion must not rely on the model's
> memory — it must be grounded in the corpus"*. That is better than the earlier version: you have
> never used the word "blind" with this panel, so introducing it here as a label for what you did
> would land as jargon. Ending on **memory vs corpus** also hands straight into slide 16's new
> opening line.
>
> **Do not put the corpus-grounded answer on this slide.** It is slide 16's reveal.

---

## Slide 16 · CSQE — 45s

> ودي فكرة الـ **CSQE — Corpus-Steered Query Expansion**: **بدل ما الموديل يعتمد على ذاكرته، يجاوب
> من الـ corpus**.
>
> فبنبني الكويري النهائية من **تلاتة components**:
>
> **أولاً** — BM25 first pass بالكويري الأصلية، بنجيب **top-5 documents**، وبنقول للموديل: استخرج
> الجمل المفتاحية من الدوكيومنتات دي. يعني معلومات **موجودة فعلاً في الـ corpus**، مش هلوسة.
>
> **ثانياً** — بنضيف **اتنين blind expansions** للـ vocabulary enrichment.
>
> **وثالثاً** — بنكرّر الكويري الأصلية **أربع مرات**.
>
> ونرجع لسؤالنا: الـ first pass رجّع المقال الصح، وفيهو **أب، أخ، حم، فو، ذو**. فالـ expansion هسي
> شايلة الكلام الصح — **مش لأنو الموديل عرفو، لكن لأنو اتنسخ من دوكيومنت موجود**. النتيجة رجعت **1.000**.
>
> والنتيجة على كل الـ dataset: الـ BM25 مع CSQE قفز من **0.4621** لـ **0.6157**.

**On slide:** the three components stacked · the grounded Arabic sentence · `0.4621 → 0.6157`
**Visual:** the final query built as three stacked bands — `corpus sentences` (teal, largest) ·
`2 blind expansions` (mid) · `original query × 4` (small, repeated four times so the repetition is
visible). Beside it, the grounded sentence with **أب، أخ، حم، فو، ذو** highlighted.

> **Ablation dropped from the talk**, as you asked. Keep 0.5381 / 0.5752 / 0.6157 on a backup slide —
> *"why not corpus-only?"* is a likely question and it has a one-line answer.

---

## Slide 17 · Fusion and placement — the contribution — 70s

> طيب. الـ BM25 والـ Dense بيفشلوا في أسئلة مختلفة — فجرّبنا **ندمجهم** في نظام **hybrid**، من غير
> أي enhancement. النتيجة **0.6267**.
>
> وبعدين جينا ندمج الـ **CSQE** مع الـ hybrid. والسؤال هنا: **منو فيهم ياخد الكويري الموسّعة؟**
> جرّبنا التلاتة configurations.
>
> لو أدّيت **الاتنين** — بتجيب **0.6936**.
> لو أدّيت الـ **Dense** بس — **0.6474**.
> لكن لو أدّيت الـ **BM25 بس**، وخلّيت الـ Dense على الكويري الأصلية — بتجيب **0.7137**.
>
> نفس التقنية، نفس الـ hybrid، نفس الموديل. **المتغيّر الوحيد منو استلم الـ expansion.**
>
> وليه؟ الـ **hybrid بيستفيد من الاختلاف** بين الطريقتين — قيمتهم كلها إنهم بيفشلوا في أسئلة مختلفة.
> لو الاتنين شالوا نفس الكويري الموسّعة، بيتقاربوا، وبيبدوا يرجّعوا نفس الدوكيومنتات ويغلطوا نفس
> الغلطات — و**الـ complementarity اللي دمجنا عشانها بتضيع**.
>
> فالمبدأ: **كل retriever محتاج الـ query representation البتخصو.**
>
> وحسب مراجعتنا لليتريتشر — الـ **asymmetric assignment** للـ expansion عبر **أنواع** مختلفة من الـ
> retrievers جوّه hybrid dense–sparse، ده **ما اتدرس قبل كده**.

**On slide:** four rows — `No QE (fusion only) 0.6267` · `Dense-expanded 0.6474` ·
`Both expanded 0.6936` · `**BM25-only 0.7137**`
**Visual:** the four rows as a bar or table, the winning row in full gradient. Beneath:
`Each retriever needs its own query format.`

> **Changes applied.** «خلينا نحدد البار الصح» is gone — you now just state the hybrid result.
> «ودي بقت الـ baseline الحقيقية» is gone, since it retroactively demoted every comparison made
> before it. **RRF → hybrid** throughout. The Query2Doc callback is out. The Exp4Fuse sentence is out.
>
> **The OOD explanation is also out** — *"mDPR is trained on short queries so expanded queries are
> out-of-distribution"* is not tested anywhere in the thesis, and *"did you measure that?"* has no
> good answer. The complementarity explanation is the one Chapter 5 actually supports.
>
> ⚠️ **Exp4Fuse must stay on your Q&A sheet.** The spoken claim is now narrow enough to match
> `chapter2.tex:410` — *asymmetric assignment across retriever types in a dense–sparse hybrid* — so
> it is defensible as stated. But your own §2.5.4 cites Exp4Fuse (Liu et al., ACL 2025 Findings) as
> the closest prior art. If anyone asks *"is this actually new?"*, name it yourself and then give the
> narrow claim. Being shown your own citation is much worse than volunteering it.

---

## Slide 18 · The full journey — 40s

*(your new draft — kept in your wording)*

> دي **wrap-up** للـ progression بتاع الإكسبيرمنتس اللي اشتغلناها، وبتوضّح **المنهجية العلمية** اللي
> كنا محافظين عليها طول التجارب: إننا **بنحلّل الـ current system** عشان نحدّد الـ weaknesses، ونبتكر
> ليها حل، ومن ثمّ **نقيس** النتيجة، ونرجع تاني من الأول — ونتابع كده في **loop مستمر** لحدي ما نصل
> لأحسن نتيجة ممكنة.
>
> بدأنا بالـ **baseline**، وحلّلنا مشكلة الـ **short queries**، وعملنا ليها **query expansion**.
> ولما ظهرت لينا مشكلة الـ **term dilution**، حليناها بالـ **query repetition**. وكمان واجهتنا مشكلة
> الـ **hallucination**، وحليناها بالـ **corpus-steered query expansion**.
>
> والسيستم النهائي بتاعنا — **hybrid**، بيدمج **BM25 بالـ Corpus-Steered Expansion** مع **Dense
> بالكويري الأصلية من غير expansion** — أدّانا **0.7137**: أحسن من الـ baseline بـ **54.5%**،
> وتفوّق على الـ hybrid اللي بدون query expansion بـ **13.9%**.
>
> والأهم إنو **الـ short queries** — اللي كانت **أول مشكلة واجهتنا** — لقيناها اتحسّنت بـ **43.6%**.

**On slide:** the progression, baseline → final
**Visual:** `fig_4_11_progression_v2_annot.png` restyled, with a small **loop diagram** in the corner:
`Analyse → Identify weakness → Design a fix → Measure → ↺`. The loop is what makes this a methodology
slide rather than a scoreboard, and it is the strongest thing in your draft — the panel is grading
method as much as result.

Mark the first and last points on the progression so the eye lands on the short-query thread closing.

---

## Slide 19 · The same trend across all four metrics — 30s

> كل الأرقام اللي عرضناها كانت **NDCG@10** — لكن إحنا قسنا **أربع metrics** في كل تجربة، **والـ
> trend كان واضح في كلها**. والسيستم النهائي بتاعنا هو الأعلى في **الأربعة**.

**On slide — the table:**

| Method | NDCG@10 | Recall@10 | Recall@100 | MRR |
|---|---|---|---|---|
| BM25S alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| Blind QE → Dense | 0.6164 | 0.7256 | 0.9001 | 0.6493 |
| Blind QE + repetition → BM25 | 0.5855 | 0.7128 | 0.9300 | 0.6165 |
| Hybrid RRF, no QE | 0.6267 | 0.7597 | 0.9466 | 0.6517 |
| CSQE → BM25 | 0.6157 | 0.7447 | 0.9422 | 0.6380 |
| CSQE → Dense | 0.5915 | 0.7073 | 0.8816 | 0.6225 |
| **CSQE on BM25 + Dense raw (RRF)** | **0.7137** | **0.8363** | **0.9734** | **0.7362** |

**Visual:** clean table, final row in full gradient, best value in each column marked. No chart.

**Provenance:** all rows from Appendix B Table B.3 and Chapter 4 Tables 4.6 / 4.13 / 4.17. The
Recall@100 for the repetition row (0.9300) is Table 4.6, chapter4.tex:438 — it is not in Table B.3,
which is why B.3 alone could not carry this slide.

> ⚠️ **Say "our final system is highest on all four" — not "the trend is monotonic".** At baseline,
> BM25S beats mDPR on Recall@100 (0.8577 vs 0.8407). That is the complementarity you already
> explained, but if you claim a clean ordering everywhere, that one cell contradicts you.

---

## Slide 20 · Conclusions — 45s

> **As a conclusion** —
>
> الـ **Query Enhancement** بتنتقل للعربي بنجاح. لكن الأهم من كده: الـ findings اللي طلعنا بيها
> **ما كانت خاصة باللغة العربية** — دي **خصائص عامة** في طريقة تفاعل الـ expansion مع الـ retrievers.
>
> الـ **term dilution** خاصية في معادلة الـ BM25 نفسها، مش في العربي. والـ **complementarity collapse**
> خاصية في الـ fusion، مش في العربي. إحنا اكتشفناهم **في** العربي — لكنهم بينطبقوا على أي hybrid
> retrieval system.

*[Then the six, briskly — a beat each, no elaboration:]*

> أسّسنا الـ **baselines** وحلّلناها … قارنّا **عشرة موديلات** مفتوحة … لقينا الـ **dense والـ sparse
> بيتفاعلوا مع الـ QE بصورة مختلفة** … الـ **query repetition** عالجت الـ degradation في الـ sparse …
> الـ **corpus grounding** اتأكّد … و**الـ retriever-specific query representation** — ودي الأهم فيهم.

> ودي مساهمتنا: إحنا شغّالين في موضوع **حيّ جداً** هسي — الـ RAG هو الطريقة اللي بتُبنى بيها أنظمة
> الـ LLM دلوقتي، والعربي **مهمَّش** فيهو. فقدّمنا أول **validation منهجي** للـ LLM-based query
> enhancement في الـ Arabic IR، بعشرة موديلات مفتوحة، على hardware مجاني — يعني **قابل للتكرار** من
> أي مجموعة بحثية عربية.
>
> وأهم finding عندنا — الـ **asymmetric placement** — إحنا **قاعدين نكتب فيهو ورقة علمية** هسي.

**On slide — seven rows. You speak six of them; row 2 is read, not said.**

1. Baselines established and error-analysed — 34% of queries fail; short queries weakest at 0.345
2. Query2Doc transfers to Arabic zero-shot — +8.9% with a 3B model, beating the original paper's +2–5% with a model 58× smaller
3. Ten open LLMs compared under one protocol — all nine viable models improved dense retrieval (+3.7% to +23.5%); Aya Expanse 8B best overall
4. Dense and sparse respond **differently** to QE — dense improved 9/9, BM25 degraded for 6/9
5. Query repetition resolves sparse degradation — all nine models brought above baseline; the optimum is model-dependent
6. Corpus grounding validated — CSQE reached 0.6157 on BM25 alone; the final system 0.7137, +54.5% over BM25 and +13.9% over the no-QE hybrid
7. **Retriever-specific query representation is critical** — CSQE on BM25 only (0.7137) beat both (0.6936) and dense-only (0.6474)

**Visual:** seven numbered rows, same treatment as the objectives slide so the two read as a matched
pair — the contract on slide 9, the delivery here. Numbers in the gradient. Row 7 given extra weight.
The contribution paragraph sits beneath in a distinct band, not as another numbered row.

> **Changes applied.** «نجي للخلاصة» → **"As a conclusion"**. «التلاتة findings» → «الـ findings»,
> since the count was wrong. «أهدافنا التلاتة اتحققت» deleted. The complementarity/ablation row is
> deleted entirely — slide and script both — so nothing on this slide contradicts dropping the
> ablation earlier.
>
> **The reframing holds up.** The **mechanisms** are general (term dilution is a BM25 scoring
> property; complementarity collapse is a fusion property), while the **validation** was Arabic-only.
> Phrased that way, *"did you test other languages?"* has an honest answer — no, and the wording
> already concedes it.

---

## Slide 21 · Future work — 20s

> للمستقبل، داير نغطّي الـ **dialectal Arabic**، ونعمل **first-pass quality gate**، ونجرّب
> **embedding models** أقوى.

**On slide:** three items.
**Visual:** three forward-pointing cards in the gradient. Keep it light — this slide is a promise,
not an argument.

---

## Slide 22 · Thanks & questions — 10s

> شكراً جزيلاً لحسن استماعكم — وجاهزين لأسئلتكم.

**On slide:** `شكراً لكم` · `Questions` · both names · supervisor
**Visual:** echo the title slide's composition — the query and the document field — but now with the
beam landing cleanly on the **correct** cards. The visual answers the opening image. Nothing else on
the slide; this stays up for the whole 10 minutes of Q&A, so it must look finished.

---

## Timing

| # | Slide | s | Cum. |
|---|---|---|---|
| 15 | الأسماء الخمسة | 50 | 0:50 |
| 16 | CSQE | 45 | 1:35 |
| 17 | Fusion & placement | 70 | 2:45 |
| 18 | The full journey | 40 | 3:25 |
| 19 | Four metrics | 30 | 3:55 |
| 20 | Conclusions | 45 | 4:40 |
| 21 | Future work | 20 | 5:00 |
| 22 | Thanks | 10 | **5:10** |

**Osman: 5:10.** Mohammed: 6:15. **Total ≈ 11:25 against a 10:00 slot.**

### The cut list, in order of least damage

1. **Slide 19, the four-metric table — 30s.** It is a rigour slide, not an argument slide, and it
   answers a question nobody may ask. Move it to backup and it costs nothing narratively. *(−30s)*
2. **Mohammed's slides 3–6 — 25s.** Already identified in F7; the intro is 30% of the talk.
3. **Slide 18 to 30s.** The loop framing is the valuable part; the number recap overlaps slide 20. *(−10s)*
4. **Slide 16 to 40s.** Without the ablation it is a three-step description. *(−5s)*
5. **Mohammed's slide 11 to 30s.** The reproduction claim can be one clause, not two sentences. *(−10s)*

All five lands ~10:20 — which a real rehearsal brings home. **Do 1 and 2 at minimum**; they are 55
seconds for almost no loss.
