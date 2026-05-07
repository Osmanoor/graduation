**المتحدث 1 (محمد الحاج سامي):** نواصل النقاشات المتمحورة حول الـ thesis uh changes. آخر شيء أنا بتذكر كان تمينا هنا، كان تمينا الـ query repetition ده. خشينا section 4 chapter 4 كان في الـ phase 4.

**المتحدث 2 (عثمان بشير):** أي انتهينا منها؟

**المتحدث 1:** انتهينا منها أي. error analysis انتهينا منه أي. chapter 4 طيب chapter 4 which is the results uh phase 4 additions section 4.6 BM25 query repetition results. النقطة الأولى بتقول إنه الـ combined single 8-column table with N = 1, 3, 5, 7, 10 and B = 2, 4, 6 side-by-side dense but readable alternatives split into two tables keep combined if you want at a glance uh at a glance comparison uh of fixed versus adaptive اللي هو ده ده اللي هو الجدول اللي هو في صفحة اللي هو في الـ results.

**المتحدث 2:** أول حاجة مش أول result، أول uh repetition.

**المتحدث 1:** section 4.6 أي ده. أي منطقي ما إحنا مرات إحنا كنا عملناها N ومرات عملناها هناي، مرات عملناها بالـ بيتا اللي هو كانت مرات ثابتة ومرات هناي، adaptive. فمنطقي نخليهم جنب بعض.

**المتحدث 2:** uh هو منطقي تتفصل لكن مفهومة يعني كده.

**المتحدث 1:** مفهومة جدًا يعني ما عندها عوجة.

**المتحدث 2:** الـ adaptive ظاهر أي أحسن. هنا 7، 5، 7، 5، 7 لا لا جميل.

**المتحدث 1:** فنخليها مفصولة؟

**المتحدث 2:** لا خليها كده أي، خليها table واحد مفهومة ما عندها عوجة. الشرح حيكون أفضل.

**المتحدث 1:** مش الشرح ده كويس؟ المكتوب ده. query columns N are fixed columns, column B are adaptive repetition columns for query as N max numerical uh value per column in bold. جميل جدًا. uh طيب جميل leave it leave it as B. طيب claim query repetition recovers all 9 previously degraded BM25.

**المتحدث 2:** أيوة. صح.

**المتحدث 1:** uh مع إنه هم ما هم ما ما التسعة degraded، هم بس الستة كانوا degraded يعني.

**المتحدث 2:** ما هو قال قال هنا، ثلاثة، ثلاثة out of 9، بقوا 9 out of 9 هو متحسن. وحقه كان يقارن مع مع الـ baseline صح مش، مش في مقارنة للموديلز كلها مع الـ مع الـ baseline with repetition or without repetition مفترض يكون في حاجة زي دي؟

**المتحدث 1:** أو دي أو دي ممكن تكون كـ graph ممكن يكون كـ graph الحاجة دي. graph، graph يوضح يعني، graph يوضح الموديلات، الموديلات كانت كيف قبل الـ repetition وبعد الـ repetition. اللي هو بيوضح يعني مثلاً الكان مثلاً الـ baseline، الـ baseline في موديلات لمن حصل ليها query expansion من دون repetition بقوا تحت الـ baseline. وتاني بعدين بعد الـ repetition بقوا فوق الـ baseline كلهم. دي حاجة كانت قاعدة في في السلايدس تقريبًا، ولا في الكولاب؟

**المتحدث 2:** كولاب قاعدة الحاجة دي.

**المتحدث 1:** اللي هي حاجة...

**المتحدث 2:** ده كان ضفناه أمس في الكولاب، ده أضفناه في السلايد في الـ presentation.

