# Open Questions & Research Challenges
**Last Updated:** 24/1/2026  
**Status:** Updated after 23/1/2026 meeting - BM25S decision, LLM research task added

---

## ✅ Resolved Questions (from 6/1/2026 and 9/1/2026 Meetings)

### 1. Problem-Oriented vs. Technology-Oriented Approach
**Status:** ✅ RESOLVED - Technology-Oriented

**Decision:** Apply techniques, discover what problems they solve.

**Rationale:**
- More flexibility for engineers
- Can discover multiple problems solved by one technique
- Aligns with Mohamed Rashad's advice

---

### 2. Baseline Retrieval Strategy
**Status:** ✅ RESOLVED - Test Dense and BM25S Separately

**Decision:** Test Dense (mDPR) and BM25S as separate baselines.

**Rationale:**
- Testing separately gives more insight into where improvements come from
- Papers often test both effects independently
- Hybrid is optional third comparison

**BM25 Implementation Decision (23/1/2026):**
- **Selected:** BM25S (pure Python implementation)
- **Rationale:** 
  * No Java dependencies (better flexibility)
  * 500x faster than traditional Pyserini (pre-computed scores)
  * Recent (July 2024) and scientifically valid
  * Results: 96% of MIRACL baseline (2% difference acceptable)
  * Used in recent papers (2024-2026)
- **Results:** Recall@100: 0.8603, NDCG@10: 0.4610, Recall@10: 0.5926, MRR: 0.4821
- **Meeting:** `meetings/23.1.2026.md`

---

### 3. Evaluation Metrics
**Status:** ✅ RESOLVED - Recall@10, NDCG@10, MRR

**Decision:** Use all three metrics, can expand later.

**Rationale:**
- MRR (AI suggestion) was explicitly approved
- Metrics are computationally cheap
- Start with three, expand if needed

---

### 4. ARABICA as Secondary Dataset
**Status:** ✅ RESOLVED - Potential/Long-term Only

**Decision:** Not committed for short-term, only for future generalization.

**Rationale:**
- Focus on near-term decisions
- Defer far-term decisions until clearer picture emerges

---

### 5. Deferring Generation Evaluation
**Status:** ✅ RESOLVED - Confirmed

**Decision:** Focus on retrieval metrics only initially.

**Rationale:**
- MIRACL is retrieval-focused
- Can add generation in optional later checkpoints

---

### 6. Timeline
**Status:** ✅ RESOLVED - ~6 Weeks (Until Feb 15, 2026)

**Decision:** 
- Average case: Complete Checkpoint 1 + some iteration
- Best case: Complete Checkpoint 1 and 2
- Acknowledged as "optimistic"

---

### 7. Evaluation Pipeline Design
**Status:** ✅ RESOLVED - Two-Phase Approach (9/1/2026)

**Decision:** Separate experiment execution from evaluation calculation.

**Pipeline Design:**
1. **Experiment Phase:** Run search → Save results to file (IDs only)
2. **Evaluation Phase:** Calculate metrics from saved results

**Storage Format:**
- Save as IDs only (Query ID + Passage ID) - NOT full passages
- Save top 100 results per query (can extract top 10 later)

**Two Purposes:**
1. Documentation for thesis (show our work)
2. Context for incremental improvement (act as context for Kiro/team)

**Experiment Documentation (MD file per experiment):**
- Why we started the experiment
- Parameters/setup used
- Prompts used (if any)
- Results and immediate effects
- Concise but comprehensive

---

### 8. Embedding Model Selection
**Status:** ✅ RESOLVED - Pyserini Pre-built Indexes (9/1/2026)

**Decision:** Start with Pyserini pre-built indexes (BM25 + mDPR) for initial baselines. Later test on stronger models (BGE-M3, E5).

**Rationale:**
1. Fastest path to implement Query Enhancement techniques
2. mDPR intentionally "weaker" (not fine-tuned on MIRACL) = more room for improvement
3. Avoids 12-15 hour embedding time on Colab
4. Query Enhancement is our main contribution, not beating already-trained models
5. Data leakage concern: E5/BGE-M3 trained on MIRACL, so high scores are "expected" not "achieved"

**Future Plan:**
- After testing QE techniques on mDPR baseline
- Try stronger models (BGE-M3, E5) to see how improvement scales

**Research Completed:** See `research_decisions/embedding_model_research.md`

---

## ⏳ Still Under Investigation

### 1. Error Analysis Approach
**Status:** ✅ RESOLVED - Research Complete (14/1/2026)

**Challenge:** MIRACL passages lack metadata (no domain labels like Law, Medical, etc.)

**Research Completed:** See `research_decisions/error_analysis_research.md`

**Key Findings:**
1. **No native metadata exists** - Confirmed by all 4 research providers
2. **NoMIRACL dataset** - Provides hard negatives and robustness labels (HuggingFace)
3. **Wikipedia categories** - Can be fetched via MediaWiki API (passages are from Wikipedia)
4. **Query-side analysis** - Highest ROI: length, AAFAQ taxonomy, score gaps

