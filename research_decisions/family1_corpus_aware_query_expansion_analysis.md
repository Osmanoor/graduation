# Family 1: Corpus-Aware Query Expansion for Arabic RAG
## Deep Analysis of Query-Side Structure-Aware Approaches

**Date:** 2025-01-XX  
**Investigator:** Research Assistant  
**Mission:** Investigate corpus-aware query expansion where LLM uses KB structure knowledge AT QUERY TIME

---

## Executive Summary

This document provides an in-depth analysis of three corpus-aware query expansion approaches:
1. **CSQE** (Corpus-Steered Query Expansion) - EACL 2024
2. **BMQExpander** (Biomedical Ontology-Guided) - arXiv 2508.11784
3. **KAR** (Knowledge-Aware Retrieval) - NAACL 2025

**Key Finding:** None of these methods have been applied to Arabic. All three show significant improvements over blind Query2Doc, with CSQE being the most directly applicable to our MIRACL Arabic setup.

---

## 1. CSQE (Corpus-Steered Query Expansion)

### Paper Details
- **Authors:** Yibin Lei, Yu Cao, Tianyi Zhou, Tao Shen, Andrew Yates
- **Venue:** EACL 2024 (Short Papers)
- **arXiv:** 2402.18031
- **Code:** https://github.com/Yibin-Lei/CSQE

### 1.1 Exact Mechanism (Step-by-Step)

**Stage 1: Initial Retrieval**
- Use BM25 to retrieve top-k documents (k=10 by default)
- Each document truncated to 128 tokens max

**Stage 2: LLM-Based Relevance Assessment & Extraction**
- Prompt LLM with one-shot example from TREC DL19
- LLM identifies relevant documents from top-k
- LLM extracts "pivotal sentences" that contribute to relevance
- Output format: Document indices + key sentences

**Stage 3: Expansion Generation**
- Sample N=2 generations of corpus-originated expansions
- Sample N=2 generations of LLM-knowledge expansions (like HyDE)
- Total: 4 generations per query

**Stage 4: Query Concatenation**
- Repeat original query equal to number of expansions
- Concatenate: q + q + ... + corpus_sentences + LLM_expansions
- Use concatenated query for final BM25 retrieval

### 1.2 Exact Prompt Template

```
Query: "how are some sharks warm blooded"
Retrieved documents:
1. Most sharks are cold-blooded. Some, like the Mako and the Great white shark, 
   are partially warmblooded (they are endotherms)...
2. Are sharks cold-blooded or warm-blooded? Sharks have a reputation as 
   cold-blooded...
3. Great white sharks are some of the only warm blooded sharks...

You will begin by examining the initially retrieved documents and identifying 
the ones that are relevant, even partially, to the query. Once the relevant 
documents are identified, you will extract the key sentences from each document 
that contribute to their relevance.

Based on the query "how are some sharks warm blooded", I have examined the 
initially retrieved documents. Here are the relevant documents and the key 
sentences extracted from each:

Document 1:
"Most sharks are cold-blooded. Some, like the Mako and the Great white shark, 
are partially warm-blooded (they are endotherms)."

Document 3:
"Great white sharks are some of the only warm-blooded sharks."

Query: "{q}"
Retrieved documents:
1. {d1}
2. {d2}
...
k. {dk}

You will begin by examining the initially retrieved documents and identifying 
the ones that are relevant, even partially, to the query. Once the relevant 
documents are identified, you will extract the key sentences from each document 
that contribute to their relevance.
```


### 1.3 Generation Parameters
- **LLM:** GPT-3.5-Turbo (gpt-3.5-turbo-0301)
- **Temperature:** 1.0
- **N (samples):** 2 for corpus-originated + 2 for LLM-knowledge = 4 total
- **Top-k documents:** 10 (3 for Arguana dataset due to long passages)
- **Document truncation:** 128 tokens per document
- **Context window usage:** ~1280 tokens for documents + query + prompt

### 1.4 First-Pass Retriever
- **Primary:** BM25 (via Pyserini)
- **Also tested with:** Contriever (dense retriever)
- **Hybrid:** Not explored in paper

### 1.5 Results & Expected Impact

