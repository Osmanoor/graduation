# النص النهائي — مناقشة مشروع التخرج

**تحسين جودة الاسترجاع في أنظمة RAG العربية باستخدام Query Enhancement**  
محمد الحاج · عثمان بشير — إشراف د. تهاني عبدالله

> هذا هو النص الذي يُقرأ منه. الأسطر العادية = ما تقوله. الأسطر المائلة = توجيه أداء، لا تُقرأ.

**محمد: الشرائح ١–١٤ · ٥:٠٣** &nbsp;&nbsp;|&nbsp;&nbsp; **عثمان: الشرائح ١٥–٢٢ · ٤:٣٢** &nbsp;&nbsp;|&nbsp;&nbsp; **المجموع ٩:٣٥**

---

# محمد الحاج

## شريحة 1 · Title — 15s

السلام عليكم ورحمة الله وبركاته. حضورنا الكرام، الدكاترة الأعزاء.

أنا محمد الحاج، ومعاي زميلي عثمان بشير. أطروحتنا اليوم بعنوان: Improving Arabic RAG Retrieval Quality with LLM-based Query Enhancement — بإشراف الدكتورة تهاني عبدالله.

*Say the title in English, as printed. Previously the script gave an Arabic rendering while the slide showed English — you would have been reading one thing with another on screen.*

---

## شريحة 2 · Agenda — 12s

ودي محاور العرض: نبدأ بالـ introduction، بعدها المشكلة والسؤال البحثي، ثم الأهداف، بعدها الـ methodology والشغل اللي عملناه، ثم النتائج والمناقشة، ونختم بالـ conclusion والعمل المستقبلي.

*Six items, one breath. Do not elaborate on any of them — you are about to explain all six.*

---

## شريحة 3 · LLMs and their limitation — 30s

الـ Large Language Models — زي ChatGPT و Claude و Gemini — بقت أدوات قوية جداً في توليد النصوص والإجابة على الأسئلة.

لكن عندها limitation أساسي: الـ memory بتاعتها parametric — المعرفة كلها مخزّنة جوّه الـ weights ومجمّدة عند لحظة التدريب. ولو الداتا اتغيّرت أو كانت داتا خاصة، الـ retraining مكلف جداً.

خلّونا نشوف مثال. لو سألنا الموديل: «ما الشروط التي تسمح للطالب بتأجيل دراسته في جامعة الخرطوم؟»

لوائح الجامعة ما موجودة في البيانات اللي اتدرّب عليها. ومع ذلك ما بيقول ليك «ما عارف» — بيجاوب. وشوفوا الإجابة: مادة رقم ١٢، ولائحة سنة ١٩٩٨، ورسوم ٥٠٠ جنيه. كل ده مُختلَق. ما في مادة زي دي ولا رسوم زي دي. بس الإجابة مكتوبة بثقة وبصياغة سليمة. ودي الـ hallucination.

---

## شريحة 4 · RAG and the librarian — 13s

عشان كده ظهر الـ RAG: بدل ما نعيد تدريب الموديل، بندّي ليهو knowledge base يفتّش فيها.

زي المكتبة بالظبط — أمين المكتبة ما بيجاوب من ذاكرتو، بيمشي يجيب الكتب، والإجابة بتتكتب منها.

*The slide already shows all four scenes. Do not walk them one by one.*

---

## شريحة 5 · Retrieval is the bottleneck — 17s

طيب — لو حطّينا لوائح الجامعة جوّه الـ RAG system، الإجابة بقت موجودة في الـ corpus. ومع ذلك ممكن النظام يرجع بـ passages غلط، فالإجابة تفضل غلط.

يعني الـ bottleneck هنا، في الـ Information Retrieval. ودي اللي دفعتنا ندرس الـ techniques اللي بتحسّنو.

*The fork diagram *is* the correct-versus-wrong sentence. Do not say it as well.*

---

## شريحة 6 · Rich in English, unvalidated in Arabic — 25s

فمشينا للـ literature. ولقينا إنو في اللغة الإنجليزية ده مجال غني جداً ومدروس كويس — الـ Query Enhancement: نصلّح الـ query قبل ما توصل للـ retriever، من غير ما نلمس الـ retriever ومن غير ما نعيد فهرسة الـ corpus. عائلة كاملة من التقنيات — Query2Doc، HyDE، GRF.

طيب — ومشينا نشوف الـ literature العربي. ولا واحدة من التقنيات دي اتعملت ليها validation على العربي. ولا في حد أثبت إنها بتشتغل بموديلات صغيرة كفاية إنو مجموعة زينا تقدر تشغّلها.

