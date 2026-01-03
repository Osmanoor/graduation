# Technical Specifications
**Project:** Arabic RAG Query Enhancement  
**Last Updated:** 2/1/2026  
**Status:** In Planning Phase

---

## System Architecture

### Overview
```
User Query (Arabic/Dialect)
    ↓
[Query Enhancement Layer] ← Our Focus
    ↓
[Retriever: Hybrid Dense + Sparse]
    ↓
Retrieved Chunks
    ↓
[Generator: LLM] ← Deferred for now
    ↓
Final Answer
```

### Component Specifications

#### 1. Query Enhancement Layer
**Purpose:** Transform/enhance user queries before retrieval to improve recall

**Candidate Techniques:**
- **HyDE:** Generate hypothetical MSA document from query
- **Query Rewriting:** Normalize dialect → MSA
- **Query Expansion:** Add synonyms, morphological variants
- **Query Decomposition:** Break complex queries into sub-queries
- **Context Injection:** Provide knowledge base structure awareness

**Implementation Approach:**
- LLM-based (for HyDE, Rewriting, Decomposition)
- Rule-based (for Expansion, Normalization)
- Hybrid (combine multiple techniques)

**Arabic LLM Candidates:**
- Jais (Arabic-focused)
- AceGPT (Arabic-focused)
- Gemini 1.5 Pro (multilingual, good Arabic support)
- GPT-4 (multilingual, expensive)

#### 2. Retriever (Hybrid)

**Dense Retrieval:**
- **Model Candidates:**
  - BGE-m3 (multilingual, open-source)
  - Jina AI embeddings (multilingual, generous free tier)
  - Qwen multilingual embeddings
  - E5 multilingual
- **Vector Database:** Chroma, FAISS, or Pinecone
- **Similarity Metric:** Cosine similarity
- **Top-K:** 10 (for Recall@10 evaluation)

**Sparse Retrieval:**
- **Algorithm:** BM25
- **Implementation:** Lucene, Elasticsearch, or custom
- **Advantages:** 
  - Resource-friendly (no GPU needed)
  - Excellent for keyword matching
  - Complements semantic search
- **Arabic Considerations:**
  - Tokenization: Handle Arabic morphology
  - Stopwords: Arabic-specific stopword list
  - Stemming: Optional (root extraction)

**Hybrid Strategy:**
- Run both retrievers in parallel
- Combine results (weighted or ranked fusion)
- Experiment with different weighting schemes

#### 3. Generator (Deferred)
**Status:** Not implemented in Phase 1

**Future Considerations:**
- Arabic LLM selection
- Prompt engineering for Arabic
- Evaluation metrics: F1, Exact Match, Truthfulness

---

## Embedding Model Selection

### Evaluation Criteria
1. **Arabic Performance:** Benchmark scores on Arabic tasks
2. **Multilingual Support:** Can handle MSA + dialects
3. **Resource Requirements:** Cost, compute, API limits
4. **Open vs. Closed:** Open-source preferred for research
5. **Community Support:** Documentation, examples, updates

### Candidates

#### BGE-m3
- **Type:** Open-source, multilingual
- **Strengths:** Widely used, good benchmarks, free
- **Weaknesses:** May not be optimized for Arabic
- **Use Case:** Safe baseline choice

#### Jina AI
- **Type:** Closed-source API, multilingual
- **Strengths:** Surprisingly good Arabic performance, generous free quota
- **Weaknesses:** API dependency, rate limits
- **Use Case:** Good for experimentation phase

#### Qwen Multilingual
- **Type:** Open-source (check), multilingual
- **Strengths:** Recent model, good multilingual support
- **Weaknesses:** Less community adoption
- **Use Case:** Alternative to BGE-m3

#### E5 Multilingual
- **Type:** Open-source, multilingual
- **Strengths:** Good benchmarks
- **Weaknesses:** Similar to BGE-m3
- **Use Case:** Comparison baseline

