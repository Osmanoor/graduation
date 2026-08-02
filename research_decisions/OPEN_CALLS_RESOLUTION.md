# Open Calls Resolution — J1–J7

**Date:** 2026-07-29
**Scope:** decisions left open by Phase A (`PHASE_A_COMPLETION_REPORT.md` §"Open items", `THESIS_FINAL_SUBMISSION_TASKS.md` "Phase A review flags").
**Status:** report only — **no `.tex` file was modified.** Paste-ready text is given for each item.
Thesis paths are relative to `University_of_Khartoum__EEE_bachelor_s_thesis_template/`.

**Verification note before you start:** several A7 fixes have already landed since that report was written. Confirmed applied in the working tree: B1 (O2 names linguistic failure patterns), B2 (§1.3 covers §3.5), B3 (Dense+CSQE in ¶8), B4+M10 (three placements, all RRF), B6 (model-dependent optimum), M1, M2, M3, M4, M5, **M6 and M7 (Ch.2 questions reordered — model comparison is now Q3, and Q1 is verbatim-aligned with the RQ)**, M8, M9, M13, A1–A4 (acronym re-glosses removed, "Normalised" sweep done). **Still open:** B5 (abstract — Phase B), M12 (partial: `chapter3.tex:265`, `chapter3.tex:186` and `5-Abstract.tex` still say "open-source"), M14 (SILMA naming). Do not re-fix the applied ones.

---

## J1 — §1.1 closing sentence (pre-announcing the asymmetric finding)

### Evidence

| Location | Text | Bearing |
|---|---|---|
| `chapter1.tex:18` (last sentence) | "In answering it, this thesis develops and validates a pipeline that couples corpus-steered query expansion with **asymmetric hybrid sparse--dense fusion, in which the expansion is applied to the sparse retriever only**." | The sentence under review |
| `chapter1.tex:44` (Objective 9) | "To determine the **optimal placement** of query expansion within the hybrid pipeline by evaluating retriever-specific application strategies---expanding the sparse retriever, the dense retriever, or both" | Poses it as open, 26 lines later |
| `chapter2.tex:473` (Gap 4) | "Whether applying query expansion to only one retriever in such a hybrid can outperform applying it to both **is therefore an open question**" | Ch.2 does **not** pre-announce |
| `chapter2.tex:485` (Q7) | "Within a hybrid sparse--dense architecture, to which retriever should the expansion be applied?" | Ch.2 does **not** pre-announce |
| `chapter2.tex:488` (closing) | "…and finally the adaptation of CSQE to Arabic **and its placement within the hybrid pipeline**" | Announces the *programme*, not the answer — the model to imitate |
| `chapter3.tex:473` (§3.8.3) | "whether expansion helps or hurts each retriever **was left as an empirical question**, with the causal interpretation reserved for the results discussion" | Ch.3 explicitly withholds the answer |
| `chapter3.tex:486` (Fig. 3.9 caption) | "CSQE-expanded queries are fed to BM25 while the original short queries are fed to mDPR … yielding the headline nDCG@10 of 0.714" | The *one* place before Ch.4 that reveals it — but attributed ("identified empirically in Chapter~4", `chapter3.tex:481`) |
| `5-Abstract.tex:9` | States 0.7137 and the corpus-steered pipeline | Normal for an abstract; not a precedent for §1.1 |

So four of the thesis's own framing sites (Ch.2 gap 4, Ch.2 Q7, §3.8.3, Objective 9) hold the placement question open, and exactly one sentence — the problem statement — closes it.

### **RECOMMENDATION: rephrase — keep the pipeline announcement, delete the "asymmetric / sparse-retriever-only" specificity, and replace it with a statement that the placement is determined empirically.**

**Reasoning.** The supervisor's technology-driven mandate and task A1 both ask for the final pipeline to appear as the answer, and that is satisfied by naming *CSQE + hybrid fusion* — the artefact. What A1 does not require is naming the *result*. The current sentence does not merely preview a finding; it contradicts Objective 9, which promises to *determine* the placement, and Ch.2 Q7/gap 4, which state that no one has determined it. An examiner reading §1.1 → §1.2 in sequence meets the answer before the question, which reads as post-hoc objective-writing — the single most common committee criticism of the Problem↔Objectives chain. The rephrase costs nothing narratively: "determines empirically where the expansion should be applied" is *more* interesting than asserting it, because it flags the contribution as a finding rather than an assumption.

### Paste-ready replacement

