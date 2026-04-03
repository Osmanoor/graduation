# Phase 4 Literature Review: Knowledge-Base-Aware & Chunking-Aware Query Enhancement

**Date:** 2026-03-28
**Status:** Research Complete -- Ready for Direction Selection
**Task:** 6.1 (Literature review for expanded experiments)
**Searcher:** Claude Code (web search across arXiv, ACL Anthology, Semantic Scholar, venues)

---

## Executive Summary

This document maps **all identified research directions** for extending the existing Query2Doc pipeline with knowledge-base-aware or structure-aware capabilities. The "mufti analogy" (knowing WHERE to search, not just WHAT to search) finds strong support in the literature across multiple sub-directions.

**Key finding:** There are two broad families of approaches:
1. **Query-side approaches** (modify the query using corpus/structure knowledge) -- directly extends Query2Doc
2. **Document-side approaches** (modify how documents are indexed/represented) -- complementary but requires re-indexing

For your pipeline, **query-side approaches are the most feasible** since they build directly on Query2Doc without requiring corpus re-indexing.

---

## Table of Contents

1. [Direction A: Corpus-Steered Query Expansion](#direction-a)
2. [Direction B: Contextual Retrieval (Document-Side)](#direction-b)
3. [Direction C: Structure-Aware Document Retrieval](#direction-c)
4. [Direction D: Hierarchical Retrieval](#direction-d)
5. [Direction E: Knowledge Graph + Retrieval](#direction-e)
6. [Direction F: Proposition-Level Retrieval](#direction-f)
7. [Direction G: Metadata-Aware Retrieval & Query Expansion](#direction-g)
8. [Direction H: Query2Doc Extensions & Alignment](#direction-h)
9. [Direction I: Term-Level Corpus Enrichment](#direction-i)
10. [Direction X: "Rebarter"](#direction-x)
11. [Feasibility Matrix](#feasibility-matrix)
12. [Recommended Directions for Phase 4](#recommendations)

---

<a name="direction-a"></a>
## Direction A: Corpus-Steered Query Expansion (CSQE)

### Core Idea
Instead of letting the LLM generate expansions purely from parametric knowledge (which may hallucinate or be misaligned with the corpus), **ground the expansion in actual corpus documents** retrieved in a first pass.

### Paper A1: Corpus-Steered Query Expansion with Large Language Models
- **Authors:** Yibin Lei, Yu Cao, Tianyi Zhou, Tao Shen, Andrew Yates
- **Year/Venue:** 2024, EACL (Short Papers)
- **arXiv:** 2402.18031
- **Code:** https://github.com/Yibin-Lei/CSQE

**What they did:** CSQE uses LLMs to identify pivotal sentences in initially-retrieved documents (pseudo-relevance feedback), then combines these corpus-originated texts with LLM-generated expansions to create a grounded query expansion. Unlike pure LLM expansion (like Query2Doc), CSQE addresses hallucination and corpus misalignment by anchoring expansions in real documents from the target corpus.

**Key result:** Strong zero-shot performance without any training. Especially effective for queries where LLMs lack domain knowledge -- the corpus provides the missing context.

**Connection to Query2Doc:** This is the most direct extension of Query2Doc. Instead of generating a blind pseudo-document, you first retrieve documents, then use the LLM to identify the most relevant sentences from those documents and combine them with LLM-generated content. It transforms Query2Doc from "blind generation" to "corpus-grounded generation."

**Feasibility for Colab:** HIGH. No training needed. Uses same LLM you already have. Adds one retrieval step before expansion. Could use BM25 for the first-pass retrieval (already implemented).

---

### Paper A2: Knowledge-Aware Query Expansion with Large Language Models (KAR)
- **Authors:** Sahel Sharifymoghaddam et al.
- **Year/Venue:** 2024/2025, NAACL 2025
- **arXiv:** 2410.13765

**What they did:** Proposed Knowledge-Aware Retrieval (KAR) which augments LLMs with structured document relations from a knowledge graph. Uses document texts as KG node representations, applies document-based relation filtering to extract query-focused relations, then feeds both textual and relational knowledge to the LLM to generate grounded query expansions.

**Key result:** Improved Hit@1 and MRR on STaRK benchmark (AMAZON, MAG, PRIME datasets). The KG relations help the LLM generate structurally relevant expansions, not just semantically similar ones.

**Connection to Query2Doc:** Extends the "what context to give the LLM" question. Instead of giving the LLM nothing (standard Query2Doc), you give it structured relations from a KG. For MIRACL/Wikipedia, you could use Wikipedia's category structure and article links as a lightweight KG.

**Feasibility for Colab:** MEDIUM. KG construction is the bottleneck. Wikipedia link structure could serve as a ready-made KG, but processing 2.1M passages for relations is heavy. Could prototype on a subset.

---

<a name="direction-b"></a>
## Direction B: Contextual Retrieval (Document-Side Context Enrichment)

### Core Idea
The problem: when you chunk a document, individual chunks lose context (e.g., "The company grew by 3%" -- which company?). Solution: prepend contextual information to each chunk before embedding.

### Paper B1: Contextual Retrieval (Anthropic)
- **Authors:** Anthropic (blog post, not peer-reviewed paper)
- **Year:** September 2024
- **URL:** https://www.anthropic.com/news/contextual-retrieval

**What they did:** For every chunk in a corpus, use an LLM to generate a short contextual snippet that situates the chunk within its parent document. Prepend this snippet to the chunk before embedding ("Contextual Embeddings") and before BM25 indexing ("Contextual BM25"). Combined with reranking, this reduces top-20 retrieval failure rate by up to 67%.

**Key result:** Contextual embeddings alone reduced retrieval failure by 35% (5.7% to 3.7%). Combined with BM25 and reranking: up to 67% reduction. Cost: $1.02 per million document tokens (using prompt caching).

**Connection to Query2Doc:** This is a DOCUMENT-SIDE approach -- it modifies how chunks are stored, not how queries are expanded. However, it addresses the SAME problem as query expansion (bridging the query-document gap) from the other side. Could be combined with Query2Doc for maximum effect.

**Feasibility for Colab:** LOW-MEDIUM. Requires re-processing and re-embedding all 2.1M MIRACL passages. Expensive LLM calls for each chunk. However, the concept of "what context does a chunk need?" informs query-side approaches. A query-side adaptation would be: instead of prepending context to chunks, include structural context in the query expansion prompt.

---

### Paper B2: Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models
- **Authors:** Michael Gunther, Isabelle Mohr, Bo Wang, Han Xiao (Jina AI)
- **Year/Venue:** 2024, arXiv:2409.04701 (accepted at ICLR 2025 Workshop)
- **Code:** https://github.com/jina-ai/late-chunking

**What they did:** Instead of chunking first then embedding (which loses context), they embed the entire document at the token level first, then segment the resulting token embeddings into chunks and mean-pool each chunk. This preserves cross-chunk contextual information without any additional LLM calls.

**Key result:** Significant improvement on retrieval tasks. Works without additional training. Available in Jina Embeddings v3 API.

**Connection to Query2Doc:** Document-side approach. Requires long-context embedding models. Conceptually interesting but not directly applicable to query enhancement.

**Feasibility for Colab:** LOW. Requires re-embedding entire corpus with a long-context model. Not compatible with existing mDPR embeddings.

---

### Paper B3: Contextual Document Embeddings
- **Authors:** John X. Morris, Alexander M. Rush (Cornell)
- **Year/Venue:** 2025, ICLR 2025
- **arXiv:** 2410.02525

**What they did:** Proposed that document embeddings should consider neighboring documents (not just the document itself), analogous to how word embeddings are contextualized. Two methods: (1) contrastive learning with document neighbors, (2) architecture that explicitly encodes neighbor information.

**Key result:** State-of-the-art on MTEB benchmark without hard negative mining or score distillation. Especially strong in out-of-domain settings.

**Connection to Query2Doc:** Document-side. But the principle (context from neighbors improves representation) could inspire a query-side variant: when expanding a query, consider what cluster of documents it might belong to and include cluster-level context.

**Feasibility for Colab:** LOW. Requires retraining embedding model with neighbor-aware objectives.

---

### Paper B4: Context is Gold to find the Gold Passage
- **Authors:** Emmanuel Monet et al. (ILLUIN Technology)
- **Year/Venue:** 2025, EMNLP 2025
- **arXiv:** 2505.24782
- **Code:** https://github.com/illuin-tech/contextual-embeddings

**What they did:** Introduced ConTEB (Context-aware Text Embedding Benchmark) to evaluate whether models can leverage document-wide context. Proposed InSeNT (In-sequence Negative Training), a contrastive post-training approach combined with late chunking that enhances contextual representation while preserving efficiency.

**Key result:** Chunks embedded with this method are more robust to suboptimal chunking strategies and larger corpus sizes. All artifacts open-sourced.

**Connection to Query2Doc:** Document-side. Demonstrates that context-awareness consistently improves retrieval quality. Validates the "mufti analogy" from the document side.

**Feasibility for Colab:** LOW-MEDIUM. Requires post-training an embedding model. Open-source code available.

---

### Paper B5: Reconstructing Context: Evaluating Advanced Chunking Strategies for RAG
- **Authors:** Carlo Merola, Jaspinder Singh
- **Year:** April 2025
- **arXiv:** 2504.19754

**What they did:** Rigorous comparative analysis of late chunking vs. contextual retrieval (Anthropic-style). Evaluated both effectiveness and efficiency in optimizing RAG systems.

**Key result:** Contextual retrieval preserves semantic coherence more effectively but requires greater computational resources. Late chunking offers higher efficiency but sacrifices some relevance and completeness. There is a clear trade-off between quality and cost.

**Connection to Query2Doc:** Useful for understanding the landscape. Confirms that context enrichment helps, but document-side approaches are costly.

**Feasibility for Colab:** N/A (evaluation study, not a new method).

---

<a name="direction-c"></a>
## Direction C: Structure-Aware Document Retrieval

### Core Idea
Use the inherent structure of documents (headings, sections, HTML tags, article boundaries) to improve retrieval.

### Paper C1: DAPR: A Benchmark on Document-Aware Passage Retrieval
- **Authors:** Kexin Wang, Nils Reimers, Iryna Gurevych (UKP Lab, TU Darmstadt)
- **Year/Venue:** 2024, ACL 2024 (Main Conference)
- **arXiv:** 2305.13915
- **Code:** https://github.com/UKPLab/acl2024-dapr

**What they did:** Created a benchmark specifically for passages that require document context to be correctly retrieved. Found that 53.5% of passage retriever errors are due to missing document context. Tested contextualized passage representations (prepending document titles, keyphrases) and hybrid retrieval.

**Key result:** Prepending document titles improved hard queries (that require document context) significantly. However, hybrid retrieval completely fails on these hard queries. This proves that structure-awareness is essential for a significant fraction of queries.

**Connection to Query2Doc:** CRITICAL paper. It quantifies exactly how much context loss hurts retrieval. For MIRACL (Wikipedia-based), every passage has a parent article with title, section headings, and categories. A Query2Doc extension could: (1) include article title/section heading information in the expansion prompt, or (2) generate expansions that explicitly reference the structural context (e.g., "This question is about [topic] in the context of [broader article]").

**Feasibility for Colab:** HIGH. The insights are directly applicable. You don't need to run DAPR -- you need to use its finding (prepend document context) in your query expansion pipeline.

---

### Paper C2: SEAL: Structure and Element Aware Learning
- **Authors:** Xinhao Huang, Zhibo Ren, Yipeng Yu, Ying Zhou, Zulong Chen, Zeyi Wen
- **Year/Venue:** 2025, EMNLP 2025 (Main Conference)
- **arXiv:** 2508.20778
- **Code:** https://github.com/xinhaoH/SEAL

**What they did:** Two components: (1) Structure-Aware Learning (SAL) -- trains model to understand document hierarchy by contrasting HTML-tagged vs. plain text versions of documents, (2) Element-Aware Alignment (EAL) -- masks random HTML elements to force fine-grained understanding. Released StructDocRetrieval dataset.

**Key result:** Boosted NDCG@10 from 73.96% to 77.84% on BGE-M3. Consistent improvements across multiple PLMs.

**Connection to Query2Doc:** Document-side (requires model fine-tuning). But the insight is important: structural elements (headings, section markers) carry significant retrieval signal. This can inform query-side approaches.

**Feasibility for Colab:** LOW. Requires fine-tuning embedding models on structured document data.

---

### Paper C3: MultiDocFusion: Hierarchical and Multimodal Chunking Pipeline
- **Authors:** Joongmin Shin, Chanjun Park, Jeongbae Park, Jaehyung Seo, Heuiseok Lim
- **Year/Venue:** 2025, EMNLP 2025
- **ACL Anthology:** 2025.emnlp-main.1062

**What they did:** Integrated vision-based document parsing, OCR, LLM-based document section hierarchical parsing (DSHP-LLM), and DFS-based hierarchical chunk construction for industrial documents.

**Key result:** Improved retrieval precision by 8-15% and QA scores by 2-3% vs. baselines. Demonstrates the critical role of explicitly leveraging document hierarchy.

**Connection to Query2Doc:** Document-side pipeline. Not directly applicable to query enhancement but validates the importance of hierarchical structure awareness.

**Feasibility for Colab:** LOW. Complex multi-stage pipeline designed for industrial documents.

---

### Paper C4: MoDora: Tree-Based Semi-Structured Document Analysis System
- **Authors:** weAIDB Lab
- **Year/Venue:** 2025/2026, Accepted at SIGMOD 2026
- **arXiv:** 2602.23061
- **Code:** https://github.com/weAIDB/MoDora

**What they did:** Designed Component-Correlation Tree (CCTree) to hierarchically organize document components. Models inter-component relations and layout distinctions through bottom-up cascade summarization. Includes question-type-aware retrieval.

**Key result:** Best performance on hierarchy-based questions. Demonstrates CCTree's effectiveness in capturing document structure.

**Connection to Query2Doc:** The CCTree concept is interesting -- for Wikipedia, you could build a lightweight tree (Article > Section > Subsection > Passage) and use it to inform query expansion.

**Feasibility for Colab:** MEDIUM. The tree concept is simpler than the full system. Could build a lightweight version for Wikipedia articles.

---

### Paper C5: Heading-Aware Chunking and Hierarchical Document Structure Integration
- **Authors:** Pham Doan Tinh et al.
- **Year:** August 2025
- **ResearchGate preprint**

**What they did:** Optimized context retrieval for RAG by using heading-aware chunking that preserves document structure, integrating heading hierarchy into chunk representations.

**Key result:** A consistent 3-level heading hierarchy strikes optimal balance between semantic granularity and retrieval efficiency.

**Connection to Query2Doc:** Directly relevant to MIRACL -- Wikipedia articles have clear heading structure. Query expansion could incorporate heading context.

**Feasibility for Colab:** HIGH concept. The heading information is readily available in Wikipedia/MIRACL data.

---

<a name="direction-d"></a>
## Direction D: Hierarchical Retrieval (Multi-Level)

### Core Idea
Don't retrieve at a single level (passage). Instead, retrieve hierarchically: first identify relevant documents/sections, then drill down to passages.

### Paper D1: RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
- **Authors:** Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, Christopher D. Manning (Stanford)
- **Year/Venue:** 2024, ICLR 2024
- **arXiv:** 2401.18059
- **Code:** https://github.com/parthsarthi03/raptor

**What they did:** Recursively clusters text chunks based on vector embeddings, generates LLM summaries of each cluster, then builds a tree from bottom-up. At inference, retrieves from multiple levels of the tree, integrating information across different levels of abstraction.

**Key result:** 20% absolute accuracy improvement on QuALITY benchmark (complex multi-step reasoning). Significant improvements over traditional retrieval-augmented LMs.

**Connection to Query2Doc:** RAPTOR's insight: different queries need different abstraction levels. A short, ambiguous query might benefit from high-level summaries. A specific factual query needs passage-level detail. For Query2Doc, you could condition the expansion on the estimated abstraction level needed.

**Feasibility for Colab:** MEDIUM. Building the tree requires LLM calls for summarization of clusters. For 2.1M MIRACL passages, this is expensive. Could prototype on a subset or use Wikipedia's existing article structure as a proxy for the tree.

---

### Paper D2: LevelRAG: Multi-hop Logic Planning over Rewriting Augmented Searchers
- **Authors:** Zhuocheng Zhang, Yang Feng, Min Zhang (ICT, CAS)
- **Year:** February 2025
- **arXiv:** 2502.18139
- **Code:** https://github.com/ictnlp/LevelRAG

**What they did:** Two-stage hierarchical framework: (1) High-level searcher decomposes complex queries into atomic sub-queries, (2) Multiple low-level searchers optimize each sub-query for specific retrievers (dense, sparse, Lucene). Each low-level searcher rewrites queries to match its retriever's strengths.

**Key result:** Outperforms all counterparts on single-hop QA and shows superior multi-hop QA performance.

**Connection to Query2Doc:** The "rewriting augmented searcher" concept directly extends Query2Doc. Instead of one expansion for all retrievers, generate retriever-specific expansions. You already test Dense and BM25 separately -- you could create Dense-optimized and BM25-optimized expansions.

**Feasibility for Colab:** MEDIUM-HIGH. The core idea (retriever-specific query rewriting) is implementable. The full multi-hop decomposition is more complex.

---

### Paper D3: Hierarchical Retrieval with Evidence Curation for Open-Domain QA
- **Year/Venue:** 2025, ACL Findings 2025

**What they did:** Multi-stage retrieval where the first stage retrieves at the document level, then drills down to extract specific evidence passages. Evidence is curated and organized before being sent to the LLM.

**Connection to Query2Doc:** The "drill down" approach could be adapted: use Query2Doc to identify the right document neighborhood, then do fine-grained passage retrieval.

**Feasibility for Colab:** MEDIUM.

---

<a name="direction-e"></a>
## Direction E: Knowledge Graph + Retrieval

### Core Idea
Use knowledge graph structure (entity relationships, community structure) to guide retrieval or query expansion.

### Paper E1: KG2RAG: Knowledge Graph-Guided Retrieval Augmented Generation
- **Authors:** Xiangrong Zhu et al. (NJU Websoft)
- **Year/Venue:** 2025, NAACL 2025
- **arXiv:** 2502.06864
- **Code:** https://github.com/nju-websoft/KG2RAG

**What they did:** Uses KGs to provide fact-level relationships between chunks. After semantic retrieval provides seed chunks, KG2RAG expands to related chunks via graph traversal (KG-guided chunk expansion) and organizes retrieved chunks into coherent paragraphs (KG-based chunk organization).

**Key result:** Advantages over existing RAG approaches on HotpotQA in both response quality and retrieval quality.

**Connection to Query2Doc:** The "seed retrieval + KG expansion" pattern maps well to Query2Doc. Step 1: Generate pseudo-document with Query2Doc. Step 2: Use initial retrieval results to find related chunks via Wikipedia's link structure (proxy KG). Step 3: Use related chunks to inform a better second-pass expansion.

**Feasibility for Colab:** MEDIUM. Wikipedia link structure is available. Building a full KG from 2.1M passages is heavy, but using Wikipedia's existing graph (article links, categories) as a proxy is feasible.

---

### Paper E2: HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs
- **Authors:** Bernal Jimenez Gutierrez et al. (OSU NLP Group)
- **Year/Venue:** 2024, NeurIPS 2024
- **arXiv:** 2405.14831
- **Code:** https://github.com/OSU-NLP-Group/HippoRAG

**What they did:** Inspired by hippocampal indexing theory: uses LLMs as the "neocortex" (general knowledge), knowledge graphs as the "hippocampus" (indexing), and Personalized PageRank as the "pattern completion" process. Builds a KG from passages, then uses PageRank to find relevant information.

**Key result:** Outperforms SOTA on multi-hop QA by up to 20%. 10-30x cheaper and 6-13x faster than iterative retrieval methods like IRCoT.

**Connection to Query2Doc:** The Personalized PageRank idea is powerful. For MIRACL, you could use Wikipedia's existing article link graph and apply PageRank starting from entities mentioned in the query to find relevant topical neighborhoods. This neighborhood information could then be fed to the LLM for query expansion.

**Feasibility for Colab:** MEDIUM. KG construction from passages is expensive. However, using Wikipedia's existing article graph would bypass this. The PageRank computation itself is lightweight.

---

### Paper E3: GraphRAG: From Local to Global
- **Authors:** Darren Edge et al. (Microsoft Research)
- **Year/Venue:** 2024, arXiv:2404.16130
- **Code:** https://github.com/microsoft/graphrag

**What they did:** Builds entity knowledge graph from source documents, generates community summaries for groups of closely-related entities, then uses these summaries for retrieval. Supports Local Search (entity-specific), Global Search (holistic), and DRIFT Search.

**Key result:** Substantial improvements for global sensemaking questions. 72-83% comprehensiveness and 62-82% diversity improvements. Up to 97% fewer tokens for root-level summaries.

**Connection to Query2Doc:** Community summaries provide pre-built context about document neighborhoods. For MIRACL, Wikipedia categories could serve as "communities," and category-level summaries could provide context for query expansion.

**Feasibility for Colab:** LOW-MEDIUM. Full GraphRAG pipeline is heavy. The community summary concept could be adapted using Wikipedia categories.

---

<a name="direction-f"></a>
## Direction F: Proposition-Level / Fine-Grained Retrieval

### Core Idea
Instead of retrieving at the passage level, decompose passages into atomic propositions (single facts) and retrieve at that granularity.

### Paper F1: Dense X Retrieval: What Retrieval Granularity Should We Use?
- **Authors:** Tong Chen, Hongwei Wang, Sihao Chen, Wenhao Yu, Kaixin Ma, Xinran Zhao, Hongming Zhang, Dong Yu
- **Year/Venue:** 2024, EMNLP 2024 (Main Conference)
- **arXiv:** 2312.06648
- **Code:** https://github.com/chentong0/factoid-wiki

**What they did:** Introduced "propositions" as a retrieval unit -- atomic expressions that each encapsulate a distinct factoid in self-contained natural language. Built FACTOIDWIKI by decomposing all of English Wikipedia into propositions using a fine-tuned Flan-T5 "Propositionizer."

**Key result:** +10.1 Recall@20 improvement with unsupervised dense retrievers, +2.7 with supervised retrievers. Retrieved propositions are more condensed with question-relevant information, reducing noise.

**Connection to Query2Doc:** Two possible connections: (1) Use the Propositionizer to decompose Query2Doc's pseudo-documents into atomic facts before expansion, ensuring each expansion term maps to a specific factoid. (2) More ambitiously, decompose MIRACL passages into propositions and index at that level. But this is document-side and requires re-indexing.

**Feasibility for Colab:** MEDIUM for query-side application (decompose pseudo-docs). LOW for document-side (re-index 2.1M passages as propositions). The Propositionizer model (Flan-T5-large) runs on T4.

---

<a name="direction-g"></a>
## Direction G: Metadata-Aware Retrieval & Query Expansion

### Core Idea
Use document metadata (titles, dates, categories, sources) to improve retrieval -- either by filtering, enriching embeddings, or guiding query expansion.

### Paper G1: Multi-Meta-RAG: Database Filtering with LLM-Extracted Metadata
- **Authors:** Maxim Poliakov et al.
- **Year/Venue:** 2024, arXiv:2406.13213, Published in Springer LNCS
- **Code:** https://github.com/mxpoliakov/Multi-Meta-RAG

**What they did:** Uses a helper LLM to extract metadata (source, date, permissions) from the query, then filters the vector database using this metadata before performing similarity search. Specifically designed for multi-hop questions that require evidence from multiple sources.

**Key result:** 17.2% increase in Hits@4 for voyage-02; GPT-4 accuracy improved from 0.56 to 0.606 (25.6% baseline improvement for Google PaLM).

**Connection to Query2Doc:** For MIRACL, queries often implicitly target specific Wikipedia article categories or topics. An LLM could extract topic/category metadata from the query, then either (1) filter passages before retrieval, or (2) include category information in the query expansion to better target relevant passages.

**Feasibility for Colab:** HIGH. Uses LLM you already have. Wikipedia categories are available via MediaWiki API (already identified in error analysis research). Simple metadata extraction + filtering pipeline.

---

### Paper G2: Metadata-Driven Retrieval-Augmented Generation for Financial QA
- **Authors:** Dadopoulos, Ladas et al.
- **Year:** October 2025
- **arXiv:** 2510.24402

**What they did:** Multi-stage architecture using LLM-generated metadata for financial documents. Key finding: embedding chunk metadata directly with text ("contextual chunks") provides the most significant performance gains, more than pre-retrieval filtering or post-retrieval reranking alone.

**Key result:** Contextual chunks (metadata embedded with text) > Reranking > Pre-retrieval filtering. The combination of all three is optimal.

**Connection to Query2Doc:** The finding that metadata-enriched embeddings outperform filtering is important. For MIRACL, this suggests that including Wikipedia article title + section heading in the passage text (before embedding) would improve retrieval. On the query side, including topic/category metadata in query expansion could similarly help.

**Feasibility for Colab:** HIGH for query-side adaptation. LOW for re-embedding passages with metadata.

---

### Paper G3: Utilizing Metadata for Better Retrieval-Augmented Generation
- **Authors:** Raquib Bin Yousuf, Shengzhe Xu, Mandar Sharma et al. (Virginia Tech)
- **Year/Venue:** January 2026, ECIR 2026
- **arXiv:** 2601.11863

**What they did:** Systematic study comparing metadata-aware retrieval strategies: metadata-as-text (prefix/suffix), dual-encoder unified embedding, late-fusion retrieval, and metadata-aware query reformulation. Tested on structured, repetitive corpora (regulatory filings).

**Key result:** Unified embeddings (fusing metadata and content in single index) emerged as the most effective and practical approach. Metadata-aware query reformulation also helps but is more complex.

**Connection to Query2Doc:** The "metadata-aware query reformulation" variant is directly applicable. Instead of expanding the query blindly, include known metadata about likely target documents. For MIRACL, this means including Wikipedia article/section context in the expansion prompt.

**Feasibility for Colab:** HIGH for query reformulation approach. LOW for re-indexing approaches.

---

### Paper G4: BMQExpander: Ontology-Guided Query Expansion for Biomedical Document Retrieval
- **Authors:** Not specified in search results
- **Year:** August 2025
- **arXiv:** 2508.11784

**What they did:** Combines UMLS Metathesaurus (medical ontology) with LLMs. Represents relevant concept hierarchies as a pruned semantic graph, serializes it, and prompts the LLM with the graph to generate medically grounded pseudo-documents. Key innovation: the ontology constrains LLM output, reducing hallucinations.

**Key result:** Up to 22.1% NDCG@10 improvement over sparse baselines, up to 6.5% over strongest baseline. Up to 15.7% improvement under query perturbation. Fewer hallucinations than other LLM-based QE.

**Connection to Query2Doc:** This is the CLOSEST match to the "mufti analogy." The ontology serves as the "mufti's knowledge of which book to look in." For Arabic/MIRACL, Wikipedia categories + article link structure could serve as a lightweight ontology. You would serialize relevant category/link context and include it in the Query2Doc prompt.

**Feasibility for Colab:** HIGH. The core idea (serialize structural context, feed to LLM) is simple. Wikipedia categories are readily available. The key challenge is building/serializing the relevant subgraph for each query.

---

<a name="direction-h"></a>
## Direction H: Query2Doc Extensions & Alignment

### Core Idea
Direct improvements to the Query2Doc paradigm: better generation, better alignment with retrievers, multi-query strategies.

### Paper H1: RFG Framework: Retrieval-Feedback-Grounded Multi-Query Expansion
- **Year/Venue:** 2025, SCITEPRESS
- **URL:** https://www.scitepress.org/Papers/2025/138369/138369.pdf

**What they did:** Instead of generating a single pseudo-document (like Query2Doc), generates multiple diverse queries grounded in retrieval feedback. Uses a three-stage process: (1) generate diverse queries, (2) retrieve documents for each, (3) rank fusion and final selection.

**Key result:** Consistently outperforms HyDE and Query2Doc. Benefits both weak and strong retrievers.

**Connection to Query2Doc:** Direct extension. Instead of one pseudo-document, generate multiple query perspectives. This is like "multi-perspective Query2Doc."

**Feasibility for Colab:** HIGH. Same LLM, same pipeline. Just generate N diverse expansions instead of 1, retrieve for each, then fuse results.

---

### Paper H2: ExpandR: Teaching Dense Retrievers Beyond Queries with LLM Guidance
- **Authors:** Yao et al. (NEUIR)
- **Year/Venue:** 2025, EMNLP 2025
- **arXiv:** 2502.17057
- **Code:** https://github.com/NEUIR/ExpandR

**What they did:** Jointly optimizes LLM query expander and dense retriever. LLM generates semantically rich expansions; retriever is trained on these. Simultaneously, LLM is aligned via DPO guided by retrieval effectiveness as reward signal.

**Key result:** >5% improvement in retrieval performance across multiple benchmarks. Joint optimization creates mutual adaptation between expander and retriever.

**Connection to Query2Doc:** Advanced extension requiring training. Shows the direction of aligned expansion, where the LLM learns to generate expansions that specifically help the retriever.

**Feasibility for Colab:** LOW. Requires training both LLM and retriever. Heavy compute.

---

### Paper H3: Aligned Query Expansion (AQE)
- **Authors:** Adam Yang, Gustavo Penha, Enrico Palumbo, Hugues Bouchard (Spotify Research)
- **Year:** July 2025
- **arXiv:** 2507.11042

**What they did:** Uses RSFT (Rejection Sampling Fine-Tuning) and DPO to align LLM-generated query expansions with retrieval effectiveness. Pipeline: (1) generate multiple expansions, (2) rank by retrieval effectiveness, (3) fine-tune LLM using top/bottom expansions as positive/negative examples.

**Key result:** ~70% reduction in processing time while improving top-1 retrieval accuracy. Strong generalization to out-of-distribution datasets.

**Connection to Query2Doc:** Alignment approach to improve Query2Doc quality. Instead of using the LLM as-is, you fine-tune it to produce retrieval-effective expansions.

**Feasibility for Colab:** MEDIUM. Requires fine-tuning a small LLM (e.g., Qwen 2.5 3B), which fits on Colab. The training data generation (ranking expansions by retrieval effectiveness) uses your existing pipeline.

---

### Paper H4: CTQE: Upcycling Candidate Tokens for Query Expansion
- **Authors:** Kim et al.
- **Year:** September 2025
- **arXiv:** 2509.02377

**What they did:** Extracts diverse expansion terms from a single LLM decoding pass by leveraging unselected candidate tokens (the probability distribution over vocabulary at each step). Since these candidates are conditioned on query context, they serve as valuable expansion signals without extra inference cost.

**Key result:** Strong retrieval performance with significantly lower cost. Comparable to or outperforms more expensive methods across 10 benchmarks.

**Connection to Query2Doc:** Efficiency improvement. Instead of generating a full pseudo-document, extract expansion terms from the token probability distribution during a single forward pass. Could dramatically speed up Query2Doc.

**Feasibility for Colab:** HIGH. No additional inference cost. Requires access to model logits (available with HuggingFace models you already use). Very efficient.

---

<a name="direction-i"></a>
## Direction I: Term-Level Corpus Enrichment

### Paper I1: tRAG: Term-level Retrieval-Augmented Generation for Domain-Adaptive Retrieval
- **Authors:** Dohyeon Lee, Jongyoon Kim, Jihyuk Kim, Seung-won Hwang, Joonsuk Park
- **Year/Venue:** 2025, NAACL 2025
- **ACL Anthology:** 2025.naacl-long.334

**What they did:** Identifies that LLMs have "seen term bias" -- they fail to generate relevant "unseen" terms needed for domain adaptation. Solution: generate domain-specific keywords from ALL documents in the corpus, not just individual ones. Filter hallucinated keywords via retrieval-based reranking.

**Key result:** 10.6% improvement in recall for unseen terms on BEIR benchmark. Outperforms LLM and RAG baselines.

**Connection to Query2Doc:** Directly relevant. Standard Query2Doc may fail when the user's query uses different terminology than the corpus. tRAG-style term enrichment could supplement Query2Doc by adding corpus-specific terms that the LLM might not generate from parametric knowledge.

**Feasibility for Colab:** MEDIUM. Requires preprocessing the entire corpus to build a term inventory. The per-query enrichment itself is lightweight.

---

<a name="direction-x"></a>
## Direction X: "Rebarter"

**Search Result:** Extensive searching for "Rebarter," "Re-Barter," "ReBARTer," and "Re-BARTer" across arXiv, ACL Anthology, Semantic Scholar, and Google Scholar yielded NO results matching a known paper or method in the retrieval/QE domain. The closest matches found were:

- **BERT-QE** (Zheng et al., 2020): Contextualized Query Expansion for Document Re-ranking
- **Rethinking Query Expansion for BERT Reranking** (Zhuyun et al., ECIR 2020)

**Possible explanations:**
1. The name may be slightly different (misspelling or informal reference)
2. It may be a very recent preprint not yet indexed
3. It may be a team-internal name for an approach discussed in a meeting
4. It could be confused with "BART-based" query expansion approaches

**AI Suggestion:** Ask the team member who mentioned "Rebarter" for the exact paper reference (arXiv ID, author names, or URL). If it refers to a BART-based approach to retrieval, the closest known methods are doc2query (Nogueira et al.) and its variants, which use sequence-to-sequence models to generate synthetic queries for documents.

---

<a name="feasibility-matrix"></a>
## Feasibility Matrix for Google Colab

| # | Paper/Approach | Query-Side? | Requires Re-indexing? | Training Needed? | Colab Feasibility | Impact Estimate |
|---|---------------|-------------|----------------------|-----------------|-------------------|----------------|
| A1 | CSQE (Corpus-Steered QE) | YES | No | No | **HIGH** | High |
| A2 | KAR (Knowledge-Aware QE) | YES | No | No | Medium | High |
| B1 | Anthropic Contextual Retrieval | No | YES | No | Low-Med | High |
| B2 | Late Chunking (Jina) | No | YES | No | Low | Medium |
| C1 | DAPR insights (title prepending) | Hybrid | Partial | No | **HIGH** | Medium |
| D1 | RAPTOR (tree retrieval) | No | YES | No | Medium | Medium |
| D2 | LevelRAG (retriever-specific QE) | YES | No | No | Med-High | Medium |
| E1 | KG2RAG (KG-guided expansion) | Hybrid | Partial | No | Medium | High |
| E2 | HippoRAG (PageRank on KG) | Hybrid | YES | No | Medium | High |
| F1 | Dense X (propositions) | Partial | YES | Yes | Medium | Medium |
| G1 | Multi-Meta-RAG (metadata filter) | YES | No | No | **HIGH** | Medium |
| G4 | BMQExpander (ontology-guided) | YES | No | No | **HIGH** | High |
| H1 | RFG (multi-query expansion) | YES | No | No | **HIGH** | Medium |
| H3 | AQE (aligned expansion) | YES | No | Yes (small) | Medium | High |
| H4 | CTQE (candidate token QE) | YES | No | No | **HIGH** | Medium |
| I1 | tRAG (term enrichment) | YES | No | No | Medium | Medium |

---

<a name="recommendations"></a>
## Recommended Directions for Phase 4

Based on feasibility (Colab), connection to existing Query2Doc pipeline, novelty, and expected impact:

### Tier 1: Most Promising (Pick 1-2)

#### 1. **Corpus-Steered Query2Doc** (Papers A1 + C1 + G4)
**The "Mufti" Approach.** Combine CSQE's corpus grounding with DAPR's structural context and BMQExpander's ontology-guided generation. Concretely:
- Step 1: Use BM25 to retrieve top-K documents for the original query (first-pass)
- Step 2: Extract structural metadata: article titles, section headings, Wikipedia categories from retrieved documents
- Step 3: Feed this structural context to the LLM alongside the original query
- Step 4: LLM generates a corpus-grounded, structure-aware pseudo-document
- Step 5: Use this enriched pseudo-document for final dense retrieval

**Why this is best:** It directly extends Query2Doc (same pipeline, same LLM). It addresses the "blind generation" weakness of Query2Doc by grounding in the actual corpus. It implements the "mufti analogy" -- the LLM now knows WHERE to look. No re-indexing needed.

#### 2. **Multi-Perspective Query2Doc** (Paper H1 + D2)
Generate multiple diverse expansions instead of one, retrieve for each, then fuse results. Can optionally generate retriever-specific expansions (one for dense, one for BM25).

**Why this is promising:** Simple to implement, directly improves on single-expansion Query2Doc, and rank fusion is well-understood.

### Tier 2: Good Alternatives

#### 3. **Metadata-Filtered Query2Doc** (Papers G1 + G2 + G3)
Extract topic/category metadata from queries, use it to filter or weight passages before/during retrieval.

#### 4. **CTQE-Enhanced Query2Doc** (Paper H4)
Extract expansion terms from token probability distributions during Query2Doc generation. Zero additional cost.

#### 5. **Aligned Query2Doc** (Paper H3)
Fine-tune your best models (Aya, Jais-2) using DPO/RSFT to generate retrieval-optimized expansions.

### Tier 3: Interesting but Heavy

#### 6. KG-Guided Expansion (Papers E1, E2, A2)
Build lightweight KG from Wikipedia structure, use for expansion guidance.

#### 7. Hierarchical Retrieval (Papers D1, D2)
Multi-level retrieval with document-then-passage strategy.

---

## How Direction 1 ("Corpus-Steered Query2Doc") Builds on Your Existing Work

```
CURRENT PIPELINE (Query2Doc):
  Query -> LLM generates pseudo-document (blind) -> Concatenate -> Dense Retrieval

PROPOSED EXTENSION (Corpus-Steered Query2Doc):
  Query -> BM25 first-pass retrieval -> Extract top-K passages
       -> Extract metadata (article titles, sections, categories)
       -> LLM generates pseudo-document WITH corpus context
       -> Concatenate -> Dense Retrieval

PROMPT TEMPLATE (concept):
  "Given the query: {query}
   The following relevant passages were found in the knowledge base:
   - From article '{article_title}', section '{section}': {passage_snippet}
   - From article '{article_title}', section '{section}': {passage_snippet}
   These articles belong to categories: {categories}

   Generate a detailed Arabic passage that would be relevant to this query,
   taking into account the knowledge base structure above."
```

This extension:
- Uses your existing BM25 baseline (already implemented)
- Uses your existing LLM models (Aya, Jais-2, etc.)
- Uses your existing dense retrieval pipeline (mDPR)
- Only adds: (1) one BM25 call per query, (2) metadata extraction, (3) modified prompt
- Is consistent with your thesis narrative (improving Query2Doc, not replacing it)
- Has clear ablation studies: with/without corpus context, with/without metadata, etc.

---

## Sources

- [Anthropic Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [CSQE - EACL 2024](https://aclanthology.org/2024.eacl-short.34/)
- [CSQE GitHub](https://github.com/Yibin-Lei/CSQE)
- [KAR - NAACL 2025](https://arxiv.org/abs/2410.13765)
- [DAPR - ACL 2024](https://aclanthology.org/2024.acl-long.236/)
- [DAPR GitHub](https://github.com/UKPLab/acl2024-dapr)
- [SEAL - EMNLP 2025](https://arxiv.org/abs/2508.20778)
- [Late Chunking - Jina AI](https://arxiv.org/abs/2409.04701)
- [Contextual Document Embeddings - ICLR 2025](https://arxiv.org/abs/2410.02525)
- [Context is Gold - EMNLP 2025](https://arxiv.org/abs/2505.24782)
- [Reconstructing Context](https://arxiv.org/abs/2504.19754)
- [RAPTOR - ICLR 2024](https://arxiv.org/abs/2401.18059)
- [LevelRAG](https://arxiv.org/abs/2502.18139)
- [KG2RAG - NAACL 2025](https://arxiv.org/abs/2502.06864)
- [HippoRAG - NeurIPS 2024](https://arxiv.org/abs/2405.14831)
- [GraphRAG - Microsoft](https://arxiv.org/abs/2404.16130)
- [Dense X Retrieval - EMNLP 2024](https://arxiv.org/abs/2312.06648)
- [Multi-Meta-RAG](https://arxiv.org/abs/2406.13213)
- [Metadata-Driven RAG for Finance](https://arxiv.org/abs/2510.24402)
- [Utilizing Metadata for Better RAG - ECIR 2026](https://arxiv.org/abs/2601.11863)
- [BMQExpander - Ontology-Guided QE](https://arxiv.org/abs/2508.11784)
- [RFG Framework](https://www.scitepress.org/Papers/2025/138369/138369.pdf)
- [ExpandR - EMNLP 2025](https://arxiv.org/abs/2502.17057)
- [AQE - Spotify Research](https://arxiv.org/abs/2507.11042)
- [CTQE](https://arxiv.org/abs/2509.02377)
- [tRAG - NAACL 2025](https://aclanthology.org/2025.naacl-long.334/)
- [MultiDocFusion - EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1062/)
- [MoDora - SIGMOD 2026](https://arxiv.org/abs/2602.23061)
- [PBR - Personalized QE](https://arxiv.org/abs/2510.08935)
- [Heading-Aware Chunking](https://www.researchgate.net/publication/395813028)
- [QE Survey 2025](https://arxiv.org/abs/2509.07794)
- [GRF - SIGIR 2023](https://arxiv.org/abs/2304.13157)