*"Almost nothing" is gone from the slide and the script. It undercut you. The claim is now the precise one Chapter 2 actually makes — *not one validated for Arabic* — which is stronger *and* defensible, because the gap you are claiming is a validation gap, not an absence of all work.*

---

## شريحة 7 · But Arabic is not English — 10s

والعربي عندو تحدياتو الخاصة: الاشتقاق، والإملاء، والتشكيل، والازدواجية اللغوية. وزي ما شايفين في الأمثلة، كلها بتكسر المطابقة بين السؤال والدوكيومنت.

Name the four and stop. Do not read كتب / كاتب / مكتوب aloud — the panel are Arabic speakers and they read the examples faster than you can say them.

---

## شريحة 8 · Research question — 20s

فالـ research question بتاعنا: إلى أي مدى الـ LLM-based Query Enhancement بتقدر تحسّن الـ Arabic Information Retrieval — عبر الـ sparse والـ dense والـ hybrid — باستخدام موديلات مفتوحة من 2 لـ 8 مليار باراميتر؟

وأبعد من الـ validation — وده الـ contribution الخاص بينا — دايرين نعرف: كيف الـ retrievers المختلفة بتتفاعل مع الـ Query Enhancement؟

---

## شريحة 9 · Objectives — 18s

وعشان نجاوب على السؤال ده حدّدنا تسعة objectives. باختصار شديد: نبني الـ baselines ونحلّل فشلها، نكيّف الـ Query2Doc للعربي ونقارن عشرة موديلات، ونشوف الـ sparse والـ dense بيتفاعلوا معاها كيف، ونعالج الـ term dilution، ونبني hybrid baseline، ونطبّق الـ CSQE، وأخيراً نحدّد المكان الأمثل للـ expansion جوّه الـ pipeline.

والتفاصيل قدامكم على الشاشة.

*One breath, no pauses between items. The nine are printed in full — let them read.*

---

## شريحة 10 · The system we built — 40s

وبدينا بأول objective: نبني الـ baseline. ودي المنظومة اللي بنيناها.

الـ corpus بتاعنا MIRACL Arabic — 2 مليون passage من ويكيبيديا العربية.

والـ retriever — وهنا في نوعين. الـ BM25، وده sparse، بيشتغل بالـ exact term matching. والـ Dense، وعندنا mDPR، بيحوّل الـ query لـ vector وبيفهم المعنى حتى لو الكلمات مختلفة. وكل واحد فيهم بيفشل في نوع مختلف من الأسئلة — يعني هم complementary.

والقياس بتاعنا NDCG@10.

---

## شريحة 11 · Baseline results — 30s

وأول حاجة، أعدنا إنتاج النتائج المنشورة بالظبط — عشان أي تحسّن بعد داك يكون بسببنا إحنا. الـ mDPR جاب 0.4993، والـ BM25 جاب 0.4621.

بعدها عملنا error analysis. لقينا 34% من الكويريز فاشلة تماماً. والأهم: الكويريز القصيرة أداءها أضعف بشكل واضح — 0.345. والسبب هو الـ information poverty.

يعني العطل في الـ query ذاتها. وعشان كده اخترنا الـ Query Expansion كـ QE technique بتاعتنا.

*This is the only place the technique choice is stated. It used to be said here *and* on slide 12 — the same justification twice, thirty seconds apart.*

---

## شريحة 12 · Query2Doc — 25s

والفكرة في الـ Query2Doc فيها حاجة ظريفة: كلنا عارفين إنو الـ LLMs بتهلوس — لكن هنا الهلوسة مش مشكلة، هي ذاتها الحل.

بنطلب من الموديل يولّد hypothetical document. وده الـ prompt الاستخدمناهو — بسيط جداً، zero-shot، من غير أي أمثلة.

المعلومات في النص ده ممكن تكون غلط تماماً — لكن الـ vocabulary بتاعو قريب من الدوكيومنتات الحقيقية، فبتقرّب المسافة اللغوية بين السؤال والإجابة.

*Opens on the mechanism, not on the diagnosis. The UofK example is gone from this slide — it was doing the same job twice and cluttering the layout. The Query2Doc figure and the real system prompt now carry it.*

---

## شريحة 13 · Dense vs BM25 — 25s

وعشان نتأكد إنو التقنية بتعمّم، عملنا comparison بين عشرة موديلات، من 2B لـ 8B، بنفس البرومبت ونفس الـ pipeline.

