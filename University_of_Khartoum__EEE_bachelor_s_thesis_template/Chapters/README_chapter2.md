# Chapter 2: Theoretical Background and Literature Review — Tracking Document

**Created:** 2026-03-27
**Last Updated:** 2026-03-27
**Status:** First complete draft
**File:** `Chapters/chapter2.tex`

---

## Final Outline

### Chapter Introduction (no section number)
Brief paragraph introducing the chapter scope and structure. No citations needed.

### 2.1 Theoretical Background
Foundational concepts the reader needs before understanding our methodology.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 2.1.1 Large Language Models and the Transformer Architecture | Self-attention, encoder-decoder vs decoder-only, pre-training, instruction tuning, parametric knowledge, hallucination problem | `papers/2020_RAG.md`, `papers/A Survey of Query Optimization in Large Language Models.md` |
| 2.1.2 Retrieval-Augmented Generation | Standard RAG architecture (retriever + generator), pipeline flow, why RAG addresses hallucination | `papers/2020_RAG.md`, `papers/2025_QE-RAG.md` |
| 2.1.3 Information Retrieval Methods | Three subsections: Sparse (BM25 concept), Dense (bi-encoder concept), Hybrid (combination) | `papers/2022_HyDE...md`, `papers/2023_Query2doc.md` |
| 2.1.4 Query Enhancement Techniques | Taxonomy: expansion, rewriting, hypothetical document generation. LLM-based generative enhancement overview (Query2Doc, HyDE concepts) | `papers/A Survey of Query Optimization in Large Language Models.md`, `papers/2023_Query2doc.md`, `papers/2022_HyDE...md` |
| 2.1.5 Arabic Language Processing Challenges | Morphological richness (root-pattern), diglossia (MSA vs dialects), orthographic variations, diacritics, impact on IR | `papers/2025_Optimizing RAG Pipelines for Arabic.md`, `papers/2024_Exploring Retrieval Augmented Generation in Arabic.md` |

### 2.2 Mathematical Models
Exact formulas with proper equation environments and labels.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 2.2.1 BM25 Scoring Function | Full formula: IDF component, TF saturation, document length normalization, parameters k1, b | Standard IR textbook formulas |
| 2.2.2 Dense Retrieval and Cosine Similarity | Bi-encoder architecture, embedding representation, cosine similarity formula, MIPS | `papers/2022_HyDE...md`, DPR paper |
| 2.2.3 Evaluation Metrics | Three sub-subsections: Recall@k, NDCG@k (with DCG, IDCG), MRR | Standard IR metric definitions |

