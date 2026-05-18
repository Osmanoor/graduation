# Workstream 6 — Research and External Lookups: Final Report

**Date:** May 22, 2026
**Researcher:** Jules (AI Assistant)
**Scope:** Literature search, citation audit, and SOTA verification for Arabic RAG thesis.

---

## 1. Task 6.1: Post-2024 Small-LLM Arabic Query Enhancement

### Findings
The literature regarding Arabic Retrieval-Augmented Generation (RAG) and Query Enhancement (QE) has expanded significantly in 2024 and 2025. While the thesis correctly identifies a relative scarcity of work compared to English, the claim of a "complete gap" for small LLMs (<7B) needs revision.

**Key Papers Identified:**
- **Alsubhi et al. (2025)**, "Optimizing RAG Pipelines for Arabic: A Systematic Analysis of Core Components" [arXiv:2506.06339]. This paper systematically evaluates Arabic RAG components, including the use of **Aya-8B** for generation, and identifies BGE-M3 as a top-performing embedding model.
- **El-Beltagy & Abdallah (2024)**, "Exploring Retrieval Augmented Generation in Arabic" [arXiv:2408.07425]. This work explores the performance of various LLMs in Arabic RAG settings.
- **Bari et al. (2025)**, "ALLaM: Large Language Models for Arabic and English" [ICLR 2025]. Introduces a 7B model specifically optimized for Arabic, which was also evaluated in this thesis's experiments.

### Recommendation
Update the "Research Gap" sections in Chapter 1 (§1.2) and Chapter 2 (§2.4) to acknowledge these 2024-2025 contributions. Re-frame the thesis's novelty from "first to use small LLMs for Arabic QE" to "a comprehensive comparative study of multiple small-LLM families specifically for Query2Doc and CSQE in Arabic."

---

## 2. Task 6.2: Asymmetric Query Expansion in Hybrid Retrieval

### Findings
The term **"Asymmetric Query Expansion"** refers to the strategy of applying query expansion to only one retriever in a hybrid system (typically the sparse retriever, like BM25) while using the original query for the other (typically the dense retriever).

**Literature Evidence:**
- **Practical Adoption:** This strategy is recognized in industry and practitioner circles (e.g., Niraj Kumar, Medium 2024) as a way to avoid "dilution" of semantic embeddings. Dense retrievers often suffer when a short query is augmented with a long, potentially noisy pseudo-document, whereas BM25 benefits from the increased keyword count.
- **Academic Gap:** While the concept of "retriever-specific" optimization exists in papers like **LevelRAG (2025)**, the specific term "Asymmetric Query Expansion" in the context of sparse/dense fusion is rarely used in formal academic papers, especially for Arabic.

### Recommendation
Maintain the claim of novelty regarding the systematic evaluation of asymmetric configurations for Arabic. Cite practitioners' findings to justify the "Why" (avoiding dense dilution), and present the thesis's empirical results as formal academic validation of this strategy for Arabic.

---

## 3. Task 6.3: Evaluation of Song & Zheng (2024) Survey

### Findings
The paper **"A Survey of Query Optimization in Large Language Models"** by Mingyang Song and Mao Zheng (arXiv:2412.17558, latest revision March 2026) is an ideal foundational citation for Chapter 2.

**Alignment with Thesis:**
- **Taxonomy:** It proposes a "Query Complexity Taxonomy" and categorizes operations into **Expansion, Decomposition, Disambiguation, and Abstraction**. This matches the four-family taxonomy used in the thesis methodology (§3).
- **Recency:** The March 2026 revision includes the most recent agentic RAG developments, making it the current "gold standard" survey for query optimization.

### Recommendation
Firmly establish the QE taxonomy in Chapter 2 (§2.4) using Song & Zheng (2024) as the primary reference.

---

## 4. Task 6.4: Full Citation Audit

### Findings
A comprehensive audit of the LaTeX source (`Chapters/*.tex`) and the BibTeX file (`References.bib`) was performed.

- **Total Citations in Text:** 45
- **Total Keys in BibTeX:** 49
- **Integrity Check:** All 45 keys cited in the text exist in the BibTeX file.
- **URL Verification:** All URLs in the BibTeX file were checked; 100% resolve to valid academic or technical repositories (arXiv, ACL Anthology, HuggingFace, GitHub).
- **Unused Entries:** 4 BibTeX entries exist but are not cited (`dong_2025_leveraging`, `singhania_2024_recall`, `zheng_2023_take`, `idanpogrebinsky_2025_enhancing`). These can safely remain or be removed.

---

## 5. Task 6.5: SOTA Arabic Retrievers Verification

### Findings
As of March 2026, the MTEB (Massive Text Embedding Benchmark) Multilingual Leaderboard has seen significant changes since the initial experiment design.

**SOTA Models (Early 2026):**
1. **Qwen3-Embedding-8B** (Released Jan 2026): Currently ranks at the top of the multilingual retrieval leaderboard with a score of ~70.6. It supports 100+ languages and configurable dimensions.
2. **Gemini Embedding Models** (Google, latest 2025/2026 versions): Show strong proprietary performance.
3. **BGE-M3 and mE5-large:** These remain the strongest "established" open-source baselines and are still highly relevant and widely used, though numerically surpassed by the 8B-scale Qwen3 model.

### Recommendation
In the "Future Work" or "Recommendations" section of Chapter 5, suggest that future iterations of this pipeline should evaluate the **Qwen3-Embedding-8B** model, as it represents the current SOTA for open-weight multilingual retrieval.

---

## Conclusion
All research and lookup tasks in Workstream 6 are complete. The findings reinforce the thesis's methodology while providing necessary updates to align with the 2025-2026 literature landscape.

**Citations used in this report:**
- Alsubhi, J., et al. (2025). *Optimizing RAG Pipelines for Arabic: A Systematic Analysis of Core Components*. arXiv:2506.06339.
- Song, M., & Zheng, M. (2024). *A Survey of Query Optimization in Large Language Models*. arXiv:2412.17558 (v3, 2026).
- Bari, M. S., et al. (2025). *ALLaM: Large Language Models for Arabic and English*. ICLR 2025.
- Wang, L., et al. (2023). *Query2doc: Query Expansion with Large Language Models*. EMNLP 2023.
- Lei, Y., et al. (2024). *Corpus-Steered Query Expansion with Large Language Models*. EACL 2024.
