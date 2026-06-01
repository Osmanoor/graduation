# Workstream 4 — Verification Report (Small Fact-Checks)

**Date:** 2026-05-30
**Scope:** Tasks 4.1–4.17 in `research_decisions/THESIS_NEXT_STEPS_TASKS.md` (Workstream 4 — "Verifications")
**Method:** Each item checked against the actual notebooks, source code, saved result files (`.pkl`), the thesis LaTeX, `References.bib`, and — where the claim concerns an external paper/model — the primary source on the web.
**Status legend:** ✅ VERIFIED (claim holds) · ⚠️ NEEDS EDIT (claim wrong/imprecise; fix required) · ❌ FAILED (claim unsupported) · 🔎 PARTIAL (in-repo evidence only; some part not checkable here)

> **Team review (Osman + Elhaj, 2026-05-31):** This report was walked through item-by-item in a review meeting. The verified items were accepted without revisiting. Decisions and notes from that meeting are recorded inline under **“Team decision”** in each relevant entry. Net changes from the meeting: **4.4** → adopt **OALL** as the base benchmark and standardise the generic "Arabic NLP benchmark" phrasing to OALL **thesis-wide** (sweep); **4.5** → keep as-is (the 30% mAP claim lives in the literature/“modern” review and is correct); **4.11** → downgraded to **PARTIAL** (depends on Workstream 1 integrity check); **4.16** → only **table/figure** labels need fixing (unused section labels are harmless); **4.17** → Config-A/C is a naming + Config-A error-analysis re-run, assigned to **Workstream 1**.

---

## Summary table

