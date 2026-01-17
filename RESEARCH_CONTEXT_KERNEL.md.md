# 🧬 RESEARCH_CONTEXT_KERNEL.md
**Project:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement
**Status:** Phase 2 - Query Enhancement Implementation
**Last Updated:** 17/1/2026

---

## 1. 🧭 Project Overview & Trajectory
**The Goal:** We aim to improve the retrieval recall of RAG systems for **Low-Resource Languages (specifically Arabic)**. We hypothesize that standard retrieval fails due to query-document mismatch (morphological, spelling, ambiguity issues).

**The Pivot:**
*   *Original Scope:* Broad RAG enhancement using GraphRAG and Agentic workflows.
*   *Current Scope:* Narrowed significantly to focus on **Query Enhancement (QE)** techniques. We believe fixing the input (the query) is the most high-leverage intervention.

**Important Note:** Our datasets (MIRACL, ARABICA) are MSA-only, so dialectical mismatch is NOT our primary focus anymore. Our techniques may still help with dialects, but we can't directly measure this.

## 2. 📍 Current Status: Query Enhancement Implementation
We are currently in the **Query Enhancement Implementation** stage.
*   **What we have done:** 
    *   Conducted broad landscape analysis of English-centric RAG papers (HyDE, RQ-RAG, QE-RAG, etc.)
    *   Consulted with Mohamed Rashad (AI researcher) on approach
    *   Analyzed 10+ Arabic datasets for suitability
    *   Clarified decision status in 6/1/2026 review meeting
    *   **Completed embedding model research (9/1/2026)**
    *   **Decided on Pyserini pre-built indexes for baselines (9/1/2026)**
    *   **Designed evaluation pipeline (9/1/2026)**
    *   **Implemented BM25 baseline (BM25S) - Recall@100: 0.8603 (12/1/2026)**
    *   **Implemented Dense baseline (mDPR) - Recall@100: 0.8407, NDCG@10: 0.4993 (14/1/2026)**
    *   **Completed error analysis (17/1/2026)** - 39% failure rate, short query gap identified
    *   **Selected first QE technique (17/1/2026)** - Query Expansion with Normalization (evidence-based)
    *   **Scientific validation (17/1/2026)** - Gemini expert review approved methodology
*   **What we are doing now:** 
    *   Ready to implement Query Expansion with Normalization (Task 4.1)
    *   Next: Experiment 002 (QE + Dense)
*   **Critical Note for Agents:** Error analysis complete and validated. Decision based on quantitative evidence (short query performance gap, N=2,896). See `ERROR_ANALYSIS_COMPLETE.md` for summary.

---

## 3. Decision Status (Updated January 9, 2026)

### A. The Dataset: **MIRACL (Arabic subset)** ✅ Confirmed
**Status:** High confidence (~95%)
*   **Rationale:** Retrieval-focused, high-quality native annotations, natural query-document mismatch
*   **Scale:** ~2.1 Million Arabic Wikipedia passages (significant resource challenge)
*   **Secondary:** ARABICA - marked as "potential/long-term" only, not committed
*   **Limitation:** MSA-only (dialectical testing not directly possible)
*   **Details:** See `meetings/6.1.2026_meeting_outcomes.md`

### B. The Baseline Pipeline: **Test All Three Separately** ✅ Confirmed
**Status:** Decided - test Dense, BM25, and optionally Hybrid separately
*   **Dense Retriever:** Test independently to measure its contribution
*   **BM25 (Sparse):** Test independently to measure its contribution
*   **Hybrid:** Optional third comparison if time permits
*   **Rationale:** Testing separately gives more insight into where improvements come from
*   **Details:** See `meetings/6.1.2026_meeting_outcomes.md`

### C. The Approach: **Technology-Oriented** ✅ Confirmed
**Status:** Decided
*   **Approach:** Apply techniques, discover what problems they solve
*   **Architecture:** User Query → [Query Enhancement Layer] → [Retriever] → Retrieved Chunks
*   **Evaluation:** Retrieval metrics (Recall@10, NDCG@10, MRR)
*   **Rationale:** More flexibility for engineers, aligns with Mohamed Rashad's advice
*   **Details:** See `meetings/Consultation with Mohammed Rashad.md`

### D. Evaluation Pipeline Design ✅ RESOLVED (9/1/2026)
**Status:** Decided - Two-Phase Approach
*   **Pipeline:** Experiment Phase (run search, save results) → Evaluation Phase (calculate metrics)
*   **Storage Format:** Save as IDs only (Query ID + Passage ID), save top 100 per query
*   **Two Purposes:** (1) Documentation for thesis, (2) Context for incremental improvement
*   **Experiment Documentation:** MD file per experiment with setup, parameters, prompts, results
*   **Details:** See `meetings/9.1.2026_meeting_outcomes.md`

