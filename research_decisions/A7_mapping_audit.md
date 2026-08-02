# A7 — Problem ↔ Objectives ↔ Methodology/Results ↔ Conclusions Mapping Audit

**Date:** 2026-07-29
**Scope:** `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter1.tex` … `chapter5.tex`
(+ `5-Abstract.tex`, `7-ListofAbbreviations.tex` where the chain runs through them)
**Status:** Report only — no thesis file was modified.

**Headline: 6 BLOCKER gaps, 14 MINOR gaps, 4 acronym violations.**

Reference for objective numbering: `chapter1.tex:27–45` (nine numbered objectives).
Central RQ: `chapter1.tex:18` — *"To what extent can LLM-based QE---blind and corpus-steered---improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms?"*

---

## (a) Master table — one row per objective

| # | Objective (short) | §1.1 problem element | Ch.3 methodology | Ch.4 results | Ch.5 conclusion para | P→O | O→M | O→R | O→C |
|---|---|---|---|---|---|---|---|---|---|
| **O1** | Establish independent dense + sparse baselines on MIRACL Arabic; quantify each paradigm and their complementarity via NDCG / Recall / MRR | "improves substantially over strong unenhanced baselines" (`ch1:18`) | §3.2 `sec:meth_baseline` (3.2.1 mDPR, 3.2.2 BM25S, 3.2.3 rationale) | §4.1 `sec:res_baseline` + §4.1.1 `sec:res_baseline_comparison` (Table 4.1) | ¶1 "Baseline establishment and error analysis" (`ch5:14`) | PASS | PASS | PASS | **GAP (MINOR M1)** — MRR named in O1 but no MRR value appears anywhere in §5.1; complementarity asserted, not quantified |
| **O2** | Systematic baseline error analysis — failure rate, query-length effect, retrieval coverage — to identify failure patterns and guide technique selection | short-query information poverty **+ Arabic vocabulary mismatch** (`ch1:18`) | §3.3 `sec:meth_error` (3.3.1 quant framework, 3.3.2 length buckets, 3.3.3 failed-query inspection) | §4.2 `sec:res_error` (4.2.1 rate, 4.2.2 length, 4.2.3 coverage, 4.2.4 technique-selection rationale) | ¶1 (`ch5:14`) | **GAP (BLOCKER B1)** — vocabulary mismatch is a named root cause in §1.1 but no objective names it | PASS | PASS | **GAP (MINOR M2)** — coverage sub-item (74.6 % @10 / 90.1 % @100, `ch4:116–132`) absent from §5.1 |
| **O3** | Adapt Query2Doc for Arabic zero-shot with openly available LLMs, incl. engineering optimisations for free cloud GPUs | openly-available-model constraint (`ch1:18`) | §3.4 `sec:meth_query2doc` (3.4.2 modifications, 3.4.3 LLM config, 3.4.4 batching, 3.4.5/3.4.6 dense/BM25 forms); §3.5.5 `sec:meth_quantisation` | §4.3 `sec:res_query2doc` (4.3.1 dense +8.9 %, 4.3.2 BM25, 4.3.3 comparison with original paper); runtime at `ch4:178` | ¶2 "Query2Doc transfers effectively to Arabic" (`ch5:16`) | PASS | PASS | PASS | PASS |
| **O4** | Standardised comparative evaluation of openly available 2–8 B LLMs; identify best model per paradigm; characterise patterns across families | only implicitly (`ch1:18` "relying only on openly available models of practical scale") | §3.5 `sec:meth_model_comparison` (3.5.1–3.5.5) | §4.4 `sec:res_model_comparison` (4.4.1–4.4.3) + §4.5 `sec:res_key_findings` (4.5.1–4.5.5) | ¶3 "Comprehensive model comparison" (`ch5:18`) + ¶4 "Patterns observed across model families" (`ch5:20`) | **GAP (MINOR M4)** — §1.1 motivates *using* open models, not *comparing* them | PASS | PASS | PASS (but see M3 — Arabic-specialised vs multilingual is Ch.2 Q7, not named in O4) |
| **O5** | Analyse sparse-vs-dense interaction with LLM expansions; establish whether QE must be paradigm-adapted | "whether an expansion that benefits dense … also benefits---or instead degrades---sparse" (`ch1:18`) | §3.4.6 `sec:meth_q2d_dense` + §3.4.7 `sec:meth_q2d_bm25`; §3.2.3 `sec:meth_baseline_rationale` | §4.3.1/4.3.2 + §4.3.2.1 `sec:res_term_dilution` + §4.5.4 `sec:res_finding_retriever` (Table 4.10) | ¶5 "Dense and sparse retrieval respond differently to QE" (`ch5:22`) | PASS | PASS | PASS | PASS |
| **O6** | Investigate query repetition as remedy for BM25 term dilution; **determine the optimal repetition factor across the evaluated models** | only implicitly ("or instead degrades", `ch1:18`) | §3.6 `sec:meth_repetition` (fixed *n*, adaptive β, sweep design) | §4.6 `sec:res_repetition` (Tables 4.11, 4.12; observation 2 at `ch4:495`) | ¶6 "Query repetition resolves sparse retrieval degradation" (`ch5:24`) | **GAP (MINOR M5)** | PASS | PASS | **GAP (BLOCKER B6)** — ¶6 says all nine models won "at their optimal β"; Table 4.12 shows 7 of 9 optima are **fixed *n*** (5/7/10). The model-dependence of the optimum — the literal wording of O6 — is not reported |
| **O7** | Establish hybrid sparse–dense fusion baseline without QE; quantify the ceiling any enhanced system must exceed | "hybrid sparse--dense architecture" / "strong unenhanced baselines" (`ch1:18`) | §3.7 `sec:meth_hybrid` (RRF, CC, α-sweep) | §4.7 `sec:res_hybrid` (Table 4.13) | ¶7 "Hybrid retrieval establishes a strong non-QE ceiling" (`ch5:26`) | PASS | PASS | PASS | PASS |
| **O8** | Adapt and evaluate CSQE for Arabic; isolate corpus-grounded vs blind components by controlled ablation | "whether grounding the expansion in evidence retrieved from the target corpus produces more reliable enhancement" (`ch1:18`) | §3.8 `sec:meth_csqe` (3.8.1 pipeline, 3.8.2 ablation design) | §4.8 `sec:res_csqe` (4.8.1 main, 4.8.2 ablation + α-sweep) | ¶8 "Corpus-steered expansion validates the corpus grounding hypothesis" (`ch5:28`) + ¶9 "Corpus-grounded and blind expansion are complementary" (`ch5:30`) | PASS | PASS | PASS | **GAP (BLOCKER B3)** — Dense+CSQE (0.5915, +18.5 % over mDPR; `ch4:597,604`) is reported in Ch.4 but never in Ch.5, leaving the *corpus-steered × dense* cell of the RQ unanswered |
| **O9** | Determine optimal placement of QE in the hybrid by evaluating **sparse / dense / both** expansion strategies; explain via per-query error analysis of the final system | "to which retriever within a hybrid … they are applied" (`ch1:18`) | §3.8.3 `sec:meth_csqe_config` (three configurations) + §3.9 `sec:meth_error_csqe` | §4.9 `sec:res_csqe_hybrid` (4.9.1 configs Table 4.16, 4.9.2 progression) + §4.10 `sec:res_error_csqe` (4.10.1–4.10.4) | ¶10 "Retriever-specific query representation is critical" (`ch5:32`) + ¶11 "Per-query analysis localises where the gains arise" (`ch5:34`) | PASS | PASS | PASS | **GAP (BLOCKER B4)** — O9 names three strategies; ¶10 reports only two (BM25-expanded 0.7137 vs Both-expanded 0.6959). Dense-expanded (0.6588 CC / 0.6474 RRF, `ch4:671–672`) is omitted |

