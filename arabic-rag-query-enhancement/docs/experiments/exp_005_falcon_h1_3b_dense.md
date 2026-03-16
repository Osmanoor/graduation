# Experiment 005: Falcon-H1-3B-Instruct + Query2Doc

**Date:** March 2, 2026
**Status:** ✅ Complete (temperature=0.1)
**Researcher:** Mohammed Elhaj
**Baseline:** Experiment 001 (Dense) / Experiment 002 (BM25)
**Reference:** Experiment 003 (Query2Doc + Qwen 2.5 3B, Dense)

---

## Objective

Test Falcon-H1-3B-Instruct as the LLM for Query2Doc query expansion, comparing it against the Qwen 2.5 3B reference (exp_003). Falcon-H1 was selected for its best-in-class Arabic OALL score (~62%) at the 3B parameter scale.

**Research Questions:**
1. Does Falcon-H1's Arabic benchmark advantage translate to better query expansion?
2. What is the impact of the model-recommended temperature (0.1) vs. standard (0.7)?
3. How does the hybrid Mamba2-Transformer architecture affect generation quality and throughput?

---

## Model: Falcon-H1-3B-Instruct

| Property | Value |
|----------|-------|
| **HuggingFace ID** | `tiiuae/Falcon-H1-3B-Instruct` |
| **Developer** | Technology Innovation Institute (TII), Abu Dhabi |
| **Parameters** | 3.15B (3,149.4M) |
| **Architecture** | Hybrid Mamba2-Transformer with SwiGLU (`falcon_h1`) |
| **Arabic OALL** | ~62% (best at 3B scale, ~10pts ahead of peers) |
| **Languages** | 18 including Arabic (first-class) |
| **Context Length** | 128K tokens |
| **Release** | May 21, 2025 |

### Why Falcon-H1 Was Selected

- **Highest Arabic OALL at 3B size** — approximately 10 percentage points ahead of Qwen 2.5 3B, Gemma 3 4B, and other 3B models
- **No quantization needed** — fits in FP16/BF16 without 4-bit quantization
- **Arabic as first-class language** — not just "multilingual support"

---

## Methodology

### Query Enhancement: Query2Doc

Same technique as exp_003. The `Query2DocEnhancer` class was reused unchanged — only `model_name` was swapped.

**System Prompt (same as exp_003):**
```
You are asked to write a passage that answers the given query.
Do not ask the user for further clarification.
Respond in Arabic only.
```

**Query Combination:**
```python
enhanced_query = f"{original_query} {pseudo_document}"
```

### Generation Parameters

| Parameter | Value | Note |
|-----------|-------|------|
| `model_name` | `tiiuae/Falcon-H1-3B-Instruct` | — |
| `max_new_tokens` | 128 | Same as exp_003 |
| `temperature` | 0.1 | Model-recommended; higher may "largely drop performance" |
| `top_p` | 0.9 | Same as exp_003 |
| `batch_size` | **1** | ⚠️ Forced single-query — see Technical Issues below |
| `dtype` | `bfloat16` | A100 supports native BF16 |

---

## Critical Engineering Issues

### Issue 1: Batched Generation Fails (Falcon-H1 Architecture Bug)

**Severity:** Blocking — required workaround
**Root cause:** `modeling_falcon_h1.py` does not extend the 4D causal attention mask as new tokens are generated during batch inference. With left-padded batches, key/value length grows while the mask stays at the original padded length, causing a shape mismatch.

**Error (SDPA):**
```
RuntimeError: The expanded size of the tensor (61) must match
the existing size (58) at non-singleton dimension 3.
```

**Workaround:** `batch_size=1` (single-query loop via `enhance()`). No padding → no mask mismatch.

Tested on: SDPA (default), eager attention — same crash on both. Flash Attention 2 requires `flash-attn` compilation (~30 min) and the bug is upstream of all backends.

### Issue 2: OOM on T4 (15 GB)

Falcon-H1 uses ~10-11 GB in BF16 (model weights ~6.3 GB + Mamba2 SSM state buffers ~4 GB). T4 has only ~4 GB free after model load, not enough for batch_size ≥ 2.

**Solution:** Upgraded to Colab Pro+ A100 (40 GB VRAM).

### Hardware Used

| Phase | GPU | Outcome |
|-------|-----|---------|
| Initial attempt | T4 (15 GB) | OOM at batch_size=8; mask bug at batch_size=2 |
| Final run | A100-SXM4-40GB (Colab Pro+) | ✅ Successful single-query loop |

### Issue 3: Transformers Version

`falcon_h1` architecture requires transformers v5.2.0+ (May 2025). Install from source:
```bash
pip install git+https://github.com/huggingface/transformers.git
```
Do NOT install `mamba-ssm` or `causal-conv1d` — they fail to build on Colab (Python 3.11 incompatibility).

---