### Selection Process
1. Review Arabic NLP benchmarks (MIRACL leaderboard)
2. Test top 2-3 models on sample MIRACL queries
3. Measure: Recall@10, NDCG@10, inference time, cost
4. Select primary model for Checkpoint 1
5. Test others in Checkpoint 3 (model generalization)

---

## Dataset Specifications

### Primary: MIRACL (Arabic)

**Structure:**
```
miracl-corpus/
├── docs.jsonl          # All documents (Wikipedia passages)
│   ├── docid
│   ├── title
│   └── text
├── topics.tsv          # Queries
│   ├── query_id
│   └── query_text
└── qrels.tsv           # Relevance judgments
    ├── query_id
    ├── docid
    ├── relevance (0-3)
    └── iteration
```

**Statistics:**
- Documents: ~2.1M Arabic Wikipedia passages
- Queries: ~2,896 (train/dev/test splits)
- Avg query length: ~8 words
- Avg document length: ~100 words
- Relevance levels: 0 (not relevant) to 3 (highly relevant)

**Preprocessing Requirements:**
1. Download Wikipedia dumps (Arabic)
2. Chunk into passages (as per MIRACL paper)
3. Index with chosen embedding model
4. Load queries and relevance judgments
5. Implement evaluation pipeline

**Gold Standard:**
- Each query has 1+ gold passages (relevance = 3)
- Hard negatives included (similar but not relevant)
- Native speaker annotations (high quality)

### Secondary: Arabic QA

**Structure:**
- 90,000+ question-answer pairs
- Difficulty labels: Hard, Easy
- Hard = answer not in BM25 top-10

**Use Case:**
- Test generalization after MIRACL experiments
- Focus on "Hard" subset for query enhancement validation

---

## Evaluation Framework

### Metrics