**المتحدث 1:** لا هو في الـ في الـ presentation إحنا كان لسه ما عملناه. الكولاب قاعد، زي دي. تقريبًا. يعني يعني بنلقى إنه الـ BM25 من دون، من دون query enhancement baseline ده أصلاً هو قاعد كده، تمام؟ قاعد عند score مثلاً 0.46، تمام؟ بنلقى إنه في ثلاثة models، في ثلاثة models الـ query expansion بتاعهم أدانا أدانا أداء أحسن من الـ baseline وفي ستة models الأداء أدانا أسوأ، تمام؟ إذا كان الـ repetition واحد، أول ما الـ repetition يبقى تلاتة بنلقى إنه الـ query enhancement بالنسبة ليهم كلهم أدى أداء أحسن من من الهناي، من الـ baseline. الـ graph ده، graph بيوضح جدًا يعني الحاجة دي بصورة كويسة، فبتلقى إنه بعد بعد الـ repetition بتاع التلاتة كل الخطوط بقت فوق الخط الأحمر ده في حين إنه لمن كان واحد ست، ستة كانوا تحت الخط الأحمر. وبنلقى إنه الأداء أحسن في في، طبعًا بعد ده الجايس كان أحسن، لكن في النهاية آية بقى أحسن برضه في في الـ BM25 بعد ما حصل repetition. بنلقاهم كلهم أحسن في 5 لـ 7، 7 حصل خلاص، حصل saturation بعد ده بدأ ينزلوا. فقصدي graph زي ده أو حاجة زي دي يعني ممتازة أيوة. أو زي الـ heatmap دي، زي دي برضه كده للـ baseline، الـ baseline ده برضه نفس الفكرة موضح إنه واحد، اتنين، تلاتة ديل ليهم الأحسن، لكن ديل كلهم كانوا قبل الـ repetition أسوأ، لكن بعد الـ repetition بقوا أحسن ودي أحسن قيمة ليهم، الـ graph ده برضه ممتاز يعني.

**المتحدث 2:** طيب أنا شايف عمومًا في graph زي دي، شايفه؟ أصلاً في task عند عمر بتاع الجرافات حنضمن إن شاء الله جرافات زي دي وأحسن وأحسن وأحسن بكتير تكون موضحة جدًا لكل التقدمات اللي بتحصل في جميع التجارب، uh يعني I think this. طيب فالـ claim is is great yes and we will add يعني graphs to this. طيب interpretation large models Coheres at Muji B = 2 mid-size 3-4 plateau at fixed N = 5. uh smallest peaks at N = 5 because its procedure documents are shorter. والله ده يعني ده، دي نظرية من نساي يعني. دي نظرية، Post hoc author theories. 8 billion at B versus 3 billion at N split the visible in data. but the visible documents are shorter claims need verification, compare actual procedure code links across models. هم الـ documents كلهم ما كانوا واحد؟ الـ length ما كان 128؟

**المتحدث 1:** أي، الـ length كان 128. لكن هسي هو قاعد يقارن بين حاجتين مختلفات، بين الـ adaptive والـ والـ repetition العادي. ده B 2 وده N 5 و 7.

**المتحدث 2:** أي هو هو ما قال إنه الموديلات الكبيرة قدمت أحسن أداء عند الهناي لمن كان يعني لو لاحظنا هنا الموديلات الكبيرة بنلقى إنه أحسن أداء عندها كان في البيتا اللي هي الجايس، جايس وآية. تمام؟ لكن ديل الموديلات الصغيرة كانوا كلهم 5 ولا 7، 5 ولا 7 في حين إنه الجايس عندنا إحنا عندنا Cohere 3 8 billion كان أحسن أداء عنده في N = 7 يعني، المشكلة وين؟

**المتحدث 1:** والأرقام دي بسيطة يعني ما فرق شديد، بين الـ N 5 والـ B 2 دي آية؟ ولا بين الـ 7، بين الـ 7 والـ B 2؟

**المتحدث 2:** أي أي فريق فريق أقل من 1%، الـ N 7 والـ B 2 فرق صغير جدًا يعني، أقل من 0.001، أقل من 0.001، يعني 6 من عشرة آلاف ده، ده فرق بسيط جدًا ما، ما بيدينا ما بيدينا بحاجة يعني ما بيدينا يعني حاجة ممكن نستند عليها. فأنا شايف ما نعمل أي interpretation، ما نعمل analysis للتفصيل ده.

