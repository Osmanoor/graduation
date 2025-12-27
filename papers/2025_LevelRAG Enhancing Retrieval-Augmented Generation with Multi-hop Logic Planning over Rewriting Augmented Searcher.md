**Short Description**
This paper introduces LevelRAG, a hierarchical Retrieval-Augmented Generation framework that decouples high-level multi-hop logic planning from low-level retriever-specific query rewriting. By utilizing a central planner to coordinate specialized sparse, dense, and web searchers, the method optimizes both the breadth and accuracy of information retrieval for complex queries.

**Research Question**
How can RAG systems effectively address the limitations of current query rewriting techniques—which are often tightly coupled to dense retrievers—to enable robust hybrid retrieval that handles both complex multi-hop reasoning and precise keyword extraction?

**Main Methodology**
The authors propose a two-tiered architecture:
1.  **High-Level Searcher:** A planning agent responsible for decomposing complex user queries into atomic sub-queries (Decompose), summarizing retrieved content (Summarize), checking if the information is sufficient (Verify), and generating follow-up queries if necessary (Supplement).
2.  **Low-Level Searchers:** Heterogeneous modules optimized for specific retrieval types:
    *   **Sparse Searcher:** A novel component that iteratively refines queries using **Lucene syntax**. It employs a feedback loop to "extend" (add keywords), "emphasize" (weight specific terms), or "filter" (exclude noise) based on retrieval results.
    *   **Dense Searcher:** Uses iterative rewriting and pseudo-document generation (similar to HyDE) to capture semantic meaning.
    *   **Web Searcher:** Leverages commercial search engines to supplement local databases with up-to-date internet knowledge.

**Dataset & Benchmark**
The method is evaluated on five knowledge-intensive datasets:
*   **Single-hop QA:** PopQA, Natural Questions (NQ), and TriviaQA.
*   **Multi-hop QA:** HotpotQA and 2WikimultihopQA.
*   **Metrics:** Retrieval Success Rate (Succ), Response Accuracy (Acc), F1 Score, and Exact Match (EM).

**Research Contributions**
The primary contribution of this work is the LevelRAG framework, which solves the incompatibility between standard query rewriting and hybrid retrieval by separating reasoning from retrieval execution. By assigning the logic planning to a High-Level Searcher and the query refinement to specialized Low-Level Searchers, the system ensures that complex queries are broken down effectively while allowing each retriever type (sparse, dense, web) to operate using its optimal syntax and strategy. This hierarchical approach prevents the "tight coupling" issue seen in prior works where rewriting was biased toward dense vector retrieval.

Additionally, the paper introduces a novel **Sparse Searcher** that explicitly leverages Lucene syntax for iterative query optimization. This searcher can dynamically adjust queries using operators (e.g., quotations for exact matches, carets for boosting weights) based on feedback, addressing the precision limitations of traditional BM25 approaches. Empirical results show that LevelRAG significantly outperforms state-of-the-art baselines, including Self-RAG and Adaptive RAG, and notably surpasses the proprietary model GPT-4o in response quality across the tested datasets.
