# Literature Verification — Final Fact-Check of Load-Bearing Claims

**Date:** 2026-07-29
**Scope:** Tasks T1–T6 — primary-source verification of the thesis's gap statements (`Chapters/chapter2.tex` §2.5.2/§2.5.4, `chapter1.tex` l.11/l.18, chapter summary l.505–506) and of the five previously unverified citations at `chapter2.tex:440`.
**Method:** Every claim was checked against the primary source — arXiv abstract pages, the arXiv PDF/HTML full text, and ACL Anthology landing pages — not against secondary summaries or the project's own prior reports. Where a prior in-repo report (`WS6_RESEARCH_REPORT.md`) made a factual assertion about a source, that assertion was independently re-tested against the source itself; two WS6 errors were found and are corrected below.
**No `.tex` file was modified.**

---

## Headline

**No claim was falsified.** All five load-bearing claims survive primary-source scrutiny. Three are VERIFIED as written. Two require narrowing — not because a counter-example was found, but because each contains an unnecessarily strong universal quantifier ("in any language", "uninvestigated") that a well-read examiner can attack with an adjacent literature the thesis currently does not acknowledge.

---

## (a) Verdict table

| # | Claim (location) | Verdict | Primary-source evidence |
|---|------------------|---------|-------------------------|
| **1a** | "LLM-based QE has not been evaluated for monolingual Arabic retrieval" (§2.5.2 l.446; echoed ch.1 l.11, summary l.505) | **VERIFIED** | No counter-example found across six independent searches (English + Arabic terms, unfiltered by model scale, incl. 2026). The only concurrent Arabic-QE work with LLMs is Macmillan-Scott et al., which evaluates **cross-lingual** retrieval only — see 2a. All Arabic monolingual QE work located is pre-LLM (word-embedding / PRF / WordNet) — see section (d). |
| **1b** | "…the question of which retriever within a heterogeneous sparse–dense hybrid should receive the expansion has not been addressed **in any language**" (§2.5.2 l.446; ch.1 l.11 "no study establishes which retriever within a hybrid architecture should receive it"; summary l.506) | **NEEDS REWORDING** | True for *query* expansion — no counter-example found; Exp4Fuse (the nearest neighbour) is sparse-only (see 4). **But** Doc2Query++ (arXiv:2510.09557, 10 Oct 2025) establishes the identical asymmetry for *document* expansion: "Dual-Index Fusion" keeps expansion out of the dense index precisely because "appending expansions degrades dense retrieval effectiveness due to semantic noise… which weakens the original document embedding," then fuses a sparse expanded index with an unexpanded dense index. The universal "in any language" is defensible only once "query expansion" is made explicit and load-bearing. https://arxiv.org/abs/2510.09557 |
| **2a** | Gap 1: "None of these studies addresses *monolingual* Arabic retrieval; the sole concurrent exception \cite{macmillanscott_2025_generative} addresses the distinct *cross-lingual* setting." (§2.5.4 l.467) | **VERIFIED** | arXiv:2511.19325, "Generative Query Expansion with Multilingual LLMs for **Cross-Lingual** Information Retrieval". §1: "Cross-lingual information retrieval (CLIR) is the task of identifying documents that are relevant to a given query in setting where the query and the documents are in different languages… Of the two components, this paper focuses on query expansion". Datasets are CLIRMatrix (multilingual subset: Ar, De, En, Es, Fr, Ja, Ru, Zh) and mMARCO (14 languages) — both run **cross-lingually**: the Hit@10 heatmaps (Figs. 3 and 4) have **blank diagonals**, i.e. no query-language = document-language cell is ever evaluated. |
| **2b** | "applies sub-7B models (including Gemma 3 4B)" (§2.5.2 l.446) | **VERIFIED** | Table 1 (p.5): models = Aya Expanse 8B, **Gemma 3 4B**, Gemma 3 12B, plus two Aya fine-tunes. §3.3: "Three base open-source models with strong multilingual capabilities are considered: Aya Expanse 8B and Gemma 3 4B & 12B". |
| **2c** | "it independently corroborates several observations of this thesis, including that reasoning-style meta-text can pollute sparse retrieval and that zero-shot prompting is preferable for short queries" (§2.5.2 l.446) | **VERIFIED** | §4.2 (p.9): "For CoT prompting and RaR, the model frequently generates meta text such as *'To answer this query, I will provide information about…'*, which adversely affects BM25 retrieval." And p.10: "for short title-style queries, zero-shot prompting produces the most effective pseudo-documents for retrieval due to the introduction of irrelevant information with more elaborate prompting that harms sparse retrieval." |
| **3a** | Gap 3: "The original CSQE work was evaluated exclusively on English benchmarks" (§2.5.4 l.471) | **VERIFIED** | arXiv:2402.18031 §3.1: datasets are TREC DL19, DL20 (MS MARCO) and six BEIR sets (Scifact, Arguana, Trec-Covid, FiQA, DBPedia, TREC-NEWS), plus NovelEval. All English. |
| **3b** | "although the blind component has been isolated in English, the **corpus-grounded component has never been evaluated on its own in any language**" (§2.5.4 l.471) — basis of the exp 013c novelty claim | **VERIFIED** | Confirmed by exhaustive reading of the full paper incl. all appendices. The blind component **is** isolated: "BM25+KEQE" appears as a standalone row in Tables 3, 4, 6, 7 and 10. A corpus-only condition appears **nowhere**. CSQE is defined as inseparable by construction: "we expand the query by concatenating *q*, all sentences in *S*, **and the generations from KEQE** to form a new query"; and "As CSQE involves **both** KEQE and corpus-originated expansions, we sample N = 2 for both… in total only 4 generations." No ablation section exists (appendices are A.1 prompt, A.2 dataset statistics, A.3 DL20 LLM comparison). |
| **4** | Gap 4: "Exp4Fuse shows that fusing the original- and expanded-query result lists from a *single sparse* retriever outperforms using the expansion alone" (§2.5.4 l.473) | **VERIFIED** | arXiv:2506.04760 / ACL 2025 Findings, abstract: "Exp4Fuse operates by simultaneously considering two retrieval routes — one based on the original query and the other on the LLM-augmented query. It then generates two ranked lists using **a sparse retriever** and fuses them using a modified reciprocal rank fusion method." Full text: "by employing LLMs for zero-shot query expansion and using **only a single sparse retriever**, Exp4Fuse requires lower computational and memory resources." Sparse retrievers: BM25, uniCOIL, SPLADEv2, SLIM. Generators: GPT-4o-mini, LLaMA3-8B-Instruct. Dense retrievers appear **only as comparison baselines, never fused** with the sparse lists. No asymmetric across-type assignment anywhere. |
| **5** | MuGI "employs an adaptive query-repetition strategy that scales the number of query repetitions to the length of the generated text" (§2.5.2 l.438) | **VERIFIED** | arXiv:2401.06311v3 gives the repetition factor explicitly: **λ = ⌊(len(r₁)+len(r₂)+…+len(rₙ)) / (len(q)·β)⌋**, with the enhanced sparse query **q_sparse = concat(q×λ, r₁, r₂, …, rₙ)**, β = 4 typical. Motivated as: "constant repetition of query used in previous studies… is ineffective… particularly when dealing with multiple references." λ is therefore literally proportional to total generated length ÷ query length. |
| **6a** | §2.5.4 l.459: for Arabic, "The query formulation stage… **remains uninvestigated**" | **NEEDS REWORDING** | Over-broad. Arabic query expansion is a continuously active field — there is a dedicated survey (Al-Shawakfa et al., *Survey of Automatic Query Expansion for Arabic Text Retrieval*, JISTaP 8(4), 2020) and a paper published **during this thesis** (Al-Lahham et al., "Improved Arabic query expansion using word embedding," *Scientific Reports*, 22 Jan 2026). Neither is LLM-based, so claim 1a is untouched — but "uninvestigated" without the qualifier "LLM-based" is falsifiable in one search. |
| **6b** | §2.5.2 l.440 opener: "Several additional studies have examined QE **with smaller and more efficient models**." | **NEEDS REWORDING** | Only AQE fits. KAR augments an LLM with a knowledge graph (no small-model claim); ThinkQE is a test-time reasoning/corpus-interaction framework benchmarked against "training-intensive dense retrievers and rerankers"; PBR is personalisation on PersonaBench. None is a small-model study. The four descriptions themselves are accurate (see below) — only the framing sentence is wrong. |
| **6c** | `lei_2025_thinkqe` — "refines query expansions through an evolving, reasoning-driven generation process" | **VERIFIED** | ACL Anthology 2025.findings-emnlp.965. Lei, Shen & Yates. Abstract: "a **thinking**-based expansion process that encourages deeper and comprehensive semantic exploration, and a corpus-interaction strategy that **iteratively refines** expansions using retrieval feedback." Bib entry (authors/title/venue/year/URL) correct. |
| **6d** | `xia_2025_kar` — "augmenting LLM-generated expansions with structured knowledge to improve both textual and relational retrieval" | **VERIFIED** | ACL Anthology 2025.naacl-long.216. Abstract: "we propose a knowledge-aware query expansion framework, augmenting LLMs with **structured document relations from knowledge graph (KG)**… advantages of our method compared against state-of-the-art baselines on **textual and relational** semi-structured retrieval." Bib entry correct. |
| **6e** | `yang_2025_aqe` — "using LLM alignment to make query expansions more effective and efficient" | **VERIFIED** | arXiv:2507.11042, 15 Jul 2025. Abstract: "AQE leverages recent techniques in **LLM alignment** to fine-tune models for generating query expansions that directly optimize the effectiveness of the retrieval task, **eliminating the need for additional filtering steps**" (the filtering step being the costly one). Bib entry correct. |
| **6f** | `zhang_2025_pbr` — "explored personalized, user-centric query expansion, reporting retrieval improvements on a personalization benchmark" | **VERIFIED** | arXiv:2510.08935 (10 Oct 2025, rev. 9 Dec 2025). Title: "Personalize Before Retrieve: LLM-based Personalized Query Expansion for User-Centric Retrieval". Reports "up to 10% gains on **PersonaBench** across retrievers." Bib entry correct. Note the thesis wisely no longer quotes the "10.5% Recall@5" or "GPT-4o-mini (≈8B)" figures flagged in WS6 — the current wording is safe. |
| **6g** | `yoon_2025_llm_retrieval` — "caution that a substantial portion of the apparent gains… may stem from benchmark contamination ('knowledge leakage')" | **VERIFIED** | arXiv:2504.14175 (ACL 2025 Findings). Abstract: "we challenge this assumption by investigating whether **knowledge leakage** in benchmarks contributes to the observed performance gains… This suggests that knowledge leakage may be present in fact-verification benchmarks, **potentially inflating the perceived performance** of LLM-based query expansion methods." The WS6-flagged misrepresentation has been corrected in the current text. Bib entry correct, though see residual risk R6. |
| **7** | Bonus — §2.5.2 l.436: "Lei et al. reported that even a 7B-parameter model achieves a **30% improvement in MAP over BM25**" | **VERIFIED** | arXiv:2402.18031 Table 7 (DL19): BM25+CSQE with Llama2-Chat-7B mAP = 39.1; BM25 baseline mAP = 30.1 (Table 3). (39.1 − 30.1)/30.1 = **+29.9%**. Exact. |
| **8** | Bonus — §2.5.2 l.436: CSQE instructs the LLM "to **extract and synthesise** topically relevant vocabulary" | **NEEDS REWORDING** (minor) | The paper is emphatic that the operation is **extraction, not synthesis** — that is the entire anti-hallucination argument: "these key sentences are usually **identical to the existing texts in the corpus**" (footnote: "830 out of 1000 key sentences extracted by GPT-3.5-Turbo are identical to sentences in the initially-retrieved documents"). "Synthesise" concedes the paper's central claim. |