على الـ Dense، الموديلات التسعة كلها اتحسّنت — أحسنها Aya Expanse بـ +23.5%. لكن على الـ BM25، ستة من تسعة بقى أداءها أسوأ من الـ baseline ذاتو.

نفس التقنية، نفس النص المولّد — ونتيجتين في اتجاهين متعاكسين.

Cut «زي ما شايفين على اليسار» and «على اليمين». They can see. Say the finding, not the reading.

---

## شريحة 14 · Query repetition — 23s

ولما فتّشنا في السبب لقيناهو الـ term dilution: لما تضيف تمانين كلمة مولّدة على سؤال من أربع كلمات، الكلمات الأصلية وزنها بيضيع.

فمعالجتنا كانت الـ query repetition — نكرّر الكويري الأصلية جوّه الكويري الموسّعة. وعملنا sweep على معامل التكرار لكل موديل، والـ optimum طلع بيختلف من موديل لموديل.

والنتيجة: كل الموديلات التسعة بقت فوق الـ baseline، وأحسن نتيجة Aya بـ 0.5855.

*The adaptive-versus-fixed detail and the β=2 / n=5–10 numbers are Q&A material. They are on your sheet, not in the talk.*

**التسليم:** وهنا أسلّم الكلام لزميلي عثمان. اتفضل يا عثمان.

---

# عثمان بشير

## شريحة 15 · Where expansion breaks — 50s

شكراً محمد. طيب عشان نشوف الـ expansion بيفشل وين، خدوا معاي المثال ده: «ما هي الأسماء الخمسة في اللغة العربية؟» — دي قاعدة نحوية مشهورة، والإجابة أب، أخ، حم، فو، ذو.

والـ BM25 العادي، بالكويري الأصلية، لقى المقال الصح في المرتبة الأولى — بنتيجة 1.000.

لكن لما ودّينا للموديل يعمل expansion، قال ليك بثقة: «فئة خاصة من الأسماء الأكثر شيوعاً: محمد، آدم، إبراهيم، إسماعيل» — أسماء أشخاص!

فالأسماء المهلوسة دي اشتغلت كـ noise — ودّت البحث في اتجاه غلط تماماً. والمقال الصح ما فيهو ولا واحدة من الكلمات دي. النتيجة نزلت من 1.000 لـ 0.000.

ودي وصّلتنا للفكرة المفتاحية: الـ expansion ما المفروض تعتمد على ذاكرة الموديل — لازم تكون grounded في الـ corpus ذاتو.

---

## شريحة 16 · CSQE — 45s

ودي فكرة الـ CSQE — Corpus-Steered Query Expansion: بدل ما الموديل يعتمد على ذاكرته، يجاوب من الـ corpus.

فبنبني الكويري النهائية من تلاتة components: أولاً — BM25 first pass بالكويري الأصلية، بنجيب top-5 documents، وبنقول للموديل: استخرج الجمل المفتاحية من الدوكيومنتات دي. معلومات موجودة فعلاً في الـ corpus، مش هلوسة. ثانياً — بنضيف اتنين blind expansions للـ vocabulary enrichment. وثالثاً — بنكرّر الكويري الأصلية أربع مرات.

ونرجع لسؤالنا: الـ first pass رجّع المقال الصح، وفيهو أب، أخ، حم، فو، ذو. فالـ expansion هسي شايلة الكلام الصح — مش لأنو الموديل عرفو، لكن لأنو اتنسخ من دوكيومنت موجود. النتيجة رجعت 1.000.

وعلى كل الـ dataset: الـ BM25 مع CSQE قفز من 0.4621 لـ 0.6157.

---

## شريحة 17 · The contribution — 62s

طيب. الـ BM25 والـ Dense بيفشلوا في أسئلة مختلفة — فجرّبنا ندمجهم في نظام hybrid، من غير أي enhancement. النتيجة 0.6267.

وبعدين جينا ندمج الـ CSQE مع الـ hybrid. والسؤال: منو فيهم ياخد الكويري الموسّعة؟ جرّبنا التلاتة configurations.

لو أدّيت الاتنين — 0.6936. لو أدّيت الـ Dense بس — 0.6474. لكن لو أدّيت الـ BM25 بس، وخلّيت الـ Dense على الكويري الأصلية — 0.7137.

ودي المعمارية النهائية اللي على اليمين: الكويري الموسّعة بتمشي للـ BM25، والكويري الأصلية بتمشي للـ mDPR، والاتنين بيتدمجوا بالـ RRF.

