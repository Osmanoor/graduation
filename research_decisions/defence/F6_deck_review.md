# F6 · Review of `Thesis defense presentation design.pptx`

**Reviewed:** 2026-08-14 · 20 slides (13 main + 7 backup) · against Ch1–Ch5 and Parts 1–4 drafts.

**Verdict: the deck is in good shape.** Structure matches Dr. Tahani's mandated order, the timings
sum to 595s against a 600s budget, the Arabic speaker notes are thorough, and the backup slides are
well chosen — slide 18's caution about 0.6936 vs 0.7137 is exactly right, and slide 15's
"never say longer is better" note prevents a real trap.

Changes below are ordered by risk. **A–E are checkable against the thesis** and are the ones that
matter.

---

## ⛔ MUST FIX

### A · There is no agenda slide — add one as slide 2

Dr. Tahani, Note 9, verbatim: *"الصفحة التانية لازم يكون فيها الـ agenda… أنا مرتبة أنا حتكلم عن شنو
ثم شنو ثم شنو."* She is on the panel and this is the one structural item she named explicitly.
The deck currently goes cover → "From LLMs to RAG".

Add: Problem · Objectives · Methodology · Results & Discussion · Conclusion. Five lines, ~20s.

### B · Slide 9 — the number 143 is being used in the wrong direction

**Notes 9 say:** *"والانقلاب الكامل ده حصل في 143 سؤال من 2,896"* — i.e. blind expansion broke 143
already-solved queries.

**The thesis says the opposite.** `chapter4.tex:787`:

> Among the 1,061 big-win queries (Δ > 0.3) … in 463 the blind baseline scored 0.000 while CSQE
> recovered the query, and **in 143 of these the recovery was complete (CSQE NDCG@10 = 1.000)**.

143 counts **CSQE recoveries** (blind 0.000 → CSQE 1.000), not blind failures (1.000 → 0.000).
This error originated in `F1_defence_script.md` and was inherited — my fault, not yours.

**Fix the sentence, keep the number:**

> «في 143 سؤال، الـ blind expansion جابت صفر، والـ corpus grounding رجّعتها لـ 1.000 كاملة.»

Just as strong, now checkable, and it lands on slide 9→10 exactly where you need the bridge.
**Do not claim a count for how often blind expansion breaks a solved query** — the thesis does not
report that figure.

### C · Slide 8 — "the first single-model experiment showed clear improvement" is false for BM25

**Notes 8 say:** *"طبقنا الفكرة أول مرة بموديل واحد، ولقينا تحسن واضح."*
**Part 3.md says it more explicitly and more wrongly:** *"بالنسبة للـ BM25 وبالنسبة للـ Sparse،
الاثنين النتائج اتتحسنت بصورة واضحة."*

Thesis, Tables 4.3 and 4.4 — Qwen 2.5 3B, the single model used first:

| Retriever | Baseline | Query2Doc | Change |
|---|---|---|---|
| mDPR (dense) | 0.4993 | 0.5435 | **+8.9%** |
| BM25S (sparse) | 0.4621 | 0.4090 | **−11.5%** |

Dense improved. **Sparse degraded by 11.5%.** Both tables are in Chapter 4 and an examiner can open
them.

**And the correct version is a better story** — the split you build the whole talk on appears in
your very first experiment:

> «أول تجربة بموديل واحد: الـ dense اتحسن 8.9%، لكن الـ BM25 نزل 11.5%. الانقسام ده ظهر من أول
> تجربة — وهو اللي ودانا للمقارنة بين عشرة موديلات.»

*(Separate slip in Part 3.md: "الـ BM25 وبالـ Sparse" — those are the same thing. You mean dense and
sparse. Say it that way or the panel will think you tested three retrievers.)*

### D · Notes 11 — the novelty claim is broader than your own Chapter 2 supports

**Notes 11:** *"وحسب مراجعتنا لليتريتشر، الـ asymmetric assignment ده ما اتدرست قبل كده."*

Your own `chapter2.tex:410` cites the closest prior art and is careful about it:

> While **Exp4Fuse** (Liu et al. 2025) shows that fusing the original- and expanded-query result
> lists from a *single sparse* retriever outperforms using the expansion alone, the asymmetric
> assignment of expansion across retriever *types* in a heterogeneous dense–sparse hybrid — and its
> behaviour for Arabic — has not been studied.

An examiner who opens Chapter 2 finds Exp4Fuse cited. **Use the thesis wording**, which is narrower
and fully defensible: not "nobody has studied asymmetric assignment", but "nobody has studied it
*across retriever types in a dense–sparse hybrid, for Arabic*."

If asked whether it is new, **name Exp4Fuse yourself first**, then state the narrow claim. Volunteering
the nearest prior art reads as command of the literature; being shown it reads as a gap in your reading.

### E · Notes 11 — the "out-of-distribution" explanation is not in the thesis

**Notes 11:** *"الـ mDPR متدرب على كويريز قصيرة، والكويري الموسعة out-of-distribution ليهو."*

