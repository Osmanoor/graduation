# Jais-2-8B-Chat: Research & Technical Findings

**Date:** March 8, 2026
**Researcher:** Mohammed Elhaj
**Purpose:** Model comparison experiment (Task 4.0b) — Jais-2-8B-Chat evaluation
**Status:** Pre-experiment research complete

---

## 1. Model Overview

| Property | Value | Source |
|----------|-------|--------|
| **HuggingFace ID** | `inceptionai/Jais-2-8B-Chat` | [Model Card](https://huggingface.co/inceptionai/Jais-2-8B-Chat) |
| **Developers** | Inception (G42), MBZUAI, Cerebras | [Cerebras Blog](https://www.cerebras.ai/blog/jais2) |
| **Parameters** | 8.09B | HF metadata |
| **Architecture** | `jais2` — standard decoder-only Transformer | [HF Docs](https://huggingface.co/docs/transformers/main/en/model_doc/jais2) |
| **Position Encoding** | RoPE (Rotary Position Embeddings) | Jais2Config |
| **Activation** | Squared-ReLU (`relu2`) | Jais2Config |
| **Normalization** | LayerNorm (NOT RMSNorm) | Jais2Config |
| **Attention** | MHA, 26 heads, 2 KV heads (GQA possible but defaults to MHA) | Jais2Config |
| **Hidden Size** | 3,328 | Jais2Config |
| **Layers** | 32 | Jais2Config |
| **Vocabulary** | 150,272 tokens (Arabic-centric) | Jais2Config |
| **Context Length** | 8,192 tokens | Jais2Config |
| **Parameterization** | muP (Maximal Update Parameterization) | Model card |
| **Tensor Type** | BF16 | HF repo |
| **Release Date** | December 9, 2024 | [MBZUAI Press Release](https://mbzuai.ac.ae/news/inception-cerebras-and-mbzuai-release-jais-2-the-next-generation-of-the-worlds-leading-arabic-open-weight-llm/) |
| **License** | Apache 2.0 (gated — click-through acceptance on HF) | Model card |

### Why Selected for Testing
- **Best 8B Arabic model:** Outperforms Fanar-1-9B and ALLaM-7B on AraGen benchmarks (Model card)
- **Custom Arabic vocabulary:** 150,272 tokens trained from scratch with Arabic-centric tokenization
- **Massive training data:** 2.6 trillion tokens (Arabic + English + code) — 6.6x more than Jais-1
- **Three-stage fine-tuning:** SFT → DPO → GRPO (most thorough alignment pipeline)
- **Standard Transformer:** No batching bugs (unlike Falcon-H1's hybrid Mamba architecture)

---

## 2. Architecture Details

### Standard Transformer (Good for Batching)

Unlike Falcon-H1-3B (hybrid Mamba2-Transformer with batching bugs), Jais-2 is a **standard decoder-only Transformer**. This means:
- Left-padding for batch generation works normally
- No SSM state buffers consuming extra VRAM
- Compatible with all attention backends (SDPA, eager, Flash Attention 2)
- `AutoModelForCausalLM.from_pretrained()` works out of the box

### Jais-2 vs Jais-1 Architecture Changes

| Aspect | Jais-1 (2023) | Jais-2 (2024) |
|--------|--------------|---------------|
| Position encoding | ALiBi | **RoPE** |
| Activation | SwiGLU | **Squared-ReLU** |
| Training tokens | 395B | **2.6T** (6.6x more) |
| FFN ratio | Standard | **8:1 filter-to-hidden** |
| Fine-tuning | SFT only | **SFT + DPO + GRPO** |
| Architecture | GPT-3 style (some adapted from LLaMA-2) | Custom `jais2` from scratch |

Source: [Cerebras Blog: Jais 2](https://www.cerebras.ai/blog/jais2)

---

## 3. Arabic Benchmarks

### AraGen-12-24 (3C3H) — from Model Card

| Metric | Score |
|--------|-------|
| **Overall 3C3H** | **58.64%** |
| Correctness | 68.94 |
| Completeness | 68.10 |
| Helpfulness | 66.88 |
| Harmlessness | 68.88 |

Outperforms Fanar-1-9B and ALLaM-7B on this benchmark.

### IFEval (Strict 0-shot)

| Language | Prompt | Instruction |
|----------|--------|-------------|
| English | 63.14 | 72.80 |
| Arabic | 58.17 | 67.09 |

### Benchmark Limitations
- **No OALL v2 score found** for Jais-2-8B-Chat specifically
- **No direct head-to-head** with Qwen 2.5 3B or Falcon-H1-3B on same benchmarks
- The AraGen benchmark focuses on generative quality — relevant for query expansion

---

## 4. VRAM & Performance Estimates

### Memory Requirements

| Configuration | Weights | Total (with overhead) |
|--------------|---------|----------------------|
| FP16/BF16 | ~16.2 GB | ~18-20 GB |
| 4-bit NF4 | ~4.0 GB | ~6-8 GB |

Confirmed by GGUF file sizes: BF16.gguf = 15.4 GiB, Q4_K_M.gguf = 4.8 GiB.
Source: [GGUF repo](https://huggingface.co/inceptionai/Jais-2-8B-Chat-GGUF)

### A100 40GB Batch Size Estimates (4-bit NF4, 128 max_new_tokens)

| Batch Size | Estimated VRAM | Feasible? |
|-----------|---------------|-----------|
| 1 | ~8 GB | Yes |
| 8 | ~12-14 GB | Yes |
| 16 | ~16-20 GB | Yes |
| 32 | ~22-28 GB | Likely yes |

**Recommendation for our experiment:** Start with `batch_size=8`, try `batch_size=16`. We have ~32 GB headroom after model load.

### CRITICAL: Must Use BF16, NOT FP16

**Discovered during experiment:** Loading Jais-2 in FP16 causes `CUDA device-side assert` error during `torch.multinomial` sampling.

**Root cause:** Jais-2's **Squared-ReLU** activation squares intermediate values. These can exceed FP16's maximum representable value (~65,504), producing NaN/Inf in the probability distribution. BF16 handles up to ~3.4e38, so it works correctly.

**Fix:** Use `torch_dtype=torch.bfloat16` (NOT `torch.float16`). A100 supports BF16 natively (compute capability 8.0). T4 does NOT support BF16 natively (compute capability 7.5) — use 4-bit quantization with `bnb_4bit_compute_dtype=torch.bfloat16` on T4.

This is the same dtype issue encountered with Falcon-H1 in exp_005 (which also required BF16 on A100).

### A100 BF16 Option (Recommended — No Quantization)

With A100's 40 GB, we run Jais-2 in **BF16 without quantization** (~18-20 GB), leaving ~20 GB for batching. This preserves full quality.

| Config | Batch Size | Expected Runtime (2,896 queries) |
|--------|-----------|----------------------------------|
| 4-bit, batch=8 | 8 | ~30-45 min |
| 4-bit, batch=16 | 16 | ~20-30 min |
| BF16, batch=4 | 4 | ~45-60 min |
| BF16, batch=8 | 8 | ~30-45 min |

---

## 5. Known Technical Quirks

### 5.1 MUST Remove `token_type_ids` Before `generate()`

The model card **explicitly** shows this in its code example:
```python
inputs.pop("token_type_ids", None)
```
Failure to do this causes an error. This is documented and our notebook handles it.

### 5.2 `pad_token` Not Set by Default

`pad_token_id` is None in the config. Must set manually:
```python
tokenizer.pad_token = tokenizer.eos_token
```

### 5.3 Left-padding for Batch Generation

Standard decoder-only model practice:
```python
tokenizer.padding_side = 'left'
```

### 5.4 Gated Model — Requires HF Login

Must accept terms at https://huggingface.co/inceptionai/Jais-2-8B-Chat before downloading.
Use `notebook_login()` in Colab.

### 5.5 MUST Use BF16 (NOT FP16) — Squared-ReLU Overflow

**Discovered experimentally.** FP16 causes `CUDA device-side assert` during `torch.multinomial`. Jais-2's Squared-ReLU activation produces intermediate values exceeding FP16 range (~65,504). BF16 (max ~3.4e38) works correctly. Use `torch_dtype=torch.bfloat16` on A100, or `bnb_4bit_compute_dtype=torch.bfloat16` for 4-bit on T4.

### 5.6 No Other Known Bugs

No other generation bugs reported. Standard Transformer = standard behavior. This is a major advantage over Falcon-H1.

---

## 6. Implications for Our Experiment (exp_006)

### Advantages Over Falcon-H1 (exp_005)
1. **Batching works** — can use batch_size=8-16 on A100 (vs batch_size=1 for Falcon)
2. **No architecture bugs** — standard Transformer, no SSM state buffer overhead
3. **Arabic-specialized vocabulary** — 150K token Arabic-centric tokenizer may produce better Arabic text
4. **More training data** — 2.6T tokens (Jais-2) vs unknown but likely less for Falcon-H1-3B
5. **Three-stage alignment** — SFT + DPO + GRPO = better instruction following

### Potential Concerns
1. **4-bit quantization quality** — 8B model in 4-bit may lose some Arabic nuance vs FP16
2. **8K context limit** — shorter than Falcon-H1's 128K, but our queries + 128 token generation = ~500 tokens total, well within limit
3. **No OALL benchmark** — can't directly compare Arabic quality pre-experiment
4. **Temperature:** Model card shows greedy decoding (temp=0). Need to test if temp=0.7 produces good diverse output or if lower temp is better

### Experiment Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **GPU** | A100 (Colab Pro) | Maximize batching throughput |
| **Precision** | BF16 (not FP16 — Squared-ReLU overflow) | A100 has native BF16 support |
| **Batch size** | 16 (suggested by VRAM auto-check) | Standard Transformer, no batching bugs |
| **Temperature** | 0.7 (match exp_003/exp_005 for fair comparison) | Worked well, model card suggests 0 |
| **max_new_tokens** | 128 (same as all other experiments) | Fair comparison |

---

## 9. Experiment Results (Query Generation Phase)

**Date:** March 14, 2026
**Status:** Query generation complete, Dense evaluation pending

### Configuration (Actual)

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100-SXM4-40GB |
| Precision | BF16 (model native dtype, no quantization) |
| VRAM used | 16.6 GB (25.8 GB free) |
| Batch size | 16 |
| Temperature | 0.7 |
| max_new_tokens | 128 |
| Queries | 2,896 (MIRACL Arabic dev) |
| Errors | 0 |

### Performance

| Metric | Value |
|--------|-------|
| **Runtime** | **12.0 minutes** |
| **Speed** | **241.5 queries/min** |
| Checkpoint every | 200 queries |

### Expansion Statistics

| Stat | Value |
|------|-------|
| Avg original length | 29.5 chars |
| Avg enhanced length | 256.0 chars |
| Avg expansion ratio | 10.46x |
| Median expansion | 5.04x |
| Min expansion | 1.13x |
| Max expansion | 51.00x |

### Comparison with Previous Models (Generation Phase Only)

| Model | Params | GPU | Precision | Batch | Runtime | Speed |
|-------|--------|-----|-----------|-------|---------|-------|
| Qwen 2.5 3B | 3B | T4 | FP16 | 8 | ~40 min | ~72 q/min |
| Falcon-H1-3B | 3.15B | A100 | BF16 | 1 | ~60-90 min | ~32-48 q/min |
| **Jais-2-8B** | **8.09B** | **A100** | **BF16** | **16** | **12 min** | **241.5 q/min** |

### Observations from Sanity Check
- Arabic output is coherent and relevant
- Some queries get very concise factual answers (e.g., "القديس بطرس" for "who is the saint called the rock?" — 2.5x ratio)
- Other queries get rich multi-paragraph expansions (21x ratio)
- High variance (1.13x–51.00x) suggests the model adapts output length to query complexity
- Median (5.04x) is lower than Qwen 2.5 3B (8.45x) — Jais-2 may be more concise/factual

---

## 10. Retrieval Evaluation Results

**Date:** March 14, 2026
**Status:** COMPLETE

### Dense Retrieval (mDPR)

| Metric | Baseline (mDPR) | Jais-2-8B | Change | vs Qwen 2.5 3B |
|--------|-----------------|-----------|--------|-----------------|
| **Recall@10** | 0.6156 | **0.7161** | **+16.3%** | +8.4% over Qwen (0.6608) |
| **Recall@100** | 0.8407 | **0.8981** | **+6.8%** | +4.5% over Qwen (0.8594) |
| **NDCG@10** | 0.4993 | **0.6018** | **+20.5%** | +10.7% over Qwen (0.5435) |
| **MRR** | 0.5328 | **0.6356** | **+19.3%** | +10.7% over Qwen (0.5742) |

### BM25 Retrieval (BM25S)

| Metric | Baseline (BM25) | Jais-2-8B | Change | vs Qwen 2.5 3B |
|--------|-----------------|-----------|--------|-----------------|
| **Recall@10** | 0.5964 | **0.6448** | **+8.1%** | Qwen HURT it (0.5384, -9.7%) |
| **Recall@100** | 0.8577 | **0.8834** | **+3.0%** | Qwen HURT it (0.8155, -4.9%) |
| **NDCG@10** | 0.4621 | **0.5122** | **+10.8%** | Qwen HURT it (0.4090, -11.5%) |
| **MRR** | 0.4836 | **0.5397** | **+11.6%** | Qwen HURT it (0.4342, -10.2%) |

### All Models Comparison (Dense)

| Model | NDCG@10 | Recall@10 | Recall@100 | MRR | vs Baseline |
|-------|---------|-----------|------------|-----|-------------|
| mDPR baseline | 0.4993 | 0.6156 | 0.8407 | 0.5328 | — |
| Qwen 2.5 3B (exp_003) | 0.5435 | 0.6608 | 0.8594 | 0.5742 | +8.9% NDCG |
| Falcon-H1-3B (exp_005) | 0.5359 | 0.6484 | 0.8531 | 0.5681 | +7.3% NDCG |
| **Jais-2-8B (exp_006)** | **0.6018** | **0.7161** | **0.8981** | **0.6356** | **+20.5% NDCG** |

### Key Findings

1. **Jais-2 is the best model by a wide margin.** +20.5% NDCG@10 over baseline — more than double the improvement of Qwen 2.5 3B (+8.9%) and Falcon-H1 (+7.3%).

2. **First model to improve BM25 retrieval.** Qwen 2.5 3B actually hurt BM25 performance (-11.5% NDCG). Jais-2 improved it by +10.8%. This suggests Jais-2's expansions contain more lexically relevant Arabic terms (important for term-matching in BM25).

3. **Arabic-specialized training matters.** Jais-2's 150K Arabic-centric vocabulary and 2.6T training tokens (with heavy Arabic representation) produce expansions with better Arabic vocabulary coverage than multilingual models.

4. **Concise expansions work better.** Despite lower median expansion ratio (5.04x vs Qwen's 8.45x), Jais-2 achieved much better retrieval. This suggests that quality and relevance of expansion terms matters more than quantity.

5. **Size + specialization > size alone.** 8B Arabic-specialized model (Jais-2) massively outperforms 3B multilingual models (Qwen, Falcon-H1), even accounting for the parameter advantage.

---

## 7. Citations

### Jais-2 (No Published Paper Yet)
- **Blog:** "Jais 2: A Blueprint for Sovereign AI." Cerebras Blog, December 2024. https://www.cerebras.ai/blog/jais2
- **Press Release:** MBZUAI, December 2024. https://mbzuai.ac.ae/news/inception-cerebras-and-mbzuai-release-jais-2-the-next-generation-of-the-worlds-leading-arabic-open-weight-llm/
- **Model Card:** https://huggingface.co/inceptionai/Jais-2-8B-Chat

### Original Jais Paper (for thesis citation)
> Sengupta, N., Sahu, S.K., Jia, B., et al. (2023). "Jais and Jais-chat: Arabic-Centric Foundation and Instruction-Tuned Open Generative Large Language Models." arXiv:2308.16149.

### HuggingFace Transformers
- Jais2 documentation: https://huggingface.co/docs/transformers/main/en/model_doc/jais2
- GGUF quantizations: https://huggingface.co/inceptionai/Jais-2-8B-Chat-GGUF

---

## 8. Lessons from Falcon-H1 (exp_005) Applied to Jais-2

| Falcon-H1 Lesson | Application to Jais-2 |
|-------------------|----------------------|
| Hybrid architectures have batching bugs | Jais-2 is standard Transformer — no issue |
| VRAM estimates must include SSM buffers | No SSM buffers in Jais-2 — standard VRAM calculation |
| Model-specific temperature matters | Test both temp=0.7 (standard) and temp=0 (model default) |
| Always test single-query first | Still do sanity check on first 5 queries before full run |
| `pyserini` is hidden dependency | Already included in install cell |
| A100 eliminates OOM issues | Use A100 from the start, maximize batch size |