نفس التقنية، نفس الـ hybrid، نفس الموديل. المتغيّر الوحيد منو استلم الـ expansion.

وليه؟ الـ hybrid بيستفيد من الاختلاف بين الطريقتين. لو الاتنين شالوا نفس الكويري، بيتقاربوا — والـ complementarity اللي دمجنا عشانها بتضيع.

فالمبدأ: كل retriever محتاج الـ query representation البتخصو. وحسب مراجعتنا لليتريتشر، الـ asymmetric assignment ده ما اتدرس قبل كده.

---

## شريحة 18 · The full journey — 40s

دي wrap-up للـ progression بتاع الإكسبيرمنتس، وبتوضّح المنهجية العلمية اللي كنا محافظين عليها: بنحلّل الـ current system عشان نحدّد الـ weaknesses، ونبتكر ليها حل، ومن ثمّ نقيس النتيجة، ونرجع تاني من الأول — loop مستمر لحدي ما نصل لأحسن نتيجة ممكنة.

بدأنا بالـ baseline، وحلّلنا مشكلة الـ short queries، وعملنا ليها query expansion. ولما ظهرت مشكلة الـ term dilution، حليناها بالـ query repetition. وواجهتنا مشكلة الـ hallucination، وحليناها بالـ corpus-steered query expansion.

والسيستم النهائي — hybrid بيدمج BM25 بالـ Corpus-Steered Expansion مع Dense بالكويري الأصلية — أدّانا 0.7137: أحسن من الـ baseline بـ 54.5%، وتفوّق على الـ hybrid اللي بدون query expansion بـ 13.9%.

والأهم إنو الـ short queries — اللي كانت أول مشكلة واجهتنا — لقيناها اتحسّنت بـ 43.6%.

---

## شريحة 19 · All four metrics — 10s

وكل الأرقام اللي عرضناها كانت NDCG@10 — لكن قسنا أربع metrics، والسيستم النهائي بتاعنا هو الأعلى في الأربعة.

*Say *"highest on all four"* — not *"the trend is consistent everywhere"*. At baseline BM25S beats mDPR on Recall@100 (0.8577 vs 0.8407), and a clean-ordering claim contradicts that cell.*

---

## شريحة 20 · Conclusions — 35s

أسّسنا الـ baselines وحلّلناها … قارنّا عشرة موديلات مفتوحة … لقينا الـ dense والـ sparse بيتفاعلوا مع الـ QE بصورة مختلفة … الـ query repetition عالجت الـ degradation في الـ sparse … الـ corpus grounding اتأكّد … والـ retriever-specific query representation — ودي الأهم فيهم.

ودي مساهمتنا: إحنا شغّالين في موضوع حيّ جداً هسي — الـ RAG هو الطريقة اللي بتُبنى بيها أنظمة الـ LLM دلوقتي، والعربي مهمَّش فيهو. فقدّمنا أول validation منهجي للـ LLM-based query enhancement في الـ Arabic IR، بعشرة موديلات مفتوحة، على hardware مجاني — يعني قابل للتكرار من أي مجموعة بحثية عربية.

وأهم finding عندنا — الـ asymmetric placement — إحنا قاعدين نكتب فيهو ورقة علمية هسي.

*As a conclusion —*

**[Then the six, briskly. One breath, no elaboration between them:]**

*The "not Arabic-specific / term dilution is a BM25 property" passage is cut, as you asked. The seven conclusions stay printed on the slide.*

---

## شريحة 21 · Future work — 20s

للمستقبل، داير نغطّي الـ dialectal Arabic، ونعمل first-pass quality gate، ونجرّب embedding models أقوى.

---

## شريحة 22 · Thanks — 10s

شكراً جزيلاً لحسن استماعكم — وجاهزين لأسئلتكم.

---

# للأسئلة — نقاط محفوظة خارج العرض

- معامل التكرار الأمثل لكل موديل: adaptive β=2 لأقوى موديلين، وثابت n=5–10 للباقي

- الـ CSQE component ablation: corpus-only 0.5381 · blind-only 0.5752 · mixed 0.6157

- أقرب شغل سابق: Exp4Fuse (Liu et al., ACL 2025 Findings) — QE على sparse retriever واحد ثم fusion

- الـ mDPR طابق الرقم المنشور بالظبط، والـ BM25S وصل 96% من Pyserini

- الأرقام الستة: 0.4621 · 0.4993 · 0.6267 · 0.7137 · +54.5% · 56.8%
