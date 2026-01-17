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
**Owner:** Osman  
**Status:** ✅ Done  
**Depends On:** None (can start immediately)

**Why:** MIRACL is our primary dataset (~2.1M Arabic Wikipedia passages). Need it set up before any experiments.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Dataset Specifications"
- `papers/bible.md` - MIRACL paper summary (if exists)
- `meetings/9.1.2026.md` - Dataset discussion and setup

**Deliverables:**
- [x] Dataset URLs identified on HuggingFace
- [x] Verify corpus size and structure
- [x] Document storage location and access method

**Outcomes:** *(Completed 9/1/2026)*
```
Dataset Access: HuggingFace (no local download needed - will use directly in Colab)

MIRACL Corpus URL: https://huggingface.co/datasets/miracl/miracl-corpus
MIRACL Topics/Qrels URL: https://huggingface.co/datasets/miracl/miracl

Arabic Dataset Structure:
1. Corpus (miracl-corpus):
   - 2,061,414 passages
   - 656,982 Wikipedia articles
   - Fields: docid, title, text
   - DocID format: X#Y (X = article, Y = passage number)

2. Topics & Qrels (miracl):
   - Train: 3,495 queries, 25,382 judgments
   - Dev: 2,896 queries, 29,197 judgments
   - Includes positive and negative passages (annotated by native speakers)

Pyserini Integration:
- MIRACL provides pre-built indexes via Pyserini
- Can reproduce baseline results (BM25 + mDPR) using Pyserini toolkit
- No need to manually embed corpus - pre-built indexes available

Storage Strategy:
- Access datasets directly from HuggingFace in Colab
- No Google Drive storage needed for corpus (saves ~50GB)
- Only store experiment results and processed data
```

---

### Task 1.3: Set Up Google Drive Storage
**Owner:** Mohammed  
**Status:** 🔄 In Progress  
**Depends On:** None (can start immediately)

**Why:** Need dedicated Google account for project storage and Colab integration. May upgrade to Pro (2TB) if needed.

**Context Files:**
- `meetings/6.1.2026_meeting_outcomes.md` - Resource planning discussion
- `meetings/9.1.2026.md` - Storage strategy discussion

**Deliverables:**
- [x] Dedicated Google account created
- [ ] Google Drive Pro subscription (if needed for 2TB storage)
- [ ] Folder structure created
- [ ] Sharing configured for team

**Outcomes:** *(In progress - 9/1/2026)*
```
Account Created: ✅
Email: graduation.uofk@gmail.com
Password: Uofk@2026

Storage Plan:
- Current: Free tier (15GB)
- Planned: Google Drive Pro (2TB) - pending subscription
- Note: With HuggingFace direct access, may not need full 2TB

Next Steps:
1. Decide if Pro subscription needed (based on experiment storage requirements)
2. Create folder structure for:
   - Experiment results
   - Processed data
   - Notebooks
   - Documentation
3. Share access with Osman

Storage Strategy (from 9/1/2026 meeting):
- MIRACL corpus: Access directly from HuggingFace (no Drive storage)
- Experiment results: Store in Drive
- Large embeddings: Consider HuggingFace datasets hosting if needed
```

---

### Task 1.4: Implement BM25 Baseline Retriever
**Owner:** Osman  
**Status:** 🔄 In Progress (CLI reproduction successful, Python code blocked)  
**Depends On:** Task 1.2 (✅ completed)

**Why:** BM25 is our sparse retrieval baseline. Simpler than Dense (no GPU needed). Test separately per our decision.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Sparse Retrieval"
- `.kiro/steering/baseline-implementation.md` - Code patterns (use `#baseline-implementation` in chat)
- `meetings/9.1.2026_meeting_outcomes.md` - Implementation status discussed
- `reports/bm25_baseline_report.md` - **Technical report on reproduction attempts**

**Deliverables:**
- [x] BM25 retriever implemented (preliminary notebook)
- [x] Can retrieve top-10 for any query (via CLI)
- [ ] Python code execution working (BLOCKED)
- [ ] Code finalized and pushed to repo

