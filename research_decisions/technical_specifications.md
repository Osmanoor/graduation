# Technical Specifications
**Project:** Arabic RAG Query Enhancement  
**Last Updated:** 6/1/2026  
**Status:** Updated after decision review meeting

---

## System Architecture

### Overview
```
User Query (Arabic)
    ↓
[Query Enhancement Layer] ← Our Focus
    ↓
[Retriever: Dense OR BM25 (tested separately)]
    ↓
Retrieved Chunks
    ↓
[Generator: LLM] ← Deferred for now
    ↓
Final Answer
```

**Key Change (6/1/2026):** Test Dense and BM25 separately, not just Hybrid.
This gives more insight into where improvements come from.

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

**Arabic LLM Candidates:** ⏳ Under Investigation
- Current suggestions (Jais, AceGPT) may be weak
- Need to research stronger Arabic LLM models
- Gemini 1.5 Pro (multilingual, good Arabic support)
- GPT-4 (multilingual, expensive)

#### 2. Retriever (Test Separately)

**Baseline Strategy (Updated 6/1/2026):**
- Test Dense and BM25 **separately** to understand individual contributions
- Hybrid is optional third comparison if time permits

**Dense Retrieval:**
- **Model Candidates:** ⏳ Under Investigation
  - BGE-m3 (multilingual, open-source) - slow iteration
  - E5 multilingual - slow iteration
  - Jina AI embeddings (multilingual, API) - fast iteration, costs money
- **Key Tradeoff:** Iteration speed vs cost
- **Vector Database:** FAISS or Chroma (local, not cloud)
- **Similarity Metric:** Cosine similarity
- **Top-K:** 10 (for Recall@10 evaluation)

**Sparse Retrieval:**
- **Algorithm:** BM25
- **Implementation:** Pyserini or ElasticSearch (based on papers)
- **Advantages:** 
  - Resource-friendly (no GPU needed)
  - Excellent for keyword matching
  - Complements semantic search
- **Arabic Considerations:**
  - Tokenization: Handle Arabic morphology
  - Stopwords: Arabic-specific stopword list
  - Stemming: Optional (root extraction)

**Hybrid Strategy (Optional):**
- Run both retrievers in parallel
- Combine results (weighted or ranked fusion)
- Only if time permits after testing separately

#### 3. Generator (Deferred)
**Status:** Not implemented in Phase 1

**Future Considerations:**
- Arabic LLM selection
- Prompt engineering for Arabic
- Evaluation metrics: F1, Exact Match, Truthfulness

---

## Embedding Model Selection

### Status: ⏳ Under Investigation

**Key Tradeoff Identified (6/1/2026):**
- **Open Source (BGE-m3, E5):** Free but slow iteration (hours for large corpus)
- **Closed Source (Jina AI):** Fast iteration (API calls) but costs money

**Approach:** Keep as side task, don't block main work.

### Evaluation Criteria
1. **Arabic Performance:** Benchmark scores on Arabic tasks
2. **Iteration Speed:** How fast can we run experiments?
3. **Cost:** API costs vs compute costs
4. **Open vs. Closed:** Open-source preferred for research reproducibility

### Candidates

#### BGE-m3
- **Type:** Open-source, multilingual
- **Strengths:** Widely used, good benchmarks, free
- **Weaknesses:** Slow iteration (local inference)
- **Use Case:** Final experiments, reproducibility

#### E5 Multilingual
- **Type:** Open-source, multilingual
- **Strengths:** Good benchmarks
- **Weaknesses:** Slow iteration
- **Use Case:** Alternative to BGE-m3

#### Jina AI
- **Type:** Closed-source API, multilingual
- **Strengths:** Fast iteration, good Arabic performance
- **Weaknesses:** API dependency, costs
- **Use Case:** Rapid prototyping, technique exploration

### Selection Process
1. Research Arabic NLP benchmarks (MIRACL leaderboard)
2. Calculate costs for MIRACL corpus embedding
3. Consider: Open Source for final results, Jina for prototyping
4. Don't block main work on this decision

---

## Dataset Specifications

### Primary: MIRACL (Arabic) ✅ Confirmed

**Status:** High confidence (~95%)

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
- Documents: **~2.1M Arabic Wikipedia passages** ⚠️ Scale challenge!
- Queries: ~2,896 (train/dev/test splits)
- Avg query length: ~8 words
- Avg document length: ~100 words
- Relevance levels: 0 (not relevant) to 3 (highly relevant)
- **Language:** MSA only (dialectical testing not possible)

**Resource Requirements:**
- Storage: ~50GB for corpus + embeddings
- Solution: Google Drive Pro (2TB)

**Preprocessing Requirements:**
1. Download Wikipedia dumps (Arabic)
2. Chunk into passages (as per MIRACL paper)
3. Index with chosen embedding model
4. Load queries and relevance judgments
5. Implement evaluation pipeline

### Secondary: ARABICA ⏳ Potential/Long-term Only

**Status:** Not committed for short-term work

**Structure:**
- 90,000+ question-answer pairs
- Difficulty labels: Hard, Easy
- Hard = answer not in BM25 top-10
- **Language:** MSA (not dialectical)

**Use Case:**
- Generalization testing AFTER primary experiments complete
- Focus on "Hard" subset for query enhancement validation
- Decision can change as project progresses

---

## Evaluation Framework

### Metrics ✅ Confirmed

