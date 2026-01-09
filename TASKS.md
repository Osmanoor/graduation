# Project Tasks
**Project:** Arabic RAG Query Enhancement  
**Timeline:** Jan 6 - Feb 15, 2026 (~6 weeks)  
**Team:** Mohammed Elhaj, Osman Bashir

---

## How to Use This File

1. **Starting work:** Trigger "Daily Research Standup" hook → Pick a task
2. **During work:** Reference the context files listed for that task
3. **After completing:** Update status, add outcomes, update related context files

---

## Phase 1: Baseline Implementation (Weeks 1-3)

### Task 1.1: Research Embedding Model Options
**Owner:** Mohammed  
**Status:** ✅ Done  
**Depends On:** None

**Why:** We need to decide between open-source (BGE-m3, E5) vs closed-source (Jina AI). This affects iteration speed and costs.

**Context Files:**
- `research_decisions/open_questions.md` - Section "Embedding Model Selection"
- `research_decisions/technical_specifications.md` - Section "Embedding Model Selection"
- `meetings/6.1.2026_meeting_outcomes.md` - Section 1.2 discusses the tradeoffs
- `research_decisions/embedding_model_research.md` - **Full research document**
- `meetings/9.1.2026_meeting_outcomes.md` - **Decision meeting outcomes**

**Deliverables:**
- [x] Cost comparison document
- [x] Performance benchmarks for Arabic
- [x] Recommendation with justification
- [x] **Final decision (discussed with Osman 9/1/2026)**

**Outcomes:** *(Completed 9/1/2026)*
```
Decision made: Yes - Use Pyserini pre-built indexes initially
Research document: research_decisions/embedding_model_research.md

Key findings:
1. Swan models (UBC-NLP) - NOT AVAILABLE (models not released)
2. Pre-built Pyserini indexes available for MIRACL Arabic (mDPR)
3. BGE-M3: Best Arabic results (80.2 nDCG@10), multi-functional
4. mE5-large: Trained on MIRACL (76.0 nDCG@10), well-documented
5. Jina-v3: Free API (10M tokens), but not evaluated on MIRACL

Paper summaries created:
- papers/2024_BGE-M3.md
- papers/2024_Multilingual_E5.md
- papers/2024_Jina_Embeddings_v3.md

DECISION (9/1/2026 meeting):
- Start with Pyserini pre-built indexes (BM25 + mDPR) for fastest iteration
- mDPR chosen intentionally as "weaker" baseline (not fine-tuned on MIRACL)
- This gives more room for Query Enhancement improvement
- Future: Test QE techniques on stronger models (BGE-M3, E5) after initial results
```

---

### Task 1.2: Download MIRACL Arabic Dataset
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** None (can start immediately)

**Why:** MIRACL is our primary dataset (~2.1M Arabic Wikipedia passages). Need it set up before any experiments.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Dataset Specifications"
- `papers/bible.md` - MIRACL paper summary (if exists)

**Deliverables:**
- [ ] Dataset downloaded to Google Drive
- [ ] Verify corpus size and structure
- [ ] Document storage location

**Outcomes:** *(Fill when complete)*
```
Storage location: [Google Drive path]
Corpus size: [X passages]
Query count: [X queries]
Issues encountered: [Any problems]
```

---

### Task 1.3: Set Up Google Drive Storage
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** None (can start immediately)

**Why:** MIRACL corpus is ~50GB. Need Google Drive Pro (2TB) for storage.

**Context Files:**
- `meetings/6.1.2026_meeting_outcomes.md` - Resource planning discussion

**Deliverables:**
- [ ] Google Drive Pro subscription active
- [ ] Folder structure created
- [ ] Sharing configured for team

**Outcomes:** *(Fill when complete)*
```
Drive path: [Path]
Storage used: [X GB]
Shared with: [Team members]
```

---

### Task 1.4: Implement BM25 Baseline Retriever
**Owner:** Osman  
**Status:** 🔄 In Progress (Preliminary notebook exists, needs finalization)  
**Depends On:** Task 1.2 (need dataset)

**Why:** BM25 is our sparse retrieval baseline. Simpler than Dense (no GPU needed). Test separately per our decision.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Sparse Retrieval"
- `.kiro/steering/baseline-implementation.md` - Code patterns (use `#baseline-implementation` in chat)
- `meetings/9.1.2026_meeting_outcomes.md` - Implementation status discussed