**Conclusion-paragraph inventory (12 bold-led paragraphs, all anchored):** ¶1→O1+O2 · ¶2→O3 · ¶3→O4 · ¶4→O4 · ¶5→O5 · ¶6→O6 · ¶7→O7 · ¶8→O8 · ¶9→O8 · ¶10→O9 · ¶11→O9 · ¶12 "Overall" (`ch5:36`)→central RQ. **No orphan conclusion paragraph.**

---

## (b) Reverse-direction orphans (content serving no objective)

| Location | Content | Severity | Note |
|---|---|---|---|
| `chapter3.tex:152` §3.3.3 *Failed Query Inspection* + `chapter4.tex:141` §4.2.4 *Technique Selection Rationale* | Manual inspection of 20 worst queries → vocabulary mismatch (آزوت / نيتروجين), entity variation, diacritics | **BLOCKER (B1, reverse side)** | This is precisely the vocabulary-mismatch evidence §1.1 demands, yet O2's enumerated sub-items are only failure rate, length, coverage. Two-sided gap |
| `chapter2.tex:239` §2.3 *Evaluation Dataset Selection* (dataset survey + Table 2.2) | Selection of MIRACL over ARCD/TyDi QA etc. | MINOR (M11a) | O1 presupposes MIRACL; no objective covers choosing it. Acceptable as background, but unmentioned in §1.3 too (see M8) |
| `chapter4.tex:324` §4.4.3 *Dropped Models Analysis* (ALLaM-7B) | Tokeniser artefact, −48.9 % NDCG@10 | MINOR (M11b) | Surfaces in Ch.5 only under *Challenges* (`ch5:50`), never under *Conclusions*. O4's "characterising the performance patterns" covers it only loosely |
| `chapter3.tex:317` §3.5.3 *Temperature Selection* → `chapter4.tex:433` finding 4 | Temp 0.1 optimal, +2.5 % over 0.7 | MINOR | Folds under O3's "engineering optimisations"; acceptable |
| `chapter4.tex:945` §4.11 *Summary of All Experiments* | Consolidated table | Not an orphan (synthesis), but unmentioned in §1.3 — see M9 |
| `chapter3.tex:8` §3.1 *Dataset and Experimental Setup* | Infrastructure | Not an orphan — serves all objectives |