**المتحدث 1:** أي، against الـ assumption بتاع point 4.4.3. طيب claim excessive repetition overweights the original query tokens and suppresses the useful expansion vocabulary. أنا أكبر لك هنا شوية. كويس كده؟

**المتحدث 2:** تحت تحت تحت يا زول قاعد تدينا وين إنت؟ أيوه.

**المتحدث 1:** طيب في 4.4.4. طيب claim excessive repetition overweights the original query tokens and suppresses the useful expansion vocabulary. check explicitly possible? the inverse term dilution explanation acceptable as discussion but present as explanation rather than proven mechanism. excessive repetition overweights the original query tokens and suppresses the useful expansion vocabulary.

**المتحدث 2:** ممم، يعني كأنه أنت لمن تزيدها شديد كأنه ما حصل expansion. يبقى بس مركز مع الـ query، مع الـ terms بتاعت الـ query. لكن أنت ما، يعني تجرب الحاجه دي شفت فيها نقصان يعني، نقصان واضح؟ ما بيحصل ليه سرعة ما شايف، من 5 لـ 7 ما في نزول كده كان يقولوا عليه؟

**المتحدث 1:** لا لا في نقصان، النقصان أي، هو من واحد لتلاتة زيادة، من تلاتة لخمسة زيادة، من خمسة لسبعة زيادة، سبعة لعشرة نقصان بسيط. لكن الزول ده هو ده قصده هو الـ متناقصة؟ اسمها شنو دي؟ اسمها شنو؟ والله متناقصة دي، نسيت أتذكرها شني. ياخي الكلمة الـ الـ الفائدة اللي اللي بتبقى بالماينص لمن تزيد. الفائدة اللي بتبقى بالماينص لمن تزيد. في غول ومُتناقصة؟

**المتحدث 2:** ياخي law of diminishing returns, diminishing return ياخي! آه! diminishing return.

**المتحدث 1:** اللي هي من 7 لـ 10 يا خواجة. من 7 لـ 10 يعني هو قال إنه في diminishing return وقال إنه الحاجة دي يعني هو سببها لأنه خلاص يعني الحاجة دي بتبقى كتيرة وبتغطي على الـ expansion ذاته.

**المتحدث 2:** لكن هو المفروض معاها يقل، يقل بصورة واضحة.

**المتحدث 1:** ما هو يعني يعني الفكرة إنه الفائدة بدت ما تزيد، يعني بقى الـ بقى الـ trend بقى ما ماشي زايد دي ما، وكونه إنه هو نقص فيهم كلهم فعلاً دي برضه حاجة. يعني عاين، كلهم كلهم كلهم بينقصوا. كلهم من 7 لـ 10 بينقصوا. ممم، ما نقصان ما واضح شديد لكن بيزيد شوية، لكن كله بينقص شوية. معناته في الغالب في الغالب إنت لو عملت 20 مثلاً، حتلقاه نقص.

**المتحدث 2:** ممم، أيوة أيوة.

**المتحدث 1:** إذا عملت 20 حتلقاه نقص، احتمال 20 يوضح الـ graph ده بصورة سمحة يعني.

**المتحدث 2:** ده كلام منطقي.

**المتحدث 1:** أي، فـ أي لكن يعني أها، ده، ده افتراض بس، ده افتراض إحنا إحنا حقيقة إحنا ما عارفين السبب بتاع الحاجة دي شنو يعني. ما هو هو قال ليك acceptable as discussions, right? as representing as explanation rather than proven mechanism. أي، إحنا بس نعمل الحاجة دي كتوضيح إنه ياخي البتاعة دي غالبًا حتنقص عشان كده، لكن ما إثبات، ولا findings هنطلع بيها. أيوه، طيب، framing query repetition "not a change of model was the missing ingredient" tutorial.

**المتحدث 2:** دي وين دي؟

**المتحدث 1:** في الـ thesis دي.

**المتحدث 2:** ما قريت الـ thesis دي؟