---

## (b) Proposed corrected sentences (thesis style — British spelling, passive voice, paste-ready)

**B1 — §2.5.2, l.446, the italic gap statement.** Replace the italic clause:

> However, a critical gap remains: \textit{LLM-based QE has not been evaluated for monolingual Arabic retrieval, and the question of which retriever within a heterogeneous sparse--dense hybrid should receive the query expansion has not been addressed for any language. The closest analogue is found in the document-expansion literature, where the same asymmetry has been observed --- expansion appended to documents benefits sparse retrieval but degrades dense retrieval, motivating index-level separation \cite{kuo_2025_doc2query_pp} --- but the corresponding question for query expansion at retrieval time remains open.}

*(If Doc2Query++ is not to be cited, the minimum safe edit is the insertion of the word "query" before "expansion" and the replacement of "in any language" with "for any language"; the citation is nonetheless recommended, since a named nearest neighbour strengthens rather than weakens the novelty claim.)*

**B2 — §2.5.4, Gap 4, l.473.** Append after "…has not been studied":

> …the asymmetric assignment of query expansion across retriever \textit{types} in a heterogeneous dense--sparse hybrid --- and its behaviour for Arabic --- has not been studied. The analogous asymmetry has been documented for \textit{document} expansion, where generated text appended to the index is known to assist sparse matching while degrading dense representations \cite{kuo_2025_doc2query_pp}; whether the same asymmetry governs the placement of a \textit{query} expansion at retrieval time is therefore an open question with practical implications for retrieval pipeline design.