---

## 4. 🔄 Under Investigation (Active Research Questions)

### A. Error Analysis Approach ✅ RESOLVED (14/1/2026)
**Status:** Research Complete
*   **Challenge:** MIRACL passages lack metadata (no domain labels like Law, Medical, etc.)
*   **Research Completed:** See `research_decisions/error_analysis_research.md`
*   **Key Findings:**
    - No native metadata exists in MIRACL (confirmed by 4 research providers)
    - NoMIRACL dataset provides hard negatives (HuggingFace available)
    - Wikipedia categories can be fetched via MediaWiki API
    - Query-side analysis is highest ROI for our timeline
*   **Framework:** Score gaps, query length, Wikipedia categories, NoMIRACL hard negatives
*   **Specification:** See `research_decisions/evaluation_pipeline_spec.md`

### B. Pyserini vs HuggingFace Understanding ⏳ (NEW - 9/1/2026)
**Status:** Under Investigation - Research Needed
*   *Question:* What does Pyserini do that HuggingFace doesn't? Why use one over the other?
*   *Context:* HuggingFace is standard practice; may switch to it later for other methods

### C. First Query Enhancement Technique ✅ RESOLVED (17/1/2026)
**Status:** Decided - Query Expansion with Normalization
*   **Decision:** Query Expansion with Normalization
*   **Justification (Quantitative Evidence, N=2,896):**
    - Short queries achieve only 59% of long query performance (NDCG 0.240 vs 0.406)
    - Problem: Information poverty in short queries
    - Solution: Query Expansion adds context to address this gap
*   **Implementation:** Two-step approach
    1. Normalize query (fix spelling, remove diacritics)
    2. Expand with LLM (add synonyms, entity variants, related terms)
*   **LLM:** Gemini 1.5 Flash (free tier, good Arabic support)
*   **Hypothesis to Test:** Query Expansion will improve performance by addressing short query information poverty (no predicted ROI)
*   **Alternative:** HyDE (if expansion shows <15% improvement)
*   **Documentation:** 
    - Main reference: `ERROR_ANALYSIS_COMPLETE.md`
    - Decision: `research_decisions/qe_technique_selection.md`
    - Scientific review: `arabic-rag-query-enhancement/SCIENTIFIC_REVIEW_ERROR_ANALYSIS.md`

### D. Hierarchical Structures ⏳
**Status:** Interesting but Needs Feasibility Study
*   *Context:* Mohamed Rashad suggested context injection (knowledge base structure awareness)
*   *Challenge:* Is this feasible given our constraints? Does it require re-embedding?
*   *Current Stance:* Defer, focus on simpler query enhancement first

### E. Arabic LLM Selection ✅ RESOLVED (17/1/2026)
**Status:** Decided - Gemini 1.5 Flash
*   **Decision:** Use Gemini 1.5 Flash for Query Expansion
*   **Rationale:** Free tier (15 RPM), fast, good Arabic support, lower cost than GPT-4
*   **Backup:** GPT-4o-mini (if Gemini quality insufficient)
*   **Use Case:** Query Expansion (generate synonyms, entity variants, related terms)

### E. Embedding Model Selection ✅ RESOLVED (9/1/2026)
**Status:** Decided - Pyserini Pre-built Indexes
*   **Decision:** Start with Pyserini pre-built indexes (BM25 + mDPR) for initial baselines
*   **Rationale:** Fastest path to implement Query Enhancement techniques; mDPR intentionally "weaker" (not fine-tuned on MIRACL) = more room for improvement
*   **Data Leakage Concern:** E5/BGE-M3 trained on MIRACL, so high scores are "expected" not "achieved"
*   **Future Plan:** After testing QE techniques on mDPR, try stronger models (BGE-M3, E5)
*   **Research Document:** `research_decisions/embedding_model_research.md`
*   **Baseline Results (17/1/2026):**
    - BM25S: Recall@100: 0.8603, NDCG@10: 0.4610, Recall@10: 0.5926
    - mDPR: Recall@100: 0.8407, NDCG@10: 0.4993, Recall@10: 0.6156, MRR: 0.5328

---

## 4.5. 📊 Baseline Results & Error Analysis (NEW - 17/1/2026)

### Baseline Performance
**Experiment 001: Dense Baseline (mDPR + Identity Enhancement)**
- Recall@10: 0.6156
- Recall@100: 0.8407
- NDCG@10: 0.4993
- MRR: 0.5328
- Dataset: MIRACL Arabic dev set (2,896 queries)
- Documentation: `docs/experiments/exp_001_baseline_dense.md`

