# Arabic RAG Query Enhancement - Graduation Project

**Project Title:** Improving Retrieval Recall in Arabic RAG Systems via Query Enhancement  
**Institution:** University of Khartoum, Faculty of Engineering  
**Team:** Mohammed Elhaj, Osman Bashir  
**Status:** Phase 1 - Implementation Planning  
**Last Updated:** January 2, 2026

---

## 🎯 Project Overview

This graduation project focuses on improving the retrieval recall of Retrieval-Augmented Generation (RAG) systems for Arabic language through query enhancement techniques. We hypothesize that standard retrieval fails due to morphological and dialectal gaps between user queries and corpus documents.

**Core Approach:** Apply query enhancement techniques to a simple RAG baseline and measure improvements in retrieval metrics.

---

## 📋 Quick Start Guide

### Essential Documents (Read First)
1. **`RESEARCH_CONTEXT_KERNEL.md.md`** - Project overview, current status, and key decisions
2. **`meetings/2.1.2026_meeting_outcomes.md`** - Complete methodology and approach finalization
3. **`research_decisions/technical_specifications.md`** - System architecture and implementation details

### For Specific Information
- **Dataset selection rationale:** `meetings/2.1.2026_meeting_outcomes.md` Section 2
- **Query enhancement techniques:** `research_decisions/technical_specifications.md` + `meetings/2.1.2026_meeting_outcomes.md` Section 4
- **Open questions and challenges:** `research_decisions/open_questions.md`
- **Expert consultation notes:** `meetings/Consultation with Mohammed Rashad.md`
- **Full meeting transcription:** `meetings/2.1.2026.md` (4 parts)

---

## 🏗️ System Architecture

```
User Query (Arabic/Dialect)
    ↓
[Query Enhancement Layer] ← Our Focus
    ↓
[Hybrid Retriever: Dense + BM25]
    ↓
Retrieved Chunks (Top-10)
    ↓
[Evaluation: Recall@10, NDCG@10]
```

**Key Components:**
- **Query Enhancement:** HyDE, Query Rewriting, Expansion, or Decomposition
- **Dense Retrieval:** Multilingual embeddings (BGE-m3, Jina AI, or Qwen)
- **Sparse Retrieval:** BM25 for keyword matching
- **Dataset:** MIRACL (Arabic subset) - 2.1M passages, ~2,896 queries

---

## 📊 Project Checkpoints

### ✅ Checkpoint 0: Planning (Completed)
- Literature review of English RAG techniques
- Dataset analysis (10+ Arabic datasets)
- Methodology finalization
- Expert consultation (Mohamed Rashad)

### 🔄 Checkpoint 1: Proof of Concept (Current)
**Goal:** Prove query enhancement improves Arabic RAG retrieval

**Tasks:**
- [ ] Select embedding model
- [ ] Implement baseline RAG system
- [ ] Implement first query enhancement technique
- [ ] Run experiments and measure improvement
- [ ] Document findings

**Timeline:** 2-3 weeks

### ⏳ Checkpoint 2: Technique Iteration
- Test multiple query enhancement approaches
- Version and compare techniques
- Identify best-performing configurations

### ⏳ Checkpoint 3: Model Generalization
- Test across different embedding models
- Validate technique-model compatibility

### ⏳ Checkpoint 4-5: Optional Extensions
- Generation impact evaluation
- Comparative benchmarking with other systems

---

## 📁 Repository Structure

```
arabic-rag-query-enhancement/
├── RESEARCH_CONTEXT_KERNEL.md.md    # Project overview and status
├── README.md                         # This file
├── meetings/
│   ├── 2.1.2026.md                  # Full meeting transcription
│   ├── 2.1.2026_meeting_outcomes.md # Structured outcomes
│   ├── Consultation with Mohammed Rashad.md
│   └── chapter2_initial_draft.md    # Thesis chapter draft
├── research_decisions/
│   ├── technical_specifications.md  # Architecture & implementation
│   └── open_questions.md            # Pending decisions & challenges
├── papers/
│   ├── 2020_RAG.md
│   ├── 2024_RQ-RAG.md
│   ├── 2025_QE-RAG.md
│   └── [other paper summaries]
├── gemini_opinions/
│   └── [strategic discussions and pivots]
└── University_of_Khartoum__EEE_bachelor_s_thesis_template/
    ├── 1-main.tex
    ├── Chapters/
    └── [thesis template files]
```

---

## 🔬 Research Methodology