**Deliverables:**
- [x] BM25 retriever implemented (preliminary notebook)
- [ ] Can retrieve top-10 for any query
- [ ] Code finalized and pushed to repo

**Outcomes:** *(In progress - 9/1/2026)*
```
Implementation: Pyserini (using pre-built MIRACL indexes)
Code location: Preliminary notebook exists (Osman), needs push to repo
Status: Working but needs cleanup and documentation
Next step: Osman to finalize and push notebook
```

---

### Task 1.5: Implement Evaluation Pipeline + Research Analysis Framework
**Owner:** Mohammed (Research), Osman (Implementation)  
**Status:** 🔄 In Progress (Design clarified, needs implementation)  
**Depends On:** Task 1.2 (need dataset with qrels)

**Why:** Need to compute Recall@10, NDCG@10, MRR for all experiments. Build once, reuse. Also need framework for analysis/insights.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Evaluation Framework"
- `meetings/6.1.2026_meeting_outcomes.md` - Section 1.3 confirms metrics
- `meetings/9.1.2026_meeting_outcomes.md` - **Detailed pipeline design**

**Deliverables:**
- [ ] Evaluation script that computes all 3 metrics
- [ ] Tested on sample data
- [ ] Code saved to repo/Colab
- [ ] **Research: Analysis framework (what insights can we extract?)**
- [ ] **Research: Error Analysis approach (MIRACL lacks metadata)**

**Outcomes:** *(Design clarified 9/1/2026, implementation pending)*
```
PIPELINE DESIGN (from 9/1/2026 meeting):

Two-Phase Approach:
1. EXPERIMENT PHASE: Run search → Save results to file
2. EVALUATION PHASE: Calculate metrics from saved results

Storage Format:
- Save as IDs only (Query ID + Passage ID) - NOT full passages
- Save top 100 results per query (can extract top 10 later)
- Lightweight, easy to store

Two Purposes:
1. Documentation for thesis (show our work)
2. Context for incremental improvement (act as context for Kiro/team)

Experiment Documentation (MD file per experiment):
- Why we started the experiment
- Parameters/setup used
- Prompts used (if any)
- Results and immediate effects
- Concise but comprehensive

RESEARCH NEEDED (Osman's suggestion):
- What analysis/insights can we extract from results?
- How to do Error Analysis when MIRACL lacks metadata?
- Find if anyone created metadata for MIRACL passages
- Framework for transforming results → reports → insights
```

---

### Task 2.1: Decide on Embedding Model
**Owner:** Both  
**Status:** ✅ Done  
**Depends On:** Task 1.1 (need research complete)

**Why:** Can't implement Dense baseline without this decision.

**Context Files:**
- Task 1.1 outcomes
- `research_decisions/open_questions.md`
- `meetings/9.1.2026_meeting_outcomes.md` - **Decision meeting**

**Deliverables:**
- [x] Decision documented in `research_decisions/open_questions.md`
- [x] Update `RESEARCH_CONTEXT_KERNEL.md.md` to mark as decided

**Outcomes:** *(Completed 9/1/2026)*
```
Decision: Pyserini pre-built indexes (BM25 + mDPR) for initial baselines

Rationale:
1. Fastest path to implement Query Enhancement techniques
2. mDPR intentionally "weaker" (not fine-tuned on MIRACL) = more room for improvement
3. Avoids 12-15 hour embedding time on Colab
4. Query Enhancement is our main contribution, not beating already-trained models

Future Plan:
- After testing QE techniques on mDPR baseline
- Try stronger models (BGE-M3, E5) to see how improvement scales

Updated files: TASKS.md, research_decisions/open_questions.md, RESEARCH_CONTEXT_KERNEL.md.md
```

---

### Task 2.2: Implement Dense Baseline Retriever
**Owner:** Osman  
**Status:** 🔄 In Progress (Using Pyserini pre-built mDPR index)  
**Depends On:** Task 2.1 (✅ decided), Task 1.2 (need dataset)

**Why:** Dense retrieval is our second baseline. Test separately from BM25.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Dense Retrieval"
- `.kiro/steering/baseline-implementation.md` - Code patterns
- Task 2.1 outcomes - **mDPR via Pyserini**
- `meetings/9.1.2026_meeting_outcomes.md` - Implementation approach