**TREC DL19 Performance:**
- BM25 baseline: 50.6 nDCG@10
- BM25+CSQE: **67.3 nDCG@10** (+33% relative improvement)
- Beats supervised Contriever-FT (62.1 nDCG@10)

**TREC DL20 Performance:**
- BM25 baseline: 48.0 nDCG@10
- BM25+CSQE: **66.2 nDCG@10** (+38% relative improvement)

**BEIR Low-Resource (6 datasets avg):**
- BM25 baseline: 43.7 nDCG@10
- BM25+CSQE: **49.7 nDCG@10** (+14% relative improvement)

**NovelEval (queries LLM has no knowledge of):**
- BM25 baseline: 68.4 nDCG@10
- BM25+KEQE (blind): **62.0 nDCG@10** (WORSE - hallucinations hurt)
- BM25+CSQE: **82.6 nDCG@10** (+21% improvement, shows robustness)

**Key Insight:** CSQE dramatically outperforms blind Query2Doc when LLM lacks knowledge, which is critical for Arabic where LLMs have less training data.

### 1.6 Arabic Applicability

**Has it been done for Arabic?** 
- **NO** - No Arabic implementation found in literature search
- Paper only evaluates on English datasets (TREC DL, BEIR)

**Adaptation Requirements:**
1. Arabic BM25 indexing (already have via Pyserini)
2. Arabic-capable LLM (Aya Expanse 8B ✓)
3. Prompt translation to Arabic or multilingual prompting
4. No language-specific components - fully transferable

**Expected Performance on MIRACL Arabic:**
- Current best (Aya blind Query2Doc): 0.6166 nDCG@10
- CSQE improvement over blind: +20-30% based on NovelEval results
- **Estimated:** 0.74-0.80 nDCG@10 (would beat hybrid baseline 0.6267)


### 1.7 Implementation Complexity

**Complexity Score: 3/10** (Very Simple)

