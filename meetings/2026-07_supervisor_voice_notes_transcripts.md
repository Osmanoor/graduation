# Supervisor Voice Notes — July 2026 (Full Transcripts)

**Source:** 16 voice notes in `recordings/`, sent by the supervisor (Dr. Tahani) to the graduation-project group. `4.ogg` is byte-identical to `3.ogg`, so 15 unique files.
**Total audio:** ~38 minutes.

## How this was produced

Every file was transcribed **twice, independently**, and the two outputs compared:

| Engine | Role | Why |
|---|---|---|
| **`gemini-3.1-pro-preview`** | **primary — the text below** | Renders code-switched English in Latin script and reconstructs whole phrases from context. Far more accurate on this material. |
| Speechmatics Batch v2 (`enhanced`, auto language ID) | cross-check | Word-accurate timestamps and no reconstruction, so it is the honest check on whether Gemini invented anything. It did not — every difference below is Gemini recovering something Speechmatics lost. |

Raw output from both engines is archived in **`meetings/voice_notes_raw/`** (`gemini/` and `speechmatics/`) so any quote here can be traced back.

> **Why two engines.** The audio is Sudanese-dialect Arabic densely code-switched with English academic terms — the hardest case for ASR. Speechmatics transliterated the English phonetically into Arabic script (`الفقر` for *Figure*, `لاست اوف اس` for *List of Abbreviations*), which made several passages unreadable and at least one materially wrong. Running both and diffing them is what caught it.

> ⚠️ **Timestamps are Gemini's and are approximate** (model-estimated, drifting by up to ~1 min near the end of long notes). Word-accurate timestamps are in the archived Speechmatics output. **Cite by quoted phrase, not by timestamp.**

> ⚠️ **Attribution is inferred.** The audio contains no self-introduction. The speaker identifies herself as the supervisor (note 13: *"وأنا ممكن برضو كـ supervisor بسألهم"*) and addresses *"انتو الأربعة مجموعات"*. Confirm before citing her by name anywhere binding.

---

## Where the two engines disagree

Every material difference. This is the audit trail for the corrections applied to `2026-07_supervisor_voice_notes_key_points.md`.

| Note | Item | Speechmatics | Gemini | Verdict |
|---|---|---|---|---|
| 8 | The ¾-page rule — what it applies to | referent absent; had to be inferred | *"فتح الـ **abstract** ولقى الـ abstract أكتر من تلاتة أرباع صفحة"* — says *abstract* twice | **Gemini.** Settles it: the ¾-page rule is the abstract. The earlier inference caveat is withdrawn. |
| 13 | Date of the wedding | "يوم واحد 8" — ambiguous | "يوم **1/8**" | **Gemini.** 1 August confirmed. |
| 13 | What she must review before submission | "بالعربي والإنجليزي" — referent inferred | *"أهم من ديل كلهم الـ **abstract** بالعربي والإنجليزي لازم أشوفهم"* | **Gemini.** Confirmed as the abstracts, not inferred. |
| 13 | Translation rule for the Arabic abstract | "ما تكون ترجمة جوجل ولا ترجمة أي" | "ما تكون ترجمة Google **ولا ترجمة AI**" | **Gemini.** Adds an explicit ban on AI translation — see the B2 conflict in the key-points file. |
| 13 | Bracket type for abbreviations | absent | "بين brackets عادية، **ما square brackets**" | **Gemini.** Round brackets, not square. |
| 7 | Name and content of Chapter 5 | "كومنت" — garbled | "comments, conclusion and **recommendations for future work**" | **Gemini.** Speechmatics's "كومنت" was an artefact. |
| 8 | Consequence of losing formatting marks | "بتطلعك من" — sentence cut off | "بتطلعك من الـ **A plus**" | **Gemini.** |
| 1 | Cover page specification | "ثم صمتت. وشنو ديبارتمنت اوف. اوف اوف خرطوم" — unusable | full spec: 20 pt TNR bold title · italic submission line · names + **index numbers** · supervisor · "Department of Electrical and Electronic Engineering, Faculty of Engineering, University of Khartoum" · date · logo | **Gemini.** This unblocks the cover-page audit deferred in task J2. |
| 1 | Chapter-title formatting | "18 بولد" | "18 bold **centered**" | **Gemini.** Adds centring. |
| 1 | Body-text weight | "بـ 12 طبعا **بولد**" (bold) | "بـ 12 طبعاً **unbold**" | **Gemini.** Speechmatics was simply wrong — body text is not bold. |
| 1 | Body alignment | "نعمل ضبط جوانب" | "نعمل ضبط جوانب يكون **justified**" | **Gemini.** Already satisfied — `1-main.tex:19-20` loads `ragged2e` and calls `\justifying`. |
| 3 | Equation numbering | absent entirely | equations numbered per chapter — *equation 2.1, 2.2* | **Gemini.** Checked against the manuscript: 15 `\begin{equation}` environments, 0 unnumbered display-math blocks. Already compliant. |
| 3 | Figure placement | absent | figure must be **centered**; number and caption **below** it, also centred | **Gemini.** |
| 9 | How much theory in the presentation | "سلايدز فقط عن ثيوري" — vague | **1 or 2 slides maximum**, with the reason: examiners cut you off and you lose the chance to present your own work | **Gemini.** |
| 5 | Level of detail required in Chapter 3 | "مين لقيتو زيد" — nonsense | "من الـ **A to Z** أي خطوة اتعملت" | **Gemini.** |
| 10 | Size of the defense panel | "معاه **ثلاث مهندسين** من أساتذة القسم" (supervisor + 3) | "معاه **two examiners** … من أساتذة القسم" (supervisor + 2) | ⚠️ **UNRESOLVED — the engines genuinely disagree** and the two readings are not acoustically similar. Low practical stakes, but do not cite a panel size without asking her. |
| 13 | Name in the greeting | "كيف يا **يوسف**" | "كيف يا **يسري**" | Gemini, probably. Trivial, but note it is a third person, not Elhaj or Osman. |