Every other major Ch.3 and Ch.4 section maps to at least one objective.

---

## (c) RQ-answer assessment

RQ: *"To what extent can LLM-based QE---**blind and corpus-steered**---improve Arabic information retrieval across **sparse, dense, and hybrid** retrieval paradigms?"* — a 2 × 3 matrix. Coverage in §5.1:

| | **Sparse (BM25)** | **Dense (mDPR)** | **Hybrid** |
|---|---|---|---|
| **Blind QE** | ANSWERED — Aya β=2, 0.5855, +26.7 % over BM25 (¶6, `ch5:24`) | PARTIAL — "+23.5 % (Aya Expanse 8B)" relative only; absolute 0.6164 not stated (¶3, `ch5:18`) | NOT ANSWERED — no blind-QE-only hybrid figure in §5.1 (nor in Ch.4 as a standalone row) |
| **Corpus-steered (CSQE)** | ANSWERED — 0.6157 (¶8, `ch5:28`); % improvement over BM25 (+33.2 %, `ch4:604`) not carried into Ch.5 | **NOT ANSWERED (B3)** — 0.5915 / +18.5 % exists at `ch4:597,604`, absent from Ch.5 | ANSWERED — 0.7137, +54.5 % over BM25, +13.9 % over no-QE hybrid (¶8, ¶12) |

**Verdict:** the RQ is answered with quantified outcomes for 3 of 6 cells, partially for 1, and not at all for 2. The "Overall" paragraph (`ch5:36`) asserts improvement "under all three retrieval paradigms examined" but quantifies only the hybrid figure in-paragraph; the per-paradigm numbers are scattered across ¶3, ¶6 and ¶8 and the reader must assemble them. The corpus-steered × dense cell is the material omission, because it is the one cell whose *negative* direction (expansion hurts a short-query-trained dense encoder) is the causal premise of the thesis's headline asymmetric-fusion finding (¶10). Recommend a single explicit three-paradigm summary sentence in ¶12.