**Practical Framework (Immediate Actions):**
- Use NoMIRACL for hard negative analysis
- Fetch Wikipedia categories for domain-based analysis
- Calculate score gaps to identify low-confidence retrievals
- Query feature engineering (length, IDF variance)

**Tools Identified:**
- `ranx` - Ranking evaluation & visualization
- `wikipedia-api` - Category extraction
- `NoMIRACL` dataset on HuggingFace
- AAFAQ framework for Arabic query classification

**Specification:** See `research_decisions/evaluation_pipeline_spec.md`

---

### 2. Pyserini vs HuggingFace Understanding
**Status:** ✅ RESOLVED - Using BM25S (23/1/2026)

**Question:** What does Pyserini do that HuggingFace doesn't? Why use one over the other?

**Decision:** Moved away from Pyserini entirely due to Java dependency issues.

**Solution:** BM25S - pure Python implementation, no Java required.

**Outcome:** Better flexibility, faster iteration, modern implementation (2024).

**Meeting:** `meetings/23.1.2026.md`

---

### 3. First Query Enhancement Technique
**Status:** ✅ RESOLVED - Query Expansion (17/1/2026, Refined 23/1/2026)

**Question:** Which technique should we implement first?

**Decision:** Query Expansion using small LLM

**Rationale (Quantitative Evidence, N=2,896):**
- Short queries achieve only 59% of long query performance (NDCG 0.240 vs 0.406)
- Problem: Information poverty in short queries
- Solution: Query Expansion adds context to address this gap

**Implementation Approach (Refined 23/1/2026):**
1. Start with Query Expansion (not HyDE initially)
2. Use small LLM that can run in Google Colab free tier (2-4B parameters)
3. Simple implementation (similar to HyDE approach but for expansion)
4. Avoid API costs initially (try local models first)
5. Fallback to API if needed (Groq with GPT-OSS 20B or Gemini 1.5 Flash)

**LLM Selection:** ⏳ Under Investigation (Task 4.0 - see below)

**Monitoring Strategy (Discussed 23/1/2026):**
- Track quantitative improvements (query length, etc.)
- Consider Wikipedia API for metadata enrichment
- Need clear indicators of what improves with prompt engineering

**Papers Referenced:** GRF (Generative Relevance Feedback), HyDE, Query2Doc

**Decision Document:** `research_decisions/qe_technique_selection.md`

**Meetings:** 
- 17/1/2026: Initial decision
- 23/1/2026: Implementation approach refined

---

### 4. Hierarchical Structures
**Status:** ⏳ Interesting but Needs Feasibility Study

**Question:** Can we implement Mohamed Rashad's suggestion about context injection?

**Idea:** Provide LLM with knowledge base structure awareness to improve query formulation.

**Challenges:**
- Does this require re-embedding the corpus?
- Is it feasible given our constraints?
- Is it too complex for our scope?

**Current Stance:** Defer, focus on simpler query enhancement first.

---

### 5. Arabic LLM Selection for Query Expansion
**Status:** ⏳ Active Research (Task 4.0 - Mohammed) - 23/1/2026

**Question:** Which small multilingual LLM should we use for Query Expansion?

**Requirements (from 23/1/2026 meeting):**
1. **Size:** Must run on T4 GPU (Colab free tier) - Target: 2-4B parameters
2. **Language:** Multilingual with good Arabic support
3. **Capability:** Can follow prompts for query expansion/rewriting
4. **Truthfulness:** Generates accurate expansions (not hallucinations)

**Candidate Models to Research:**
- **Gemma 2B** - Google's efficient model, multilingual
- **Qwen 4B** - With quantization (initial test failed on T4)
- **GPT-OSS 20B** - Quantized via Unsloth (4-bit/8-bit)
- **Llama variants** - Small versions with quantization
- **Gemma Translator 270M** - Very small, but translation-focused

**Research Approach:**
1. Review HyDE and Query2Doc papers - what models do they use?
2. Search for "latest most powerful multilingual models" that fit constraints
3. Check model cards for Arabic performance
4. Test quantized versions in Colab
5. Evaluate prompt-following capability