**المتحدث 1:** ياخي! يعني ما دي الحاجات اللي أنا شايف نركز عليها this confirm that query repetition not a change of model was the missing ingredient for the six originally degraded systems. لكن لقطة جميلة يعني!

**المتحدث 2:** بس الكلمة بتاعت ingredient يعني كلام...

**المتحدث 1:** أي the missing ingredient تخليها حاجة scientific يعني.

**المتحدث 2:** نحولها بصورة scientific أي ما دايرين حاجة energetic حاجة punchy.

**المتحدث 1:** جميل. أي طيب، والله يا زول ده دقيق يعني طيب، المكتوب الأول ما قريته يا زول. لا ده ما هو يا زول، ده summation يا زول، حشاو يا زول! طيب 26.7%، الزول ده لو غلط حا، القروش دي حنقعد ندفع فيها ساي إحنا. 26.7% improvement claim for Aya B = 2 grounded, grounded. uh correct. طيب Hybrid Fusion Results، طيب في عندنا أي assumption، إنه RRFK = 20, CC alpha = 0.5 are statistically indistinguishable in NDCG at 10. uh إحنا في الحقيقة ما عملنا statistical tests، T-test أو permutation test أيًا كانت أنا متذكر الـ T-test دي قريتها في حاجة إحصائية لكن متذكر كان شنو. was done عشان نشوف الفرق بين...

**المتحدث 2:** دي، بس عشان تعمله كم مرة بس، مش؟ تقريبًا.

**المتحدث 1:** practically identical but statistically indistinguishable implies a test. أيوه والله الزول ده صاحي ياخي! قال إنت ما ممكن تستعمل اللفظ ده ما لم إنت...

**المتحدث 2:** الله يسامحك، المشكلة، المشكلة! numerically، numerically جميلة جدًا. numerically numerically unless unless you run a... كويس كلامك صح ياخي يا عم obis. يا دي دي فحص حاجات عجيبة زازي ياخي. interpretation يا زول والله والله أنا بفكر أديه الـ thesis يا زول، بفكر أقول ليه أمسك، بركت الشغل ده!

**المتحدث 2:** جميل.

**المتحدث 1:** interpretation of CC boundaries at alpha = 0.9 the result is essentially MTPR alone. At uh alpha 0.1 the result 0.5248 is higher than BM25 alone because CC still picks up the dense retrievers' tie-breaking contribution. The tie-breaking explanation is plausible but unproven. We also see that min-max normalization rescales scores present as possibility not established.

**المتحدث 2:** min-max شنو؟ الفا بيساوي 9 دي ما قلنا الهناي مش؟ ده الـ بيور هناي، أو ما بيور، قريب للـ BM25؟

**المتحدث 1:** تقريبًا بيور، لا لا ده تقريبًا MPR، ده تقريبًا MPR. الفا بيساوي 0.1 ده، أي، ده ده الـ BM25. فهو قال ليك، قال ليك لما...

**المتحدث 2:** آه ما كلام إنه ده. نفسه. ده نفسه لكن لمن كان 0.1 كان أكتر منه. لكن ده أكتر منه. لأنه قال لك مرات بياخد الـ dense في الـ tie-breaking contribution.

**المتحدث 1:** والله الكلام ده إنت تفهم فيه أكتر مني أنا يا، يا عم Obis! فـ present as possibility not established mechanism.

**المتحدث 2:** ده افتراض منه، هو ما افتراض منه!

**المتحدث 1:** الزول ده الفا بيساوي واحد ده ما، ما بيور، ما بيور BM25. فـ فيه حاجة من الـ dense. الكلام الغريب يعني ما هو فعلاً فخلاص دي معناها حسنت الموضوع، لكن الهناك التانية داك، الما كان بيور dense في نفس النتائج، ما عارف شايفة دي كده غطت أي تفسير. أي، دي تفسيرها واضح يعني إنه دي فعلاً ياخي هو شال جزء من الـ dense الـ .1 دي ولا شنو؟