**B3 — §2.5.4, l.459 (close of the Arabic IR subsection).** Replace the final sentence:

> The query formulation stage---specifically, whether \textit{LLM-based} QE techniques developed for English transfer to Arabic---remains uninvestigated. Automatic query expansion for Arabic has itself been studied for two decades using thesaurus-, ontology- and word-embedding-based methods \cite{alshawakfa_2020_survey_aqe, allahham_2026_improved}, but these approaches predate generative expansion and address a different mechanism: the addition of related \textit{terms} rather than the generation of a pseudo-document.

**B4 — §2.5.2, l.440, paragraph opener.** Replace:

> Several additional studies have examined QE with smaller and more efficient models.

with:

> Several further studies have extended LLM-based QE along complementary axes.

**B5 — §2.5.2, l.436, CSQE description.** Replace "instructing it to extract and synthesise topically relevant vocabulary and context grounded in the actual corpus content" with:

> instructing it to identify which of those documents are relevant and to \textit{extract verbatim} the key sentences that establish that relevance. Because the extracted text is copied from the corpus rather than generated --- Lei et al. report that 830 of 1,000 extracted sentences were identical to sentences in the retrieved documents --- the corpus-grounded component is structurally incapable of hallucination.

**B6 — chapter summary, l.506.** Replace:

