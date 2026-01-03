# Open Questions & Research Challenges
**Last Updated:** 2/1/2026  
**Status:** Living document - updated as questions are resolved

---

## Critical Decisions (Pending Supervisor Input)

### 1. Problem-Oriented vs. Technology-Oriented Approach
**Question:** Should we pre-define a specific problem (e.g., dialectical mismatch) or apply techniques and discover what they solve?

**Current Stance:** Technology-oriented (apply techniques, analyze improvements)

**Arguments For Technology-Oriented:**
- Safer approach with existing datasets
- Can discover multiple problems solved by one technique
- Easier to scale experiments
- Aligns with Mohamed Rashad's advice (simple baseline + layer)

**Arguments For Problem-Oriented:**
- Clearer research narrative
- More targeted contribution
- Better alignment with specific Arabic challenges
- Easier to justify technique selection

**Decision Needed By:** Today's supervisor meeting

**Impact:** Affects dataset selection, technique prioritization, paper framing

---

### 2. Embedding Model Selection
**Question:** Which embedding model should we use for baseline?

**Candidates:**
1. **BGE-m3** - Safe, widely used, open-source
2. **Jina AI** - Good Arabic performance, API-based
3. **Qwen** - Recent, multilingual
4. **E5** - Alternative baseline

**Evaluation Criteria:**
- Arabic performance on MIRACL benchmark
- Resource requirements (cost, compute)
- Open-source vs. closed-source trade-offs

**Next Steps:**
- Review MIRACL leaderboard
- Test top 2-3 models on sample queries
- Measure Recall@10, inference time, cost

**Decision Needed By:** End of this week

**Impact:** Affects baseline performance, experiment reproducibility, resource budget

---

### 3. First Query Enhancement Technique
**Question:** Which technique should we implement first?

**Candidates:**
1. **HyDE (Hypothetical Document Embeddings)**
   - Pros: Well-established, works for both dense and sparse
   - Cons: Requires Arabic LLM, hallucination concerns
   - Complexity: Medium

2. **Query Rewriting (Dialect → MSA)**
   - Pros: Directly addresses Arabic challenge
   - Cons: Requires dialectical dataset for testing
   - Complexity: Medium

3. **Query Expansion**
   - Pros: Simple, rule-based possible
   - Cons: May add noise, requires Arabic morphology handling
   - Complexity: Low

4. **Query Decomposition**
   - Pros: Handles complex queries
   - Cons: Requires orchestration, more complex
   - Complexity: High

**Current Preference:** HyDE or Query Rewriting

**Decision Needed By:** After baseline is established

**Impact:** Affects implementation timeline, paper narrative, contribution clarity

---

## Technical Challenges

### 4. Dialectical Support
**Challenge:** MIRACL is MSA-only, but Arabic dialects are a major real-world challenge

**Questions:**
- Should we defer dialectical support to Checkpoint 2?
- Should we use Multi-Native QA dataset instead?
- Can we test dialect handling without a dialectical dataset?
- Should we create synthetic dialectical queries?

**Potential Solutions:**
1. Start with MSA (MIRACL), add dialect support later
2. Use Query Rewriting to normalize dialects → MSA
3. Test on Multi-Native QA as secondary dataset
4. Generate synthetic dialectical queries from MIRACL

**Trade-offs:**
- MSA-only: Easier to start, but misses key Arabic challenge
- Dialectical: More impactful, but harder to evaluate, smaller datasets

**Status:** Deferred pending supervisor input

---

### 5. Synthetic Data Generation
**Challenge:** Synthetic queries may be too semantically similar to documents

**Questions:**
- Is synthetic data viable for query enhancement research?
- How to avoid semantic similarity bias?
- Can we use LLMs to generate diverse queries?
- Should we use templates or free-form generation?

**Concerns:**
- Queries generated from documents → too easy to retrieve
- Doesn't reflect real user queries (natural mismatch)
- May not test query enhancement effectively

**Potential Solutions:**
1. Generate queries without showing documents (like MIRACL)
2. Use diverse prompts to increase query variety
3. Add noise (typos, paraphrasing) to synthetic queries
4. Validate synthetic data against human-written queries

**Status:** Not critical for Checkpoint 1 (using MIRACL), revisit if needed

---

### 6. Hierarchical Structures (RAPTOR, LevelRAG)
**Challenge:** How to integrate hierarchical approaches with retrieval-only evaluation?

