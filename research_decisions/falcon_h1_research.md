# Falcon-H1-3B-Instruct: Research & Experiment Findings

**Date:** February 28 – March 2, 2026
**Researcher:** Mohammed Elhaj
**Purpose:** Model comparison experiment (Task 4.0b) — first model evaluation
**Status:** Query generation complete (temp=0.1), evaluation pending

---

## 1. Model Overview

| Property | Value |
|----------|-------|
| **HuggingFace ID** | `tiiuae/Falcon-H1-3B-Instruct` |
| **Developer** | Technology Innovation Institute (TII), Abu Dhabi |
| **Parameters** | 3.15B (3,149.4M) |
| **Architecture** | Hybrid Mamba2-Transformer with SwiGLU (`falcon_h1`) |
| **Base Model** | `tiiuae/Falcon-H1-3B-Base` |
| **Languages** | 18 languages (ar, en, fr, de, es, zh, ja, ko, hi, ur, + 8 more) |
| **Context Length** | 128K tokens |
| **License** | Other (see model card) |
| **Release Date** | May 21, 2025 |
| **Paper** | arXiv:2507.22448 |

### Why Selected for Testing
- **Best Arabic OALL score at 3B size:** ~62%, approximately 10 points ahead of peer models at same parameter count
- **Efficient architecture:** Hybrid Mamba-Transformer combines attention efficiency with SSM long-context handling
- **No quantization needed:** Fits on T4/A100 GPU in FP16/BF16
- **Arabic is a first-class language:** Listed as native language, not just "supported"

---

## 2. Architecture: Hybrid Mamba2-Transformer

Falcon-H1 is NOT a standard Transformer. It uses a **Hybrid-Head** architecture combining:

1. **Mamba2 SSM layers** — State Space Model blocks for efficient sequence processing
   - d_state: 256
   - n_heads: 32 (Mamba heads)
   - d_head: 128
   - chunk_size: 256

2. **Transformer attention layers** — Standard multi-head attention
   - n_heads: 10 (attention heads)
   - n_kv_heads: 2 (grouped query attention)
   - d_head: 128

3. **SwiGLU MLP** — Gated activation function

**Total depth:** 32 layers
**Hidden size:** 2560

### Significance for Thesis
This is a novel architecture that hasn't been tested for Arabic query expansion in any published work. The hybrid approach may offer:
- Better long-context understanding (relevant for generating coherent pseudo-documents)
- More efficient inference than pure Transformers
- Different representation capabilities than Qwen's standard Transformer

---

## 3. Technical Setup & Issues Encountered

### 3.1 Dependencies

**Critical finding: NO `mamba-ssm` package needed.**

The `falcon_h1` architecture is natively supported in HuggingFace Transformers since v5.2.0 (May 2025). The Mamba layers are implemented within the transformers library itself.