### 2.3 Models Used in Experiments
ALL models described here so Chapter 3 only references by section number.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 2.3 intro paragraph | Selection criteria: Arabic support, size constraints (T4 GPU), open-source preference | `research_decisions/llm_model_research.md` |
| 2.3.1 Arabic-Specialized Models | | |
| — 2.3.1.1 Falcon-H1-Arabic-3B | TII, hybrid Mamba2-Transformer, 3.15B params, 128K context, OALL ~62% | `research_decisions/falcon_h1_research.md` |
| — 2.3.1.2 Jais-2-8B | MBZUAI/Inception/Cerebras, standard Transformer, 8.09B, custom 150K Arabic vocab, 2.6T training tokens | `research_decisions/jais_2_research.md` |
| — 2.3.1.3 ALLaM-7B | SDAIA, LlamaForCausalLM, 7B, 5.2T training tokens (540B Arabic), ICLR 2025, preview status | `research_decisions/allam_7b_research.md` |
| — 2.3.1.4 SILMA Kashif-2B | SILMA AI, 2B, Arabic RAG-specific, RAGQA 0.3575 | `research_decisions/llm_model_research.md` |
| 2.3.2 Multilingual Models | | |
| — 2.3.2.1 Qwen 2.5 3B | Alibaba, 3B, 29+ languages, 18T training tokens, Apache 2.0 | `research_decisions/llm_model_research.md` |
| — 2.3.2.2 Qwen 2.5 7B | Alibaba, 7B, same family, requires 4-bit on T4 | `research_decisions/llm_model_research.md`, `OSMAN_MODEL_COMPARISON_RESULTS.md` |
| — 2.3.2.3 Qwen3-4B | Alibaba, 4B, 119 languages, 36T training tokens, thinking mode | `research_decisions/qwen3_4b_research.md` |
| — 2.3.2.4 Qwen3-8B | Alibaba, 8B, same generation as Qwen3-4B | `OSMAN_MODEL_COMPARISON_RESULTS.md` |
| — 2.3.2.5 Gemma 3 4B-IT | Google DeepMind, 4B, 140+ languages, 128K context | `research_decisions/llm_model_research.md`, `OSMAN_MODEL_COMPARISON_RESULTS.md` |
| — 2.3.2.6 Aya Expanse 8B | Cohere Labs, 8B, 101 languages, Arabic explicitly optimized | `OSMAN_MODEL_COMPARISON_RESULTS.md` |
| 2.3.3 Experimental Models | | |
| — 2.3.3.1 GPT-OSS-20B | OpenAI, 20.9B total / 3.6B active, MoE (32 experts, top-4), English-dominant | `research_decisions/gpt_oss_20b_research.md` |
| 2.3.4 Retrieval Models | | |
| — 2.3.4.1 Multilingual DPR | Facebook AI, bi-encoder, BERT-based, pre-built MIRACL index | DPR paper, `RESEARCH_CONTEXT_KERNEL.md.md` |
| — 2.3.4.2 BM25S | Python-native BM25 implementation (2024), no Java dependency | `RESEARCH_CONTEXT_KERNEL.md.md` |
| Table 2.1 | Summary comparison: Model, Developer, Parameters, Architecture, Arabic Benchmark, License | All model research files |

### 2.4 Related Work
Thematically grouped, highlighting research gap.

| Subsection | Content | Source Files |
|------------|---------|-------------|
| 2.4.1 Foundational QE (2022–2023) | HyDE, Query2Doc, GRF, Rewrite-Retrieve-Read — all used 175B models | `papers/2022_HyDE...md`, `papers/2023_Query2doc.md`, `papers/2023_GRF.md`, `papers/2023_GRF_dense.md`, `papers/2023_Query Rewriting...md` |
| 2.4.2 Modern LLM-Based QE (2024–2025) | CSQE, MUGI, PBR, KAR, AQE, ThinkQE — prove 7-8B models sufficient; GaQR, RQ-RAG — knowledge distillation; QE-RAG — query noise robustness | `research_decisions/llm_model_research.md`, `papers/2024_GaQR.md`, `papers/2024_RQ-RAG...md`, `papers/2025_QE-RAG.md`, `papers/2024_Query augmentation...md` |
| 2.4.3 Arabic IR and RAG | MIRACL benchmark, Arabic RAG optimization, Aya-8B for Arabic generation | `papers/2025_Optimizing RAG Pipelines for Arabic.md`, `papers/2024_Exploring...md` |
| 2.4.4 Research Gap | No paper tests modern 2-4B models for zero-shot Arabic QE | Synthesis of all above |

### 2.5 Chapter Summary
Brief recap positioning our research within the identified gap.

---

## How to Update This Chapter

### Adding New Models (e.g., from expanded experiments Phase 4)
1. Add model description subsection under 2.3.1 (Arabic) or 2.3.2 (Multilingual)
2. Update Table 2.1 (model comparison summary)
3. Add BibTeX entry to `References.bib`
4. Update the intro paragraph of 2.3 if selection criteria changed
5. No changes needed in 2.1, 2.2, or 2.4 unless the model introduces a new concept

