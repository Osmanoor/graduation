# 🧬 RESEARCH_CONTEXT_KERNEL.md
**Project:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement
**Status:** Phase 2 - Query Enhancement (Model Comparison)
**Last Updated:** 11/2/2026

---

## 1. 🧭 Project Overview & Trajectory
**The Goal:** We aim to improve the retrieval recall of RAG systems for **Low-Resource Languages (specifically Arabic)**. We hypothesize that standard retrieval fails due to query-document mismatch (morphological, spelling, ambiguity issues).

**The Pivot:**
*   *Original Scope:* Broad RAG enhancement using GraphRAG and Agentic workflows.
*   *Current Scope:* Narrowed significantly to focus on **Query Enhancement (QE)** techniques. We believe fixing the input (the query) is the most high-leverage intervention.

**Important Note:** Our datasets (MIRACL, ARABICA) are MSA-only, so dialectical mismatch is NOT our primary focus anymore. Our techniques may still help with dialects, but we can't directly measure this.

## 2. 📍 Current Status: Model Comparison for Query Expansion
We are currently in the **Model Comparison** stage of Query Enhancement.
*   **What we have done:**
    *   Conducted broad landscape analysis of English-centric RAG papers (HyDE, RQ-RAG, QE-RAG, etc.)
    *   Consulted with Mohamed Rashad (AI researcher) on approach
    *   Analyzed 10+ Arabic datasets for suitability
    *   Clarified decision status in 6/1/2026 review meeting
    *   **Completed embedding model research (9/1/2026)**
    *   **Decided on Pyserini pre-built indexes for baselines (9/1/2026)**
    *   **Designed evaluation pipeline (9/1/2026)**
    *   **Implemented BM25S baseline - Recall@100: 0.8577, NDCG@10: 0.4621 (26/1/2026)**
    *   **Implemented Dense baseline (mDPR) - Recall@100: 0.8407, NDCG@10: 0.4993 (14/1/2026)**
    *   **Completed error analysis (17/1/2026)** - 39% failure rate, short query gap identified
    *   **Selected QE technique (17/1/2026)** - Query Expansion (LLM-based, Query2Doc approach)
    *   **Completed LLM model research (11/2/2026)** - 15 papers reviewed, 10 models identified
    *   **Implemented Query2Doc with Qwen 2.5 3B (11/2/2026)** - +8.9% NDCG@10 improvement!
    *   **Created model comparison guide (11/2/2026)** - 10 models split between team members
*   **What we are doing now:**
    *   **Model comparison experiments** - Testing 10 open-source models on same Query2Doc pipeline
    *   Split: Mohammed (Falcon-H1-3B, Jais-2-8B, ALLaM-7B, Qwen3-4B, GPT-OSS 20B)
    *   Split: Osman (SILMA Kashif-2B, Qwen2.5-7B, Qwen3-8B, Gemma 3 4B, Aya 8B)
    *   Testing on Dense (priority), then BM25S, then Hybrid for top models
*   **Critical Note for Agents:** First QE experiment (exp_003) shows strong results (+8.9% NDCG@10 with Qwen 2.5 3B). Now comparing models to find the best one for Arabic.

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
**Status:** Decided - test Dense and BM25S separately
*   **Dense Retriever:** ✅ Complete - mDPR baseline (Recall@10: 0.6156, NDCG@10: 0.4993)
*   **BM25S (Sparse):** ✅ Decided (23/1/2026) - Python-native implementation
    - Decision: Use BM25S instead of Pyserini (no Java dependencies)
    - Results: 96% of MIRACL baseline, 2% difference acceptable
    - Status: Implementation complete, experiment documentation in progress
*   **Hybrid:** Optional third comparison if time permits
*   **Rationale:** Testing separately gives more insight into where improvements come from
*   **Details:** See `meetings/6.1.2026_meeting_outcomes.md`, `meetings/23.1.2026.md`

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

### A. LLM Model Selection for Query Expansion ✅ Research Complete (11/2/2026)
**Status:** Research done, now in model comparison phase (Task 4.0b)
*   **Goal:** Compare 10 open-source models for Arabic Query2Doc expansion
*   **Research Completed:**
    - 15 papers reviewed (HyDE, Query2Doc, CSQE, PBR, MUGI, KAR, AQE, ThinkQE, etc.)
    - 10 open-source models identified and split between team members
    - First model tested: Qwen 2.5 3B → +8.9% NDCG@10 improvement