## Experimental Setup

### Dataset
- **Corpus:** MIRACL Arabic (2,061,414 passages)
- **Queries:** 2,896 (dev set)
- **Language:** Modern Standard Arabic (MSA)

### Retrieval Configuration
- **Dense:** mDPR (`castorini/mdpr-tied-pft-msmarco`) + FAISS prebuilt index
- **BM25:** BM25S (pure Python) with pre-built index
- **k:** 100 documents per query

### Evaluation Metrics
- Recall@10, Recall@100, NDCG@10, MRR

---

## Results

### Dense Retrieval

| Metric | Baseline (exp_001) | Falcon-H1 temp=0.1 | vs Baseline | vs Qwen 2.5 3B (exp_003) |
|--------|--------------------|--------------------|-------------|--------------------------|
| **NDCG@10** | 0.4993 | **0.5359** | +7.3% ✅ | 0.5435 (-1.4%) |
| **Recall@10** | 0.6156 | **0.6484** | +5.3% ✅ | 0.6608 (-1.9%) |
| **Recall@100** | 0.8407 | **0.8531** | +1.5% ✅ | 0.8594 (-0.7%) |
| **MRR** | 0.5328 | **0.5681** | +6.6% ✅ | 0.5742 (-1.1%) |

**Key Finding:** Falcon-H1 improves over the dense baseline across all metrics, but underperforms Qwen 2.5 3B by ~1–2% on each metric.

### BM25 Retrieval

| Metric | Baseline (exp_002) | Falcon-H1 temp=0.1 | vs Baseline | vs Qwen 2.5 3B (exp_004) |
|--------|--------------------|--------------------|-------------|--------------------------|
| **NDCG@10** | 0.4621 | 0.4038 | -12.6% ❌ | 0.4090 (-1.3%) |
| **Recall@10** | 0.5964 | 0.5311 | -11.0% ❌ | 0.5384 (-1.4%) |
| **Recall@100** | 0.8577 | 0.8084 | -5.7% ❌ | 0.8155 (-0.9%) |
| **MRR** | 0.4836 | 0.4274 | -11.6% ❌ | 0.4342 (-1.6%) |

**Key Finding:** Same pattern as exp_004 — simple concatenation hurts BM25 (term dilution). Falcon-H1 is slightly worse than Qwen for BM25 but the difference is small (~1%). The BM25 decline is a technique limitation, not a model limitation.

### Full Comparison Table

| Model | Retriever | NDCG@10 | Recall@10 | Recall@100 | MRR |
|-------|-----------|---------|-----------|------------|-----|
| No enhancement | Dense | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| No enhancement | BM25 | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| Qwen 2.5 3B (exp_003) | Dense | 0.5435 | 0.6608 | 0.8594 | 0.5742 |
| Qwen 2.5 3B (exp_004) | BM25 | 0.4090 | 0.5384 | 0.8155 | 0.4342 |
| **Falcon-H1-3B (exp_005)** | **Dense** | **0.5359** | **0.6484** | **0.8531** | **0.5681** |
| **Falcon-H1-3B (exp_005)** | **BM25** | **0.4038** | **0.5311** | **0.8084** | **0.4274** |

---

## Analysis

### 1. Arabic Benchmark Score ≠ Query Expansion Quality

Falcon-H1 has a higher Arabic OALL score (~62%) than Qwen 2.5 3B, yet Qwen outperforms it for query expansion (+1–2% on all dense metrics). Possible reasons:

- **Temperature effect:** Falcon's recommended temperature (0.1) produces highly deterministic, focused output. This may lack the lexical diversity that benefits retrieval.
- **OALL evaluates different skills:** Arabic reading comprehension, QA, and reasoning benchmarks don't directly measure the ability to write fluent, vocabulary-rich pseudo-documents for retrieval.
- **Batching limitation:** Single-query generation may produce slightly different output distributions than batch generation.

### 2. Dense Retrieval: Consistent Positive Effect

Both Falcon-H1 and Qwen 2.5 3B improve dense retrieval over baseline. The Query2Doc technique works for dense retrieval regardless of the LLM used (as long as Arabic output is coherent).

- Falcon NDCG@10 improvement: **+7.3%** (vs +8.9% for Qwen)
- Technique is robust but model choice matters at the margin.

### 3. BM25: Term Dilution Confirmed Again

The BM25 decline pattern (first seen in exp_004 with Qwen) repeats identically with Falcon-H1. This confirms the issue is the technique's naive concatenation, not the specific model. Both models show ~-11 to -13% NDCG@10 on BM25.

Fix (from Query2Doc paper): repeat original query 5× before concatenation for sparse retrieval.

### 4. Engineering Cost vs. Performance Gain

