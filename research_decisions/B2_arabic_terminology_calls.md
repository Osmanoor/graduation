# B2 — Arabic abstract: terminology judgement calls

**Date:** 2026-08-08
**For review by:** Elhaj **and** Osman, before submission.
**Files changed:** `5-Abstract.tex` (English, revised), `6-ARAbstract.tex` (Arabic, re-derived).

---

## 0. Read this first

Dr. Tahani's instruction (voice note 13):

> *"الترجمة حاولوا بقدر الإمكان ما تكون ترجمة Google ولا ترجمة AI، حاولوا استخدموا الـ terminologies
> المستخدمة عندنا في اللغة العربية الصحيحة."*

**The Arabic below was drafted with AI assistance.** That is exactly what she warned about.

**Elhaj's decision, 2026-08-08:** offered the choice between Osman rewriting the Arabic in his own
voice and shipping this draft for the two of them to review, **he chose to ship the draft and
review it.** The risk is accepted knowingly. What remains is not optional, though:

1. **Read it aloud, both of you.** Anything that sounds translated, rewrite it. The meaning must
   not change; the phrasing may.
2. **Sign off on the term table in §2.** Every row is a decision, not a fact.

The draft was written to avoid the usual machine-translation tells: no em dashes, Arabic sentence
order rather than mirrored English clauses, and connectives (`غير أن`, `ومن ثَمَّ`, `وبذلك`)
chosen for Arabic rhythm. That reduces the risk. It does not remove it — she reads Arabic natively
and will be reading this one personally.

---

## 1. How the draft was produced

Three independent drafts, then reconciled:

| Source | Words | Notes |
|---|---|---|
| Mine | 343 | base; kept the placement evidence and the mechanism |
| Gemini 3.1 Pro | 376 | too long; good on `مدوَّنة`, `أساليب` vs `النماذج` ambiguity |
| GPT-5.5 | 270 | tightest; best call on `blind` and on `term dilution` |

Each was given the approved English and the same rules, without seeing the others. Where two of
three agreed independently, I took the agreed term. Where they disagreed, §2 records why.

Verified by web search against Arabic IR/NLP usage: `التوليد المعزَّز بالاسترجاع`,
`النماذج اللغوية الكبيرة`, `الاسترجاع الكثيف`, `توسيع الاستعلام`.

---

## 2. Judgement calls — each one needs a yes or no

| # | English | Chosen | Rejected | Why |
|---|---|---|---|---|
| 1 | Retrieval-Augmented Generation | التوليد المعزَّز بالاسترجاع | التوليد المحسَّن / المدعوم بالاسترجاع | Used by IBM Arabic and MIT Tech Review Arabic. Both models agreed independently. Same term as the old abstract. |
| 2 | proprietary models | **نماذج احتكارية** | نماذج مملوكة | **Reversed 2026-08-08 after expert review.** I had chosen `مملوكة`, worried that `احتكارية` implies monopoly. Four independent opinions said otherwise: `مملوكة` reads as a commercial-ownership term, and every model has an owner, so it fails to carry the "closed" sense. If the point is specifically that the weights are not released, `نماذج مغلقة الأوزان` is the sharper alternative. |
| 3 | modular remedy | حلاً يمكن إضافته دون تغيير بقية النظام | حلاً تركيبياً / علاجاً معيارياً | The models split, and neither term is settled Arabic. A short gloss says the thing plainly instead of betting on a contested word. Costs 4 words. |
| 4 | blind QE | **الأعمى** | غير الموجَّه | **Reversed 2026-08-08 after expert review.** GPT-5.5 had argued `أعمى` reads like a literal translation. Both expert reviews disagreed and gave the reason: `الأعمى` is the *established* term in Arabic IR writing, by analogy with Blind Relevance Feedback. An established term cannot read as a machine translation. |
| 5 | corpus | المدوَّنة | المتن / المجموعة | All three agreed. Standard in Arabic NLP. |
| 6 | paradigms (sparse/dense/hybrid) | أنماط الاسترجاع | النماذج | `النماذج` would collide with "models" in the same sentence. Gemini caught this. |
| 7 | term dilution | **تخفيف أوزان مصطلحات الاستعلام الأصلية** | إضعاف وزن… / تمييع المصطلحات | **Refined 2026-08-08.** The mechanism description stays — no settled Arabic term exists — but both experts flagged my phrasing as clumsy and agreed on `تخفيف أوزان`. Also fixes a number-agreement wobble (`وزن` singular against `مصطلحات` plural). |
| 8 | NDCG | **الكسب التراكمي المخصوم المُعيَّر** (NDCG@10) | … المُطبَّع | **Changed 2026-08-08.** **No settled Arabic term exists** — the web search found none. All four opinions agreed on `الكسب التراكمي المخصوم` and split on *Normalised*. I originally took `مُطبَّع` (`التطبيع` being standard for normalisation in machine learning); the expert round went 2-in-favour of `مُعيَّر`, with Gemini calling `مُطبَّع` actively jarring. **This is the weakest row in the table — it is a coin-flip between two defensible words. If Dr. Tahani has a preference, take hers.** GPT-5.6 offered a third route: drop the Arabic gloss and write `مقياس NDCG@10` alone, which is defensible precisely *because* no standard equivalent exists. |
| 9 | parameters (model size) | معلمة (8 مليارات معلمة) | معامل | **Changed from the old abstract**, which said `معامل`. **Held against a direct challenge:** Gemini's expert review argued for `معامل` in an electronics context. GPT-5.6 explicitly said not to — `معامل` is *coefficient* or *factor*; `معلمة` is the parameter of a model. Three of four opinions back `معلمة`. |
| 10 | pipeline | المسار الهجين | خط الأنابيب | Literal rendering is wrong in Arabic software writing. Both models agreed. |
| 11 | openly available | متاحة علناً | مفتوحة المصدر | The thesis does not claim these models are open-source — Aya Expanse is CC-BY-NC. `متاحة علناً` is the accurate claim. |
| 12 | MIRACL, BM25, BM25S, mDPR, Query2Doc, CSQE | left in Latin script | Arabised | Product and dataset names, not translatable concepts. Dr. Tahani's rule is Arabic term first *where a standard Arabic equivalent exists*; for these it does not. CSQE additionally carries its Arabic gloss `التوسيع الموجَّه بالمدوَّنة` before the acronym. |