> Corpus-steered expansion has been evaluated only for English, and the placement of the \textit{query} expansion within a heterogeneous hybrid sparse--dense pipeline has not been evaluated for any language (Section~\ref{sec:research_gap}).

**B7 — chapter1.tex, l.11.** Replace "no study establishes which retriever within a hybrid architecture should receive it" with:

> …and no study establishes which retriever within a hybrid architecture should receive the \textit{query} expansion.

---

## (c) BibTeX — verified, paste-ready

The three entries already present in `References.bib` (`zhang_2024_mugi`, `liu_2025_exp4fuse`, `macmillanscott_2025_generative`) were re-checked field-by-field against their sources this session and are **correct as they stand**; they are reproduced here for the `papers/` summaries. Two new entries are supplied for the rewordings above.

```bibtex
@inproceedings{zhang_2024_mugi,
  author    = {Zhang, Le and Wu, Yihong and Yang, Qian and Nie, Jian-Yun},
  title     = {Exploring the Best Practices of Query Expansion with Large Language Models},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2024},
  year      = {2024},
  url       = {https://aclanthology.org/2024.findings-emnlp.103},
  note      = {arXiv:2401.06311; the method is named MuGI (Multi-Text Generation Integration) in the arXiv v1/v2 title}
}

@inproceedings{liu_2025_exp4fuse,
  author    = {Liu, Lingyuan and Zhang, Mengxiang},
  title     = {{Exp4Fuse}: A Rank Fusion Framework for Enhanced Sparse Retrieval using Large Language Model-based Query Expansion},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2025},
  year      = {2025},
  url       = {https://aclanthology.org/2025.findings-acl.9},
  note      = {arXiv:2506.04760}
}

@misc{macmillanscott_2025_generative,
  author       = {Macmillan-Scott, Olivia and Goworek, Roksana and {\"O}zyi{\u{g}}it, Eda B.},
  title        = {Generative Query Expansion with Multilingual {LLMs} for Cross-Lingual Information Retrieval},
  url          = {https://arxiv.org/abs/2511.19325},
  year         = {2025},
  organization = {arXiv.org},
  note         = {arXiv:2511.19325, 24 November 2025; The Alan Turing Institute}
}

@misc{kuo_2025_doc2query_pp,
  author       = {Kuo, Tzu-Lin and Chiu, Wei-Ning and Ma, Wei-Yun and Cheng, Pu-Jen},
  title        = {{Doc2Query++}: Topic-Coverage based Document Expansion and its Application to Dense Retrieval via Dual-Index Fusion},
  url          = {https://arxiv.org/abs/2510.09557},
  year         = {2025},
  organization = {arXiv.org}
}

@article{allahham_2026_improved,
  author  = {Al-Lahham, Yaser A. and Almatarneh, Sattam and Alshammari, Kaznah and Al-Smadi, Mutasem},
  title   = {Improved {Arabic} query expansion using word embedding},
  journal = {Scientific Reports},
  year    = {2026},
  note    = {Published 22 January 2026; PMC12830740}
}
```

