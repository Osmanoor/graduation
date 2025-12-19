- **Short Description:** This paper presents a comprehensive case study on implementing and evaluating Retrieval Augmented Generation (RAG) pipelines specifically for the Arabic language. It investigates the effectiveness of various semantic embedding models for retrieval and multiple Large Language Models (LLMs) for generation, while also addressing linguistic challenges such as dialectal variations.

- **Research Question:** How effective are current multilingual semantic embedding models and LLMs when applied to Arabic RAG systems, particularly in handling the discrepancy between Modern Standard Arabic (MSA) documents and dialectal user queries?

- **Main Methodology:** The authors constructed a two-stage RAG pipeline using Chroma DB as the vector store. The first stage involved benchmarking twelve semantic embedding models (including E5, BGE, OpenAI, and AraBERT) to identify the most accurate retriever. The second stage utilized the best-performing retriever to evaluate the generation capabilities of five LLMs (GPT-3.5 Turbo, Mistral 7B, Llama 3, Mixtral, and JAIS) based on retrieved context.

- **Dataset & Benchmark:**
  - **Datasets:**
    1. **Ar_EduText:** A custom dataset compiled from MSA high school textbooks, featuring questions available in both MSA and Egyptian dialect.
    2. **ARCD (Arabic Reading Comprehension Dataset):** A Wikipedia-based QA dataset, which the authors manually modified to disambiguate context-dependent questions.
  - **Metrics:**
    - *Retrieval:* Recall@k (k=1, 3, 5) and Mean Reciprocal Rank (MRR).
    - *Generation:* F1 Score, BLEU Score, and Cosine Similarity.

- **Research Contributions:**
  The study fills a significant technical gap by benchmarking the resilience of embedding models against Arabic dialectal variations. The authors demonstrate that while retrieving MSA segments using Egyptian dialect queries typically degrades performance, Microsoft’s E5 and BAAI’s BGE models exhibit remarkable robustness, significantly outperforming other models including the Arabic-centric JAIS (quantized). Furthermore, the work highlights the importance of data preprocessing in Arabic RAG, showing that manual disambiguation of interdependent questions in standard datasets like ARCD leads to substantial improvements in retrieval accuracy.

  Additionally, the paper challenges the assumption that proprietary or highly specialized models are required for effective Arabic text generation. The experiments reveal that open-source models, specifically Llama 3 and Mistral 7B, are highly capable generators, performing comparably to or better than GPT-3.5 Turbo on the ARCD dataset. This finding establishes that accessible, general-purpose multilingual LLMs can be effectively leveraged to build high-quality Arabic RAG pipelines without heavy computational resources.