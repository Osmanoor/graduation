# Open Questions & Research Challenges
**Last Updated:** 6/1/2026  
**Status:** Updated after decision review meeting

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
**Status:** ✅ RESOLVED - Test All Three Separately

**Decision:** Test Dense, BM25, and optionally Hybrid as separate baselines.

**Rationale:**
- Testing separately gives more insight into where improvements come from
- Papers often test both effects independently
- Hybrid is optional third comparison

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
**Status:** ⏳ Under Investigation - Research Needed (9/1/2026)

**Challenge:** MIRACL passages lack metadata (no domain labels like Law, Medical, etc.)

**Research Needed:**
- Find if anyone has created metadata for MIRACL passages
- Determine what analysis/insights we can extract from results
- Framework for transforming results → reports → insights

**Potential Directions:**
- Query categorization by length, complexity
- Manual sampling and analysis
- Look for existing MIRACL analysis papers

---

### 2. Pyserini vs HuggingFace Understanding
**Status:** ⏳ Under Investigation - Research Needed (9/1/2026)

**Question:** What does Pyserini do that HuggingFace doesn't? Why use one over the other?

**Context:**
- HuggingFace is standard practice
- May switch to HuggingFace later for other methods
- Need to understand the difference for future flexibility

---

### 3. First Query Enhancement Technique
**Status:** ⏳ Under Investigation - Decide After Baseline

**Question:** Which technique should we implement first?

**Candidates:**
1. **HyDE** - Generate hypothetical document
2. **Query Rewriting** - Normalize/improve query
3. **Query Expansion** - Add synonyms, morphology
4. **Query Decomposition** - Break complex queries

**Approach:**
1. Build baseline first
2. Analyze errors from baseline
3. Research papers that used MIRACL with query enhancement
4. Select based on: baseline errors, paper precedents, feasibility

**Lead:** Found paper about "efficient generation augmented query rewriter" citing MIRACL - needs reading.

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

### 5. Arabic LLM Selection
**Status:** ⏳ Under Investigation - Current Suggestions Weak

**Question:** Which Arabic LLM should we use for query enhancement?

**AI Suggested:** Jais, AceGPT, Gemini 1.5 Pro, GPT-4

**Problem:** These may not be the best options available now.

**Action:** Research stronger Arabic LLM models.

---

### 6. Meta-data Filtering Integration
**Status:** ⏳ New Research Direction Identified

**Question:** Can we combine query enhancement with meta-data filtering?

**Idea:** If MIRACL has meta-data columns, we could:
- Use query enhancement to identify relevant sections
- Filter 2.1M passages down to relevant subset
- Potentially exponential improvement

**Dependency:** Check if MIRACL has useful meta-data columns.

---

## Technical Challenges (Ongoing)

### 7. Scale Challenge
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

### 8. Dialectical Support
**Challenge:** Both MIRACL and ARABICA are MSA-only

**Implication:** We cannot directly test dialectical improvements.

**New Understanding:**
- Dialectical mismatch was originally a key problem
- But our datasets don't support testing this
- Our techniques may still help with dialects (can't measure)
- If approach improves Arabic AND English, that's a strong contribution

**Status:** Not primary focus anymore.

---

### 9. Arabic Morphology Handling
**Status:** Test with baseline first, add preprocessing if needed

**Question:** How to handle Arabic morphology?

**Options:**
1. **Preprocessing:** Normalize spelling, apply stemming
2. **LLM-based:** Use query rewriting to standardize
3. **Embedding-based:** Trust multilingual embeddings
4. **Hybrid:** Combine approaches

**Approach:** Start simple, add complexity if needed.

---

### 10. Evaluation Granularity
**Status:** Plan for this in experiment design

**Question:** How to understand *what* improved, not just *that* it improved?

**Solutions:**
1. Error analysis: Review improved/degraded queries
2. Query categorization: Group by length, complexity, domain
3. Ablation studies: Test individual components
4. Qualitative analysis: Case studies

**Importance:** Critical for understanding contribution and writing paper.

---

### 11. Prototyping with Subsets
**Status:** Allowed but with caution

**Question:** Can we use smaller subsets for faster iteration?

**Decision:** Yes, but must ensure subsets don't give misleading results.

**Use Cases:**
- Technique exploration (HyDE vs Query Rewriting)
- Debugging and development
- NOT for final results

---

## Questions for Future Consideration

### 12. Contribution Framing
**Question:** What is our primary contribution?

**Options:**
1. Technique adaptation (English → Arabic)
2. Empirical study of query enhancement for Arabic
3. System building (better Arabic RAG)

**Status:** Will clarify after Checkpoint 1 results.

---

### 13. Generalization Testing
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
| First Technique | ⏳ Under Investigation |
| Hierarchical Structures | ⏳ Under Investigation |
| Arabic LLMs | ⏳ Under Investigation |
| Meta-data Filtering | ⏳ New Direction |
| Error Analysis Approach | ⏳ Research Needed (9/1/2026) |
| Pyserini vs HuggingFace | ⏳ Research Needed (9/1/2026) |

---

**Document Status:** ✅ Updated after 9/1/2026 meeting  
**Next Update:** After baseline is established