### Approach: Technology-Oriented
We apply query enhancement techniques to a baseline system and analyze which problems they solve, rather than pre-defining specific problems to address.

**Rationale:**
- Safer with existing datasets (MIRACL)
- Can discover multiple problems solved by one technique
- Easier to scale experiments
- Aligns with expert advice (Mohamed Rashad)

### Dataset: MIRACL (Arabic)
**Why MIRACL?**
- ✅ Retrieval-focused (not QA generation)
- ✅ High-quality native annotations
- ✅ Natural query-document mismatch
- ✅ Gold passages + hard negatives
- ✅ Industry standard benchmark

**Limitation:** MSA-only (dialectical support deferred)

### Evaluation Metrics
- **Recall@10:** Did we retrieve relevant passages?
- **NDCG@10:** Did we rank them correctly?
- **MRR:** How quickly did we find relevant docs?

---

## 🛠️ Query Enhancement Techniques (Candidates)

1. **HyDE (Hypothetical Document Embeddings)**
   - Generate hypothetical MSA document from query
   - Use for retrieval instead of original query
   - Papers: HyDE (2022)

2. **Query Rewriting**
   - Transform dialect queries to MSA
   - Normalize morphological variations
   - LLM-based or rule-based

3. **Query Expansion**
   - Add synonyms, related terms
   - Handle Arabic morphology (roots, patterns)
   - Papers: Query2doc, QE-RAG

4. **Query Decomposition**
   - Break complex queries into sub-queries
   - Handle multi-hop reasoning
   - Papers: LevelRAG, Take a Step Back

5. **Context Injection**
   - Provide LLM with knowledge base structure
   - Inspired by Mohamed Rashad's suggestion

---

## 📚 Key References

### Papers
- **HyDE (2022):** Hypothetical Document Embeddings for zero-shot retrieval
- **RQ-RAG (2024):** Learning to Refine Queries for RAG
- **QE-RAG (2025):** Query Enhancement addressing typos and noise
- **LevelRAG (2025):** Multi-hop logic planning with query rewriting
- **RAPTOR:** Hierarchical retrieval (deemed too complex for our scope)

### Datasets
- **MIRACL:** Multilingual Information Retrieval Across a Continuum of Languages
- **Arabic QA:** 90K+ questions with difficulty labels
- **TyDi QA:** Typologically diverse QA dataset
- **Multi-Native QA:** Includes Arabic dialects

### Expert Consultations
- **Mohamed Rashad:** AI Researcher, Research Lead (Saudi Arabia)
  - Recommendation: Simple baseline + query enhancement layer
  - Advice: Avoid hierarchical complexity, scale through experiments

---

## ⚠️ Known Challenges

1. **Dialectical Gap:** MIRACL is MSA-only, may miss key Arabic challenge
2. **Evaluation Granularity:** Need to understand *what* improved, not just *that* it improved
3. **Resource Constraints:** Limited GPU, API costs, time pressure
4. **Contribution Clarity:** Unclear if adapting techniques or solving problems (will clarify after results)

See `research_decisions/open_questions.md` for full list.

---

## 📅 Timeline

- **Week 1 (Current):** Finalize embedding model, setup MIRACL, implement baseline
- **Week 2-3:** Implement first query enhancement technique, run experiments
- **Week 4:** Analyze results, document findings
- **Week 5+:** Iterate on techniques, test generalization, write thesis

---

## 👥 Team

- **Mohammed Elhaj** - Project lead, implementation
- **Osman Bashir** - Research, dataset analysis, implementation
- **Supervisor:** [To be confirmed in today's meeting]

---

## 📞 Contact

For questions or collaboration:
- Repository: [GitHub link if applicable]
- Documentation: See `RESEARCH_CONTEXT_KERNEL.md.md` for detailed project context

---

## 🔄 Document Status

**Last Updated:** January 2, 2026  
**Next Update:** After supervisor meeting and Checkpoint 1 completion  
**Maintained By:** Mohammed Elhaj, Osman Bashir

---

## 🚀 Getting Started (For New Contributors/Reviewers)

1. Read `RESEARCH_CONTEXT_KERNEL.md.md` for project overview
2. Read `meetings/2.1.2026_meeting_outcomes.md` for methodology
3. Check `research_decisions/open_questions.md` for current challenges
4. Review `research_decisions/technical_specifications.md` for implementation details
5. See `meetings/Consultation with Mohammed Rashad.md` for expert guidance

**For AI Agents:** Always check these documents before making suggestions or assumptions about the project direction.
