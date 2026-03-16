# Qwen3-4B: Research & Technical Findings

**Date:** March 13, 2026
**Researcher:** Mohammed Elhaj
**Purpose:** Model comparison experiment (Task 4.0b) — Qwen3-4B evaluation
**Status:** COMPLETE — 2nd best model. Dense NDCG@10=0.5691 (+14.0% over baseline).

---

## 1. Model Overview

| Property | Value | Source |
|----------|-------|--------|
| **HuggingFace ID** | `Qwen/Qwen3-4B` | [Model Card](https://huggingface.co/Qwen/Qwen3-4B) |
| **Developer** | Alibaba Cloud (Qwen Team) | Model Card |
| **Parameters** | 4.0B total, 3.6B non-embedding | Model Card |
| **Architecture** | Standard dense Transformer (`Qwen3ForCausalLM`) | [config.json](https://huggingface.co/Qwen/Qwen3-4B/blob/main/config.json) |
| **Position Encoding** | RoPE (rope_theta=1,000,000) | config.json |
| **Activation** | SiLU (SwiGLU) | config.json |
| **Normalization** | RMSNorm (eps=1e-6) | config.json |
| **Attention** | GQA: 32 Q heads, 8 KV heads, head_dim=128 | config.json |
| **Hidden Size** | 2,560 | config.json |
| **Intermediate Size** | 9,728 | config.json |
| **Layers** | 36 | config.json |
| **Vocabulary** | 151,936 tokens | config.json |
| **Context Length** | 32,768 native; 131,072 with YaRN | Model Card |
| **max_position_embeddings** | 40,960 | config.json |
| **tie_word_embeddings** | true | config.json |
| **torch_dtype** | bfloat16 | config.json |
| **Languages** | 119 languages and dialects (including Arabic variants) | [Qwen3 Blog](https://qwenlm.github.io/blog/qwen3/) |
| **Training Data** | ~36 trillion tokens | Qwen3 Blog |
| **License** | Apache 2.0 | Model Card |
| **Paper** | [arXiv:2505.09388](https://arxiv.org/abs/2505.09388) | HF Collection |
| **transformers requirement** | >= 4.51.0 | Model Card |

### Why Consider for Testing
- **Standard Transformer:** No batching bugs (unlike Falcon-H1's hybrid Mamba architecture)
- **Matches Qwen2.5-7B performance at 4B params:** Demonstrated across multiple benchmarks
- **119 languages including Arabic dialects:** MSA, Najdi, Levantine, Egyptian, Moroccan, Mesopotamian, Ta'izzi-Adeni, Tunisian explicitly listed
- **Same vocab as Qwen 2.5:** 151,936 tokens — same tokenizer family, good Arabic tokenization
- **Fits on T4 in FP16/BF16** (see VRAM section)

---

## 2. Architecture Details

### Standard Dense Transformer (Good for Batching)

Qwen3-4B is a **standard decoder-only Transformer** — no Mamba, no SSM, no hybrid architecture. This means:
- Left-padding for batch generation works normally
- No SSM state buffers consuming extra VRAM
- Compatible with all attention backends (SDPA, eager, Flash Attention 2)
- `AutoModelForCausalLM.from_pretrained()` works out of the box

### Architecture Comparison: Qwen3-4B vs Qwen2.5-3B

| Property | Qwen3-4B | Qwen2.5-3B | Change |
|----------|----------|-------------|--------|
| **Parameters** | 4.0B (3.6B non-emb) | 3.09B (2.77B non-emb) | +29% params |
| **Hidden Size** | 2,560 | 2,048 | +25% wider |
| **Intermediate Size** | 9,728 | 11,008 | -12% narrower FFN |
| **Layers** | 36 | 36 | Same depth |
| **Q Heads** | 32 | 16 | 2x more heads |
| **KV Heads** | 8 | 2 | 4x more KV heads |
| **Head Dim** | 128 (2560/20? No: 2560/32=80... but config says 128) | 128 (2048/16=128) | See note |
| **Vocab Size** | 151,936 | 151,936 | Same |
| **Context Length** | 32,768 | 32,768 | Same |
| **max_position_embeddings** | 40,960 | 32,768 | +25% |
| **Languages** | 119 | 29+ | 4x more languages |
| **Training Tokens** | ~36T | ~18T | 2x more data |
| **tie_word_embeddings** | true | true | Same |
| **Activation** | SiLU | SiLU | Same |
| **Normalization** | RMSNorm | RMSNorm | Same |
| **model_type** | `qwen3` | `qwen2` | New model type |

**Note on head_dim:** config.json explicitly sets `head_dim: 128` despite hidden_size=2560 and num_attention_heads=32 (which would normally give 80). This means the attention layer projects to a larger dimension (32 * 128 = 4096) before attention, not using hidden_size directly. This is a deliberate architectural choice.

### Key Generational Differences (Qwen3 vs Qwen2.5)
1. **More GQA heads:** Qwen3-4B uses 32Q/8KV vs Qwen2.5-3B's 16Q/2KV — better attention quality
2. **Wider hidden, narrower FFN:** Shifted compute balance toward attention
3. **2x training data:** 36T tokens vs 18T tokens
4. **4x language coverage:** 119 vs 29 languages
5. **Thinking mode:** Qwen3 introduces built-in reasoning with `<think>` tags (critical for our use case)
6. **No sliding window:** Qwen3-4B has `use_sliding_window: false` — full attention throughout

---

## 3. VRAM Requirements

### FP16/BF16 Size
- **Safetensors total:** ~8.05 GB (3 files: 3.96 + 3.99 + 0.10 GB)
- **Model weights in memory:** ~8 GB in FP16/BF16
- **KV cache overhead (GQA):** With 8 KV heads * 128 dim * 36 layers * 2 (K+V) = moderate
- **Estimated total VRAM at inference:** ~9-10 GB for short sequences (batch_size=1)

### GPU Fit Analysis

| GPU | FP16 Fit? | Notes |
|-----|-----------|-------|
| **T4 (15 GB)** | YES | ~8 GB model + ~2-3 GB KV cache = ~10-11 GB. Leaves ~4 GB headroom. Batch generation possible with small batches. |
| **A100 (40 GB)** | YES, comfortably | Plenty of room for larger batch sizes |
| **V100 (16 GB)** | YES, tight | Similar to T4 |

### 4-bit Quantization (if needed)
- Estimated 4-bit size: ~2.5-3 GB
- Would leave ~12 GB free on T4 for batching

**Recommendation:** Start with FP16/BF16 on T4. No quantization needed. If OOM on batching, reduce batch_size before trying 4-bit.

---

## 4. CRITICAL: Thinking Mode

### What Is Thinking Mode?
Qwen3 models can generate internal reasoning in `<think>...</think>` tags before producing the final answer. This is enabled by default.

### How to Disable Thinking Mode

**Method 1: `enable_thinking=False` in chat template (RECOMMENDED)**
```python
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False  # Disables <think> tags
)
```

**Method 2: `/no_think` soft switch in user message**
```python
messages = [
    {"role": "user", "content": "Write a passage about X /no_think"}
]
# With enable_thinking=True, the /no_think tag disables thinking for this turn
```

**Method 3: `/think` and `/no_think` per-turn control**
```python
# Multi-turn: can toggle per message
messages = [
    {"role": "user", "content": "Complex math problem"},       # thinking ON
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "Summarize briefly /no_think"}, # thinking OFF
]
```

### Why We MUST Disable Thinking for Query Expansion
- **Thinking adds massive token overhead:** The `<think>` block can be thousands of tokens of internal reasoning before the actual answer
- **We only need the pseudo-document:** Our Query2Doc pipeline extracts the generated text as query expansion — we don't want reasoning artifacts
- **Cost:** Thinking mode wastes compute on reasoning we discard
- **Parsing complexity:** Would need to strip `<think>...</think>` from output

### Recommended Sampling Parameters

| Mode | Temperature | top_p | top_k | min_p |
|------|------------|-------|-------|-------|
| **Thinking enabled** | 0.6 | 0.95 | 20 | 0 |
| **Non-thinking (USE THIS)** | 0.7 | 0.8 | 20 | 0 |

**CRITICAL WARNING from model card:** "DO NOT use greedy decoding" — it causes performance degradation and endless repetitions. Always use sampling.

### Chat Template Internals
- When `enable_thinking=False`: The template does NOT add `<think>` tags to the generation prompt
- When `enable_thinking=True`: Template adds `<think>\n` after the assistant start token
- The `</think>` token ID is `151668` — used for parsing thinking content from output
- **Known bug (GitHub #1826):** When `enable_thinking=False`, the chat template creates inconsistent tokenization across turns, breaking KV-cache reuse in multi-turn conversations. For our single-turn query expansion, this is NOT an issue.

---

## 5. Known Issues & Warnings

### From HuggingFace Model Card
1. **Endless repetitions:** If encountered, set `presence_penalty=1.5`
2. **Requires transformers >= 4.51.0:** Earlier versions throw `KeyError: 'qwen3'`
3. **YaRN performance degradation:** Static YaRN scaling may hurt short texts — only enable for long contexts (we won't need this)
4. **rope_scaling warnings:** Upgrade transformers to silence warnings

### From GitHub Issues
1. **#1826 — KV-cache breaks with enable_thinking=False:** Chat template inconsistency in multi-turn. Not relevant for our single-turn use case.
2. **#1553 — Infinite repetition with emojis:** Edge case, unlikely for Arabic query expansion.
3. **#1817 — Tool calling fails ~60% in thinking mode:** Not relevant (we don't use tools).
4. **#1642 — Tab characters in JSON output:** Not relevant for our text generation.

### Potential Issues for Our Experiment
- **No `token_type_ids` issue reported** (unlike Jais-2 which required removing them)
- **No padding issues reported** for standard batch generation
- **Standard `AutoModelForCausalLM` loading** works without special model class

---

## 6. Benchmark Results

### Base Model Comparison (from Technical Report, arXiv:2505.09388, Table 7)

| Benchmark | Qwen2.5-3B | Qwen2.5-7B | Qwen3-4B | Qwen3-4B vs Q2.5-3B |
|-----------|-----------|-----------|---------|---------------------|
| **MMLU** | 65.62 | 74.16 | 72.99 | +7.37 |
| **MMLU-Redux** | 63.68 | 71.06 | 72.79 | +9.11 |
| **MMLU-Pro** | 34.61 | 45.00 | 50.58 | +15.97 |
| **SuperGPQA** | 20.31 | 26.34 | 28.43 | +8.12 |
| **BBH** | 56.30 | 70.40 | 72.59 | +16.29 |
| **GPQA** | 26.26 | 36.36 | 36.87 | +10.61 |
| **GSM8K** | 79.08 | 85.36 | 87.79 | +8.71 |
| **MATH** | 42.64 | 49.80 | 54.10 | +11.46 |
| **EvalPlus** | 46.28 | 62.18 | 63.53 | +17.25 |
| **MultiPL-E** | 39.65 | 50.73 | 53.13 | +13.48 |
| **MBPP** | 54.60 | 63.40 | 67.00 | +12.40 |
| **CRUX-O** | 36.50 | 48.50 | 55.00 | +18.50 |
| **MGSM** | 47.53 | 63.60 | 67.74 | +20.21 |
| **MMMLU** | 65.55 | 71.34 | 71.42 | +5.87 |
| **INCLUDE** | 45.90 | 53.98 | 56.29 | +10.39 |

**Key takeaway:** Qwen3-4B matches or exceeds Qwen2.5-7B on nearly every benchmark, while having only 4B parameters. The multilingual score (MMMLU 71.42) is close to Qwen2.5-7B (71.34), confirming strong multilingual capability.

### Arabic-Specific Benchmarks
- **OALL (Open Arabic LLM Leaderboard):** No Qwen3-4B results found on the leaderboard as of March 2026. The leaderboard data could not be retrieved (dynamic page).
- **AMMLU:** Not reported in the technical report for individual model sizes.
- **AraGen:** Not reported.
- **MMMLU (multilingual MMLU, includes Arabic):** 71.42 — significantly higher than Qwen2.5-3B (65.55).

### Comparison with Our Tested Models

| Model | Params | MMMLU | MMLU | Arabic Focus? |
|-------|--------|-------|------|--------------|
| Qwen3-4B | 4.0B | 71.42 | 72.99 | 119 langs, Arabic dialects listed |
| Qwen2.5-3B | 3.09B | 65.55 | 65.62 | 29 langs |
| Falcon-H1-3B | 3.15B | N/A | N/A | 18 langs, Arabic-first |
| Jais-2-8B | 8.09B | N/A | N/A | Arabic-first, custom vocab |

---

## 7. Training Data

### Pre-training: 36 Trillion Tokens
- **Coverage:** 119 languages and dialects
- **2x more than Qwen 2.5** (which used ~18T tokens)
- **Data sources:** Web content, PDF documents (extracted via Qwen2.5-VL), synthetic data (from Qwen2.5-Math and Qwen2.5-Coder)

### Training Stages
1. **Stage 1:** 30+ trillion tokens at 4K context length — broad knowledge acquisition
2. **Stage 2:** 5 trillion additional tokens emphasizing STEM, coding, reasoning — knowledge intensification
3. **Stage 3:** Context extension to 32K tokens

### Arabic Language Coverage
Qwen3 explicitly lists these Arabic variants in its training:
- Modern Standard Arabic (MSA) — **this is what MIRACL uses**
- Najdi Arabic
- Levantine Arabic
- Egyptian Arabic
- Moroccan Arabic
- Mesopotamian Arabic
- Ta'izzi-Adeni Arabic
- Tunisian Arabic

---

## 8. Implementation Notes for Our Experiment

### Loading the Model
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-4B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",  # Will use BF16
    device_map="auto"
)
```

### Query Expansion Generation (Non-Thinking Mode)
```python
messages = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False  # CRITICAL: disable thinking
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=128,
    temperature=0.7,  # Non-thinking recommended
    top_p=0.8,        # Non-thinking recommended
    top_k=20,         # Non-thinking recommended
    do_sample=True    # MUST sample, never greedy
)
```

### Batching Strategy
- **Architecture:** Standard Transformer — batching should work normally
- **Recommended starting batch_size:** 8 on A100, 4 on T4
- **Left-padding:** Use `tokenizer.padding_side = "left"` for batch generation
- **No known batching bugs** (unlike Falcon-H1)

### Critical Reminders
1. **`enable_thinking=False`** — always set this for query expansion
2. **Never use greedy decoding** — always `do_sample=True` with temperature > 0
3. **transformers >= 4.51.0** required
4. **No `token_type_ids` issues reported** — but remove from inputs if model complains (standard precaution)

---

## 9. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Thinking mode accidentally enabled | HIGH | Always pass `enable_thinking=False` |
| Greedy decoding causes repetitions | HIGH | Always use `do_sample=True`, temp=0.7 |
| OOM on T4 | LOW | 8 GB model fits in 15 GB; reduce batch_size if needed |
| transformers version too old | MEDIUM | Require >= 4.51.0 at notebook top |
| Repetitive outputs | MEDIUM | Set `presence_penalty=1.5` if observed |
| Arabic performance unknown | MEDIUM | No OALL scores; rely on MMMLU (71.42) as proxy |

---

## 10. Summary & Recommendation

**Qwen3-4B is a strong candidate for our Arabic query expansion experiment.**

Pros:
- Standard Transformer — no batching issues like Falcon-H1
- Matches Qwen2.5-7B benchmarks at 4B params — major efficiency gain
- 119 languages with explicit Arabic dialect support
- Trained on 2x more data than Qwen 2.5 (36T vs 18T tokens)
- Fits on T4 in FP16 without quantization
- Same vocab/tokenizer family as Qwen 2.5 (proven Arabic tokenization)

Cons:
- Thinking mode must be explicitly disabled — easy to forget
- No published Arabic-specific benchmarks (OALL, AMMLU)
- Slightly larger than our 3B comparison group (4B vs 3B)
- Must use sampling (no greedy) — slight non-determinism

**Verdict:** Proceed with experiment. Use `enable_thinking=False` and non-thinking sampling parameters (temp=0.7, top_p=0.8, top_k=20).

---

## 11. Experiment Results (exp_007)

**Date:** March 16, 2026
**Status:** COMPLETE

### Configuration (Actual)

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA A100-SXM4-40GB |
| Precision | FP16 (no quantization) |
| VRAM used | 8.5 GB (33.9 GB free) |
| Batch size | 32 |
| Temperature | 0.7 |
| top_p | 0.8 |
| top_k | 20 |
| max_new_tokens | 128 |
| enable_thinking | False |
| Queries | 2,896 (MIRACL Arabic dev) |
| Errors | 0 |

### Performance

| Metric | Value |
|--------|-------|
| **Runtime** | **12.4 minutes** |
| **Speed** | **232.6 queries/min** |

### Dense Retrieval Results

| Metric | Baseline (mDPR) | Qwen3-4B | Change | vs Qwen 2.5 3B |
|--------|-----------------|----------|--------|-----------------|
| **Recall@10** | 0.6156 | **0.6824** | **+10.9%** | +3.3% over Qwen (0.6608) |
| **Recall@100** | 0.8407 | **0.8726** | **+3.8%** | +1.5% over Qwen (0.8594) |
| **NDCG@10** | 0.4993 | **0.5691** | **+14.0%** | +4.7% over Qwen (0.5435) |
| **MRR** | 0.5328 | **0.6015** | **+12.9%** | +4.8% over Qwen (0.5742) |

### BM25 Retrieval Results

| Metric | Baseline (BM25) | Qwen3-4B | Change |
|--------|-----------------|----------|--------|
| **Recall@10** | 0.5964 | 0.5403 | -9.4% |
| **Recall@100** | 0.8577 | 0.8152 | -5.0% |
| **NDCG@10** | 0.4621 | 0.4145 | -10.3% |
| **MRR** | 0.4836 | 0.4415 | -8.7% |

### All Models Comparison (Dense)

| Model | NDCG@10 | Recall@10 | Recall@100 | MRR | vs Baseline |
|-------|---------|-----------|------------|-----|-------------|
| mDPR baseline | 0.4993 | 0.6156 | 0.8407 | 0.5328 | — |
| ALLaM-7B (exp_008) | 0.2550 | 0.3335 | 0.5465 | 0.2708 | -48.9% NDCG |
| Falcon-H1-3B (exp_005) | 0.5359 | 0.6484 | 0.8531 | 0.5681 | +7.3% NDCG |
| Qwen 2.5 3B (exp_003) | 0.5435 | 0.6608 | 0.8594 | 0.5742 | +8.9% NDCG |
| **Qwen3-4B (exp_007)** | **0.5691** | **0.6824** | **0.8726** | **0.6015** | **+14.0% NDCG** |
| Jais-2-8B (exp_006) | 0.6018 | 0.7161 | 0.8981 | 0.6356 | +20.5% NDCG |

### Key Findings

1. **Generational improvement confirmed.** Qwen3-4B beats Qwen 2.5-3B on every metric (+4.7% NDCG, +3.3% Recall@10, +4.8% MRR). The 2x training data, 119 languages, and wider architecture translate directly to better Arabic QE.

2. **2nd best model overall.** Ranks behind Jais-2-8B but significantly ahead of Qwen 2.5-3B and Falcon-H1.

3. **BM25 term dilution continues.** Same pattern as all non-Jais models. Only Jais-2's concise Arabic expansions improve BM25.

4. **Training data > Arabic specialization.** Qwen3-4B (multilingual, 36T tokens) outperforms Falcon-H1 (Arabic-specialized, OALL ~62%). Volume matters more than benchmark scores for QE.

5. **Easiest model in the comparison.** No batching bugs, no dtype issues, no token_type_ids. Just disable thinking and run.

---

## 12. Lessons Applied from Previous Experiments

| Lesson Source | Lesson | Application to Qwen3-4B |
|--------------|--------|------------------------|
| Falcon-H1 (exp_005) | Hybrid architectures have batching bugs | Qwen3 is standard Transformer — no issue |
| Falcon-H1 (exp_005) | VRAM estimates must include SSM buffers | No SSM buffers — standard VRAM calculation |
| Falcon-H1 (exp_005) | Model-specific temperature matters | temp=0.7 matches both baseline and Qwen3's non-thinking recommendation |
| Falcon-H1 (exp_005) | Always test single-query first | Sanity check on first 5 queries before full run |
| Falcon-H1 (exp_005) | `pyserini` is hidden dependency | Included in install cell |
| Jais-2 (exp_006) | Must remove `token_type_ids` | Not needed for Qwen3 (doesn't produce them) |
| Jais-2 (exp_006) | Standard Transformer allows batching | Same here — batch_size=32 on A100 |
| **NEW for Qwen3** | Thinking mode produces `<think>` tags | Must disable with `enable_thinking=False` — worked perfectly, zero leaks |
| **NEW for Qwen3** | Never use greedy decoding | Always `do_sample=True`, temp >= 0.6 |
| **NEW for Qwen3** | `total_mem` vs `total_memory` | Correct attr is `torch.cuda.get_device_properties(0).total_memory` |