### Adding New Techniques (e.g., chunking-aware QE, HyDE, few-shot)
1. If concept is already in 2.1.4 (Query Enhancement Techniques): no change needed
2. If new concept (e.g., chunking-aware retrieval): add subsection to 2.1
3. Add relevant papers to 2.4 (Related Work)
4. Add BibTeX entries to `References.bib`

### Adding New Papers
1. Add paper summary to `papers/` folder
2. Add BibTeX entry to `References.bib`
3. Add citation in appropriate subsection of 2.4
4. If paper introduces new concepts, update 2.1 theoretical background

### Updating Results References
- Chapter 2 does NOT contain results — only model descriptions
- Results go in Chapter 4; methodology goes in Chapter 3
- If a model is dropped, keep it in 2.3 (Dr. Tahani: "even dropped models must be described")

---

## Cross-Reference Labels (for Chapters 3 and 4)

| Label | Section | Usage |
|-------|---------|-------|
| `chap:background` | Chapter 2 | "As discussed in Chapter~\ref{chap:background}" |
| `sec:theoretical` | 2.1 | General theoretical reference |
| `sec:llm_transformer` | 2.1.1 | LLM/Transformer concepts |
| `sec:rag` | 2.1.2 | RAG architecture |
| `sec:ir_methods` | 2.1.3 | IR methods overview |
| `sec:sparse_retrieval` | 2.1.3.1 | BM25 concept |
| `sec:dense_retrieval` | 2.1.3.2 | Dense retrieval concept |
| `sec:qe_techniques` | 2.1.4 | Query enhancement taxonomy |
| `sec:arabic_challenges` | 2.1.5 | Arabic NLP challenges |
| `sec:math_models` | 2.2 | Mathematical models section |
| `eq:bm25` | 2.2.1 | BM25 equation |
| `eq:cosine` | 2.2.2 | Cosine similarity equation |
| `eq:recall` | 2.2.3.1 | Recall@k equation |
| `eq:ndcg` | 2.2.3.2 | NDCG equation |
| `eq:mrr` | 2.2.3.3 | MRR equation |
| `sec:models_used` | 2.3 | Models section |
| `sec:falcon_h1` | 2.3.1.1 | Falcon-H1 |
| `sec:jais2` | 2.3.1.2 | Jais-2 |
| `sec:allam` | 2.3.1.3 | ALLaM |
| `sec:silma` | 2.3.1.4 | SILMA |
| `sec:qwen25_3b` | 2.3.2.1 | Qwen 2.5 3B |
| `sec:qwen25_7b` | 2.3.2.2 | Qwen 2.5 7B |
| `sec:qwen3_4b` | 2.3.2.3 | Qwen3-4B |
| `sec:qwen3_8b` | 2.3.2.4 | Qwen3-8B |
| `sec:gemma3` | 2.3.2.5 | Gemma 3 4B |
| `sec:aya` | 2.3.2.6 | Aya Expanse 8B |
| `sec:gptoss` | 2.3.3.1 | GPT-OSS-20B |
| `sec:mdpr` | 2.3.4.1 | mDPR |
| `sec:bm25s` | 2.3.4.2 | BM25S |
| `tab:model_comparison` | 2.3 | Model comparison table |
| `eq:rrf_ch2` | 2.1.3.3 | RRF equation (hybrid retrieval) |
| `eq:hybrid_cc_ch2` | 2.1.3.3 | Convex Combination equation (hybrid retrieval) |
| `sec:related_work` | 2.4 | Related work section |
| `sec:research_gap` | 2.4.4 | Research gap |

---

## Formatting Rules
- **Passive voice** throughout ("The model was trained..." not "We trained...")
- **Abbreviations**: Full form (ABBR) on first use, then ABBR only
- **IEEE references**: Numbered by order of appearance, `[1]` before full stop
- **Figures**: Figure 2.X, caption below, `\label{fig:xxx}`
- **Tables**: Table 2.X, caption ABOVE, `\label{tab:xxx}`
- **Dr. Tahani's rule**: Chapter 3 must NOT re-explain any concept from Chapter 2