*   **10 Models Selected (split between Mohammed & Osman):**
    - Mohammed: Falcon-H1-Arabic-3B, Jais-2-8B, ALLaM-7B, Qwen3-4B, GPT-OSS 20B
    - Osman: SILMA Kashif-2B, Qwen2.5-7B, Qwen3-8B, Gemma 3 4B-IT, Aya Expanse 8B
*   **Key Research Gap Identified:** No paper tests modern 2-4B models for zero-shot Arabic QE
*   **Technical Approach:** 4-bit quantization (bitsandbytes NF4) for 7B+ models on T4 GPU
*   **API Options:** Documented but deferred (focus on open-source first)
*   **Documentation:**
    - Full research: `research_decisions/llm_model_research.md`
    - Deep Research raw data: `research_decisions/models_reserch.md`
    - Model comparison guide: `research_decisions/model_comparison_guide.md`
*   **Meeting:** `meetings/23.1.2026.md`

### B. Error Analysis Approach ✅ RESOLVED (14/1/2026)
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

### C. Pyserini vs HuggingFace Understanding ✅ RESOLVED (23/1/2026)
**Status:** Resolved - Using BM25S (Python-native)
*   **Decision:** Moved away from Pyserini entirely due to Java dependency issues
*   **Solution:** BM25S - pure Python implementation, no Java required
*   **Outcome:** Better flexibility, faster iteration, modern implementation (2024)

### C. First Query Enhancement Technique ✅ RESOLVED (17/1/2026, Refined 23/1/2026)
**Status:** Decided - Query Expansion (LLM-based)
*   **Decision:** Query Expansion using small LLM
*   **Justification (Quantitative Evidence, N=2,896):**
    - Short queries achieve only 59% of long query performance (NDCG 0.240 vs 0.406)
    - Problem: Information poverty in short queries
    - Solution: Query Expansion adds context to address this gap
*   **Implementation Approach (Refined 23/1/2026):**
    1. Start with Query Expansion (not HyDE initially)
    2. Use small LLM that can run in Google Colab free tier
    3. Simple implementation (similar to HyDE approach but for expansion)
    4. Avoid API costs initially (try local models first)
    5. Fallback to API if needed (Groq with GPT-OSS 20B or Gemini 1.5 Flash)
*   **LLM Selection:** ✅ Research Complete (11/2/2026) - See Section 4.A
    - 10 open-source models selected for comparison
    - First test: Qwen 2.5 3B → +8.9% NDCG@10
*   **Monitoring Strategy (Discussed 23/1/2026):**
    - Track quantitative improvements (query length, etc.)
    - Consider Wikipedia API for metadata enrichment
    - Need clear indicators of what improves with prompt engineering
*   **Papers Referenced:** GRF (Generative Relevance Feedback), HyDE, Query2Doc
*   **Documentation:** 
    - Main reference: `ERROR_ANALYSIS_COMPLETE.md`
    - Decision: `research_decisions/qe_technique_selection.md`
    - Meeting: `meetings/23.1.2026.md`

### D. Monitoring/Evaluation Strategy for Query Enhancement ⏳ (23/1/2026)
**Status:** Needs Planning
*   **Challenge:** Need to track what improves with prompt engineering iterations
*   **Potential Approaches (Discussed):**
    - Wikipedia API for metadata enrichment
    - Track quantitative metrics (query length improvements)
    - Need clear indicators of where improvement happens
*   **Context:** Related to error analysis, important for iterative prompt optimization
*   **Meeting:** `meetings/23.1.2026.md`

### E. Hierarchical Structures ⏳
**Status:** Interesting but Needs Feasibility Study
*   *Context:* Mohamed Rashad suggested context injection (knowledge base structure awareness)
*   *Challenge:* Is this feasible given our constraints? Does it require re-embedding?
*   *Current Stance:* Defer, focus on simpler query enhancement first

### F. Embedding Model Selection ✅ RESOLVED (9/1/2026)
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

## 4.5. 📊 Experiment Results & Error Analysis

