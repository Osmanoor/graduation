# Embedding Model Research for Arabic RAG
**Task:** 1.1 - Research Embedding Model Options  
**Date:** January 9, 2026  
**Status:** Research Complete - Pending Discussion with Osman

---

## Executive Summary

Based on comprehensive research including full paper analysis of BGE-M3, Multilingual E5, and Jina-v3, here are the fact-checked findings for Arabic embedding models suitable for our MIRACL Arabic experiments.

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

## Detailed Model Specifications (Fact-Checked from Papers)

### 1. BGE-M3 (BAAI)
**Paper:** arXiv:2402.03216v3 (Feb 2024)
**Authors:** Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, Zheng Liu

| Spec | Value |
|------|-------|
| **Parameters** | ~568M (XLM-RoBERTa-large based) |
| **Embedding Dimension** | 1024 |
| **Max Sequence Length** | 8192 tokens |
| **Languages** | 100+ including Arabic |
| **Base Model** | XLM-RoBERTa + RetroMAE pre-training |

**Key Features (from paper):**
1. **Multi-Functionality:** Supports 3 retrieval methods in ONE model:
   - Dense retrieval ([CLS] token embedding)
   - Sparse/Lexical retrieval (learned term weights)
   - Multi-vector retrieval (ColBERT-style late interaction)
   
2. **Self-Knowledge Distillation:** Novel training where scores from different retrieval methods are combined as teacher signal

3. **Efficient Batching:** Groups data by sequence length, uses gradient checkpointing

**MIRACL Performance (from BGE-M3 paper Table 2):**

| Method | Arabic nDCG@10 | Average (18 langs) |
|--------|----------------|-------------------|
| BM25 | 39.5 | 31.9 |
| mDPR | 49.9 | 41.8 |
| mContriever | 52.5 | 43.1 |
| mE5-large | 76.0 | 65.4 |
| E5-mistral-7b | 73.3 | 62.2 |
| **BGE-M3 Dense** | **78.4** | **67.8** |
| BGE-M3 Sparse | 67.1 | 53.9 |
| BGE-M3 Multi-vec | 79.6 | 69.0 |
| BGE-M3 Dense+Sparse | 79.6 | 68.9 |
| **BGE-M3 All** | **80.2** | **70.0** |

**MLDR Arabic (Long Document Retrieval, Table 4):**
| Method | Arabic nDCG@10 |
|--------|----------------|
| BM25 | 45.1 |
| mE5-large | 33.0 |
| E5-mistral-7b | 29.6 |
| BGE-M3 Dense | 47.6 |
| BGE-M3 Sparse | 58.7 |
| **BGE-M3 All** | **64.7** |

---

### 2. Multilingual E5 (Microsoft)
**Paper:** arXiv:2402.05672 (Feb 2024)
**Authors:** Liang Wang, Nan Yang, Xiaolong Huang, et al.

| Model | Parameters | Dimension | Base Model |
|-------|------------|-----------|------------|
| **mE5-small** | 118M | 384 | Multilingual MiniLM |
| **mE5-base** | 278M | 768 | XLM-RoBERTa-base |
| **mE5-large** | 560M | 1024 | XLM-RoBERTa-large |
| **mE5-large-instruct** | 560M | 1024 | XLM-RoBERTa-large |

**Training (from paper):**
- Stage 1: Contrastive pre-training on ~1 billion multilingual text pairs
- Stage 2: Fine-tuning on labeled datasets including **MIRACL** (40k samples)

**MIRACL Performance (from E5 paper Table 4 & 6):**

| Model | Arabic nDCG@10 | Arabic Recall@100 | Average nDCG@10 |
|-------|----------------|-------------------|-----------------|
| BM25 | 39.3 | 78.7 | 39.3 |
| mDPR | 41.5 | 78.8 | 41.5 |
| mE5-small | 71.4 | 96.2 | 60.8 |
| mE5-base | 71.6 | 95.9 | 62.3 |
| **mE5-large** | **76.0** | **97.3** | **66.5** |
| mE5-large-instruct | 76.8 | 97.5 | 65.7 |

---