**Fallback Options (if local models don't work):**
- **Groq API** with GPT-OSS 20B (8000 tokens/min rate limit)
- **Gemini 1.5 Flash** (free tier, good Arabic)
- Note: Prefer local models to avoid API costs and dependencies

**Fine-tuning Consideration:**
- Status: Deferred ("to be determined later")
- Potential approach: Use AI Studio to generate correct rewriting examples, then fine-tune
- Only if small models can't follow prompts well enough

**Meeting:** `meetings/23.1.2026.md`

---

### 6. Monitoring/Evaluation Strategy for Query Enhancement
**Status:** ⏳ Needs Planning (23/1/2026)

**Question:** How to track what improves during prompt engineering iterations?

**Challenge:** Need clear indicators of where improvement happens with different prompts.

**Potential Approaches (Discussed 23/1/2026):**
- Wikipedia API for metadata enrichment
- Track quantitative metrics (query length improvements)
- Need clear indicators of what improves

**Context:** Related to error analysis, important for iterative prompt optimization.

**Meeting:** `meetings/23.1.2026.md`

---

### 7. Meta-data Filtering Integration
**Status:** ⏳ New Research Direction Identified

**Question:** Can we combine query enhancement with meta-data filtering?

**Idea:** If MIRACL has meta-data columns, we could:
- Use query enhancement to identify relevant sections
- Filter 2.1M passages down to relevant subset
- Potentially exponential improvement

**Dependency:** Check if MIRACL has useful meta-data columns.

---

## Technical Challenges (Ongoing)

### 8. Scale Challenge
**Challenge:** MIRACL has 2.1 Million Arabic Wikipedia passages

**Implications:**
- ~50GB storage required
- Embedding takes significant time/cost
- Need careful resource planning

**Mitigations:**
- Google Drive Pro (2TB) for storage
- Google Colab Pro for GPU
- Smaller subsets for prototyping (if not misleading)
- **NEW (9/1/2026):** Using Pyserini pre-built indexes avoids embedding time entirely

---

### 9. Dialectical Support
**Challenge:** Both MIRACL and ARABICA are MSA-only

**Implication:** We cannot directly test dialectical improvements.

**New Understanding:**
- Dialectical mismatch was originally a key problem
- But our datasets don't support testing this
- Our techniques may still help with dialects (can't measure)
- If approach improves Arabic AND English, that's a strong contribution

**Status:** Not primary focus anymore.

---

### 10. Arabic Morphology Handling
**Status:** Test with baseline first, add preprocessing if needed

**Question:** How to handle Arabic morphology?

**Options:**
1. **Preprocessing:** Normalize spelling, apply stemming
2. **LLM-based:** Use query rewriting to standardize
3. **Embedding-based:** Trust multilingual embeddings
4. **Hybrid:** Combine approaches

**Approach:** Start simple, add complexity if needed.

---

### 11. Evaluation Granularity
**Status:** Plan for this in experiment design

**Question:** How to understand *what* improved, not just *that* it improved?

**Solutions:**
1. Error analysis: Review improved/degraded queries
2. Query categorization: Group by length, complexity, domain
3. Ablation studies: Test individual components
4. Qualitative analysis: Case studies

**Importance:** Critical for understanding contribution and writing paper.

---

### 12. Prototyping with Subsets
**Status:** Allowed but with caution

**Question:** Can we use smaller subsets for faster iteration?

**Decision:** Yes, but must ensure subsets don't give misleading results.

**Use Cases:**
- Technique exploration (HyDE vs Query Rewriting)
- Debugging and development
- NOT for final results

---

## Questions for Future Consideration

### 13. Contribution Framing
**Question:** What is our primary contribution?

**Options:**
1. Technique adaptation (English → Arabic)
2. Empirical study of query enhancement for Arabic
3. System building (better Arabic RAG)

**Status:** Will clarify after Checkpoint 1 results.

---

### 14. Generalization Testing
**Question:** How to prove approach generalizes?

**Options:**
1. Test on ARABICA (secondary dataset)
2. Test on different embedding models
3. Test on English datasets (language-agnostic proof)

**Status:** Phased approach, prioritize depth over breadth initially.

---

## Summary of Status

| Question | Status |
|----------|--------|
| Approach (Tech vs Problem) | ✅ Resolved |
| Baseline Strategy | ✅ Resolved |
| Evaluation Metrics | ✅ Resolved |
| Secondary Dataset | ✅ Resolved |
| Generation Deferral | ✅ Resolved |
| Timeline | ✅ Resolved |
| Evaluation Pipeline Design | ✅ Resolved (9/1/2026) |
| Embedding Model | ✅ Resolved (9/1/2026) - Pyserini pre-built |
| First Technique | ✅ Resolved (17/1/2026) - Query Expansion |
| Hierarchical Structures | ⏳ Under Investigation |
| Arabic LLMs | ⏳ Active Research (23/1/2026) - Task 4.0 |
| Monitoring Strategy | ⏳ Needs Planning (23/1/2026) |
| Meta-data Filtering | ⏳ New Direction |
| Error Analysis Approach | ✅ Resolved (14/1/2026) - See error_analysis_research.md |
| Pyserini vs HuggingFace | ✅ Resolved (23/1/2026) - Using BM25S |
| BM25 Implementation | ✅ Resolved (23/1/2026) - BM25S selected |

---

**Document Status:** ✅ Updated after 23/1/2026 meeting  
**Next Update:** After LLM model research (Task 4.0) and Query Expansion implementation (Task 4.1)
