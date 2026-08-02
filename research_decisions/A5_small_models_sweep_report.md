# Task A5 — Old-Framing Sweep of Chapters 2–5

**Date:** 2026-07-29
**Scope:** `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter2.tex`, `chapter3.tex`, `chapter4.tex`, `chapter5.tex` (+ verification pass on `chapter1.tex`)
**Purpose:** Locate every surviving instance of the OLD framing ("can small open-source LLMs do Arabic QE?") and classify it against the NEW framing (CSQE + asymmetric hybrid BM25–dense fusion; central RQ = *"To what extent can LLM-based QE---blind and corpus-steered---improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms?"*).
**No `.tex` file was modified.** All proposed text below is a suggestion for the A6 editing pass.

---

## (a) Summary Counts

| Chapter | In-scope occurrences | KEEP | FIX | Severity of worst FIX |
|---|---|---|---|---|
| chapter2.tex | 25 | 16 | **9** | HIGH (research-gap section is wholly old-framed) |
| chapter3.tex | 6 | 6 | **0** | — (terminology-only nits) |
| chapter4.tex | 13 | 11 | **2** | MED (§4.5 titled "Key Findings" over model-comparison only) |
| chapter5.tex | 11 | 8 | **3** | HIGH (opening sentence states the old thesis scope) |
| **Total** | **55** | **41** | **14** | |

LaTeX `\small` font commands (chapter2 L249, L389; chapter3 L300; chapter4 L232, L928) were matched by the regex and excluded as non-prose.

**Headline:** the old framing is concentrated in exactly two places — **chapter2 §2.5.4 Research Gap + chapter 2 summary bullets**, and **chapter5 §5.1 opening / "Overall" paragraph**. Chapters 3 and 4 are substantively clean: their small-model language is methodological or literature fact and should be kept.

---

## (b) Findings Table

### chapter2.tex