---

## (d) Ch.2 open questions ↔ Ch.1 objectives

Source: `chapter2.tex:478–486` (7 itemised questions), following the 4 gaps at `chapter2.tex:466–474`.

| Ch.2 Q | Question (short) | Ch.1 objective(s) | Verdict |
|---|---|---|---|
| Q1 (`ch2:479`) | Extent LLM-based QE improves Arabic IR under sparse/dense/hybrid, zero-shot, openly available 2–8 B LLMs | The RQ itself; O1, O3, O7, O8, O9 collectively | **Scope mismatch (M7)** — Q1 adds "zero-shot" and "2–8 billion" but omits "blind and corpus-steered"; the §1.1 RQ does the reverse. Two different sentences for the same question |
| Q2 (`ch2:480`) | Does Query2Doc transfer to Arabic zero-shot? | O3 | PASS |
| Q3 (`ch2:481`) | Sparse-vs-dense interaction; must strategy be paradigm-adapted? | O5 | PASS |
| Q4 (`ch2:482`) | Does query repetition transfer; at what factor; does the optimum hold across models? | O6 | PASS (but the Ch.5 answer is incomplete — B6) |
| Q5 (`ch2:483`) | Does corpus grounding beat blind; individual component contributions? | O8 | PASS |
| Q6 (`ch2:484`) | Within a hybrid, to which retriever should the expansion be applied? | O9 | PASS |
| Q7 (`ch2:485`) | Which 2–8 B LLMs are best per paradigm; **do Arabic-specialised models outperform multilingual models of comparable scale?** | O4 | **Partial (M3)** — O4 says only "characterising the performance patterns observed across model families"; the Arabic-vs-multilingual contrast is answered at `ch4:386–393` and `ch5:20` but is not promised by any objective |
| — | *(no Ch.2 question)* | O1 (baselines), O2 (error analysis), O7 (no-QE hybrid ceiling) | **Note (M6)** — three instrumental objectives have no matching Ch.2 question. Defensible (they are internal prerequisites, not literature gaps), but should be acknowledged |

**Ordering mismatch (M6):** Ch.2 orders the questions *extent → Query2Doc → sparse/dense → repetition → grounding → placement → model comparison* (Q7 last); Ch.1 orders the objectives with model comparison at **O4**, i.e. fourth of nine. A committee reading the two lists side by side will see the model-comparison item jump from last to fourth. Either reorder Ch.2's list so model comparison sits after Q2, or reorder the objectives so O4 follows O5–O6.

---

## (e) §1.3 Thesis Layout discrepancies

