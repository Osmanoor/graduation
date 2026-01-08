# Embedding Model Research for Arabic RAG
**Task:** 1.1 - Research Embedding Model Options  
**Date:** January 8, 2026  
**Status:** Research Complete - Decision Pending

---

## Executive Summary

Based on comprehensive research including full paper analysis of BGE-M3, Multilingual E5, and Jina-v3, here are the detailed findings for Arabic embedding models suitable for our MIRACL Arabic experiments.

**Key Discovery:** Pyserini provides pre-built FAISS indexes for MIRACL Arabic with mDPR embeddings, potentially saving us embedding time entirely!

**Note:** Swan models (UBC-NLP) were found to be unavailable/not released yet. Focus is on BGE-M3, mE5, and Jina.

---

## 🔥 Critical Finding: Pre-built Indexes Available

From the Pyserini MIRACL reproduction page (https://castorini.github.io/pyserini/2cr/miracl.html):

| Model | Arabic nDCG@10 | Pre-built Index Available |
|-------|----------------|---------------------------|
| BM25 | 0.481 | ✅ Yes (`miracl-v1.0-ar`) |
| mDPR pFT | 0.499 | ✅ Yes (`miracl-v1.0-ar-mdpr-tied-pft-msmarco`) |
| mDPR pFT+FT1 | 0.578 | ✅ Yes |
| mDPR pFT+FT2 | **0.725** | ✅ Yes (fine-tuned on MIRACL Arabic) |
| mContriever | 0.525 | ✅ Yes |
| BM25+mDPR Hybrid | 0.673 | ✅ Yes (fusion of above) |

**Implication:** We could potentially skip corpus embedding entirely and use pre-built indexes for baseline experiments!

---

## Detailed Model Specifications

### 1. BGE-M3 (BAAI)
**Paper:** arXiv:2402.03216 (Feb 2024) - "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity"
**Authors:** Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, Zheng Liu

| Spec | Value |
|------|-------|
| **Parameters** | ~568M (XLM-RoBERTa based) |
| **Embedding Dimension** | 1024 |
| **Max Sequence Length** | 8192 tokens |
| **GPU Memory (FP16)** | ~2-3GB |
| **Languages** | 100+ including Arabic |
| **Base Model** | XLM-RoBERTa + RetroMAE pre-training |

**Key Features (from paper):**
1. **Multi-Functionality:** Supports 3 retrieval methods in ONE model:
   - Dense retrieval (single [CLS] vector)
   - Sparse retrieval (learned term weights, like BM25)
   - Multi-vector retrieval (ColBERT-style late interaction)
   
2. **Self-Knowledge Distillation:** Novel training where scores from different retrieval methods are combined as teacher signal

3. **Efficient Batching:** Groups data by sequence length, uses gradient checkpointing for long sequences

**MIRACL Arabic Performance (from BGE-M3 paper Table 1):**
| Method | nDCG@10 |
|--------|---------|
| BM25 | 39.5 |
| mDPR | 49.9 |
| mContriever | 52.5 |
| mE5-large | 76.0 |
| **BGE-M3 Dense** | **78.4** |
| BGE-M3 Sparse | 67.1 |
| BGE-M3 Multi-vec | 79.6 |
| **BGE-M3 All (hybrid)** | **80.2** |

**Why BGE-M3 is Widely Cited:**
From arXiv search (2024-2025 papers):
- **RusBEIR** (Russian benchmark) - Uses BGE-M3 as primary baseline
- **ViRanker** (Vietnamese reranking) - Built on BGE-M3 encoder
- **SEAL** (Long document retrieval) - Uses BGE-M3 as baseline
- **Optimizing RAG for Arabic** (2025) - Recommends BGE-M3 for Arabic RAG
- **Thai Legal RAG** - Uses BGE-M3 embeddings
- **Multiple Chinese RAG systems** - BGE-M3 for dense retrieval
- **mGTE paper** - Compares against BGE-M3

---

### 2. Multilingual E5 (Microsoft)
**Paper:** arXiv:2402.05672 (Feb 2024) - "Multilingual E5 Text Embeddings: A Technical Report"
**Authors:** Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, Furu Wei

| Model | Parameters | Dimension | Base Model |
|-------|------------|-----------|------------|
| **mE5-small** | 118M | 384 | Multilingual MiniLM |
| **mE5-base** | 278M | 768 | XLM-RoBERTa-base |
| **mE5-large** | 560M | 1024 | XLM-RoBERTa-large |
| **mE5-large-instruct** | 560M | 1024 | XLM-RoBERTa-large |

**Training (from paper):**
- Stage 1: Contrastive pre-training on ~1 billion multilingual text pairs
- Stage 2: Fine-tuning on labeled datasets including **MIRACL** (40k samples)!

**MIRACL Arabic Performance (from E5 paper Table 6):**
| Model | nDCG@10 | Recall@100 |
|-------|---------|------------|
| mE5-small | 71.4 | 96.2 |
| mE5-base | 71.6 | 95.9 |
| **mE5-large** | **76.0** | 97.3 |
| mE5-large-instruct | 76.8 | 97.5 |

**Why mE5 is Important:**
- **Explicitly trained on MIRACL Arabic** - Direct applicability
- **Microsoft-backed** - Well-documented, reliable
- **Multiple sizes** - Can choose based on resources
- **Used as baseline in MIRACL paper itself**

---

### 3. Jina-embeddings-v3 (Jina AI)
**Paper:** arXiv:2409.10173 (Sep 2024) - "jina-embeddings-v3: Multilingual Embeddings With Task LoRA"
**Authors:** Saba Sturua, Isabelle Mohr, Mohammad Kalim Akram, et al.

| Spec | Value |
|------|-------|
| **Parameters** | 570M (559M base + 13M adapters) |
| **Embedding Dimension** | 1024 (can reduce to 32 with MRL) |
| **Max Sequence Length** | 8192 tokens |
| **Base Model** | Modified XLM-RoBERTa with RoPE |

**Key Features:**
1. **Task-Specific LoRA Adapters:** 5 adapters for different tasks:
   - `retrieval.query` - for encoding queries
   - `retrieval.passage` - for encoding documents
   - `text-matching` - for STS, symmetric retrieval
   - `classification` - for classification tasks
   - `separation` - for clustering, reranking

2. **Matryoshka Representation Learning (MRL):** Can truncate embeddings from 1024 down to 32 dimensions

3. **Failure Analysis Training:** Specifically trained to handle:
   - Misleading syntactic similarities
   - Named entity misinterpretation
   - Polar questions
   - Low-quality document preference

**Jina API Free Tier:**
- **10 million tokens FREE** per account
- Multiple accounts possible for more free tokens
- **IMPORTANT:** 10M tokens ≈ embedding ~2.5M short passages OR ~500K long passages
- For MIRACL (2.1M passages), would need ~8-10M tokens just for corpus (one-time)
- Query embedding is cheap: ~3000 queries × ~20 tokens = 60K tokens per iteration

---

## Google Colab Free Tier Analysis

### Hardware Specs (Free Colab)
- GPU: Tesla T4 (16GB VRAM) or K80 (12GB)
- RAM: ~12GB
- Session limit: ~12 hours, may disconnect

### Embedding Time Estimates for MIRACL (2.1M passages)

| Model | Size | Batch Size | Est. Time (T4) | Fits in VRAM? |
|-------|------|------------|----------------|---------------|
| **mE5-small** | 118M | 64 | ~3-4 hours | ✅ Yes |
| **mE5-base** | 278M | 32 | ~6-8 hours | ✅ Yes |
| **mE5-large** | 560M | 16 | ~12-15 hours | ⚠️ Tight |
| **BGE-M3** | 568M | 16 | ~12-15 hours | ⚠️ Tight |
| **Jina-v3** | 570M | 16 | ~12-15 hours | ⚠️ Tight |

### Your Decision: Use Large Models
You mentioned preferring large models since:
1. Corpus embedding is one-time
2. Query embedding time is negligible (~2-3 min for 3000 queries)

**Recommendation:** Use mE5-large or BGE-M3 for best quality. Run overnight on Colab.

---

## Which Models Are Used as Baselines in Research?

### From BGE-M3 Paper (Table 1 - MIRACL):
- BM25 (lexical baseline)
- mDPR (multilingual DPR)
- mContriever (Facebook)
- mE5-large (Microsoft)
- E5-mistral-7b (LLM-based)
- OpenAI text-embedding-3

### From mE5 Paper (Table 4 - MIRACL):
- BM25
- mDPR (fine-tuned on MIRACL)

### From Recent Arabic RAG Paper (arXiv:2506.06339, June 2025):
**"Optimizing RAG Pipelines for Arabic"** explicitly tested:
- BGE-M3 ✅ (recommended)
- Multilingual-E5-large ✅ (recommended)
- bge-reranker-v2-m3 (for reranking)

**Quote from paper:** "BGE-M3 and Multilingual-E5-large emerge as the most effective embedding models" for Arabic RAG.

### From RusBEIR Paper (arXiv:2504.12879, April 2025):
"Neural models, such as mE5-large and BGE-M3, demonstrate superior performance on most datasets"

---

## Feature Impact on Our Work

### BGE-M3's Multi-Functionality
| Feature | Impact on Our Project |
|---------|----------------------|
| Dense retrieval | Primary method for semantic search |
| Sparse retrieval | Can compare with standalone BM25 - interesting ablation |
| ColBERT mode | Optional advanced retrieval (computationally expensive) |
| 8192 tokens | Handles long Arabic passages without truncation |
| Self-knowledge distillation | Better quality embeddings |

### mE5's MIRACL Training
| Feature | Impact on Our Project |
|---------|----------------------|
| Trained on MIRACL | Directly applicable, no domain shift |
| Multiple sizes | Can use small for prototyping, large for final |
| No special prefix needed | Simpler implementation |
| Well-documented | Easy to reproduce |

### Jina's Task Adapters
| Feature | Impact on Our Project |
|---------|----------------------|
| Query adapter | Better query encoding (asymmetric retrieval) |
| Passage adapter | Better document encoding |
| MRL (dimension reduction) | Faster search, less storage |
| Free API | Fast prototyping without GPU |

---

## 💡 AI Suggestion: Recommended Strategy

### Option A: Use Pre-built Pyserini Indexes (Fastest)
1. Download pre-built mDPR index for MIRACL Arabic
2. Use Pyserini for retrieval
3. Focus entirely on query enhancement
4. **Pros:** No embedding time, reproducible baselines
5. **Cons:** Limited to mDPR model, less flexibility

### Option B: Embed with mE5-large (Recommended)
1. Use mE5-large (trained on MIRACL)
2. ~12-15 hours embedding on Colab (overnight)
3. Store embeddings on Google Drive
4. **Pros:** Best documented performance on MIRACL Arabic
5. **Cons:** Long embedding time

### Option C: Embed with BGE-M3 (Most Flexible)
1. Use BGE-M3 for multi-functional embeddings
2. Can compare dense vs sparse vs hybrid
3. **Pros:** Most cited, multi-functional
4. **Cons:** Slightly more complex setup

### Option D: Jina API for Prototyping
1. Use Jina API for initial experiments
2. 10M tokens = enough for corpus + many query iterations
3. Switch to open-source for final experiments
4. **Pros:** No GPU needed, fast iteration
5. **Cons:** API dependency, need to re-embed for final

---

## Paper Summaries

### BGE-M3 (arXiv:2402.03216)

**Year:** 2024
**Authors:** Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, Zheng Liu (BAAI & USTC)
**Venue:** ACL 2024

#### Short Description
M3-Embedding achieves unprecedented versatility in multi-linguality (100+ languages), multi-functionality (dense, sparse, multi-vector retrieval), and multi-granularity (up to 8192 tokens). Uses novel self-knowledge distillation where different retrieval methods reinforce each other.

#### Research Question
How to create a single embedding model that supports multiple languages, multiple retrieval methods, and multiple input lengths?

#### Main Methodology
1. Pre-train XLM-RoBERTa with RetroMAE on 1.2B multilingual text pairs
2. Fine-tune with self-knowledge distillation (combine dense+sparse+multi-vec scores as teacher)
3. Efficient batching by grouping sequences by length
4. Synthetic data generation for long documents

#### Dataset & Benchmark
- **Training:** 1.2B text pairs, 194 languages, 2655 cross-lingual pairs
- **Evaluation:** MIRACL (18 languages), MKQA (25 languages), MLDR (long-doc)
- **MIRACL Arabic included:** Yes, both training and evaluation

#### Key Results
| Benchmark | BGE-M3 Dense | BGE-M3 All | Best Baseline |
|-----------|--------------|------------|---------------|
| MIRACL Arabic | 78.4 | 80.2 | 76.0 (mE5-large) |
| MKQA Arabic | 71.1 | 71.5 | 68.7 (mE5-large) |
| MLDR Arabic | 47.6 | 64.7 | 35.4 (mE5-large) |

#### Relevance to Our Project
- **Applicable to Arabic?** ✅ Yes - Explicitly tested on MIRACL Arabic with SOTA results
- **Uses MIRACL?** ✅ Yes - Both training and evaluation
- **Retrieval metrics reported?** nDCG@10, Recall@100
- **Feasible for us?** ⚠️ Tight fit on free Colab (568M params), but doable overnight

---

### Multilingual E5 (arXiv:2402.05672)

**Year:** 2024
**Authors:** Liang Wang, Nan Yang, Xiaolong Huang, et al. (Microsoft)
**Venue:** Technical Report

#### Short Description
Open-source multilingual text embedding models (small/base/large) trained with contrastive pre-training on 1B multilingual pairs, followed by fine-tuning on labeled datasets including MIRACL.

#### Research Question
How to extend English E5 embeddings to support 100+ languages while maintaining competitive performance?

#### Main Methodology
1. Contrastive pre-training on 1B multilingual text pairs (Wikipedia, mC4, NLLB, etc.)
2. Supervised fine-tuning on labeled datasets (MS-MARCO, NQ, MIRACL, Mr.TyDi)
3. Knowledge distillation from cross-encoder
4. Instruction-tuned variant with GPT-4 synthetic data

#### Dataset & Benchmark
- **Training:** ~1B pairs (pre-training) + 1.6M labeled (fine-tuning)
- **Fine-tuning includes:** MIRACL (40k), Mr.TyDi (50k)
- **Evaluation:** MTEB, MIRACL, Bitext mining

#### Key Results (MIRACL Arabic)
| Model | nDCG@10 | Recall@100 |
|-------|---------|------------|
| mE5-small | 71.4 | 96.2 |
| mE5-base | 71.6 | 95.9 |
| mE5-large | 76.0 | 97.3 |
| mE5-large-instruct | 76.8 | 97.5 |

#### Relevance to Our Project
- **Applicable to Arabic?** ✅ Yes - Explicitly trained and evaluated on MIRACL Arabic
- **Uses MIRACL?** ✅ Yes - 40k samples in fine-tuning
- **Retrieval metrics reported?** nDCG@10, Recall@100
- **Feasible for us?** ✅ Yes - mE5-base (278M) fits easily, mE5-large (560M) fits with care

---

### Jina-embeddings-v3 (arXiv:2409.10173)

**Year:** 2024
**Authors:** Saba Sturua, Isabelle Mohr, Mohammad Kalim Akram, et al. (Jina AI)
**Venue:** arXiv preprint

#### Short Description
570M parameter multilingual embedding model with task-specific LoRA adapters for query/passage encoding, classification, clustering, and text matching. Supports 8192 tokens and Matryoshka representation learning.

#### Research Question
How to create task-optimized embeddings without complex instruction prompts?

#### Main Methodology
1. XLM-RoBERTa backbone with RoPE positional embeddings
2. Task-specific LoRA adapters (5 adapters, <3% of params)
3. Three-stage training: MLM pre-training → embedding fine-tuning → adapter training
4. Synthetic data to fix retrieval failures (named entities, polar questions)

#### Dataset & Benchmark
- **Pre-training:** CulturaX corpus (89 languages)
- **Fine-tuning:** MS-MARCO, NQ, STS datasets
- **Evaluation:** MTEB, multilingual benchmarks

#### Key Results (MTEB)
| Task | Jina-v3 | mE5-large-instruct |
|------|---------|-------------------|
| Retrieval | 53.87 | 52.47 |
| Classification | 82.58 | 77.56 |
| STS | 85.80 | 84.78 |
| Average | 65.52 | 64.41 |

#### Relevance to Our Project
- **Applicable to Arabic?** ⚠️ Maybe - Supports Arabic but not specifically evaluated on MIRACL
- **Uses MIRACL?** ❌ No - Not mentioned in training or evaluation
- **Retrieval metrics reported?** MTEB retrieval metrics
- **Feasible for us?** ✅ Yes - API available with 10M free tokens

---

### Swan/ArabicMTEB (arXiv:2411.01192)

**Year:** 2024
**Authors:** Fakhraddin Alwajih, et al. (UBC-NLP)
**Venue:** arXiv preprint

#### Short Description
Arabic-specific embedding models (Swan-Small, Swan-Large) trained on Arabic data, with ArabicMTEB benchmark for evaluation.

#### Research Question
How to create Arabic-optimized embeddings that outperform multilingual models?

#### Key Results (from paper)
- Swan-Large matches OpenAI performance at 13x lower cost
- Best on ArabicMTEB benchmark

#### Relevance to Our Project
- **Applicable to Arabic?** ✅ Yes - Arabic-specific
- **Uses MIRACL?** Unknown
- **Model Available?** ❌ **NO - Models not released yet**
- **Feasible for us?** ❌ No - Cannot use unavailable models

**Note:** We documented this finding but cannot use Swan models.

---

## Comparison Table: Models as Research Baselines

| Model | Used in BGE-M3 Paper | Used in mE5 Paper | Used in Arabic RAG Papers | Recommended |
|-------|---------------------|-------------------|---------------------------|-------------|
| BM25 | ✅ | ✅ | ✅ | ✅ Standard baseline |
| mDPR | ✅ | ✅ | - | ✅ Pre-built indexes |
| mContriever | ✅ | - | - | Optional |
| mE5-large | ✅ | - | ✅ | ✅ **Recommended** |
| BGE-M3 | - | - | ✅ | ✅ **Recommended** |
| Jina-v3 | - | - | - | For prototyping |

---

## Action Items

- [ ] Check if Pyserini pre-built indexes work for our use case
- [ ] Test mE5-large embedding time on sample (1000 passages)
- [ ] Test Jina API with sample MIRACL queries
- [ ] Make final decision: Pre-built indexes vs. Custom embedding
- [ ] Document decision in `research_decisions/open_questions.md`

---

## References

1. BGE-M3 Paper: arXiv:2402.03216 (Feb 2024) - **Full paper read**
2. Multilingual E5 Paper: arXiv:2402.05672 (Feb 2024) - **Full paper read**
3. Jina-embeddings-v3 Paper: arXiv:2409.10173 (Sep 2024) - **Full paper read**
4. Swan/ArabicMTEB Paper: arXiv:2411.01192 (Nov 2024) - Swan unavailable
5. MIRACL Benchmark: https://project-miracl.github.io/
6. Pyserini MIRACL Reproductions: https://castorini.github.io/pyserini/2cr/miracl.html
7. Optimizing RAG for Arabic: arXiv:2506.06339 (June 2025)

---

**Document Status:** Research Complete  
**Next Step:** Team decision meeting  
**Prepared by:** Kiro (AI Research Assistant)  
**Updated:** January 8, 2026