| Line | Current text (trimmed) | Verdict | Rationale | Proposed replacement (FIX only) | Conf. |
|---|---|---|---|---|---|
| 259 | "ARCD … Small scale & Low" | KEEP | Table cell describing dataset size, not model framing. | — | — |
| 275 | "(2) compatibility with consumer-grade GPU hardware, specifically the NVIDIA T4 … and (3) open-source availability with permissive licensing" | KEEP | Factual selection criteria; hardware and licensing constraints are methodology, not contribution framing. | — | — |
| 279 | Caption: "Open-source LLMs evaluated for Arabic QE in this thesis" | KEEP | Factual caption. Optional terminology sweep to "Openly available LLMs (2--8 billion parameters) evaluated for Arabic QE in this thesis" for consistency with Ch.1. | *(optional)* `\caption{Openly available LLMs evaluated for Arabic QE in this thesis, ordered by parameter count.}` | LOW |
| 320 | "Its small size makes it the most computationally efficient model in the comparison, suitable for deployment on consumer-grade hardware without quantization." | KEEP | Factual per-model description of SILMA Kashif-2B. | — | — |
| 416 | "The review progresses from foundational work on generative query expansion to modern approaches using **smaller LLMs**, and concludes with Arabic-specific information retrieval research." | **FIX** | Sets model size as the sole organising axis of the review; the review now also covers corpus grounding (CSQE, L436) and fusion (Exp4Fuse, L480), which the roadmap sentence hides. | "This section reviews the published literature on QE for information retrieval and RAG systems, organised chronologically and thematically. The review progresses from foundational work on generative query expansion with proprietary large-scale models, through modern approaches in which openly available LLMs are employed and the expansion is grounded in the target corpus, and concludes with Arabic-specific information retrieval research." | **MED** |
| 421 | "an instruction-following LLM (InstructGPT, 175B parameters)" | KEEP | Literature fact about HyDE. | — | — |
| 423 | "Using `text-davinci-003` (175B parameters) … the authors found smaller models insufficient … a finding that has since been challenged by newer, more capable small models." | KEEP | Literature fact plus a defensible literature-level correction. The trailing clause is borderline (see §e). | — | — |
| 427 | "This work demonstrated that small, trainable models can effectively improve the performance of large, frozen LLMs…" | KEEP | Literature fact about Rewrite-Retrieve-Read. | — | — |
| 429 | "A common characteristic of all foundational work is the reliance on 175B-parameter models … with smaller models either untested or found inadequate." | KEEP | Literature fact. Optionally extend with the retriever-agnosticism observation (see §e). | — | — |
| 434 | "The period from 2024 to 2025 saw significant progress in demonstrating that moderately-sized open-source LLMs (7--8B parameters) can perform effective query expansion, overturning the assumption that 175B-scale models are necessary." | KEEP | Literature fact and accurate topic sentence for the subsection. | — | — |
| 442 | "Research on knowledge distillation further reduced the model size requirements…" | KEEP | Literature fact. | — | — |
| 446 | "Collectively, this body of work demonstrates that the model size requirement … has decreased dramatically … However, **a critical gap remains: *no prior study has evaluated sub-7B models for zero-shot query expansion in monolingual Arabic retrieval*.**" | **FIX** | This is the italicised, load-bearing gap statement of the whole review, and it is defined *entirely by model size*. Under the new framing the gap is the language and the retriever interaction; scale is a constraint, not the gap. | "Collectively, this body of work demonstrates that the parameter requirement for effective query expansion has fallen sharply, from 175 billion in 2022--2023 to 7--8 billion in 2024--2025, with further compression possible via knowledge distillation. However, a critical gap remains: *LLM-based QE has not been evaluated for monolingual Arabic retrieval, and the interaction between the generated expansion and the retrieval paradigm to which it is submitted has been left largely unexamined in any language*." | **HIGH** |
| 457 | "open-source models (Llama 3, Mistral 7B) performed comparably to GPT-3.5 Turbo…" | KEEP | Literature fact about El-Beltagy and Abdallah. | — | — |
| 459 | "The query formulation stage---specifically, whether LLM-based QE techniques developed for English transfer effectively to Arabic---remains uninvestigated." | KEEP | Already aligned with the new RQ. | — | — |
| 464–469 | "The literature review reveals a clear gap at the intersection of **two** well-studied areas: 1. LLM-based QE … 2. Arabic RAG systems …" | **FIX** (structural) | The gap is presented as a two-way intersection (English QE × Arabic RAG). The corpus-grounding gap and the retriever-interaction / asymmetric-fusion gap are relegated to an unnumbered trailing paragraph (L480) and thereby read as afterthoughts, although Objectives 5, 8 and 9 rest on them. | See full rewrite in §(c). | **HIGH** |
| 467 | "…recent work demonstrating that 7--8B parameter models are sufficient for effective query expansion. However, none of these studies evaluate query expansion for *monolingual* Arabic retrieval…" | KEEP | Content is correct; only its emphasis is reweighted in the §(c) rewrite. | — | — |
| 474 | "Can modern open-source LLMs (2--8B parameters) perform effective zero-shot query expansion for Arabic information retrieval?" | **FIX** | Direct restatement of the OLD research question as the first and therefore primary open question. | "To what extent can LLM-based QE improve Arabic information retrieval under sparse, dense, and hybrid retrieval, when the expansion is generated zero-shot by openly available LLMs (2--8 billion parameters)?" | **HIGH** |
| 475 | "How do Arabic-specialized models compare against multilingual models for this task?" | KEEP | Legitimately supported by Objective 4 ("patterns observed across model families"), provided it is subordinated rather than listed among the primary questions. Repositioned in §(c). | — | — |
| 476 | "Does the Query2Doc technique, originally validated with 175B-parameter models on English text, transfer to Arabic with smaller models?" | KEEP | Maps to Objective 3. "with smaller models" is a scope condition, not a contribution claim; reworded for terminology in §(c). | — | — |
| 477 | "What model characteristics (parameter count, architecture, Arabic training data volume, vocabulary design) most influence query expansion quality for Arabic?" | **FIX** | Direct echo of the clause explicitly DE-SCOPED from the research question. Promises a predictive characterisation the thesis does not deliver (Ch.4 reports only hedged, confounded observations). | Delete. If a model-selection question is still wanted, replace with the subordinated form: "Which openly available LLMs (2--8 billion parameters) are the most effective Arabic expansion generators under each retrieval paradigm, and what patterns are observed across model families?" | **HIGH** |
| 480 | "A further gap exists in the application of corpus-steered expansion to non-English retrieval… the asymmetric assignment of expansion across retriever *types* … has not been studied." | KEEP (promote) | Content is exactly right for the new framing and is well written; it is only mis-placed. Promoted to a numbered gap in §(c). | — | — |
| 482 | "This thesis addresses these questions through **a systematic evaluation of ten open-source language models for Query2Doc-based query expansion** on the MIRACL Arabic benchmark…" | **FIX** | Presents the model comparison as the entire contribution. Omits query repetition, hybrid fusion, CSQE and the asymmetric-placement result — i.e. Objectives 6–9. | "These questions are addressed in this thesis through a staged experimental programme on the MIRACL Arabic benchmark, progressing from independent sparse and dense baselines, through a standardised comparison of openly available LLMs (2--8 billion parameters) as expansion generators, to corpus-steered expansion and its placement within a hybrid sparse--dense retrieval pipeline, as described in the following chapter." | **HIGH** |
| 499 | "Recent literature demonstrates that 7--8B parameter models are sufficient for English query expansion, but no study has evaluated this approach for Arabic" | **FIX** | Summary bullet reproduces the model-size gap statement corrected at L446. | "Recent literature has established that openly available LLMs (2--8 billion parameters) are capable expansion generators for English, but LLM-based QE has not been evaluated for Arabic, and the interaction between the expansion and the retrieval paradigm remains largely unexamined (Section~\ref{sec:related_work})." **Plus a new bullet:** "Corpus-steered expansion and the placement of expansion within hybrid sparse--dense retrieval have been evaluated only for English, leaving both unexamined for Arabic (Section~\ref{sec:research_gap})." | **MED** |
| 500 | "A clear research gap exists at the intersection of QE techniques and Arabic information retrieval, which this thesis addresses **through systematic model comparison** on the MIRACL benchmark" | **FIX** | Names model comparison as the thesis's answer to the gap. | "A research gap therefore exists at the intersection of LLM-based QE and Arabic information retrieval, which is addressed in this thesis by evaluating blind and corpus-steered expansion across sparse, dense, and hybrid retrieval on the MIRACL Arabic benchmark (Section~\ref{sec:research_gap})." | **HIGH** |
| 503 | "The following chapter presents the methodology … the experimental design, dataset, evaluation pipeline, and **the specific configurations used for each model**." | **FIX** | Describes Chapter 3 as if model configuration were its terminal content; Chapter 3 also covers repetition, hybrid fusion, CSQE, ablation and error analysis. | "The following chapter presents the methodology employed to address this research gap, describing the dataset and experimental environment, the baseline and error-analysis procedures, the adaptation of Query2Doc for Arabic, the model comparison protocol, the query-repetition and hybrid-fusion methodologies, and the CSQE pipeline together with its ablation and retriever-assignment designs." | **MED** |