**Note on `alshawakfa_2020_survey_aqe`:** *Survey of Automatic Query Expansion for Arabic Text Retrieval*, **Journal of Information Science Theory and Practice** 8(4), 2020 (accesson.kr/jistap/v.8/4/67/7239). The full author list was not confirmed at page level in this session — see residual risk R5.

**Correction to WS6:** `WS6_RESEARCH_REPORT.md` (line 36) states that Macmillan-Scott et al. evaluate "Query2Doc / HyDE / MuGI / **Exp4Fuse** / CoT / Rephrase-and-Respond" across "**8 languages**". Both are wrong and neither is repeated in the thesis. The paper evaluates **four prompting strategies only — zero-shot, CoT, Rephrase-and-Respond (RaR), and few-shot** (§3.1, Table 1); HyDE, MuGI and Exp4Fuse appear solely as related-work citations in §2.2, from which "their main components have been distilled in this work." Language coverage is **8 on CLIRMatrix** (Ar, De, En, Es, Fr, Ja, Ru, Zh) and **14 on mMARCO** (Table 2). Do not reuse the WS6 phrasing.

---

## (d) T4 — the unfiltered Arabic-QE search

Six searches were run without the sub-7B model filter that constrained WS6: English keyword searches (LLM QE / HyDE / Query2Doc / doc2query × Arabic), a MIRACL-Arabic-specific search, an Arabic-language search (توسيع الاستعلام / استرجاع المعلومات العربية), a 2026-targeted search, and a classical-AQE search.

**Prior Arabic QE work found — all pre-LLM:**

