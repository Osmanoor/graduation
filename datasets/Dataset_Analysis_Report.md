
This report analyzes Arabic and multilingual datasets to identify the most suitable benchmarks for researching **Query Enhancement (QE)** techniques in Arabic RAG systems. The analysis focuses on the "Retrieval" component, prioritizing datasets that challenge query-document matching.

---

## 1. Individual Dataset Analyses

### 1.1 MIRACL (Multilingual Information Retrieval Across a Continuum of Languages)
*Based on the provided `MIRACL.pdf`.*

#### A. Basic Information
*   **Year Released:** 2022/2023 (WSDM Cup)
*   **Source:** University of Waterloo, Huawei Noah’s Ark Lab, et al.
*   **Availability:** Open-source (Apache 2.0).
*   **Language Coverage:** 18 languages, including **Arabic (ar)**.

#### B. Size & Scale Metrics (Arabic Subset)
*   **Number of Queries:** ~8,700 (Train: 3,495, Dev: 2,896, Test-A: 936, Test-B: 1,405).
*   **Number of Judgments:** ~68,000 (relevance judgments).
*   **Corpus Size:** ~2 million passages (from 656k Arabic Wikipedia articles).
*   **Avg. Query Length:** 5.8 tokens (based on TyDi stats, as it builds on it).

#### C. Task & Domain Characteristics
*   **Primary Task:** Ad-hoc Retrieval (Ranking).
*   **Domain:** Wikipedia (Open-domain).
*   **Annotation Quality:** High. Native speakers (not crowd-workers, hired annotators). Explicit relevance judgments (graded).

#### D. Linguistic Properties
*   **Language Variety:** MSA (Modern Standard Arabic).
*   **Query Naturalness:** **High.** Queries are written by native speakers prompted by valid information needs, *before* seeing the answer.
*   **Vocabulary Coverage:** General encyclopedic.