### chapter3.tex — 0 FIX

| Line | Current text (trimmed) | Verdict | Rationale |
|---|---|---|---|
| 5 | "conducting a comprehensive model comparison across ten open-source LLMs" | KEEP | Factual chapter roadmap; the remainder of the sentence already lists repetition, hybrid, CSQE and error analysis. Optional: "openly available LLMs". |
| 174 | Caption: "an open-source LLM generates a short pseudo-document" | KEEP | Factual figure caption. |
| 184 | "This decision was driven by resource constraints (small open-source models have limited context windows for few-shot examples)…" | KEEP | Methodological justification for zero-shot prompting. See §(e) for an accuracy caveat. |
| 186 | "**Small open-source models:** Rather than using proprietary API-based models, all experiments utilised open-source models with 2--8 billion parameters that can run on Google Colab free-tier GPUs. This approach ensures reproducibility and eliminates API costs." | KEEP | This is a legitimate itemised *deviation from the original paper*, i.e. a methodological fact. Only the bold label reads as a banner. Optional relabel: "**Openly available LLMs (2--8 billion parameters):**". | 
| 265 | "Ten open-source models were evaluated using the identical Query2Doc pipeline." | KEEP | Factual. |
| 270 | "(2) parameter count within the 2--8 billion range to remain executable on Google Colab GPUs; and (3) open-source availability with permissive licences" | KEEP | Factual selection criteria. |

