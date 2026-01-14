# Error Analysis Research Synthesis
**Date:** January 2025
**Sources:** Gemini Deep Research, Qwen Deep Research, ChatGPT Deep Research, Perplexity Pro

## Executive Summary
*   **No Native Metadata:** All four reports confirm that MIRACL contains **no** built-in domain labels (e.g., "Medical," "Law") or difficulty scores. This is confirmed by **Gemini** (citing *Zhang et al., 2023*) [1] and **ChatGPT** (citing the *Project MIRACL GitHub Repository*) [2].
*   **The "NoMIRACL" Dataset is Critical:** Three out of four reports (Perplexity, Qwen, Gemini) identify **NoMIRACL** as a game-changer. It is an extension of MIRACL that explicitly identifies "hard negatives" and hallucination triggers. **Perplexity** cites *Thakur et al., "NoMIRACL: Knowing When You Don't Know"* [3], and **Qwen** references the *EMNLP 2024 Findings* [4], noting this allows for robust error analysis without needing new annotations.
*   **Wikipedia is the Key to Labels:** Since MIRACL is sourced from Wikipedia, the most immediate "hack" is to fetch category tags via the MediaWiki API based on article titles. **Gemini** suggests this approach referencing *"Leveraging Corpus Metadata to Detect Template-based Translation"* [5], and **Perplexity** lists it as "Option 3" in their automated classification section.
*   **Query-Side Analysis is High-ROI:** Instead of analyzing 2.1M passages, focus on analyzing the ~3,000 queries using the **AAFAQ** framework (Arabic specific). **Gemini** references *Abdelaziz et al., "A Benchmark Arabic Dataset for Arabic Question Classification"* [6] for this framework. Additionally, **Qwen** suggests using statistical metrics like score gaps and length, referencing *Mahmoud Namnam's "Arabic NLP Text Preprocessing Guide"* [7].

---

## Key Finding: MIRACL Metadata Status
**Consensus:** There is **zero** extended metadata in the official MIRACL release. The dataset consists strictly of query-passage pairs with binary relevance judgments.
*   *ChatGPT* and *Perplexity* confirm any topic/difficulty tagging must be created post-hoc.
*   *Gemini* notes the lack of granular labels prevents easy diagnosis of subject-specific failures, referencing the original MIRACL paper *Zhang et al., 2023* [1].
*   *Qwen* highlights that while MIRACL lacks metadata, the *NoMIRACL* extension fills the gap regarding "robustness" and "hard negative" identification, citing *"NoMIRACL: Knowing When You Don't Know for Robust Multilingual Retrieval-Augmented Generation"* [8].

---

## Practical Error Analysis Approaches

### A. Immediate Actions (Week 1 - Low Compute/Setup)

#### 1. Leverage NoMIRACL for "Hard Negative" Analysis
*   **What:** Use the *NoMIRACL* dataset subset (which extends MIRACL) to identify queries where the retriever is confused by non-relevant but highly similar documents.
*   **Sources:**
    *   **Perplexity** (citing *Thakur et al., EMNLP 2024 Findings*) [3].
    *   **Qwen** (citing *EMNLP 2024 Findings* [4] and *WikiNLP 2024* [9]).
    *   **Gemini** (citing the *Hugging Face NoMIRACL Dataset*) [10].
*   **Difficulty:** Easy (Dataset is available on HuggingFace).
*   **Colab Compatible:** Yes.
*   **Action:** Calculate the "Score Gap" (difference between relevant doc score and top non-relevant doc score). **Qwen** suggests this metric, citing *"Rank-at-k optimization...", MRL 2025* [11]. Small gaps = low confidence/high confusion.

#### 2. Wikipedia Category Extraction
*   **What:** MIRACL preserves the original Wikipedia article titles. Use the `wikipedia-api` or MediaWiki API to fetch the "Category" tags for the retrieved passages.
*   **Sources:**
    *   **ChatGPT** (citing *Project MIRACL GitHub*) [2].
    *   **Gemini** (citing *arXiv:2404.00565*) [5].
    *   **Perplexity** (Listed as "Option 3: Wikipedia Category Extraction").
*   **Difficulty:** Easy.
*   **Colab Compatible:** Yes (requires internet access).
*   **Action:** Map the ~3,000 query-relevant passages to high-level categories (e.g., History, Science) to check if one domain fails more than others.

#### 3. Basic Query Feature Engineering
*   **What:** Calculate statistical features for every query using standard Python string operations.
*   **Sources:**
    *   **Qwen** (citing *Mahmoud Namnam, "Arabic NLP Text Preprocessing Guide"*) [7].
    *   **ChatGPT** (citing *Leung et al., "Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems"*) [12].