**المتحدث 2:** ما هو دي برضه يعني كونه دي أحسن، أو دي أسوأ يعني يعني هو المفترض الـ tie-breaking ده 0.1 دي مفترض الـ tie-breaking بتاع الـ BM25 يحسن النتائج بتاعتها بتاعت الـ بتاعت الـ hybrid أي أحسن أحسن تكون أحسن من الـ dense، إلا إلا إذا شنو، إلا إذا شنو، إلا إذا أصلاً مثلاً في ميكانيزم أصلاً already جوه بتقول إذا في tie-break دائمًا شيل الـ dense، بس إلا في الحالة دي، وبالتالي أثر الـ BM25 لمن يكون الـ majority للـ dense زي الـ 0.9 بيكون بسيط يعني. قال لك هل في أصلاً يعني في...

**المتحدث 1:** أظن أظن حيكون في setup زي ده، حيكون في setup ده يعني الحاجات دي، إنه إذا، إنه إذا في tie-break، يا تشيل الـ BM25 يا تشيل الـ dense، احتمال يكون الـ setup إنه يشيل الـ dense عشان كده لمن الـ BM25 الأثر ده بيظهر، هناك ما بيظهر.

**المتحدث 2:** طيب دي كده معناها assumption عجيبة جدًا.

**المتحدث 1:** لا لا ما assumption صح!

**المتحدث 2:** لا الـ tie breaking ده هل هو موجود أصلاً ولا ما موجود يعني؟

**المتحدث 1:** ده لازم يكون فيه. ما ممكن يكون قطعه من راسه.

**المتحدث 2:** لا وإنت الـ tie breaking ده يعني منطقيًا حاجة منطقية تكون في الـ tie. يعني جد جد يعني لو حصل tie حيحصل شنو؟ حتى لو كان hybrid، لو حصل tie كيف يعني دي؟ والله بالذات أنا ما قادر أفهم الحاجة دي قاعد يحصل fusion كيف. وما أي واحد بأرقام مختلفة. أنا هسي الاختلاف كيف يعني حيحصل الـ tie ده؟

**المتحدث 1:** إنت هسي بتجيب ده وتخت دي حاجة يعني بتخت دي حاجة على شي على حسب الرقم بتاعك.

**المتحدث 2:** والله ما عارف والله، ما عارف والله صراحةً. إنت بتدي score لده في ده بنسبة، زائد score ده في نسبته، بتطلع ليك الـ score بتاع الـ document.

**المتحدث 1:** أها.

**المتحدث 2:** تقريبًا وما عارف فعلاً الـ tie حيكون بالـ document to document، حاجة تعامل معها كيف؟

**المتحدث 1:** والله يا أخي كدي... we don't understand the concept of tie-break. if we had time please, uh, we will let the AI explain it for us. but for now we accept the AI uh point that we should present this as possibility, not as established mechanism because for sure we don't understand what is happening and we didn't do enough tests on that and we didn't measure this perfectly. طيب point 4.4.9 declarative claim uh 6267 NDCG at 10 higher baseline the target that all subsequent clear enhancement methods must surpass. this framing factually correct it is your non-QE ceilings up declarative.

**المتحدث 2:** ده الـ non هناي مش؟ أيوة Non-QE. ممم بتاع الـ paper بتاع الميريكل، أي.

**المتحدث 1:** أي، acceptable as thesis narrative. كويس. لكن هو surpass في الـ hybrids وبدونهم أي ولا ما فرقت؟

**المتحدث 2:** ممم.

**المتحدث 1:** يعني إحنا كأنه ختينا baseline جديد، في نص الكلام. إحنا الـ baseline بتاعنا كان من دون الـ hybrid.

**المتحدث 2:** ممم.

**المتحدث 1:** طيب الـ hybrid ده بنخته قدام مع الـ baselines بتاعتنا بس.

**المتحدث 2:** يعني نخته مع الـ baselines بس؟

**المتحدث 1:** أي. أي بس تمام. تمام.

**المتحدث 2:** طيب The Call At 100 cited as كدة rather than كدة. يا أخي تخريب يا أخي! تخريب يا ابني يا أخي! brief correctly identified. and recommend verify across all tables.

