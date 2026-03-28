# 🧬 RESEARCH_CONTEXT_KERNEL.md
**Project:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement
**Status:** Phase 3 - Thesis Writing & Phase 4 - Expanded Experiments
**Last Updated:** 27/3/2026

---

## 1. 🧭 Project Overview & Trajectory
**The Goal:** We aim to improve the retrieval recall of RAG systems for **Low-Resource Languages (specifically Arabic)**. We hypothesize that standard retrieval fails due to query-document mismatch (morphological, spelling, ambiguity issues).

**The Pivot:**
*   *Original Scope:* Broad RAG enhancement using GraphRAG and Agentic workflows.
*   *Current Scope:* Narrowed significantly to focus on **Query Enhancement (QE)** techniques. We believe fixing the input (the query) is the most high-leverage intervention.

**Important Note:** Our datasets (MIRACL, ARABICA) are MSA-only, so dialectical mismatch is NOT our primary focus anymore. Our techniques may still help with dialects, but we can't directly measure this.

## 2. 📍 Current Status (Updated 27/3/2026)

### Phase 2 — Model Comparison: ✅ COMPLETE
*   **All 10 models tested** on Query2Doc pipeline with MIRACL Arabic
*   **Best model (Dense):** Aya Expanse 8B (+23.5% NDCG@10) and Jais-2-8B (+20.5%)
*   **Best model (BM25):** Jais-2-8B (+10.8%), Aya (+9.2%) — only 3/9 models improved BM25
*   **Dropped:** ALLaM-7B (-48.9%, tokenizer bug), GPT-OSS-20B (70x slower, hallucinations)
*   **Key findings:** Model size correlates with QE quality; multilingual support critical; Arabic vocab helps BM25

### Phase 3 — Thesis Writing: 🔄 IN PROGRESS
*   **Chapters 2, 3, 4:** ✅ First draft complete (27/3/2026)
*   **Chapters 1, 5, Abstract:** ⏳ Next to write
*   **Supervisor meeting (17/3/2026):** Dr. Tahani provided comprehensive thesis writing guidelines
*   **Writing guide:** `research_decisions/thesis_writing_guide.md`
*   **Deadline:** Mid-April 2026 (thesis draft + all practical work)

### Phase 4 — Expanded Experiments: ⏳ PLANNING
*   **Goal:** Build on Query2Doc with chunking-aware QE or other techniques
*   **Constraint:** Must be consistent with existing work, not a new path
*   **Research needed:** Literature review of chunking-aware QE, brainstorming, idea selection
*   **Publication:** Dr. Tahani encouraged publishing a paper (pre-print or journal)

### What was done (chronological):
*   Landscape analysis, dataset selection, baseline pipeline design (Jan 2026)
*   BM25S + mDPR baselines implemented (Jan 2026)
*   Error analysis: 39% failure rate, short query gap identified (Jan 2026)
*   Query2Doc selected as QE technique, implemented with Qwen 2.5 3B: +8.9% NDCG@10 (Feb 2026)
*   10-model comparison completed across Dense + BM25 retrieval (Feb–Mar 2026)
*   Thesis Chapters 2, 3, 4 drafted (Mar 2026)

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

### A. LLM Model Selection & Comparison ✅ COMPLETE (Mar 2026)
**Status:** All 10 models tested, best models identified
*   **Research:** 15 papers reviewed, 10 open-source models selected
*   **Results (Dense NDCG@10):**
    - **Aya Expanse 8B: 0.6166 (+23.5%)** — Best overall
    - **Jais-2-8B: 0.6018 (+20.5%)** — Best for BM25 too
    - Qwen3-8B: 0.5958 (+19.3%), Qwen 2.5-7B: 0.5813 (+16.4%)
    - Qwen3-4B: 0.5691 (+14.0%), Gemma 3 4B: 0.5435 (+8.9%)
    - Qwen 2.5 3B: 0.5435 (+8.9%), Falcon-H1-3B: 0.5359 (+7.3%)
    - SILMA Kashif-2B: 0.5178 (+3.7%)
    - ~~ALLaM-7B: 0.2550 (-48.9%)~~ — DROPPED
    - ~~GPT-OSS-20B~~ — DROPPED (70x slower, hallucinations)