### chapter4.tex — 2 FIX

| Line | Current text (trimmed) | Verdict | Rationale | Proposed replacement (FIX only) | Conf. |
|---|---|---|---|---|---|
| 174 | "The smaller Recall@100 improvement (+2.2\%)…" | KEEP | Not model-related. | — | — |
| 225 | Table row "LLM & GPT-3 (175B) & Qwen 2.5 3B" | KEEP | Factual comparison table against the original paper. | — | — |
| 235 | "despite using a model that is 58$\times$ smaller and zero-shot rather than few-shot prompting" | KEEP | A finding presented as a finding, correctly hedged in the following sentence. | — | — |
| 242 | "ten open-source LLMs were evaluated using the identical Query2Doc pipeline" | KEEP | Factual. | — | — |
| 337 | `\section{Key Findings and Analysis}` | **FIX** | Placed over the *model-comparison* phase only, before repetition, hybrid fusion, CSQE and the error analysis are reported. As titled, it asserts that the model-comparison findings are the thesis's key findings — precisely the old framing. | `\section{Cross-Cutting Findings from the Model Comparison}` | **MED** |
| 341 | "This section synthesises the results **across all experiments** to identify the key findings and their implications." | **FIX** | Factually incorrect as well as mis-framed: the expanded experiments (Sections 4.6–4.10) follow this section. | "This section synthesises the results of the model comparison reported above, identifying the patterns observed across models and their implications for the experiments that follow." | **MED** |
| 343 / 346 | §"Model Size Correlates with Dense Retrieval Performance" — "A positive association was observed … though it must be interpreted cautiously: across the full model set, parameter count is confounded with architecture, training-data volume, and tokeniser design…" | KEEP | Exemplary hedging; observational reporting of a size correlation, explicitly not a predictive claim. Only the subsection *title* asserts more than the body (see §e). | — | — |
| 363 | "This suggests that larger models generate higher-quality pseudo-documents…" | KEEP | Hedged observational inference. | — | — |
| 389 / 391 | "a model's Arabic-capability score on the OALL does not directly predict its query expansion quality" | KEEP | A *negative* result about a predictor is a finding, not a promise of predictive characterisation. Consistent with the de-scoping. | — | — |
| 419 | "QE techniques must be adapted to the retrieval paradigm…" | KEEP | Directly serves Objective 5 under the new framing. | — | — |
| 427–433 | "Strongest overall performance / Strongest BM25 improvement / Best efficiency profile: Qwen3-4B … while fitting on a T4 GPU in FP16" | KEEP | Model-selection guidance stated as results; matches Objective 4. | — | — |
| 495 | "These differences likely reflect variation in pseudo-document length rather than model size per se." | KEEP | Actively resists the size-explains-everything reading. | — | — |
| 985 | "The best system … achieved 0.7137 nDCG@10---a 54.5\% improvement over the BM25 baseline and a 13.9\% improvement over the no-QE hybrid system." | KEEP | Already the new framing. | — | — |

### chapter5.tex — 3 FIX

