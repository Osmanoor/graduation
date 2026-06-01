# Workstream 6 — Research / External Lookups Report

**Date:** 2026-05-30
**Scope:** Tasks 6.1–6.5 in `research_decisions/THESIS_NEXT_STEPS_TASKS.md` (Workstream 6 — "Research / external lookups").
**Method:** Each task checked against (a) the thesis LaTeX (`Chapters/chapter1.tex`, `chapter2.tex`, `References.bib`), (b) the project's prior literature-review docs in `research_decisions/`, and (c) the primary external source on the web (arXiv abstract pages, ACL Anthology, official model reports). Citation fields were verified by fetching the authoritative source page for each entry and comparing author/title/venue/URL.
**Status legend:** ✅ DONE / VERIFIED · ⚠️ NEEDS EDIT (claim or framing must be qualified/fixed) · ❌ WRONG (fabricated/broken; fix required) · 🔎 PARTIAL (in-repo or abstract-level evidence only).

> **Context from WS4:** The WS4 verification report (2026-05-30) already proved that at least two AI-generated BibTeX entries (`zhang_2024_mugi`, `lei_2024_csqe`) have **correct URLs but fabricated titles/authors**, and explicitly escalated Task 6.4 (full citation audit). This report confirms that the fabrication is **systematic across the AI-added 2024–2025 query-expansion citations**.

---

## Summary table

| # | Task | Verdict | One-line outcome |
|---|------|---------|------------------|
| 6.1 | Post-2024 small-LLM (<7B) Arabic QE papers | ⚠️ NEEDS EDIT | One concurrent paper (Macmillan-Scott et al., Nov 2025) uses **Gemma 3 4B** (<7B) for QE *including Arabic* — but **cross-lingual (CLIRMatrix/mMARCO), not monolingual MIRACL**. Gap survives only if **narrowed to monolingual MSA Arabic retrieval**. |
| 6.2 | Post-2024 asymmetric CSQE × hybrid | ⚠️ NEEDS EDIT | **Exp4Fuse (Liu et al., ACL 2025 Findings)** applies QE to a *single sparse retriever* and fuses original+expanded lists. This is the closest prior art and **must be cited**, but it is **sparse-only, not dense–sparse hybrid**, so the thesis's *retriever-type-asymmetry* claim is **partially novel** — downgrade to "not previously studied in a hybrid dense–sparse (and Arabic) setting." |
| 6.3 | Read or replace Song & Zheng 2024 | ✅ KEEP | Song & Zheng = "A Survey of Query Optimization in LLMs" (arXiv 2412.17558). Bib entry is **correct**; the four-operation taxonomy in §2.4 (expansion/decomposition/disambiguation/abstraction) **matches the source exactly**. Defensibly citable. Optionally supplement with the dedicated QE survey arXiv 2509.07794. |
| 6.4 | Full citation audit | ❌ MAJOR | **10 entries are wrong** (fabricated authors/titles and/or broken URLs), incl. the headline model `aya_2024` (**URL points to an unrelated MRI paper**) and `yoon_2025_llm_retrieval` (**thesis misrepresents a skeptical paper as supporting**). 8 spot-checked entries verified correct. 11 entries are orphaned (defined, never cited). |
| 6.5 | SOTA Arabic retrievers at submission | ⚠️ NEEDS EDIT | BGE-M3 / multilingual-E5-large are **still defensible** (and recommended by the cited Alsubhi 2025 Arabic-RAG paper), but **mE5-large is now dated**: Arabic-centric **Swan/ArabicMTEB (2024)** beats it on most Arabic tasks, and newer multilingual encoders (Arctic-Embed 2.0, Nomic-Embed-multilingual, Voyage-3) have appeared. Update Recommendation 3 to reflect this. |

**Bottom line.** The literature gap claims (6.1, 6.2) are **not invalidated but must be qualified** — concurrent 2025 work now touches both, so the thesis should narrow each claim and cite the new papers (this *strengthens* credibility rather than weakening the contribution). The single highest-impact result is **6.4**: the citation base has a systematic AI-fabrication problem affecting **every recent QE reference the §2.4 "modern QE" narrative rests on**, plus a broken URL for the best-performing model. These must be fixed before submission.