*   **BM25 results:** Only Jais-2 (+10.8%), Aya (+9.2%), Qwen 2.5-7B (+1.3%) improved BM25
*   **Key findings:** Model size → QE quality correlation; Arabic vocab helps BM25; preview models risky
*   **Documentation:**
    - Full research: `research_decisions/llm_model_research.md`
    - Model comparison guide: `research_decisions/model_comparison_guide.md`
    - Per-model research: `research_decisions/{model}_research.md`
    - Osman's results: `arabic-rag-query-enhancement/docs/OSMAN_MODEL_COMPARISON_RESULTS.md`

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

### E. Hierarchical Structures / Chunking-Aware QE ⏳ Phase 4 (Mar 2026)
**Status:** Planning — next research priority
*   *Context:* Mohamed Rashad suggested context injection; team wants to build on Query2Doc
*   *Goal:* Use knowledge of knowledge base structure (chunks, hierarchy, metadata) to improve QE
*   *Constraint:* Must be consistent extension of Query2Doc work, not a new path
*   *Papers to review:* Rebarter and related chunking-aware approaches
*   *Current Stance:* Active research track — Task 6.1 in TASKS.md

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

### Completed Checkpoints
*   **Checkpoint 1: Proof of Concept** ✅ (Feb 2026) — Query2Doc improves Arabic RAG retrieval (+8.9% NDCG@10)
*   **Checkpoint 2: Model Comparison** ✅ (Mar 2026) — 10 models tested, best models identified (Aya, Jais-2)
*   **Checkpoint 3: Thesis Draft (Chapters 2-4)** ✅ (27/3/2026) — First draft complete

### Current Timeline (from supervisor meeting 17/3/2026)
| Milestone | Target | Status |
|-----------|--------|--------|
| Thesis Chapters 2, 3, 4 | March 2026 | ✅ Done |
| Thesis Chapters 1, 5, Abstract | Late March 2026 | ⏳ Next |
| Expanded experiments (chunking-aware QE) | April 2026 | ⏳ Planning |
| Full thesis draft ready | Mid-April 2026 | 🔄 In Progress |
| Exams period | May 2026 | — |
| Presentation recording | After exams | — |
| Project submission | 1 week after last exam | — |

*Details:* See `meetings/17.3.2026.md`, `research_decisions/thesis_writing_guide.md`

---

## 7. ⚠️ Current Challenges & Risks
1.  **Scale Challenge:** MIRACL has 2.1M passages - significant storage (~50GB) and compute requirements. **Mitigated:** Using Pyserini pre-built indexes avoids embedding time.
2.  **Dialectical Gap:** MIRACL and ARABICA are MSA-only. We cannot directly test dialectical improvements.
3.  **Error Analysis Challenge (NEW):** MIRACL passages lack metadata for categorization (no domain labels). **Mitigated:** Use NoMIRACL hard negatives, Wikipedia categories, query-side analysis (see `research_decisions/error_analysis_research.md`)
4.  **Evaluation Rigor:** Need to understand *what* improved, not just *that* it improved
5.  **Resource Constraints:** Limited GPU access, API costs, 6-week timeline
6.  **Arabic LLM Quality:** ✅ Resolved — Aya and Jais-2 identified as best models

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

### Completed (Phases 1 & 2)
- [x] Baselines: BM25S (exp_002) + mDPR (exp_001) ✅
- [x] Error analysis: 39% failure rate, short query gap ✅
- [x] Query2Doc implementation + first experiment (exp_003) ✅
- [x] Model comparison: all 10 models tested (exp_003–009 + Osman's 5) ✅
- [x] Thesis Chapters 2, 3, 4 first draft ✅ (27/3/2026)

### Current (Phase 3: Thesis Writing)
- [ ] **Task 5.4:** Write Chapter 1 (Introduction)
- [ ] **Task 5.5:** Write Chapter 5 (Conclusion & Recommendations)
- [ ] **Task 5.6:** Write Abstract (English + Arabic)
- [ ] **Task 5.7:** Front matter & Appendices

### Upcoming (Phase 4: Expanded Experiments)
- [ ] **Task 6.1:** Literature review — chunking-aware QE and other extensions
- [ ] **Task 6.2:** Brainstorm & select approach (must build on Query2Doc logically)
- [ ] **Task 6.3:** Implement expanded experiments
- [ ] **Task 6.4:** Update thesis with new results
- [ ] **Task 6.5:** Evaluate publication potential

*Details:* See `TASKS.md`