#### E. Retrieval-Specific Properties
*   **Retrieval Challenge Level:** **High.** Explicitly designed to handle the "typo-logical diversity" gap.
*   **Gold Passage Annotations:** Yes, robust qrels (query-relevance files).
*   **Negative Samples:** Yes, includes hard negatives (passages that look relevant but aren't).
*   **Query-Document Mismatch:** Natural mismatch arising from native phrasing vs. encyclopedic text.

---

### 1.2 TyDi QA (Arabic Subset)
*Based on the provided `TyDi QA.pdf`.*

#### A. Basic Information
*   **Year Released:** 2020
*   **Source:** Google Research.
*   **Availability:** Open-source.
*   **Language Coverage:** 11 languages, including **Arabic**.

#### B. Size & Scale Metrics (Arabic Subset)
*   **Number of QA Pairs:** ~23,000 (Train) + ~1,300 (Dev).
*   **Corpus:** Wikipedia snapshots.
*   **Avg. Query Length:** ~5.8 tokens.

#### C. Task & Domain Characteristics
*   **Primary Task:** Question Answering (Passage Selection & Minimal Span Extraction).
*   **Domain:** Wikipedia.
*   **Annotation Quality:** High. Native speakers write questions without seeing the answer first (Information-Seeking).

#### D. Linguistic Properties
*   **Language Variety:** MSA.
*   **Query Naturalness:** **Very High.** Avoids "priming" effects (where users copy words from the text).
*   **Vocabulary Coverage:** Diverse typological phenomena (morphology, etc.).

#### E. Retrieval-Specific Properties
*   **Retrieval Challenge:** Medium-High.
*   **Gold Passage Annotations:** Yes.
*   **Corpus Type:** Open-domain.
*   **Query-Document Mismatch:** High morphological variation (e.g., root-pattern system, attached prepositions) creates lexical mismatch.

---

### 1.3 ArabicaQA
*Based on the provided `ArabicaQA.pdf`.*

#### A. Basic Information
*   **Year Released:** 2024
*   **Source:** University of Innsbruck, Assuit University, DISCO AI.
*   **Availability:** Publicly accessible (GitHub).
*   **Language Coverage:** Arabic (MSA).

#### B. Size & Scale Metrics
*   **Number of QA Pairs:** **89,095** (MRC & Open-Domain).
*   **Number of Unanswerable:** 3,701.
*   **Corpus:** Arabic Wikipedia (~4 million articles indexed).

#### C. Task & Domain Characteristics
*   **Primary Task:** Machine Reading Comprehension (MRC) and Open-Domain QA (ODQA).
*   **Domain:** Wikipedia.
*   **Answer Type:** Concise (52k) and Elaborate (39k).
*   **Annotation Quality:** Crowd-sourced, validated by experts.

#### D. Linguistic Properties
*   **Language Variety:** MSA.
*   **Query Naturalness:** Moderate/High (Crowd-workers instructed to reformulate and use synonyms).
*   **Vocabulary Coverage:** Broad.

#### E. Retrieval-Specific Properties
*   **Retrieval Challenge:** Hard. (Training set split into ~27k "Easy" and ~34k "Difficult" based on retrieval rank).
*   **Gold Passage Annotations:** Yes.
*   **Negative Samples:** Includes unanswerable questions (good for thresholding).
*   **Query-Document Mismatch:** Explicitly introduces synonyms and sentence structure variations.

---

### 1.4 MultiNativQA
*Based on the provided `MultiNativQA.pdf`.*

#### A. Basic Information
*   **Year Released:** 2024/2025 (ArXiv preprint).
*   **Source:** Qatar Computing Research Institute (QCRI), et al.
*   **Availability:** Publicly available (HuggingFace).
*   **Language Coverage:** 7 languages, 9 regions (Includes Arabic-Doha).

#### B. Size & Scale Metrics
*   **Total QA Pairs:** ~64k (12,311 Arabic).
*   **Seed Queries:** Manually collected + synthesized.
*   **Corpus:** Web-based (Open).

#### C. Task & Domain Characteristics
*   **Primary Task:** QA / Cultural Benchmarking.
*   **Domain:** Open Web (Everyday topics: Food, Tradition, Travel).
*   **Annotation Quality:** High. Native speakers from specific regions.

#### D. Linguistic Properties
*   **Language Variety:** **MSA + Dialects.** Specifically captures regional nuances (e.g., Arabic-Doha).
*   **Query Naturalness:** **Extreme.** Derived from "People also ask" and native user intent.
*   **Vocabulary Coverage:** Cultural and region-specific entities.

#### E. Retrieval-Specific Properties
*   **Retrieval Challenge:** High (Cultural nuance gap).
*   **Corpus Type:** Open Web (requires cleaning/indexing).
*   **Query-Document Mismatch:** **Cultural Mismatch.** Queries may use local terms not present in global Wikipedia-style documents.

---

### 1.5 Mintaka
*Based on the provided `Mintaka.pdf`.*

#### A. Basic Information
*   **Year Released:** 2022
*   **Source:** Amazon Alexa AI.
*   **Availability:** Public (GitHub).
*   **Language Coverage:** 9 languages (Includes Arabic).

#### B. Size & Scale Metrics
*   **Number of QA Pairs:** 20,000 (Total).
*   **Complexity:** 8 types (Superlative, Intersection, Multi-hop).

#### C. Task & Domain Characteristics
*   **Primary Task:** Complex QA (End-to-End).
*   **Domain:** Wikidata / Wikipedia.
*   **Query Complexity:** **High (Complex/Multi-hop).**
*   **Annotation Quality:** Elicited in English, translated by professionals to Arabic.

#### D. Linguistic Properties
*   **Language Variety:** MSA (Translated).
*   **Query Naturalness:** Moderate (Translationese risk, though professional).
*   **Vocabulary Coverage:** Complex reasoning terms.

#### E. Retrieval-Specific Properties
*   **Retrieval Challenge:** **Very High.** Requires multi-hop retrieval or decomposition.
*   **Query-Document Mismatch:** Structural mismatch (query requires logic A + B, document has only A or B).

---

### 1.6 ACQAD (Arabic Complex Question Answering Dataset)
*Based on `ArQuAD.md` content (ACQAD section).*

#### A. Basic Information
*   **Year Released:** 2023
*   **Source:** Ecole Militaire Polytechnique, Algeria.
*   **Language Coverage:** Arabic.

#### B. Size & Scale Metrics
*   **Number of Questions:** 118,000+.
*   **Generation:** **Synthetic/Template-based.**

#### C. Task & Domain Characteristics
*   **Primary Task:** Complex QA (Comparison, Multi-hop).
*   **Query Complexity:** High (conceptually).
*   **Annotation Quality:** Low/Synthetic (Generated via templates from Wikipedia Infoboxes).

#### D. Linguistic Properties
*   **Query Naturalness:** **Low.** Template-based generation usually results in rigid, unnatural phrasing.

#### E. Retrieval-Specific Properties
*   **Suitability for QE:** Low. Because queries are generated from the data, the mismatch is artificial.

---

### 1.7 ARCD (Arabic Reading Comprehension Dataset)
*Based on `Neural Arabic Question Answering.pdf`.*

#### A. Basic Information
*   **Year Released:** 2019
*   **Source:** American University of Beirut (AUB).
*   **Language Coverage:** Arabic.

#### B. Size & Scale Metrics
*   **Number of Questions:** 1,395.
*   **Domain:** Wikipedia.

#### C. Task & Domain Characteristics
*   **Primary Task:** Machine Reading Comprehension.
*   **Annotation Quality:** Crowd-sourced (Amazon Turk).

#### D. Linguistic Properties
*   **Language Variety:** MSA.
*   **Query Naturalness:** Medium. Workers encouraged to use own words.

#### E. Retrieval-Specific Properties
*   **Retrieval Challenge:** Low (Small scale).
*   **Use Case:** Validation/Testing only.

---

## 2. Comparison Matrix

| Dataset          | Size (Arabic Queries) | Language Variety | Query Origin             | Primary Challenge      | Annotation Quality | Suitability for QE |
| :--------------- | :-------------------- | :--------------- | :----------------------- | :--------------------- | :----------------- | :----------------- |
| **MIRACL**       | ~8,700                | MSA              | Native (Ad-hoc)          | Retrieval Recall       | ★★★★★              | ★★★★★              |
| **ArabicaQA**    | ~89,000               | MSA              | Crowd (Paraphrased)      | Scale / Ambiguity      | ★★★★☆              | ★★★★★              |
| **TyDi QA**      | ~23,000               | MSA              | Native (Info-seeking)    | Typology / Morphology  | ★★★★★              | ★★★★☆              |
| **MultiNativQA** | ~12,000               | MSA + Dialect    | Native (Search/Cultural) | Cultural / Dialect Gap | ★★★★☆              | ★★★★☆              |
| **Mintaka**      | ~20,000 (Total)       | MSA (Trans)      | Translated               | Reasoning / Multi-hop  | ★★★☆☆              | ★★★☆☆              |
| **ARCD**         | 1,395                 | MSA              | Crowd                    | Basic Matching         | ★★★☆☆              | ★★☆☆☆              |
| **Arabic-SQuAD** | ~48,000               | MSA (Auto)       | Machine Translation      | Noise / Translationese | ★☆☆☆☆              | ★☆☆☆☆              |
| **ACQAD**        | 118,000               | MSA (Synth)      | Template Generated       | Synthetic Structure    | ★★☆☆☆              | ★☆☆☆☆              |
| **AAFAQ**        | 5,009                 | MSA              | Classified               | Categorization         | ★★★★☆              | ★★☆☆☆              |

---

## 3. Suitability Scores (1-5) for Query Enhancement Research

1.  **MIRACL:** **5/5** (The industry standard for retrieval; explicit relevance judgments; native queries).
2.  **ArabicaQA:** **5/5** (Massive scale; specifically labels "Hard" vs "Easy" retrieval questions).
3.  **MultiNativQA:** **4/5** (Excellent for testing QE on cultural/dialectal queries, but corpus requires web indexing).
4.  **TyDi QA:** **4/5** (Great natural queries, but MIRACL improves upon its retrieval setup).
5.  **Mintaka:** **3/5** (Good for *Query Decomposition* specifically, but translationese issues).
6.  **ACQAD/ArSQuAD:** **1/5** (Synthetic or Translated data introduces artificial patterns that QE shouldn't overfit to).

---

## 4. Recommendations

### Primary Dataset Recommendation

**Dataset Name:** **MIRACL (Arabic Subset)**

**Justification:**
MIRACL (Multilingual Information Retrieval Across a Continuum of Languages) is the scientifically most robust choice for a graduation project focusing on *retrieval recall*. It was explicitly built to address the flaws in previous datasets (like TyDi QA) regarding passage segmentation and relevance judgments.

**Strengths for this research:**
*   **Gold-Standard Retrieval Signal:** Unlike MRC datasets (SQuAD-style) where retrieval is secondary, MIRACL focuses purely on the ad-hoc retrieval task.
*   **Hard Negatives:** It includes "hard negatives" (passages that share keywords but don't answer the query). This is the *perfect* test bed for Query Enhancement—can the enhanced query distinguish the true answer from the distractor?
*   **Native Formulation:** Queries are written by native Arabic speakers, ensuring the "mismatch" is linguistic and natural, not a translation artifact.
*   **Manageable Size:** ~3.5k training queries is efficient for a student project with limited compute, while the corpus (Wikipedia) is standard.

**Limitations:**
*   Focuses primarily on Wikipedia (MSA), so it won't fully test dialectal query enhancement unless supplemented.

**Preprocessing:**
*   Requires indexing the provided Arabic Wikipedia dump (Pyserini/Anserini is recommended in the paper).

---

### Secondary Datasets

**Option 1: ArabicaQA (for Scale & Difficulty Analysis)**
*   **Why:** It offers nearly 90k queries, significantly more than MIRACL. Crucially, it categorizes questions into **"Easy" vs. "Difficult"** retrieval (based on BM25 rank).
*   **Role in Research:** Use the "Difficult" subset of ArabicaQA to specifically test if Query Enhancement improves recall where standard keyword search fails. This proves the *utility* of the QE technique.

**Option 2: MultiNativQA (for Cultural/Dialectal Robustness)**
*   **Why:** It contains questions derived from "People also ask" and specific regional contexts (e.g., Doha).
*   **Role in Research:** Use this to test **Query Rewriting/Correction**. Can the QE module translate a user's dialectal/informal query into the formal MSA required to retrieve documents from a standard corpus? This validates the "Query Correction" hypothesis.