---

## Task 6.1 — Post-2024 small-LLM Arabic QE papers ⚠️ NEEDS EDIT

**Thesis claims under test:**
- §2.4 (`sec:modern_qe`, l.393): *"none of these studies tested models smaller than 7B for zero-shot query expansion on Arabic text."*
- §2.4 (`sec:research_gap`, l.414): QE studies "evaluate [neither] Arabic [n]or other morphologically rich languages."
- §1.2 (resource gap, l.23): "Whether small open-source models with 2–8 billion parameters … can generate useful Arabic query expansions remains an open question."

**Finding — one concurrent paper is a partial counter-example:**

> **Macmillan-Scott, Goworek & Özyiğit (2025), "Generative Query Expansion with Multilingual LLMs for Cross-Lingual Information Retrieval"** — arXiv:2511.19325 (24 Nov 2025).
> - Evaluates generative QE (Query2Doc / HyDE / MuGI / Exp4Fuse / CoT / Rephrase-and-Respond) across **8 languages including Arabic** on **CLIRMatrix** and **mMARCO**.
> - QE models: **Aya Expanse 8B, Gemma 3 4B, Gemma 3 12B** — i.e. it **does** use a sub-7B model (**Gemma 3 4B**) on Arabic, with **overlapping model choices** to this thesis.
> - Key results echo this thesis: zero-shot prompting best for short queries; CoT/RaR **meta-text pollutes BM25**; cross-lingual QE helps weakest-baseline languages most.

**Why the gap survives (with narrowing):**
1. **Task mismatch.** That paper studies **cross-lingual IR** (query and documents in *different* languages); this thesis studies **monolingual MSA Arabic retrieval on MIRACL**. The expansion step there is applied monolingually as one stage of a CLIR pipeline, but the *retrieval task and benchmark differ*.
2. **Concurrency.** It is dated **Nov 2025**, after this thesis's literature freeze and overlapping with the work — legitimate concurrent work, not prior art that pre-empts the contribution.
3. **No monolingual Arabic small-LLM QE on MIRACL exists** — the project's own earlier finding ("No paper tests modern 2–4B models for zero-shot Arabic QE", `llm_model_research.md`) still holds for the *specific* setting.

Other 2024–2025 hits (LLM-QE arXiv 2502.17057; the QE survey arXiv 2509.07794; MILL; MuGI) are **English/general**, not Arabic — they do not threaten the gap.

**Recommended edits (→ feeds 5.A.3 / 5.E.1 problem-statement reframe):**
- Reword l.393 to: *"no prior study has evaluated sub-7B models for zero-shot query expansion in **monolingual Arabic retrieval**; the closest concurrent work \cite{...2511.19325} applies sub-7B models (Gemma 3 4B) to **cross-lingual** Arabic IR."*
- Add the Macmillan-Scott citation to §2.4 and note the convergent findings (BM25 meta-text pollution, short-query/zero-shot preference) as **independent corroboration** of this thesis's results.
- Keep §1.2 resource-gap framing but bound it to "monolingual Arabic information retrieval."

---

## Task 6.2 — Post-2024 asymmetric CSQE × hybrid ⚠️ NEEDS EDIT

**Thesis claim under test** (§2.4, `sec:research_gap`, l.427):
> "the interaction between corpus-steered expansion and hybrid BM25–Dense fusion has not been studied: specifically, whether applying query expansion asymmetrically to only one retriever in a hybrid system can outperform applying it to both is an open question."

**Finding — closest prior art (must be cited):**

> **Liu et al. (2025), "Exp4Fuse: A Rank Fusion Framework for Enhanced Sparse Retrieval using LLM-based Query Expansion"** — ACL 2025 **Findings** (aclanthology 2025.findings-acl.9; arXiv:2506.04760).
> - Runs **two retrieval routes through the *same sparse retriever*** — one with the original query, one with a zero-shot LLM expansion — and fuses them with a **modified RRF**.
> - Finding: feeding the sparse retriever both the raw and expanded queries beats using the expanded query alone, and reaches SOTA on several benchmarks. Reported up to **+8.7** absolute (per `hybrid_retrieval_qe_literature_review.md`).