**One conflict is unresolved: the panel size (note 10).** Everything else resolves in Gemini's favour, and in every case Speechmatics's version is degraded rather than contradictory — which is the expected failure mode, and evidence that Gemini is recovering signal rather than hallucinating.

---

## Contents

**Part I — Thesis document: structure, formatting, chapter-by-chapter**

- [Note 1](#note-1) — General guidance · document formatting · cover page · page numbering · Chapter 1
- [Note 2](#note-2) — Chapter 2 (Literature Review) · citations · reference formatting
- [Note 3](#note-3) — Figures, tables and equations · captions · what belongs in Ch.2 vs Ch.3
- [Note 4](#note-4) — (duplicate of note 3 — byte-identical file)
- [Note 5](#note-5) — Chapter 3 (Methodology) and its zig-zag pairing with Chapter 4
- [Note 6](#note-6) — Chapter 4 — results analysis, and why graphics beat tables
- [Note 7](#note-7) — Chapter 5 — conclusion, comments and recommendations for future work
- [Note 8](#note-8) — Pagination · appendices · PAGE COUNT · abstract length · how marks are lost

**Part II — Final presentation and defense**

- [Note 9](#note-9) — Final presentation — structure and the 1–2 slide theory cap
- [Note 10](#note-10) — The defense panel — composition, split roles, what to bring
- [Note 11](#note-11) — Presentation delivery skills and handling questions
- [Note 12](#note-12) — Defense format confirmed — live on Google Meet, mixed language accepted
- [Note 16](#note-16) — Rehearsal method — mirror, teammate, group

**Part III — Logistics, review gate, supervisor availability**

- [Note 13](#note-13) — Review gate · her availability (1/8) · abbreviations · publications
- [Note 14](#note-14) — Proposed rehearsal day (the 5th, after submission)
- [Note 15](#note-15) — Reassurance — no reason to be nervous

---

# Part I — Thesis document: structure, formatting, chapter-by-chapter

<a id="note-1"></a>

## Note 1 — `1.ogg`

**Duration:** 08:12 &nbsp;|&nbsp; **Topic:** General guidance · document formatting · cover page · page numbering · Chapter 1

**[00:00]** طيب عموماً يعني بعض الإرشادات الأولية ممكن نقولها يعني. أول حاجة ما شاء الله تبارك الله انتو الأربعة مجموعات اشتغلتوا شغل ممتاز ومتميز جداً في مشروعاتكم وكده ونتائج جميلة، وبالتالي نحتاج إنه إخراج التقارير يكون بنفس المستوى لو ما أفضل يعني. لأنه الـ thesis بتعكس مدى اهتمام الطالب بكتابة الأطروحة وعندها درجة يعني الـ examiners من 60 بيدوا 10 درجات للـ thesis بس. يعني كونها هي حسب الموجهات العامة وكده.

**[00:54]** طيب بالنسبة ليكم انتو الأربعة يعني عملنا بعض التوصيات أو الموجهات في كتابة الـ proposal مثلاً زي الـ body قلنا بنكتبه بـ مثلاً font 12 Times New Roman واحد ونص line spacing نعمل ضبط جوانب يكون justified وكده والـ subtitles وكده يعني عرفنا إنه 14، 16 لحدي 18 العنوان الكبير وكده. فده الشكل، ده من الناحية بتاعت شكل يعني الشكل العام للـ thesis بيكون كالآتي.

**[01:34]** أول حاجة الصفحات الأولى اللي هي من صفحة الغلاف، وصفحة الغلاف عندها standard يعني ما بتعمل صفحة غلاف من راسك، بتعمل صفحة الغلاف الـ standard حسب الموجهات، موجهات القسم. خلاص اسم الـ مثلاً الـ project بخط حتى نوع الخط وحجمه بيكون محدد يعني مثلاً 20 Times New Roman 20 bold ده اسم المشروع مثلاً، بعدين بتكتبوا الجملة thesis كده italic بـ font معين كويس، بعدين أسماء الطلاب والـ index numbers بتاعتهم واسم الـ supervisor وبعدين submitted to شنو Department of Electrical and Electronic Engineering, Faculty of Engineering, University of Khartoum بعدين التاريخ. دي صفحة الغلاف اللي هي عندها standard شايفة في السنوات الأخيرة بقوا يضعوا الـ logo بتاع الجامعة في الصفحة الأولى. إذا حصل تغيير والمنسقة رسلت تغيير يعني template محدد الناس تمشي على الـ template بتاع المنسقة.

**[02:56]** طيب طبعاً صفحة الغلاف هي صفحة 1 أو صفحة i بالـ Roman لكن ما بيظهر عليها أو لا يظهر الترقيم في الصفحة الأولى، بيبدأ الترقيم من الصفحات اللي بعديها. يعني في ناس بيعملوا dedication, acknowledgment, declaration, whatever كل الصفحات دي بما فيها الـ abstract بالـ English والمستخلص بالعربي، الـ table of contents والـ list of figures, list of tables, list of abbreviations كل الصفحات دي هي Roman ترقيمها Roman بتعملوها في section مختلف أو section منفصل وترقيم منفصل اللي هو Roman.

**[03:43]** أول صفحة بـ Chapter 1 اللي هي Chapter 1 مثلاً introduction، Chapter 1 introduction كتبتوها بـ 18 bold centered اسمه مثلاً introduction بتجي بعد داك للعناوين الجانبية 1.1 مثلاً preface أو preamble whatever general أي اسم تسموه ليها بيكون هو بـ 16 Times New Roman 16 bold بيجي الـ body بتاع المحتوى بـ 12 طبعاً unbold 12 واحد ونص line spacing. ok؟ فبنجي على هذا المنوال في لحدي التفاصيل Chapter 1.

**[04:33]** Chapter 1 إلى حد كبير هو بيشبه الـ proposal بمعنى إنه هو بيكون فيه الـ objective بيكون فيه الـ يعني general introduction بعدين الـ problem definition والـ objectives والحاجات دي. بس ما بكتب الـ methodology والـ results ليه؟ لأنهم هم أصلاً أنا حأكمل باقي الـ thesis بالـ methodology كاملة وبالـ results والـ discussion بتاعتها وبالتالي أنا بكتب الـ مثلاً في ناس بتكتب state of art بتكتب ما عارف بعد ما عملت الـ definition الـ problem definition وحددت الـ objectives وبالمناسبة الـ objectives ممكن لحدي كتابة الـ thesis يمكن التعديل فيها يعني من حقة الـ proposal. ليه؟ لأنه هنا لازم الـ objectives هي تشير إلى الـ methodology اللي انتو عملتوها وتشير إلى إنه اتحلت المشكلة اللي نحن شرحناها في الـ problem definition. فهنا يجب إنه الـ objectives تكون very specific، very specific تكون محددة ويكون فعلاً المشروع هو حلا الـ يعني هدف المشروع اتحلا بالـ methodology اللي انتو عملتوها. تمام؟

**[05:59]** وآخر حاجة اللي هو بيكون في Chapter 1 إذا حتى لو كتبنا حاجة عن الـ methodology في بعض الناس بيجيبوا الـ بيجيبوا الـ اللي هو الـ history أو الـ related work أو whatever literature review whatever حاجة زي دي بيجيبوها في Chapter 1 وما في ما يمنع إنه أنا بعد ما حددت الـ problem عملت الـ problem definition وحددت الـ objectives أجيب الـ related work ممكن في Chapter 1 وعلى أساسها إنه أحدد إنه أنا عايزة أعمل شنو أو ممكن قبل الـ objectives أعمل الـ related work اللي هي الـ solutions السابقة وكده زي ما عملنا في الـ proposal. لكن المتعارف عليه أكتر هو بنكتب في بنكتبه في Chapter 2 اللي هو literature review. فيستحسن عشان يترتب ويكون تاخدوا راحتكم فيه يكون في Chapter 2.

**[06:56]** Chapter 1 دايماً بيكون قصير، لازم نختمه بالـ thesis outline أو الـ thesis أو يعني thesis layout whatever إنه سميتوها اللي هو دي بيكون هي paragraphs فيها فقط شرح عام يعني بتدي القارئ مدخل لإنه ترتيب الأطروحة حقتي دي شكله كيف. يعني بتتكلمي مثلاً أول حاجة بتتكلموا عن إنه الـ this thesis مثلاً organized in five chapters or انتو four chapters حسب كويس Chapter 1 this chapter is كده كده introduction to كده Chapter 2 whatever بيتكلم ممكن يكون one long paragraph in sentences أو ممكن يكون different paragraphs لكن يستحسن إنه هو لأنها حاجة continuous أنا بشرح عن ترتيب الـ chapters بتاعتي لإعطاء القارئ فكرة عن ترتيب البحث ok؟ من البداية إلى النهاية لحدي ما أصل لإنه أنا Chapter 1 كتبت فيه شنو Chapter 2 لشنو Chapter 3 وهكذا. ok؟

<a id="note-2"></a>

## Note 2 — `2.ogg`

**Duration:** 02:07 &nbsp;|&nbsp; **Topic:** Chapter 2 (Literature Review) · citations · reference formatting

**[00:00]** طيب نجي لـ Chapter 2 واللي هو في الغالب هو الـ literature review. والـ literature review بتكون هي لأي معلومات مجمعة من الـ literature، يعني عن أدبيات البحث، أي theories أو equations أو related work أو أي يعني معلومات عامة اللي هي من المراجع أو من صفحات الإنترنت أو من كتب أو من whatever. اوكي؟

**[00:40]** فـ Chapter 2 هو دايماً بيكون Chapter ثر، لكن يستحسن إنه يعني نكتب فيه المهم، الأشياء المهمة. أي معلومة محتاجة لشرح بشرحها هنا. إذا جبت الشرح من مرجع لازم في نهاية الـ paragraph أعمل between two square brackets رقم المرجع.

**[01:03]** وبالمناسبة ترقيم المراجع بيكون according لورود المراجع وين؟ داخل الـ thesis وليس لأهميتها. يعني Chapter 1 في الغالب ما بيكون فيه مراجع، لكن Chapter 2 بدينا بالـ related work for example، أول مرجع هو المرجع number 1، المرجع التاني number 2، بكتبها between two square brackets.

**[01:30]** وبعدين بمشي في صفحة الـ references في نهاية الـ thesis بكتب فيها المراجع according للـ IEEE. حسب الشكل العام لكتابة المراجع المعتمد من الـ IEEE. إذا كان المرجع كتاب، إذا كان journal paper، إذا كان whatever إنها هي كانت conference paper أو كانت أو كانت website بنكتب الـ URL كامل وبنكتب accessed on كده، تاريخ التصفح للصفحة.

<a id="note-3"></a>

## Note 3 — `3.ogg`

**Duration:** 02:43 &nbsp;|&nbsp; **Topic:** Figures, tables and equations · captions · what belongs in Ch.2 vs Ch.3

**[00:00]** نواصل في chapter 2 اللي هو chapter 2 إذا كان فيه equations إذا كان فيه figures إذا كان فيه tables من ال literature برقم ال equations برقم ال figures بعمل caption لل figure figure مثلا أول figure هو figure 2.1 في chapter 2 أول figure هو figure 2.1 واسمه كذا الاسم لازم يكون اسم توضيحي كويس ما أكتب مثلا

**[00:31]** كلمة كلمة واحدة أو كلمة مبهمة يعني لابد إنه اسم ال figure هو يكون بيشرح معنى ال figure عشان كده بيسموه ال figure caption ويكون اسم يعني واضح كويس بيشرح نفسه ما يضطر ال examiner إنه يسألك يقول لك ال figure ده بتاع شنو أو الاسم ده ما واضح أو الاسم ده ما بيعني المحتوى

**[01:00]** بتكتب تحت ال table تحت ال figure طبعا ال figure centered واسمه تحته ورقمه والاسم بيكون تحته و centered كذلك. أما ال tables بتتكتب أسماءها بفوق ليها يعني أول table في chapter 2 هو table 2.1 واسمه يتكتب كمان واضح ولازم يكون اسم مفهوم اوكي وبتكتب

**[01:30]** في الغالب اللي هم table مثلا 2.1 كده بتتكتب bold وشايفة في بعض الأحيان بتتكتب عادي ما bold وال figures كمان برضه بنكتب ال caption bold في وسط الصفحة. ال equations ترقم ال equations ب equation 2.1 equation 2.2 حسب ال equations وحسب ترتيبها داخل ال chapter الكلام ده بينطبق طبعا على كل ال chapters وليس chapter 2 فقط يعني أنا chapter 2 ك example لكن كل ال chapters بيتكتب الترقيم ال figures وال tables وإذا في equations قلنا بنفس الطريقة

**[02:18]** دايما chapter 2 خليه خلوا فيه كل ال theories behind ال research أي حاجة عندها علاقة بال research بتاعكم معلومة definition equations كلها بتخليها في chapter 2 لما أجي أشتغل في chapter 3 فقط بشير إلى ال section أو ال subsection الفيه المعلومة.

<a id="note-4"></a>

## Note 4 — `4.ogg`

> **Duplicate.** `4.ogg` is byte-identical to `3.ogg` (same MD5). It was not transcribed. See [Note 3](#note-3).

<a id="note-5"></a>

## Note 5 — `5.ogg`

**Duration:** 01:22 &nbsp;|&nbsp; **Topic:** Chapter 3 (Methodology) and its zig-zag pairing with Chapter 4

**[00:00]** طيب بجي لـ chapter 3 و chapter 3 في الغالب هم الناس بيسموه methodology لكن ممكن تسميه اسم بيشبه اسم المشروع ذات نفسه حسب المحتوى، حسب محتوى الـ chapter 3. فـ chapter 3 هو معني بـ الإنتو عملتوه شنو في البحث. بالتفصيل، بالتفصيل. يعني من الـ A to Z أي خطوة اتعملت. 

**[00:28]** وأفتكر نحن already بدينا في كتابة chapter 3 مع chapter 4 الـ results and discussion مع بعض زي ما كنا بنقول إنه يعني شكل zigzagging. كل paragraph اتكتب في chapter 3 في الـ methodology النتايج بتاعته ظهرت في chapter 4. برجع تاني لـ chapter 3 الجديد شنو ونتايجه في chapter 4 وهكذا بالـ sections والـ subtitles يعني 3.1, 3.2, 3.3. 

**[01:00]** وهناك في chapter 4 الـ results discussion أو الـ results and discussion أو results analysis and discussion whatever إنه كان اسم chapter 4 هو بيكون تحليل للـ نتايج وتحليل النتايج اللي هي حسب النتايج اللي وصلنا ليها في المشروع في chapter 3.

<a id="note-6"></a>

## Note 6 — `6.ogg`

**Duration:** 01:41 &nbsp;|&nbsp; **Topic:** Chapter 4 — results analysis, and why graphics beat tables

**[00:00]** Chapter 4 من أهم الـ chapters ليه لأنه بيوضح رؤية الطالب وإدراكه في فهم وتحليل النتائج. ليس بالضرورة يعني دايما أنا بقول ليكم ما كسر رقبة إنه النتائج تكون perfect. ما بالقوة إنه لازم الحاجات تكون هي يعني ممتازة، لكن ليه ما جات ممتازة؟ ليه ما جات الحاجة اللي نحن كنا متوقعينها؟ فلا بد إنه برؤية هندسية فنية نقدر نحلل النتيجة بالطريقة الصحيحة.

**[00:35]** كويس؟ كل جزئية وقبل كده اتناقشنا أكتر من مرة في طريقة تحليل النتائج وكلكم ما شاء الله تبارك الله يعني طريقة تحليلكم very professional. بتعرفوا تحللوا النتائج كويس وإذا سئلتوا عنها بعدين في المناقشات أكيد ما حيكون عندكم فيها إشكال. بس إخراجها بالطريقة الصحيحة وبطريقة الـ standard هو المهم.

**[01:01]** يعني لازم نقدر نرتب النتائج بطريقة واضحة، إخراج النتائج في شكل بالذات الـ graphics يعني لأنها بتسهل الفهم وبتسرع الفهم بتاع النتيجة اللي وصلتوا ليها. دايما الكلام الـ theory والـ tables وكده بتكون فهمها صعب فيستحسن إنه تتعمل النتائج في شكل بتاع graphs يعني أو رسومات بتشرح النتائج أو مقارنات. أو حتى لو كانت tabulated في tables برضه تكون لكن حاجة مفهومة وذات معنى يعني.

<a id="note-7"></a>

## Note 7 — `7.ogg`

**Duration:** 01:15 &nbsp;|&nbsp; **Topic:** Chapter 5 — conclusion, comments and recommendations for future work

**[00:00]** طيب بالنسبة لـ Chapter 5 واللي هو في الغالب هو بيكون conclusion, comments and recommendations، recommendations for future work أو حاجة زي دي يعني الاسم ما شرط لكن في الغالب بيكون هو بيحتوي على comments عامة عن المشروع والنتائج والـ conclusion الخاتمة والـ recommendations. والـ recommendations مهمة جداً لأنه بتوضح إنك إنت فاهم المشروع وعارف أوجه القصور.

**[00:30]** أو رؤى جديدة لحل المشكلة أو طرق جديدة ممكن ظهرت أثناء ما إنت شغال في المشروع بتضعها في شكل recommendations وتكون عارف إنك إنت ليه ما عملت الحاجة اللي إنت أصلاً وضعتها في توصية. التوصيات دايماً بتكون هي يعني هادا، هادية للطلاب اللي جايين بعديكم في إنهم هم ممكن يعملوا نفس المشروع بطريقة تانية أو يعملوا يواصلوا في المشروع أو كده. وبتكون كل ما كانت الـ recommendations يعني واضحة وقوية كل ما أثبتت إنه الطالب فاهم هو عمل شنو ووصل لنتائج شنو وممكن يعمل تحسين للمشروع بياتو طريقة.

<a id="note-8"></a>

## Note 8 — `8.ogg`

**Duration:** 04:23 &nbsp;|&nbsp; **Topic:** Pagination · appendices · PAGE COUNT · abstract length · how marks are lost

**[00:00]** طيب آخر حاجة في الـ thesis ده كله الترقيم ده من واحد اتنين كده لحدي بينتهي بصفحة الـ references وزي ما ذكرنا الـ references بترقم والترقيم بتاعها بيكون حسب ورودها داخل محتوى البحث. كتابة المراجع بتكون حسب الـ IEEE كويس standard وبينتهي الـ thesis بنهاية الـ references.

**[00:30]** أما إذا كان هنالك معلومات إضافية أو معلومات يعني هي ما جزء أصيل في الـ thesis أو في المشروع لكنها مفيدة وممكن تكون صعبة إنه القارئ يلقاها أو أحياناً الـ code ذات نفسه إذا كتبتوا برنامج أو كده بنخليها دي في الـ appendices. يعني الـ appendix بيكون appendix A, appendix B, appendix C كده. الـ appendix برقمه ترقيم مختلف. 

**[01:00]** appendix A بيترقم A1, A2, A3 وهكذا. appendix B, B1, B2, B3 لأنهم هم ديل بيعتبروا ملاحق للـ thesis لكن ما جزء أصيل منها يعني. أوكي فبكده بيكون عندكم يعني ما في عدد محدد ولكن متوقع يعني...

**[01:30]** من 50، 70 أقصى حاجة ممكن 80 صفحة. It's quite enough يعني للمشروع. نحاول بقدر الإمكان يكون ما قل ودل، يكون فيه الـ يعني المحتوى يكون وفق الـ recommendations أو وفق الموجهات وفي نفس الوقت تكون مليانة يعني تكون حاجة تشير تماماً إلى المجهود اللي انتوا بذلتوه.

**[02:00]** طبعاً نحن مقتنعين تماماً إنه انتوا بذلتوا مجهود وفي زمن قياسي ويعني في ظروف صعبة، لكن لو ما تم إخراج الشغل ده في الأطروحة ما في يعني بتكون ظلمت نفسك انت كطالب في درجاتك بعدين في تقييم البحث وكده. فإخراج البحث مهم جداً في الـ thesis بتاعتك وتكون وفق يعني لو واحد من الأساتذة...

**[02:30]** ...فتح الـ abstract ولقى الـ abstract أكتر من تلاتة أرباع صفحة حسب الموجهات دي، أكتر من تلاتة أرباع صفحة، صفحتين، صفحة ونص، أو لقاه two paragraphs ما واصلة نص صفحة أو كده، أو لقى مثلاً الـ abstract ما مضبوط الجوانب، لقاه مكتوب بخط يعني يعني أشياء بسيطة جداً جداً طوالي بيجي انطباع إنه الطالب ما مهتم بشكل البحث. 

**[03:00]** تخيل إنه ده شكل البحث وشكل الـ thesis بتاعتك مش المحتوى، بغض النظر عن إنك انت كاتب محتوى يعني مليان قدر شنو، بغض النظر عن إنه المحتوى حقيقي وممتاز، بغض النظر عن أي شيء، عدم اهتمام الطالب بإخراج البحث هو نقطة سوداء ممكن على إثرها الطالب يفقد...

**[03:30]** ...درجات كبيرة جداً اللي هي إذا فقدت انت من الـ 10 درجات فقدت ليك 5، 6 درجات في ترتيب البحث وترتيب الأطروحة وإخراجها بتطلعك من الـ A plus. فنكون حريصين جداً في إنه نحن كيف يعني to collect الـ marks دي بأي صورة لأنها هي موزعة وتوزيعها ده يعني الأستاذ ما يقدر ما يقدر يقول الطالب مثلاً...

**[04:00]** ...عامل الـ thesis مية المية ما يقدر يديك 10 من 10 أصلاً لو في أي نقص أو في يعني أشياء ما وفق الـ standards. فلازم نكون حريصين على إخراج الأطروحة وما نهمل الكتابة وفي نفس الوقت نكون حريصين على إخراج البحث بتاعنا بالطريقة الصحيحة.

---

# Part II — Final presentation and defense

<a id="note-9"></a>

## Note 9 — `9.ogg`

**Duration:** 03:51 &nbsp;|&nbsp; **Topic:** Final presentation — structure and the 1–2 slide theory cap

**[00:00]** طيب انتهينا من كتابة الـ thesis نجي للـ presentation. انا ما عارفة هم هسة رسلوا قالوا شنو يعني هل قالوا يتعمل تسجيل زي السنتين الفاتو ولا قالوا حتكون في مناقشة يعني حضورية ولا قالوا مناقشة online صراحة ما عندي معلومة. لكن anyway ممكن نعمل يعني تلخيص عن الـ presentation.

**[00:30]** طيب بالنسبة للـ final project presentation. اول حاجة بيكون عندك صفحة الغلاف، صفحة الغلاف طبعا في ناس بتعمل PowerPoint في الغالب يعني وفي ناس بتعمل بـ tools تانية يعني Prezi وغيرها ممكن من الـ presentations لكن مافي اشتراط محدد لكن الغالب الاعم هم الناس بتشتغل على الـ PowerPoint. طيب الصفحة الاولى هي صفحة الغلاف فيها اسم المشروع كبير واسم الطالب واسم الـ supervisor وكده يعني تمام.

**[01:09]** الصفحة التانية لازم يكون فيها الـ agenda. agenda اللي هي محتوى الـ presentation وقبل كده انا رسلت ليكم محاضرة مسجلة عن how to write your presentation افتكر. فلازم في الـ presentation يكون عندي agenda، الـ agenda انه انا مرتبة انا حتكلم عن شنو ثم شنو ثم شنو ثم شنو تمام. طيب بعد كده بجي بـ... طبعا في الـ presentation ما زي الـ report يعني هنا ما قل ودل وبتم الباقي شرح. بكتب كتابة بسيطة بميل للرسومات والـ bullets والشرح بيكون بعد داك يعني verbal.

**[02:00]** فـ... introduction او الـ slide عن الـ problem definition اهم حاجة. بعدين الـ objectives. بعد كده الـ methodology اللي هنا بتكون فيها البحث ذات نفسه عملنا شنو وعملنا شنو كمان قلنا نكون to the point. الـ results والـ discussion والـ conclusion كلها دي بتتكتب في الـ presentation باختصار كويس. اهم حاجة ما نسهب في الـ theories.

**[02:30]** يعني تقعد تتكلم عن الشرح النظريات والـ... لا لا لا دي بتضيع الزمن. ما قل ودل ونركز على الـ methodology والـ results and discussion والـ conclusion. يعني النظريات دي كلها معروفة للناس بعد ما شرحت الـ problem بتاعتي وحددت الـ objectives. slide او two slides فقط عن الـ theory او الـ theoretical parts.

**[03:00]** لكن ركز بعد داك على تفاصيل الـ presentation... سوري على تفاصيل الـ methodology والـ results and discussion عشان الزمن ما يضيع وتكون انت ما عملت حاجة في الشرح يقولوا ليك لا خلاص كفاية امشي خلاص للنتائج. انت هنا بتكون ما قدرت وصلت انك انت عملت شنو بالظبط لانك ضيعت الزمن كله في النظريات وفي الشرح الـ theoretical parts والحاجات دي. فحاولوا بقدر الامكان تقللوا وتركزوا على شغلكم اللي انتو اشتغلتوه، النتائج اللي انتو وصلتوا ليها وتحليل هذه النتائج وبعدين الـ conclusion.

<a id="note-10"></a>

## Note 10 — `10.ogg`

**Duration:** 03:27 &nbsp;|&nbsp; **Topic:** The defense panel — composition, split roles, what to bring

**[00:00]** طيب أنا بصراحة ما قاعدة أقرأ في رسايلكم لحد ما أخلص برجع بشوف الرسايل. طيب عايزين نتكلم على الـ discussion أو الـ panel. في الغالب بيكون في يعني عادة زمان كان بيتعمل الـ panel كالاتي: بيكون الـ supervisors، الـ supervisor للمشروع ومعاه two examiners. خلاص؟ من القسم، من أساتذة القسم. كويس؟ طبعاً المناقشة الحضورية...

**[00:31]** بيكون... قبل كده كان بيجي كل طالب بيناقش لوحده وبيطلع بيجي طالب تاني يناقش لوحده. هم بيكونوا اشتغلوا نفس المشروع ولكن كل طالب كان بيكتب thesis لوحده ويناقش لوحده. فدي كانت الهدف منها إن الناس تقوي مهارات الـ thesis writing والحاجات دي وبعدين يتأكدوا الـ examiners إنه فعلاً الطالب ده اشتغل المشروع ده بنفسه وكده.

**[01:00]** في السنوات الأخيرة وكتخفيف يعني للطلاب بقوا يدخلوا الطلاب الاتنين في نفس الـ panel. يعني بيبقى المناقشة واحدة ليهم الاتنين. فطالب مثلاً يشتغل الجزء الأول بتاع الـ introduction والـ problem definition وكده والطالب التاني شرح الـ methodology، داك رجع اشتغل الـ results and discussion وهكذا يعني. الطلاب بيقسموا الأدوار بينهم وبيعرضوا الشغل بطريقة...

**[01:30]** أهم حاجة إنه يكون الانتقال سلس جداً ما بين الطالب والطالب الآخر يعني. يكون واضح إنه في انسجام في الـ team. لازم يكون واضح إنه كل طالب فاهم اللي اشتغله زميله أو اللي شرحه زميله لأنهم هم اشتغلوه كـ group. ما... ما يعني ما يركز على إنه والله زميله اشتغل أو هيشتغل على جزئية أو يشرح جزئية هو ما يفهمها، لأ لازم تكونوا فاهمين كل شيء.

**[02:01]** لأنه الأسئلة ممكن تكون موجهة مباشرة لطالب محدد، طالب بعينه. وهنا في الحالة دي لو ما فاهم بتكون هنا نقطة سالبة في تقييمه وكده. فهنا حيكون الطلاب لازم يكونوا... أو الـ team يعني اللي فيه الطالبين لازم يكونوا هم فاهمين كل شيء. وعادي ممكن يقول لك افتح صفحة كده في الـ report، اعمل كده، ورينا اشرح لينا الـ figure الفلاني وهكذا عادي جداً.

**[02:33]** ممكن يقول لك الـ table ده بيعني شنو؟ الـ figure دي ليه جات شكلها كده؟ تحليلك للنتيجة دي من الـ thesis. فلازم يكون عندك نسخة من الـ thesis معاك. برضو كتخفيف للطلاب طبعاً غير السنتين الأخيرات بتاعت الحرب لكن حتى قبل كده كان الطلاب بيسلموا soft copies يعني بتطبعوا نسخة واحدة أنتو الاتنين حتى لو...

**[03:00]** two different covers ممكن لكن أهم حاجة نسخة إلكترونية تكون موجودة. فالنسخة الإلكترونية إذا هسي قالوا ليكم سلموا soft copy وواحدة hard copy أوكي، بتكون معاكم الـ hard copy أثناء المناقشة. قالوا لأ كلها تكون soft copy المهم حسب موجهات اللي هو المنسق. المنسق هو بيوضح للناس يعملوا شنو والمطلوب منهم شنو.

<a id="note-11"></a>

## Note 11 — `11.ogg`

**Duration:** 01:18 &nbsp;|&nbsp; **Topic:** Presentation delivery skills and handling questions

**[00:00]** طيب بعدين في برضو محاضرة كانت رسلتها ليكم قبل كده عن تقديم الـ presentation كيف. يعني لو متذكرين كنا بنتكلم عن الـ presentation skills وانتو كلكم ما عندكم مشكلة يعني في الـ presentation skills ولا الـ communication skills ولا كده يعني. دايما بقول ليك ركز على الـ eye contact لكل الناس الموجودين، لغة الجسد، الـ body language لازم يعني عندها تفسير معين. بطل الحركة السريعة، ما تدخل يديك في جيوبك، ما تقيف وقفة كده، ما... وهكذا يعني الأشياء المعروفة بالنسبة ليكم دي. دي بصورة عامة.

**[00:45]** لكن الأهم من كده المحتوى. يعني فهمك للسؤال، إذا ما فهمت السؤال ممكن تطلب من الأستاذ يعيد السؤال مرة تانية عادي مافي مشكلة. لكن تفهم السؤال عشان تجاوب الإجابة المنطقية، الإجابة العلمية المنطقية. عشان ما تؤخذ عنك... تؤخذ نقطة سالبة في إنك إنت جاوبت إجابة أي كلام أو جاوبت إجابة off point. فهنا برضو في التقييم بتكون يعني نقطة سيئة بالنسبة ليك.

<a id="note-12"></a>

## Note 12 — `12.ogg`

**Duration:** 01:11 &nbsp;|&nbsp; **Topic:** Defense format confirmed — live on Google Meet, mixed language accepted

**[00:00]** هم قالوا كده يعني حتكون live في Google Meet أنا والله ما سمعتها، لكن عادي عادي يعني هو الكلام اللي أنا سجلته ليكم ده، بتشرحوا الـ presentation حقكم وعادي بتجاوبوا على الأسئلة وزي ما قلت ليكم الأسئلة يجي منو الإجابات تكون to the point. حتى الأسئلة ما قاعد ما بتكون أسئلة يعني تعجيزية أو كده، أسئلة بغرض إنه التأكد من إنه الطالب عمل المشروع بنفسه واشتغل بنفسه وكده، عشان التقييم يكون fair يعني، ما يكون تاخد حاجة ما حقتك ولا تتظلم يعني.

**[00:40]** فـ take it easy وعادي طبعاً هم بيقولوا ليك يعني اعمل الـ presentation، fully in English لكن عادي نحن الطلاب بيشتغلوا mix يعني زي الـ presentations اللي بتعملوها في المقررات وكده. فما في ما في يعني تعقيد، ما في تعقيد. أهم حاجة تكونوا واثقين من نفسكم، وتقدروا توصلوا المعلومة بالطريقة الصحيحة والسهلة، وتقدروا تجاوبوا على الأسئلة وتدافعوا عن شغلكم.

<a id="note-16"></a>

## Note 16 — `16.ogg`

**Duration:** 00:43 &nbsp;|&nbsp; **Topic:** Rehearsal method — mirror, teammate, group

**[00:00]** كمان في في الحتة بتاعت الـ rehearsal دي ممكن تعملوا شنو؟ يعني دايما لو متذكرين في الـ presentation الكان رسلته ليكم داك، عن الـ presentation skills، بيقول لك بعد ما انت أهم حاجة الإعداد، إعداد المحتوى، وفهم المحتوى. الحاجة التانية، ممكن تعمل البروفة مع زميلك، ممكن تعمل البروفة مع المراية عديل يعني، تشرح لنفسك وكده. الـ المرة التالتة ممكن تشرح لـ زملائك كـ team. فخلو عندكم بروفتين قبل يعني، واحدة مع نفسك في المراية، والتانية مع زميلك في الـ team، والتالتة حتى تجي في الـ group بتاعنا ده كله مع بعض إن شاء الله.

---

# Part III — Logistics, review gate, supervisor availability

<a id="note-13"></a>

## Note 13 — `13.ogg`

**Duration:** 04:08 &nbsp;|&nbsp; **Topic:** Review gate · her availability (1/8) · abbreviations · publications

**[00:00]** السلام عليكم ورحمة الله وبركاته، كيف يا يسري تمام؟ وكل المجموعة. ما في مشكلة ممكن نعمل، هو عادة أنا يعني في لما كان المناقشات حضورية كنت بطلب من الطلاب في نص الـ... أو في نهاية الـ semester الأول أو بداية الـ semester التاني كنا بنعمل presentation أول، وقبل الـ final التسليم النهائي كنا بنعمل presentation تاني. وبنخلي الـ team، الـ team عندي كلهم يسألوا بعض يعني، يسألوا بعض وأنا ممكن برضو كـ supervisor بسألهم، ويعني بغرض إنه نعرف مكامن النقص والخلل وين والإجابات ممكن يكون شكلها كيف وكده. فما في ما يمنع إنه نعمل الـ rehearsal ده يعني، لكن أنا للأسف عندي زواج بتي يوم 1/8، فهكون في حالة بتاعت عدم استقرار في الفترة الجاية.

**[01:00]** إنتو اعملوا الـ recommendations العندكم القلتها ليكم دي كلها تظبطوها عشان ما ترجعوا، لأنه التعديل والـ editing أصعب من الكتابة من أول مرة يعني، كل ما الحاجات تكون يعني من الأول مظبوطة وكده بتكون بالنسبة ليكم تمام وبالنسبة لي أنا تمام. خلاص؟ اتبعوا الموجهات دي واشتغلوا عليها، وأنا قبل كده شفت يعني في ناس كنت شفت عندهم Chapter 2 كامل و Chapter 3، 3 و 4 كان partial. قبل ما يعني نختم النتائج النهائية اللي هو قلنا بعد داك تمشوا للامتحانات وكده، بكون ممكن محتاجة أشوف Chapter 1 و Chapter 5 اللي هو comments, conclusion and recommendations for future work، ده بكون مهم أشوفه. أهم من ديل كلهم الـ abstract بالعربي والإنجليزي لازم أشوفهم، لازم أشوفهم قبل التسليم. فإنتو اكتبوا الشغل بتاعكم صح، الترجمة حاولوا بقدر الإمكان ما تكون ترجمة Google ولا ترجمة AI، حاولوا استخدموا الـ terminologies المستخدمة عندنا في اللغة العربية الصحيحة، ده في ترجمة المستخلص يعني، خلاص؟

**[02:15]** كمان نسيت في حاجة مهمة في الصفحات الأولى يعني بعد ما نعمل الـ table of contents و list of figures و list of tables، في list of abbreviations، ما تنسوها. الـ abbreviations مهمة جداً إنه أول مرة يظهر الـ abbreviation في الـ thesis بيتكتب كامل، بيتكتب كامل والحروف الجاية منها الـ abbreviation هي تكون capital وباقي الحروف تكون small، ويتكتب الـ abbreviation بين brackets عادية، ما square brackets العادية دي، وبعد كده بستخدم الـ abbreviated word عادي، كويس؟ فدي مهمة جداً لأنه يعني بيكون عليها ملاحظات إذا كانت ظهرت abbreviations بدون ما يحصل يعني شرح ليها.

**[03:07]** بالرغم من كده بتتعمل الـ list of abbreviations في الصفحات الأولى وبتترتب ترتيب أبجدي، يعني alphabetical، كويس؟ ترتيب الـ list of abbreviations بيكون alphabetical، دي مهمة جداً لازم تنتبهوا ليها ولازم تعملوها، بتظهر معاكم في الـ contents الأولى يعني ما قبل التقرير وبتكون مهمة. كمان إذا في مجموعة قدمت paper للنشر حتى ولو ما نشرت يستحسن كمان تشيروا ليها كـ contribution، فالـ contribution مهم وبيزيد من يعني أسهم الطلاب في إنه والله أنا عندي published paper في الشغل ده أو عندي accepted so far أو whatever يعني، فدي مهم جداً إنه الطلاب إذا عندهم حاجة زي دي يشيروا ليها كنوع من الـ contribution.

<a id="note-14"></a>

## Note 14 — `14.ogg`

**Duration:** 00:32 &nbsp;|&nbsp; **Topic:** Proposed rehearsal day (the 5th, after submission)

**[00:00]** فا يعني ممكن من يوم خمسة اللي هو بعد التسليم نحدد يوم ان شاء الله يوم خمسة انا بكون ان شاء الله فضيت ربنا يعدي على خير وعقبال نفرح بيكم كلكم ان شاء الله. 

**[00:14]** ان شاء الله بكون خلصت فبحدد يوم يكون يوم طويل كل المجموعات تشتغل الـ presentations بتاعتها تعمل البروفات ونعمل discussion ونشوف اول حاجة نقيم الـ presentation ذات نفسها وفي نفس الوقت نعمل البروفة للـ discussion والـ defense بيكون شكله كيف.

<a id="note-15"></a>

## Note 15 — `15.ogg`

**Duration:** 01:16 &nbsp;|&nbsp; **Topic:** Reassurance — no reason to be nervous

**[00:00]** لا لا لا لا ما في اي توتر ولا حاجة زي ما بقولوا المصريين انتو قدها وقدود. يعني اول حاجة انا واثقة كل المجموعات عندي اشتغلت شغلها. كويس كل المجموعات اشتغلت الشغل بتاعها تمام التمام، والـ theoretical background عندهم ممتازة، الـ الشغل العملي ممتاز، النتائج والـ discussion. فما في حاجة بتخليكم تتوتروا او تخافوا.

**[00:31]** كلكم ما شاء الله تبارك الله الـ skills بتاعتكم حلوة، الـ presentation skills ما عندكم فيها مشكلة. الباقي هو ثقة، اهم حاجة ثقتك بنفسك كويس هي بتكون 90%. لانو انت فاهم الشغل وانت اكتر واحد بتكون مستوعب الـ problem والـ solution اللي انت عملتو، لانك انت يعني اشتغلت فيه او يعني انتو كـ team يعني اشتغلتو فيه بعمق شديد.

**[01:01]** ففاهمين كل صغيرة وكبيرة فيه وبالتالي يعني ما في حاجة بتدعو للخوف ولا بتدعو للتوتر. اهم حاجة الناس تكون relax وتكون واثقة بنفسها 100%.

---

## Reproducing this

**Speechmatics Batch v2.** Two gotchas cost real time: `language_identification_config` is a **sibling** of `transcription_config`, not a child (the API rejects the nested form); and the transcript response must be read as `response.content.decode('utf-8')` — `response.text` mis-decodes Arabic as Latin-1 and silently produces mojibake.

```json
{"type": "transcription",
 "transcription_config": {"language": "auto", "operating_point": "enhanced",
                          "diarization": "speaker"},
 "language_identification_config": {"expected_languages": ["ar", "en"]}}
```

**Gemini.** `gemini-3.1-pro-preview`, audio sent inline as base64 (`inline_data`, `audio/ogg`), `temperature: 0.0`. The prompt is what makes the difference: it states the speaker, the dialect, the setting, gives ~15 example English terms she is likely to use, and — the single most important instruction — orders code-switched English rendered in **Latin script, spelled correctly** rather than transliterated. It also asks for a separate `UNCERTAIN` section, which is where a model will flag a guessed number instead of quietly asserting it.