#### Primary (Retrieval)
1. **Recall@K (K=10)** ✅
   - Formula: (# relevant docs in top-K) / (# total relevant docs)
   - Measures: Did we retrieve the relevant passages?
   - Target: Improve over baseline

2. **NDCG@K (K=10)** ✅
   - Formula: Normalized Discounted Cumulative Gain
   - Measures: Did we rank relevant passages higher?
   - Target: Improve over baseline

3. **MRR (Mean Reciprocal Rank)** ✅
   - Formula: 1 / (rank of first relevant doc)
   - Measures: How quickly do we find relevant docs?
   - Target: Improve over baseline

**Note:** Can expand to more metrics later (different K values, Precision@K, etc.)
Metrics are computationally cheap - just code running on results.

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

### Timeline: ~6 Weeks (Jan 6 - Feb 15, 2026)
**Note:** Acknowledged as "optimistic"

### Phase 1: Baseline Setup (Weeks 1-3)
**Goal:** Establish reproducible baseline with Dense and BM25 separately

**Tasks:**
1. Set up development environment
   - Python 3.9+
   - Libraries: transformers, sentence-transformers, faiss, rank-bm25
2. Download MIRACL dataset
3. Implement data loaders
4. Implement Dense retriever (separate baseline)
5. Implement BM25 retriever (separate baseline)
6. Implement evaluation pipeline (Recall@10, NDCG@10, MRR)
7. Run baseline experiments
8. Document baseline performance

**Deliverables:**
- Baseline code (GitHub repo)
- Baseline metrics report (Dense AND BM25 separately)
- Documentation

### Phase 2: Query Enhancement (Weeks 4-5)
**Goal:** Implement and test first technique

**Tasks:**
1. Analyze baseline errors
2. Select technique based on error analysis and paper research
3. Implement enhancement layer
4. Integrate with baseline system
5. Run experiments
6. Analyze results
7. Document findings

**Deliverables:**
- Enhanced system code
- Comparison report (baseline vs. enhanced)
- Analysis of improvements

### Phase 3: Analysis & Documentation (Week 6)
**Goal:** Comprehensive analysis and thesis writing

**Tasks:**
1. Error analysis: What improved? What didn't?
2. Query categorization: Which query types benefited?
3. Write thesis chapters
4. Prepare final documentation

**Deliverables:**
- Comprehensive analysis report
- Thesis chapters
- Full experiment documentation

---

## Resource Requirements

### Computational
- **GPU:** Recommended for embedding inference (can use CPU for BM25)
- **RAM:** 16GB+ for loading embeddings
- **Storage:** ~50GB for MIRACL corpus + embeddings
- **Cloud:** Google Colab Pro for GPU, Google Drive Pro (2TB) for storage

### API Costs (if using closed-source)
- **Jina AI:** Good for fast iteration, costs for large-scale
- **OpenAI:** Expensive for large-scale experiments
- **Gemini:** Competitive pricing, good for prototyping

### Prototyping Strategy
- Can use smaller subsets for technique exploration
- Must ensure subsets don't give misleading results
- Full dataset for final experiments

### Time Estimates
- Baseline setup: 2-3 weeks
- First technique implementation: 1-2 weeks
- Analysis and documentation: 1 week

---

## Code Structure ✅ Approved

```
arabic-rag-query-enhancement/
├── data/
│   ├── miracl/              # MIRACL dataset
│   ├── arabica/             # Secondary dataset (future)
│   └── processed/           # Preprocessed data
├── src/
│   ├── retrievers/
│   │   ├── dense.py         # Dense retrieval (separate baseline)
│   │   ├── sparse.py        # BM25 (separate baseline)
│   │   └── hybrid.py        # Hybrid retriever (optional)
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
│   ├── baseline_dense.py    # Dense baseline experiments
│   ├── baseline_bm25.py     # BM25 baseline experiments
│   ├── enhanced_v1.py       # First enhancement experiments
│   └── analysis.ipynb       # Results analysis
├── docs/
│   ├── experiments/         # Experiment documentation (CRITICAL)
│   │   ├── exp_001_baseline_dense.md
│   │   ├── exp_002_baseline_bm25.md
│   │   └── ...
│   ├── setup.md             # Setup instructions
│   └── decisions.md         # Decision log
├── results/
│   ├── baseline_dense/      # Dense baseline results
│   ├── baseline_bm25/       # BM25 baseline results
│   └── enhanced/            # Enhanced results
├── configs/
│   ├── baseline.yaml        # Baseline config
│   └── enhanced.yaml        # Enhanced config
├── requirements.txt
└── README.md
```

**Documentation Emphasis (from 6/1/2026 meeting):**
- Every experiment must be fully documented
- Document: Why → How → Errors → Code → Results → Analysis
- Hierarchical structure for easy reference
- Future AI agents should be able to write thesis from this documentation

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
- **Reality (6/1/2026):** Both MIRACL and ARABICA are MSA-only
- **Implication:** Cannot directly test dialectical improvements
- **Note:** Our techniques may still help with dialects, but we can't measure this

### Stopwords
- **Challenge:** Arabic-specific stopwords (و، في، من، إلى، etc.)
- **Solution:** Use Arabic stopword list (NLTK, custom)
- **Impact:** Reduce noise in BM25 retrieval

---

**Document Status:** ✅ Updated after 6/1/2026 meeting  
**Next Update:** After baseline implementation
