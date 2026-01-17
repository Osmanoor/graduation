# Literature Alignment: Query Enhancement Strategy

**Date:** January 17, 2026
**Ref:** Alignment with Thesis Chapter 2 & Provided Papers

## 1. Core Objective
To scientifically translate proven English RAG techniques to the Arabic domain, adhering strictly to the methodologies defined in the literature (`papers/` directory).

## 2. Technique Definition: Query Expansion vs. HyDE

The decision to use **Query Expansion** over **HyDE** is grounded in *Query2doc* (Wang et al., 2023), which empirically demonstrated the superiority of concatenation over replacement.

### 2.1 The Distinction
| Feature | HyDE (Gao et al., 2022) | Query2doc (Wang et al., 2023) |
| :--- | :--- | :--- |
| **Method** | `Vector(Pseudo-Doc)` | `Vector(Original Query + Pseudo-Doc)` |
| **Mechanism** | **Replaces** query with hallucinated text. | **Augments** query with hallucinated text. |
| **Risk** | High. If hallucination is off-topic, retrieval fails completely. | Low. Original query terms preserve intent even if expansion drifts. |
| **Result** | Good for zero-shot, but lower precision. | **State-of-the-Art** for dense retrieval. |

**Decision**: We will implement the **Query2doc** methodology:
$$Q^+ = \text{concat}(Q_{original}, \text{[SEP]}, D'_{pseudo})$$

## 3. Model Selection: Open Source vs. Proprietary

The user correctly noted that the literature emphasizes reproducible, open methodologies.

### 3.1 Literature Precedent
-   **Query2doc**: Originally used `text-davinci-003` (GPT-3).
-   **Optimizing Arabic RAG (Mokhtar et al., 2025)**: Explicitly benchmarks and recommends **Aya-8B** and **StableLM** for Arabic generation tasks, highlighting that open-weight models are sufficient for high-quality Arabic text generation.

### 3.2 The Argument for Open Source
Using **Gemini 1.5 Flash** (Proprietary API) creates a dependency that weakens the "scientific reproduction" aspect of the thesis. Switching to an **Open Source Arabic-Centric Model** aligns better with the goal of "Optimizing Arabic RAG".

### 3.3 Recommended Model: **Aya-23-8B** or **Llama-3-Arabic**
-   **Why**: These models are fine-tuned for Arabic, open-weight, and run locally or via open-inference providers.
-   **Feasibility**:
    -   *Option A (Local)*: If you have a GPU (16GB+ VRAM), we run locally via vLLM/Ollama.
    -   *Option B (API)*: Use HuggingFace Inference API or Groq (Llama 3) as a proxy for open-source availability.

**Revised Proposal**:
We will target **Aya-23-8B** (via HuggingFace API or local) as the generator for Query Expansion. This aligns with *Mokhtar et al. (2025)*.

## 4. Revised Implementation Plan

1.  **Technique**: **Query Expansion (Query2doc style)**.
    -   *Input*: User Query.
    -   *Prompt*: "Write a passage that answers the given question in Arabic." (Few-shot if possible).
    -   *Output*: Pseudo-document.
    -   *Final Query*: `"{query} {pseudo_doc}"`.
2.  **Generator**: **Aya-23-8B** (or Llama-3-8B-Instruct).
3.  **Normalization**: Continued use of `pyarabic` as a pre-processing step before expansion.
