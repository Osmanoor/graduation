- **Short Description:**
This paper presents L3X (LM-based Long List eXtraction), a two-stage framework designed to extract comprehensive lists of object entities related to a subject from extremely long documents, such as entire books. The method combines recall-oriented retrieval-augmented generation (RAG) with a precision-oriented scrutinization phase to maximize coverage while minimizing false positives.

- **Research Question:**
How can automated systems effectively extract long, complete lists of object entities that stand in a specific relation to a subject when the supporting evidence is sparse and scattered across extensive texts (e.g., identifying all 57 friends of Harry Potter from the book series)?

- **Main Methodology:**
The authors propose **L3X**, which operates in two distinct stages:
1.  **Recall-oriented Generation:** This stage utilizes an LLM (specifically Llama-3) in a RAG setup. It employs dense retrieval (Contriever) enhanced by **re-ranking heuristics** (such as entity mention frequency) and **pseudo-relevance feedback (*amp*)**, which iteratively refines retrieval queries using previously found high-confidence passages. Passages are grouped using **batching strategies** (like named entity overlap) to prompt the LLM for maximum entity discovery.
2.  **Precision-oriented Scrutinization:** To filter the noisy list from Stage 1, this stage retrieves specific "support passages" for each candidate Subject-Object pair. It then validates them using self-supervised **classifiers** (such as predicate-specific embedding comparisons or discriminative classifiers) to prune incorrect entities based on semantic evidence.

- **Dataset & Benchmark:**
*   **Datasets:** Two newly curated datasets were introduced: a **Books Dataset** (11 popular novels/series, such as *Harry Potter* and *A Song of Ice and Fire*, covering 8 relations like *opponent* or *hasMember*) and a **Web Dataset** (derived from the C4 corpus, focusing on business relations like *hasSubsidiary*).
*   **Metrics:** The primary evaluation metric is **Recall@PrecisionX (R@Px)** (specifically R@P50 and R@P80), alongside standard Precision, Recall, and Area Under the Curve (AUC).

- **Research Contributions:**
This work addresses a significant gap in Information Extraction (IE) by defining the problem of "long-list extraction from long documents," moving beyond the standard single-sentence or short-passage paradigms that struggle to aggregate scattered cues. The authors demonstrate that standard LLMs relying on parametric memory exhibit severe recall deficits on long-tail facts (e.g., minor characters in fiction). By treating entire books as the input context, the paper establishes a new benchmark for handling the "two longs"—long object lists and long source texts—that prior methods and datasets (like DocRED) could not accommodate.

Technically, the paper contributes the L3X methodology, distinguishing itself through the *amp* (pseudo-relevance feedback) technique which significantly boosts recall by using initial extraction results to find better context passages. Furthermore, the introduction of self-supervised scrutinization classifiers allows for high-precision filtering without requiring annotated passage labels. Experiments show that L3X dramatically outperforms LLM-only baselines, raising recall from roughly 50% to nearly 85% on the Books dataset and achieving almost 50% Recall at 50% Precision.