**المتحدث 1:** قال لك بس الـ consistency matters خلينا نشوف 9466 دي دي دي. Cloud stream. حلو. حلو. حلو. حلو. حلو. 7 6 ياهم، شكرًا جزيلاً. شكرًا جزيلاً، الرقم ما مرتب أيوة. جميل.

**المتحدث 2:** طيب uh corpus test query enhancement interpreted dense encoder was trained on short natural language query and long expansion degrades the embedding quality.

**المتحدث 1:** وين وين الـ degrading حصل؟ أها الـ degrading، البتاع ده بقى بقى كويس الـ dense يعني، plausible but unconfirmed. لا لا بعدين إنت لمن تعمله إنت عشان كده جيت تعمله dense only أو BM25 only. لأنه الحاجة دي كسرتها إنه يا أخي الـ expansion بتاعك ده بياثر على الـ dense بتاعك. الـ dense أصلاً هو مدرب على إنه بس الـ query براها. وإنت كترتها شديد يعني في الـ expansion.

**المتحدث 2:** لكن، لكن الـ dense بتاع الـ corpus steered query enhancement أحسن من الـ query enhancement العادية! أيوة، أحسن من الـ query enhancement العادية! دي قاعدة. دي دي دي المقارنة بتاعة. إنت أهو، إنت الكاربيتيشن حنقارنه مع الـ BM25 بس معناها!

**المتحدث 1:** أي إنت يعني إنت كمان إنت ما تعملي، يا تقول لي هو حسّن حسّن الـ BM25 بصورة كويسة، لكن ما تقول لي عمل عمل عمل degradation يعني degradation، لأنه يعني أنا عندي آية، آية corpus steered عندي الـ NDCG كم؟ 0.59، 0.59. الـ BM25 0.61. طيب أنا عندي، أنا عندي آية تحت، آية تحت، أنا عندي آية هنا أنا عندي آية expansion 0.50 بالـ BM25. طيب أنا عندي آية بالـ dense، عندي آية بالـ dense 0.61. أوبا! أوبا! باااه. الصفين ديل المقارنة بيناتهم مهمة جدًا! حاجة عجيبة! الـ dense الـ blind، الـ blind أحسن من الهناي. الأرقام دي شديد verified.

**المتحدث 2:** الأرقام دي first of all should be verified. إن إحنا عندنا آية، عندنا آية كان 50.

**المتحدث 1:** إنت لا لا لا لا لا، إنت كلامك داك في الهناي، في الـ hybrid. إنه إنت الـ BM25 بيكون blind والـ dense بيكون corpus steered is still هو حيكون أحسن من شنو، من من الـ dense براهو، و still أحسن من الـ hybrid بدون الهناي، بدون الـ corpus steered. التحت التحت في التيبل التحت ده تحت تاني. والله أنا كلامي كان النقطة دي لكن إنت نقطتك دي برضه كويسة. يعني أنا عندي، أنا ما عملت الـ hybrid، ما عملت الـ hybrid للـ query enhancement. ما عارف ما عارف.

**المتحدث 2:** لا لا مالي الـ query enhancement.

**المتحدث 1:** أيوه ما فاهم الفكرة. لا لا الـ hybrid العادي ده ما بقدر أعمل له حاجة. هو، هو قصده قصده المقارنة، المقارنة ما بين شنو؟ المقارنة ما بين الـ blind query enhancement وما بين الـ corpus steered query enhancement. قال لك بوضوح قال لك الـ corpus steered query enhancement خلت نتائج بتاعت الـ dense لو خليته براهو، لو بقيت معاه BM25 ممكن يرفعها ليك، لكن لو خليته براهو بينقصها، الحاجة دي موثقة وين، موثقة في الرقمين ديل. موثقة في الرقمين ديل! يعني حصله degradation عديل، الـ dense البراهو ده حصله degradation. بس ديل أرقام محتاجة verification صراحةً. واحتمال احتمال إنت هسي لو عملت الـ blind ده، الـ blind ده لو عملت ليه hybrid لو عملت ليه hybrid احتمال تطلع درجته أحسن من الـ أحسن من الـ hybrid اللي هو config c اللي هو إنت عامل، اللي هو إنت عامل الـ BM25 اللي هو config B اللي عامل BM25 مع الـ dense الـ corpus steered. احتمال الـ hybrid داك يطلع أحسن منه.