**Questions:**
- Can we test RAPTOR-style chunking with Recall@10 metrics?
- Does hierarchical indexing improve retrieval or just generation?
- How to provide "knowledge base structure" to LLM (Mohamed Rashad's suggestion)?
- Is this too complex for our scope?

**Mohamed Rashad's Feedback:**
- Hierarchical structures are overly complex
- Better to focus on simple baseline + query enhancement
- Knowledge-aware RAG is interesting but not priority

**Current Stance:** Defer hierarchical approaches, focus on query enhancement

**Potential Future Work:**
- Context injection: Provide LLM with corpus summary/tree
- Test if knowledge awareness improves query formulation
- Compare with RAPTOR in Checkpoint 5 (benchmarking)

**Status:** Deferred, not critical for core contribution

---

### 7. Arabic Morphology Handling
**Challenge:** Arabic has rich morphology (roots, patterns, affixes)

**Questions:**
- Should we use Arabic-specific tokenization (Farasa, CAMeL Tools)?
- Should we apply stemming/lemmatization?
- How to handle spelling variations (Hamza, Ya, Alif)?
- Can embedding models handle morphology automatically?

**Potential Solutions:**
1. **Preprocessing:** Normalize spelling, apply stemming
2. **LLM-based:** Use query rewriting to standardize
3. **Embedding-based:** Trust multilingual embeddings to handle it
4. **Hybrid:** Combine preprocessing + embeddings

**Trade-offs:**
- Preprocessing: Explicit control, but may lose nuance
- LLM-based: Flexible, but adds latency and cost
- Embedding-based: Simple, but less control

**Status:** Test with baseline first, add preprocessing if needed

---

### 8. Evaluation Granularity
**Challenge:** How to understand *what* improved, not just *that* it improved?

**Questions:**
- How to analyze which query types benefited from enhancement?
- How to identify failure cases?
- Should we categorize queries (simple, complex, dialectical, etc.)?
- How to measure improvement beyond aggregate metrics?

**Potential Solutions:**
1. **Error Analysis:** Manually review improved/degraded queries
2. **Query Categorization:** Group by length, complexity, domain
3. **Ablation Studies:** Test individual components
4. **Qualitative Analysis:** Case studies of interesting examples

**Importance:** Critical for understanding contribution and writing paper

**Status:** Plan for this in experiment design

---

## Methodological Questions

### 9. Baseline Definition
**Question:** What constitutes a "fair" baseline?

**Options:**
1. **Minimal:** BM25 only (sparse retrieval)
2. **Standard:** Dense retrieval with off-the-shelf embeddings
3. **Hybrid:** Dense + BM25 (our current plan)
4. **SOTA:** Best-performing system on MIRACL leaderboard

**Trade-offs:**
- Minimal: Easy to beat, but less impressive
- Standard: Reasonable comparison
- Hybrid: More realistic, but harder to beat
- SOTA: Impressive if we beat it, but risky

**Current Plan:** Hybrid (Dense + BM25) as baseline

**Justification:** Represents realistic RAG system, allows fair comparison

---

### 10. Generalization Testing
**Question:** How to prove our approach generalizes beyond MIRACL?

**Options:**
1. Test on secondary dataset (Arabic QA)
2. Test on different embedding models
3. Test on different query enhancement techniques
4. Test on dialectical dataset (Multi-Native QA)
5. Test on English datasets (prove technique is language-agnostic)

**Current Plan:**
- Checkpoint 1: MIRACL only
- Checkpoint 2: Multiple techniques on MIRACL
- Checkpoint 3: Multiple models on MIRACL
- Checkpoint 4: Secondary dataset (Arabic QA)
- Checkpoint 5: (Optional) English datasets

**Status:** Phased approach, prioritize depth over breadth initially

---

### 11. Contribution Framing
**Question:** What is our primary contribution?

**Options:**
1. **Technique Adaptation:** Adapting English techniques (HyDE, etc.) to Arabic
2. **Problem Solving:** Solving dialectical/morphological challenges in Arabic RAG
3. **Empirical Study:** Comprehensive evaluation of query enhancement for Arabic
4. **System Building:** Building a better Arabic RAG system
5. **Benchmark:** Creating new evaluation framework for Arabic query enhancement

**Current Uncertainty:** Depends on results and approach (problem vs. tech-oriented)

**Ideal Contribution:** "We show that query enhancement technique X improves Arabic RAG retrieval by Y%, particularly for Z types of queries, addressing the W challenge in Arabic NLP."

**Status:** Will clarify after Checkpoint 1 results

---

## Resource & Practical Challenges

### 12. Computational Budget
**Question:** How to manage computational costs?

**Constraints:**
- Limited GPU access
- API costs for closed-source models
- Time constraints (graduation deadline)

**Strategies:**
1. Use free tiers (Jina AI, Google Colab)
2. Prioritize experiments (don't test everything)
3. Use smaller subsets for prototyping
4. Cache embeddings to avoid recomputation

**Status:** Monitor costs, adjust strategy as needed

---

### 13. Time Management
**Question:** How to balance depth vs. breadth given time constraints?

**Priorities:**
1. **Must Have:** Baseline + one technique on MIRACL
2. **Should Have:** Multiple techniques, secondary dataset
3. **Nice to Have:** Multiple models, dialectical support, generation evaluation

**Current Plan:** Focus on Checkpoint 1, scale based on time available

**Status:** Adjust based on supervisor feedback and progress

---

## Questions for Supervisor (Today's Meeting)

1. **Approach:** Do you prefer problem-oriented or technology-oriented approach?
2. **Dialectical:** Should we prioritize dialectical support or defer it?
3. **Scope:** Is focusing on retrieval (not generation) acceptable for graduation project?
4. **Contribution:** What level of contribution is expected (technique adaptation vs. novel method)?
5. **Timeline:** What are the key milestones and deadlines?
6. **Resources:** Any recommendations for computational resources or collaborations?

---

**Document Status:** ✅ Complete  
**Next Update:** After supervisor meeting (today)
