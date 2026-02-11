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
**Status:** ✅ Done (BM25S selected and implemented)  
**Depends On:** Task 1.2 (✅ completed)

**Why:** BM25 is our sparse retrieval baseline. Simpler than Dense (no GPU needed). Test separately per our decision.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Sparse Retrieval"
- `.kiro/steering/baseline-implementation.md` - Code patterns (use `#baseline-implementation` in chat)
- `meetings/9.1.2026_meeting_outcomes.md` - Implementation status discussed
- `meetings/23.1.2026.md` - **BM25S decision meeting**
- `reports/bm25_baseline_report.md` - Technical report on reproduction attempts

**Deliverables:**
- [x] BM25 retriever implemented (BM25S)
- [x] Can retrieve top-10 for any query
- [x] Python code execution working
- [x] Decision finalized

**Outcomes:** *(Completed 23/1/2026)*
```
DECISION: BM25S (Pure Python Implementation) ✅

RATIONALE (from 23/1/2026 meeting):
- Pure Python (no Java dependencies) - better flexibility
- 500x faster than traditional Pyserini (pre-computed scores)
- Recent (July 2024) and scientifically valid
- Results: 2% difference from MIRACL baseline (acceptable)
- Used in recent papers (2024-2026)
- Same algorithm, different implementation (optimization, not algorithm change)
- Can cite as "BM25 implemented using BM25S"

PERFORMANCE RESULTS:
- Recall@100: 0.8603 (Target: 0.889) = 96.8% achievement
- NDCG@10: 0.4610 (Target: 0.481) = 95.8% achievement  
- Recall@10: 0.5926 (Thesis metric)
- MRR: 0.4821

ADVANTAGES:
- Python-native (no Java/Pyserini complexity)
- Clean API for Query Enhancement integration
- Faster iteration for experiments
- Modern implementation (2024)

NEXT: Task 2.3 - Run full BM25S baseline experiment with documentation
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

### Task 2.3: Run BM25S Baseline Experiments
**Owner:** Osman  
**Status:** 🔄 In Progress  
**Depends On:** Task 1.4 (✅ completed), Task 1.5 (evaluation pipeline)

**Why:** Establish BM25S baseline metrics before any enhancements. Document as Experiment 002.

**Context Files:**
- `.kiro/steering/experiment-documentation.md` - Documentation template
- Task 1.4 outcomes (BM25S implementation)
- `meetings/23.1.2026.md` - Decision to use BM25S
- `docs/experiments/exp_001_baseline_dense.md` - Template reference

**Deliverables:**
- [ ] Run BM25S on full dev set (2,896 queries)
- [ ] Record all 3 metrics (Recall@10, NDCG@10, MRR)
- [ ] Create `experiments/exp_002_baseline_bm25s.md`
- [ ] Save results to `results/baseline_bm25s/`

**Outcomes:** *(In progress - 23/1/2026)*
```
Implementation: BM25S (Python-native)
Target: Complete experiment documentation following exp_001 template
Expected metrics: ~96% of MIRACL baseline (based on initial tests)

Next steps:
1. Finalize BM25S code structure
2. Run full experiment
3. Document results
4. Compare with Dense baseline (exp_001)
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
**Status:** ✅ Done (Refined in 23/1/2026 meeting)  
**Depends On:** Task 3.3 (✅ completed)

**Why:** This is a key decision that shapes Phase 2.

**Context Files:**
- Task 3.3 outcomes (error analysis)
- `research_decisions/qe_technique_selection.md` - **Decision document**
- `research_decisions/error_analysis_phase1_quantitative.md`
- `meetings/23.1.2026.md` - **Implementation approach discussion**
- `research_decisions/open_questions.md` - Technique candidates

**Deliverables:**
- [x] Decision documented
- [x] Update `research_decisions/open_questions.md`
- [x] Update `RESEARCH_CONTEXT_KERNEL.md.md`
- [x] Implementation approach clarified (23/1/2026)