| Line | Current text (trimmed) | Verdict | Rationale | Proposed replacement (FIX only) | Conf. |
|---|---|---|---|---|---|
| 12 | "This thesis investigated the effectiveness of LLM-based QE for Arabic information retrieval, **focusing on the Query2Doc technique applied using small open-source models**." | **FIX** | The single most consequential remnant: the conclusion chapter opens by scoping the thesis to blind Query2Doc with small models, contradicting the new problem statement and Objectives 7–9 entirely. | "This thesis investigated the extent to which LLM-based QE---generated blindly or steered by the target corpus---can improve Arabic information retrieval across sparse, dense, and hybrid retrieval paradigms. The following conclusions were drawn from the experimental results." | **HIGH** |
| 14 | "**Baseline establishment and error analysis.** …" | KEEP | Findings as findings; maps to Objectives 1–2. (Number-accuracy caveat in §e.) | — | — |
| 16 | "…was successfully adapted for Arabic zero-shot application using models as small as 3 billion parameters … despite using a model 58 times smaller" | KEEP | Finding presented as a finding, correctly attributed to Objective 3. | — | — |
| 18 | "Ten open-source LLMs were evaluated … **For resource-constrained environments**, Qwen3-4B achieved +14.0\% dense improvement while fitting on a T4 GPU in FP16 precision without quantisation." | KEEP | Deployment guidance derived from Objective 4; presented as a practical corollary, not as the contribution. | — | — |
| 20 | "**Analytical findings on model characteristics.**" (bold lead-in only) | **FIX** | The lead-in reproduces the exact de-scoped phrase "model characteristics", signalling a predictive claim that the (well-hedged) body does not make. | "**Patterns observed across model families.**" — body unchanged. | **MED** |
| 22 | "**Dense and sparse retrieval respond differently to QE.** …" | KEEP | Objective 5; central to the new framing. | — | — |
| 24 | "**Query repetition resolves sparse retrieval degradation.** …" | KEEP | Objective 6. | — | — |
| 26 | "**Hybrid retrieval establishes a strong non-QE ceiling.** …" | KEEP | Objective 7. | — | — |
| 28 | "**Corpus-steered expansion validates the corpus grounding hypothesis.** …" | KEEP | Objective 8 (partially — the ablation is missing; see §d). | — | — |
| 30 | "**Retriever-specific query representation is critical.** …" | KEEP | Objective 9 (placement half). | — | — |
| 32 | "**Overall.** LLM-based QE is an effective, modular, and resource-efficient strategy … **Small open-source models with 4--8 billion parameters can deliver substantial retrieval improvements without API costs or proprietary dependencies.** Combined with corpus grounding and hybrid fusion, this approach raised retrieval quality from a BM25 baseline of 0.4621 to 0.7137 NDCG@10…" | **FIX** | The small-model sentence is a legitimate secondary finding, but as the second of three sentences it is given equal billing with the headline result, and corpus steering plus asymmetric fusion appear only as a subordinate clause ("Combined with…"). Reordering is required, not deletion. | "**Overall.** LLM-based QE was found to be an effective and modular strategy for improving Arabic information retrieval under all three retrieval paradigms examined. The largest gains were obtained when the expansion was steered by the target corpus and applied asymmetrically---to the sparse retriever alone---within a hybrid sparse--dense pipeline, which raised retrieval quality from a BM25 baseline of 0.4621 to 0.7137 NDCG@10, an improvement of 54.5\%, and exceeded the strongest unenhanced hybrid baseline by 13.9\%. That these results were obtained with openly available LLMs (2--8 billion parameters), without API costs or proprietary dependencies, makes the approach a practical strategy for real-world Arabic RAG deployments." | **MED** |
| 42, 46, 48 | Challenges: "Resource constraints … limited model sizes to 8 billion parameters", "preview-stage model", "MIRACL … exclusively MSA" | KEEP | Limitations stated as limitations; entirely factual. | — | — |

---

## (c) Proposed Rewrite — chapter2.tex §2.5.4 Research Gap (lines 461–482)

Replaces the whole subsection. British spelling, passive voice, terminology aligned with Chapter 1; the existing L480 paragraph is preserved almost verbatim but promoted into the numbered list.