*   **Difficulty:** Easy.
*   **Colab Compatible:** Yes.
*   **Metrics to compute:**
    *   Query Length (tokens) — Short queries (<10 tokens) are often ambiguous (**Qwen** citing *Namnam* [7]).
    *   Exact Match overlap (Query terms appearing in Top-10 docs).
    *   IDF Variance (Are keywords rare or common?) (**ChatGPT** citing *Leung et al.* [12]).

### B. Short-term Options (Week 2-3 - Medium Effort)

#### 1. AAFAQ Taxonomy Classification (Arabic Specific)
*   **What:** Manually or heuristically tag queries using the **AAFAQ** (Arabic Analytical Framework for Advanced Questions) dimensions: Factoid vs. Non-factoid, Subjective vs. Objective, etc.
*   **Sources:**
    *   **Gemini** (citing *Abdelaziz et al., "A Benchmark Arabic Dataset for Arabic Question Classification"*) [6].
    *   **ChatGPT** (citing the same work by *Abdelaziz et al.* [6]).
*   **Difficulty:** Medium (Requires understanding the framework).
*   **Colab Compatible:** Yes.
*   **Value:** Explains *why* a query fails (e.g., "System fails on 'Why' questions but succeeds on 'Who' questions").

#### 2. Lightweight Unsupervised Clustering
*   **What:** Use a lightweight multilingual embedding model (e.g., **E5-NL** or **mBERT**) to embed the top failed queries and cluster them (K-Means).
*   **Sources:**
    *   **Qwen** (citing *"MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch"* [13] and *arXiv:2509.12340* [14]).
    *   **Perplexity** (citing *Hang et al., "WC-SBERT: Zero-Shot Topic Classification Using SBERT", ACM 2024*) [15].
    *   **ChatGPT** (citing *Markus Stoll, "Visualize your RAG Data"*) [16].
*   **Difficulty:** Medium.
*   **Colab Compatible:** Yes (if using small models like E5-small).
*   **Action:** Visualize clusters with UMAP to see if failures are thematically grouped (e.g., a cluster of "religious history" queries failing together).

#### 3. Ranking Analysis with `ranx`
*   **What:** Use the `ranx` Python library to generate comparative reports and visualize "drop-offs" in ranking.
*   **Sources:**
    *   **Gemini** (citing *Bassani et al., "ranx: A Blazing-Fast Python Library for Ranking Evaluation and Comparison"*) [17].
*   **Difficulty:** Easy/Medium.
*   **Colab Compatible:** Yes.
*   **Action:** Visualize Recall@K distribution to spot if relevant docs are just missing the cutoff (Rank 11-20) or totally lost (Rank >100).

### C. Advanced/Future Options (Thesis Extension)

#### 1. Zero-Shot LLM Topic Labeling
*   **What:** Use an LLM (Qwen-2.5 or Llama-3 via API) to classify passages into 14 fixed categories (based on *ArBNTopic*).
*   **Sources:**
    *   **Perplexity** (citing *Albared et al., "Arabic Topic Classification in the Generative and AutoML Era", ArabicNLP 2023*) [18].
*   **Difficulty:** Medium/Hard (API costs or GPU RAM constraints).
*   **Constraint:** On Colab free tier, running a local LLM for 2.1M passages is impossible. Only viable for the ~3,000 query-related passages.

#### 2. MEMERAG Methodology
*   **What:** A rigorous flow-chart-based manual annotation process to check for "faithfulness" vs "factuality."
*   **Sources:**
    *   **Perplexity** (citing *Blandón et al., "MEMERAG: A Multilingual End-to-End Meta-Evaluation Benchmark...", ACL 2025*) [19].
    *   **Gemini** (citing the same *Blandón et al.* work via ResearchGate) [20].
*   **Difficulty:** Hard (Labor intensive).

---

## Arabic-Specific Considerations
*   **AAFAQ Framework:** *Gemini* heavily stresses using this 11-dimension framework for query classification, as it captures Arabic-specific nuances (particle types, morphology) better than generic taxonomies, referencing *Abdelaziz et al., 2025* [6].
*   **Morphology & Roots:** *Qwen* suggests analyzing failures based on "Root Frequency." Queries containing words with rare roots or complex morphology (clitics) often fail in sparse retrieval (BM25) if not properly segmented, citing *"Persian Text Correction"*, *arXiv:2407.14795* [21] as an analogous study.
*   **Diacritics:** *Qwen* notes that lack of diacritics introduces ambiguity. Check if failures correlate with highly ambiguous undiacritized terms, citing *"Arabic Natural Language Processing for Qur'anic Research"* [22].
*   **ArBNTopic:** *Perplexity* identifies this as a specific Arabic topic classification dataset/model (14 categories) that can be used for zero-shot labeling, referencing *Albared et al., 2023* [18].