| # | What was checked | Verdict | One-line outcome |
|---|------------------|---------|------------------|
| 4.1 | GPT-OSS "English-dominant" | ✅ VERIFIED | Official model card: "trained on trillions of **mostly English** text-only data." |
| 4.2 | BM25S params (k1/b) | ✅ VERIFIED | Index built with **k1=0.9, b=0.4, method="lucene"**. §2.3.2's k1=1.5/b=0.75 is wrong. |
| 4.3 | SILMA temperatures | ⚠️ NEEDS EDIT | SILMA was run at **0.1 and 0.7** (two saved pkls). Not 0.0. |
| 4.4 | Which Arabic benchmark in §4.7 | ⚠️ NEEDS EDIT | §4.7 names **no single benchmark**; team decision → standardise generic "Arabic NLP benchmark" → **OALL thesis-wide** `[SWEEP]` (keep Ch.2 per-model scores + MIRACL-dataset mentions as-is). |
| 4.5 | CSQE "30% mAP over BM25" | ✅ VERIFIED *(corrected 2026-05-30)* | TREC DL19 mAP: BM25 **30.1** → CSQE Llama2-Chat-7B **39.1** = **+29.9% ≈ 30%** (Table 3 + Table 7). GPT-3.5 reaches 47.2. *(My first pass wrongly read only the BEIR nDCG@10 table and marked this FAILED.)* |
| 4.6 | Retrieval depth in hybrid exp | ✅ VERIFIED | Depth = **top-100** everywhere (`k=100`). Not top-1000. |
| 4.7 | CSQE temp=1.0 | ✅ VERIFIED | Config + every generate call use **temperature=1.0, do_sample=True**. |
| 4.8 | First-pass "relevant" = qrel ≥1 or ≥2 | ✅ VERIFIED (by data) | MIRACL qrels are **binary**; only qrel≥1 is meaningful. (Analysis notebook not in repo.) |
| 4.9 | CSQE expansion ≈1500 chars | ✅ VERIFIED | Computed from pkl: **mean 1486, median 1530** chars (orig mean 29.5). |
| 4.10 | "mDPR trained on short queries" | ✅ VERIFIED (citable) | mDPR = `mdpr-tied-pft-msmarco`, fine-tuned on MS MARCO (short Bing web queries). Cite Bajaj et al. 2016. |
| 4.11 | 258 failures: exhaustive or sampled | 🔎 PARTIAL *(team-revised)* | Inspection **was exhaustive** (all 258 classified), **but** the "irretrievable" conclusion depends on the WS1 dataset-integrity check → mark PARTIAL. |
| 4.12 | Three big-win examples | ✅ RESOLVED *(2026-05-31)* | Final trio chosen + **score-verified** (blind 0.000 → CSQE 1.000): **الرباط المنصوري (10061), الأسماء الخمسة (3034), الفن الجزيري (11753)**. Verbatim expansions to paste into §4.10 are in the detailed entry. |
| 4.13 | Type B "first-pass poisoning" (general mode) | ✅ RESOLVED *(2026-05-31)* | **Reframed to the general Type-B pattern** (131 queries, homonym/name collisions poison BM25's first pass → CSQE grounds on wrong docs; blind ignores first pass and succeeds). Documented as a representative *set* (928 ماهو-homonym, 11371 نجيب محفوظ name-homonym, 11739 ويكيبيديا wrong-entity) — no single query singled out. Also fixed the §Regression bucket tables (84/928/3164 were mis-placed in Type A; 3702 mislabelled Type B). |
| 4.14 | 0.3 threshold rationale | ✅ VERIFIED (no rationale) | The 0.3 "strong BM25" cut has **no stated justification** in the analysis — arbitrary. Supports softening (5.C.18). |
| 4.15 | `zhang_2024_mugi` BibTeX | ⚠️ NEEDS EDIT | **Venue (EMNLP Findings 2024) is correct**, but **title and authors are fabricated.** (Also: `lei_2024_csqe` authors are wrong.) |
| 4.16 | Ch.3/Ch.4 cross-ref labels used | ⚠️ NEEDS EDIT | **48 of 115 defined labels are never referenced** — incl. 3 table labels + 5 figure labels that prose should cite. |
| 4.17 | Spot-check brief numbers | 🔎 PARTIAL | In-repo numbers reconcile, **except** the error-analysis doc reports 0.6936 (looks like Config C) under a "Config A RRF 0.7137" header — the known WS1.3 Config-A-vs-C issue. |

**Bottom line:** 8 fully verified, 1 verified-by-data, 5 need edits, 3 partial (after team review). The highest-impact corrections: **4.15** (fabricated citation fields — and a second one, CSQE) and **4.12** (two thesis showcase examples are factually wrong → replace). *Note: 4.5 was initially marked FAILED here but is in fact VERIFIED — the "30%" is real on TREC DL19 mAP (Llama2-Chat-7B); see corrected entry below.*

---

## Detailed findings

### 4.1 — GPT-OSS "English-dominant" ✅ VERIFIED
- **Source checked:** OpenAI gpt-oss-120b & gpt-oss-20b Model Card (arXiv:2508.10925).
- **Finding:** Model card states the models are "trained on trillions of **mostly English**, text-only data, with a focus on STEM, coding, and general knowledge"; multilingual eval is limited to MMMLU (14 languages). The "English-dominant" descriptor is directly supported.
- **Action:** Keep the claim; cite the official model card. (If GPT-OSS is deleted per 5.A.8, moot.)

### 4.2 — BM25S parameters ✅ VERIFIED
- **Source checked:** `experiments/bm25s_baseline.ipynb` (index build) lines 196–199; `experiments/bm25_baseline_new_index.ipynb` line 627 (Pyserini cross-check).
- **Finding:** `bm25s.BM25(method="lucene", k1=0.9, b=0.4)`; Pyserini `set_bm25(k1=0.9, b=0.4)`. The runtime retriever (`src/retrievers/bm25.py`) loads this prebuilt index, so **k1=0.9, b=0.4** are the operative values. The bm25s library default (k1=1.5, b=0.75) was **not** used.
- **Action:** Feeds 5.A.6 / 2.3 — §2.3.2's "k1=1.5/b=0.75" is wrong; standardise on **k1=0.9, b=0.4**.

### 4.3 — SILMA temperatures ⚠️ NEEDS EDIT
- **Source checked:** `experiments/Query_generator_silma_2B.ipynb` (`TEMPERATURE = 0.1`); saved outputs `results/enhanced_queries/silma_2b_temp01.pkl` **and** `silma_2b_temp07.pkl`.
- **Finding:** SILMA was actually run at **both 0.1 and 0.7** (two result files exist). The notebook's committed config is 0.1. No 0.0 run exists.
- **Action:** Feeds 5.B.5 — fix §3.6.x to "0.7 vs 0.1" (matching the task's own guess), not "0.0 vs 0.1".
- **Team decision (Osman + Elhaj):** Accepted — NEEDS EDIT. Apply the §3.6.x ("section guide") temperature correction.

### 4.4 — Which Arabic benchmark in §4.7 ⚠️ NEEDS EDIT
- **Source checked:** `Chapters/chapter4.tex` lines 370–377; `Chapters/chapter2.tex` model descriptions.
- **Finding:** The §4.7 claim ("Arabic NLP benchmark scores do not directly predict QE quality") **names no specific benchmark**. But Ch.2 reports each model on a *different* benchmark: Falcon-H1 **OALL** ~62%, Gemma 3 **OALL**, Jais-2 **AraGen** 3C3H 58.64%, ALLaM **AMMLU** 67.78, Qwen3-4B **MMMLU** 71.42, SILMA **RAGQA** 0.3575. These are not comparable. README_chapter4 anchors §4.5.3 on **OALL**.
- **Action:** Feeds 5.C.3 — restrict the claim to **OALL** (the only score shared by ≥3 models) instead of the generic "Arabic NLP benchmark" framing.
- **Team decision (Osman + Elhaj):** **Adopt OALL as the base/primary benchmark, and apply it thesis-wide — `[SWEEP]`.** Rephrase **every** generic occurrence of "Arabic NLP benchmark" / "Arabic benchmark(s)" to **OALL** for consistency (not just §4.7). Known generic occurrences to convert: §4.7 / §4.5.3 (`chapter4.tex` ~lines 370–377, the "benchmarks don't predict QE quality" argument), plus the matching sentences in **Ch.5** (e.g. README_chapter5 "Arabic benchmarks ≠ QE quality") and any Ch.4 key-findings recap. The argument stays the same (Falcon-H1 has the top OALL score at its scale yet loses on retrieval to multilingual models with lower OALL).
  - ⚠️ **Do NOT blind-replace these (they are not the generic claim):** (a) the **per-model scores in Ch.2 §2.4** that are genuinely reported on *other* benchmarks — Jais-2 **AraGen** 58.64, ALLaM **AMMLU** 67.78, Qwen3-4B **MMMLU** 71.42, SILMA **RAGQA** 0.3575 — keep these as the real reported numbers (or add the model's OALL score if you want true comparability); (b) every "**MIRACL (Arabic) benchmark**" mention, which refers to the *dataset*, not a capability benchmark. Sweep the generic-claim sentences only.

### 4.5 — CSQE "30% mAP over BM25" ✅ VERIFIED *(corrected)*
- **Source checked:** Lei et al., *Corpus-Steered Query Expansion with LLMs*, **EACL 2024** (aclanthology 2024.eacl-short.34; arXiv:2402.18031). Tables 3 + 7.
- **Finding:** On **TREC DL19, mAP**: BM25 baseline **30.1** → **BM25+CSQE with Llama2-Chat-7B = 39.1** (Table 7) = **+29.9% ≈ 30%**. (Llama2-13B 41.4, 70B 43.6; GPT-3.5-Turbo, the primary model, reaches 47.2 in Table 3.) The thesis "Llama2-7B gave +30% mAP over BM25" is **accurate** for DL19.
- **Correction note:** My initial pass marked this FAILED because I only read the BEIR **nDCG@10** table (Table 4, BM25 43.7→49.7) and the abstract, missing the TREC-DL **mAP** tables where the 30% figure lives. The other report (Mohammed/Osman) located the exact table. The metric is mAP-on-DL19, not nDCG@10-on-BEIR.
- **Action:** Keep the claim; cite Table 7 (DL19, Llama2-Chat-7B). Optionally note GPT-3.5 is even higher (47.2).
- **Team decision (Osman + Elhaj):** **Keep as-is.** The 30% (mAP) figure appears in our **literature review / "modern" QE review** (foundational query-enhancement research section), where it is correctly attributed to the CSQE paper. Reminder for the writers: this number is **mAP** (the paper's metric), *not* nDCG@10 like our own results — make sure the sentence doesn't imply it is on our metric/dataset.

### 4.6 — Retrieval depth in hybrid experiment ✅ VERIFIED
- **Source checked:** `experiments/phase4_quick_wins (1).ipynb` — `retriever.search(queries, k=100)`, `truncate_top_k(run, k=100)` for CC/RRF fusion.
- **Finding:** All retrieval and fusion operate at **top-100**. No top-1000 path exists.
- **Action:** Feeds 5.B.10 — confirm §3.7 says top-100.

### 4.7 — CSQE temperature = 1.0 ✅ VERIFIED
- **Source checked:** `experiments/exp_013_csqe_aya_8b.ipynb` config `'temperature': 1.0`; both corpus- and blind-sample generation pass `temperature=1.0, do_sample=True`. Confirmed again in the saved pkl `config`.
- **Action:** Supports 5.B.8 (show the CSQE prompt + temp in §3.8).

### 4.8 — First-pass "relevant" definition (qrel ≥1 vs ≥2) ✅ VERIFIED (by data constraint)
- **Source checked:** `src/utils/data_loader_hf.py` (`qrels[qid][docid] = int(rel)`); MIRACL qrels are **binary** (relevance ∈ {0,1}); there are no grade-2 judgments.
- **Finding:** "first-pass relevant" can only mean **qrel ≥ 1**. The qrel≥2 alternative is vacuous for MIRACL. **Code located:** the actual function is `first_pass_is_relevant(qid)` in `experiments/phase4_quick_wins (1).ipynb` cell 63 — it returns True iff the **top-1** BM25 first-pass doc has `rel > 0`. *(The error-analysis doc misnames its notebook as `phase4_quick_wins_Ablation_erroranalysis.ipynb`, which is why I first reported the code as not-in-repo; it actually lives in `phase4_quick_wins (1).ipynb`.)*
- **Action:** State precisely: "a query's first pass is counted relevant iff its **top-1** retrieved doc has MIRACL judgment = 1." Fix the notebook name in the error-analysis doc.

### 4.9 — CSQE expansion length ≈1500 chars ✅ VERIFIED
- **Source checked:** computed over all 2,896 rows of `results/enhanced_queries/exp_013_csqe_aya_8b.pkl`.
- **Finding:** enhanced text **mean = 1485.9, median = 1530.0** chars (min 651, max 2128); original query mean 29.5. The "≈1500 chars" statement is accurate.
- **Note:** §4.8's "trained on short queries" speculation was already dropped (5.C.11); this number can now be **restored** with a verified source if desired.

### 4.10 — "mDPR trained on short queries" ✅ VERIFIED (citable)
- **Finding:** The dense encoder is `castorini/mdpr-tied-pft-msmarco` — "pft" = **pre-fine-tuned on MS MARCO** passage ranking. MS MARCO queries are real Bing web-search queries and are short (the literature explicitly notes "NQ has longer queries than MS MARCO").
- **Action:** Citable as: mDPR is MS-MARCO-fine-tuned (MIRACL paper, Zhang et al. 2023) and MS MARCO queries are short web queries (**Bajaj et al., 2016, arXiv:1611.09268**). This supports re-adding the claim in §4.8 if 5.C.11's degradation explanation is restored.

### 4.11 — 258 failures: exhaustive or sampled 🔎 PARTIAL *(team-revised from VERIFIED)*
- **Source checked:** `docs/experiments/exp_error_analysis_csqe.md` §Failure Analysis.
- **Finding:** The **inspection itself was exhaustive** — all 258 were classified: 257 "universally irretrievable" (CSQE, blind, BM25 all = 0.000) + 1 genuine CSQE failure (qid 1060). Not a sample.
- **Caveat:** The "irretrievable" *conclusion* depends on the **Workstream 1.1 dataset-integrity check** (whether the qrel passages actually exist in the indexed corpus).
- **Team decision (Osman + Elhaj):** **Downgrade to PARTIAL.** The team believes the 257 "irretrievable" cases stem from a real **dataset / chunking** problem in the indexed Wikipedia dump, but this must be **confirmed in Workstream 1** before the §4.10 wording is finalised. So: inspection = exhaustive (verified); irretrievability = pending WS1.

### 4.12 — Three big-win examples ✅ RESOLVED *(2026-05-31)*

**Resolution.** The original trio (الرباط المنصوري / John Dewey / Boileau) was reworked. The per-query analysis was **re-run** (`phase4_quick_wins_Ablation_erroranalysis.ipynb`, self-contained miner cell) and sanity-checked against the published aggregates (blind **0.5046** / CSQE **0.6936** / BM25 **0.4621** — all matched). Mohammed selected a **final trio of score-verified examples**, each **blind nDCG@10 = 0.000 → CSQE nDCG@10 = 1.000**:

| # | Query (qid) | blind | CSQE | plain BM25 |
|---|---|---|---|---|
| 1 | ما هو الرباط المنصوري؟ (10061) | **0.000** | **1.000** | 1.000 |
| 2 | ما هي الأسماء الخمسة في اللغة العربية؟ (3034) | **0.000** | **1.000** | 1.000 |
| 3 | ما هو الفن الجزيري؟ (11753) | **0.000** | **1.000** | 1.000 |

> **Framing note for the writers (important).** For all three, **plain BM25 (raw query, no QE) also scores 1.000** — the relevant article was retrievable from the bare query. So these examples show the **blind (hallucinated) pseudo-document *poisoning* a query the retriever had already solved, while CSQE's corpus-grounded pseudo-document stays on target and preserves the hit.** Phrase §4.10 accordingly — they are *not* "BM25 could not find it" cases. (Full write-up + golden-diagram recommendation: `research_decisions/WS4_TASK_4.12_BIGWIN_EXAMPLES.md`.)

**Action for §4.10 (5.C.17): replace the descriptive table with the verbatim text below.** Each expansion is the **exact** string generated by Aya and fed to the retriever; both blind and CSQE generations were **capped at 128 new tokens**, so each ends mid-sentence — reproduce as-is and append an ellipsis (…) or note the cap. (Drop the old "spinal surgery / French businessman / John Dewey" wording entirely.)

#### Example 1 — ما هو الرباط المنصوري؟ (qid 10061)
*English: "What is al-Ribāṭ al-Manṣūrī?" — blind invents a **surgical suture**; corpus grounds to a **Mamluk Sufi lodge endowed by Sultan al-Manṣūr Qalāwūn** (681 AH / 1282–83 CE).*

**BLIND expansion (System B — scored 0.000), verbatim:**
> ما هو الرباط المنصوري؟ الرباط المنصوري هو نوع من الأربطة الجراحية التي تستخدم في العمليات الجراحية لتثبيت العظام أو الأنسجة الرخوة. يتميز هذا النوع من الأربطة بكونه مرناً وقابلاً للامتصاص، مما يجعله مثالياً للاستخدام في المناطق التي تتطلب حركة وتمدداً بعد الجراحة. يُصنع الرباط المنصوري عادةً من مواد متنوعة مثل البولي بروبيلين أو البولي إيثيلين، ويأتي على شكل شريط رفيع ومرن. يتم إ

**CSQE corpus-grounded expansion (scored 1.000), verbatim** *(sample #2 — quotes the doc most cleanly; sample #1 also available):*
> بناءً على الاستعلام "ما هو الرباط المنصوري؟"، قمت بفحص الوثائق المسترجعة وحددت الوثائق ذات الصلة، حتى ولو جزئياً، بالسؤال. إليك الوثائق ذات الصلة والجمل الرئيسية المستخرجة من كل وثيقة: **الوثيقة 1:** * "الرباط المنصوري، وهو رباط (ملجأ الفقراء من الصوفية) وقفه السلطان المملوكي المنصور قلاوون الصالحي على فقراء وزوار القدس في سنة 68

#### Example 2 — ما هي الأسماء الخمسة في اللغة العربية؟ (qid 3034) ⭐ *recommended golden / diagram example*
*English: "What are the Five Nouns in Arabic?" — blind mistakes it for a list of **popular proper names** (Muhammad, Adam, Ibrahim…); corpus grounds to the **grammar category أب أخ حم فو ذو**.*

**BLIND expansion (System B — scored 0.000), verbatim:**
> ما هي الأسماء الخمسة في اللغة العربية؟ في اللغة العربية، الأسماء الخمسة هي فئة خاصة من الأسماء التي تُعرف بأنها أكثر شيوعًا واستخدامًا، ولها قواعد نحوية محددة في الإعراب. هذه الأسماء الخمسة هي: 1. **محمد**: اسم علم مذكر، وهو من أكثر الأسماء انتشارًا في العالم الإسلامي. 2. **آدم**: اسم علم مذكر، وهو أول إنسان حسب المعتقدات الإسلامية. 3. **إبراهيم**: اسم علم مذكر، ويُعتبر أحد الأنبياء الكبار في الإسلام. 4. **إ

**CSQE corpus-grounded expansion (scored 1.000), verbatim:**
> بناءً على استعراض الوثائق المُستخرجة، يمكنني تحديد الوثائق ذات الصلة جزئيًا أو كليًا بالاستعلام "ما هي الأسماء الخمسة في اللغة العربية؟" وهنا الجمل الرئيسية المستخرجة من كل وثيقة: * **الوثيقة 1:** "أسماء خمسة الأسماء الخمسة المعروفة في اللغة العربية هي (أب، أخ، حم، فو، ذو) واختلف بعض علماء النحو في الاسم السادس، وهو (هن) بسبب عدم استخدامه كثيرًا؛ لأن الأشهر في

#### Example 3 — ما هو الفن الجزيري؟ (qid 11753)
*English: "What is Insular art?" — blind reads it as modern **"environmental / land art"**; corpus grounds to **Insular (Hiberno-Saxon) art** of the post-Roman British Isles (Latin* insula *= island).*

**BLIND expansion (System B — scored 0.000), verbatim:**
> ما هو الفن الجزيري؟ الفن الجزيري هو شكل من أشكال الفن المعاصر الذي يدمج بين العناصر الطبيعية والتقنيات الحديثة لإنشاء أعمال فنية فريدة ومبتكرة. يُعرف هذا النوع من الفن أيضًا باسم "الفن البيئي" أو "الفن الأرضي". يستخدم الفنانون الجزيريون البيئة الطبيعية كمصدر إلهام ووسيلة للتعبير الفني، حيث يقومون بخلق أعمال فنية مؤقتة أو دائمة باستخدام مواد طبيعية مثل التراب، والحجر، والنباتات، والماء، وغيرها من العناصر المتوفرة في البيئة

**CSQE corpus-grounded expansion (scored 1.000), verbatim:**
> بناءً على استعراض الوثائق المُستخرجة والمتعلقة بالاستعلام "ما هو الفن الجزيري؟"، يمكن تحديد الوثائق ذات الصلة وهي: - الوثيقة 1: تُعرّف الفن الجزيري (أو الفن الهايبر-ساكسوني) كنمط فني تطوّر في الجزر البريطانية بعد الحقبة الرومانية، وتُشير إلى أصل المصطلح من الكلمة اللاتينية "insula" التي تعني جزيرة. - الوثيقة 5: تتحدث عن جزيرة المتاحف في برلين، التي تضم

**Source/reproduction:** all six strings pulled verbatim from `results/enhanced_queries/enhanced_queries_aya_expanse_8b.pkl` (`enhanced`, blind) and `results/enhanced_queries/exp_013_csqe_aya_8b.pkl` (`full_results[*].corpus_expansions`, CSQE). Scores from the re-run miner cell (§4.12 of the task doc). ⚠️ CSQE score read from the saved **Config C** run (0.6936); the 1.000 holds for **Config A** too since it is carried by the shared BM25+CSQE component — cite the Config-A number once WS1.3 re-runs it.

### 4.13 — Type B "first-pass poisoning" (general failure mode) ✅ RESOLVED *(2026-05-31)*

**Reframed from a single example to the whole category (team request).** Task 4.13 originally asked only whether "ماهو التطرف" retrieves dialect content. Per the team decision, both this verification and the §4.10 wording should describe the **general Type B failure mode** — with "ماهو التطرف" as *one* illustration, not the headline. The corrected `exp_error_analysis_csqe.md` now documents Type B as a category (**131 queries, 36% of regressions, BM25 < 0.1**) with a shared mechanism and three representative examples.

**The general Type B mechanism (verified across examples).** The query is short/ambiguous and its surface form collides with an Arabic **homonym or name**, so BM25's *first pass* retrieves the wrong entity. CSQE then grounds its pseudo-document on those off-topic docs and the final expanded query misses — **even when the LLM's generation is clean**. Blind QE, which ignores the first pass and generates from parametric knowledge, answers correctly. The re-run (`phase4_quick_wins_Ablation_erroranalysis.ipynb`) now exposes the per-qid first-pass docs (`retrieved_doc_texts`), so the poisoning is directly checkable — confirming the mode is real, not anecdotal.

**Three representative Type B cases** (each **BM25 = 0.000 → blind = 1.000 → CSQE low/0.000**):

| qid | query | first-pass "poison" (what BM25 retrieved) | collision type |
|---|---|---|---|
| 928 | «ماهو التطرف ؟» | **4 of 5** docs match the token **ماهو** — a *southern-dialect* article (لهجة جنوبية), a *song* (ماهو انت), a *novel*, an Iranian *village* (ماهوت); only 1/5 is the real extremism doc | tokenisation / dialect homonym |
| 11371 | «متى ولد نجيب محفوظ؟» | **نجيب باشا محفوظ** — a *different* person (a physician), not the novelist | personal-name homonym |
| 11739 | «من هو مصمم موقع ويكيبيديا؟» | "حظر ويكيبيديا في تركيا" (Turkey-ban article) → CSQE then grounds on "Wapedia / Florian Amrhein" | wrong-entity / near-topic collision |

These span the three sub-flavours of the mode (tokenisation homonym, name homonym, near-topic wrong entity), which is why the thesis should present Type B **as a pattern** rather than a one-off. *(The per-qid first-pass docs were spot-checked against `retrieved_doc_texts` to confirm the mechanism is real — e.g. the original "ماهو التطرف → لهجة جنوبية" claim holds — but no single query is singled out for a deep-dive; the examples stay as a representative set.)*

**Mis-bucketing fix (already applied to `exp_error_analysis_csqe.md`, 2026-05-31):** the example tables had been mislabelled — 84/928/3164 (all BM25 = 0.000) were under Type A (which requires BM25 ≥ 0.3) and 928 was double-listed, while 3702 (BM25 = 0.356) sat in Type B. Fixed: **Type A** now holds genuine BM25 ≥ 0.3 cases (5518 Louvre→*Louvre Abu Dhabi*, 5424 الزفير→*PEEP*, 3702 static→ordinary electricity); **Type B** holds 928 / 11371 / 11739; disjoint thresholds (A ≥ 0.3, B < 0.1, C 0.1–0.3) stated so no query sits in two buckets; bucket counts (191/131/45) were already correct.

- **Action for §4.10 (5.C.18 / WS1.3):** narrate **Type B as a general failure mode** with these 2–3 examples and the shared homonym/wrong-entity mechanism; do **not** name the mode after a single query. Pair with the Type-A narration from the corrected tables.
- **Team decision (Osman + Elhaj):** the earlier "replace ماهو التطرف" instruction is **superseded** — keep it, but demote it to one illustration within the general Type B discussion.

### 4.14 — 0.3 threshold rationale ✅ VERIFIED (there is none)
- **Source checked:** `exp_error_analysis_csqe.md` regression breakdown (Type A defined as "BM25 baseline ≥ 0.3").
- **Finding:** The 0.3 cut for "strong/well-handled BM25" is used **without any stated justification** — it is an arbitrary bucket boundary.
- **Action:** Feeds 5.C.18 — soften "dominant predictor" and drop or explicitly flag the 0.3 cut as an arbitrary convenience threshold.

### 4.15 — `zhang_2024_mugi` BibTeX ⚠️ NEEDS EDIT (and a second bad citation found)
- **Source checked:** `References.bib` entry vs aclanthology.org/2024.findings-emnlp.103.
- **Finding (MuGI):** **Venue is CORRECT** (Findings of the ACL: EMNLP 2024). **Title and authors are fabricated:**
  - Bib title: *"MUGI: Multi-Granularity Query Expansion with LLMs…"* → real title: **"Exploring the Best Practices of Query Expansion with Large Language Models"** (MuGI = **Multi-Text Generation Integration**, not "Multi-Granularity").
  - Bib authors: *Zhang, Jianfei; Deng, Minghan; Zhou, Yifan; Wang, Shuangyin; Li, Wentao* → real authors: **Le Zhang, Yihong Wu, Qian Yang, Jian-Yun Nie** (Mila / Univ. de Montréal).
- **Bonus finding:** `lei_2024_csqe` has the **same problem** — bib authors *"Lei, Xiao; Lian, Zhong; Zhang, Xinyu; Lin, Yanzhao"* are wrong; real authors are **Yibin Lei, Yu Cao, Tianyi Zhou, Tao Shen, Andrew Yates** (EACL 2024, short). The arXiv id (2402.18031) is correct.
- **Action:** Fix both entries. This strongly suggests the **full citation audit (WS6 Task 6.4) should be prioritised** — at least two of the AI-generated BibTeX entries have hallucinated author/title fields with correct URLs.
- **Team decision (Osman + Elhaj):** Confirmed NEEDS EDIT. Elhaj independently searched and confirmed the real MuGI title (*"…Enhancing Information Retrieval through Multi-Text Generation Integration…"* on arXiv; published as *"Exploring the Best Practices of Query Expansion with LLMs"*, Findings of EMNLP 2024 — **use the published title to match the cited venue**). **Fix MuGI title + authors**, and **fix the second entry (`lei_2024_csqe`) title + authors** the same way. Important context for the audit: **the papers themselves were genuinely read** (they came up in the methodology/discussion); only the BibTeX *metadata* (author/title) is wrong — content/claims are fine. MuGI is used only for the **fusion / query-repetition (β) parameter**, not as a core method.

### 4.16 — Cross-reference labels actually used ⚠️ NEEDS EDIT
- **Method:** extracted every `\label{}` defined in `chapter3.tex` / `chapter4.tex` and checked for any `\ref/\cref/\autoref/\eqref/...` anywhere in the thesis (`ws4_labels.py`).
- **Finding:** Ch.3 defines 42 labels, **21 unused**; Ch.4 defines 73 labels, **27 unused** → **48 dead labels.** Most are subsection anchors (harmless), but the unused set includes **3 table labels** (`tab:q2d_params`, `tab:coverage`, `tab:qwen_generations`) and **5 figure labels** (`fig:csqe_scatter`, `fig:dense_bar_chart`, `fig:hybrid_comparison`, `fig:regression_pie`, `fig:repetition_heatmap`) — every table/figure should be cited in prose.
- **Action:** The "23 cross-reference labels" framing is inaccurate (far more labels exist, ~42% unused). Add in-text references for the table/figure labels (ties into 5.C.5 table audit and 7.1 figure plan); remove or use the dead section labels. *(Figure labels are currently placeholders, so those are expected until the figure plan lands.)*
- **Team decision (Osman + Elhaj):** **Unused *section* labels are harmless — leave them** (a `\label` with no `\ref` produces no error and breaks nothing). The ones that **must** be fixed are the **table and figure** labels: every table/figure should be referenced in the prose. Do this **after** the text/tables/figures are finalised (so it dovetails with 5.C.5 table audit + 7.1 figure plan). Scope the action to tables + figures only.

### 4.17 — Spot-check brief numbers vs experiment docs 🔎 PARTIAL
- **Correction:** The brief **does** exist in the repo as `thesis_update_brief.md` (my first glob pattern missed it). The other report spot-checked 5 headline numbers against it (BM25 0.4621, mDPR 0.4993, Hybrid RRF 0.6267, Qwen 2.5 3B 0.5435, Aya n=1 BM25 0.5046) — all confirmed correct, which matches the raw metrics. My added check below still stands as a *separate* issue those 5 didn't cover.
  - CSQE config (temp 1.0 / k=5 / 2+2 / α=4 / 128 tok) — matches pkl config ✅
  - CSQE+BM25 0.6157 / R@100 0.9422 / MRR 0.6380 — matches `evaluate_enhanced_queries.ipynb` output ✅
  - Error-analysis headline numbers (56.8% improved, 16.6% regress, +0.1890 mean, 258 failures, 1061 big wins, 0.8877 vs 0.5814) — internally consistent ✅
  - **Discrepancy:** `exp_error_analysis_csqe.md` header says it analyses **"Config A RRF (0.7137)"**, but its per-query "CSQE+Hybrid" column reports **0.6936** for all queries — which matches the **Config C / Both-expanded** value, not Config A. This is precisely the **known WS1 Task 1.3 problem** ("re-run per-query error analysis for Config A, replaces Config C analysis"). Independent spot-check confirms the error analysis is currently on the wrong configuration.
- **Action:** When the brief is available, diff its Quick Reference block. Meanwhile, WS1.3 (Config-A redo) must fix the 0.7137-vs-0.6936 labelling before §4.10 is finalised.
- **Team decision (Osman + Elhaj):** The 5 spot-checked headline numbers are accepted as correct. The Config-A-vs-C discrepancy is treated as a **naming-consistency issue + the per-query error-analysis re-run for Config A** — both **assigned to Workstream 1** (Task 1.3). Considered **resolved here / noted** in this file; the actual fix happens in WS1, not WS4.

---

## Cross-workstream consequences (what these outcomes unblock)

| Verification | Unblocks / changes |
|--------------|--------------------|
| 4.2 (k1=0.9/b=0.4) | 5.A.6 §2.3.2-vs-§3.2.2 fix; 2.3 notation note |
| 4.3 (0.1 & 0.7) | 5.B.5 SILMA temperature wording |
| 4.4 (standardise → OALL) | 5.C.3 + thesis-wide `[SWEEP]`: generic "Arabic NLP benchmark" → OALL (excl. Ch.2 per-model scores & MIRACL-dataset mentions) |
| 4.5 (DL19 mAP, Llama2-7B, +30%) | §2.4 CSQE claim is correct as written — cite Table 7 |
| 4.9 (~1500 chars) + 4.10 (MS MARCO short) | optional restore of §4.8 dense-degradation explanation (5.C.11) |
| 4.12 (✅ final verified trio) | 5.C.17 big-win table: paste verbatim blind+CSQE expansions for 10061 / 3034 / 11753 (in the 4.12 entry); golden diagram = الأسماء الخمسة |
| 4.13 (✅ ماهو التطرف verified; Type-A table mis-bucketed) | 5.C.18 / WS1.3 §4.10 regression rewrite: KEEP ماهو التطرف (Type B); fix 928 double-listing; repopulate Type A with real BM25≥0.3 examples (regression-miner cell) — qid 3702 confirmed Type A |
| 4.15 (bad bib) | escalates WS6 Task 6.4 full citation audit |
| 4.16 (dead labels) | 5.C.5 table audit + 7.1 figure plan |
| 4.17 (Config A vs C) | confirms WS1 Task 1.3 is required before §4.10 final |

## Artifacts produced during verification
- `ws4_labels.py` — label-usage audit script (repo root; scratch — safe to delete).
- Computations on `results/enhanced_queries/exp_013_csqe_aya_8b.pkl` and `enhanced_queries_aya_expanse_8b.pkl` (expansion length; example extraction).

**END.**
