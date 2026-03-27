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
**Status:** ✅ Done (BM25S approach)  
**Depends On:** Task 1.2 (✅ completed)

**Why:** BM25 is our sparse retrieval baseline. Simpler than Dense (no GPU needed). Test separately per our decision.

**Context Files:**
- `research_decisions/technical_specifications.md` - Section "Sparse Retrieval"
- `.kiro/steering/baseline-implementation.md` - Code patterns (use `#baseline-implementation` in chat)
- `meetings/9.1.2026_meeting_outcomes.md` - Implementation status discussed
- `reports/bm25_baseline_report.md` - **Technical report on reproduction attempts**
- `src/retrievers/bm25.py` - **Final BM25S implementation**

**Deliverables:**
- [x] BM25 retriever implemented (BM25S library)
- [x] Can retrieve top-10 for any query
- [x] Python code execution working
- [x] Code finalized and pushed to repo

**Outcomes:** *(Completed 26/1/2026)*
```
DECISION: Implement using BM25S (Approach E)

After Pyserini blocker (Java 21 vs Java 11 conflict), switched to pure Python solution:

Implementation: BM25S Library
- Library: bm25s v0.2+ (https://github.com/xhluca/bm25s)
- No Java dependencies
- Clean API for QE integration
- Pure Python implementation

IMPLEMENTATION DETAILS:
- Tokenization: Arabic stemming (PyStemmer) + NLTK stopwords (245+ words)
- BM25 Parameters: k1=0.9, b=0.4 (Lucene-style)
- Index Storage: Google Drive (~5GB)
- Loading: Symbolic links in Colab

TRADE-OFF ACCEPTED:
- 96% of Pyserini performance (vs 100%)
- Benefits: No Java, easier QE integration, pure Python
- Conclusion: Acceptable trade-off for thesis goals

BLOCKER RESOLUTION:
- Original blocker: Pyserini Java 21 vs Java 11 conflict
- Solution: Switch to BM25S (pure Python)
- Status: ✅ Resolved and implemented
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
**Owner:** Osman  
**Status:** ✅ Done  
**Depends On:** Task 1.4, Task 1.5

**Why:** Establish BM25 baseline metrics before any enhancements.

**Context Files:**
- `.kiro/steering/experiment-documentation.md` - Documentation template
- Task 1.4 outcomes (retriever code)
- Task 1.5 outcomes (evaluation code)
- `docs/experiments/exp_002_baseline_bm25.md` - **Full experiment documentation**

**Deliverables:**
- [x] Run on full dev set (2,896 queries)
- [x] Record all 3 metrics
- [x] Create experiment documentation
- [x] Save results to `results/baseline_bm25/`

**Outcomes:** *(Completed 26/1/2026)*
```
EXPERIMENT 002: BM25 Baseline (BM25S + Identity Enhancement)

RESULTS (MIRACL Arabic Dev Set - 2,896 queries):
✅ Recall@10:  0.5964 (Thesis baseline metric)
✅ Recall@100: 0.8577 (Target: 0.889) = 96.48% achievement
✅ NDCG@10:    0.4621 (Target: 0.481) = 96.07% achievement
✅ MRR:        0.4836

FILES GENERATED:
- results/baseline_bm25/exp_002_baseline_bm25.txt (TREC format)
- results/baseline_bm25/exp_002_metrics.json (metrics)
- docs/experiments/exp_002_baseline_bm25.md (documentation)

COLAB NOTEBOOK:
https://colab.research.google.com/drive/1AJmPYlLrhY1kLbwTWF2Ga7AyXWNWYemh

KEY FINDINGS:
1. Achieved 96%+ of Pyserini target (acceptable for pure Python)
2. Higher Recall@100 than mDPR (0.8577 vs 0.8407) = +2.0%
3. Lower NDCG@10 than mDPR (0.4621 vs 0.4993) = -7.5%
4. Complementary strengths: BM25 better at recall, mDPR better at ranking

COMPARISON WITH DENSE (Exp 001):
- BM25 retrieves more relevant docs (higher Recall@100)
- mDPR ranks them better (higher NDCG@10, MRR)
- Suggests potential for hybrid approaches

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

