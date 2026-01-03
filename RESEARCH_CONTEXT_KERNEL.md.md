# 🧬 RESEARCH_CONTEXT_KERNEL.md
**Project:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement
**Status:** Phase 1 - Foundational Investigation & Validation
**Last Updated:** 1/1/2026

---

## 1. 🧭 Project Overview & Trajectory
**The Goal:** We aim to improve the retrieval recall of RAG systems for **Low-Resource Languages (specifically Arabic)**. We hypothesize that standard retrieval fails due to the "Morphological & Dialectal Gap" (mismatch between user queries and corpus documents).
**The Pivot:**
*   *Original Scope:* Broad RAG enhancement using GraphRAG and Agentic workflows.
*   *Current Scope:* Narrowed significantly to focus on **Query Enhancement (QE)** techniques. We believe fixing the input (the query) is the most high-leverage intervention for Arabic morphology and dialects.

## 2. 📍 Current Status: Methodology Finalized, Implementation Starting
We are currently in the **Implementation Planning** stage.
*   **What we have done:** 
    *   Conducted broad landscape analysis of English-centric RAG papers (HyDE, RQ-RAG, QE-RAG, etc.)
    *   Consulted with Mohamed Rashad (AI researcher) on approach
    *   Analyzed 10+ Arabic datasets for suitability
    *   Finalized research methodology and approach
*   **What we are doing now:** 
    *   Setting up baseline RAG system with MIRACL dataset
    *   Selecting embedding model for experiments
    *   Preparing to implement first query enhancement technique
*   **Critical Note for Agents:** We have **finalized** our approach (simple baseline + query enhancement layer) and dataset (MIRACL primary). See `meetings/2.1.2026_meeting_outcomes.md` for full decisions.

---

## 3. ✅ Finalized Decisions (January 2, 2026)

### A. The Dataset: **MIRACL (Arabic subset)** ✓
**Decision:** Use MIRACL as primary dataset for all initial experiments.
*   **Rationale:** Retrieval-focused, high-quality native annotations, natural query-document mismatch, gold passages, hard negatives
*   **Secondary:** Arabic QA (90K questions with difficulty labels) for generalization testing
*   **Limitation:** MSA-only (dialectical support deferred to later checkpoint)
*   **Details:** See `meetings/2.1.2026_meeting_outcomes.md` Section 2

### B. The Baseline Pipeline: **Hybrid (Dense + BM25)** ✓
**Decision:** Implement hybrid retrieval as baseline.
*   **Dense:** Multilingual embedding model (BGE-m3, Jina AI, or Qwen - selection in progress)
*   **Sparse:** BM25 for keyword matching
*   **Rationale:** Represents realistic RAG system, resource-friendly, complementary strengths
*   **Details:** See `research_decisions/technical_specifications.md`

### C. The Approach: **Simple Baseline + Query Enhancement Layer** ✓
**Decision:** Focus on query enhancement techniques applied to simple RAG baseline.
*   **Architecture:** User Query → [Query Enhancement Layer] → [Hybrid Retriever] → Retrieved Chunks
*   **Evaluation:** Retrieval metrics only initially (Recall@10, NDCG@10)
*   **Rationale:** Based on Mohamed Rashad's advice - avoid complex hierarchical structures, scale through experiments
*   **Details:** See `meetings/Consultation with Mohammed Rashad.md`

---

## 4. 🔄 Pending Decisions (Active Research Questions)

### A. Embedding Model Selection (In Progress)
*   *Candidates:* BGE-m3, Jina AI, Qwen, E5
*   *Next Steps:* Benchmark on MIRACL sample, measure Recall@10 and inference time
*   *Decision Needed By:* End of this week

### B. First Query Enhancement Technique (Pending)
*   *Candidates:* HyDE, Query Rewriting, Query Expansion, Query Decomposition
*   *Current Preference:* HyDE or Query Rewriting
*   *Decision Needed By:* After baseline is established
*   *Details:* See `research_decisions/open_questions.md`

### C. Problem-Oriented vs. Technology-Oriented (Pending Supervisor Input)
*   *Current Stance:* Technology-oriented (apply techniques, discover what they solve)
*   *Alternative:* Problem-oriented (target specific challenge like dialectical mismatch)
*   *Decision Needed By:* Today's supervisor meeting

---

## 4. 📂 Repository Structure & Knowledge Base
*The Agent should use these files to understand our accumulated knowledge.*

### Core Documentation
*   **`RESEARCH_CONTEXT_KERNEL.md.md`** (this file): Project overview, status, and decisions
*   **`meetings/2.1.2026_meeting_outcomes.md`**: Complete outcomes from methodology finalization meeting
*   **`meetings/Consultation with Mohammed Rashad.md`**: Expert advisor feedback and recommendations
*   **`research_decisions/technical_specifications.md`**: System architecture, components, implementation details
*   **`research_decisions/open_questions.md`**: Pending decisions and research challenges