---

## Tools & Resources Summary

| Tool | Purpose | Colab? | Difficulty | Primary Source & Reference |
| :--- | :--- | :--- | :--- | :--- |
| **NoMIRACL** | Dataset for hard negatives/robustness | Yes | Easy | **Perplexity** [3]; **Qwen** [4] |
| **Wikipedia-API** | Fetching categories for passages | Yes | Easy | **Gemini** [5]; **ChatGPT** |
| **Pyserini** | Baseline retrieval & Indexing | Yes | Easy | **Gemini** & **Qwen** [2] |
| **AAFAQ** | Taxonomy for Arabic Query Classification | Yes | Medium | **Gemini** [6]; **ChatGPT** |
| **Ranx** | Ranking evaluation & visualization | Yes | Easy | **Gemini** [17] |
| **Sentence-Transformers** | Embeddings for clustering (e.g., E5) | Yes | Medium | **Qwen** [13] |
| **ir_explain** | Post-hoc explanation of ranking | Yes | Medium | **Gemini** [23] |
| **XTools API** | Wikipedia article metadata stats | Yes | Easy | **Gemini** [5] |

---

## Gaps & Open Questions
1.  **Dialectal Retrieval:** *Gemini* notes a gap in dialect support (MIRACL is MSA), referencing *"Language Drift in Multilingual Retrieval-Augmented Generation"* [24]. None of the reports offered a concrete tool to auto-detect dialect in queries to see if dialect mismatches cause failures.
2.  **Standardized Arabic Hard Negatives:** While *NoMIRACL* exists, *Perplexity* notes there is no specific taxonomy for *why* a hard negative is hard in Arabic (e.g., is it root sharing? is it entity confusion?). This requires manual qualitative analysis.

---

## Recommended Next Steps (For your 6-week timeline)

1.  **Week 1 (Baseline & Data):**
    *   Run Pyserini baselines (BM25 + mDPR).
    *   Download **NoMIRACL** to get the "Hard Negative" labels (**Qwen** citing [4]).
    *   Write a script using `wikipedia-api` to fetch categories for the relevant passages in the dev set.

2.  **Week 2 (Query Analysis):**
    *   Implement **AAFAQ** logic (or simplified version): Tag queries by "Type" (Factoid/List) and "Topic" (using the Wikipedia categories fetched in Week 1).
    *   Calculate **Score Gaps**: Identify queries where the top-1 doc score is very close to the top-2 score (confusion) (**Qwen** citing [11]).

3.  **Week 3 (Pattern Recognition):**
    *   Cluster the *failed* queries (NDCG < 0.1) using **E5-small** embeddings.
    *   Visual inspection: Do the failed queries cluster around specific topics (e.g., Sports) or specific linguistic features (e.g., very short queries)?

4.  **Week 4-6 (Enhancement):**
    *   Use these insights to select your enhancement strategy (e.g., if short queries fail, use Query Expansion; if score gaps are small, use Re-ranking).

---

## References