**المتحدث 2:** ما ديل بيتساووا؟

**المتحدث 1:** لا الـ hybrid بتاع ديلك...

**المتحدث 2:** لا بتاع الـ blind، الـ hybrid بتاع الـ blind مافي. ده طبعًا hybrid بتاع الـ blind.

**المتحدث 1:** لا تحت تحت، الـ A الـ A ده blind، الـ dense blind؟ أنا قصدي ليك blind مع blind، أنا قصدي ليك blind مع blind، A ده BM25 مع corpus steered مع dense blind؟ أها، يكون enhanced؟ أي أها، قصدك enhanced أي أي أي. عادي، أي، تجربة كنا مفروض نجربها كان لقينا زمن. أيوه أيوه أيوه، ودي أنا هسي يعني إذا إذا إذا إنت عندك إذا إنت عندك الـ blind أحسن من الـ dense براهو، فـ ممكن الـ blind مع الـ blind يكون أحسن من الـ blind من الـ blind بتاع الـ BM25 مع الـ dense مع الـ dense والـ corpus steered. عرفت؟ إنت كده حتثبت، إذا فعلاً الـ blind مع الـ blind أحسن، معناها إنت فعلاً كده حتثبت إنه، إنه الـ corpus steered قاعد يعمل degradation للـ dense بتاع الـ dense. قاعد يعمل degradation للنتائج بتاعت الـ dense. وإنت كده حتثبت...

**المتحدث 2:** هسي ده ما مثبت برضه، هسي مثبت ما. هسي هو مثبت، هسي هو مثبت فعلاً لدرجة ما، من النقطة التم ذكراها هسي دي اللي هي بتاعت إيه...

**المتحدث 1:** فوق. أيوة، section، طيب..

**المتحدث 2:** أنا ما عارف والله.

**المتحدث 1:** أيوة. 1500 character دي إحنا ما قسناها. أنا ما عارف إنه الـ dense إذا مدرب على الـ short ولا لا. لكن عمومًا النتائج بتثبت كده. والله لو لقينا طريقة نعمل التجربة دي وهي تجربة ما معقدة إن شاء الله، بنقدر نعملها. نعمل التجربة بتاعت الـ blind hybrid.

**المتحدث 2:** دقيقة دقيقة، blind hybrid يعني يكون الهناي ده blind وده blind.

**المتحدث 1:** أي، blind وblind بس. إحنا ما سويناه؟ دي ما سويناها للاسف.

**المتحدث 2:** لا لا أنا ما سويتها أنا. أنا ما تجارب دي ما عملتها أنا. الـ hybrid، الـ hybrid اللي إنت بتعمل فيه، الـ hybrid اللي إنت كنت بتعمل فيهو..

**المتحدث 1:** الـ hybrid ده هناي إنت بتجرب شنو؟ hybrid سادة؟

**المتحدث 2:** ما جربت hybrid للـ blind بس. عملت repetition للموديلز، عملت repetition للموديلز كلها. عملت hybrid لشنو؟ عملت hybrid للهناي ذاتها. لتجاربك القديمة. لكن ما عملت hybrid للـ models كلها. ممكن أعمل hybrid لـ آية.

**المتحدث 1:** لتجاربك القديمة؟ دقيقة، تجاربك القديمة دي ما ياها؟ ياها الـ blind ذاتها!

**المتحدث 2:** لا لا، لا لا، ما تجاربك، ما تجاربك بتاعة الـ blind، تجاربك الأولى الـ blind، لمن عملت blind.

**المتحدث 1:** أيوة أيوة، أيوه، أيوه.

**المتحدث 2:** خلاص تمام.

**المتحدث 1:** تمام يلا وقف الريكوردينج.