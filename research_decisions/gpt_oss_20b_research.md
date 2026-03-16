# GPT-OSS-20B: Research & Technical Findings

**Date:** March 16, 2026
**Researcher:** Mohammed Elhaj
**Purpose:** Model comparison experiment (Task 4.0b) — GPT-OSS-20B evaluation
**Status:** COMPLETE — DROPPED. Too slow (est. 14h on A100) + severe hallucinations. Not viable for Arabic QE.

---

## 1. Model Overview

| Property | Value | Source |
|----------|-------|--------|
| **HuggingFace ID** | `openai/gpt-oss-20b` | [Model Card](https://huggingface.co/openai/gpt-oss-20b) |
| **Developer** | OpenAI | [Announcement](https://openai.com/index/introducing-gpt-oss/) |
| **Parameters** | 20.91B total, **3.61B active per token** | [Paper](https://arxiv.org/abs/2508.10925) Table 1 |
| **Architecture** | MoE Transformer (`GptOssForCausalLM`) | config.json |
| **Experts** | 32 total, top-4 routed per token | Paper Section 2.2 |
| **Position Encoding** | RoPE with YaRN scaling (factor=32) | config.json |
| **Activation** | Gated SwiGLU (with clamping, `swiglu_limit: 7.0`) | config.json |
| **Normalization** | RMSNorm (eps=1e-5), pre-LN | config.json |
| **Attention** | GQA: 64 Q heads, 8 KV heads, head_dim=64 | config.json |
| **Hidden Size** | 2,880 | config.json |
| **Layers** | 24 | config.json |
| **Vocabulary** | 201,088 tokens (o200k_harmony BPE via tiktoken) | Paper Section 2.3 |
| **Context Length** | 131,072 tokens (128K) | config.json |
| **Quantization** | Native MXFP4 on MoE weights (4.25 bits/param) | Paper Section 2.1 |
| **Checkpoint Size** | 12.8 GiB | Paper Table 1 |
| **Release Date** | August 5, 2025 | OpenAI announcement |
| **Paper** | arXiv:2508.10925 | HuggingFace |
| **License** | Apache 2.0 | Model card |
| **transformers_version** | >= 4.55.0 (dev) | config.json |

### Why Selected for Testing
- **OpenAI's first open-source model:** Historic release, Apache 2.0 license
- **MoE architecture:** Only MoE model in our comparison — unique thesis finding regardless of results
- **Only 3.6B active params:** Despite 20.9B total, compute cost is similar to a 3.6B dense model
- **Fits on T4:** Native MXFP4 quantization keeps checkpoint at 12.8 GiB
- **Strong English reasoning:** Rivals o3-mini on AIME (92.1%), GPQA Diamond (71.5%)
- **English-dominant training:** NOT Arabic-specialized — tests whether general English capability transfers to Arabic QE

### Why This Experiment Matters for Thesis
This is the **only non-Arabic-specialized model AND the only MoE model** in our comparison:
- If it performs well despite English-dominant training → general-purpose MoE models can do Arabic QE
- If it performs poorly → confirms importance of Arabic-specialized training data for QE
- Either way, the MoE vs dense architecture comparison is a novel contribution

---

## 2. Architecture: Mixture of Experts (MoE) Transformer

### MoE Configuration

| Component | Params | % of Total |
|-----------|--------|------------|
| **MLP (MoE experts)** | 19.12B | 91.4% |
| **Attention** | 0.64B | 3.1% |
| **Embed + Unembed** | 1.16B | 5.5% |
| **Total** | 20.91B | 100% |
| **Active per token** | 3.61B | 17.3% |

Each MoE layer has 32 experts. A learned router (linear projection + softmax) selects the **top-4 experts** per token. Only these 4 experts compute on that token; the other 28 contribute nothing.

### Attention Pattern: Alternating Sliding Window + Full

The 24 layers alternate between:
- **Sliding window attention** (bandwidth=128 tokens) — efficient local attention
- **Full attention** — standard global attention

This alternating pattern is defined in `layer_types` in config.json. Each attention head also has a **learned bias in the softmax denominator** (attention sinks).

### Architecture Comparison with Our Models

| Aspect | GPT-OSS-20B | Jais-2-8B | Qwen3-4B | Falcon-H1-3B |
|--------|-------------|-----------|----------|---------------|
| Type | MoE Transformer | Dense Transformer | Dense Transformer | Hybrid Mamba-Transformer |
| Total params | 20.91B | 8.09B | 4.0B | 3.15B |
| **Active params** | **3.61B** | **8.09B** | **4.0B** | **3.15B** |
| Experts | 32 (top-4) | N/A | N/A | N/A |
| Layers | 24 | 32 | 36 | 32 |
| Hidden | 2,880 | 3,328 | 2,560 | 2,560 |
| Attention heads | 64 | 26 | 32 | 10 |
| KV heads | 8 | 2 | 8 | 2 |
| Head dim | 64 | 128 | 128 | 128 |
| Vocab | 201,088 | 150,272 | 151,936 | Unknown |
| Context | 128K | 8K | 32K | 128K |
| Batching | Should work (standard Transformer) | Works | Works | BROKEN (bug) |

### Implications for Batching
GPT-OSS-20B is a **standard Transformer** (NOT hybrid like Falcon-H1). MoE routing is a simple linear projection + softmax — it should be compatible with batched generation. However:
- MoE models can have higher memory overhead during batching (different experts activated per sample)
- The alternating sliding window / full attention pattern may add complexity
- **Test with small batch sizes first** (4-8) before scaling up

---

## 3. Quantization: Native MXFP4

### What is MXFP4?
MXFP4 (Microscaling FP4) is a 4-bit floating-point format standardized by the Open Compute Project (OCP):
- **Block size:** 32 values share a single FP8 (E8M0) scale factor
- **Effective bits:** 4.25 bits per parameter
- **Applied to:** MoE expert weights ONLY (90%+ of total params)
- **NOT applied to:** Attention layers, router, embeddings, LM head (remain BF16)

### Critical: MXFP4 Was Used DURING Training
Unlike post-training quantization (NF4, GPTQ, AWQ), GPT-OSS's MoE weights were **trained at MXFP4 precision**. All published benchmarks reflect MXFP4 performance — this is the model's native precision, not a lossy approximation.

### MXFP4 vs Other Quantization Formats

| Format | Block Size | Applied | Quality Loss |
|--------|-----------|---------|-------------|
| **MXFP4 (GPT-OSS)** | 32 values | During training | None (native) |
| NF4 (bitsandbytes) | Per-group | Post-training | Some |
| GPTQ | Per-group | Post-training (calibration) | Some |
| AWQ | Per-group | Post-training (activation-aware) | Minimal |

### Hardware Compatibility

| GPU | Compute Cap | Native MXFP4? | Workaround |
|-----|------------|---------------|------------|
| H100, B100 | >= 9.0 | YES | N/A |
| **A100** | 8.0 | NO | Triton kernel emulation |
| **T4** | 7.5 | NO | Triton kernel emulation |

**The HuggingFace `transformers` library initially blocked non-H100 GPUs** with error: `"MXFP4 quantized models is only supported on GPUs with compute capability >= 9.0"`. This was fixed in PRs #39940 and #40026 (requires latest transformers from source + `kernels` + `triton>=3.4.0`).

### Two Loading Paths

| Path | Model ID | Quantization | T4 Compatible? | Complexity |
|------|----------|-------------|----------------|------------|
| **Unsloth (RECOMMENDED)** | `unsloth/gpt-oss-20b` | bitsandbytes NF4 | YES | Low |
| **HuggingFace native** | `openai/gpt-oss-20b` | Native MXFP4 via Triton | YES (patched) | High |
| **GGUF** | `unsloth/gpt-oss-20b-GGUF` | Various (Q4_K_M etc.) | N/A (CPU) | Low |

**For our experiment:** Use the Unsloth path (`load_in_4bit=True`). It's the most tested on Colab T4/A100 and avoids MXFP4 hardware compatibility issues entirely.

---

## 4. Chat Format: Harmony (MANDATORY)

### Critical Warning
From the paper: *"should only be used with the harmony format as it will not work correctly otherwise"*

### Harmony Format Structure
```
<|start|>ROLE<|message|>CONTENT<|end|>
```

Output channels:
- `analysis` — Chain-of-thought reasoning (not shown to users)
- `commentary` — Function calling preambles
- `final` — Answers shown to users

### Using with HuggingFace
`tokenizer.apply_chat_template()` handles harmony format automatically:
```python
messages = [{"role": "user", "content": "..."}]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
    reasoning_effort="low"  # "low", "medium", "high"
)
```

### Reasoning Effort Control
| Level | Effect | For Query Expansion |
|-------|--------|-------------------|
| `low` | Minimal CoT, faster | RECOMMENDED — we don't need reasoning |
| `medium` | Balanced | Fallback if `low` produces poor output |
| `high` | Deep reasoning, slowest | Overkill for QE |

### Special Tokens
| Token ID | Token | Purpose |
|----------|-------|---------|
| 199998 | `<\|startoftext\|>` | BOS |
| 199999 | `<\|endoftext\|>` | PAD |
| 200002 | `<\|return\|>` | EOS |
| 200006 | `<\|start\|>` | Harmony start |
| 200007 | `<\|end\|>` | Harmony end |
| 200008 | `<\|message\|>` | Message marker |

### Known Bug (Discussion #215)
Chat template missing `<|constrain|>` tokens for tool calling. Does NOT affect basic text generation — only tool/function calls.

---

## 5. Arabic Benchmarks & Multilingual Assessment

### Arabic MMMLU (from Paper, Table 2)

| Model | low | medium | high |
|-------|-----|--------|------|
| **gpt-oss-20b** | **65.6** | **73.4** | **76.3** |
| gpt-oss-120b | 75.0 | 80.4 | 82.7 |
| o3-mini (high) | 81.9 | — | — |
| o4-mini (high) | 86.1 | — | — |

Arabic MMMLU 76.3 (high reasoning) is decent but below proprietary models.

### ILMAAM Arabic Benchmark (Community Evaluation)

| Model | Avg Accuracy | Source |
|-------|-------------|--------|
| GPT-OSS-20B | ~58% | [HuggingFace Blog](https://huggingface.co/blog/Omartificial-Intelligence-Space/gpt-oss-eval-on-ilmaam-benchamrks) |
| GPT-OSS-120B | ~74.5% | Same |

**Largest gap:** Arabic Language (Middle School) — 120B beats 20B by **48 percentage points**. This suggests the 20B model handles Arabic language tasks poorly.

### Multilingual Weaknesses (from arXiv 2508.12461)
- Both GPT-OSS models achieved **below 45% accuracy on Chinese tasks**
- GPT-OSS-20B scored **28% on C-Eval** (Chinese)
- Paper concludes: *"general-purpose pretraining alone is insufficient for robust multilingual capability, particularly in non-English domains"*
- Models with language-specific optimization (e.g., Qwen3) achieve substantially higher non-English accuracy

### Training Data
From paper: *"We train the models on a text-only dataset with trillions of tokens, with a focus on STEM, coding, and general knowledge."*
- **Mostly English** — no specific Arabic data percentage disclosed
- Model card warns: *"GPT-OSS may not perform as well in other languages or may prefer English responses"*
- Knowledge cutoff: June 2024

### No OALL / AMMLU / AraGen Scores Found
GPT-OSS-20B has not been evaluated on any of the Arabic-specific benchmarks used for our other models.

---

## 6. MoE Implications for Arabic Query Expansion

### Does It Behave Like 3.6B or 20B for Arabic?

**For English reasoning:** The full 20B expert pool is effectively leveraged — GPT-OSS-20B rivals o3-mini on AIME (92.1%).

**For Arabic text generation:** Likely behaves closer to a poorly-trained 3.6B model. Key evidence:

1. **Research finding (arXiv 2601.14050):** *"High-resource languages rely on shared experts while low-resource languages depend more on language-exclusive experts despite weaker performance."* If Arabic-exclusive experts received limited training data, they will underperform.

2. **Layerwise specialization:** Early and late MoE layers handle language-specific processing. If these layers' Arabic experts are weak, the language-agnostic middle layers cannot compensate.

3. **Empirical precedent:** GPT-OSS-20B scored 28% on C-Eval (Chinese) while Qwen3 scores much higher — demonstrating that English-dominant MoE models can dramatically underperform on non-English tasks vs. multilingual-focused models.

### Comparison with Other MoE Models' Multilingual Behavior

| MoE Model | Multilingual Approach | Non-English Performance |
|-----------|----------------------|------------------------|
| **GPT-OSS-20B** | English-dominant, no multilingual optimization | Weak (28% C-Eval, ~58% ILMAAM) |
| Mixtral-8x7B | More multilingual training data | Decent multilingual |
| DeepSeek-V3 | Bilingual EN+CN optimization | Strong Chinese, moderate Arabic |
| NLLB MoE (Meta) | 128 experts, language-specific routing | Strong for low-resource languages |

### Bottom Line
For our Arabic QE task, GPT-OSS-20B will likely behave as a **weakly-trained ~3.6B model for Arabic** despite its 20.9B total parameters. The question is: can OpenAI's strong general architecture and o200k tokenizer partially compensate for the lack of Arabic training data?

---

## 7. VRAM & Performance Estimates

### Memory Requirements

| Loading Path | Weights | Total (with overhead) | Fits T4? |
|-------------|---------|----------------------|----------|
| Unsloth BNB 4-bit | ~10-12 GB | ~14 GB | YES (tight) |
| Native MXFP4 | ~12.8 GB | ~16 GB | Borderline |
| GGUF Q4_K_M | 11.6 GB | N/A (CPU) | N/A |

### GPU Strategy

| GPU | Loading Path | Batch Size | Expected Runtime |
|-----|-------------|-----------|-----------------|
| **T4 (15 GB)** | Unsloth BNB 4-bit | 1-2 (tight) | ~2-4 hours |
| **A100 (40 GB)** | Unsloth BNB 4-bit | 4-8 | ~30-60 min |
| **A100 (40 GB)** | Native MXFP4 | 4-8 | ~30-60 min |

**Recommendation:** Use A100 with Unsloth BNB 4-bit loading. Start with batch_size=4, try 8 if VRAM allows. The MoE routing may add memory overhead compared to dense models of the same active size.

### Inference Speed Estimate
With only 3.6B active params per token, inference should be faster than Jais-2's 8B (all active). However, MoE routing overhead and the larger KV cache (64 Q heads) may partially offset this advantage. Expect **slower than Qwen3-4B, faster than full 8B models**.

---

## 8. Known Technical Issues

### 8.1 MXFP4 Compute Capability Check (HuggingFace)
- **Error:** `"MXFP4 quantized models is only supported on GPUs with compute capability >= 9.0"`
- **Trigger:** Loading `openai/gpt-oss-20b` directly on T4/A100
- **Fix:** Latest `transformers` from source + `kernels` + `triton>=3.4.0`
- **Bypass:** Use Unsloth's `load_in_4bit=True` (recommended)

### 8.2 Harmony Format Required
- **Model will not work correctly without harmony format**
- `tokenizer.apply_chat_template()` handles this automatically
- Cannot use raw text prompts or simple ChatML format

### 8.3 Bleeding-Edge Dependencies
- Requires `transformers >= 4.55.0` (dev version)
- Requires `torch >= 2.8.0`
- Requires `triton >= 3.4.0`
- Unsloth requires specific commit of triton_kernels

### 8.4 OOM Reports on Multi-GPU (Discussion #231)
- Some users report OOM during MXFP4 conversion on A100-40GB
- Not an issue with Unsloth's BNB 4-bit path

### 8.5 T4 Triton MXFP4 Bias Dtype Assertion (GitHub #3506)
- **Error:** `"Mismatched type for bias between then block (<['256'], fp16>) and else block (<['256'], fp32>)"`
- **Trigger:** GRPO training on T4, not pure inference
- **Fix:** Use official Unsloth Docker image or latest Unsloth

### 8.6 Reasoning Output Channels — Analysis Channel Leaks (CONFIRMED)
With `reasoning_effort="low"`, the model STILL generates in the `analysis` channel first (English CoT reasoning) before producing the `final` channel answer. This causes:
- Output is mostly English (12% Arabic on some queries)
- Wasted tokens on reasoning we don't need
- Massive slowdown (reasoning uses many tokens before actual answer)

**Fix discovered:** Force generation to start in the `final` channel by appending `<|start|>assistant<|channel|>final<|message|>` as the generation prefix instead of the default `<|start|>assistant`. This skips analysis entirely — output becomes 100% Arabic.

There is no `reasoning_effort="none"` or `"off"` option. The parameter only accepts `"low"`, `"medium"`, `"high"`.

### 8.7 Extreme Inference Slowness (CONFIRMED — BLOCKING)
**Measured: ~71 seconds per batch of 4 queries on A100-40GB.**
- Estimated full run: **~14 hours** for 2,896 queries
- Compare: Jais-2-8B = 12 min, Qwen3-4B = 12.4 min (both on same A100)
- **~70x slower** than our other models
- Root cause: MoE expert routing with BNB 4-bit quantization creates massive overhead. 32 experts with top-4 routing per token means significant memory transfer and computation per forward pass, despite only 3.6B active parameters.

---

## 9. Implementation Plan

### Loading (Unsloth — Recommended)
```python
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/gpt-oss-20b",
    dtype=None,  # auto-detect
    max_seq_length=1024,
    load_in_4bit=True,
    full_finetuning=False,
)
FastLanguageModel.for_inference(model)  # 2x speedup
```

### Generation
```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": query}
]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
    reasoning_effort="low"
).to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=128,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)
```

### Output Parsing
Need to handle harmony format output — extract the `final` channel content and strip any `analysis` reasoning tokens. The exact parsing depends on whether `reasoning_effort="low"` produces any analysis tokens at all.

### Recommended Sampling Parameters (from model card)
| Parameter | Value |
|-----------|-------|
| Temperature | 1.0 (model default) — test 0.7 for cross-model comparison |
| Top-P | 1.0 |
| Top-K | 0 (disabled) |
| Reasoning effort | "low" |

### Required Packages (from Unsloth notebook)
```bash
pip install "torch>=2.8.0" "triton>=3.4.0" torchvision bitsandbytes "transformers==4.56.2"
pip install "unsloth_zoo[base] @ git+https://github.com/unslothai/unsloth-zoo"
pip install "unsloth[base] @ git+https://github.com/unslothai/unsloth"
pip install git+https://github.com/triton-lang/triton.git@0add68262ab0a2e33b84524346cb27cbb2787356#subdirectory=python/triton_kernels
```

---

## 10. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Poor Arabic output (English-dominant training) | **HIGH** | Sanity check first 5 queries. If English/mixed output, try stronger Arabic system prompt. If still fails, document as finding. |
| MXFP4/dependency issues | **HIGH** | Use Unsloth BNB 4-bit path (avoids MXFP4 entirely) |
| Harmony format parsing | **MEDIUM** | `apply_chat_template()` handles format; extract `final` channel only |
| OOM on T4 | **MEDIUM** | Use A100. If OOM, reduce batch_size to 1. |
| Bleeding-edge transformers breaks | **MEDIUM** | Pin exact versions from Unsloth notebook |
| MoE batching issues | **MEDIUM** | Start batch_size=4, reduce to 1 if errors |
| Reasoning tokens in output | **LOW** | Set `reasoning_effort="low"`, strip analysis channel |

---

## 11. Experiment Results — DROPPED

**Date:** March 17, 2026
**Status:** Sanity check complete. Full run abandoned (estimated 14 hours on A100).

### Configuration

| Parameter | Value |
|-----------|-------|
| **GPU** | NVIDIA A100-SXM4-40GB |
| **Loading** | Unsloth BNB 4-bit (`unsloth/gpt-oss-20b`) |
| **VRAM used** | 21.2 GB / 42.4 GB total |
| **Batch size** | 4 |
| **Temperature** | 0.7 |
| **max_new_tokens** | 128 |
| **top_p** | 0.9 |
| **Reasoning** | Forced final channel (skips analysis) |

### Sanity Check Results (5 queries)

**With default `reasoning_effort="low"` (BEFORE fix):**
- Query 3 output was 12% Arabic, 88% English — analysis channel leaked through
- Output started with `analysisWe need to answer in Arabic...` — English CoT reasoning

**With forced final channel prefix (AFTER fix):**
All 5 queries produced 100% Arabic output. However:

| Query | Topic | Arabic % | Expansion | Factual Accuracy |
|-------|-------|----------|-----------|-----------------|
| 1 | Ali bin Muhammad al-Samari | 100% | 17.3x | Plausible but unverifiable |
| 2 | First submarine use | 100% | 12.6x | **WRONG** — confuses submarines with irrigation canals |
| 3 | Saint called "the Rock" | 100% | 12.5x | **WRONG** — says Paul (correct: Peter/بطرس) |
| 4 | Domestic violence & depression | 100% | 12.3x | Correct — relevant, well-structured |
| 5 | First Congo War | 100% | 3.8x | **WRONG** — says 1939-1945 (correct: 1996) |

**3 out of 5 queries had severe factual hallucinations.** Same pattern as ALLaM-7B (exp_008).

### Speed: Not Viable

| Metric | GPT-OSS-20B | Jais-2-8B | Qwen3-4B |
|--------|-------------|-----------|----------|
| **Batch speed** | 71.4 s/batch of 4 | ~3 s/batch of 16 | ~3 s/batch of 32 |
| **Queries/min** | ~2.5 | 241.5 | 232.6 |
| **Est. full run** | **~14 hours** | 12 min | 12.4 min |
| **Slowdown vs Jais** | **~70x** | — | — |

Root cause: MoE with 32 experts + BNB 4-bit on Unsloth creates massive per-token routing overhead. Despite only 3.6B active parameters, the expert selection, weight loading, and routing computation for each token across 32 experts is far more expensive than a dense 8B model.

### Verdict: DROP

GPT-OSS-20B is **not viable for Arabic query expansion** due to:
1. **Speed:** ~14 hours on A100 vs 12 minutes for Jais-2 (70x slower)
2. **Hallucinations:** 3/5 sanity check queries had severe factual errors
3. **Architecture overhead:** MoE routing with BNB 4-bit is catastrophically slow
4. **No Arabic training:** English-dominant data produces grammatically correct but factually unreliable Arabic

### Value for Thesis

Despite being dropped, this experiment provides several novel findings:

1. **MoE ≠ efficient for all tasks:** Despite only 3.6B active params (similar to Qwen3-4B), MoE routing makes GPT-OSS-20B ~70x slower. The "active parameter" count is misleading for practical inference speed.

2. **English-dominant MoE models hallucinate on Arabic:** The model produces fluent Arabic text but with wrong facts — worse than not generating at all. This is more dangerous than ALLaM's obvious tokenizer corruption, because the output *looks* correct.

3. **Forced-final-channel trick works:** Appending `<|start|>assistant<|channel|>final<|message|>` successfully bypasses reasoning. This is a useful technique for any GPT-OSS deployment where CoT is unwanted.

4. **Arabic-specialized training is essential for QE:** Jais-2 (Arabic-specialized, 8B dense) massively outperforms GPT-OSS (English-dominant, 20.9B MoE) in both speed and quality. Model size and architecture cannot compensate for lack of Arabic training data.

---

## 12. Lessons Applied from Previous Models

| Previous Lesson | Application to GPT-OSS-20B |
|-----------------|---------------------------|
| **Falcon-H1:** Hybrid architectures have batching bugs | GPT-OSS is standard Transformer MoE — batching should work, but test first |
| **Falcon-H1:** Model-specific temperature matters | Model card says temp=1.0; test both 1.0 and 0.7 for comparison |
| **Jais-2:** Must remove `token_type_ids` | Check if GPT-OSS tokenizer produces these |
| **Jais-2:** BF16 required (Squared-ReLU overflow) | GPT-OSS uses SwiGLU with clamping — FP16/BF16 should be fine |
| **ALLaM:** Sentencepiece `▁` leak destroyed retrieval | GPT-OSS uses BPE (tiktoken) — different tokenizer, but verify decoded output for artifacts |
| **ALLaM:** Preview models carry real risks | GPT-OSS is a stable release (not preview) — lower risk |
| **Qwen3:** Thinking mode must be disabled | GPT-OSS has `reasoning_effort` control — set to "low" |
| **Qwen3:** Never use greedy decoding | Use `do_sample=True`, temp >= 0.7 |
| **All:** Always sanity-check first 5 queries | Critical here — Arabic quality is the biggest unknown |
| **All:** pyserini is hidden dependency | Include in install cell |

---

## 13. Citations

### GPT-OSS Paper
> OpenAI (2025). "GPT-OSS." arXiv:2508.10925. August 5, 2025.

### OpenAI Announcement
> "Introducing GPT-OSS." OpenAI Blog, August 5, 2025. https://openai.com/index/introducing-gpt-oss/

### Model Card
> https://openai.com/index/gpt-oss-model-card/
> https://huggingface.co/openai/gpt-oss-20b

### MXFP4 Format
> Open Compute Project (OCP) Microscaling Formats Specification, 2024.

### MoE Multilingual Research
> arXiv:2601.14050 — "Understanding Multilingualism in MoE LLMs" (2026)

### Independent Evaluation
> arXiv:2508.12461 — "Is GPT-OSS Good?" (2025)
> HuggingFace Blog — "GPT-OSS evaluation on ILMAAM Arabic benchmarks"

### Unsloth
> https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune
> https://unsloth.ai/blog/gpt-oss
> https://huggingface.co/unsloth/gpt-oss-20b