[1] Zhang et al., "MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages", TACL 2023. Available: [https://aclanthology.org/2023.tacl-1.63.pdf](https://aclanthology.org/2023.tacl-1.63.pdf)

[2] Project MIRACL GitHub Repository. Available: [https://github.com/project-miracl/miracl](https://github.com/project-miracl/miracl)

[3] Thakur et al., "NoMIRACL: Knowing When You Don't Know", arXiv 2312.11361. Available: [https://arxiv.org/abs/2312.11361](https://arxiv.org/abs/2312.11361)

[4] Thakur et al., "Knowing When You Don't Know: A Multilingual Relevance Assessment Dataset for Robust Retrieval-Augmented Generation", EMNLP 2024 Findings. Available: [https://aclanthology.org/2024.findings-emnlp.730.pdf](https://aclanthology.org/2024.findings-emnlp.730.pdf)

[5] "Leveraging Corpus Metadata to Detect Template-based Translation", arXiv 2404.00565. Available: [https://arxiv.org/html/2404.00565v1](https://arxiv.org/html/2404.00565v1)

[6] Abdelaziz et al., "A Benchmark Arabic Dataset for Arabic Question Classification", Scientific Data 2025. Available: [https://www.nature.com/articles/s41597-025-05688-0](https://www.nature.com/articles/s41597-025-05688-0)

[7] Mahmoud Namnam, "Arabic NLP Text Preprocessing Guide". Available: [https://www.linkedin.com/posts/mahmoudnamnam_arabic-nlp-text-preprocessing-guide-activity-7293354136169803776-2_lX](https://www.linkedin.com/posts/mahmoudnamnam_arabic-nlp-text-preprocessing-guide-activity-7293354136169803776-2_lX)

[8] "NoMIRACL: Knowing When You Don't Know for Robust Multilingual Retrieval-Augmented Generation", arXiv 2312.11361v1. Available: [https://arxiv.org/html/2312.11361v1](https://arxiv.org/html/2312.11361v1)

[9] "NoMIRACL: Knowing When You Don't Know...", WikiNLP 2024. Available: [https://aclanthology.org/2024.wikinlp-1.3.pdf](https://aclanthology.org/2024.wikinlp-1.3.pdf)

[10] Hugging Face NoMIRACL Dataset. Available: [https://huggingface.co/datasets/miracl/nomiracl](https://huggingface.co/datasets/miracl/nomiracl)

[11] "Rank-at-k optimization...", MRL 2025. Available: [https://aclanthology.org/2025.mrl-main.42.pdf](https://aclanthology.org/2025.mrl-main.42.pdf)

[12] Leung et al., "Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems", arXiv 2510.13975. Available: [https://arxiv.org/html/2510.13975v1](https://arxiv.org/html/2510.13975v1)

[13] "MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch". Available: [https://www.researchgate.net/publication/395541274_MTEB-NL_and_E5-NL_Embedding_Benchmark_and_Models_for_Dutch](https://www.researchgate.net/publication/395541274_MTEB-NL_and_E5-NL_Embedding_Benchmark_and_Models_for_Dutch)

[14] "MTEB-NL and E5-NL", arXiv 2509.12340. Available: [https://arxiv.org/pdf/2509.12340](https://arxiv.org/pdf/2509.12340)

[15] Hang et al., "WC-SBERT: Zero-Shot Topic Classification Using SBERT", ACM 2024. Available: [https://arxiv.org/abs/2303.10310](https://arxiv.org/abs/2303.10310)

[16] Markus Stoll, "Visualize your RAG Data". Available: [https://medium.com/data-science/visualize-your-rag-data-evaluate-your-retrieval-augmented-generation-system-with-ragas-fc2486308557](https://medium.com/data-science/visualize-your-rag-data-evaluate-your-retrieval-augmented-generation-system-with-ragas-fc2486308557)

[17] Bassani et al., "ranx: A Blazing-Fast Python Library for Ranking Evaluation and Comparison". Available: [https://www.researchgate.net/publication/359735510_ranx_A_Blazing-Fast_Python_Library_for_Ranking_Evaluation_and_Comparison](https://www.researchgate.net/publication/359735510_ranx_A_Blazing-Fast_Python_Library_for_Ranking_Evaluation_and_Comparison) or [https://github.com/AmenRa/ranx](https://github.com/AmenRa/ranx)

[18] Albared et al., "Arabic Topic Classification in the Generative and AutoML Era", ArabicNLP 2023. Available: [https://arxiv.org/abs/2504.16304](https://arxiv.org/abs/2504.16304)

[19] Blandón et al., "MEMERAG: A Multilingual End-to-End Meta-Evaluation Benchmark...", ACL 2025. Available: [https://ebooks.iospress.nl/doi/10.3233/SSW240006](https://ebooks.iospress.nl/doi/10.3233/SSW240006)

[20] Blandón et al., "MEMERAG...", ResearchGate. Available: [https://www.researchgate.net/publication/389315704_MEMERAG_A_Multilingual_End-to-End_Meta-Evaluation_Benchmark_for_Retrieval_Augmented_Generation](https://www.researchgate.net/publication/389315704_MEMERAG_A_Multilingual_End-to-End_Meta-Evaluation_Benchmark_for_Retrieval_Augmented_Generation)

[21] "Persian Text Correction", arXiv 2407.14795. Available: [https://arxiv.org/pdf/2407.14795](https://arxiv.org/pdf/2407.14795)

[22] "Arabic Natural Language Processing for Qur'anic Research: A Systematic Review". Available: [https://www.researchgate.net/publication/350788763_Arabic_Natural_Language_Processing_for_Qur'anic_Research_A_Systematic_Review](https://www.researchgate.net/publication/350788763_Arabic_Natural_Language_Processing_for_Qur'anic_Research_A_Systematic_Review)

[23] "ir_explain: a Python Library of Explainable IR Methods", arXiv 2404.18546. Available: [https://arxiv.org/html/2404.18546v3](https://arxiv.org/html/2404.18546v3)

[24] "Language Drift in Multilingual Retrieval-Augmented Generation", arXiv 2511.09984. Available: [https://arxiv.org/html/2511.09984v1](https://arxiv.org/html/2511.09984v1)