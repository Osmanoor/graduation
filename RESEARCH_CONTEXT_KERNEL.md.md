# 🧬 RESEARCH_CONTEXT_KERNEL.md
**Project:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement
**Status:** Phase 1 - Foundational Investigation & Validation
**Last Updated:** [Current Date]

---

## 1. 🧭 Project Overview & Trajectory
**The Goal:** We aim to improve the retrieval recall of RAG systems for **Low-Resource Languages (specifically Arabic)**. We hypothesize that standard retrieval fails due to the "Morphological & Dialectal Gap" (mismatch between user queries and corpus documents).
**The Pivot:**
*   *Original Scope:* Broad RAG enhancement using GraphRAG and Agentic workflows.
*   *Current Scope:* Narrowed significantly to focus on **Query Enhancement (QE)** techniques. We believe fixing the input (the query) is the most high-leverage intervention for Arabic morphology and dialects.

## 2. 📍 Current Status: The "Investigation" Phase
We are currently in the **Literature Review & Methodology Definition** stage.
*   **What we have done:** We have conducted a broad landscape analysis of English-centric RAG papers (HyDE, RQ-RAG, QE-RAG, etc.) to understand the "Schools of Thought."
*   **What we are doing now:** We are trying to **bridge the gap to Arabic**. We are investigating whether these English techniques work for Arabic or if we need a novel adaptation.
*   **Critical Note for Agents:** **DO NOT ASSUME IMPLEMENTATION DETAILS.** We have **not** yet finalized the dataset, the baseline model, or the specific Query Enhancement technique. We are currently gathering evidence to make these decisions.

---

## 3. 📉 The "Undecided" Variables (Active Research Questions)
*The Agent's primary goal is to help us resolve these variables using evidence, not assumptions.*

### A. The Dataset (Selection Pending)
We need a dataset that specifically challenges **Retrieval** (not just Reasoning) and features **Dialectal/Morphological complexity**.
*   *Candidates under review:* TyDi QA (GoldP), MIRACL (Arabic), ARCD, or a custom-synthesized dataset.
*   *The Dilemma:* General datasets might not have enough dialect queries. Specialized dialect datasets might be too small or focused on sentiment analysis rather than retrieval.

### B. The Baseline Pipeline (Selection Pending)
We need to define a "Standard Control" to measure improvement against.
*   *Candidates under review:* BM25 (Sparse), `bge-m3` (Dense), or a Hybrid approach.
*   *The Dilemma:* We need to determine the current SOTA baseline for Arabic retrieval so we don't compare our work against a weak system.

### C. The Query Enhancement Technique (Selection Pending)
We have identified English paradigms, but haven't selected the Arabic solution.
*   *Candidates under review:*
    *   **Generative Expansion (HyDE):** Hallucinating MSA documents from Dialect queries.
    *   **Query Rewriting:** Translating Dialect $\to$ MSA using an LLM.
    *   **Decomposition:** Breaking complex Arabic queries into sub-queries.
*   *The Dilemma:* Does Arabic LLM hallucination (e.g., Jais/AceGPT) create more noise than signal? Is simple translation better?

---

## 4. 📂 Repository Structure & Knowledge Base
*The Agent should use these files to understand our accumulated knowledge.*

*   **`/gemini_opinions/`**: Contains strategic discussions, pivots, and "Project Management" decisions.
    *   *Key File:* `Branch of Critical Feedback...` (Explains why we dropped GraphRAG).
    *   *Key File:* `Branch of RQ-RAG...` (Analysis of the "Active Generator" architecture).
*   **`/papers/`**: Contains raw summaries of the academic literature we have read.
    *   *Key Insight:* We have analyzed `QE-RAG.md` (Query Noise), `RQ-RAG.md` (Iterative Feedback), and `Optimizing RAG Pipelines for Arabic.md` (Baseline components).
*   **`summaries/`**: (If applicable) Contains broader summaries of chat logs.

---

## 5. ⚠️ Current Challenges & Risks
1.  **The "English Bias":** Most of our insights come from English papers. We risk assuming a technique like HyDE works for Arabic without evidence.
2.  **Evaluation Rigor:** We lack a standardized "Ruler" for Arabic RAG. We are struggling to define a rigorous evaluation methodology that goes beyond simple "Recall@K."
3.  **Data Scarcity:** We are concerned about the lack of high-quality "Dialect Query $\to$ MSA Document" pairs for training or evaluation. We are considering **Synthetic Data Generation** but haven't validated the workflow.

---

## 6. 🎯 Immediate Agent Objectives
When interacting with this codebase, the Agent should:
1.  **Synthesize:** Read the `/papers/` summaries to find connections between English methods and Arabic problems.
2.  **Validate:** Help us formulate search prompts or experiments to validate if English methods (like HyDE) are transferable to Arabic.
3.  **Document:** Update this kernel as we make decisions (e.g., "Decision: We selected Dataset X because of reason Y").