**Deliverables:**
- [x] Embedding model decided (mDPR via Pyserini pre-built index)
- [ ] Dense retriever implemented
- [ ] Can retrieve top-10 for any query

**Outcomes:** *(In progress - 9/1/2026)*
```
Embedding model: mDPR (Pyserini pre-built index)
Index type: Pyserini pre-built FAISS index
Code location: To be added to same notebook as BM25
Embedding time: N/A - using pre-built index (no embedding needed!)

Note: mDPR chosen as "weaker" baseline (not fine-tuned on MIRACL)
This is intentional - gives more room for Query Enhancement improvement
```

---

### Task 2.3: Run BM25 Baseline Experiments
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 1.4, Task 1.5

**Why:** Establish BM25 baseline metrics before any enhancements.

**Context Files:**
- `.kiro/steering/experiment-documentation.md` - Documentation template
- Task 1.4 outcomes (retriever code)
- Task 1.5 outcomes (evaluation code)

**Deliverables:**
- [ ] Run on full dev set (or document subset size)
- [ ] Record all 3 metrics
- [ ] Create `experiments/exp_001_baseline_bm25.md`

**Outcomes:** *(Fill when complete)*
```
Recall@10: [X.XXX]
NDCG@10: [X.XXX]
MRR: [X.XXX]
Dataset: [Full / subset of X]
Experiment doc: experiments/exp_001_baseline_bm25.md
```

---

### Task 2.4: Document BM25 Baseline Results
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 2.3

**Why:** Proper documentation for thesis and future reference.

**Context Files:**
- Task 2.3 outcomes
- `.kiro/steering/experiment-documentation.md`

**Deliverables:**
- [ ] Complete experiment doc with analysis
- [ ] Update `RESEARCH_CONTEXT_KERNEL.md.md` with baseline numbers
- [ ] Note any interesting observations

**Outcomes:** *(Fill when complete)*
```
Experiment doc: [Path]
Key observations: [What we learned]
Context files updated: [List]
```

---

### Task 3.1: Run Dense Baseline Experiments
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 2.2, Task 1.5

**Why:** Establish Dense baseline metrics before any enhancements.

**Context Files:**
- `.kiro/steering/experiment-documentation.md`
- Task 2.2 outcomes (retriever code)

**Deliverables:**
- [ ] Run on full dev set (or document subset size)
- [ ] Record all 3 metrics
- [ ] Create `experiments/exp_002_baseline_dense.md`

**Outcomes:** *(Fill when complete)*
```
Recall@10: [X.XXX]
NDCG@10: [X.XXX]
MRR: [X.XXX]
Embedding model: [Model used]
Experiment doc: experiments/exp_002_baseline_dense.md
```

---

### Task 3.2: Document Dense Baseline Results
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 3.1

**Why:** Proper documentation for thesis and future reference.

**Context Files:**
- Task 3.1 outcomes
- `.kiro/steering/experiment-documentation.md`

**Deliverables:**
- [ ] Complete experiment doc with analysis
- [ ] Update `RESEARCH_CONTEXT_KERNEL.md.md` with baseline numbers
- [ ] Compare with BM25 results

**Outcomes:** *(Fill when complete)*
```
Experiment doc: [Path]
Comparison with BM25: [Which is better, by how much]
Context files updated: [List]
```

---

### Task 3.3: Analyze Baseline Errors
**Owner:** Both  
**Status:** ⏳ Not Started  
**Depends On:** Task 2.4, Task 3.2

**Why:** Understanding what queries fail helps us choose the right QE technique.

**Context Files:**
- `experiments/exp_001_baseline_bm25.md`
- `experiments/exp_002_baseline_dense.md`
- `research_decisions/open_questions.md` - Section on first technique selection

**Deliverables:**
- [ ] List of query types that fail
- [ ] Hypotheses about why they fail
- [ ] Recommendations for which QE technique to try

**Outcomes:** *(Fill when complete)*
```
Common failure patterns: [List]
Hypotheses: [Why queries fail]
Recommended technique: [HyDE / Rewriting / etc]
Analysis doc: [Path if created]
```

---

### Task 3.4: Select First Query Enhancement Technique
**Owner:** Both  
**Status:** ⏳ Not Started  
**Depends On:** Task 3.3