### Task 4.0: Research LLM Models for Query Expansion
**Owner:** Mohammed
**Status:** ✅ Done (Research complete)
**Depends On:** Task 3.4 (✅ completed)

**Why:** Identify multilingual LLMs for Arabic Query Expansion on Google Colab.

**Context Files:**
- `research_decisions/llm_model_research.md` - **Full research document**
- `research_decisions/models_reserch.md` - **ChatGPT Deep Research raw output**
- `research_decisions/model_comparison_guide.md` - **Model comparison experiment guide**
- `meetings/23.1.2026.md` - LLM discussion and requirements

**Deliverables:**
- [x] Research multilingual LLMs (2-8B parameters, open-source focus)
- [x] Review 15 QE papers for model choices (8 foundational + 7 from Deep Research)
- [x] Identify quantization options (4-bit via bitsandbytes)
- [x] Identify 10 open-source candidate models with Arabic benchmarks (OALL)
- [x] Map API options with pricing for fallback
- [x] Document findings in `research_decisions/llm_model_research.md`
- [x] Create model comparison guide: `research_decisions/model_comparison_guide.md`

**Outcomes:** *(Completed 11/2/2026)*
```
RESEARCH COMPLETED (11/2/2026):

Phase 1: Literature Review (15 papers)
- All foundational QE papers used 175B models (GPT-3)
- Query2Doc (2023) tested small models (OPT-1.3B/6.7B) → failed
- BUT 2024-2025 papers prove modern 7-8B models work (CSQE, MUGI, KAR, ThinkQE)
- CSQE: Llama2-7B gave +30% mAP over BM25
- No paper tested modern 2-4B for zero-shot Arabic QE → our research gap

Phase 2: Model Discovery
- 10 open-source candidates identified and ranked by Arabic quality
- Arabic-specialized: Falcon-H1-Arabic-3B (~62% OALL), Jais-2-8B (best 8B)
- Multilingual: Qwen 2.5 3B/7B, Qwen3-4B/8B, Gemma 3 4B, Aya 8B
- Specialty: SILMA Kashif-2B (Arabic RAG), GPT-OSS 20B (experimental)
- API fallback: Gemini 2.0 Flash (free), Groq Qwen3-32B (free), Cohere Aya (~$2)

Phase 3: Preliminary Testing (Osman)
- Qwen 2.5 3B tested → +8.93% NDCG@10 over baseline (exp_003)
- Confirms: modern 3B models CAN do zero-shot Arabic QE

DECISION: Compare 10 open-source models (breadth-first)
- Split 5/5 between Mohammed and Osman
- Guide: research_decisions/model_comparison_guide.md
- Preference: Open-source, API as comparison/backup only
```

---

### Task 4.0b: Model Comparison Experiments (NEW)
**Owner:** Both (Mohammed: 5 models, Osman: 5 models)
**Status:** 🔄 In Progress
**Depends On:** Task 4.0 (✅), Task 4.1 (✅)

**Why:** Compare multiple open-source LLMs to find the best model for Arabic query expansion. Replicate exp_003 (Query2Doc) methodology with different models.

**Context Files:**
- `research_decisions/model_comparison_guide.md` - **Experiment guide with per-model instructions**
- `research_decisions/llm_model_research.md` - Model research and benchmarks
- `docs/experiments/exp_003_query2doc_dense.md` - Reference experiment to replicate

**Mohammed's Models:**
1. ✅ Falcon-H1-Arabic-3B — exp_005 (Dense NDCG@10=0.5359, BM25 NDCG@10=0.4038)
2. ✅ Jais-2-8B-Chat — exp_006 (Dense NDCG@10=0.6018, BM25 NDCG@10=0.5122) **BEST MODEL**
3. ✅ ALLaM-7B — exp_008 (Dense NDCG@10=0.2550) **WORST — DROP**
4. ✅ Qwen3-4B — exp_007 (Dense NDCG@10=0.5691, BM25 NDCG@10=0.4145) **2nd BEST**
5. ✅ GPT-OSS 20B — exp_009 **DROPPED** (70x slower than Jais-2, 3/5 hallucinations, English-dominant)

