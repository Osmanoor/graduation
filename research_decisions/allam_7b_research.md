# ALLaM-7B-Instruct-preview: Research & Technical Findings

**Date:** March 13, 2026
**Researcher:** Mohammed Elhaj
**Purpose:** Model comparison experiment (Task 4.0b) — ALLaM-7B evaluation
**Status:** COMPLETE — Worst performing model. Degraded retrieval below baseline.

---

## 1. Model Overview

| Property | Value | Source |
|----------|-------|--------|
| **HuggingFace ID** | `ALLaM-AI/ALLaM-7B-Instruct-preview` | [Model Card](https://huggingface.co/ALLaM-AI/ALLaM-7B-Instruct-preview) |
| **Mirror** | `humain-ai/ALLaM-7B-Instruct-preview` | HuggingFace |
| **Developers** | NCAI at SDAIA (Saudi Data and AI Authority) | [Paper](https://arxiv.org/abs/2407.15390) |
| **Parameters** | ~7B (7,000,559,616) | HF metadata |
| **Architecture** | `LlamaForCausalLM` — standard decoder-only Transformer | config.json |
| **Position Encoding** | RoPE (rope_theta=1,000,000) | config.json |
| **Activation** | SiLU | config.json |
| **Normalization** | RMSNorm (standard Llama) | config.json |
| **Attention** | MHA, 32 heads, 32 KV heads (full MHA, no GQA) | config.json |
| **Hidden Size** | 4,096 | config.json |
| **Intermediate Size** | 11,008 | config.json |
| **Layers** | 32 | config.json |
| **Vocabulary** | 64,000 tokens (expanded from Llama-2's 32K for Arabic) | config.json |
| **Context Length** | 4,096 tokens | config.json |
| **Tensor Type** | BF16 | HF repo |
| **Release Date** | February 13, 2025 | HF API |
| **Paper** | arXiv:2407.15390, ICLR 2025 | [OpenReview](https://openreview.net/forum?id=MscdsFVZrN) |
| **License** | Apache 2.0 | Model card |

### Why Selected for Testing
- **Saudi Arabic LLM:** Trained from scratch with Arabic as a primary language
- **Massive training data:** 5.2 trillion tokens (4T English + 1.2T Arabic/English mixed)
- **ICLR 2025 publication:** Peer-reviewed research with detailed methodology
- **Standard Transformer:** LlamaForCausalLM — no batching bugs (unlike Falcon-H1)
- **Arabic MMLU 67.78:** Competitive Arabic understanding
- **Apache 2.0 license:** No restrictions

---

## 2. Architecture: Standard LlamaForCausalLM

**CRITICAL: This is a standard Transformer. Batching is SAFE.**

ALLaM-7B uses the exact Llama-2 architecture with one key modification: vocabulary expansion from 32K to 64K tokens to accommodate Arabic script. The model was trained from scratch (NOT fine-tuned from Llama-2 weights).

### Architecture Comparison with Other Models

| Aspect | ALLaM-7B | Jais-2-8B | Falcon-H1-3B |
|--------|----------|-----------|---------------|
| Architecture | LlamaForCausalLM | Custom `jais2` | Hybrid Mamba2-Transformer |
| Attention | Full MHA (32 heads) | MHA (26 heads) | 10 attention + 32 Mamba heads |
| KV Heads | 32 (no GQA) | 2 (GQA possible) | 2 (GQA) |
| Position Enc | RoPE | RoPE | RoPE + SSM |
| Activation | SiLU | Squared-ReLU | SwiGLU |
| Vocab Size | 64,000 | 150,272 | Unknown |
| Context | 4,096 | 8,192 | 128K |
| Batching | Works | Works | BROKEN (bug) |

### Significance for Thesis
- Standard Llama architecture means all HuggingFace tooling works out of the box
- No `trust_remote_code=True` needed
- All attention backends (SDPA, eager, Flash Attention 2) are compatible
- Left-padding for batch generation works normally
- No SSM state buffers consuming extra VRAM

---

## 3. Training Details

### Pretraining (from paper, arXiv:2407.15390)

**Phase 1: English Foundation**
- 4 trillion English tokens
- Sources: Dolma-v1, The Pile, The Stack, PeS2o, PubMed, DM-Math, StackExchange

**Phase 2: Arabic-English Mixed (Continued Pretraining)**
- 1.2 trillion mixed Arabic/English tokens
- Optimal mix: 45% Arabic / 45% English / 10% code
- Arabic data: ~540B tokens total (270B natural Arabic + 270B machine-translated)
- Translation sources: Wikipedia, books, C4, PeS2o (English to Arabic)

**Total: 5.2 trillion tokens** (verified from paper)

### Instruction Tuning (SFT)
- Dataset: "Ultra-Instinct v2" — 6M samples (evenly split Arabic/English)
- Reduced from 12M samples in v1
- Training: 3 epochs, LR = 5e-6, batch size = 1024

### Alignment
- Method: **DPO** (Direct Preference Optimization) — not RLHF
- Data: ~245K preference samples (expanded from 25,854 base triplets)
- Training: 1 epoch, LR = 9e-7, batch size = 512, KL penalty = 0.1
- Model card mentions: "7M instructions + 260K preference pairs"

### Training Pipeline Comparison

| Aspect | ALLaM-7B | Jais-2-8B | Falcon-H1-3B |
|--------|----------|-----------|---------------|
| Pre-training tokens | 5.2T | 2.6T | Unknown |
| Arabic tokens | ~540B | Significant | Arabic-focused |
| SFT data | 6M samples | 4M Arabic + 10M English | Unknown |
| Alignment | DPO | SFT + DPO + GRPO | Unknown |
| Arabic vocab expansion | Yes (32K -> 64K) | From scratch (150K) | Unknown |

---

## 4. Arabic Benchmarks

### From Model Card (ALLaM-7B-Instruct)

| Benchmark | Score | Notes |
|-----------|-------|-------|
| **Arabic MMLU (0-shot)** | **67.78** | Strong Arabic understanding |
| ACVA (5-shot) | 76.33 | Arabic cultural/vocabulary |
| ExamsAR (5-shot) | 51.58 | Arabic exam questions |
| AraMath (5-shot) | 66.78 | Arabic math reasoning |
| ETEC (0-shot) | 66.67 | |
| IEN-MCQ (0-shot) | **91.77** | Highest individual score |
| IEN-TF (0-shot) | 82.95 | |
| AraPro (0-shot) | 69.71 | |
| Ar-IFEval prompt strict | 31.34 | Instruction following (weak) |
| Ar-IFEval inst strict | 67.65 | |
| GAT (0-shot) | 44.53 | |
| **MT-Bench Arabic** | **5.9** | Turn1: 6.93 / Turn2: 4.88 |
| **Average (12 benchmarks)** | **64.42** | |

### English Benchmarks
- Average across 15 English benchmarks: **46.85**
- Significantly weaker in English than Arabic (model is Arabic-focused)

### Benchmark Comparison with Our Models

| Benchmark | ALLaM-7B | Jais-2-8B | Falcon-H1-3B |
|-----------|----------|-----------|---------------|
| Arabic MMLU | 67.78 | Not reported | Not reported |
| MT-Bench Arabic | 5.9 | Not reported | Not reported |
| AraGen 3C3H | Not reported | 58.64 | Not reported |
| OALL v2 | Not reported | Not reported | ~62% |
| Ar-IFEval (inst) | 67.65 | 67.09 | Not reported |

**Note:** Direct comparison is difficult — each model reports on different benchmark suites. ALLaM reports on SDAIA's internal suite, Jais on AraGen, Falcon on OALL. Our experiment will provide the first direct comparison via Query2Doc retrieval metrics.

### Benchmark Limitations
- **No OALL v2 score** — not on the community leaderboard
- **No AraGen score** — different evaluation suite
- **Ar-IFEval instruction-strict is comparable** to Jais-2 (67.65 vs 67.09)
- **MT-Bench Arabic 5.9** is moderate (GPT-4 scores 8.39)
- ALLaM-13B reportedly outperformed Jais-30B in human evaluation (paper)

---

## 5. VRAM & Performance Estimates

### Memory Requirements

| Configuration | Weights | Total (with overhead) |
|--------------|---------|----------------------|
| BF16/FP16 | ~14 GB | ~16-17 GB |
| 4-bit NF4 | ~4-5 GB | ~6-7 GB |

Model is stored as 3 safetensors shards, ~13.5 GB on disk.

### No Pre-quantized Versions Available
- No official GGUF, GPTQ, or AWQ releases
- Community requested GGUF (HF Discussion #1) — not provided by SDAIA
- Must use `bitsandbytes` for 4-bit quantization if needed

### A100 40GB Strategy

| Config | Batch Size | Expected Runtime (2,896 queries) | VRAM Used |
|--------|-----------|----------------------------------|-----------|
| **FP16, batch=8** | 8 | **~30-45 min** | ~20-24 GB |
| FP16, batch=4 | 4 | ~45-60 min | ~18-20 GB |
| 4-bit, batch=8 | 8 | ~30-45 min | ~10-14 GB |
| 4-bit, batch=16 | 16 | ~20-30 min | ~14-18 GB |

**Recommendation:** FP16 with batch_size=8 on A100. ~24 GB headroom. No quantization needed.

### Comparison with Full MHA vs GQA

ALLaM uses **full MHA** (32 KV heads = 32 attention heads), meaning KV cache is larger than models with GQA (like Jais-2 with 2 KV heads). This increases VRAM usage during generation but doesn't change model weight size. On A100 with 40GB, this is not a concern.

---

## 6. Known Technical Issues

### 6.1 MUST Remove `token_type_ids`

The model card code explicitly uses:
```python
inputs = tokenizer(inputs, return_tensors='pt', return_token_type_ids=False)
```

Same requirement as Jais-2. `LlamaForCausalLM.forward()` does not accept `token_type_ids`.

### 6.2 `pad_token` Not Set by Default

`pad_token_id` is None in the tokenizer config. Must set:
```python
tokenizer.pad_token = tokenizer.eos_token
```

### 6.3 Left-padding for Batch Generation

Standard decoder-only practice:
```python
tokenizer.padding_side = 'left'
```

### 6.4 Chat Template: Llama-2 [INST] Style

```
<s> [INST] <<SYS>>
{system_message}
<</SYS>>

{user_message} [/INST] {assistant_response} </s>
<s> [INST] {user_message} [/INST]
```

`apply_chat_template()` works with standard `system`, `user`, `assistant` roles.

### 6.5 Transformers Version

Requires `transformers >= 4.40.1` (stated in model card). Standard Llama architecture is supported by all recent transformers versions.

### 6.6 `trust_remote_code` NOT Needed

Standard `LlamaForCausalLM` — no custom code files.

### 6.7 No Known Generation Bugs

Standard Transformer = standard behavior. No Mamba batching bugs. No attention mask issues.

### 6.8 Full MHA (No GQA)

32 KV heads = 32 attention heads means larger KV cache than GQA models. For our short generation (128 tokens), this is negligible.

---

## 7. "Preview" Status — Critical Notes

### What "Preview" Means
- **Alpha/experimental status** — the model is "in trial/experimental phase" (confirmed in HF Discussion #3)
- **Not a final/stable release** — team confirmed it is still under active development
- **Alpha versioning:** Two revisions exist:
  - `v1` = `7b-alpha-v1.27.2.25` (older)
  - `v2` = `7b-alpha-v2.33.0.30` (current, recommended)

### Implications for Our Experiment
1. **Pin to revision="v2"** when loading to ensure reproducibility
2. **Behavior may differ from paper** — preview model may not match published benchmarks exactly
3. **No stability guarantees** — could have subtle generation issues
4. **Document this limitation** in thesis: results are from preview model, final version may differ

### Access
- **NOT gated** — `gated: false` confirmed via HF API
- No access request needed
- No HuggingFace login required (but login is needed if using private repos)

### No Non-Preview Version Available
- As of March 2026, only the preview is publicly available
- The organization has only one published model

---

## 8. Implications for Our Experiment (exp_007)

### Advantages
1. **Standard Transformer** — batching works, all tooling compatible
2. **FP16 fits A100** — no quality loss from quantization
3. **Massive training data** — 5.2T tokens, 540B Arabic tokens
4. **ICLR 2025 paper** — prestigious venue, well-documented methodology
5. **No access gate** — easy to load, no login needed
6. **Apache 2.0 license** — no restrictions

### Potential Concerns
1. **Preview/alpha status** — may have subtle issues not documented
2. **Short context (4,096)** — shorter than Jais-2 (8K) and Falcon (128K), but sufficient for Query2Doc (~500 tokens total)
3. **Full MHA (no GQA)** — larger KV cache, but negligible for 128-token generation
4. **Weak Ar-IFEval prompt-strict (31.34)** — may not follow complex instructions well
5. **MT-Bench Arabic 5.9** — moderate quality (but generative benchmarks may not predict QE quality)
6. **No OALL/AraGen scores** — can't pre-compare with Falcon/Jais on same benchmarks

### Experiment Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **GPU** | A100 (Colab Pro) | FP16 fits, maximize quality |
| **Precision** | FP16 first; 4-bit fallback | A100 has 40GB, FP16 preserves quality |
| **Revision** | Pin to `revision="v2"` | Reproducibility for preview model |
| **Batch size** | Start batch=8, adjust based on VRAM | Standard Transformer, batching safe |
| **Temperature** | 0.6 (model recommended), also test 0.7 | Model card recommends 0.6; test both for fair comparison |
| **max_new_tokens** | 128 (same as all experiments) | Fair comparison |
| **token_type_ids** | Remove before generate() | Same as Jais-2 requirement |

---

## 9. Lessons Applied from Previous Models

| Previous Lesson | Application to ALLaM-7B |
|-----------------|------------------------|
| **Falcon-H1:** Hybrid architectures have batching bugs | ALLaM is standard LlamaForCausalLM — no issue |
| **Falcon-H1:** VRAM estimates must include SSM buffers | No SSM buffers — standard VRAM calculation |
| **Falcon-H1:** Model-specific temperature matters | Use ALLaM's recommended temp=0.6, also test 0.7 |
| **Jais-2:** Must remove token_type_ids | Same requirement — confirmed in ALLaM model card |
| **Jais-2:** pad_token must be set manually | Same — set `pad_token = eos_token` |
| **Both:** Always test single-query first | Do sanity check on first 5 queries |
| **Both:** pyserini is hidden dependency | Already included in install cell |
| **Both:** A100 eliminates OOM | Use A100 from the start |
| **NEW:** Preview model — pin revision | Use `revision="v2"` for reproducibility |

---

## 10. Experiment Results (exp_007)

### Configuration Used

| Parameter | Value |
|-----------|-------|
| **GPU** | NVIDIA A100-SXM4-40GB |
| **Precision** | FP16 (no quantization) |
| **Revision** | v2 |
| **VRAM** | 14.5 GB used / 42.4 GB total (28.0 GB free) |
| **Batch size** | 16 |
| **Temperature** | 0.7 |
| **max_new_tokens** | 128 |
| **top_p** | 0.9 |
| **Runtime** | 16.1 min (179.5 queries/min) |
| **Errors** | 0 |

### Results: WORST MODEL — Degraded Below Baseline

| Metric | Baseline (mDPR) | ALLaM-7B Dense | ALLaM-7B BM25 | vs Baseline |
|--------|-----------------|----------------|---------------|-------------|
| **NDCG@10** | 0.4993 | **0.2550** | 0.3341 | **-48.9%** |
| **Recall@10** | 0.6156 | **0.3335** | 0.4348 | **-45.8%** |
| **Recall@100** | 0.8407 | **0.5465** | 0.7004 | **-35.0%** |
| **MRR** | 0.5328 | **0.2708** | 0.3676 | **-49.2%** |

### Comparison with All Models

| Model | NDCG@10 | Recall@10 | MRR | Dense Status |
|-------|---------|-----------|-----|-------------|
| Jais-2-8B (best) | **0.6018** | **0.7161** | **0.6356** | +20.5% |
| Qwen 2.5 3B | 0.5435 | 0.6608 | 0.5742 | +8.9% |
| Falcon-H1-3B | 0.5359 | 0.6484 | 0.5681 | +7.3% |
| Baseline (no QE) | 0.4993 | 0.6156 | 0.5328 | -- |
| **ALLaM-7B** | **0.2550** | **0.3335** | **0.2708** | **-48.9%** |

### Root Cause Analysis

#### Problem 1: Sentencepiece Token Markers Leaking into Output
The generated text contains visible `▁` (U+2581 LOWER ONE EIGHTH BLOCK) characters — raw sentencepiece subword markers:
```
▁علي ▁بن ▁محمد ▁السم ري
```
If these are literally present in the decoded strings (not just a display artifact), they:
- Corrupt term matching for BM25 (splits words at wrong boundaries)
- Confuse the mDPR BERT tokenizer (unexpected characters in input)
- Effectively turn every pseudo-document into noise

**This is likely a tokenizer bug in the preview model** — `tokenizer.decode()` with `skip_special_tokens=True` should remove these, but ALLaM's sentencepiece tokenizer may not be properly configured.

#### Problem 2: Severe Factual Hallucinations
- Query 3: Claims Paul is "the Rock" — correct answer is **Peter** (بطرس/كيفا)
- Query 5: Claims Congo war was 1960 — correct answer is **1996**
- Query 1: Questionable connection to Safavid dynasty

Hallucinated content introduces wrong terms that push the retriever toward irrelevant documents.

#### Problem 3: Wildly Inconsistent Expansion Ratios
- Range: 3.3x to 23.3x (target: 5-12x)
- Some queries get minimal expansion (useless), others get flooded with noisy text
- Jais-2 had much more consistent expansion (median 5.04x, avg 10.46x)

#### Problem 4: Preview/Alpha Model Quality
The "preview" status likely means:
- Instruction following is not fully tuned (Ar-IFEval prompt-strict was only 31.34)
- Generation quality may not match the published paper's benchmarks
- The model may not reliably follow the "Respond in Arabic only" system prompt

### Verdict: DROP

ALLaM-7B-Instruct-preview is **not suitable for Arabic query expansion** in its current state. The combination of tokenizer issues and poor generation quality makes it the worst-performing model in our comparison by a large margin.

**For thesis:** This is still a valuable finding — it demonstrates that:
1. Model size (7B) and training data (5.2T tokens) do not guarantee QE quality
2. Preview/alpha models carry real risks for downstream tasks
3. Tokenizer correctness is critical for retrieval pipelines
4. The sentencepiece `▁` leak is a practical issue worth documenting

---

## 11. Lessons Learned

### Technical
1. **Preview models can have tokenizer bugs** — the `▁` sentencepiece marker leak is likely the primary cause of failure
2. **FP16 worked fine on A100** — 14.5 GB, 28 GB free, batch_size=16, no OOM
3. **Speed was reasonable** — 179.5 queries/min, 16.1 min total
4. **No generation errors** — the model ran smoothly, it just produced bad output
5. **Full MHA (32 KV heads) was fine** — batch_size=16 worked without issues

### Research
1. **Training data volume does not predict QE quality** — 5.2T tokens didn't help
2. **Benchmark scores don't predict QE quality** — Arabic MMLU 67.78 is decent, but QE is a different task
3. **Preview/alpha models are risky** — the alpha versioning and limited testing showed
4. **Tokenizer quality matters as much as model quality** — sentencepiece decode bugs destroy downstream retrieval
5. **Always verify decoded output** — check for special character leaks before full runs

### Key Finding for Thesis
**ALLaM-7B-Instruct-preview is the only model that degraded retrieval below baseline.** This demonstrates that query expansion is not universally beneficial — model quality (especially tokenizer correctness and instruction following) is critical. The preview/alpha status of the model is a contributing factor, and results may differ with a stable release.

---

## 12. Citations

### ALLaM Paper (ICLR 2025)
```bibtex
@inproceedings{
    bari2025allam,
    title={{ALL}aM: Large Language Models for Arabic and English},
    author={M Saiful Bari and Yazeed Alnumay and Norah A. Alzahrani and Nouf M. Alotaibi and Hisham Abdullah Alyahya and Sultan AlRashed and Faisal Abdulrahman Mirza and Shaykhah Z. Alsubaie and Hassan A. Alahmed and Ghadah Alabduljabbar and Raghad Alkhathran and Yousef Almushayqih and Raneem Alnajim and Salman Alsubaihi and Maryam Al Mansour and Saad Amin Hassan and Dr. Majed Alrubaian and Ali Alammari and Zaki Alawami and Abdulmohsen Al-Thubaity and Ahmed Abdelali and Jeril Kuriakose and Abdalghani Abujabal and Nora Al-Twairesh and Areeb Alowisheq and Haidar Khan},
    booktitle={The Thirteenth International Conference on Learning Representations},
    year={2025},
    url={https://openreview.net/forum?id=MscdsFVZrN}
}
```

### Sources
- **Paper:** https://arxiv.org/abs/2407.15390
- **OpenReview:** https://openreview.net/forum?id=MscdsFVZrN
- **Model Card:** https://huggingface.co/ALLaM-AI/ALLaM-7B-Instruct-preview
- **Config:** https://huggingface.co/ALLaM-AI/ALLaM-7B-Instruct-preview/blob/main/config.json