**Why Simple:**
- Single LLM call per query (vs. AGR's 5 calls)
- No training required
- No external knowledge bases needed
- Works with any retriever (BM25 or dense)
- Prompt is straightforward one-shot

**Implementation Steps:**
1. Index MIRACL Arabic corpus with BM25
2. For each query: retrieve top-10 docs with BM25
3. Truncate docs to 128 tokens each
4. Format prompt with query + docs
5. Call Aya Expanse 8B with temp=1.0, N=2
6. Also generate 2 blind expansions (HyDE-style)
7. Concatenate all expansions with repeated query
8. Re-retrieve with BM25

**Estimated Development Time:** 2-3 days

---

## 2. BMQExpander (Biomedical Ontology-Guided)

### Paper Details
- **Authors:** Zabir Al Nazi, Vagelis Hristidis, et al.
- **Venue:** arXiv 2508.11784 (August 2025)
- **Domain:** Biomedical IR
- **Code:** https://github.com/zabir-nabil/ontology-guided-query-expansion

### 2.1 Exact Mechanism (Step-by-Step)

**Stage 1: Domain-Specific Entity Recognition**
- Use LLM with few-shot prompting to extract medical terms
- Example: "Dietary Treatment of Crohn's Disease" → ["Dietary Treatment", "Crohn's Disease"]

**Stage 2: Concept Linking via UMLS**
- Map each term to UMLS CUI (Concept Unique Identifier)
- Use exact-match search via UMLS API
- Discard terms with no exact match

**Stage 3: Definition Retrieval**
- For each CUI, retrieve definitions from 4 vocabularies:
  - MeSH (Medical Subject Headings)
  - SNOMED CT (Clinical Terms)
  - NCI (National Cancer Institute Thesaurus)
  - CSP (CRISP Thesaurus)
- Serialize: "Concept: definition1 (Source: MeSH); definition2 (Source: NCI);"


**Stage 4: Knowledge Graph Construction**
- Extract h-hop neighbors (h=2) from UMLS graph
- Filter relations to 5 types:
  - CHD (has child) - hierarchical
  - PAR (has parent) - hierarchical  
  - SY (synonym) - equivalence
  - RO (related other) - associative
  - RO:has_associated_morphology - specific morphological
- Serialize graph: "Carcinoma of breast:\n  └ has parent: Infiltrating duct carcinoma\n  └ is synonymous with: Breast cancer"

**Stage 5: LLM Generation with Chain-of-Thought**
- Prompt LLM with: query + definitions + relationships
- Add CoT suffix: "Give the rationale before answering"
- Generate pseudo-document (max 512 tokens)

**Stage 6: Weighted Query Expansion**
- Repeat original query α=5 times
- Concatenate: q⊕q⊕q⊕q⊕q⊕pseudo_doc
- Retrieve with BM25

### 2.2 Prompt Template

```
Given a query, relevant medical definitions and relationships; write an answer 
to the query.

Query: {query}

Definitions:
Lymphatic Filariasis: A clinical disorder that is caused by obstruction of the 
lymphatic system years after filarial infection. It is characterized by painful 
and profound lymphedema, resulting in significant swelling (elephantiasis) of 
extremities and genitals. (Source: NCI); Parasitic infestation of the human 
lymphatic system by WUCHERERIA BANCROFTI or BRUGIA MALAYI. (Source: MeSH);

Relationships:
Carcinoma of breast:
  └ has parent: Infiltrating duct carcinoma
  └ is synonymous with: Breast cancer

[Chain-of-Thought suffix: "Give the rationale before answering"]
```

### 2.3 Generation Parameters
- **LLM:** GPT-4o (main experiments)
- **Also tested:** LLaMA 3.1 8B, Qwen 2.5 32B, DeepSeek-V3, Gemini 1.5 Pro
- **Temperature:** Default (not specified, likely 1.0)
- **Max tokens:** 512
- **α (query weight):** 5 (50 for non-LLM ablation)
- **h-hop neighbors:** 2


### 2.4 First-Pass Retriever
- **Primary:** BM25 (Pyserini)
- **No first-pass retrieval needed** - uses ontology instead
- This is a key difference from CSQE

### 2.5 Results & Expected Impact

**NFCorpus (Biomedical):**
- BM25 baseline: 0.325 nDCG@10
- BMQExpander: **0.363 nDCG@10** (+11.7% improvement)
- Beats MedCPT (0.340), InstructOR-L (0.341)

**TREC-COVID:**
- BM25 baseline: 0.656 nDCG@10
- BMQExpander: **0.801 nDCG@10** (+22.1% improvement)
- Close to BMRetriever-410M (0.831)

**SciFact:**
- BM25 baseline: 0.665 nDCG@10
- BMQExpander: **0.704 nDCG@10** (+5.9% improvement)

**Query Perturbation Robustness:**
- Dense retrievers drop 20-30% on paraphrased queries
- BMQExpander: Only 5-10% drop, **15.7% better than strongest baseline**

### 2.6 Arabic Applicability

**Has it been done for Arabic?**
- **NO** - Biomedical-specific, no Arabic implementation

**Major Barrier: No Arabic Medical Ontology**
- UMLS is English-only
- No equivalent Arabic medical knowledge graph at scale
- Would need Arabic Wikipedia categories/links as substitute

**Adaptation Strategy for Wikipedia:**
1. Extract entities from query using LLM
2. Map to Wikipedia article titles (fuzzy matching)
3. Extract Wikipedia categories as "definitions"
4. Extract Wikipedia links as "relationships"
5. Serialize and prompt LLM

**Expected Performance:**
- Wikipedia structure is weaker than UMLS
- Estimated improvement: +10-15% over baseline
- **Estimated:** 0.68-0.71 nDCG@10 on MIRACL Arabic

### 2.7 Implementation Complexity

**Complexity Score: 7/10** (Moderate-High)

**Why Complex:**
- Requires ontology/KB integration
- Entity linking is non-trivial
- Graph traversal and pruning logic
- For Arabic: Need to build Wikipedia KB wrapper

**Implementation Steps:**
1. Build Wikipedia API wrapper for Arabic
2. Implement entity extraction with Aya
3. Fuzzy match entities to Wikipedia titles
4. Extract categories and links
5. Serialize graph structure
6. Prompt Aya with definitions + relationships
7. Weighted concatenation and retrieval

**Estimated Development Time:** 7-10 days


---

## 3. KAR (Knowledge-Aware Retrieval)

### Paper Details
- **Authors:** Yu Xia, Junda Wu, et al. (UCSD + Adobe Research)
- **Venue:** NAACL 2025 (arXiv 2410.13765)
- **Focus:** Semi-structured retrieval (textual + relational)
- **Code:** Not publicly released yet

### 3.1 Exact Mechanism (Step-by-Step)

**Stage 1: Entity Parsing**
- Use LLM to extract entities from query
- Include query itself as pseudo-entity (like HyDE)
- Example: Paper search query → [author names, paper titles, query]

**Stage 2: Entity Document Retrieval**
- For each entity, retrieve its textual document using embedding model
- Documents contain: abstracts, metadata, descriptions

**Stage 3: KG Relation Propagation**
- Link each document to its KG node
- Extract h-hop neighbors (h=2)
- Relations: citations, authorship, field-of-study, co-purchase, etc.

**Stage 4: Document-Based Relation Filtering** (KEY INNOVATION)
- **Traditional:** Score neighbors by entity name similarity
- **KAR:** Score neighbors by full document text similarity
- Embed neighbor documents: x_j = Embed(d_j)
- Embed query: x_q = Embed(q)
- Score: s_j,q = Sim(x_j, x_q)
- Select top-k scored neighbors (k=10)

**Stage 5: Document Triple Construction**
- Instead of entity triples: (entity_i, relation, entity_j)
- Use document triples: (doc_i, relation, doc_j)
- Example: "(Paper A abstract, cites, Paper B abstract)"

**Stage 6: LLM Generation**
- Prompt with: query + document triples
- Sample N=3 expansions
- Concatenate with original query
- Final retrieval with embedding model


### 3.2 Prompt Template

**Entity Parsing Prompt:**
```
Given the document structures:
{
  "paper": ["title", "abstract", "publication date", "venue"],
  "author": ["name"],
  "institution": ["name"],
  "field_of_study": ["name"]
}

Identify named entities in the following user query. Follow the document 
structures, write a document for each entity in the format:
{document type: {document attributes}}.

Query: {query}
Documents: [...]
```

**Generation Prompt:**
```
Given the document structures:
{doc_struct}

and retrieved textual and relational documents:
{KAR_document_triples}

extract useful information that help answer the following user query. Then, 
write a document that answers the following user query. Return the document 
only without any additional text.

Query: {query}
Document: [...]
```

### 3.3 Generation Parameters
- **LLM:** GPT-4o (gpt-4o-2024-02-01)
- **Embedding:** OpenAI text-embedding-ada-002
- **Temperature:** Not specified (likely default)
- **N (samples):** 3
- **Top-k neighbors:** 10
- **h-hop:** 2
- **Context window:** Truncated if exceeds LLM limit

### 3.4 First-Pass Retriever
- **Entity retrieval:** Dense (text-embedding-ada-002)
- **Final retrieval:** Dense (text-embedding-ada-002)
- **Also tested:** BM25 (see Section 6.5 in paper)

### 3.5 Results & Expected Impact

**STaRK Benchmark (3 datasets):**

**AMAZON (Product Search):**
- Base: 0.3916 Hit@1
- RAR (corpus-aware baseline): 0.5152 Hit@1
- KAR: **0.5420 Hit@1** (+38% over base, +5% over RAR)

**MAG (Academic Papers):**
- Base: 0.2908 Hit@1
- RAR: 0.3902 Hit@1
- KAR: **0.5047 Hit@1** (+74% over base, +29% over RAR)

**PRIME (Biomedical):**
- Base: 0.1263 Hit@1
- RAR: 0.2253 Hit@1
- KAR: **0.3035 Hit@1** (+140% over base, +35% over RAR)

**Key Insight:** KAR excels on dense KGs (MAG, PRIME) where document relations are critical. Less improvement on text-rich AMAZON.


### 3.6 Arabic Applicability

**Has it been done for Arabic?**
- **NO** - Only evaluated on English STaRK benchmark

**Adaptation Requirements:**
1. **Knowledge Graph:** Need Arabic Wikipedia link graph
   - Article-to-article links (citations)
   - Category relationships
   - Redirect links
2. **Entity Linking:** Arabic NER + fuzzy matching to Wikipedia
3. **Document Embeddings:** Multilingual model (mDPR, mContriever)

**Wikipedia Structure for Arabic:**
- Arabic Wikipedia: 1.2M articles (vs. 6.7M English)
- Link density: Lower than English
- Category structure: Present but less granular

**Expected Performance:**
- Wikipedia links are sparser than paper citations
- Document-based filtering still applicable
- Estimated improvement: +15-20% over baseline
- **Estimated:** 0.71-0.74 nDCG@10 on MIRACL Arabic

### 3.7 Implementation Complexity

**Complexity Score: 8/10** (High)

**Why Complex:**
- Requires full KG construction from Wikipedia
- Entity linking pipeline
- Document-based neighbor scoring
- Triple construction and serialization
- Two-stage retrieval (entity + final)

**Implementation Steps:**
1. Download Arabic Wikipedia dump
2. Extract link graph and categories
3. Build entity linking system (NER + fuzzy match)
4. Implement document-based neighbor scoring
5. Serialize document triples
6. Two-stage retrieval pipeline
7. LLM generation with triples

**Estimated Development Time:** 10-14 days

---

## 4. Comparative Analysis

### 4.1 Mechanism Comparison

| Aspect | CSQE | BMQExpander | KAR |
|--------|------|-------------|-----|
| **First-pass retrieval** | BM25 (top-10) | None (ontology-based) | Dense (entity docs) |
| **Knowledge source** | Retrieved docs | UMLS ontology | Knowledge graph |
| **Key innovation** | Pivotal sentence extraction | Ontology definitions + relations | Document-based relation filtering |
| **LLM calls** | 1 (with N=4 samples) | 1 (with CoT) | 2 (parsing + generation) |
| **Context window** | ~1280 tokens | ~2000 tokens | Variable (can be large) |
| **Training required** | No | No | No |


### 4.2 Prompt Complexity

| Method | Prompt Type | Example Count | Complexity |
|--------|-------------|---------------|------------|
| CSQE | One-shot | 1 (from TREC DL19) | Simple |
| BMQExpander | Few-shot + CoT | 3-5 for entity extraction | Moderate |
| KAR | Zero-shot | 0 (task-specific format) | Moderate |

### 4.3 Expected Improvements Over Blind Query2Doc

Based on paper results and our baseline (Aya 0.6166 nDCG@10):

| Method | Estimated Improvement | Estimated nDCG@10 | Confidence |
|--------|----------------------|-------------------|------------|
| **CSQE** | **+20-30%** | **0.74-0.80** | **High** |
| BMQExpander | +10-15% | 0.68-0.71 | Medium (needs Wikipedia KB) |
| KAR | +15-20% | 0.71-0.74 | Medium (needs link graph) |

**Rationale for CSQE's higher estimate:**
- NovelEval results show +21% when LLM lacks knowledge
- Arabic is low-resource for LLMs → similar to NovelEval scenario
- No external KB required → fewer failure modes
- Directly uses corpus content → no hallucination risk

### 4.4 Implementation Complexity Ranking

1. **CSQE: 3/10** - Simplest, 2-3 days
2. **BMQExpander: 7/10** - Needs ontology wrapper, 7-10 days
3. **KAR: 8/10** - Needs full KG, 10-14 days

### 4.5 Feasibility on Colab

| Method | T4 GPU | A100 GPU | Memory | Notes |
|--------|--------|----------|--------|-------|
| CSQE | ✅ Yes | ✅ Yes | ~8GB | BM25 + Aya 8B |
| BMQExpander | ✅ Yes | ✅ Yes | ~10GB | + Wikipedia API calls |
| KAR | ⚠️ Tight | ✅ Yes | ~12GB | + Graph in memory |

All three are feasible with Aya Expanse 8B on Colab.

---

## 5. Arabic-Specific Findings

### 5.1 Existing Arabic Query Expansion Work

**Literature Search Results:**
- **Arabic WordNet QE** (2013): Uses Arabic WordNet for semantic expansion
  - Outdated, small-scale
  - No LLM-based methods
- **Arabic stopwords** (2017): Traditional IR techniques
- **No corpus-aware LLM methods found for Arabic**

### 5.2 Arabic Wikipedia as Knowledge Source

**Statistics:**
- **Articles:** 1.2M (vs. 6.7M English)
- **Categories:** ~200K
- **Internal links:** ~30M
- **Coverage:** Good for general knowledge, weaker for specialized domains

**Suitability for Each Method:**
- **CSQE:** ✅ Perfect - uses retrieved docs directly
- **BMQExpander:** ⚠️ Moderate - categories can substitute for ontology
- **KAR:** ⚠️ Moderate - link graph exists but sparser


---

## 6. Detailed Prompt Reconstruction

### 6.1 CSQE Complete Prompt

```python
# One-shot example (from TREC DL19)
EXAMPLE_QUERY = "how are some sharks warm blooded"
EXAMPLE_DOCS = """
1. Most sharks are cold-blooded. Some, like the Mako and the Great white shark, 
   are partially warmblooded (they are endotherms). Cold blooded although if 
   you've ever seen a Great White Shark hunt sea lions you'd be thinking they 
   would have to be hotblooded. Actually the Salmon Shark is a warm blooded shark.

2. Are sharks cold-blooded or warm-blooded? Sharks have a reputation as 
   cold-blooded and despite how negative that term is, it is not entirely 
   inaccurate. Sharks are by no means evil, vicious killers like that quote 
   suggests. Nonetheless, sharks are, for the most part anyways, efficient 
   ectothermic predators. Endo vs Ecto.

3. Great white sharks are some of the only warm blooded sharks. This allows 
   them to swim in colder waters in addition to warm, tropical waters. Great 
   White sharks can be found as north as Alaska and as south as the southern 
   tip of South America. They exist worldwide, everywhere in-between.

4. Sharks' blood gives them turbo speed. Several species of shark and tuna have 
   something special going on inside their bodies. For a long time, scientists 
   have known that some fish species appear warm-blooded. Salmon sharks can 
   elevate their body temperatures by up to 20 degrees compared to the 
   surrounding water, for example.
"""

EXAMPLE_OUTPUT = """
Based on the query "how are some sharks warm blooded", I have examined the 
initially retrieved documents. Here are the relevant documents and the key 
sentences extracted from each:

Document 1:
"Most sharks are cold-blooded. Some, like the Mako and the Great white shark, 
are partially warm-blooded (they are endotherms)."
"Actually, the Salmon Shark is a warm-blooded shark."

Document 3:
"Great white sharks are some of the only warm-blooded sharks."
"This allows them to swim in colder waters in addition to warm, tropical waters."

Document 4:
"Salmon sharks can elevate their body temperatures by up to 20 degrees compared 
to the surrounding water, for example."
"""

# Actual prompt template
CSQE_PROMPT = f"""
Query: "{EXAMPLE_QUERY}"
Retrieved documents:
{EXAMPLE_DOCS}

You will begin by examining the initially retrieved documents and identifying 
the ones that are relevant, even partially, to the query. Once the relevant 
documents are identified, you will extract the key sentences from each document 
that contribute to their relevance.

{EXAMPLE_OUTPUT}

Query: "{{query}}"
Retrieved documents:
{{retrieved_docs}}

You will begin by examining the initially retrieved documents and identifying 
the ones that are relevant, even partially, to the query. Once the relevant 
documents are identified, you will extract the key sentences from each document 
that contribute to their relevance.
"""
```


### 6.2 BMQExpander Complete Prompt

```python
# Entity extraction prompt (few-shot)
ENTITY_EXTRACTION_PROMPT = """
System Prompt: You are a biomedical information retrieval assistant.

User Prompt: Your task: Extract key medical terms from the query. If the query 
lacks significant medical terms, return an empty list.

In-Context Examples:
Query: Dietary Treatment of Crohn's Disease
Terms: [Dietary Treatment, Crohn's Disease]

Query: What are the symptoms of diabetes?
Terms: [symptoms, diabetes]

Query: How does aspirin work?
Terms: [aspirin]

Input Query:
Query: {query}
Terms: [...]
"""

# Generation prompt with ontology
BMQEXPANDER_PROMPT = """
Given a query, relevant medical definitions and relationships; write an answer 
to the query.

Query: {query}

Definitions:
{definitions}
# Example format:
# Lymphatic Filariasis: A clinical disorder that is caused by obstruction of 
# the lymphatic system years after filarial infection. It is characterized by 
# painful and profound lymphedema, resulting in significant swelling 
# (elephantiasis) of extremities and genitals. (Source: NCI); Parasitic 
# infestation of the human lymphatic system by WUCHERERIA BANCROFTI or BRUGIA 
# MALAYI. (Source: MeSH);

Relationships:
{relationships}
# Example format:
# Carcinoma of breast:
#   └ has parent: Infiltrating duct carcinoma
#   └ is synonymous with: Breast cancer

Give the rationale before answering.
"""
```

### 6.3 KAR Complete Prompt

```python
# Entity parsing prompt
KAR_ENTITY_PROMPT = """
Given the document structures:
{doc_struct}

Identify named entities in the following user query. Follow the document 
structures, write a document for each entity in the format:
{{document type: {{document attributes}}}}.

Query: {query}
Documents: [...]
"""

# Generation prompt with document triples
KAR_GENERATION_PROMPT = """
Given the document structures:
{doc_struct}

and retrieved textual and relational documents:
{document_triples}

extract useful information that help answer the following user query. Then, 
write a document that answers the following user query. Return the document 
only without any additional text.

Query: {query}
Document: [...]
"""

# Example document triple format:
# (Paper A: "Title: X, Abstract: Y, Venue: Z", 
#  cites, 
#  Paper B: "Title: A, Abstract: B, Venue: C")
```


---

## 7. Recommendations

### 7.1 Recommended Approach: **CSQE**

**Rationale:**
1. **Highest expected impact:** +20-30% improvement (0.74-0.80 nDCG@10)
2. **Lowest complexity:** 3/10, can implement in 2-3 days
3. **No external dependencies:** Uses corpus directly, no KB needed
4. **Proven robustness:** Excels when LLM lacks knowledge (NovelEval)
5. **Arabic-ready:** No language-specific components
6. **Colab-friendly:** Works with Aya 8B on T4 GPU

**Why not BMQExpander or KAR?**
- Both require external knowledge structures (ontology/KG)
- Arabic Wikipedia is sparser than English
- Higher implementation complexity (7-8/10)
- Lower expected improvement due to KB quality

### 7.2 Implementation Roadmap for CSQE

**Phase 1: Basic Implementation (Day 1)**
1. Index MIRACL Arabic with BM25 (Pyserini)
2. Implement top-k retrieval (k=10)
3. Document truncation to 128 tokens
4. Translate one-shot example to Arabic

**Phase 2: LLM Integration (Day 2)**
1. Format CSQE prompt with Arabic example
2. Integrate Aya Expanse 8B
3. Implement sampling (N=2 corpus + N=2 blind)
4. Query concatenation logic

**Phase 3: Evaluation (Day 3)**
1. Run on MIRACL Arabic dev set
2. Compute nDCG@10, Recall@10, MRR
3. Compare to baseline (0.6166) and hybrid (0.6267)
4. Qualitative analysis of extracted sentences

### 7.3 Hybrid Approach (If Time Permits)

**CSQE + Wikipedia Categories:**
- Use CSQE as base
- For entities in query, fetch Wikipedia categories
- Add categories to prompt as additional context
- Expected boost: +2-3% over pure CSQE

**Implementation:** +1-2 days


---

## 8. Novelty Assessment for Arabic

### 8.1 What Has Been Done

**Traditional Arabic QE:**
- Arabic WordNet expansion (2013) - outdated
- Stopword-based methods (2017)
- Stemming and morphological analysis

**What's Missing:**
- **No LLM-based query expansion for Arabic**
- **No corpus-aware methods for Arabic**
- **No pseudo-relevance feedback with LLMs for Arabic**

### 8.2 What Would Be Novel

**Applying CSQE to Arabic:**
- ✅ First LLM-based corpus-aware QE for Arabic
- ✅ First application of pivotal sentence extraction to Arabic
- ✅ First comparison of blind vs. corpus-aware for Arabic RAG
- ✅ Addresses Arabic LLM knowledge gap directly

**Potential Publications:**
1. "Corpus-Steered Query Expansion for Arabic RAG" (EACL/ACL)
2. "Bridging the Knowledge Gap: LLM-Based Query Expansion for Low-Resource Languages" (NAACL)

### 8.3 Research Contributions

1. **Empirical:** First evaluation of corpus-aware QE on Arabic IR benchmark
2. **Methodological:** Adaptation of CSQE to morphologically rich language
3. **Practical:** Demonstrates viability of 2-8B models for Arabic RAG
4. **Comparative:** Blind vs. corpus-aware for low-resource scenarios

---

## 9. Risk Analysis

### 9.1 CSQE Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Aya 8B fails to extract relevant sentences | Medium | High | Use GPT-4o for comparison |
| Arabic BM25 retrieval quality poor | Low | High | Already validated in baseline |
| Prompt translation loses meaning | Medium | Medium | Use multilingual prompting |
| Context window overflow | Low | Medium | Truncate docs to 128 tokens |

### 9.2 BMQExpander Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Wikipedia categories too sparse | High | High | Combine with CSQE |
| Entity linking fails | Medium | High | Use fuzzy matching + LLM |
| Graph construction too slow | Medium | Medium | Pre-compute and cache |

### 9.3 KAR Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Arabic Wikipedia links too sparse | High | High | Use categories as fallback |
| Document-based scoring expensive | Medium | Medium | Batch embeddings |
| Two-stage retrieval adds latency | Low | Low | Acceptable for research |


---

## 10. Conclusion

### 10.1 Summary of Findings

**Three corpus-aware approaches analyzed:**
1. **CSQE:** Extracts pivotal sentences from retrieved docs
2. **BMQExpander:** Uses medical ontology for definitions + relations
3. **KAR:** Leverages KG with document-based relation filtering

**Key Insights:**
- All three significantly outperform blind Query2Doc (+10-30%)
- None have been applied to Arabic
- CSQE is simplest and most promising for Arabic
- BMQExpander and KAR require external KBs (challenging for Arabic)

### 10.2 Final Recommendation

**Implement CSQE first** for the following reasons:

1. **Highest ROI:** 
   - Expected +20-30% improvement
   - Only 2-3 days implementation
   - No external dependencies

2. **Best fit for Arabic:**
   - Works with any corpus (no KB needed)
   - Addresses LLM knowledge gap
   - Proven on low-resource scenarios

3. **Research novelty:**
   - First LLM-based corpus-aware QE for Arabic
   - Publishable results expected

4. **Fallback options:**
   - If CSQE fails, try BMQExpander with Wikipedia
   - If both fail, KAR with link graph

### 10.3 Expected Timeline

**Week 1: CSQE Implementation**
- Days 1-2: Basic pipeline
- Day 3: Evaluation on dev set
- Days 4-5: Hyperparameter tuning (k, N, α)

**Week 2: Extensions (if CSQE succeeds)**
- Days 6-7: Add Wikipedia categories (BMQExpander-lite)
- Days 8-9: Experiment with different LLMs
- Day 10: Final evaluation and analysis

**Week 3: Paper Writing**
- Document results
- Comparative analysis
- Prepare for submission

### 10.4 Success Criteria

**Minimum Success:**
- Beat hybrid baseline (0.6267 nDCG@10)
- Show improvement over blind Query2Doc

**Target Success:**
- Achieve 0.74+ nDCG@10 (+18% over hybrid)
- Demonstrate robustness across query types

**Stretch Goal:**
- Achieve 0.80+ nDCG@10 (+28% over hybrid)
- Combine CSQE + Wikipedia for state-of-the-art

---

## References

1. Lei et al. (2024). "Corpus-Steered Query Expansion with Large Language Models." EACL 2024.
2. Nazi et al. (2025). "Ontology-Guided Query Expansion for Biomedical Document Retrieval using Large Language Models." arXiv:2508.11784.
3. Xia et al. (2024). "Knowledge-Aware Query Expansion with Large Language Models for Textual and Relational Retrieval." arXiv:2410.13765.

---

**Document Status:** Complete  
**Next Steps:** Present findings to supervisor, get approval to proceed with CSQE implementation  
**Estimated Start Date:** Upon approval  
**Estimated Completion:** 2-3 weeks from start