| Layout paragraph | Claim | Actual chapter content | Verdict |
|---|---|---|---|
| Ch.2 (`ch1:54`) | "introduces LLMs, RAG, IR methods, QE techniques … mathematical formulations … descriptions of all models … concludes with a review of related literature and the identification of the research gap" | §2.1 Theoretical Background, §2.2 Mathematical Models, **§2.3 Evaluation Dataset Selection**, §2.4 Models Used, §2.5 Related Work (incl. §2.5.4 Research Gap), **§2.6 Chapter Summary** | **GAP (M8)** — §2.3 (dataset survey, Table 2.2) is unmentioned; the chapter does not in fact *conclude* with the research gap but with §2.6 |
| Ch.3 (`ch1:56`) | dataset → hardware/software → metrics → baselines → error analysis → Query2Doc adaptation → query repetition → hybrid fusion → CSQE (+ablation +retriever-specific) → per-query error analysis | §3.1 … §3.4 Query2Doc, **§3.5 Model Comparison Methodology (3.5.1–3.5.5)**, §3.6 Repetition, §3.7 Hybrid, §3.8 CSQE, §3.9 Per-Query Error Analysis | **GAP (BLOCKER B2)** — an entire numbered section (§3.5, five subsections: selection criteria, standardised protocol, temperature, model-specific issues, quantisation) is skipped. Ch.3's own roadmap (`ch3:5`) *does* list it, so §1.3 contradicts §3.0 |
| Ch.4 (`ch1:58`) | baselines → error analysis → Query2Doc (dense + sparse) → model-comparison leaderboards incl. dropped models → repetition sweep → hybrid fusion → CSQE ablation + α-sweep → CSQE+hybrid three configs → overall system progression table → per-query error analysis | §4.1 … §4.4 leaderboards, **§4.5 Cross-Cutting Findings (4.5.1–4.5.5)**, §4.6 … §4.8 CSQE (**4.8.1 Main CSQE Results** then 4.8.2 ablation), §4.9 CSQE+hybrid (4.9.2 = progression), §4.10 per-query, **§4.11 Summary of All Experiments** | **GAP (M9)** — three omissions: §4.5 (five subsections of cross-cutting findings, incl. the O5 anchor §4.5.4), §4.8.1 (main CSQE BM25/Dense results — the layout jumps straight to the ablation), and §4.11 (the final consolidated table; "overall system progression table" refers to §4.9.2, a different table) |
| Ch.5 (`ch1:60`) | "overall conclusions, challenges encountered, recommendations for future work" | §5.1 Conclusions, §5.2 Challenges, §5.3 Recommendations | PASS |

---

## (f) Acronym first-mention violations

Checked: QE, HyDE, GRF, GPT-3, APIs, MIRACL, NDCG, MRR, GPUs, BM25, CSQE, LLM, RAG, mDPR (+ MSA).

**Clean (defined once, in Ch.1, never re-expanded later):** RAG (`ch1:5`), LLM (`ch1:5`), MSA (`ch1:7`), QE (`ch1:9`), GPT-3 (`ch1:11`), APIs (`ch1:11`), MIRACL (`ch1:28`), GPUs (`ch1:32`), BM25 (`ch1:38`), CSQE (`ch1:42`), mDPR (`ch1:56`).
*(Benign non-violation: `chapter3.tex:49` "In the first phase (QE)" is a phase label, not a re-definition.)*

**Violations:**

| # | Acronym | First definition | Later re-definition | Problem |
|---|---|---|---|---|
| **A1** | **NDCG** | `Chapters/chapter1.tex:28` — "Normalis**ed** Discounted Cumulative Gain (NDCG)" | `Chapters/chapter2.tex:208` — "Normali**z**ed Discounted Cumulative Gain (NDCG)" | Duplicate full-form definition **and** British/American spelling divergence. Compounded by `7-ListofAbbreviations.tex:45` ("Normalized") and `5-Abstract.tex:7` ("Normalized"). Thesis style is British (`ch1:28` "Normalised", and "optimisation/quantisation/tokenisation" throughout) |
| **A2** | **MRR** | `Chapters/chapter1.tex:28` — "Mean Reciprocal Rank (MRR)" | `Chapters/chapter2.tex:229` — "Mean Reciprocal Rank (MRR)" | Duplicate full-form definition |
| **A3** | **HyDE** | `Chapters/chapter1.tex:11` — "Hypothetical Document Embedding**s** (HyDE)" | `Chapters/chapter5.tex:54` — "HyDE (hypothetical document embedding)" | Reverse-order re-gloss in the Conclusion; also singular vs. plural and lower- vs. upper-case |
| **A4** | **GRF** | `Chapters/chapter1.tex:11` — "Generative Relevance Feedback (GRF)" | `Chapters/chapter5.tex:54` — "GRF (generative relevance feedback)" | Reverse-order re-gloss in the Conclusion |

*Note:* `5-Abstract.tex` defines RAG, LLM, QE, MIRACL, mDPR, BM25, GPUs and NDCG in full before Ch.1 does. This is normal practice (abstracts must be self-contained) and is **not** counted as a violation, but it does mean the abstract's "Normalized" (A1) is a third instance of the same spelling inconsistency.