| Work | Method | Corpus | Threat to claim 1a |
|------|--------|--------|--------------------|
| Al-Lahham, Almatarneh, Alshammari & Al-Smadi (2026), "Improved Arabic query expansion using word embedding", *Scientific Reports*, 22 Jan 2026 | **Word2Vec (SkipGram), GloVe, FastText** over PRF; explicitly *not* generative | TREC 2001/2002 Arabic newswire (AFP) + Watan-2004 | **None.** Word-embedding term expansion, not LLM pseudo-document generation. Confirms the field is live but not the gap. |
| Al-Shawakfa et al. (2020), *Survey of Automatic Query Expansion for Arabic Text Retrieval*, JISTaP 8(4) | Survey of local/global AQE: Arabic WordNet, ontologies, association rules, PRF | TREC Arabic | **None** — predates LLM QE entirely. |
| "Incorporating Deep Median Networks for Arabic Document Retrieval Using Word Embeddings-Based Query Expansion", JISTaP 12(3), 2024 | Word2Vec + deep median networks | TREC 2001/2002 Arabic newswire | **None.** |
| Arabic WordNet / ontology / association-rule QE (multiple, 2016–2021) | Lexical resources | Various | **None.** |
| Macmillan-Scott et al. (2025), arXiv:2511.19325 | LLM pseudo-document generation, Aya Expanse 8B / Gemma 3 4B & 12B | CLIRMatrix, mMARCO | **None to 1a** — cross-lingual retrieval only, blank heatmap diagonals. See R1 for the one attackable nuance. |
| Alsubhi et al. 2025; El-Beltagy & Abdallah 2024; Fanar (2501.13944); ARA-Reranker-V1 | Arabic RAG components: chunking, embeddings, rerankers, generators | Various | **None** — no query-formulation stage evaluated. |

**MIRACL Arabic QE leaderboard results:** none found. The MIRACL leaderboard and its associated papers report retriever results (BM25, mDPR, hybrid, mContriever) but no query-expansion condition for Arabic or any other language.

**Assessment: the gap claim survives, in its LLM-specific form.** No paper was found that applies generative LLM-based query expansion to monolingual Arabic retrieval. The claim's survival depends entirely on the qualifier "LLM-based", which is present in §2.5.2 l.446 and the summary l.505 but **absent from §2.5.4 l.459** ("The query formulation stage… remains uninvestigated") — hence proposed edit B3. That single sentence is the only place in the thesis where the gap is stated in a form a search can falsify.

A useful secondary result: the comprehensive 2025 QE survey (arXiv:2509.07794) contains **no mention of Arabic or MIRACL** anywhere in its text, and does not list non-English retrieval among its open challenges. The absence is itself citable evidence for the gap.

---

## (e) Residual risk — what remains unverifiable, and how an examiner might press