### Strategic Discussions
*   **`/gemini_opinions/`**: Contains strategic discussions, pivots, and "Project Management" decisions.
    *   *Key File:* `Branch of Critical Feedback...` (Explains why we dropped GraphRAG).
    *   *Key File:* `Branch of RQ-RAG...` (Analysis of the "Active Generator" architecture).

### Literature Review
*   **`/papers/`**: Contains raw summaries of the academic literature we have read.
    *   *Key Insight:* We have analyzed `QE-RAG.md` (Query Noise), `RQ-RAG.md` (Iterative Feedback), and `Optimizing RAG Pipelines for Arabic.md` (Baseline components).

### Meeting Records
*   **`/meetings/`**: Full transcriptions and summaries of planning sessions
    *   `2.1.2026.md`: Full 4-part meeting transcription
    *   `2.1.2026_meeting_outcomes.md`: Structured outcomes and decisions
    *   `Consultation with Mohammed Rashad.md`: Expert consultation notes

---

## 5. 🎯 Project Checkpoints & Scaling Strategy

### Checkpoint 1: Proof of Concept ✓ (Current Focus)
**Goal:** Prove query enhancement improves Arabic RAG retrieval
*   **Fixed:** Single embedding model, MIRACL dataset, one technique
*   **Success:** Measurable improvement in Recall@10, NDCG@10
*   **Timeline:** Next 2-3 weeks

### Checkpoint 2: Technique Iteration
**Goal:** Test multiple query enhancement approaches
*   **Experiments:** HyDE v0.1-v0.3, Query Rewriting, Expansion, Decomposition
*   **Versioning:** Track improvements across technique variations

### Checkpoint 3: Model Generalization
**Goal:** Test across different embedding models
*   **Models:** BGE-m3, Jina AI, Qwen, E5
*   **Insight:** Some techniques may work better with specific models

### Checkpoint 4: Generation Impact (Optional)
**Goal:** Measure end-to-end RAG performance
*   **Metrics:** F1 Score, Exact Match, Truthfulness

### Checkpoint 5: Comparative Benchmarking (Optional)
**Goal:** Compare with other RAG systems
*   **Comparisons:** Other papers, hierarchical approaches, standard baselines

*Details:* See `meetings/2.1.2026_meeting_outcomes.md` Section 3

---

## 6. ⚠️ Current Challenges & Risks
1.  **Dialectical Gap:** MIRACL is MSA-only. We risk missing a key Arabic challenge (dialectical mismatch). Mitigation: Defer to Checkpoint 2 or use secondary dataset.
2.  **Evaluation Rigor:** Need to understand *what* improved, not just *that* it improved. Mitigation: Error analysis, query categorization, qualitative case studies.
3.  **Resource Constraints:** Limited GPU access, API costs, time pressure. Mitigation: Use free tiers, prioritize experiments, cache embeddings.
4.  **Synthetic Data Bias:** If we generate data, queries may be too similar to documents. Mitigation: Use MIRACL (native queries) for primary experiments.
5.  **Contribution Clarity:** Unclear if we're adapting techniques or solving problems. Mitigation: Clarify after Checkpoint 1 results, frame based on findings.

*Details:* See `research_decisions/open_questions.md`

---

## 7. 🎯 Immediate Agent Objectives
When interacting with this codebase, the Agent should:
1.  **Reference Decisions:** Check `meetings/2.1.2026_meeting_outcomes.md` for finalized decisions before suggesting alternatives.
2.  **Technical Details:** Refer to `research_decisions/technical_specifications.md` for architecture and implementation details.
3.  **Open Questions:** Check `research_decisions/open_questions.md` before proposing solutions to known challenges.
4.  **Synthesize:** Read the `/papers/` summaries to find connections between English methods and Arabic problems.
5.  **Document:** Update this kernel and related documents as new decisions are made.
6.  **Validate:** Help formulate experiments to validate if English methods transfer to Arabic.

---

## 8. 📅 Next Actions (Priority Order)

### Today (2/1/2026)
- [x] Document meeting outcomes
- [ ] Generate Chapter 2 draft for thesis
- [ ] Prepare presentation slides for supervisor meeting
- [ ] Attend supervisor meeting and get feedback

### This Week
- [ ] Finalize embedding model selection
- [ ] Download and preprocess MIRACL dataset
- [ ] Implement baseline RAG system (Dense + BM25)
- [ ] Establish evaluation pipeline
- [ ] Document baseline performance

### Next 2 Weeks
- [ ] Select first query enhancement technique
- [ ] Implement enhancement layer
- [ ] Run Checkpoint 1 experiments
- [ ] Analyze results and document findings
- [ ] Update research context with learnings

*Details:* See `meetings/2.1.2026_meeting_outcomes.md` Section 9