---

## 2b. Expert review round — 2026-08-08

After the draft was applied, it was sent to two models in **expert-reviewer mode** (not drafting
mode): Gemini 3.1 Pro and GPT-5.6-terra, each asked to judge as an Arabic-native academic whether
the text reads machine-translated, and to quote the specific phrases that give it away.

**Both scored it 6–6.5 out of 10 and said a practised supervisor would sense AI involvement.**
That is the most useful result in this whole file: it confirms Dr. Tahani's concern was not
paranoia, and it says the earlier draft was *not* safe to ship unchanged.

Fixes applied where both reviewers independently flagged the same phrase:

| Was | Now | Why |
|---|---|---|
| إرساء خطوط الأساس | وضع خطوط أساس | `إرساء` is a literal rendering of *establish*; not the verb used in Arabic experimental reports |
| تطويع | تكييف | `تطويع` reads generated; `تكييف` is the standard for *adapt* |
| معرفة النموذج المخزَّنة | المعرفة الكامنة في النموذج | literal calque of *stored knowledge* |
| وقد حسَّن تحسين الاستعلام… | وقد حسَّن توسيع الاستعلام… | the `حسّن/تحسين` echo was the single most obvious AI tell |
| نماذج مولِّدة | نماذج توليدية | `توليدية` is the Arabic academic adjective |
| متاحة علناً | متاحة للعموم | `علناً` is a weak rendering of *publicly* |
| المسار الهجين / معمارية هجينة | النظام الهجين / بنية هجينة | `مسار` and `معمارية` are direct calques |
| القسم العربي… وفيه | الجزء العربي… الذي يضم | `وفيه` separates the figure from its referent |
| كشف تحليل الأخطاء عن إخفاق | أظهر تحليل الأخطاء إخفاق | `كشف عن` is journalistic, not experimental |
| ثم تبيَّن أن الموضع | وتبيَّن أن موضع تطبيق التوسيع | "the placement" alone was ambiguous — placement of what? |
| بحجم 8 مليارات معلمة | يضم 8 مليارات معلمة | parameters are not a "size" in Arabic |
| تباين الرسم الإملائي | التباين الإملائي | shorter and more common |
| the long `فقصْر… على… وعلى قصْره…` sentence | rebuilt around `إذ تفوَّق تطبيقه…` | both reviewers called it the heaviest sentence in the text |

**One reviewer suggestion was rejected:** Gemini wanted `الاسترجاع المتناثر` → `الاسترجاع المتخلخل`.
GPT-5.6 said `المتناثر` is correct and should not change, the earlier GPT-5.5 draft used it, and so
did the old Arabic abstract. Three against one.

**One question GPT-5.6 raised that resolved itself:** it asked whether `QE` means Query *Expansion*
(→ `توسيع الاستعلام`) or Query *Enhancement* (→ `تحسين الاستعلام`). In this thesis it is
Enhancement, the broader term, with expansion as the specific technique — so `تحسين الاستعلام` for
QE and `توسيع` for the expansion itself is correct, and the text already made that distinction.

---

## 3. Compliance with her stated rules

| Rule | Status |
|---|---|
| ≈ ¾ page | **77% of the text block (538pt of 700pt).** Was 2 pages. |
| Never spills to a second page | Verified by full build — `1-main.pdf` p6, one page |
| One paragraph | Yes. Was four. |
| Arabic term first, English acronym after | RAG, LLM, QE, CSQE, NDCG@10 all follow this |
| Western digits | Yes — no Arabic-Indic digits present (checked programmatically) |
| Re-derived from the new English, not patched | Yes — the old text carried the pre-B1 framing Phase A removed |

**Dropped from the old Arabic abstract**, because the new English no longer claims them:
- the named per-model results (Aya +23.5% dense, Jais-2 +10.8% sparse);
- the "3B model beat GPT-3 175B" comparison;
- `ارتبط حجم النموذج إيجابياً بتحسّن الاسترجاع الكثيف` — a flat model-size claim that
  **contradicts** Chapter 5, which states it only with heavy qualification. This one had to go
  regardless of length.

---

## 4. Build verification

Full `xelatex` run on `1-main.tex`: **0 errors, 125 pages.**
p5 English abstract (1 page) → p6 المستخلص (1 page) → p7 Contents.