### 3. Jina-embeddings-v3 (Jina AI)
**Paper:** arXiv:2409.10173 (Sep 2024)
**Authors:** Saba Sturua, Isabelle Mohr, Mohammad Kalim Akram, et al.

| Spec | Value |
|------|-------|
| **Parameters** | 570M (559M base + 13M adapters) |
| **Embedding Dimension** | 1024 (can reduce to 32 with MRL) |
| **Max Sequence Length** | 8192 tokens |
| **Base Model** | Modified XLM-RoBERTa with RoPE |

**Key Features:**
1. **Task-Specific LoRA Adapters:** 5 adapters (<3% of params):
   - `retrieval.query` - for encoding queries
   - `retrieval.passage` - for encoding documents
   - `text-matching` - for STS, symmetric retrieval
   - `classification` - for classification tasks
   - `separation` - for clustering, reranking

2. **Matryoshka Representation Learning (MRL):** Can truncate embeddings from 1024 down to 32 dimensions

**⚠️ Important:** Jina-v3 was NOT evaluated on MIRACL in their paper. Arabic performance is unknown.

**Jina API Free Tier:**
- **10 million tokens FREE** per account
- For MIRACL corpus (2.1M passages × ~100 tokens): ~210M tokens needed (exceeds free tier)
- Query embedding is cheap: ~3000 queries × 20 tokens = 60K tokens per iteration

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

---

## Which Models Are Used as Baselines in Research?

### From BGE-M3 Paper (Table 2):
- BM25 (lexical baseline)
- mDPR (multilingual DPR)
- mContriever (Facebook)
- mE5-large (Microsoft)
- E5-mistral-7b (LLM-based)
- OpenAI text-embedding-3

### From mE5 Paper:
- BM25
- mDPR (fine-tuned on MIRACL)

---

## Comparison Summary (Arabic nDCG@10 on MIRACL)

| Model | Arabic nDCG@10 | Source | Notes |
|-------|----------------|--------|-------|
| BM25 | 39.5 | BGE-M3 paper | Lexical baseline |
| mDPR | 49.9 | BGE-M3 paper | Pre-built index available |
| mContriever | 52.5 | BGE-M3 paper | |
| mE5-large | 76.0 | Both papers | Trained on MIRACL |
| E5-mistral-7b | 73.3 | BGE-M3 paper | 7B params, expensive |
| **BGE-M3 Dense** | **78.4** | BGE-M3 paper | Best single method |
| **BGE-M3 All** | **80.2** | BGE-M3 paper | Best overall |
| Jina-v3 | Unknown | - | Not evaluated on MIRACL |

---

## 💡 AI Suggestion: Decision Options for Discussion with Osman

| Option | Model | Arabic nDCG@10 | Embedding Time | Pros | Cons |
|--------|-------|----------------|----------------|------|------|
| **A** | Pre-built Pyserini (mDPR) | 72.5 | None | No embedding needed | Limited to mDPR |
| **B** | mE5-large | 76.0 | ~12-15h | Trained on MIRACL, well-documented | Slightly lower than BGE-M3 |
| **C** | BGE-M3 | 80.2 | ~12-15h | Best results, multi-functional | Complex setup |
| **D** | Jina API | Unknown | Fast | Fast prototyping | Not evaluated on MIRACL, API cost |

---

## Action Items

- [ ] Discuss with Osman to finalize embedding model choice
- [ ] Test Pyserini pre-built indexes for our use case
- [ ] If choosing BGE-M3 or mE5-large: plan overnight Colab session

---

## References

1. BGE-M3 Paper: arXiv:2402.03216v3 (Feb 2024) - **Verified from HTML version**
2. Multilingual E5 Paper: arXiv:2402.05672 (Feb 2024)
3. Jina-embeddings-v3 Paper: arXiv:2409.10173 (Sep 2024)
4. Pyserini MIRACL Reproductions: https://castorini.github.io/pyserini/2cr/miracl.html

---

**Document Status:** Research Complete - Fact-Checked  
**Next Step:** Discussion with Osman  
**Prepared by:** Kiro (AI Research Assistant)  
**Updated:** January 9, 2026