Plausible, but you never tested it, and *"did you measure that?"* is an easy follow-up with no good
answer. The thesis explanation (Ch5, conclusion ix) is the one you can defend:

> Applying CSQE to both retrievers **reduced the complementarity** between their ranked lists,
> lowering the fusion ceiling; applying it only to BM25 preserved the dense retriever's independent
> semantic signal.

Your notes already say this immediately afterwards. **Drop the OOD sentence**, or mark it audibly as
interpretation ("تفسيرنا إنو…"). Do not present it as a finding.

---

## ⚠️ SHOULD FIX

### F · Slide 9 gives away slide 10

Slide 9 currently carries *"✓ CORPUS-GROUNDED (next slide) «أبٌ، أخٌ، حمٌ، فو، ذو» → correct passage
retrieved"*. That is the punchline of slide 10, spent one slide early.

**End slide 9 on the failure: 1.000 → 0.000, and nothing else.** Let the room sit with the broken
query. Slide 10 then delivers the recovery, which is where the method earns its introduction.

### G · Adding the agenda puts you 20s over — take it from slide 5

Current: 595s + cover. Plus agenda = ~615s. Trim **slide 5 from 0:55 → 0:40** — notes 5 carries both
the theory and the dataset setup, and the theory half is exactly what Dr. Tahani caps. Keep the
complementarity line; it is load-bearing for slide 11.

### H · Slide 12 — say "largest *proportional* gain"

Slide 12 says short queries "+43.6% — the largest gain". In **absolute** terms 4–8 word queries gained
more: **+0.197 vs +0.161** (Table 4.19). The claim is true only proportionally, and a jury member with
that table open can catch it. One word fixes it.

### I · Table 4.26 prints the query without «في اللغة العربية»

The deck uses the full query — correct, and strictly stronger, because the model was *told* the domain
and still failed. But the thesis table abbreviates it. If an examiner opens Table 4.26 and sees a
different string, have the answer ready: the table abbreviates; the full query is what was run, and it
is in `enhanced_queries_aya_expanse_8b.pkl`. *(Already noted in `F1_csqe_example.md` Part D.)*

---

## 📝 CORRECTIONS TO THE SPOKEN DRAFTS — the deck is right, the drafts are not

These never reached the slides. Fix them in Parts 3–4 so nobody says them aloud.

| # | Draft says | Correct |
|---|---|---|
| J | **Part 3:** "8 موديلز" | **Ten** evaluated, nine viable. Deck and thesis both say 10. |
| K | **Part 4:** hallucinated names «أحمد، إسماعيل، مبارك، خالد، منصر» | Real output is «**محمد، آدم، إبراهيم، إسماعيل**» — traced to `enhanced_queries_aya_expanse_8b.pkl`. The deck has it right. This is real experimental output shown to a jury; it must match the file. |
| L | **Part 4:** "إحنا ما عملنا أدابشن، إحنا بس جبنا الإنجلش وجبناه في العربي" | Contradicts slide 13's headline (**"Yes, but not unmodified"**) and Ch5's conclusion that three adaptations were required. You cannot say both. The deck is right. |
| M | **Part 4:** short queries benefited "about 80%" | Not in the thesis. The real figure is **+43.6% proportional gain** for 1–3 word queries. Do not say 80. |
| N | **Part 4:** hybrid = "نشوف الأحسن من الاثنين" | RRF does not pick the better list — it **fuses the ranks** of both. Small, but directly probe-able. |
| O | **Part 4:** "0.71 مقارنة بـ 0.48، أنا ما متأكد من الرقم الأول" | The baseline is **0.4621**. Slide 12's +54.5% is computed correctly — trust the deck, not the memory. |

---

## ✅ Verified correct — do not change these

- Slide 6: mDPR 0.4993 = official MIRACL result exactly; BM25S 0.4621 = 96% of Pyserini *(ch4:30)*
- Slide 6: 34% fail · ~10% nothing at top-100 · 0.345 for 1–3 word queries
- Slide 9: the blind output محمد/آدم/إبراهيم/إسماعيل, and 1.000 → 0.000
- Slide 10: ablation 0.5381 / 0.5752 / 0.6157, and the 2 corpus + 2 blind + α=4 config
- Slide 11: 0.6267 / 0.6474 / 0.6936 / **0.7137** — all RRF, consistently, no CC values mixed in
- Slide 12: +54.5% · +13.9% · 56.8% · mean +0.189
- Slide 15 backup: the non-monotonic warning
- Slide 18 backup: the 0.6936-vs-0.7137 caution — this is the single best backup slide in the deck

---

## Order to apply

1. **B and C first** — they are wrong numbers in the spoken notes, and they are the two an examiner
   is most likely to check.
2. **A** — add the agenda slide, trim slide 5 by 15s.
3. **D and E** — soften the two claims in notes 11.
4. **F** — move the corpus-grounded reveal off slide 9.
5. **H** — one word on slide 12.
6. **J–O** — mark up Parts 3 and 4 so the rehearsal uses the corrected wording.