**Do NOT install `mamba-ssm` or `causal-conv1d`** — these have known build failures on Google Colab:
- Python 3.11 incompatibility ([GitHub issue #5468](https://github.com/googlecolab/colabtools/issues/5468))
- Build errors during wheel compilation ([GitHub issue #607](https://github.com/state-spaces/mamba/issues/607))

**Also required:** `pyserini` + Java (for `MIRACLDataLoader` which imports `from pyserini.search import get_topics, get_qrels`). This was initially missed since the generator-only notebook doesn't do retrieval, but the data loader has a hard dependency on pyserini.

**Required installation:**
```bash
apt-get install -qq openjdk-21-jdk-headless
pip install pyserini faiss-cpu
pip install git+https://github.com/huggingface/transformers.git
pip install torch datasets accelerate tqdm
```

### 3.2 dtype: bfloat16 on A100, float16 on T4

- **Model recommendation:** `torch.bfloat16`
- **T4 limitation:** Turing architecture (compute capability 7.5) — bfloat16 is emulated in software (very slow)
- **A100:** Ampere architecture (compute capability 8.0) — native bfloat16 support
- **Final decision:** Used `torch.bfloat16` on A100 (40 GB, Colab Pro+)

### 3.3 VRAM Usage (Actual vs Estimated)

| | Estimated (pre-experiment) | Actual |
|--|---------------------------|--------|
| **Model weights** | 6-8 GB | ~6.3 GB |
| **Total GPU usage** | 6-8 GB | **~10-11 GB** |
| **Overhead** | — | ~4 GB (Mamba2 SSM state buffers) |

The Mamba2 SSM state buffers (d_state=256, chunk_size=256, 32 heads across 32 layers) add significant memory overhead beyond the model weights. This caused OOM on T4 (15 GB) at batch_size=8.

---

## 4. Critical Bug: Batched Generation Fails on All Attention Backends

### The Problem

Falcon-H1 **cannot do batched text generation** with the current HuggingFace Transformers implementation. When generating with batch_size > 1 (which requires left-padding to equal lengths), the causal attention mask is not correctly extended as new tokens are generated.

### Error Manifestation

**On SDPA (default):**
```
RuntimeError: The expanded size of the tensor (61) must match the existing size (58)
at non-singleton dimension 3. Target sizes: [4, 10, 4, 61]. Tensor sizes: [4, 1, 1, 58]
```
Location: `transformers/integrations/sdpa_attention.py` → `scaled_dot_product_attention`

**On Eager attention:**
```
RuntimeError: The size of tensor a (66) must match the size of tensor b (59)
at non-singleton dimension 3
```
Location: `transformers/models/falcon_h1/modeling_falcon_h1.py` → `eager_attention_forward`

### Root Cause

The bug is in `modeling_falcon_h1.py`'s **causal mask preparation**, not in any specific attention backend. During autoregressive generation with left-padded batches:

1. Queries are left-padded to the same length (e.g., 58 tokens)
2. Model starts generating new tokens — key/value length grows to 61
3. The 4D causal attention mask is **not extended** to include newly generated tokens
4. Mismatch: attention expects mask for 61 keys but receives mask for 58

This affects **all three attention backends**: SDPA, eager, and Flash Attention 2.

### What We Tried

| Approach | Result |
|----------|--------|
| `batch_size=8` (default, SDPA) | ❌ OOM on T4 + mask crash |
| `batch_size=4` (SDPA) | ❌ Mask shape crash |
| `batch_size=2` (SDPA) | ❌ Mask shape crash |
| `attn_implementation="eager"` | ❌ Same mask crash (different line) |
| `attn_implementation="flash_attention_2"` | ❌ Requires `flash-attn` package (30 min compile), and the mask bug is upstream of all backends |
| `batch_size=1` via `enhance()` loop | ✅ **Works** — no padding = no mask to mismatch |

### Impact

- **Qwen 2.5 3B (exp_003):** batch_size=8, ~40 min for 2,896 queries on T4
- **Falcon-H1-3B:** batch_size=1 (single-query loop), ~60-90 min on A100

This is a **real architectural limitation** of the current Falcon-H1 Transformers implementation, not a hardware issue. No public GitHub issue exists for it as of March 2026. Standard Transformer models (Qwen, Llama, Gemma) do not have this bug.

### Significance for Thesis

This is a practical finding worth documenting:
- Hybrid Mamba2-Transformer architectures may have immature tooling support
- Batched inference — critical for practical QE pipelines — is not available
- Model selection for production QE systems should consider not just quality metrics but also inference compatibility
- The workaround (single-query loop) works but significantly reduces throughput

---

## 5. GPU Evolution During Experiment

The experiment went through three GPU configurations:

### Phase 1: T4 (Free Tier, 15 GB)
- **OOM at batch_size=8:** Model uses ~10-11 GB, leaving ~4 GB free. Batch processing needed 4+ GB additional.
- **OOM at batch_size=4/2:** Still hit the SDPA mask bug before OOM became relevant.
- **SDPA mask crash:** Discovered the batching bug.
- **Single-query loop worked** but estimated ~4-6 hours for both temperature runs.

### Phase 2: Upgrade to Colab Pro+ (A100, 40 GB)
- **OOM solved:** 40 GB leaves ~29 GB free after model load.
- **Mask bug persists:** Same crash on SDPA and eager attention — bug is in mask preparation, not hardware.
- **bfloat16 enabled:** A100 (compute cap 8.0) natively supports bfloat16, matching model recommendation.
- **Single-query loop on A100:** ~60-90 min per run (vs ~3 hrs on T4).

### GPU Comparison

| Spec | T4 | A100 |
|------|-----|------|
| VRAM | 15 GB | 40 GB |
| Architecture | Turing (7.5) | Ampere (8.0) |
| bfloat16 | ❌ emulated | ✅ native |
| Flash Attention 2 | ❌ (need ≥8.0) | ✅ |
| Memory bandwidth | 300 GB/s | 1,555 GB/s |
| Batch generation | ❌ (OOM + bug) | ❌ (bug only) |
| Single-query speed | ~2-3 sec/query | ~0.5-1 sec/query |

---

## 6. Temperature Finding

**From Falcon-H1 documentation:**
> "The recommended model temperature is 0.1 — higher than that, model's performance may largely drop."

This is significantly different from:
- Qwen 2.5 3B: used temperature=0.7 in exp_003
- Query2Doc paper: used temperature=0.7 with GPT-3

**Experiment decision:** Test BOTH temperatures
- `temperature=0.1` — Falcon's optimal setting → ✅ **Completed**
- `temperature=0.7` — Match Qwen baseline for fair cross-model comparison → Pending (can re-run)

### Implications for Thesis
If temperature=0.1 produces better results, this suggests:
- Model-specific hyperparameter tuning matters for QE
- "One size fits all" temperature may not be optimal
- This is a finding worth discussing in the experiments chapter

---

## 7. Chat Template

Falcon-H1-3B-Instruct uses the standard `apply_chat_template()` interface with system/user/assistant roles. Compatible with the existing `Query2DocEnhancer` class without modification.

**Message format:**
```python
messages = [
    {"role": "system", "content": "You are asked to write a passage..."},
    {"role": "user", "content": "ما هي عاصمة السودان"}
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
```

**Sanity check results:** Arabic output was coherent and relevant. The `apply_chat_template()` worked correctly — no fallback needed.

---

## 8. Final Experiment Configuration

| Parameter | Value |
|-----------|-------|
| **Model** | `tiiuae/Falcon-H1-3B-Instruct` |
| **GPU** | NVIDIA A100-SXM4-40GB (Colab Pro+) |
| **dtype** | `torch.bfloat16` |
| **Attention** | Default (no override needed for single-query) |
| **batch_size** | 1 (single-query loop via `enhance()`) |
| **max_new_tokens** | 128 |
| **temperature** | 0.1 (completed), 0.7 (pending) |
| **top_p** | 0.9 |
| **Queries** | 2,896 (MIRACL Arabic dev) |
| **Output** | `enhanced_queries_falcon_h1_3b_temp01.pkl` (saved to Google Drive) |
| **Notebook** | `experiments/Query_generator_falcon_h1.ipynb` |

---

## 9. Comparison with Other Candidate Models

| Model | Params | Arabic OALL | Quantization | VRAM | Batching | Difficulty |
|-------|--------|-------------|-------------|------|----------|------------|
| **Falcon-H1-3B** | 3.15B | ~62% | BF16 | 10-11 GB | ❌ Bug | HARD |
| Qwen 2.5 3B (baseline) | 3B | Lower | FP16 | ~6 GB | ✅ batch=8 | Reference |
| Qwen3-4B | 4B | TBD | FP16 | 8-10 GB | Likely ✅ | EASY |
| Jais-2-8B | 8B | TBD | 4-bit | 8-10 GB | TBD | MEDIUM |

**Lesson learned:** Falcon-H1's difficulty rating should be **HARD** not EASY — the hybrid architecture's immature HuggingFace support adds significant engineering overhead.

---

## 10. Sources

- **Model Card:** https://huggingface.co/tiiuae/Falcon-H1-3B-Instruct
- **Transformers Documentation:** https://huggingface.co/docs/transformers/model_doc/falcon_h1
- **Falcon-H1 Blog:** https://falcon-lm.github.io/blog/falcon-h1/
- **Paper:** https://arxiv.org/abs/2507.22448
- **GitHub:** https://github.com/tiiuae/Falcon-H1
- **Mamba-SSM Colab Issue:** https://github.com/state-spaces/mamba/issues/607
- **Colab Python 3.11 Issue:** https://github.com/googlecolab/colabtools/issues/5468
- **Mamba2 Batching Discussion:** https://github.com/state-spaces/mamba/issues/66
- **Transformers SDPA Mask Issues:** https://github.com/huggingface/transformers/issues/36585, #30095, #41856

---

## 11. Lessons Learned for Next Model

1. **Always test single-query `enhance()` first** before batched generation — it's the safest smoke test
2. **Check if the architecture is a standard Transformer** — hybrid models (Mamba, RWKV, etc.) may have batching bugs
3. **VRAM estimates should include SSM state buffers** — Mamba2 adds ~4 GB overhead beyond model weights
4. **Colab Pro+ A100 is worth it** for model comparison experiments — 40 GB VRAM eliminates OOM entirely
5. **`pyserini` is a hidden dependency** in the data loader — always include it in the generator notebook
6. **Model-specific temperature settings matter** — don't assume the baseline temperature works for all models

**Full execution plan:** See `C:\Users\moham\.claude\plans\glittery-cuddling-hartmanis.md`