```latex
\subsection{Research Gap}
\label{sec:research_gap}

Taken together, the literature reviewed above leaves four gaps at the intersection of
LLM-based QE and Arabic information retrieval.

\begin{enumerate}
    \item \textbf{Language.} LLM-based QE has been developed and validated almost
    exclusively on English benchmarks, with recent work establishing that openly
    available LLMs of 7--8 billion parameters are capable expansion generators
    (Section~\ref{sec:modern_qe}). None of these studies addresses \textit{monolingual}
    Arabic retrieval; the sole concurrent exception \cite{macmillanscott_2025_generative}
    addresses the distinct \textit{cross-lingual} setting. Conversely, Arabic RAG research
    has established retrieval and generation baselines (Section~\ref{sec:arabic_ir}) but
    has left the query-formulation stage---which operates upstream of both---uninvestigated.

    \item \textbf{Retriever interaction.} The foundational techniques treat the retriever
    as a black box: the same expanded query is submitted whether retrieval is sparse,
    dense, or hybrid. Whether an expansion that benefits dense semantic matching also
    benefits sparse lexical matching, and whether the remedy proposed for sparse
    retrieval---repetition of the original query---generalises across generator models,
    has not been established for Arabic.

    \item \textbf{Corpus grounding.} The original CSQE work \cite{lei_2024_csqe} was
    evaluated exclusively on English benchmarks using English-language models. Whether
    corpus grounding confers the same benefit for Arabic---where BM25 homonym sensitivity
    may corrupt the first pass and misdirect the expansion---has not been investigated,
    nor have the corpus-grounded and blind components been separated by ablation outside
    English.

    \item \textbf{Placement within a hybrid pipeline.} The interaction between
    corpus-steered expansion and hybrid BM25--Dense fusion remains underexplored. While
    Exp4Fuse \cite{liu_2025_exp4fuse} shows that fusing the original- and expanded-query
    result lists from a \textit{single sparse} retriever outperforms using the expansion
    alone, the asymmetric assignment of expansion across retriever \textit{types} in a
    heterogeneous dense--sparse hybrid---and its behaviour for Arabic---has not been
    studied. Whether applying query expansion to only one retriever in such a hybrid can
    outperform applying it to both is therefore an open question with practical
    implications for retrieval pipeline design.
\end{enumerate}

Specifically, the following questions remain unanswered:

\begin{itemize}
    \item To what extent can LLM-based QE improve Arabic information retrieval under
    sparse, dense, and hybrid retrieval, when the expansion is generated zero-shot by
    openly available LLMs (2--8 billion parameters)?
    \item Does the Query2Doc technique, originally validated with proprietary
    175-billion-parameter models on English text, transfer to Arabic when applied
    zero-shot?
    \item How do LLM-generated expansions interact with sparse as opposed to dense
    retrieval, and must the expansion strategy therefore be adapted to the retrieval
    paradigm?
    \item Can the term dilution that pseudo-document concatenation induces in BM25 be
    remedied by repetition of the original query, and at what repetition factor?
    \item Does grounding the expansion in documents retrieved from the target corpus
    yield more reliable enhancement for Arabic than blind generation, and how do the
    corpus-grounded and blind components contribute individually?
    \item Within a hybrid sparse--dense architecture, to which retriever should the
    expansion be applied?
    \item Which openly available LLMs (2--8 billion parameters) are the most effective
    Arabic expansion generators under each retrieval paradigm, and do Arabic-specialised
    models outperform multilingual models of comparable scale?
\end{itemize}

These questions are addressed in this thesis through a staged experimental programme on
the MIRACL Arabic benchmark, progressing from independent sparse and dense baselines and
their error analysis, through a standardised comparison of openly available LLMs
(2--8 billion parameters) as expansion generators and a query-repetition sweep for sparse
retrieval, to a hybrid sparse--dense fusion baseline and finally the adaptation of CSQE to
Arabic and its placement within the hybrid pipeline, as described in the following chapter.
```

**Notes on the rewrite**
- Ordering of the question list mirrors the objective order in Chapter 1 (Obj 3 → 5 → 6 → 8 → 9), with the model-comparison question (Obj 4) placed last so that it reads as a supporting question rather than the primary one.
- The old bullet "How do Arabic-specialized models compare against multilingual models?" is retained, merged into the final question.
- The de-scoped "what model characteristics…" bullet is dropped entirely.
- Gap 4 preserves the existing L480 wording verbatim from "While Exp4Fuse" onward, so no new citations are introduced.

---

## (d) chapter5.tex Conclusion — Objective Mapping (A6 Preparation)

### Mapping table