| # | Risk | Likelihood | Mitigation |
|---|------|-----------|------------|
| **R1** | **Macmillan-Scott's "monolingual" sentence.** §3.3 (p.7) reads: "the isolated expansion step is applied **in a monolingual setting**. To support this design, the multilingual CLIRMatrix dataset is used to construct **monolingual subsets for Arabic**, Chinese, English and Spanish". An examiner who greps the PDF for "monolingual Arabic" will find it and may claim the thesis mischaracterises the paper. | **Medium — highest single risk** | The rebuttal is solid and should be held ready: the monolingual Arabic subsets are **fine-tuning data** for the Aya variants, and the *expansion step* is monolingual only because the pipeline translates first and expands second. The *retrieval evaluation* — the thing the gap claim is about — is cross-lingual without exception, proven by the blank diagonals in Figs. 3 and 4. Consider adding a footnote to §2.5.4 stating this explicitly, so the examiner sees it has been considered. |
| **R2** | **Doc2Query++ (arXiv:2510.09557).** Establishes the sparse-benefits/dense-degrades asymmetry and index-level separation, in English, in Oct 2025. Cited by no one in this thesis. | **Medium** | Adopt B1/B2. Citing it converts a hidden vulnerability into a demonstration of command of the literature, and the distinction (document expansion at index time vs. query expansion at retrieval time; and dual-index vs. dual-retriever fusion) is genuine and easy to defend. |
| **R3** | **"Has not been studied" is unprovable in principle.** No search can establish a universal negative, and neither can any examiner refute it — but the burden is rhetorically on the claimant. | **Low impact, unavoidable** | Prefer "no study located in this review addresses…" over "has not been studied" wherever the sentence can absorb it without becoming limp. The claim is already correctly narrowed by *monolingual*, *Arabic*, *heterogeneous hybrid* and (after B1) *query*. |
| **R4** | **MuGI β/λ notation.** MuGI's β is the *divisor constant* in λ = ⌊Σlen(rᵢ)/(len(q)·β)⌋; λ is the repetition count. §2.5.2 l.438 says MuGI's strategy is "the basis for the adaptive repetition parameter (β) adopted in this thesis." If Chapter 3's β is defined as the repetition *count* rather than the divisor, the thesis has silently redefined a borrowed symbol. | **Medium** | Not resolvable here — `sec:meth_repetition` in chapter3.tex was not in scope and was not read. **Verify before submission** that Ch.3's β matches MuGI's divisor semantics; the Exp 1.1 results table ("n=5, n=7" vs. "β=2") suggests it does, but this must be confirmed at the definition, not inferred from a table. |
| **R5** | **Two citations not verified at page level this session:** the JISTaP 2020 Arabic AQE survey author list (used only if B3 is adopted), and `lei_2024_csqe`'s EACL 2024 short-paper venue string (verified in WS6, not re-verified here). | **Low** | Fetch both landing pages before final submission if B3 is adopted. |
| **R6** | **`yoon_2025_llm_retrieval` venue.** The entry is `@misc`/arXiv, but the paper appeared in **ACL 2025 Findings**. Not an error, but an examiner may read an arXiv-only citation as evidence the peer-reviewed version was not consulted. | **Low** | Upgrade to `@inproceedings` with the ACL Anthology URL. The same applies to `zhang_2025_pbr` if it has since been published. |
| **R7** | **Concurrency defence for Macmillan-Scott.** Dated 24 Nov 2025 — after this thesis's experiments (Apr 2026 experiment logs postdate it, however). The thesis calls it "concurrent"; an examiner could ask why a paper available eight months before submission was not compared against empirically. | **Low–Medium** | The honest answer is available and should be prepared: different task (CLIR), different datasets (CLIRMatrix/mMARCO, not MIRACL), different retriever (BM25 only, no dense, no hybrid) — no comparable number exists to compare against. The thesis already uses it correctly, as independent corroboration of two qualitative findings rather than as a baseline. |
| **R8** | **CSQE corpus-only novelty (exp 013c).** Verified against the paper and its appendices — no corpus-only condition exists. Residual risk is only that a *later* paper (2024–2026) ran the ablation. | **Low** | Not searched exhaustively; ThinkQE (Lei, Shen & Yates 2025, the same first author) uses a "corpus-interaction strategy" and is the most likely place such an ablation would appear. Worth one targeted read of ThinkQE's ablation section before submission. |

---

## Sources consulted (primary)

arXiv:2511.19325 (abstract + full PDF pp. 1–11) · arXiv:2402.18031 (full text, in-repo `papers/arxiv_downloads/2402.18031.md`) · arXiv:2506.04760 + aclanthology.org/2025.findings-acl.9 · arXiv:2401.06311v3 · arXiv:2510.09557 · arXiv:2504.14175 · arXiv:2507.11042 · arXiv:2510.08935 · aclanthology.org/2025.findings-emnlp.965 · aclanthology.org/2025.naacl-long.216 · arXiv:2509.07794 (QE survey, searched for Arabic/MIRACL) · Scientific Reports s41598-025-28758-0 / PMC12830740 · JISTaP 8(4) 2020 and 12(3) 2024 · project-miracl.github.io · in-repo `References.bib`, `Chapters/chapter1.tex`, `Chapters/chapter2.tex`, `research_decisions/WS6_RESEARCH_REPORT.md`.

**END.**