Replace the final sentence of `chapter1.tex:18`:

> In answering it, this thesis develops and validates a pipeline that couples corpus-steered query expansion with asymmetric hybrid sparse--dense fusion, in which the expansion is applied to the sparse retriever only.

with:

> In answering it, this thesis develops and validates a pipeline that couples corpus-steered query expansion with hybrid sparse--dense fusion, and determines empirically at which point in that pipeline the expansion should be applied.

*(Optional companion, if you also want Fig. 3.9's caption to stop pre-empting §4.9: change "Architecture of the thesis's best-performing system" to "Architecture of the configuration identified in Chapter~\ref{chap:results} as the best-performing system". Low priority — the caption already carries the forward reference in the body text.)*

---

## J2 — Reinstating the word "small" in the objectives

### Evidence

- **Objectives (`chapter1.tex:28–44`):** "small" appears **zero** times. Scope is carried numerically: O3 "openly available LLMs"; O4 "openly available LLMs spanning 2--8 billion parameters".
- **Ch.5 conclusions:** "small" **already appears once, legitimately** — `chapter5.tex:16` (¶2): "successfully adapted for Arabic zero-shot application using models **as small as 3 billion parameters**". Also `chapter5.tex:36` "a small cost in effectiveness" (unrelated sense).
- **Ch.2:** every remaining "small" refers to the *literature*, not to this thesis's models — `chapter2.tex:423` ("the authors found smaller models insufficient"), `:427`, `:429`, `:440`. All legitimate, all kept by the A5 sweep.
- **Ch.3:** two self-descriptive survivals — `chapter3.tex:184` ("small open-source models have limited context windows", see J4) and `chapter3.tex:186` (bold item label **"Small open-source models"**).
- **`5-Abstract.tex:3,5`:** "small, open-source models", "small open-source LLMs" — pre-A1 framing, already slated for rewrite under B1.

### **RECOMMENDATION: do NOT reinstate "small" in any objective; instead delete the two remaining self-descriptive uses in Ch.3, so the thesis scopes itself by parameter count everywhere.**

**Reasoning.** The A5 sweep's purpose was to move the thesis's headline off "small models can do QE" and onto CSQE + placement; putting "small" back into the objectives — the most load-bearing list in the document — partially undoes that at the highest-visibility point. The word is also contestable in a way the number is not: a committee member can dispute whether 8B is "small" in 2026, but not that it is 8 billion parameters. Crucially, **the absence creates no inconsistency with Ch.5**, because ¶2 already carries the claim in its evidence-backed form ("as small as 3 billion parameters" — tied to the Qwen 2.5 3B result). The only real inconsistency runs the other way: Ch.3 still calls the models "small open-source", which conflicts with both the objectives' numeric phrasing and the M12 "openly available" standard. Fix Ch.3, not Ch.1.

**Trade-off, stated honestly:** if Osman or Dr. Tahani wants the small-model angle visible in the objectives for the defence narrative, the least damaging single site is **Objective 3** (the Query2Doc-transfer objective, where the 175B→3B contrast is the actual point), not Objective 4 (the comparison objective, where the numeric range is doing precise work). Wording in that case: `…for Arabic zero-shot application using small, openly available LLMs, including…`. I recommend against it, but it is defensible there.

### Paste-ready edits (Ch.3 alignment, recommended path)

`chapter3.tex:186` — replace the item label and first clause:

> \item \textbf{Small open-source models:} Rather than using proprietary API-based models, all experiments utilised open-source models with 2--8 billion parameters that can run on Google Colab free-tier GPUs.

with:

> \item \textbf{Openly available models of 2--8 billion parameters:} Rather than using proprietary API-based models, all experiments used openly available models that run on Google Colab free-tier GPUs.

`chapter3.tex:265` (folds in the outstanding half of M12):

> Ten open-source models were evaluated using the identical Query2Doc pipeline.

→

> Ten openly available models were evaluated using the identical Query2Doc pipeline.

*(`chapter2.tex:275` "open-source availability with permissive licensing" and `chapter2.tex:279` caption "Open-source LLMs" are the last two M12 sites; note `chapter2.tex:275` also still says "permissive licensing", which M13 already corrected in §3.5.1 — see J3.)*

---

## J3 — Aya CC-BY-NC licence caveat: placement

### Evidence — licence facts verified against `tab:model_comparison` (`chapter2.tex:390–409`)

| Model | Licence (Ch.2 table) | Corroboration |
|---|---|---|
| **Aya Expanse 8B** | **CC-BY-NC** | `chapter2.tex:363`: "distributed under a CC-BY-NC-4.0 (non-commercial) license" |
| Jais-2-8B | **Apache 2.0** | `chapter2.tex:304`: "Apache 2.0 license (**gated access**)" |
| ALLaM-7B | Apache 2.0 | (dropped model — not an alternative) |
| Qwen 2.5 7B / Qwen3-4B / Qwen3-8B | Apache 2.0 | — |
| Qwen 2.5 3B | Qwen Research (non-commercial) | `chapter2.tex:330` |
| Gemma 3 4B | Gemma TOU | — |
| Falcon-H1-3B, SILMA Kashif-2B | "Open" (unspecified) | — |

**Best Apache-2.0 alternative = Jais-2-8B**, and the measured gap to Aya is:

| Comparison | Aya | Jais-2 | Gap | Source |
|---|---|---|---|---|
| Dense, blind QE | 0.6164 | 0.6018 | −0.0146 (−2.4 % rel.) | `chapter4.tex:259–260` |
| BM25, blind QE, *n*=1 | 0.5046 | **0.5122** | **Jais-2 is +0.0076 ahead** | `chapter4.tex:306–307` |
| BM25, best repetition (β=2 both) | 0.5855 | 0.5731 | −0.0124 (−2.1 % rel.) | `chapter4.tex:477–478` |
| **CSQE / final 0.7137 system** | Aya only | **never run** | **not measured** | `chapter3.tex:436`, `:468` |

**This is the material finding.** The current wording at `chapter5.tex:36` — "Apache-2.0 alternatives such as Jais-2-8B **follow at a small cost in effectiveness**" — is attached to a sentence about the 0.7137 headline, but no Jais-2 CSQE run exists anywhere in the thesis or the experiment log. The claim is an extrapolation from the blind-QE leaderboards to the CSQE pipeline. It is also directionally wrong for one of the three comparisons (Jais-2 beats Aya on BM25 at *n*=1).

### §5.2 Challenges — current contents and style

Seven numbered items (`chapter5.tex:45–59`): 1 Resource constraints · 2 BM25 term dilution · 3 Dropped model · 4 Dataset scope · 5 Single QE technique · 6 Baseline retriever strength · 7 First-pass quality dependence. Each is a bold label + 2–4 sentences stating a limitation and its consequence for interpretation. Items 4–6 are **scope limitations**, not literal "challenges encountered" — so a licensing/generality limitation fits the established style without strain.

### **RECOMMENDATION: SPLIT — keep a shortened, factually scoped licence clause in ¶12 (Overall) where the deployment claim is made, and add a new §5.2 Challenges item that states the untested extrapolation honestly.**

**Reasoning.** The caveat must stay in ¶12 because that is where the vulnerable claim lives ("practical for Arabic RAG deployments"); an examiner who spots CC-BY-NC will attack that exact sentence, and a caveat in a later section does not defend it. But ¶12 is the wrong place to carry the *evidential* weakness, because the Overall paragraph is the thesis's strongest rhetorical moment and should not host a hedge about an experiment that was not run. Splitting keeps ¶12 short and true (the licence fact, plus a comparison scoped to where it was measured) and moves the honest limitation to Challenges, where limitations belong and where item 6 ("Baseline retriever strength") already establishes the "the magnitude may differ under X" pattern.

### Paste-ready text

**(a)** `chapter5.tex:36` — replace the final clause, from "the approach is therefore practical…" to the end:

> …without API costs or dependence on proprietary models. The approach is therefore practical for Arabic RAG deployments, subject to the licence of the chosen generator: the best-performing model, Aya Expanse 8B, is released under a non-commercial licence, whereas Apache-2.0 alternatives are available, the strongest of which---Jais-2-8B---was within 2.4 per cent of Aya Expanse in the model comparison (Table~\ref{tab:model_comparison}).

**(b)** New item 8 in §5.2 Challenges, after `chapter5.tex:58` (item 7):

> \item \textbf{Generator licensing.} The generator used for the corpus-steered pipeline, Aya Expanse 8B, is distributed under a CC-BY-NC-4.0 licence and may therefore not be used commercially (Section~\ref{sec:aya}). Apache-2.0 models of the same scale were evaluated in the model comparison, where Jais-2-8B trailed Aya Expanse by 2.4 per cent on dense retrieval and 2.1 per cent on sparse retrieval and in fact led it before query repetition was applied (Sections~\ref{sec:res_model_comparison} and~\ref{sec:res_repetition}); the CSQE and fusion experiments, however, were run with Aya Expanse alone, so the cost of substituting a permissively licensed generator into the final pipeline was not measured directly.

**(c)** *Optional* — §5.3 Recommendations, new item 9 (only if you want the loop closed):

> \item \textbf{Permissively licensed generator for the final pipeline.} The CSQE and fusion experiments should be repeated with an Apache-2.0 generator such as Jais-2-8B to quantify the effectiveness cost of removing the non-commercial licence constraint from the best-performing configuration.

*(Also note for consistency: `chapter2.tex:275` still lists selection criterion 3 as "open-source availability with **permissive licensing**", which M13 already corrected at `chapter3.tex:270` to "whether permissive or non-commercial". Align `chapter2.tex:275` the same way.)*

---

## J4 — `chapter3.tex:184` zero-shot justification ("limited context windows")

### Evidence

Current text (`chapter3.tex:184`):
> \item \textbf{Zero-shot prompting:} The original Query2Doc paper employed few-shot prompting with 4 demonstration examples using GPT-3 (\texttt{text-davinci-003}, 175B parameters). In this work, zero-shot prompting was adopted **exclusively**. This decision was driven by **resource constraints (small open-source models have limited context windows for few-shot examples)** and the desire to evaluate model capabilities without task-specific demonstrations.

**Context windows actually stated in Ch.2** — the claim is false on the thesis's own evidence:

| Model | Context window | Source |
|---|---|---|
| Falcon-H1-Arabic-3B | **128K tokens** | `chapter2.tex:293` |
| Gemma 3 4B-IT | **128K tokens** | `chapter2.tex:354` |
| SILMA Kashif-2B | **12K tokens** (the smallest stated anywhere) | `chapter2.tex:320` |

Four Query2Doc demonstrations are a few hundred tokens. Even the 12K floor leaves ~11.7K spare. No model in Table 2.4 is stated to have a context window that constrains few-shot prompting, and none is claimed to.

**Second defect in the same sentence:** "adopted **exclusively**" is contradicted by the thesis's own CSQE prompt — `chapter3.tex:452`: "A single English worked example (a query about warm-blooded sharks, taken from the original CSQE paper) was prepended as a **one-shot demonstration**." As written, §3.4.2 makes a thesis-wide claim that §3.8.1 breaks.

**What else §3.4.2 claims** (`chapter3.tex:183–191`): item 2 openly available 2–8B models on free-tier GPUs; item 3 Arabic-only generation via system prompt; item 4 retriever-specific concatenation. None of these supplies a context-window rationale. The genuine, defensible grounds available in the document are: (i) the capability-evaluation argument already in the sentence; (ii) generation cost — 2,896 queries × 10 models under the batching budget of §3.4.4 (`chapter3.tex:226–234`), where prompt length multiplies directly into runtime; (iii) no curated Arabic demonstration set exists — the original demonstrations are English, and `chapter5.tex:75` (Recommendation 4) explicitly parks "few-shot prompting with curated Arabic demonstration examples" as *future work*, which is the honest reason.

### **RECOMMENDATION: replace the parenthetical with the generation-cost argument, drop "exclusively" in favour of scoping the claim to pseudo-document generation, and add the missing-Arabic-demonstrations reason, which is the strongest of the three and already forward-referenced in §5.3.**

**Reasoning.** The context-window claim is the only factually false statement in §3.4.2 and it is falsifiable from Table 2.4 two chapters earlier — cheap ammunition for an examiner. The replacement loses nothing: the honest reasons are stronger, since "no Arabic demonstration set exists, and building one would introduce a design variable absent from the original method" both justifies the choice and pre-empts "why didn't you try few-shot?", which §5.3 item 4 already answers as future work. Dropping "exclusively" removes the §3.8.1 contradiction at the cost of one word.

### Paste-ready replacement

Replace all of `chapter3.tex:184` with:

> \item \textbf{Zero-shot prompting:} The original Query2Doc paper employed few-shot prompting with 4 demonstration examples using GPT-3 (\texttt{text-davinci-003}, 175B parameters). In this work, pseudo-document generation was performed zero-shot. The demonstrations of the original method are English query--passage pairs, and no curated set of Arabic demonstrations was available; constructing one would have introduced a design variable absent from the original method, and it is therefore left as a direction for future work (Section~\ref{sec:recommendations}). Zero-shot prompting also keeps every prompt short, which matters when generation is batched over 2,896 queries for each of ten models within the available GPU budget (Section~\ref{sec:meth_q2d_batch}), and it allows each model's Arabic expansion capability to be assessed without task-specific demonstrations.

*(This wording is deliberately compatible with §3.8.1's one-shot CSQE prompt: it scopes the claim to "pseudo-document generation". If you prefer to be explicit, append to `chapter3.tex:452`: "This one-shot demonstration is the sole exception to the zero-shot protocol of Section~\ref{sec:meth_q2d_modifications}." — recommended, it costs one sentence and closes the loop.)*

---

## J5 — CSQE missing from the Ch.2 QE taxonomy (§2.1.4)

### Evidence

- **§2.1.4 taxonomy** (`chapter2.tex:81–102`): four bold pseudo-headings — Query Expansion (`:86`), Query Decomposition (`:94`), Query Disambiguation (`:96`), Query Abstraction (`:98`). The Query Expansion itemize (`:88–92`) lists **HyDE** (`:89`), **Query2Doc** (`:90`), **GRF** (`:91`). **CSQE is absent.**
- The lead-in at `chapter2.tex:86` already names the ancestor: "Traditional query expansion methods such as **Relevance Model 3 (RM3)** extract expansion terms from **pseudo-relevant documents retrieved in a first pass**." — a perfect hook, currently unused.
- **CSQE's full form is first written in Chapter 1**, at `chapter1.tex:42` (Objective 8), and the technique is not explained until `chapter2.tex:436` (§2.5.2, Related Work). A reader who meets "Corpus-Steered Query Expansion (CSQE)" in Objective 8 and turns to the QE taxonomy to find out what it is finds nothing.
- §2.5.2's description (`chapter2.tex:436`) covers: the two-stage pipeline, top-*k* first pass, combination with blind expansion, the anti-hallucination motivation, and the 30 % MAP figure. **The taxonomy entry must not repeat any of that.**
- **C5 interaction** (`THESIS_FINAL_SUBMISSION_TASKS.md:106–107`): C5 promotes the four bold pseudo-headings to 2.1.4.1–2.1.4.4. The HyDE/Query2Doc/GRF itemize sits *inside* "Query Expansion" and remains an itemize under the new §2.1.4.1. **An `\item` therefore survives C5 unchanged** — no rework needed either way.

### **RECOMMENDATION: yes — add CSQE as a fourth `\item` in the Query Expansion itemize, immediately after GRF (`chapter2.tex:91`), written as a *taxonomic* entry (what class of thing it is) that defers all mechanism and results to §2.5.2.**

**Reasoning.** CSQE is the thesis's central technique and the only one of the four named LLM-expansion methods that is missing from the chapter whose stated job (`chapter1.tex:54`) is to introduce "QE techniques". Its omission also loses a genuinely useful taxonomic point that no other section makes: HyDE, Query2Doc and GRF all draw expansion text from the model's parametric knowledge, whereas CSQE draws it from the corpus — which is *exactly* the axis Ch.2 gap 3 and Objective 8 turn on, and which the RM3 sentence at `:86` sets up but never pays off. Placing it last in the itemize preserves the list's existing order (chronological, and Query2Doc-then-its-extension reads naturally). Two to three sentences is enough; anything longer duplicates §2.5.2.

### Paste-ready text

Insert after `chapter2.tex:91` (the GRF item), as the last item of the itemize:

> \item \textbf{CSQE:} Proposed by Lei et al. \cite{lei_2024_csqe}, CSQE draws part of the expansion from documents retrieved in a first pass over the target corpus rather than from the model's parametric knowledge alone, and combines this corpus-grounded material with a blind Query2Doc expansion. It therefore sits between generative expansion and the classical pseudo-relevance feedback of RM3: the retrieval step supplies the candidate text, and the LLM performs the selection that RM3 performs statistically. CSQE is the technique adapted for Arabic in this thesis; its pipeline and reported results are described in Section~\ref{sec:modern_qe}.

**If C5 has already converted the itemize to numbered subsections**, use the identical body under a heading:

> \subsubsection{CSQE}
> \label{sec:qe_csqe}
>
> Proposed by Lei et al. \cite{lei_2024_csqe}, CSQE draws part of the expansion from documents retrieved in a first pass over the target corpus rather than from the model's parametric knowledge alone, and combines this corpus-grounded material with a blind Query2Doc expansion. It therefore sits between generative expansion and the classical pseudo-relevance feedback of RM3: the retrieval step supplies the candidate text, and the LLM performs the selection that RM3 performs statistically. CSQE is the technique adapted for Arabic in this thesis; its pipeline and reported results are described in Section~\ref{sec:modern_qe}.

**One-word companion edit** (recommended, because CSQE is not purely generative): at `chapter2.tex:86`, change

> Modern approaches leverage LLMs to generate expansion content, which can take several forms:

to

> Modern approaches leverage LLMs to generate or select expansion content, which can take several forms:

---

## J6 — CLAUDE.md drift: exact corrections

`f:\Desktop\graduation\CLAUDE.md` was checked table-by-table against `chapter4.tex`. **Result: the Dense, BM25-repetition, Hybrid, CSQE and CSQE-ablation tables are all numerically correct** (spot-verified against `chapter4.tex:22–25, 166–169, 257–270, 304–315, 453–462, 477–485, 533–547, 593–599, 619–622, 669–678, 695–697, 712–715`). Five defects follow.

### (a) BLOCKER — query-length buckets are from a superseded bucketing

**Find:**
```
- Short queries (< 5 words, n=865): Δ = +0.1990 | Long queries (≥10 words, n=131): Δ = +0.1053
```
**Replace with:**
```
- Query-length buckets — CANON is 1-3 / 4-8 / 9+ words (ch4 Tables 4.4 and 4.19). Do NOT use "<5 / >=10 words".
- Baseline (mDPR, no QE) by bucket: 1-3 words 0.345 (n=147) | 4-8 words 0.511 (n=2,495) | 9+ words 0.476 (n=254)
- CSQE+Hybrid gain by bucket: 1-3 words +0.161 (+43.6%) | 4-8 words +0.197 (+38.8%) | 9+ words +0.132 (+23.3%)
```
*Sources: `chapter4.tex:95–97` (baseline buckets), `chapter4.tex:850–852` (gain buckets). The old n=865/n=131 counts do not correspond to any table in the thesis.*

### (b) BLOCKER — Exp 2.1 table mixes CC and RRF, and omits the two RRF rows Ch.5 ¶10 now cites

The current table lists Dense-expanded and Both-expanded only in their **CC** form, but Ch.5 ¶10 (`chapter5.tex:32`) was rewritten under A7/B4+M10 to compare all three placements **like-for-like under RRF**. Anyone quoting CLAUDE.md today would reproduce the exact defect M10 fixed.

**Find** the five data rows under `### Reference Baselines — CSQE + Hybrid Fusion (Exp 2.1, 2026-04-10)` and **replace the whole table body with:**
```
| Method | Fusion | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|--------|---------|-----------|------------|-----|
| Hybrid RRF k=20 (no QE) | RRF | 0.6267 | 0.7597 | 0.9466 | 0.6517 |
| B: Dense-expanded (BM25 raw + Dense+CSQE) | RRF | 0.6474 | 0.7928 | 0.9571 | 0.6578 |
| B: Dense-expanded (BM25 raw + Dense+CSQE) | CC α=0.4 | 0.6588 | 0.7851 | 0.9569 | 0.6777 |
| C: Both-expanded (BM25+CSQE + Dense+CSQE) | RRF | 0.6936 | 0.8290 | 0.9660 | 0.7037 |
| C: Both-expanded (BM25+CSQE + Dense+CSQE) | CC α=0.5 | 0.6959 | 0.8249 | 0.9647 | 0.7079 |
| A: BM25-expanded (BM25+CSQE + Dense raw) | CC α=0.6 | 0.7088 | 0.8302 | 0.9717 | 0.7268 |
| **A: BM25-expanded (BM25+CSQE + Dense raw)** | **RRF k=20** | **0.7137** | **0.8363** | **0.9734** | **0.7362** |

**Like-for-like RRF comparison (use THIS for the placement claim): 0.7137 (sparse-only) > 0.6936 (both) > 0.6474 (dense-only).**
```
*Source: `chapter4.tex:669–678`.*

### (c) MAJOR — missing corpus-level vs per-query-mean warning (a live trap)

**Find:**
```
### Error Analysis Key Numbers (2026-04-11)
- CSQE improves 56.8% of queries, regresses 16.6%, mean delta +0.1890 nDCG@10
```
**Replace with:**
```
### Error Analysis Key Numbers (2026-04-11)
- CSQE improves 56.8% of queries, regresses 16.6%, ties 26.6%; mean delta +0.1890 nDCG@10
- ⚠️ Per-query MEAN of the best system is 0.6936, NOT 0.7137. The 0.7137 headline is the corpus-level
  pooled evaluation. Never mix the two (ch4 Table 4.17 caption, chapter4.tex:793).
- Baseline for all per-query deltas = Aya blind BM25 n=1 = 0.5046 (not the hybrid, not 0.5855)
```
*Sources: `chapter4.tex:793`, `:803–808`, `:835`.*

### (d) MINOR — regression counts, and an unresolved thesis-side conflict

**Find:**
```
- Regressions (367): 52% Type A (strong BM25 hurt by expansion), 36% Type B (poisoned first-pass), 12% Type C
```
**Replace with:**
```
- Regressions (367): Type A 191 (52%, strong BM25 hurt by expansion), Type B 131 (36%, poisoned first-pass), Type C 45 (12%)
- ⚠️ OPEN CONFLICT — SILMA 2B, BM25, n=1: chapter4.tex:311 (Table 4.7) says 0.4277 (-7.4%);
  chapter4.tex:462 (Table 4.11) says 0.4194. The tables are each internally consistent but disagree
  with each other. The number below (0.4194) follows Table 4.11. Resolve before submission.
```
*Sources: `chapter4.tex:908–910`; the SILMA conflict is a genuine thesis-side inconsistency — see J7 item 6.*

### (e) MINOR — stale project facts (outside the reference tables, but actively misleading)

**Find:** `- **Deadline:** February 15, 2026` → **Replace:** `- **Deadline:** thesis in final-submission editing (see research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md)`

**Find** the whole block:
```
## What's NOT Decided (Do Not Assume)
- Which embedding model to use
- Which query enhancement technique first
- Which Arabic LLM for enhancement
- Specific implementation details
```
**Replace with:**
```
## Settled (was "not decided" — all resolved by experiment)
- Retrievers: mDPR (dense) + BM25S (sparse), k1=0.9 b=0.4
- Technique: Query2Doc first, then CSQE (2 corpus + 2 blind, α=4)
- Generator: Aya Expanse 8B (CC-BY-NC — see Ch.5 licence caveat)
## Still open
- Nothing experimental. Remaining work is thesis editing (see THESIS_FINAL_SUBMISSION_TASKS.md).
```

**Also:** the heading `### Reference Baselines — Dense Retrieval (mDPR + Query2Doc)` contains an `Aya 8B CSQE (exp_013)` row, which is not Query2Doc. Either retitle to `— Dense Retrieval (mDPR)` or move that row into the CSQE table. Cosmetic; your call.

---

## J7 — Remaining cross-list inconsistencies

Checked: the 9 objectives (`chapter1.tex:28–44`), the 7 Ch.2 questions (`chapter2.tex:479–485`), the 12 Ch.5 conclusion paragraphs (`chapter5.tex:14–36`).

**Good news first:** "openly available" is now used consistently across **all three** lists (O3, O4; Q1, Q3; ¶3, ¶12) — no "open-source" survives in any of them. The Ch.2/Ch.1 **ordering mismatch (A7 M6) and the Q1/RQ wording mismatch (A7 M7) are both already fixed**: Ch.2's questions now run Q1↔RQ, Q2↔O3, Q3↔O4, Q4↔O5, Q5↔O6, Q6↔O8, Q7↔O9, and `chapter2.tex:488` acknowledges O1/O2/O7 as prerequisites. Six issues remain.

| # | Term | Where it diverges | **Recommended standard** |
|---|---|---|---|
| **1** | "query enhancement" spelled out after (QE) is defined | `chapter1.tex:40` (**Objective 7**): "hybrid sparse--dense fusion baseline without **query enhancement**". QE is defined at `chapter1.tex:9`. This is the **only** re-expansion left in Ch.1–5 (verified by grep) and is the same defect class as A7's A1–A4. | **Objective 7 → "…without QE, quantifying the performance ceiling…"** |
| **2** | Capitalised "Dense" in prose | `chapter5.tex:32` (¶10): "preserved **the Dense retriever's** independent semantic signal" vs `chapter5.tex:28` (¶8): "Applied to **the dense retriever**", and lower-case in O1, O5, ¶1, ¶5. | **Lower-case "dense retriever" in prose everywhere.** Capitals only inside configuration labels ("Dense+CSQE", "BM25-expanded"), where they are table identifiers. One edit in ¶10. |
| **3** | Four names for "blind" | O8 "blind expansion components" · Q6 "blind **generation**" · ¶8 "blind **Query2Doc**" · ¶9 "blind-only expansion" · ¶11 "the **blind-QE** baseline". Five surface forms, three lists. | **"blind expansion"** for the concept; **"blind Query2Doc"** only when the specific baseline *run* is named. Retire "blind generation" (Q6 → "blind expansion") and "blind-QE baseline" (¶11 → "blind-expansion baseline (Aya Expanse~8B, BM25, $n=1$; 0.5046 NDCG@10)"). |
| **4** | Four nouns for the placement concept | O9 "**placement** … retriever-specific **application** strategies" · Q7 "to which retriever should the expansion **be applied**" · `chapter2.tex:473` "asymmetric **assignment**" · `chapter3.tex:473` "retriever--query **assignment**" · ¶10 "retriever-specific query **representation**" · ¶12 "**applied** asymmetrically". | **"placement"** as the reader-facing noun in all three lists (O9 already leads with it). Keep "**retriever-specific query representation principle**" in ¶10 *once*, as the name of the coined principle — that is a distinct object, not a synonym. Drop "assignment" from O9 and §3.8.3. |
| **5** | Model-name form inside Ch.5 alone | ¶3 and ¶6 "**Jais-2 8B**" (`chapter5.tex:18`, `:24`) vs ¶12 "**Jais-2-8B**" (`chapter5.tex:36`). Ch.2's heading is "Jais-2-8B" (`chapter2.tex:297`); Ch.4 tables use "Jais-2 8B". Same class as the open M14 (SILMA Kashif-2B vs SILMA 2B). | **"Jais-2-8B"** everywhere (matches the Ch.2 §2.4.1.2 heading and the developer's naming). Sweep with M14 in one pass. |
| **6** | **Numeric conflict, not terminology** | **SILMA 2B, BM25, no repetition:** `chapter4.tex:311` (Table 4.7) = **0.4277** (−7.4 %, arithmetically consistent with 0.4621) vs `chapter4.tex:462` (Table 4.11, *n*=1 column) = **0.4194** (which is what Table 4.12's Δ=+0.0639 is computed from). Both tables are internally consistent; they disagree with each other. No other model differs between the two tables. | **Resolve before submission.** Most likely two runs of the same configuration. If Table 4.11 is the later canonical sweep, change `chapter4.tex:311` to `0.4194 & 0.5550 & 0.4485 & $-$9.2\%` and re-check the Recall@10/MRR; if not, change `chapter4.tex:462` to 0.4277 and Table 4.12's Δ to +0.0555. **I cannot tell from the thesis which run is canonical — this needs the experiment logs.** Do not guess: whichever way it goes, one of the two tables must change, and the −7.4 % / +0.0639 derived figures move with it. |

**Not an inconsistency, flagged so it isn't "fixed" by mistake:** the `NDCG` / `nDCG` casing split (81 vs 46 occurrences) is already tracked as an open item under C3 and is **internally consistent within all three lists** (they all use `NDCG`); it only diverges in Ch.3/Ch.4 body text and captions. Leave it to the C3/E3 sweep.

---

## Summary of recommendations

| Item | Recommendation | Files touched (by the caller) |
|---|---|---|
| **J1** | Rephrase — announce the pipeline, not the finding | `chapter1.tex:18` (+ optional `chapter3.tex:486`) |
| **J2** | Do **not** reinstate "small"; instead de-"small" Ch.3 | `chapter3.tex:186`, `:265` |
| **J3** | **Split** — shortened accurate clause in ¶12 + new Challenges item 8 | `chapter5.tex:36`, `:58` (+ optional `:84`, `chapter2.tex:275`) |
| **J4** | Replace the false context-window reason; scope "zero-shot" to generation | `chapter3.tex:184` (+ optional `:452`) |
| **J5** | **Add CSQE** as a 4th item in the §2.1.4 expansion list | `chapter2.tex:91` (+ optional `:86`) |
| **J6** | 5 corrections to CLAUDE.md (2 blockers) | `CLAUDE.md` |
| **J7** | 5 terminology standardisations + 1 unresolved numeric conflict | `chapter1.tex:40`, `chapter2.tex:484`, `chapter5.tex:32`, `:34`, `:18`, `:24`; **`chapter4.tex:311`/`:462` needs a data decision** |