**Comparison with BM25:**
| Metric | mDPR (Dense) | BM25S (Sparse) | Winner |
|--------|--------------|----------------|--------|
| Recall@100 | 0.8407 | 0.8603 | BM25S (+2.3%) |
| NDCG@10 | 0.4993 | 0.4610 | mDPR (+8.3%) |
| Recall@10 | 0.6156 | 0.5926 | mDPR (+3.9%) |
| MRR | 0.5328 | 0.4821 | mDPR (+10.5%) |

**Key Insight:** BM25 retrieves more docs, mDPR ranks them better. Complementary strengths!

### Error Analysis Findings (17/1/2026)
**Phase 1: Quantitative Analysis (N=2,896 queries - VALIDATED)**
- **39% failure rate** (1,130 queries with NDCG@10 < 0.3)
- **Short query performance gap:** Short queries (1-3 tokens) achieve 59% of long query performance (NDCG 0.240 vs 0.406)
- **Query length correlation:** r=0.125 (p<0.001, weak but significant)
- **Retrieval vs ranking gap:** 99.4% coverage in top-100, but only 93.4% in top-10
- **Key insight:** Information poverty (short queries) is validated driver of failure
- Document: `research_decisions/error_analysis_phase1_quantitative.md`

**Phase 2: Qualitative Observations (N=20 sample - EXPLORATORY ONLY)**
- Observed spelling variations, entity mismatches, diacritics in sample
- Status: Hypotheses only, NOT used for decision-making
- Archived: `archive/error_analysis/error_analysis_phase2_qualitative.md`

**Scientific Review:** ✅ Approved by Gemini expert review
- Decision basis: Quantitative evidence only (short query gap)
- Review: `arabic-rag-query-enhancement/SCIENTIFIC_REVIEW_ERROR_ANALYSIS.md`
- Summary: `ERROR_ANALYSIS_COMPLETE.md`

- Document: `research_decisions/error_analysis_phase2_qualitative.md`

**Key Insight:** 80% of failures stem from three patterns that Query Expansion directly addresses: spelling errors, named entity variations, and vocabulary mismatch.

---

## 5. 📂 Repository Structure & Knowledge Base
*The Agent should use these files to understand our accumulated knowledge.*

### Core Documentation
*   **`RESEARCH_CONTEXT_KERNEL.md.md`** (this file): Project overview, status, and decisions
*   **`meetings/9.1.2026_meeting_outcomes.md`**: Latest meeting outcomes - embedding decision, evaluation pipeline design
*   **`meetings/6.1.2026_meeting_outcomes.md`**: Decision clarifications from review meeting
*   **`meetings/2.1.2026_meeting_outcomes.md`**: Original planning meeting outcomes
*   **`meetings/Consultation with Mohammed Rashad.md`**: Expert advisor feedback and recommendations
*   **`research_decisions/technical_specifications.md`**: System architecture, components, implementation details
*   **`research_decisions/open_questions.md`**: Pending decisions and research challenges
*   **`research_decisions/embedding_model_research.md`**: Full embedding model research (BGE-M3, E5, Jina)
*   **`research_decisions/qe_technique_selection.md`**: Query Enhancement technique decision (Query Expansion with Normalization)
*   **`research_decisions/error_analysis_phase1_quantitative.md`**: Quantitative error analysis results
*   **`research_decisions/error_analysis_phase2_qualitative.md`**: Qualitative error analysis results
*   **`research_decisions/evaluation_pipeline_spec.md`**: Evaluation pipeline specification
*   **`docs/experiments/exp_001_baseline_dense.md`**: Baseline experiment documentation
*   **`reports/mdpr_baseline_report.md`**: Technical report on mDPR baseline reproduction
*   **`research_decisions/AI_ASSUMED_DECISIONS_REVIEW.md`**: What AI got wrong (for context)

### Strategic Discussions
*   **`/gemini_opinions/`**: Contains strategic discussions, pivots, and "Project Management" decisions.
    *   *Key File:* `Branch of Critical Feedback...` (Explains why we dropped GraphRAG).
    *   *Key File:* `Branch of RQ-RAG...` (Analysis of the "Active Generator" architecture).

### Literature Review
*   **`/papers/`**: Contains raw summaries of the academic literature we have read.
    *   *Key Insight:* We have analyzed `QE-RAG.md` (Query Noise), `RQ-RAG.md` (Iterative Feedback), and `Optimizing RAG Pipelines for Arabic.md` (Baseline components).

### Meeting Records
*   **`/meetings/`**: Full transcriptions and summaries of planning sessions
    *   `9.1.2026_meeting_outcomes.md`: Embedding decision meeting outcomes - **LATEST**
    *   `9.1.2026.md`: Full transcription (3 parts)
    *   `6.1.2026_meeting_outcomes.md`: Structured outcomes from review meeting
    *   `6.1.2026.md`: Decision review meeting (3 parts)
    *   `2.1.2026_meeting_outcomes.md`: Original structured outcomes
    *   `2.1.2026.md`: Full 4-part planning meeting transcription
    *   `Consultation with Mohammed Rashad.md`: Expert consultation notes