| Ch.5 paragraph (line) | Bold lead-in | Maps to objective | Coverage | Action |
|---|---|---|---|---|
| L14 | Baseline establishment and error analysis | **1** and **2** | Full (one paragraph covers two objectives) | Keep. Consider splitting so each objective has its own paragraph. |
| L16 | Query2Doc transfers effectively to Arabic | **3** | **Partial** — the "engineering optimisations required for practical execution on freely available cloud GPUs" half of Objective 3 appears only in §5.2 Challenges (L42), never as a conclusion | Add one sentence (below). |
| L18 | Comprehensive model comparison | **4** (best model per paradigm) | Full | Keep. |
| L20 | Analytical findings on model characteristics | **4** (patterns across families) | Full in body; lead-in mis-titled | Retitle lead-in (see §b). |
| L22 | Dense and sparse retrieval respond differently to QE | **5** | Full | Keep. |
| L24 | Query repetition resolves sparse retrieval degradation | **6** | Full | Keep. |
| L26 | Hybrid retrieval establishes a strong non-QE ceiling | **7** | Full | Keep. |
| L28 | Corpus-steered expansion validates the corpus grounding hypothesis | **8** and part of **9** | **Partial** — the component ablation promised by Objective 8 ("isolating the contributions of its corpus-grounded and blind expansion components through controlled ablation") is never reported in Chapter 5, although Table 4.x gives 0.5381 / 0.5752 / 0.6157 | Add an ablation paragraph (below). |
| L30 | Retriever-specific query representation is critical | **9** (placement half) | Full for placement | Keep. |
| — | *(absent)* | **9** (per-query error analysis half) | **Missing** — the error analysis appears only as one supporting clause inside L28 | Add an error-analysis paragraph (below). |
| L32 | Overall | *(synthesis — no single objective)* | Mis-weighted | Replace (see §b, L32). |

**Objectives with no dedicated conclusion paragraph:** none entirely absent, but **Obj 3 (engineering half)**, **Obj 8 (ablation half)** and **Obj 9 (error-analysis half)** are under-covered.

**Conclusion content with no objective:** none. The "resource-constrained environments / Qwen3-4B on a T4" sentence (L18) attaches acceptably to Objective 3's "practical execution on freely available cloud GPUs"; the ALLaM drop is handled in §5.2 Challenges, which is the right place.

**Opening sentence (L12):** does not match the new problem statement — replacement given in §(b). Confidence **HIGH**.
**"Overall" paragraph (L32):** partially matches; the three-paradigm claim of the RQ is not stated and the headline mechanism is subordinated — replacement given in §(b). Confidence **MED**.

### Proposed additional conclusion paragraphs

**1. Extend L16 (Objective 3, engineering half)** — append to the existing paragraph:

> "Practical execution on freely available cloud GPUs was achieved through a set of engineering optimisations---batched generation, a 128-token generation limit, 4-bit quantisation where memory required it, and a two-notebook workflow separating query generation from retrieval evaluation---which reduced a full-corpus experiment to approximately forty minutes."
> *(Confidence: HIGH — every figure is already stated in §5.2 Challenges, item 1.)*

**2. New paragraph after L28 (Objective 8, ablation half):**

> "**Corpus-grounded and blind expansion are complementary.** Component ablation confirmed that neither expansion source is sufficient in isolation. On BM25, corpus-only expansion achieved 0.5381 NDCG@10 and blind-only expansion 0.5752, whereas the balanced two-corpus/two-blind configuration achieved 0.6157---an improvement of +0.0405 over the stronger single component. The same ordering held within the fused system, where corpus-only, blind-only and combined expansion yielded 0.6616, 0.7082 and 0.7137 respectively. Corpus samples were found to anchor the expansion to attested Wikipedia vocabulary, while blind samples widened answer-space coverage beyond the first-pass retrieval window (Section~\ref{sec:res_csqe_ablation})."
> *(Confidence: HIGH — all five figures verified against chapter4.tex L620–622 and L695–697.)*

**3. New paragraph after L30 (Objective 9, error-analysis half):**