| | Qwen 2.5 3B | Falcon-H1-3B |
|--|-------------|-------------|
| **GPU required** | T4 (free) | A100 (Colab Pro+, ~$10/month) |
| **Batch size** | 8 | 1 |
| **Runtime** | ~40 min | ~60-90 min |
| **Dense NDCG@10** | 0.5435 | 0.5359 |
| **Complexity** | Low | High (bugs, OOM) |

The engineering overhead of Falcon-H1 is significantly higher while the retrieval quality is marginally lower.

---

## Sample Enhanced Queries (Sanity Check)

Verified before full run. Output was coherent Arabic, relevant to query.

**Example:**
- **Original:** `من هو علي بن محمد السمري؟`
- **Enhanced:** `من هو علي بن محمد السمري؟ [130-character Arabic pseudo-document about the historical figure]`

Output was in Arabic, relevant, and reasonable expansion ratio. Chat template (`apply_chat_template`) worked correctly — no fallback needed.

---

## Runtime Performance

| Phase | Time | Notes |
|-------|------|-------|
| Model download | ~3 min | ~6.3 GB (first run only) |
| Query generation | ~60-90 min | Single-query loop, A100 |
| Dense retrieval | ~5 min | FAISS prebuilt index download ~5 GB + search |
| BM25 retrieval | ~5 min | Pre-built index from Drive |
| Evaluation | <1 min | — |

- **Speed:** ~0.5–1 sec/query on A100 (vs ~0.83 sec/query for Qwen on T4)
- **Colab tier:** Pro+ required (A100, 40 GB)

---

## Files Generated

```
enhanced_queries_falcon_h1_3b_temp01.pkl   # Enhanced queries, saved to Google Drive
```

Pickle file structure:
```python
{
    'query_ids': [...],       # 2,896 query IDs
    'original': [...],        # Original query texts
    'enhanced': [...],        # Enhanced query texts (original + pseudo-doc)
    'metadata': {
        'model': 'tiiuae/Falcon-H1-3B-Instruct',
        'architecture': 'Hybrid Mamba2-Transformer (falcon_h1)',
        'temperature': 0.1,
        'max_new_tokens': 128,
        'batch_size': 1,
        'dtype': 'float16',
        'technique': 'query2doc',
        'dataset': 'miracl-ar-dev',
        'date': '2026-03-02T...',
        'num_queries': 2896,
        'runtime_minutes': ...
    }
}
```

---

## Lessons Learned

### Technical

1. **Hybrid architectures may have batching bugs** — always test `enhance()` single-query first before relying on `enhance_batch()`. For standard Transformers (Qwen, Llama, Gemma) this is a non-issue.

2. **VRAM estimate for Mamba2 models needs SSM overhead** — Falcon-H1 uses ~4 GB for SSM state buffers on top of model weights, not visible in the parameter count.

3. **Check GPU compute capability before setting dtype** — bfloat16 requires CC ≥ 8.0 (Ampere); T4 is CC 7.5 (Turing) and emulates bfloat16 slowly.

4. **`pyserini` is a hidden dependency in `MIRACLDataLoader`** — always include it even in generation-only notebooks.

5. **Transformers version matters for new architectures** — `pip install git+https://github.com/huggingface/transformers.git` for anything added in 2025.

### Research

1. **High Arabic NLP benchmark ≠ high query expansion quality** — Falcon-H1 outperforms Qwen on Arabic reading comprehension tasks but not on query expansion. These skills are different.

2. **Temperature interacts with retrieval quality** — Falcon's recommended temp=0.1 may be optimal for accuracy tasks but produce less lexically diverse expansions for retrieval. Testing temp=0.7 would reveal this.

3. **Query2Doc technique works reliably for dense retrieval** — both 3B models show consistent +7–9% NDCG@10 improvement, suggesting the technique is robust.

4. **BM25 incompatibility is technique-level, not model-level** — confirmed by identical decline pattern with two different models.

---

## Next Steps

1. [ ] **Run temperature=0.7** — compare Falcon temp=0.1 vs temp=0.7 to isolate temperature effect
2. [ ] **Test next model** — Qwen3-4B or Jais-2-8B-Chat (see `research_decisions/model_comparison_guide.md`)
3. [ ] **Fix BM25 implementation** — implement 5× query repetition as per Query2Doc paper recommendation

---

## References

1. Wang, L., Yang, N., & Wei, F. (2023). Query2doc: Query Expansion with Large Language Models. arXiv:2303.07678.
2. Zhang, X., et al. (2023). MIRACL: A Multilingual Retrieval Dataset. TACL.
3. TII (2025). Falcon-H1: A Family of Hybrid-Head Language Models. arXiv:2507.22448.
4. Model card: https://huggingface.co/tiiuae/Falcon-H1-3B-Instruct
5. Research notes: `research_decisions/falcon_h1_research.md`

---

**Experiment conducted by:** Mohammed Elhaj
**Institution:** University of Khartoum
**Date:** March 2, 2026