---

## 6. 🎯 Project Checkpoints & Timeline

**Total Time Available:** ~6 weeks (Jan 6 - Feb 15, 2026)
**Note:** Timeline is acknowledged as "optimistic"

### Checkpoint 1: Proof of Concept (Current Focus)
**Goal:** Prove query enhancement improves Arabic RAG retrieval
*   **Fixed:** MIRACL dataset, baseline retrievers (Dense + BM25 separately)
*   **Success:** Measurable improvement in Recall@10, NDCG@10, MRR
*   **Timeline:** Weeks 1-3

### Checkpoint 2: Technique Iteration
**Goal:** Test multiple query enhancement approaches
*   **Experiments:** Multiple techniques, versioned improvements
*   **Versioning:** Track improvements across technique variations
*   **Timeline:** Weeks 4-5

### Checkpoint 3: Analysis & Documentation
**Goal:** Comprehensive analysis and thesis writing
*   **Analysis:** Error analysis, query categorization, insights
*   **Documentation:** Full experiment documentation, thesis chapters
*   **Timeline:** Week 6

### Scenarios:
*   **Average Case:** Complete Checkpoint 1 + some iteration
*   **Best Case:** Complete Checkpoint 1 and 2 with good documentation

*Details:* See `meetings/6.1.2026_meeting_outcomes.md`

---

## 7. ⚠️ Current Challenges & Risks
1.  **Scale Challenge:** MIRACL has 2.1M passages - significant storage (~50GB) and compute requirements. **Mitigated:** Using Pyserini pre-built indexes avoids embedding time.
2.  **Dialectical Gap:** MIRACL and ARABICA are MSA-only. We cannot directly test dialectical improvements.
3.  **Error Analysis Challenge (NEW):** MIRACL passages lack metadata for categorization (no domain labels). **Mitigated:** Use NoMIRACL hard negatives, Wikipedia categories, query-side analysis (see `research_decisions/error_analysis_research.md`)
4.  **Evaluation Rigor:** Need to understand *what* improved, not just *that* it improved
5.  **Resource Constraints:** Limited GPU access, API costs, 6-week timeline
6.  **Arabic LLM Quality:** Current candidates (Jais, AceGPT) may not be optimal

**Mitigations:**
- Use Google Drive (2TB with Pro) for storage
- Use Google Colab Pro for GPU
- Use Pyserini pre-built indexes (avoids 12-15h embedding time)
- Use smaller subsets for prototyping (if not misleading)
- Prioritize experiments, document everything

*Details:* See `research_decisions/open_questions.md`

---

## 8. 🎯 Guidance for AI Agents
When interacting with this codebase, the Agent should:
1.  **Check Latest Status:** Read `meetings/9.1.2026_meeting_outcomes.md` for latest decisions, then `research_decisions/open_questions.md`
2.  **Understand Uncertainty:** Many things are "under investigation" - don't assume decisions are final
3.  **Document What We Don't Know:** Uncertainty is valuable information
4.  **Technical Details:** Refer to `research_decisions/technical_specifications.md` for architecture
5.  **Open Questions:** Check `research_decisions/open_questions.md` before proposing solutions
6.  **Mark AI Suggestions:** Clearly label any AI suggestions as such, not as decisions
7.  **Validate:** Help formulate experiments to validate if English methods transfer to Arabic

**Key Principle:** We are in "active investigation" mode, not "blind implementation" mode.

---

## 9. 📅 Next Actions (Priority Order)

### Immediate (This Week - Jan 17-19)
- [x] Update documentation to reflect actual decision status
- [x] Research embedding model costs/performance ✅ Complete
- [x] Decide on embedding model approach ✅ Pyserini pre-built indexes
- [x] Design evaluation pipeline ✅ Two-phase approach
- [x] Finalize baseline BM25 retriever (BM25S) ✅ Complete
- [x] Finalize baseline mDPR retriever ✅ Complete
- [x] Analyze baseline errors ✅ Complete (Phase 1 & 2)
- [x] Select first QE technique ✅ Query Expansion with Normalization
- [ ] Implement Query Expansion with Normalization (Task 4.1)
- [ ] Run Experiment 002 (QE + Dense)

### Short-term (Weeks 4-5)
- [ ] Evaluate Experiment 002 results
- [ ] Iterate on Query Expansion if needed
- [ ] Consider HyDE if expansion <15% improvement
- [ ] Try stronger models (BGE-M3, E5) if time permits
- [ ] Document findings thoroughly

### Medium-term (Week 6)
- [ ] Final experiments and analysis
- [ ] Write thesis chapters
- [ ] Prepare final presentation

*Details:* See `meetings/9.1.2026_meeting_outcomes.md` and `TASKS.md`