---

## (g) Prioritised fix list

### BLOCKERS

**B1 — Vocabulary mismatch has no objective.** `chapter1.tex:30` (Objective 2).
§1.1 names two root causes — short-query information poverty *and* Arabic vocabulary mismatch — but O2 enumerates only failure rate, query length and coverage. §3.3.3 and §4.2.4 produce the vocabulary-mismatch evidence, so the content exists with nothing claiming it.
*Proposed fix — replace O2 with:*
> To conduct a systematic error analysis of the baseline results---quantifying the overall failure rate, the effect of query length, and retrieval coverage, and characterising the linguistic failure patterns arising from Arabic morphological, orthographic and lexical variation---in order to identify the failure modes that QE must address and to guide the selection of the enhancement technique.

**B2 — §1.3 omits the whole of §3.5 (Model Comparison Methodology).** `chapter1.tex:56`.
Contradicts Ch.3's own roadmap at `chapter3.tex:5`. A committee cross-reading the layout against the table of contents will find a five-subsection section unaccounted for.
*Proposed fix — insert after "…including modifications from the original paper and engineering optimisations.":*
> The methodology of the comparative model evaluation is then described, covering the model selection criteria, the standardised generation protocol, the temperature setting, the model-specific technical issues encountered, and the quantisation strategy adopted for models exceeding the available memory.

**B3 — Corpus-steered dense retrieval is never reported in the Conclusions.** `chapter5.tex:28` (¶8).
The RQ promises coverage of corpus-steered expansion across all three paradigms; Ch.4 has the number (0.5915, +18.5 % over mDPR, `chapter4.tex:597,604`) but Ch.5 does not.
*Proposed fix — insert after "…substantially outperforming blind Query2Doc.":*
> Applied to the dense retriever instead, the same expansion raised mDPR from 0.4993 to 0.5915 NDCG@10 (+18.5 per cent), an improvement smaller than that obtained on BM25; the expanded query was therefore found to be better matched to lexical than to semantic retrieval, an asymmetry that was exploited in the fusion experiments (Section~\ref{sec:res_csqe_main}).

**B4 — Objective 9 promises three placement strategies; only two are reported.** `chapter5.tex:32` (¶10).
*Proposed fix — replace the parenthetical "(BM25-expanded: 0.7137 > Both-expanded: 0.6959)" and extend the sentence:*
> A key finding is that applying CSQE asymmetrically---only to the BM25 retriever---outperformed both alternative placements: expanding both retrievers yielded 0.6936 NDCG@10 under the same RRF fusion, and expanding only the dense retriever yielded 0.6474, against 0.7137 for the sparse-only assignment (Table~\ref{tab:csqe_hybrid_configs}).

*(Using the like-for-like RRF column also resolves M10 — the current text compares an RRF result with a CC result.)*

**B5 — The Abstract still carries the pre-rewrite framing.** `5-Abstract.tex:5` and `:9`.
`5-Abstract.tex:5` states the thesis "investigates the extent to which small open-source LLMs can improve Arabic information retrieval through QE, and identifies the model characteristics that determine effectiveness" — a model-comparison framing that predates the A1–A6 rewrite. The abstract never states the central RQ, never names CSQE, and never states the asymmetric-placement finding, which §5.1 ¶10 and ¶12 present as the thesis's principal contribution.
*Proposed fix — replace the opening sentence of `5-Abstract.tex:5` with:*
> This thesis investigates the extent to which LLM-based QE---generated blindly or steered by the target corpus---can improve Arabic information retrieval across sparse, dense and hybrid retrieval paradigms, using only openly available models of 2--8 billion parameters.

*and extend `5-Abstract.tex:9`:*
> Corpus-Steered Query Expansion (CSQE) was subsequently adapted for Arabic and applied asymmetrically---to the sparse retriever alone---within a hybrid BM25--dense pipeline. This configuration achieved 0.7137 NDCG@10 on the MIRACL Arabic benchmark---a 54.5 per cent improvement over the BM25 baseline and a 13.9 per cent improvement over the strongest hybrid system without QE---and outperformed the symmetric alternative in which both retrievers receive the expanded query.