#### Primary (Retrieval)
1. **Recall@K (K=10)**
   - Formula: (# relevant docs in top-K) / (# total relevant docs)
   - Measures: Did we retrieve the relevant passages?
   - Target: Improve over baseline

2. **NDCG@K (K=10)**
   - Formula: Normalized Discounted Cumulative Gain
   - Measures: Did we rank relevant passages higher?
   - Target: Improve over baseline

3. **MRR (Mean Reciprocal Rank)**
   - Formula: 1 / (rank of first relevant doc)
   - Measures: How quickly do we find relevant docs?
   - Target: Improve over baseline

#### Secondary (Future)
- **Precision@K:** Relevant docs / K retrieved docs
- **F1 Score:** For generation tasks
- **Exact Match:** For generation tasks

### Evaluation Pipeline

```python
# Pseudocode
def evaluate_system(queries, qrels, retriever):
    results = []
    for query in queries:
        # Baseline
        baseline_docs = retriever.retrieve(query, k=10)
        baseline_metrics = compute_metrics(baseline_docs, qrels[query])
        
        # Enhanced
        enhanced_query = query_enhancer.enhance(query)
        enhanced_docs = retriever.retrieve(enhanced_query, k=10)
        enhanced_metrics = compute_metrics(enhanced_docs, qrels[query])
        
        # Compare
        improvement = enhanced_metrics - baseline_metrics
        results.append({
            'query': query,
            'baseline': baseline_metrics,
            'enhanced': enhanced_metrics,
            'improvement': improvement
        })
    
    return aggregate_results(results)
```

### Experiment Tracking
- **Tool:** Weights & Biases, MLflow, or custom logging
- **Track:**
  - Hyperparameters (model, technique, version)
  - Metrics (Recall@10, NDCG@10, MRR)
  - Runtime (inference time, cost)
  - Qualitative analysis (which queries improved/degraded)

---

## Implementation Roadmap

### Phase 1: Baseline Setup
**Goal:** Establish reproducible baseline

**Tasks:**
1. Set up development environment
   - Python 3.9+
   - Libraries: transformers, sentence-transformers, faiss, rank-bm25
2. Download MIRACL dataset
3. Implement data loaders
4. Implement baseline retriever (Dense + BM25)
5. Implement evaluation pipeline
6. Run baseline experiments
7. Document baseline performance

**Deliverables:**
- Baseline code (GitHub repo)
- Baseline metrics report
- Documentation

### Phase 2: Query Enhancement
**Goal:** Implement and test first technique

**Tasks:**
1. Select technique (HyDE or Query Rewriting)
2. Implement enhancement layer
3. Integrate with baseline system
4. Run experiments
5. Analyze results
6. Document findings

**Deliverables:**
- Enhanced system code
- Comparison report (baseline vs. enhanced)
- Analysis of improvements

### Phase 3: Iteration & Scaling
**Goal:** Test multiple techniques and models

**Tasks:**
1. Implement additional techniques
2. Version and compare
3. Test on different embedding models
4. Test on secondary dataset
5. Identify best configurations

**Deliverables:**
- Comprehensive comparison report
- Best-practice recommendations
- Research paper draft

---

## Resource Requirements

### Computational
- **GPU:** Recommended for embedding inference (can use CPU for BM25)
- **RAM:** 16GB+ for loading embeddings
- **Storage:** ~50GB for MIRACL corpus + embeddings
- **Cloud:** Google Colab Pro, AWS, or local GPU

### API Costs (if using closed-source)
- **Jina AI:** Generous free tier, then pay-per-use
- **OpenAI:** Expensive for large-scale experiments
- **Gemini:** Competitive pricing, good for prototyping

### Time Estimates
- Baseline setup: 1-2 weeks
- First technique implementation: 1 week
- Experiments per technique: 2-3 days
- Analysis and documentation: 1 week per checkpoint

---

## Code Structure (Proposed)

```
arabic-rag-query-enhancement/
├── data/
│   ├── miracl/              # MIRACL dataset
│   ├── arabic_qa/           # Secondary dataset
│   └── processed/           # Preprocessed data
├── src/
│   ├── retrievers/
│   │   ├── dense.py         # Dense retrieval
│   │   ├── sparse.py        # BM25
│   │   └── hybrid.py        # Hybrid retriever
│   ├── enhancers/
│   │   ├── hyde.py          # HyDE implementation
│   │   ├── rewriter.py      # Query rewriting
│   │   ├── expander.py      # Query expansion
│   │   └── decomposer.py    # Query decomposition
│   ├── evaluation/
│   │   ├── metrics.py       # Recall, NDCG, MRR
│   │   └── pipeline.py      # Evaluation pipeline
│   └── utils/
│       ├── data_loader.py   # Dataset loading
│       └── preprocessing.py # Text preprocessing
├── experiments/
│   ├── baseline.py          # Baseline experiments
│   ├── hyde_v1.py           # HyDE experiments
│   └── analysis.ipynb       # Results analysis
├── configs/
│   ├── baseline.yaml        # Baseline config
│   └── hyde.yaml            # HyDE config
├── results/
│   ├── baseline/            # Baseline results
│   └── enhanced/            # Enhanced results
├── docs/
│   ├── setup.md             # Setup instructions
│   └── experiments.md       # Experiment logs
├── requirements.txt
└── README.md
```

---

## Arabic-Specific Considerations

### Morphology
- **Challenge:** Rich morphology (roots, patterns, affixes)
- **Solution:** Use Arabic-aware tokenization (e.g., Farasa, CAMeL Tools)
- **Impact:** Better matching between query and document terms

### Spelling Variations
- **Challenge:** Hamza (ء، أ، إ، ؤ، ئ), Ya (ي، ى), Alif (ا، آ)
- **Solution:** Normalization rules or LLM-based correction
- **Impact:** Reduce false negatives from spelling mismatches

### Dialects
- **Challenge:** MSA vs. Egyptian, Levantine, Gulf, Maghrebi dialects
- **Solution:** Query rewriting (dialect → MSA) or multilingual embeddings
- **Impact:** Enable cross-dialect retrieval

### Stopwords
- **Challenge:** Arabic-specific stopwords (و، في، من، إلى، etc.)
- **Solution:** Use Arabic stopword list (NLTK, custom)
- **Impact:** Reduce noise in BM25 retrieval

---

**Document Status:** ✅ Complete  
**Next Update:** After embedding model selection