### Baseline Performance
**Experiment 001: Dense Baseline (mDPR + Identity Enhancement)**
- Recall@10: 0.6156
- Recall@100: 0.8407
- NDCG@10: 0.4993
- MRR: 0.5328
- Dataset: MIRACL Arabic dev set (2,896 queries)
- Documentation: `docs/experiments/exp_001_baseline_dense.md`

**Experiment 002: BM25S Baseline (26/1/2026)**
- Recall@10: 0.5964
- Recall@100: 0.8577
- NDCG@10: 0.4621
- MRR: 0.4836
- Documentation: `docs/experiments/exp_002_baseline_bm25.md`

**Baseline Comparison:**
| Metric | mDPR (Dense) | BM25S (Sparse) | Winner |
|--------|--------------|----------------|--------|
| Recall@100 | 0.8407 | 0.8577 | BM25S (+2.0%) |
| NDCG@10 | 0.4993 | 0.4621 | mDPR (+8.1%) |
| Recall@10 | 0.6156 | 0.5964 | mDPR (+3.2%) |
| MRR | 0.5328 | 0.4836 | mDPR (+10.2%) |

**Key Insight:** BM25S retrieves more docs, mDPR ranks them better. Complementary strengths!

### First Query Enhancement Result
**Experiment 003: Query2Doc + Dense Retrieval (11/2/2026)**
- Model: Qwen 2.5 3B (FP16, zero-shot)
- Method: Query2Doc (LLM generates pseudo-document, concatenated with original query)
- Recall@10: 0.6608 (+7.3% over dense baseline)
- NDCG@10: 0.5435 (+8.9% over dense baseline)
- MRR: 0.5742 (+7.8% over dense baseline)
- Runtime: ~40 min on free Colab T4 for 2,896 queries
- Documentation: `docs/experiments/exp_003_query2doc_dense.md`

**BM25S Implementation Decision (23/1/2026):**
- **Selected:** BM25S (pure Python, no Java)
- **Rationale:** 500x faster, modern (2024), scientifically valid, better flexibility
- **Results:** 96% of MIRACL baseline (2% difference acceptable)
- **Status:** Implementation complete, experiment documented

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
*   **`docs/experiments/exp_001_baseline_dense.md`**: Dense baseline experiment (mDPR)
*   **`docs/experiments/exp_002_baseline_bm25.md`**: BM25S baseline experiment
*   **`docs/experiments/exp_003_query2doc_dense.md`**: Query2Doc + Dense (Qwen 2.5 3B)
*   **`research_decisions/llm_model_research.md`**: Comprehensive LLM research (15 papers, 10 models)
*   **`research_decisions/models_reserch.md`**: ChatGPT Deep Research raw output
*   **`research_decisions/model_comparison_guide.md`**: Model comparison experiment guide (10 models)
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

### Completed
- [x] Update documentation to reflect meeting decisions (23/1/2026) ✅
- [x] **Task 4.0:** Research LLM models for Query Expansion ✅ (11/2/2026)
- [x] **Task 2.3:** BM25S baseline experiment (exp_002) ✅ (Osman)
- [x] **Task 4.1:** Implement Query2Doc enhancer ✅ (Osman)
- [x] **Task 4.3:** First QE experiment - exp_003 with Qwen 2.5 3B ✅

### Current (Model Comparison Phase)
- [ ] **Task 4.0b:** Model Comparison Experiments
  - Mohammed: Falcon-H1-3B → Jais-2-8B → ALLaM-7B → Qwen3-4B → GPT-OSS 20B
  - Osman: SILMA Kashif-2B → Qwen2.5-7B → Qwen3-8B → Gemma 3 4B → Aya 8B
  - Test each on Dense retrieval first, then BM25S and Hybrid for top models
  - Guide: `research_decisions/model_comparison_guide.md`

### Upcoming
- [ ] Analyze model comparison results, select best model(s)
- [ ] Run full experiments on Dense, Sparse, and Hybrid with top models
- [ ] Develop monitoring strategy for prompt engineering iterations
- [ ] Error analysis on enhanced queries
- [ ] Write thesis chapters
- [ ] Explore use cases (voice agents, etc.)

*Details:* See `TASKS.md`