**Why:** This is a key decision that shapes Phase 2.

**Context Files:**
- Task 3.3 outcomes (error analysis)
- `research_decisions/open_questions.md` - Technique candidates
- `papers/` - Relevant paper summaries

**Deliverables:**
- [ ] Decision documented
- [ ] Update `research_decisions/open_questions.md`
- [ ] Update `RESEARCH_CONTEXT_KERNEL.md.md`

**Outcomes:** *(Fill when complete)*
```
Chosen technique: [Name]
Rationale: [Why this one based on error analysis]
Updated files: [List]
```

---

## Phase 2: Query Enhancement (Weeks 4-5)

### Task 4.1: Implement First QE Technique
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 3.4

**Context Files:**
- Task 3.4 outcomes (which technique)
- `research_decisions/technical_specifications.md` - QE section
- Relevant paper in `papers/`

**Deliverables:**
- [ ] QE layer implemented
- [ ] Can enhance any query
- [ ] Code saved

**Outcomes:** *(Fill when complete)*
```
Technique: [Name]
Implementation: [Approach used]
Code location: [Path]
```

---

### Task 4.2: Run QE + BM25 Experiments
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 4.1

**Context Files:**
- Task 4.1 outcomes
- `experiments/exp_001_baseline_bm25.md` (baseline to compare)

**Deliverables:**
- [ ] Run enhanced queries through BM25
- [ ] Record all 3 metrics
- [ ] Create `experiments/exp_003_qe_bm25.md`

**Outcomes:** *(Fill when complete)*
```
Recall@10: [X.XXX] (baseline was [X.XXX])
NDCG@10: [X.XXX] (baseline was [X.XXX])
MRR: [X.XXX] (baseline was [X.XXX])
Improvement: [+X.X% / -X.X%]
```

---

### Task 4.3: Run QE + Dense Experiments
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 4.1

**Context Files:**
- Task 4.1 outcomes
- `experiments/exp_002_baseline_dense.md` (baseline to compare)

**Deliverables:**
- [ ] Run enhanced queries through Dense
- [ ] Record all 3 metrics
- [ ] Create `experiments/exp_004_qe_dense.md`

**Outcomes:** *(Fill when complete)*
```
Recall@10: [X.XXX] (baseline was [X.XXX])
NDCG@10: [X.XXX] (baseline was [X.XXX])
MRR: [X.XXX] (baseline was [X.XXX])
Improvement: [+X.X% / -X.X%]
```

---

### Task 4.4: Document QE Results & Analysis
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Task 4.2, Task 4.3

**Context Files:**
- All experiment docs
- `.kiro/steering/experiment-documentation.md`

**Deliverables:**
- [ ] Complete analysis of what improved
- [ ] Update `RESEARCH_CONTEXT_KERNEL.md.md`
- [ ] Decide if iteration needed

**Outcomes:** *(Fill when complete)*
```
Overall improvement: [Summary]
Best configuration: [QE + BM25 or QE + Dense]
Next steps: [Iterate / Move to writing]
```

---

## Phase 3: Documentation & Writing (Week 6)

### Task 5.1: Write Methodology Chapter
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Phase 2 complete

**Context Files:**
- `research_decisions/technical_specifications.md`
- All experiment docs in `experiments/`
- `.kiro/steering/thesis-writing.md`

---

### Task 5.2: Write Experiments/Results Chapter
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** Phase 2 complete

**Context Files:**
- All experiment docs in `experiments/`
- `.kiro/steering/thesis-writing.md`

---

### Task 5.3: Update Literature Review (Chapter 2)
**Owner:** TBD  
**Status:** ⏳ Not Started  
**Depends On:** None

**Context Files:**
- `meetings/chapter2_initial_draft.md`
- `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter2_generated.tex`
- All papers in `papers/`

---

## Status Legend

- ⏳ Not Started
- 🔄 In Progress
- ✅ Done
- ❌ Blocked (add reason in outcomes)

---

## Quick Links

| Document | Purpose |
|----------|---------|
| `RESEARCH_CONTEXT_KERNEL.md.md` | Project state & decisions |
| `WORKFLOW.md` | How we work |
| `research_decisions/technical_specifications.md` | Architecture details |
| `research_decisions/open_questions.md` | Undecided items |
| `experiments/` | Experiment documentation |