**B6 — "at their optimal β" misstates Table 4.12.** `chapter5.tex:24` (¶6).
Table 4.12 (`chapter4.tex:469–488`) shows that only Aya Expanse 8B and Jais-2 8B peak at adaptive β=2; the other seven models peak at fixed *n* = 5, 7 or 10. Ch.4 observation 2 (`chapter4.tex:495`) states this explicitly. The Conclusion also fails to deliver O6's "determining the optimal repetition factor across the evaluated models".
*Proposed fix — replace the second sentence of ¶6 with:*
> By prepending the original query before the pseudo-document, all nine models were brought above the BM25 baseline at their optimal repetition setting. The optimum was found to be model-dependent: the 8-billion-parameter models peaked under adaptive repetition ($\beta=2$), whereas the 3--4-billion-parameter models peaked at a fixed count of five to seven repetitions, a difference attributable to pseudo-document length rather than to model size.

### MINOR

| # | Location | Gap | Proposed fix (thesis style) |
|---|---|---|---|
| **M1** | `chapter5.tex:14` | O1 names MRR; no MRR figure appears in §5.1 | Extend ¶1's first sentence: "…mDPR achieved superior ranking quality (NDCG@10 = 0.4993, MRR = 0.5328), while BM25S achieved broader retrieval coverage (Recall@100 = 0.8577)." |
| **M2** | `chapter5.tex:14` | O2 names retrieval coverage; §5.1 omits it | Add after the failure-rate sentence: "Coverage analysis further showed that no relevant passage was surfaced within the top 100 for approximately one query in ten (Recall@100 coverage = 90.1 per cent), establishing a recall ceiling that query-side intervention alone could not lift." |
| **M3** | `chapter1.tex:34` (O4) | Arabic-specialised vs multilingual contrast (Ch.2 Q7, §4.5.3, ¶4) is promised by no objective | Extend O4: "…identifying the most effective model under each retrieval paradigm and establishing whether Arabic-specialised models outperform multilingual models of comparable scale." |
| **M4** | `chapter1.tex:18` | §1.1 motivates *using* open models but not *comparing* them (O4) | Extend the constraint clause: "…while relying only on openly available models of practical scale, among which the choice of generator is itself an open question." |
| **M5** | `chapter1.tex:18` | Term dilution / repetition (O6) is raised in §1.1 only as "or instead degrades" | Extend the same clause: "…also benefits---or instead degrades, through dilution of the original query terms---sparse lexical retrieval, and whether that degradation can be remedied." |
| **M6** | `chapter2.tex:478–486` | Ch.2 question order places model comparison last (Q7); Ch.1 places it fourth (O4). Ch.2 has no question for O1, O2, O7 | Move Q7 to third position (after the Query2Doc-transfer question), and add a closing sentence to `chapter2.tex:488`: "Answering these questions additionally requires independent sparse and dense baselines, a diagnostic error analysis of their failures, and a hybrid fusion reference established without enhancement; these are treated as prerequisite objectives rather than as gaps in the literature." |
| **M7** | `chapter2.tex:479` vs `chapter1.tex:18` | Ch.2 Q1 and the §1.1 RQ are two different sentences for the same question | Align Q1 verbatim with the RQ, adding the constraint as a trailing clause: "To what extent can LLM-based QE---blind and corpus-steered---improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms, when the expansion is generated zero-shot by openly available LLMs of 2--8 billion parameters?" |
| **M8** | `chapter1.tex:54` | §1.3 omits §2.3 and misstates the chapter ending | Insert "The selection of the evaluation dataset from among the candidate Arabic retrieval and question-answering benchmarks is then justified," before "followed by detailed descriptions…", and change the final clause to "…and closes with a review of related literature, the identification of the research gap addressed by this thesis, and a summary of the chapter." |
| **M9** | `chapter1.tex:58` | §1.3 omits §4.5, §4.8.1 and §4.11 | Insert "followed by the cross-cutting findings drawn from that comparison," after "including the examination of dropped models,"; change "CSQE component ablation and alpha sweep" to "the main CSQE results for both retrievers together with the component ablation and alpha sweep"; and append "The chapter closes with a consolidated summary of all experiments." |
| **M10** | `chapter5.tex:32` | 0.7137 (RRF) is compared with 0.6959 (CC α=0.5) — mixed fusion methods | Resolved by the B4 fix (use the RRF column throughout: 0.7137 / 0.6936 / 0.6474) |
| **M11** | `chapter4.tex:324`; `chapter2.tex:239` | §4.4.3 (dropped models) and §2.3 (dataset selection) anchor to no objective | Covered by the M3 extension to O4 for §4.4.3 (add "…and characterising the failure modes that render a model unusable for the task"); §2.3 needs no objective but should be named in §1.3 (M8) |
| **M12** | Throughout | "openly available" (Ch.1 ×4, Ch.2 ×5, Ch.5 ×2) vs "open-source" (Ch.2 ×3, Ch.3 ×6, Ch.4 ×1, Ch.5 ×1) | Standardise on "openly available", which the rewritten Ch.1 uses; replace `chapter3.tex:265`, `chapter4.tex` and `chapter5.tex:18` ("Ten open-source LLMs" → "Ten openly available LLMs") |
| **M13** | `chapter5.tex:36`; `chapter3.tex:270` | ¶12's licence claim has no cross-reference; §3.5.1 says "permissive licences for research use" while Aya Expanse is CC-BY-NC | Add "(Table~\ref{tab:model_comparison})" after the licence clause in ¶12, and amend §3.5.1 criterion 3 to "open weights under a licence permitting research use, whether permissive or non-commercial" |
| **M14** | `chapter5.tex:18`; `chapter2.tex:315` vs `chapter3.tex:288`, `chapter4.tex:275` | "SILMA Kashif-2B" vs "SILMA 2B" | Use "SILMA Kashif-2B" at first mention per chapter, "SILMA 2B" thereafter (or standardise on the full name in all tables) |
| **A1** | `chapter2.tex:208`; `7-ListofAbbreviations.tex:45`; `5-Abstract.tex:7` | NDCG re-defined, with American spelling, after `chapter1.tex:28` | In `chapter2.tex:208` delete the full form: "NDCG measures ranking quality by considering both the relevance of retrieved documents and their positions." Change "Normalized" → "Normalised" in `7-ListofAbbreviations.tex:45` and `5-Abstract.tex:7` |
| **A2** | `chapter2.tex:229` | MRR re-defined after `chapter1.tex:28` | Replace with "MRR measures the average of the reciprocal ranks of the first relevant document across a set of queries $Q$:" |
| **A3/A4** | `chapter5.tex:54` | HyDE and GRF re-glossed in the Conclusion | Replace "Other approaches---HyDE (hypothetical document embedding), GRF (generative relevance feedback), query rewriting, and iterative refinement---were not compared." with "Other approaches---HyDE, GRF, query rewriting, and iterative refinement---were not compared." |

---

## Summary of counts

- **BLOCKER: 6** (B1 vocabulary-mismatch objective, B2 §1.3 omits §3.5, B3 corpus-steered dense unreported, B4 third placement strategy unreported, B5 stale Abstract framing, B6 "optimal β" misstatement)
- **MINOR: 14** (M1–M14)
- **Acronym violations: 4** (NDCG, MRR, HyDE, GRF)
- **Orphan conclusion paragraphs: 0** — all 12 bold-led paragraphs anchor to an objective or to the RQ
- **Objectives with no methodology: 0** — all 9 map to at least one Ch.3 section
- **Objectives with no results: 0** — all 9 map to at least one Ch.4 section
- **Ch.3 major sections serving no objective: 0**; **Ch.4: 1 partial** (§4.4.3, resolvable via M3/M11)