**Outcomes:** *(Completed 17/1/2026, Refined 23/1/2026)*
```
DECISION: Query Expansion (LLM-based) ✅

JUSTIFICATION (Quantitative Evidence Only, N=2,896):
- Primary: Short queries achieve 59% of long query performance
- Problem: Information poverty in short queries
- Solution: Query Expansion adds context to address this gap

IMPLEMENTATION APPROACH (Refined 23/1/2026):
1. Start with Query Expansion (not HyDE initially)
2. Use small LLM that can run in Google Colab free tier
3. Simple implementation (similar to HyDE approach but for expansion)
4. Avoid API costs initially (try local models first)
5. Fallback to API if needed (Groq with GPT-OSS 20B)

LLM SELECTION: See Task 4.0 (NEW) - LLM Model Research

MONITORING STRATEGY (Discussed):
- Track quantitative improvements (query length, etc.)
- Consider Wikipedia API for metadata enrichment
- Need clear indicators of what improves

PAPERS REFERENCED:
- GRF (Generative Relevance Feedback) - 2 papers
- HyDE, Query2Doc approaches

NEXT: Task 4.0 - Research LLM models, then Task 4.1 - Implementation
```

---

## Phase 2: Query Enhancement (Weeks 4-5)

### Task 4.0: Research LLM Models for Query Expansion (NEW)
**Owner:** Mohammed  
**Status:** 🔄 In Progress  
**Depends On:** Task 3.4 (✅ completed)

**Why:** Need to identify small multilingual LLMs that can run in Google Colab free tier for Query Expansion implementation.

**Context Files:**
- `meetings/23.1.2026.md` - LLM discussion and requirements
- `research_decisions/qe_technique_selection.md` - Query Expansion decision
- `papers/2023_GRF_dense.md` - GRF/PRF approaches for reference

**Deliverables:**
- [ ] Research small multilingual LLMs (<4B parameters)
- [ ] Test models in Google Colab free tier (T4 GPU)
- [ ] Identify quantization options (4-bit, 8-bit)
- [ ] Review HyDE and Query2Doc papers for model choices
- [ ] Document findings in `research_decisions/llm_model_research.md`

**Requirements (from 23/1/2026 meeting):**
1. **Size:** Must run on T4 GPU (Colab free tier)
   - Target: 2-4B parameters
   - Consider quantized versions (4-bit, 8-bit)
2. **Language:** Multilingual with good Arabic support
3. **Capability:** Can follow prompts for query expansion/rewriting
4. **Truthfulness:** Generates accurate expansions (not hallucinations)

**Candidate Models to Research:**
- **Gemma 2B** - Google's efficient model, multilingual
- **Qwen 4B** - With quantization (initial test failed on T4)
- **GPT-OSS 20B** - Quantized via Unsloth (4-bit/8-bit)
- **Llama variants** - Small versions with quantization
- **Gemma Translator 270M** - Very small, but translation-focused

**Research Approach:**
1. Review HyDE and Query2Doc papers - what models do they use?
2. Search for "latest most powerful multilingual models" that fit constraints
3. Check model cards for Arabic performance
4. Test quantized versions in Colab
5. Evaluate prompt-following capability

**Fallback Options (if local models don't work):**
- **Groq API** with GPT-OSS 20B (8000 tokens/min rate limit)
- **Gemini 1.5 Flash** (free tier, good Arabic)
- Note: Prefer local models to avoid API costs and dependencies

**Fine-tuning Consideration:**
- Status: Deferred ("to be determined later")
- Potential approach: Use AI Studio to generate correct rewriting examples, then fine-tune
- Only if small models can't follow prompts well enough

**Outcomes:** *(Fill when complete)*
```
Selected Model: [Name]
Size: [Parameters]
Quantization: [4-bit/8-bit/none]
Arabic Performance: [Benchmark scores if available]
Colab Compatibility: [Yes/No, RAM usage]
Prompt Following: [Test results]
Fallback: [API option if needed]
```

---

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