**Outcomes:** *(In progress - 10/1/2026)*
```
Implementation: Pyserini (using pre-built MIRACL indexes)
Technical Report: reports/bm25_baseline_report.md

SUMMARY OF ATTEMPTS:
✅ Attempt C (CLI): Successfully reproduced SOTA (Recall@100 = 0.889)
   - Environment: Python 3.8, OpenJDK 11, Pyserini 0.19.0
   - Command: python -m pyserini.search.lucene ...
   
❌ Attempt D (Python Code): BLOCKED (Recall@100 = 0.235)
   - Same environment as Attempt C
   - Issue: Python code (LuceneSearcher) falls back to System Java 21
   - Root cause: Pyjnius JVM initialization ignores Conda JAVA_HOME
   
CRITICAL BLOCKER:
Phase 2 (Query Enhancement) requires Python code execution to intercept queries
in a loop for LLM expansion. Cannot use CLI approach for this.

CURRENT STATUS:
- Environment validated ✅
- Binary dependencies fixed ✅
- Code execution BLOCKED ⚠️

NEXT STEPS:
1. Investigate JVM injection to force Java 11 in Python code
2. Consider "Scorched Earth": Remove System Java 21 entirely
3. Manual Pyjnius binding to Conda libjvm.so before import

Code location: Preliminary notebook exists, pending blocker resolution
```

**Update (12/1/2026) - BM25S Alternative Solution:**
```
ATTEMPT E: BM25S (Pure Python Implementation)

Given Pyserini blocker, implemented alternative using BM25S library:
- Library: BM25S v0.2+ (https://github.com/xhluca/bm25s)
- No Java dependencies
- Clean API for QE integration

PERFORMANCE RESULTS:
- Recall@100: 0.8603 (Target: 0.889) = 96.8% achievement
- NDCG@10: 0.4610 (Target: 0.481) = 95.8% achievement  
- Recall@10: 0.5926 (Thesis metric)
- MRR: 0.4821
```

---

### Task 1.5: Implement Evaluation Pipeline + Research Analysis Framework
**Owner:** Mohammed (Research), Osman (Implementation)  
**Status:** 🔄 In Progress (Research complete, implementation pending)  
**Depends On:** Task 1.2 (need dataset with qrels)

**Why:** Need to compute Recall@10, NDCG@10, MRR for all experiments. Build once, reuse. Also need framework for analysis/insights.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Evaluation Framework"
- `meetings/6.1.2026_meeting_outcomes.md` - Section 1.3 confirms metrics
- `meetings/9.1.2026_meeting_outcomes.md` - **Detailed pipeline design**
- `research_decisions/error_analysis_research.md` - **Error analysis research (NEW)**
- `research_decisions/evaluation_pipeline_spec.md` - **Pipeline specification (NEW)**

**Deliverables:**
- [ ] Evaluation script that computes all 3 metrics
- [ ] Tested on sample data
- [ ] Code saved to repo/Colab
- [x] **Research: Analysis framework (what insights can we extract?)** ✅ Complete
- [x] **Research: Error Analysis approach (MIRACL lacks metadata)** ✅ Complete
- [x] **Experiment documentation template** ✅ Complete

**Outcomes:** *(Research complete 14/1/2026, implementation pending)*
```
RESEARCH COMPLETED (14/1/2026):
- Error analysis research: research_decisions/error_analysis_research.md
- Pipeline specification: research_decisions/evaluation_pipeline_spec.md
- Experiment template: experiments/EXPERIMENT_TEMPLATE.md

KEY FINDINGS:
1. MIRACL has NO native metadata (confirmed by 4 research providers)
2. NoMIRACL dataset provides hard negatives (HuggingFace available)
3. Wikipedia categories can be fetched via API
4. Query-side analysis is highest ROI for our timeline

ANALYSIS FRAMEWORK:
- Immediate: Score gaps, query length correlation, rank distribution
- Short-term: Wikipedia categories, NoMIRACL hard negatives, AAFAQ taxonomy
- Advanced: Failed query clustering, LLM topic labeling

TOOLS IDENTIFIED:
- ranx: Ranking evaluation & visualization
- wikipedia-api: Category extraction
- NoMIRACL: Hard negative dataset
- pytrec_eval: Standard IR metrics

IMPLEMENTATION PENDING (Osman):
- Results saving function (JSONL format)
- Metric calculation function
- Integration with Pyserini
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
**Status:** ✅ Done  
**Depends On:** Task 2.1 (✅ decided), Task 1.2 (✅ completed)

**Why:** Dense retrieval is our second baseline. Test separately from BM25.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Dense Retrieval"
- `.kiro/steering/baseline-implementation.md` - Code patterns
- Task 2.1 outcomes - **mDPR via Pyserini**
- `meetings/9.1.2026_meeting_outcomes.md` - Implementation approach
- `reports/mdpr_baseline_report.md` - **Full technical report**

**Deliverables:**
- [x] Embedding model decided (mDPR via Pyserini pre-built index)
- [x] Dense retriever implemented
- [x] Can retrieve top-10 for any query
- [x] GPU-accelerated implementation (5-7x speedup)
- [x] Technical report documenting reproduction

**Outcomes:** *(Completed 14/1/2026)*
```
Implementation: GPU-Accelerated mDPR via Pyserini
Technical Report: reports/mdpr_baseline_report.md
Code Location: arabic-rag-query-enhancement/experiments/mDPR_baseline.ipynb
Colab Link: https://colab.research.google.com/drive/15_9-gna4tJD9ST2CLtxfIZ1p8t2HUspg 