**Why the thesis claim is *partially* (not fully) novel:**
- Exp4Fuse is a **single-retriever (sparse-only) query-variant fusion**: fuse {sparse(q), sparse(q+expansion)}.
- The thesis's "asymmetric" finding is a **retriever-*type* asymmetry in a dense–sparse hybrid**: fuse {**BM25**(q+CSQE), **Dense**(q\_raw)} — expansion applied to *one retriever type* and the raw query to the *other*.
- These are **related but distinct**: Exp4Fuse never varies *which retriever* gets the expansion in a heterogeneous (dense+sparse) fusion; it independently validates the weaker sub-claim ("expansion helps the sparse side").

Supporting theory already in the repo: Chuang (2024 MIT thesis) and the dense-vs-sparse response analysis (`hybrid_retrieval_qe_literature_review.md`) explain *why* sparse benefits from and dense degrades on long expansions — consistent with the thesis's Config-A result.

**Recommended edits (→ §2.4 gap framing; supports Ch.4/Ch.5 discussion):**
- Cite **Exp4Fuse** in §2.4 and reframe: *"While Exp4Fuse \cite{...} shows that fusing original- and expanded-query lists from a **single sparse retriever** outperforms using the expansion alone, the **asymmetric assignment of expansion across retriever *types* in a dense–sparse hybrid** — and its behaviour for **Arabic** — has not been studied."*
- Downgrade "has not been studied" → "has not been studied **for Arabic, in a heterogeneous dense–sparse hybrid**." This keeps the novelty honest and is **stronger** because it now has a named, citable nearest neighbour.

---

## Task 6.3 — Read or replace Song & Zheng 2024 ✅ KEEP

> **Song, Mingyang & Zheng, Mao (2024), "A Survey of Query Optimization in Large Language Models"** — arXiv:2412.17558 (submitted 23 Dec 2024; last revised 3 Mar 2026).