**Osman's Models:**
1. SILMA Kashif-2B (FP16, Arabic RAG)
2. Qwen 2.5-7B (4-bit, multilingual)
3. Qwen3-8B (4-bit, multilingual)
4. Gemma 3 4B-IT (FP16, multilingual)
5. Aya Expanse 8B (4-bit, multilingual)

**Deliverables:**
- [ ] Dense retrieval results for all 10 models
- [ ] BM25S results for top models
- [ ] Hybrid (RRF) results for top models
- [ ] Comparison table with all metrics
- [ ] Best model selection with justification

**Progress (Mohammed):**
- ✅ Falcon-H1-3B (exp_005): Dense +7.3% NDCG@10, BM25 -12.6% (technique issue, not model)
  - Key finding: Batching bug in falcon_h1 — requires single-query loop + A100
  - See: `docs/experiments/exp_005_falcon_h1_3b_dense.md`, `research_decisions/falcon_h1_research.md`
- ✅ Jais-2-8B (exp_006): Dense +20.5% NDCG@10, BM25 +10.8%. **BEST MODEL** by wide margin.
  - Key finding: Only model to improve BM25. Arabic-specialized vocab produces lexically precise expansions.
  - See: `research_decisions/jais_2_research.md`
- ✅ ALLaM-7B (exp_008): Dense -48.9% NDCG@10. **WORST — DROPPED.** Tokenizer bug + hallucinations.
  - See: `research_decisions/allam_7b_research.md`
- ✅ Qwen3-4B (exp_007): Dense +14.0% NDCG@10, BM25 -10.3%. **2nd BEST.** Easiest model.
  - Key finding: Generational improvement confirmed — Qwen3 beats Qwen 2.5 by +4.7% NDCG.
  - See: `docs/experiments/exp_007_qwen3_4b_dense.md`, `research_decisions/qwen3_4b_research.md`
- ✅ GPT-OSS-20B (exp_009): **DROPPED.** MoE 70x slower than Jais-2. 3/5 sanity queries hallucinated.
  - Key findings: MoE+BNB4bit impractical for batch QE. Forced-final-channel fix achieved 100% Arabic but facts wrong.
  - See: `research_decisions/gpt_oss_20b_research.md`

**Testing Protocol:**
1. Phase 1: Dense retrieval for all models (priority)
2. Phase 2: BM25S for top models
3. Phase 3: Hybrid (RRF) for top models

---

### Task 4.1: Implement First QE Technique
**Owner:** Osman
**Status:** ✅ Done
**Depends On:** Task 3.4 (✅), Task 4.0 (✅)

**Why:** Implement Query2Doc (LLM-based query expansion) as our first QE technique.

**Context Files:**
- `src/enhancers/query2doc.py` - **Query2Doc enhancer implementation**
- `src/enhancers/base.py` - **QueryEnhancer base class**
- `docs/experiments/exp_003_query2doc_dense.md` - **Experiment documentation**

**Deliverables:**
- [x] QE layer implemented (Query2DocEnhancer class)
- [x] Can enhance any query (single + batch with parallel processing)
- [x] Code saved to `src/enhancers/query2doc.py`
- [x] Batch processing optimized (8x speedup, 16x total with other optimizations)

**Outcomes:** *(Completed 11/2/2026)*
```
Technique: Query2Doc (Wang et al., 2023)
Implementation: LLM generates pseudo-document, concatenated with original query
Model: Qwen 2.5 3B Instruct (zero-shot, FP16)
Code: src/enhancers/query2doc.py (Query2DocEnhancer class)

PROMPT:
- System: "You are asked to write a passage that answers the given query.
  Do not ask the user for further clarification. Respond in Arabic only."
- User: [original query]

GENERATION PARAMS:
- max_new_tokens: 128
- temperature: 0.7
- top_p: 0.9
- batch_size: 8

OPTIMIZATIONS:
1. Batch processing (8 queries in parallel) → 8x speedup
2. Reduced token generation (128 vs 256) → 2x speedup
3. FP16 + eval mode + no_grad → inference optimized
4. Left-padding for decoder-only models (critical for correctness)
Total: 16x speedup → ~40 min for 2,896 queries

ARCHITECTURE:
- Inherits from QueryEnhancer base class
- enhance() for single query
- enhance_batch_parallel() for batch processing
- enhance_batch() orchestrates batched processing with progress bar
- model_name parameter allows swapping LLM (used in model comparison)
```