RESULTS (MIRACL Arabic Dev Set - 2,896 queries):
✅ Recall@100: 0.8407 (Target: 0.841) = 99.96% achievement
✅ NDCG@10:    0.4993 (Target: 0.499) = 100.06% achievement
✅ Recall@10:  0.6156 (Thesis baseline metric)
✅ MRR:        0.5328

IMPLEMENTATION APPROACH:
- Manual GPU batch encoding (64 queries/batch)
- Bypassed Pyserini's slow CPU encoder
- Speed: ~2-3 minutes (vs 35 minutes CPU)
- Hardware: Google Colab T4 GPU

KEY TECHNICAL DETAILS:
- Encoder: castorini/mdpr-tied-pft-msmarco (loaded on GPU)
- Index: Pyserini pre-built FAISS (5.47 GB)
- Batch size: 64 queries
- GPU utilization: 80-90% during encoding

COMPARISON WITH BM25:
- BM25 higher Recall@100 (0.8603 vs 0.8407) - retrieves more relevant docs
- mDPR higher NDCG@10 (0.4993 vs 0.4610) - better ranking in top 10
- mDPR higher MRR (0.5328 vs 0.4821) - finds first relevant doc earlier
- Complementary strengths suggest potential for hybrid approaches

ADVANTAGES FOR PHASE 2:
✅ Clean QE integration points
✅ Fast iteration (2-3 min per experiment)
✅ No Java conflicts (unlike BM25)
✅ Modular design ready for conversion
✅ Reproducible in Colab

NEXT STEPS:
1. Convert notebook to module for QE integration
2. Design QueryEnhancer interface
3. Select first QE technique based on error analysis
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
**Owner:** Osman  
**Status:** ✅ Done  
**Depends On:** Task 2.2 (✅ completed), Task 1.5 (evaluation pipeline)

**Why:** Establish Dense baseline metrics before any enhancements.

**Context Files:**
- `.kiro/steering/experiment-documentation.md`
- Task 2.2 outcomes (retriever code)
- `docs/experiments/exp_001_baseline_dense.md` - **Full experiment documentation**

**Deliverables:**
- [x] Run on full dev set (2,896 queries)
- [x] Record all 3 metrics
- [x] Create experiment documentation
- [x] Save results to `results/baseline_dense/`

