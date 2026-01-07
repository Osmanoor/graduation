# 🧬 RESEARCH_CONTEXT_KERNEL.md
**Project:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement
**Status:** Phase 1 - Active Investigation & Baseline Setup
**Last Updated:** 6/1/2026

---

## 1. 🧭 Project Overview & Trajectory
**The Goal:** We aim to improve the retrieval recall of RAG systems for **Low-Resource Languages (specifically Arabic)**. We hypothesize that standard retrieval fails due to query-document mismatch (morphological, spelling, ambiguity issues).

**The Pivot:**
*   *Original Scope:* Broad RAG enhancement using GraphRAG and Agentic workflows.
*   *Current Scope:* Narrowed significantly to focus on **Query Enhancement (QE)** techniques. We believe fixing the input (the query) is the most high-leverage intervention.

**Important Note:** Our datasets (MIRACL, ARABICA) are MSA-only, so dialectical mismatch is NOT our primary focus anymore. Our techniques may still help with dialects, but we can't directly measure this.

## 2. 📍 Current Status: Active Investigation, Baseline Setup Starting
We are currently in the **Baseline Implementation** stage.
*   **What we have done:** 
    *   Conducted broad landscape analysis of English-centric RAG papers (HyDE, RQ-RAG, QE-RAG, etc.)
    *   Consulted with Mohamed Rashad (AI researcher) on approach
    *   Analyzed 10+ Arabic datasets for suitability
    *   Clarified decision status in 6/1/2026 review meeting
*   **What we are doing now:** 
    *   Setting up baseline RAG system with MIRACL dataset
    *   Researching embedding model options (cost vs performance)
    *   Planning parallel tasks for team members
*   **Critical Note for Agents:** We are in **active investigation** mode. Many decisions are confirmed but some remain open. Check `meetings/6.1.2026_meeting_outcomes.md` for the latest decision status. Document what we DON'T know, not just what we know.

---

## 3. Decision Status (Updated January 6, 2026)

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

---

## 4. 🔄 Under Investigation (Active Research Questions)

### A. Embedding Model Selection ⏳
**Status:** Under Investigation - Research Needed
*   *Candidates:* BGE-m3, E5 (Open Source) vs Jina AI (Closed Source)
*   *Key Tradeoff:* Open Source = free but slow iteration; Closed Source = fast iteration but API costs
*   *Concern:* Iteration speed with Open Source (hours for embedding vs API calls)
*   *Next Steps:* Research cost/performance benchmarks, calculate MIRACL embedding costs
*   *Decision Approach:* Keep as side task, don't block main work

### B. First Query Enhancement Technique ⏳
**Status:** Under Investigation - Decide After Baseline
*   *Candidates:* HyDE, Query Rewriting, Query Expansion, Query Decomposition
*   *Approach:* Build baseline first, analyze errors, then select technique
*   *Lead:* Found paper about "efficient generation augmented query rewriter" citing MIRACL - needs reading
*   *Decision Needed By:* After baseline is established

### C. Hierarchical Structures ⏳
**Status:** Interesting but Needs Feasibility Study
*   *Context:* Mohamed Rashad suggested context injection (knowledge base structure awareness)
*   *Challenge:* Is this feasible given our constraints? Does it require re-embedding?
*   *Current Stance:* Defer, focus on simpler query enhancement first

### D. Arabic LLM Selection ⏳
**Status:** Under Investigation - Current Suggestions Weak
*   *Problem:* AI suggested Jais, AceGPT - these may not be the best options
*   *Need:* Research stronger Arabic LLM models for query enhancement
*   *Use Case:* HyDE, Query Rewriting, Query Decomposition

---

## 5. 📂 Repository Structure & Knowledge Base
*The Agent should use these files to understand our accumulated knowledge.*

### Core Documentation
*   **`RESEARCH_CONTEXT_KERNEL.md.md`** (this file): Project overview, status, and decisions
*   **`meetings/6.1.2026_meeting_outcomes.md`**: Latest decision clarifications (READ THIS FIRST)
*   **`meetings/2.1.2026_meeting_outcomes.md`**: Original planning meeting outcomes
*   **`meetings/Consultation with Mohammed Rashad.md`**: Expert advisor feedback and recommendations
*   **`research_decisions/technical_specifications.md`**: System architecture, components, implementation details
*   **`research_decisions/open_questions.md`**: Pending decisions and research challenges
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
    *   `6.1.2026.md`: Decision review meeting (3 parts) - clarified AI assumptions
    *   `6.1.2026_meeting_outcomes.md`: Structured outcomes from review meeting
    *   `2.1.2026.md`: Full 4-part planning meeting transcription
    *   `2.1.2026_meeting_outcomes.md`: Original structured outcomes
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
1.  **Scale Challenge:** MIRACL has 2.1M passages - significant storage (~50GB) and compute requirements
2.  **Dialectical Gap:** MIRACL and ARABICA are MSA-only. We cannot directly test dialectical improvements.
3.  **Embedding Model Tradeoff:** Open Source = slow iteration; Closed Source = API costs
4.  **Evaluation Rigor:** Need to understand *what* improved, not just *that* it improved
5.  **Resource Constraints:** Limited GPU access, API costs, 6-week timeline
6.  **Arabic LLM Quality:** Current candidates (Jais, AceGPT) may not be optimal

**Mitigations:**
- Use Google Drive (2TB with Pro) for storage
- Use Google Colab Pro for GPU
- Use smaller subsets for prototyping (if not misleading)
- Prioritize experiments, document everything

*Details:* See `research_decisions/open_questions.md`

---

## 8. 🎯 Guidance for AI Agents
When interacting with this codebase, the Agent should:
1.  **Check Latest Status:** Read `meetings/6.1.2026_meeting_outcomes.md` FIRST for current decision status
2.  **Understand Uncertainty:** Many things are "under investigation" - don't assume decisions are final
3.  **Document What We Don't Know:** Uncertainty is valuable information
4.  **Technical Details:** Refer to `research_decisions/technical_specifications.md` for architecture
5.  **Open Questions:** Check `research_decisions/open_questions.md` before proposing solutions
6.  **Mark AI Suggestions:** Clearly label any AI suggestions as such, not as decisions
7.  **Validate:** Help formulate experiments to validate if English methods transfer to Arabic

**Key Principle:** We are in "active investigation" mode, not "blind implementation" mode.

---

## 9. 📅 Next Actions (Priority Order)

### Immediate (This Week - Jan 6-12)
- [x] Update documentation to reflect actual decision status
- [ ] Research embedding model costs/performance (side task)
- [ ] Prepare clear task list for parallel work
- [ ] Download MIRACL dataset
- [ ] Set up development environment

### Short-term (Weeks 2-3)
- [ ] Implement baseline Dense retriever
- [ ] Implement baseline BM25 retriever
- [ ] Establish evaluation pipeline (Recall@10, NDCG@10, MRR)
- [ ] Document baseline performance
- [ ] Analyze baseline errors

### Medium-term (Weeks 4-6)
- [ ] Select first query enhancement technique (based on baseline analysis)
- [ ] Implement enhancement layer
- [ ] Run experiments and iterate
- [ ] Document findings thoroughly
- [ ] Write thesis chapters

*Details:* See `meetings/6.1.2026_meeting_outcomes.md`