- **Bib entry is correct.** Authors (Song, Mingyang / Zheng, Mao), title, URL, year all match the source. No fix needed for `song_2024_a`.
- **Taxonomy faithfully represented.** The survey defines exactly **four atomic operations: Query Expansion, Query Decomposition, Query Disambiguation, Query Abstraction.** The thesis (chapter2.tex l.90) states "expansion, decomposition, disambiguation, and abstraction" — an **exact match**. (Note: §5.A.4 of the task list paraphrases the families as "expansion, rewriting, decomposition, abstraction" — when writing that section, use the source's term **disambiguation**, not "rewriting.")
- The survey also adds a Query Complexity Taxonomy and a 5-phase Query Optimization Lifecycle — extra framing the thesis could draw on if §2.4 is expanded (5.A.4).

**Decision:** **KEEP and cite** — it is defensible. Item 2.14 (was it actually read?) is resolved: the taxonomy claim is accurate.
**Optional supplement:** the more QE-specific survey **"Query Expansion in the Age of Pre-trained and Large Language Models: A Comprehensive Survey"** (arXiv:2509.07794, 2025) could be added alongside it for the QE-techniques expansion (5.A.4) if a second, QE-focused survey citation is wanted.

---

## Task 6.4 — Full citation audit ❌ MAJOR (systematic fabrication)

**Coverage:** All 38 keys cited in the compiled thesis (`chapter1–5.tex` + abstracts) were enumerated; the **load-bearing QE / Arabic / model entries were verified against their authoritative source pages**. Famous foundational entries (HyDE, Query2Doc, DPR, RAG, Attention, BM25, MIRACL, Mamba, Pyserini, QLoRA, RRF) were field-inspected and look standard/correct but were not each web-fetched — a final line-by-line pass on those is recommended for completeness.

### 6.4a — Confirmed WRONG (fix before submission)

| Key | Problem | Correct data (verified) |
|-----|---------|-------------------------|
| `aya_2024` | ❌ **URL points to an unrelated MRI paper** (arXiv 2501.01482 = "An unsupervised method for MRI recovery"); title wrong; co-authors partly invented (Beeching not an author). **Highest priority — this is the thesis's best model.** | Title: **"Aya Expanse: Combining Research Breakthroughs for a New Multilingual Frontier"**; arXiv **2412.04261**; authors **Dang, Singh, D'souza, Ahmadian, et al.** (Cohere For AI). |
| `yoon_2025_llm_retrieval` | ❌ Title + authors fabricated **and finding misrepresented** — thesis cites it as showing "all LLMs improved retrieval, 8B≈GPT-4"; the real paper is **skeptical**, attributing apparent QE gains to **benchmark contamination ("knowledge leakage")**. | Title: **"Hypothetical Documents or Knowledge Leakage? Rethinking LLM-based Query Expansion"**; authors **Yejun Yoon, Jaeyoon Jung, Seunghyun Yoon, Kunwoo Park**; arXiv 2504.14175. |
| `zhang_2024_mugi` | ❌ Title + authors fabricated (WS4). MuGI = **Multi-Text Generation Integration**, not "Multi-Granularity." Thesis prose "Multi-Granularity Indexing" is also wrong. | Title: **"Exploring the Best Practices of Query Expansion with Large Language Models"**; authors **Le Zhang, Yihong Wu, Qian Yang, Jian-Yun Nie**; Findings EMNLP 2024 (2024.findings-emnlp.103; arXiv 2401.06311). |
| `lei_2024_csqe` | ❌ Authors fabricated (WS4); venue should be EACL 2024 (short). | Authors **Yibin Lei, Yu Cao, Tianyi Zhou, Tao Shen, Andrew Yates**; EACL 2024 Short (2024.eacl-short.34); arXiv 2402.18031. |
| `lei_2025_thinkqe` | ❌ Title + authors fabricated (same fake "Lei, Xiao" as CSQE). Thesis "Qwen-14B / chain-of-thought" model claim unverified. | Title: **"ThinkQE: Query Expansion via an Evolving Thinking Process"**; authors **Yibin Lei, Tao Shen, Andrew Yates**; Findings EMNLP 2025 (2025.findings-emnlp.965). |
| `yang_2025_aqe` | ❌ Title + authors fabricated. | Title: **"Aligned Query Expansion: Efficient Query Expansion for Information Retrieval through LLM Alignment"**; authors **Adam Yang, Gustavo Penha, Enrico Palumbo, Hugues Bouchard**; arXiv 2507.11042. |
| `zhang_2025_pbr` | ❌ Title + authors fabricated. Thesis "GPT-4o-mini (≈8B)" is a guess (params undisclosed); "10.5% Recall@5" vs source "up to 10% on PersonaBench"; it is **personalized/user-centric** QE, tangential to the small-model narrative. | Title: **"Personalize Before Retrieve: LLM-based Personalized Query Expansion for User-Centric Retrieval"**; authors **Yingyi Zhang, Pengyue Jia, Derong Xu, … Xiangyu Zhao** (12 authors); arXiv 2510.08935. |
| `xia_2025_kar` | ❌ Title + authors fabricated. Thesis "36 MRR points over HyDE" **unverified** (abstract does not mention HyDE/36 MRR); scope is textual *and relational/semi-structured* retrieval. | Title: **"Knowledge-Aware Query Expansion with Large Language Models for Textual and Relational Retrieval"**; authors **Yu Xia, Junda Wu, Sungchul Kim, Tong Yu, Ryan A. Rossi, Haoliang Wang, Julian McAuley**; NAACL 2025 Long (2025.naacl-long.216). |
| `young_2024_gaqr` | ⚠️ First author first name wrong (**Orion → Oliver**); rest OK. | **Oliver Young**, Yixing Fan, Ruqing Zhang, Jiafeng Guo, Maarten de Rijke, Xueqi Cheng; CIKM '24 (10.1145/3627673.3679930). |
| `louis_2024_query` | ❌ Author "Louis, Louis" invented; it is a **single-author master's thesis by Anish Bhusal** (UAH, 2024), not a paper. Thesis prose "Louis and Bhusal" is wrong → should be "Bhusal." Weak source (unrefereed thesis). | `@mastersthesis`, author **Anish Bhusal**, University of Alabama in Huntsville, 2024; https://louis.uah.edu/uah-theses/663/ |

### 6.4b — Spot-checked and VERIFIED correct

| Key | Status |
|-----|--------|
| `song_2024_a` | ✅ authors/title/url/year all correct (see 6.3). |
| `chan_2024_rqrag` | ✅ authors + title correct; "trains Llama2-7B" claim correct. |
| `elbeltagysamhaar_2024_exploring` | ✅ authors (El-Beltagy, Abdallah) + title correct. *(Thesis's "twelve embedding models, five LLMs" not confirmable from abstract — 🔎 verify against full PDF.)* |
| `alsubhi_2025_optimizing` | ✅ all 8 authors + title correct; **all thesis claims confirmed** (sentence-aware chunking; BGE-M3 & mE5-large best embeddings; Aya-8B > StableLM). |
| `mackie_2023_grf_dense` | ✅ authors + title correct; "≈10% / fusion best recall on 95%≈17 of 18" consistent with source. |
| `qwen3_2025` | ✅ arXiv 2505.09388 = "Qwen3 Technical Report". |
| `gemma3_2025` | ✅ arXiv 2503.19786 = "Gemma 3 Technical Report". |
| `falcon_h1_2025` | ✅ arXiv 2507.22448 = "Falcon-H1: A Family of Hybrid-Head Language Models…". |

### 6.4c — Orphaned entries (defined in `References.bib`, **never cited** in the compiled thesis)

11 keys are unused in `chapter1–5.tex` (several are cited only in `chapter2_generated.tex`, which is **not** `\include`d by `1-main.tex` — see note below):
`asai_2024_selfrag`, `chen_2024_dense`, `dong_2025_leveraging`, `guo_2024_lightrag`, `han_2024_retrievalaugmented`, `idanpogrebinsky_2025_enhancing`, `perin_2025_investigating`, `sarthi_2024_raptor`, `singhania_2024_recall`, `wang_2025_levelrag`, `zheng_2023_take`.
- **Action:** delete the unused entries, **or** cite them where relevant. Note `zheng_2023_take` ("Take a Step Back" — the canonical **abstraction** QE paper) is a natural citation for the abstraction family in the §2.4 expansion (5.A.4); consider using rather than deleting it.

### 6.4d — Build-file hazard
`Chapters/chapter2_generated.tex` exists alongside the compiled `chapter2.tex` and contains its own (overlapping) citations and a different intro. The `missing_references_review.md` audit was run against `chapter2_generated.tex` — i.e. **against the non-compiled file**. Ensure `chapter2_generated.tex` is not accidentally compiled and that citation reviews target `chapter2.tex`.

### 6.4e — Pattern & recommendation
The signature is unmistakable: **AI-added recent QE entries keep a correct arXiv/ACL URL but carry a plausible-sounding fabricated title and author list** (often the right first-author surname with a wrong first name + invented co-authors). Every recent QE citation in §2.4's "modern QE" paragraph is affected. Because some of these also **misstate the papers' findings** (`yoon` most seriously; `xia`, `zhang_pbr`, `lei_thinkqe` on specifics), this is not only a `.bib` cleanup — it intersects **WS3.1 (decorative-citation audit)** and **WS3.2 (fabricated-rationale audit)**: each affected sentence in §2.4 must be re-checked against the *real* paper, not just the bib fixed. Corrected BibTeX for all 10 entries is provided in the appendix below.

---

## Task 6.5 — SOTA Arabic retrievers at submission time ⚠️ NEEDS EDIT

**Thesis claim under test** (Recommendation 3, §5.3 / item P4.5.8): future work should use "stronger embedding models" naming **BGE-M3** and **multilingual-E5-large**.

**Findings (as of May 2026):**
- **BGE-M3 remains a strong, defensible open-source recommendation.** It leads/【is competitive on MIRACL (M3-dense ≈ 67.8 nDCG@10 across 18 langs vs mE5-large ≈ 65.4; combined heads ≈ 70.0) and is the open production standard for multilingual + long-doc retrieval. The thesis's own cited Arabic-RAG paper (**Alsubhi 2025**) independently concludes "**BGE-M3 and Multilingual-E5-large emerge as the most effective embedding models**" for Arabic — so the recommendation is grounded, not invented.
- **multilingual-E5-large is now dated.** Arabic-centric encoders released **after** the recommendation was written beat it on Arabic:
  - **Swan / ArabicMTEB** (Alwajih et al., 2024, arXiv:2411.01192): **Swan-Large surpasses multilingual-E5-large on most Arabic tasks**; ships with ArabicMTEB (8 tasks, 94 datasets, incl. retrieval).
  - **GATE** (2025, arXiv:2505.24581): Arabic embedding with Matryoshka representation — strong on Arabic **STS** (less retrieval-focused; weaker evidence for IR).
- **Newer multilingual options** worth naming: **Qwen3-Embedding-8B** (released **June 2025**; **#1 on the MTEB multilingual leaderboard, score 70.58**; 100+ languages; arXiv:2506.05176) — the strongest current *open-weight* multilingual retriever; **Arctic-Embed 2.0**, **Nomic-Embed-multilingual**, and commercial **Voyage-3-large** / **Cohere embed v3/v4**.

**Recommended edit (→ 5.D.3 Recommendation 3):**
- Keep **BGE-M3** as a primary recommendation (still SOTA-class, open, MIRACL-validated, and cited via Alsubhi 2025).
- **Replace bare "multilingual-E5-large"** with (a) **Qwen3-Embedding-8B** as the current open-weight multilingual leader, and (b) Arabic-centric **Swan-Large**, which now outperforms multilingual-E5-large on most Arabic tasks. Optionally name Arctic-Embed 2.0 / Nomic-Embed-multilingual.
- One caveat sentence: leaderboard scores are mostly **MTEB/MMTEB (and Arabic STS)**, not specifically **MIRACL Arabic retrieval**, so a small validation run is advisable before adopting (honest hedge).

---

## Cross-workstream consequences (what these outcomes unblock)

| WS6 result | Unblocks / changes |
|-----------|--------------------|
| 6.1 (Gemma-3-4B Arabic QE is cross-lingual, concurrent) | 5.A.3 / 5.E.1 problem-statement reframe; §2.4 l.393 wording; cite arXiv 2511.19325. |
| 6.2 (Exp4Fuse = nearest prior art, sparse-only) | §2.4 l.427 gap reframe; strengthens Ch.4/Ch.5 asymmetry discussion (5.C.13) with a citable neighbour. |
| 6.3 (Song & Zheng correct) | Closes item 2.14; informs §2.4 QE-techniques expansion (5.A.4) — use "disambiguation," not "rewriting." |
| 6.4 (10 bad entries incl. `aya_2024`, `yoon`) | **Blocks submission readiness.** Feeds WS3.1 (decorative-citation) + WS3.2 (fabricated-rationale) — each affected §2.4 sentence must be re-verified, not just the bib fixed. Confirms/extends WS4 §4.15. |
| 6.5 (mE5-large dated; Swan exists) | 5.D.3 Recommendation 3 update. |

---

## Reconciliation with the parallel WS6 report (Jules, 2026-05-22)

A second agent (Jules) produced an independent WS6 report. The two agree on 6.3 and on the *direction* of 6.1/6.2/6.5, but **diverge sharply on 6.4**. Settlement, with verification:

| Task | Agreement / divergence | Settled position |
|------|------------------------|------------------|
| 6.3 | **Full agreement.** Both: keep Song & Zheng; taxonomy (expansion/decomposition/disambiguation/abstraction) matches. | Confirmed — high confidence. |
| 6.1 | Jules cites Alsubhi 2025, El-Beltagy 2024, ALLaM 2025 as papers that narrow the gap. **But those are Arabic-RAG *component/model* papers (embeddings, generation, a base model) — none test small LLMs for *query expansion*.** They do not actually bear on the QE gap. Jules **missed** the one paper that does: **Macmillan-Scott et al. (arXiv 2511.19325)**, which uses Gemma-3-4B for Arabic QE (cross-lingual). | **My evidence is the correct basis.** Both agree the gap should be *reframed/narrowed* rather than dropped, but the narrowing must hinge on the **cross-lingual vs monolingual** distinction, not on the RAG-component papers. |
| 6.2 | Jules cites a **Medium blog (Niraj Kumar)** + **LevelRAG** for "retriever-specific" optimization and says the academic term is rare. I found **Exp4Fuse (ACL 2025 Findings, peer-reviewed)** — the actual nearest prior art. | **Cite Exp4Fuse, not a blog** (a Medium post is not a defensible thesis citation). Jules's "asymmetric avoids dense dilution" intuition is correct and matches this thesis's mechanism — but the *citable* anchor is Exp4Fuse. (`wang_2025_levelrag` is currently orphaned in the bib and is about multi-hop rewriting — weak fit; use only if genuinely relevant.) |
| 6.4 | **Direct contradiction.** Jules: "All URLs 100% resolve … integrity check passes … only 4 unused entries." Me: **10 entries have fabricated authors/titles and/or wrong URLs.** | **My finding stands; Jules's is wrong — and verifiable.** Root cause: Jules tested whether each URL *resolves to a valid repository*, **not** whether it points to the *correct paper* or whether *author/title fields match the source*. Proof: `aya_2024`'s URL (arXiv 2501.01482) resolves fine — to **"An unsupervised method for MRI recovery,"** not Aya Expanse. `yoon_2025`'s URL resolves — to a different-titled paper by different authors whose finding is the *opposite* of the thesis's characterization. **WS4 independently** found `zhang_2024_mugi` and `lei_2024_csqe` fabricated. A "does-the-link-open" check cannot catch fabricated metadata; field-level comparison (done here) does. |
| 6.4 (unused) | Jules: **4 unused** (`dong`, `singhania`, `zheng_take`, `idanpogrebinsky`). Me: **11 unused.** | **11 is correct** (verified by `grep` across all chapter files): Jules's 4 are a subset; the other 7 (`asai_2024_selfrag`, `chen_2024_dense`, `guo_2024_lightrag`, `han_2024_retrievalaugmented`, `sarthi_2024_raptor`, `perin_2025_investigating`, `wang_2025_levelrag`) are cited **0 times** in both the compiled chapters and `chapter2_generated.tex`. |
| 6.5 | Jules adds **Qwen3-Embedding-8B** (#1 MTEB multilingual, ~70.6) — which I had not named. I add **Swan/ArabicMTEB** (Arabic-centric) — which Jules did not name. | **Both belong.** Folded Qwen3-Embedding-8B into §6.5 above (correcting Jules's release date: **June 2025**, not "Jan 2026"). Qwen3-Embedding = best open-weight *multilingual*; Swan = best *Arabic-centric*. Recommend naming both. |

**Net:** Jules is a useful corroboration on 6.3 and contributes Qwen3-Embedding-8B for 6.5, but its **6.4 "clean bill of health" is incorrect and must not be relied on** — the citation base has a systematic fabrication problem (independently confirmed by WS4). Where the two reports conflict on substance, the field-level/web-fetched verification in this report is authoritative.

---

## Appendix — Corrected BibTeX for the 10 wrong entries

```bibtex
@misc{aya_2024,
  author = {Dang, John and Singh, Shivalika and D'souza, Daniel and Ahmadian, Arash and others},
  title = {Aya Expanse: Combining Research Breakthroughs for a New Multilingual Frontier},
  url = {https://arxiv.org/abs/2412.04261},
  year = {2024},
  organization = {arXiv.org}
}

@misc{yoon_2025_llm_retrieval,
  author = {Yoon, Yejun and Jung, Jaeyoon and Yoon, Seunghyun and Park, Kunwoo},
  title = {Hypothetical Documents or Knowledge Leakage? Rethinking {LLM}-based Query Expansion},
  url = {https://arxiv.org/abs/2504.14175},
  year = {2025},
  organization = {arXiv.org}
}

@inproceedings{zhang_2024_mugi,
  author = {Zhang, Le and Wu, Yihong and Yang, Qian and Nie, Jian-Yun},
  title = {Exploring the Best Practices of Query Expansion with Large Language Models},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2024},
  year = {2024},
  url = {https://aclanthology.org/2024.findings-emnlp.103}
}

@inproceedings{lei_2024_csqe,
  author = {Lei, Yibin and Cao, Yu and Zhou, Tianyi and Shen, Tao and Yates, Andrew},
  title = {Corpus-Steered Query Expansion with Large Language Models},
  booktitle = {Proceedings of the 18th Conference of the European Chapter of the ACL (EACL): Short Papers},
  year = {2024},
  url = {https://aclanthology.org/2024.eacl-short.34},
  note = {arXiv:2402.18031}
}

@inproceedings{lei_2025_thinkqe,
  author = {Lei, Yibin and Shen, Tao and Yates, Andrew},
  title = {{ThinkQE}: Query Expansion via an Evolving Thinking Process},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2025},
  year = {2025},
  url = {https://aclanthology.org/2025.findings-emnlp.965}
}

@misc{yang_2025_aqe,
  author = {Yang, Adam and Penha, Gustavo and Palumbo, Enrico and Bouchard, Hugues},
  title = {Aligned Query Expansion: Efficient Query Expansion for Information Retrieval through {LLM} Alignment},
  url = {https://arxiv.org/abs/2507.11042},
  year = {2025},
  organization = {arXiv.org}
}

@misc{zhang_2025_pbr,
  author = {Zhang, Yingyi and Jia, Pengyue and Xu, Derong and Wen, Yi and Li, Xianneng and Wang, Yichao and Zhang, Wenlin and Li, Xiaopeng and Gan, Weinan and Guo, Huifeng and Liu, Yong and Zhao, Xiangyu},
  title = {Personalize Before Retrieve: {LLM}-based Personalized Query Expansion for User-Centric Retrieval},
  url = {https://arxiv.org/abs/2510.08935},
  year = {2025},
  organization = {arXiv.org}
}

@inproceedings{xia_2025_kar,
  author = {Xia, Yu and Wu, Junda and Kim, Sungchul and Yu, Tong and Rossi, Ryan A. and Wang, Haoliang and McAuley, Julian},
  title = {Knowledge-Aware Query Expansion with Large Language Models for Textual and Relational Retrieval},
  booktitle = {Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the ACL (NAACL): Long Papers},
  year = {2025},
  url = {https://aclanthology.org/2025.naacl-long.216}
}

@inproceedings{young_2024_gaqr,
  author = {Young, Oliver and Fan, Yixing and Zhang, Ruqing and Guo, Jiafeng and de Rijke, Maarten and Cheng, Xueqi},
  title = {{GaQR}: An Efficient Generation-augmented Question Rewriter},
  booktitle = {Proceedings of the 33rd ACM International Conference on Information and Knowledge Management (CIKM '24)},
  pages = {4228--4232},
  year = {2024},
  doi = {10.1145/3627673.3679930}
}

@mastersthesis{louis_2024_query,
  author = {Bhusal, Anish},
  title = {Query augmentation for information retrieval (IR) using large language model (LLM)},
  school = {University of Alabama in Huntsville},
  year = {2024},
  url = {https://louis.uah.edu/uah-theses/663/}
}
```

> Author lists for `aya_2024` use `and others` to stay faithful while avoiding a 40-name list; expand if the citation style requires the full set. Verify the final author ordering against each source before committing.

## Artifacts / sources consulted
- Thesis: `Chapters/chapter1.tex`, `Chapters/chapter2.tex`, `References.bib`, `1-main.tex`, `missing_references_review.md`.
- Repo prior work: `hybrid_retrieval_qe_literature_review.md`, `llm_model_research.md`, `qe_techniques_comparison_research.md`, `WS4_VERIFICATION_REPORT.md`.
- External (web, May 2026): arXiv 2511.19325, 2412.17558, 2506.04760 (ACL 2025 Findings), 2504.14175, 2507.11042, 2510.08935, 2402.18031/2024.eacl-short.34, 2401.06311/2024.findings-emnlp.103, 2025.naacl-long.216, 2025.findings-emnlp.965, 2305.07477, 2412.04261, 2505.09388, 2503.19786, 2507.22448; CIKM'24 GaQR (10.1145/3627673.3679930); UAH thesis 663; ArabicMTEB/Swan (2411.01192), GATE (2505.24581); Alsubhi 2025 (2506.06339); El-Beltagy & Abdallah 2024 (2408.07425); QE survey (2509.07794).

**END.**