> "**Improvement is concentrated where the query is underspecified and the first pass succeeds.** The per-query analysis showed that the final system improved 56.8\% of queries and regressed 16.6\%, with a mean per-query gain of +0.1890 NDCG@10. The gain held across every query-length bucket, being largest proportionally for short queries of one to three words (+43.6\%) and largest in absolute terms for medium queries of four to eight words (+0.197), and smallest for long queries of nine or more words (+0.132, +23.3\%), whose greater information content already mitigates the information poverty that motivates expansion. First-pass quality was identified as the largest single modulator: where the first pass had already retrieved a relevant document at rank one (36.6\% of queries), near-ceiling retrieval of 0.8877 NDCG@10 was achieved, against 0.5814 where it had not (Section~\ref{sec:res_error_csqe})."
> *(Confidence: HIGH — figures verified against chapter4.tex L799–803, L832–833 and L850–852. **Note:** these are the thesis's own 1--3 / 4--8 / 9+ word buckets, which differ from the `<5` / `>=10` word buckets recorded in `CLAUDE.md`; the chapter-4 values are the ones used above.)*

---

## (e) Borderline Calls

1. **chapter2 L423**, "a finding that has since been challenged by newer, more capable small models." Ruled KEEP as a literature-level correction, but it is the one sentence in the review whose *rhetorical purpose* is to set up the old small-model thesis. If the A6 pass wants to be strict, "…a finding since overturned by more capable models at smaller scale (Section~\ref{sec:modern_qe})" is more neutral. Confidence that KEEP is correct: MED.

2. **chapter2 L429 and L434.** Both are accurate literature summaries organised around parameter count. They are KEEP under the rubric, but L429 would carry the new framing better with an added clause: "…and, in every case, on a retriever-agnostic application of the expansion." Optional, LOW priority.

3. **chapter2 L279 caption and chapter3 L186 label** use "open-source" where Chapter 1 uses "openly available". Not framing errors, purely a terminology-consistency question. I did not count these as FIX; if the A6 pass runs a global terminology sweep, they are the natural targets.

4. **chapter4 L343 subsection title**, "Model Size Correlates with Dense Retrieval Performance." The body is exemplary in its hedging and I ruled KEEP, but the title asserts a correlation more strongly than the confounded evidence supports. A retitle to "Model Size and Dense Retrieval Performance" would cost nothing. Confidence LOW that this needs changing.

5. **chapter3 L184**, "small open-source models have limited context windows for few-shot examples." Ruled KEEP as methodology, but the claim is questionable on the facts: the models used have 12K–128K context windows (chapter2 L293, L320), so context length is not a credible obstacle to four demonstrations. This is an *accuracy* issue rather than a framing one; the honest justification is the one already given in the same sentence ("the desire to evaluate model capabilities without task-specific demonstrations"). Flagged for the A6 pass, LOW.

6. **chapter2 §2.1.4 QE taxonomy (L86–92)** lists HyDE, Query2Doc and GRF but not CSQE, which is introduced only in Related Work (L436). Not an old-framing remnant, but under the new framing the thesis's central technique should appear in the technique taxonomy, not solely in the literature narrative. Out of A5 scope; recorded here because it will surface in any Chapter 2 edit.

7. **chapter4 L876**, "All 1,061 big-win queries" — the same count (1,061) appears at L832 as the number of first-pass-successful queries. Possibly a genuine coincidence, possibly a transcription collision. Unrelated to A5, but worth verifying before A6 quotes either number.

8. **chapter5 L14** repeats the baseline error-analysis figures ("34\% of queries failed", "72\% of long-query performance"). The project memory records that the §4.2/§3.3 baseline error analysis was derived from a buggy file with corrected canonical values. Ruled KEEP for A5 purposes (it is not a framing issue), but these numbers should be reconciled with the corrected run before the conclusion is finalised.

---

## chapter1.tex Verification (quick check, no rewrite)

Four in-scope occurrences, **all clean**:

| Line | Text | Status |
|---|---|---|
| 11 | "developed and validated on English benchmarks using proprietary models with 175 billion or more parameters" | Literature fact — correct |
| 11 | "under the practical constraint of openly available models of modest scale rather than commercial application programming interfaces (APIs)" | Constraint framed as a constraint — correct |
| 18 | "leaving unanswered the questions on which Arabic deployment depends… while relying only on openly available models of practical scale" | Correct; scale is a condition on the answer, not the question |
| 32, 34 | "openly available LLMs" / "openly available LLMs spanning 2--8 billion parameters" | Sanctioned phrasing — correct |

No survivals of the old research question, no "model characteristics" clause, no small-model-viability contribution claim. The central RQ at L18 and the nine objectives at L28–L44 match the brief exactly.

**One minor terminology drift:** L11 says "openly available models of modest scale" and L18 "openly available models of practical scale", where the sanctioned form is "openly available LLMs (2--8 billion parameters)". Cosmetic only; flagged, not proposed as a fix.