---

### Task 4.2: Run QE + BM25 Experiments
**Owner:** Osman  
**Status:** ✅ Done  
**Depends On:** Task 4.1 (✅)

**Context Files:**
- `docs/experiments/exp_004_query2doc_bm25.md` - **Full experiment documentation**
- `docs/TWO_NOTEBOOK_WORKFLOW.md` - Two-notebook approach used
- `experiments/exp_002_baseline_bm25.md` (baseline comparison)

**Deliverables:**
- [x] Run enhanced queries through BM25 (2,896 queries)
- [x] Record all metrics
- [x] Create experiment documentation

**Outcomes:** *(Completed 12/2/2026)*
```
EXPERIMENT 004: Query2Doc + BM25 Retrieval (Qwen 2.5 3B)

RESULTS (MIRACL Arabic Dev Set - 2,896 queries):
❌ Recall@10:  0.5384 (baseline: 0.5964) = -9.7%
❌ Recall@100: 0.8155 (baseline: 0.8577) = -4.9%
❌ NDCG@10:    0.4090 (baseline: 0.4621) = -11.5%
❌ MRR:        0.4342 (baseline: 0.4836) = -10.2%
```

---

### Task 4.3: Run QE + Dense Experiments
**Owner:** Osman
**Status:** ✅ Done (Qwen 2.5 3B; other models in Task 4.0b)
**Depends On:** Task 4.1 (✅)

**Context Files:**
- `docs/experiments/exp_003_query2doc_dense.md` - **Full experiment documentation**
- `results/exp_003_query2doc_dense/exp_003_metrics.json` - **Metrics**
- `experiments/exp_003_query2doc_dense.ipynb` - **Colab notebook**

**Deliverables:**
- [x] Run enhanced queries through Dense (2,896 queries)
- [x] Record all metrics
- [x] Create experiment documentation

