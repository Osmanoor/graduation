# Project Tasks & Workflow
**Project:** Arabic RAG Query Enhancement  
**Timeline:** Jan 6 - Feb 15, 2026 (~6 weeks)  
**Team:** Mohammed Elhaj, Osman Bashir

---

## Current Phase: Baseline Implementation (Weeks 1-3)

### Week 1 Tasks (Jan 6-12)

| # | Task | Owner | Status | Depends On |
|---|------|-------|--------|------------|
| 1.1 | Research embedding model costs/performance (BGE-m3 vs Jina) | TBD | ⏳ Not Started | - |
| 1.2 | Download MIRACL Arabic dataset | TBD | ⏳ Not Started | - |
| 1.3 | Set up Google Drive storage for corpus (~50GB) | TBD | ⏳ Not Started | - |
| 1.4 | Implement BM25 baseline retriever | TBD | ⏳ Not Started | 1.2 |
| 1.5 | Implement evaluation pipeline (Recall@10, NDCG@10, MRR) | TBD | ⏳ Not Started | 1.2 |

### Week 2 Tasks (Jan 13-19)

| # | Task | Owner | Status | Depends On |
|---|------|-------|--------|------------|
| 2.1 | Decide on embedding model | Both | ⏳ Not Started | 1.1 |
| 2.2 | Implement Dense baseline retriever | TBD | ⏳ Not Started | 2.1, 1.2 |
| 2.3 | Run BM25 baseline experiments | TBD | ⏳ Not Started | 1.4, 1.5 |
| 2.4 | Document BM25 baseline results | TBD | ⏳ Not Started | 2.3 |

### Week 3 Tasks (Jan 20-26)

| # | Task | Owner | Status | Depends On |
|---|------|-------|--------|------------|
| 3.1 | Run Dense baseline experiments | TBD | ⏳ Not Started | 2.2, 1.5 |
| 3.2 | Document Dense baseline results | TBD | ⏳ Not Started | 3.1 |
| 3.3 | Analyze baseline errors (which queries fail?) | Both | ⏳ Not Started | 2.4, 3.2 |
| 3.4 | Select first query enhancement technique | Both | ⏳ Not Started | 3.3 |

---

## Phase 2: Query Enhancement (Weeks 4-5)

| # | Task | Owner | Status | Depends On |
|---|------|-------|--------|------------|
| 4.1 | Implement first QE technique | TBD | ⏳ Not Started | 3.4 |
| 4.2 | Run QE experiments on BM25 | TBD | ⏳ Not Started | 4.1 |
| 4.3 | Run QE experiments on Dense | TBD | ⏳ Not Started | 4.1 |
| 4.4 | Document QE results | TBD | ⏳ Not Started | 4.2, 4.3 |
| 4.5 | Analyze improvements (what improved, why?) | Both | ⏳ Not Started | 4.4 |
| 4.6 | Iterate on technique if needed | TBD | ⏳ Not Started | 4.5 |

---

## Phase 3: Documentation & Writing (Week 6)

| # | Task | Owner | Status | Depends On |
|---|------|-------|--------|------------|
| 5.1 | Write Methodology chapter | TBD | ⏳ Not Started | 4.5 |
| 5.2 | Write Experiments chapter | TBD | ⏳ Not Started | 4.5 |
| 5.3 | Update Chapter 2 (Literature Review) | TBD | ⏳ Not Started | - |
| 5.4 | Prepare final presentation | Both | ⏳ Not Started | 5.1, 5.2 |

---

## Task Assignment Guidelines

**Parallelizable Tasks (can split between Mohammed & Osman):**
- 1.1 and 1.2 can run in parallel
- 1.4 (BM25) and research tasks can run in parallel
- 4.2 (BM25+QE) and 4.3 (Dense+QE) can run in parallel

**Sequential Dependencies:**
- Must have dataset (1.2) before any retriever implementation
- Must have evaluation pipeline (1.5) before any experiments
- Must have baseline results before selecting QE technique

---

## How to Update This File

When completing a task:
1. Change status from `⏳ Not Started` to `✅ Done`
2. Add completion date
3. Link to experiment doc if applicable: `See experiments/exp_001.md`

Status options:
- `⏳ Not Started`
- `🔄 In Progress`
- `✅ Done`
- `❌ Blocked` (add reason)

---

## Quick Links

- **Project Context:** `RESEARCH_CONTEXT_KERNEL.md.md`
- **Latest Decisions:** `meetings/6.1.2026_meeting_outcomes.md`
- **Technical Specs:** `research_decisions/technical_specifications.md`
- **Open Questions:** `research_decisions/open_questions.md`
- **Experiment Docs:** `experiments/`