**Outcomes:** *(Completed 16/1/2026)*
```
EXPERIMENT 001: Dense Baseline (mDPR + Identity Enhancement)

RESULTS (MIRACL Arabic Dev Set - 2,896 queries):
✅ Recall@10:  0.6156 (Thesis baseline metric)
✅ Recall@100: 0.8407 (Target: 0.841) = 99.96% achievement
✅ NDCG@10:    0.4993 (Target: 0.499) = 100.06% achievement
✅ MRR:        0.5328

PERFORMANCE:
- Runtime: ~2-3 minutes (T4 GPU)
- GPU utilization: 80-90% during encoding
- Index size: 5.47 GB (cached after first run)

FILES GENERATED:
- results/baseline_dense/exp_001_baseline_dense.txt (TREC format)
- results/baseline_dense/exp_001_metrics.json (metrics)
- docs/experiments/exp_001_baseline_dense.md (documentation)

COLAB NOTEBOOK:
https://colab.research.google.com/drive/1WAqG5-fK0NTjKZFCir15x4km3a1n4P1M?usp=sharing

KEY FINDINGS:
1. Successfully reproduced MIRACL results (<0.1% difference)
2. GPU acceleration provides 5-7x speedup vs CPU
3. mDPR better at ranking (NDCG@10) than recall (vs BM25)
4. Complementary strengths with BM25 suggest hybrid potential

COMPARISON WITH BM25:
- BM25 higher Recall@100 (0.8603 vs 0.8407) - retrieves more docs
- mDPR higher NDCG@10 (0.4993 vs 0.4610) - better ranking
- mDPR higher MRR (0.5328 vs 0.4821) - finds first relevant doc earlier

NEXT STEPS:
1. Error analysis - identify which queries fail
2. Select first QE technique based on error patterns
3. Implement QE technique in src/enhancers/
4. Run Experiment 002 (QE + Dense)
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
**Status:** ✅ Done  
**Depends On:** Task 3.1 (✅ completed)

**Why:** Understanding what queries fail helps us choose the right QE technique.

**Context Files:**
- `docs/experiments/exp_001_baseline_dense.md` - Experiment documentation
- `research_decisions/error_analysis_plan_exp001.md` - Analysis plan
- `research_decisions/error_analysis_phase1_quantitative.md` - **Phase 1 results**
- `research_decisions/error_analysis_phase2_qualitative.md` - **Phase 2 results**
- `research_decisions/HANDOFF_ERROR_ANALYSIS.md` - Handoff document

**Deliverables:**
- [x] **Phase 1: Quantitative Analysis** ✅ Complete (17/1/2026)
- [x] **Phase 2: Qualitative Analysis** ✅ Complete (17/1/2026)
- [x] **Phase 3: Synthesis & Recommendation** ✅ Complete (17/1/2026)

**Outcomes:** *(Completed 17/1/2026)*
```
QUANTITATIVE FINDINGS (N=2,896 - VALIDATED):
- 39% failure rate (1,130 queries with NDCG@10 < 0.3)
- Short queries achieve 59% of long query performance (NDCG 0.240 vs 0.406)
- Query length correlation: r=0.125 (p<0.001, weak but significant)
- Retrieval vs ranking gap: 84% Recall@100 but 50% NDCG@10

KEY INSIGHT:
Information poverty (short queries) is a validated, dataset-wide driver of failure.

QUALITATIVE OBSERVATIONS (N=20 - EXPLORATORY ONLY):
- Observed spelling variations, entity mismatches, diacritics in sample
- Status: Hypotheses only, NOT used for decision-making

SCIENTIFIC REVIEW: ✅ Approved (Gemini expert review)
- Decision basis: Quantitative evidence only (short query gap)
- Qualitative findings: Labeled as exploratory hypotheses

FILES:
- ERROR_ANALYSIS_COMPLETE.md ← Main reference
- arabic-rag-query-enhancement/SCIENTIFIC_REVIEW_ERROR_ANALYSIS.md
- research_decisions/error_analysis_phase1_quantitative.md
- archive/error_analysis/ ← Process documents archived
```

---

### Task 3.4: Select First Query Enhancement Technique
**Owner:** Both  
**Status:** ✅ Done  
**Depends On:** Task 3.3 (✅ completed)

**Why:** This is a key decision that shapes Phase 2.

**Context Files:**
- Task 3.3 outcomes (error analysis)
- `research_decisions/qe_technique_selection.md` - **Decision document**
- `research_decisions/error_analysis_phase1_quantitative.md`
- `research_decisions/error_analysis_phase2_qualitative.md`
- `research_decisions/open_questions.md` - Technique candidates

**Deliverables:**
- [x] Decision documented
- [x] Update `research_decisions/open_questions.md`
- [x] Update `RESEARCH_CONTEXT_KERNEL.md.md`

**Outcomes:** *(Completed 17/1/2026)*
```
DECISION: Query Expansion with Normalization ✅

JUSTIFICATION (Quantitative Evidence Only, N=2,896):
- Primary: Short queries achieve 59% of long query performance
- Problem: Information poverty in short queries
- Solution: Query Expansion adds context to address this gap
- Secondary: Normalization as low-cost preprocessing

IMPLEMENTATION APPROACH:
1. Normalization: Fix spelling, remove diacritics, standardize spacing
2. Expansion: Use Gemini 1.5 Flash to add synonyms, entity variants, related terms

HYPOTHESIS TO TEST (Experiment 002):
Query Expansion will improve performance by addressing short query information poverty.
NO PREDICTED ROI - actual impact will be measured in Experiment 002.

ALTERNATIVE: HyDE (if expansion shows <15% improvement)

FILES:
- ERROR_ANALYSIS_COMPLETE.md ← Main reference
- research_decisions/qe_technique_selection.md
- arabic-rag-query-enhancement/SCIENTIFIC_REVIEW_ERROR_ANALYSIS.md

NEXT: Task 4.1 - Implement Query Expansion with Normalization
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