**Outcomes:** *(Completed 11/2/2026)*
```
EXPERIMENT 003: Query2Doc + Dense Retrieval (Qwen 2.5 3B)

RESULTS (MIRACL Arabic Dev Set - 2,896 queries):
✅ Recall@10:  0.6608 (baseline: 0.6156) = +7.3%
✅ Recall@100: 0.8594 (baseline: 0.8407) = +2.2%
✅ NDCG@10:    0.5435 (baseline: 0.4993) = +8.9%
✅ MRR:        0.5742 (baseline: 0.5328) = +7.8%

ALL METRICS IMPROVED. Key finding: +8.9% NDCG@10 is significant.

QUERY EXPANSION STATISTICS:
- Original query length: 29.5 chars (median: 27.0)
- Enhanced query length: 247.6 chars (median: 250.0)
- Expansion ratio: 9.73x (median: 8.45x)

COMPARISON WITH QUERY2DOC PAPER:
- Paper (GPT-3 175B, few-shot, English): +2-5% NDCG@10 on dense
- Ours (Qwen 2.5 3B, zero-shot, Arabic): +8.9% NDCG@10 on dense
- Our improvement EXCEEDS the original paper's results

RUNTIME: ~40 minutes on Colab T4 (free tier), cost: $0
COLAB: https://colab.research.google.com/drive/1dfjqvgYbELPimgUvtnnFkTegZHPL5IQl

NEXT: Model comparison (Task 4.0b) - test 10 more models
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

## Phase 3: Thesis Initial Draft (March–April 2026)

**Goal:** Complete the first full draft of the thesis based on existing Query2Doc experiments (10 models).
**Deadline:** Mid-April 2026 (per Dr. Tahani — thesis must be ready before May exams)
**Writing Guide:** `research_decisions/thesis_writing_guide.md` — read this BEFORE starting any chapter

**Writing Order (from supervisor):** Chapter 2 → Chapter 3 (zigzag with 4) → Chapter 4 → Chapter 1 → Chapter 5 → Abstract

---

### Task 5.1: Update Chapter 2 — Literature Review & Theoretical Background
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** None (can start immediately)
**Priority:** HIGH — write first

**Why:** Chapter 2 is the thickest chapter. ALL definitions, models, and background go here. Chapter 3 will only reference Chapter 2 by section number, so this must be complete first.

**Context Files:**
- `research_decisions/thesis_writing_guide.md` — Section 2 (Chapter 2 guidelines)
- `.claude/contexts/thesis-writing.md` — writing context and rules
- `meetings/chapter2_initial_draft.md` — existing initial draft
- `University_of_Khartoum__EEE_bachelor_s_thesis_template/Chapters/chapter2_generated.tex` — generated version
- `papers/` — all paper summaries
- `research_decisions/llm_model_research.md` — model research
- Per-model research: `research_decisions/falcon_h1_research.md`, `jais_2_research.md`, `qwen3_4b_research.md`, `allam_7b_research.md`, `gpt_oss_20b_research.md`

**Deliverables:**
- [ ] 2.1 Theoretical background: LLMs, Transformers, RAG systems, Query Enhancement
- [ ] 2.2 Mathematical models: BM25 formula, dense retrieval / cosine similarity, NDCG, MRR, Recall@k
- [ ] 2.3 Description of ALL models used: Falcon-H1, Jais-2, Qwen 2.5 3B, Qwen3-4B, ALLaM, Aya, Gemma, SILMA, Qwen 2.5 7B, Qwen3 8B, GPT-OSS 20B
- [ ] 2.4 Related Work: Query2Doc, HyDE, CSQE, PBR, MUGI, KAR, AQE, ThinkQE, and other reviewed papers
- [ ] All abbreviations written in full on first use
- [ ] IEEE references numbered by order of appearance

---

### Task 5.2: Write Chapter 3 — Methodology
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Task 5.1 (Chapter 2 must define all concepts/models first)
**Priority:** HIGH — most important chapter

**Why:** Dr. Tahani: "This is the most important chapter — it contains your real research process." Write in zigzag with Chapter 4.

**Context Files:**
- `research_decisions/thesis_writing_guide.md` — Section 2 (Chapter 3 guidelines)
- `research_decisions/technical_specifications.md` — system architecture
- `docs/experiments/exp_001_baseline_dense.md` through `exp_009` — all experiment documentation
- `research_decisions/error_analysis_phase1_quantitative.md` — error analysis methodology
- `research_decisions/qe_technique_selection.md` — technique selection rationale
- `research_decisions/model_comparison_guide.md` — experiment design

**Deliverables:**
- [ ] 3.1 Dataset: MIRACL Arabic description, dev set (2,896 queries, 2.1M passages)
- [ ] 3.2 Baseline Implementation: BM25S approach, mDPR approach, evaluation pipeline
- [ ] 3.3 Error Analysis: quantitative analysis methodology, short query gap discovery
- [ ] 3.4 Query Enhancement Technique: Query2Doc approach, modifications (zero-shot, temperature tuning, no repetition for BM25)
- [ ] 3.5 Model Comparison: experimental setup, 10 models, same prompt/pipeline, GPU/quantization config
- [ ] Flowcharts: overall pipeline, Query2Doc process, evaluation workflow
- [ ] Processing diagrams for each major step
- [ ] NO code in the body — reference Appendix for code

---

### Task 5.3: Write Chapter 4 — Results and Discussion
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Task 5.2 (zigzag — write sections as corresponding Ch. 3 sections are written)
**Priority:** HIGH

**Why:** Contains all results, comparisons, and engineering analysis. Written in zigzag with Chapter 3.

**Context Files:**
- `research_decisions/thesis_writing_guide.md` — Section 2 (Chapter 4 guidelines)
- `.claude/contexts/thesis-writing.md` — results reference tables
- All `docs/experiments/exp_*` files
- `research_decisions/error_analysis_phase1_quantitative.md`

**Deliverables:**
- [ ] 4.1 Baseline Results: Dense vs BM25 comparison, complementary strengths analysis
- [ ] 4.2 Error Analysis Findings: 39% failure rate, short query gap (59% performance), query length correlation
- [ ] 4.3 Query2Doc Results (Dense): +8.9% NDCG@10, comparison with original paper (zero-shot Arabic > few-shot English)
- [ ] 4.4 Query2Doc Results (BM25): term dilution problem, negative results analysis
- [ ] 4.5 Model Comparison (Dense): full leaderboard, best model (Jais-2 / Aya), dropped models analysis
- [ ] 4.6 Model Comparison (BM25): Jais-2 and Aya success, why most models degrade BM25
- [ ] 4.7 Key Findings: model size vs performance, multilingual support importance, Arabic vocab impact
- [ ] All figures properly numbered (Figure 4.X), captions below
- [ ] All tables properly numbered (Table 4.X), captions above
- [ ] Engineering analysis for every result

---

### Task 5.4: Write Chapter 1 — Introduction
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Tasks 5.1, 5.2, 5.3 (write AFTER Chapters 2, 3, 4)
**Priority:** MEDIUM

**Why:** Dr. Tahani: "Write this after the other chapters — it should read like the Proposal but written by people who understand the work." Objectives must match actual methodology.

**Deliverables:**
- [ ] 1.1 General Introduction / Preamble
- [ ] 1.2 Problem Definition (Arabic query-document mismatch, short query information poverty)
- [ ] 1.3 Objectives (must match what was actually done in Chapter 3)
- [ ] 1.4 Thesis Layout (brief description of each chapter)

---

### Task 5.5: Write Chapter 5 — Conclusion and Recommendations
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Tasks 5.1, 5.2, 5.3 (write AFTER Chapters 2, 3, 4)
**Priority:** MEDIUM

**Why:** Conclusions summarize findings. Recommendations guide future researchers — Dr. Tahani: "Your recommendations are very important because you are the domain experts."

**Deliverables:**
- [ ] 5.1 Conclusions: overall findings, what was proven, best model selection
- [ ] 5.2 Challenges: resource limitations, dropped models, BM25 term dilution
- [ ] 5.3 Recommendations for Future Work: stronger embedding models, hybrid retrieval, chunking-aware QE, dialect testing, prompt optimization

---

### Task 5.6: Write Abstract (English) + المستخلص (Arabic)
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Tasks 5.1–5.5 (write LAST — summarizes everything)
**Priority:** MEDIUM

**Why:** First thing the examiner reads. ~300–350 words. Must cover: intro → problem → objectives → methodology → results → conclusion.

**Deliverables:**
- [ ] English Abstract (~300-350 words, ~3/4 page)
- [ ] Arabic المستخلص (faithful translation)

---

### Task 5.7: Front Matter & Appendices
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** All other Phase 3 tasks
**Priority:** LOW (generate after content is written)

**Deliverables:**
- [ ] Cover page (per university guidelines)
- [ ] Table of Contents with page numbers
- [ ] List of Figures
- [ ] List of Tables
- [ ] List of Abbreviations (alphabetically sorted)
- [ ] Roman numeral page numbering for front matter
- [ ] Appendix A: Code listings
- [ ] Appendix B: Supplementary material (if needed)
- [ ] IEEE references list (numbered by order of appearance)

---

## Phase 4: Expanded Experiments & Research (March–April 2026)

**Goal:** Build on Query2Doc results to make a stronger, publishable contribution. Explore chunking-aware query enhancement and other techniques that logically extend our current work.
**Constraint:** Must be consistent with existing Query2Doc work — not a completely new path, but a logical addition.
**Deadline:** Mid-April 2026 (practical work must be done before May exams)

---

### Task 6.1: Literature Review — Chunking-Aware Query Enhancement
**Owner:** Both (Mohammed leads, with AI research assistance)
**Status:** ⏳ Not Started
**Depends On:** None (can start immediately, in parallel with thesis writing)

**Why:** We want to explore how knowledge of the knowledge base structure (chunks, hierarchy, metadata) can improve query enhancement. This could be our key research contribution beyond basic Query2Doc.

**Context Files:**
- Previous papers on chunking-aware approaches (Rebarter, etc.) — referenced in earlier meetings
- `papers/` — existing paper summaries
- `research_decisions/llm_model_research.md` — context on current approach

**Deliverables:**
- [ ] Collect and review all papers on chunking-aware QE, knowledge-base-aware QE, hierarchical retrieval
- [ ] Summarize each approach: what they did, what gap remains
- [ ] Create `research_decisions/chunking_aware_qe_research.md` with findings
- [ ] Identify ideas that can logically build on our Query2Doc pipeline

---

### Task 6.2: Brainstorm & Select Expanded Experiment Approach
**Owner:** Both (with AI as research assistant)
**Status:** ⏳ Not Started
**Depends On:** Task 6.1

**Why:** Need to select the best approach that (a) builds logically on Query2Doc, (b) represents a true contribution, (c) is feasible within our timeline and resources.

**Key Constraint (from Mohammed):** "We don't want to start a completely new path. We want consistency with all efforts done so far — the expanded work should be a logical addition to Query2Doc."

**Deliverables:**
- [ ] List all candidate ideas from literature review
- [ ] Evaluate each for: feasibility, contribution potential, consistency with Query2Doc
- [ ] Select 1-2 approaches to implement
- [ ] Document rationale in `research_decisions/expanded_experiments_plan.md`

**Candidate Ideas to Explore:**
- Chunking-aware query enhancement (hierarchical structure / metadata injection)
- Knowledge-base-aware prompting (inject KB structure into LLM prompt)
- Query2Doc + re-ranking combination
- Multi-stage query enhancement (iterative refinement)
- Hybrid retrieval optimization (tuning RRF with QE)
- Other approaches from Rebarter and related papers

---

### Task 6.3: Implement Expanded Experiments
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Task 6.2

**Why:** Run the selected expanded experiments to generate results for the thesis contribution.

**Deliverables:**
- [ ] Implementation notebook(s) in `experiments/`
- [ ] Run on Dense + BM25 (same evaluation pipeline)
- [ ] Compare against Query2Doc baselines
- [ ] Document experiments in `docs/experiments/`
- [ ] Sanity check first 5 queries before full run

---

### Task 6.4: Analyze Expanded Results & Update Thesis
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Task 6.3

**Why:** Integrate expanded experiment results into thesis Chapters 3, 4, and 5.

**Deliverables:**
- [ ] Add methodology sections to Chapter 3
- [ ] Add results sections to Chapter 4
- [ ] Update Chapter 5 conclusions and recommendations
- [ ] Update comparison tables and leaderboards

---

### Task 6.5: Evaluate Publication Potential
**Owner:** Both
**Status:** ⏳ Not Started
**Depends On:** Task 6.4

**Why:** Dr. Tahani strongly encouraged publishing. Having a published paper significantly strengthens the graduation evaluation.

**Options (from supervisor):**
1. Pre-print (arXiv) — fastest, ~3 pages
2. Faculty of Engineering journal (University of Khartoum)
3. Engineering Society journal
4. Regional/International conference

**Deliverables:**
- [ ] Assess if results constitute a publishable contribution
- [ ] Select target venue
- [ ] Draft paper outline (if proceeding)

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
| `research_decisions/thesis_writing_guide.md` | **Dr. Tahani's thesis writing guidelines** |
| `.claude/contexts/thesis-writing.md` | Writing context for AI assistant |
| `WORKFLOW.md` | How we work |
| `research_decisions/technical_specifications.md` | Architecture details |
| `research_decisions/open_questions.md` | Undecided items |
| `docs/experiments/` | Experiment documentation |
| `research_decisions/model_comparison_guide.md` | Model comparison guide |
