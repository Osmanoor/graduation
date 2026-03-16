# Model Comparison Guide: Query2Doc with Multiple LLMs
**Created:** 11/2/2026
**Status:** Active
**Owners:** Mohammed & Osman
**Deadline:** 15/2/2026

---

## Goal

Replicate Osman's exp_003 (Query2Doc + Qwen 2.5 3B) with **10 additional open-source models**, compare results, and identify the best LLM for Arabic query expansion.

**Reference Baseline (exp_003):**
| Metric | Qwen 2.5 3B |
|--------|-------------|
| Recall@10 | 0.6608 |
| Recall@100 | 0.8594 |
| NDCG@10 | 0.5435 |
| MRR | 0.5742 |
| Runtime | ~40 min |

All new experiments must beat or match these numbers to be considered.

---

## Architecture (Already Built)

The codebase has clean separation of concerns. You only need to **swap the model** — everything else stays the same.

```
src/enhancers/
├── base.py           # QueryEnhancer base class
├── query2doc.py      # Query2DocEnhancer (currently Qwen 2.5 3B)
└── __init__.py

src/retrievers/
├── dense.py          # mDPR dense retriever (FAISS index)
├── bm25.py           # BM25S sparse retriever
└── __init__.py

src/evaluation/
└── metrics.py        # Recall@10, Recall@100, NDCG@10, MRR
```

**Key:** `Query2DocEnhancer.__init__()` takes a `model_name` parameter. You can pass any HuggingFace model ID.

```python
# This is all you change per model:
enhancer = Query2DocEnhancer(
    model_name="tiiuae/Falcon-H1-3B-Instruct",  # <-- swap this
    max_new_tokens=128,
    temperature=0.7,
    top_p=0.9,
    batch_size=8
)
```

---

## Models to Test (10 total)

### Assignment Split

#### Mohammed (5 models) — Arabic-specialized + experimental

| # | Model | Params | Quantization | Priority | Difficulty |
|---|-------|--------|-------------|----------|------------|
| M1 | **Falcon-H1-Arabic-3B** | 3B | None (FP16) | HIGH | Easy |
| M2 | **Jais-2-8B-Chat** | 8B | 4-bit needed | HIGH | Medium |
| M3 | **ALLaM-7B** | 7B | 4-bit needed | MEDIUM | Medium |
| M4 | **Qwen3-4B** | 4B | None (FP16) | MEDIUM | Easy |
| M5 | **GPT-OSS 20B** | 20B | 4-bit needed | LOW | Hard |

**Rationale:** Mohammed takes the Arabic-specialized models (Falcon, Jais, ALLaM) since the research covers them in depth. Qwen3-4B is easy (no quantization). GPT-OSS 20B is experimental.

#### Osman (5 models) — Multilingual + Qwen family

| # | Model | Params | Quantization | Priority | Difficulty |
|---|-------|--------|-------------|----------|------------|
| O1 | **SILMA Kashif-2B** | 2B | None (FP16) | HIGH | Easy |
| O2 | **Qwen 2.5-7B** | 7B | 4-bit needed | HIGH | Easy (familiar) |
| O3 | **Qwen3-8B** | 8B | 4-bit needed | MEDIUM | Medium |
| O4 | **Gemma 3 4B-IT** | 4B | None (FP16) | MEDIUM | Easy |
| O5 | **Aya Expanse 8B** | 8B | 4-bit needed | MEDIUM | Medium |

**Rationale:** Osman already knows Qwen, so Qwen 2.5-7B and Qwen3-8B are natural. SILMA Kashif-2B is interesting as a RAG-specific model. Gemma and Aya round out the multilingual options.

---

## Testing Protocol

### Phase 1: Dense Retrieval (Priority — do this first for ALL models)

Replicate exp_003 exactly, just swap the model. Use the existing notebook as template.

**For each model, record:**
1. Does it load on T4? (Y/N, VRAM used)
2. Does it follow the Arabic prompt? (check first 5 outputs manually)
3. Full metrics: Recall@10, Recall@100, NDCG@10, MRR
4. Runtime (total for 2,896 queries)
5. Any issues encountered

### Phase 2: Sparse Retrieval (BM25S) — after Dense is done for all models

Same enhanced queries, but retrieve with BM25S instead of mDPR.

**Important for BM25S:** The Query2Doc paper notes that for sparse retrieval, the original query should be **repeated** to avoid the pseudo-document dominating:
```python
# For sparse retrieval (BM25), repeat original query:
enhanced_query = f"{original_query} {original_query} {pseudo_document}"

# For dense retrieval (mDPR), simple concat:
enhanced_query = f"{original_query} {pseudo_document}"
```

### Phase 3: Hybrid (RRF) — after Dense and Sparse are done

Combine Dense + Sparse results using Reciprocal Rank Fusion:
```python
def rrf_fusion(dense_results, sparse_results, k=60):
    """Reciprocal Rank Fusion"""
    fused_scores = {}
    for results in [dense_results, sparse_results]:
        for rank, (docid, _) in enumerate(results, 1):
            if docid not in fused_scores:
                fused_scores[docid] = 0
            fused_scores[docid] += 1.0 / (k + rank)
    return sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
```

---

## Per-Model Guide

---

### M1: Falcon-H1-Arabic-3B-Instruct (Mohammed)

**HuggingFace ID:** `tiiuae/Falcon-H1-3B-Instruct`
**License:** Apache 2.0
**Why test:** Best Arabic OALL score at 3B size (~62%), 10pts ahead of peers

#### Loading
```python
enhancer = Query2DocEnhancer(
    model_name="tiiuae/Falcon-H1-3B-Instruct",
    max_new_tokens=128,
    temperature=0.7,
    batch_size=8
)
```

#### Special Considerations
- **Hybrid Mamba-Transformer architecture** — may need specific library versions
- Install: `pip install mamba-ssm causal-conv1d` (for Mamba layers)
- If Mamba install fails on Colab, try: `pip install mamba-ssm[causal-conv1d]`
- If still fails, the model may fall back to pure Transformer mode — check model card
- **Chat template:** Check if the model uses a specific chat template format. If `apply_chat_template` fails, try:
  ```python
  # Fallback if chat template not defined:
  prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{query}\n<|assistant|>\n"
  ```
- **VRAM:** ~6-8 GB in FP16. Fits T4 easily.
- **Batch size:** Start with 8, reduce if OOM

#### Resources
- Model card: https://huggingface.co/tiiuae/Falcon-H1-3B-Instruct
- Blog: https://huggingface.co/blog/tiiuae/falcon-h1-arabic
- Paper: Check model card for citation

---

### M2: Jais-2-8B-Chat (Mohammed)

**HuggingFace ID:** `inceptionai/Jais-2-8B-Chat`
**License:** Apache 2.0 (gated — click-through)
**Why test:** Best 8B Arabic model, custom Arabic vocabulary, 2.6T training tokens
**Status:** Query generation DONE (12 min, 0 errors). Dense evaluation pending.

#### Research Complete (March 2026)
See `research_decisions/jais_2_research.md` for full technical findings.

#### Architecture: Standard Transformer (jais2)
- **NOT hybrid** — standard decoder-only Transformer, batching works perfectly
- 32 layers, 3328 hidden, 26 attention heads, MHA (not GQA)
- RoPE position encoding, Squared-ReLU activation, LayerNorm
- Vocab: 150,272 (Arabic-centric, trained from scratch)
- Context: 8,192 tokens
- Developers: Inception (G42) + MBZUAI + Cerebras

#### Loading (BF16 on A100 — MUST NOT use FP16)
```python
MODEL_NAME = "inceptionai/Jais-2-8B-Chat"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token  # MUST set — not set by default
tokenizer.padding_side = 'left'

# CRITICAL: Use bfloat16, NOT float16
# Squared-ReLU activation overflows FP16 range (max 65,504)
# causing CUDA device-side assert in torch.multinomial
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
```

#### Special Considerations
- **CRITICAL: Must use BF16** — FP16 causes CUDA assert (Squared-ReLU overflow)
- **MUST remove `token_type_ids`** before `generate()` (documented in model card)
- **MUST set pad_token** — `tokenizer.pad_token = tokenizer.eos_token`
- **Chat template:** Standard HF format, `apply_chat_template()` works perfectly
- **Gated model** — accept terms on HF + `notebook_login()`
- **VRAM (BF16):** 16.6 GB used on A100. No quantization needed.
- **Batch size:** 16 on A100 (25.8 GB free after model load)
- **Speed:** 241.5 queries/min — fastest model tested so far

#### Actual Results (Query Generation)
| Metric | Value |
|--------|-------|
| Runtime | 12.0 min |
| Speed | 241.5 q/min |
| Avg expansion | 10.46x (256.0 chars) |
| Median expansion | 5.04x |
| Errors | 0 |

#### Resources
- Model card: https://huggingface.co/inceptionai/Jais-2-8B-Chat
- Blog: https://www.cerebras.ai/blog/jais2
- Paper (Jais-1): arXiv:2308.16149
- Research doc: `research_decisions/jais_2_research.md`
- Notebook: `experiments/Query_generator_jais_2_8b.ipynb`

---

### M3: ALLaM-7B-Instruct (Mohammed) — COMPLETED, DROP

**HuggingFace ID:** `ALLaM-AI/ALLaM-7B-Instruct-preview`
**License:** Apache 2.0
**Why test:** Saudi Arabic LLM, 5.2T tokens training, ICLR 2025 paper, Arabic MMLU 67.78
**Status:** COMPLETE — **Worst performing model. Degraded retrieval -48.9% below baseline. DROP.**

#### Results (exp_007)
| Metric | Dense | BM25 | vs Baseline |
|--------|-------|------|-------------|
| NDCG@10 | 0.2550 | 0.3341 | -48.9% |
| Recall@10 | 0.3335 | 0.4348 | -45.8% |
| Recall@100 | 0.5465 | 0.7004 | -35.0% |
| MRR | 0.2708 | 0.3676 | -49.2% |
| Runtime | 16.1 min | — | 179.5 q/min |

**Root causes:** (1) Sentencepiece `▁` token markers leaking into decoded text — corrupts retriever input. (2) Severe factual hallucinations. (3) Inconsistent expansion ratios (3.3x-23.3x). Preview/alpha model quality issues.

#### Research Complete (March 2026)
See `research_decisions/allam_7b_research.md` for full technical findings.

#### Architecture: Standard LlamaForCausalLM
- **NOT hybrid** — standard Transformer, batching works
- 32 layers, 4096 hidden, 32 attention heads, 32 KV heads (full MHA, no GQA)
- RoPE position encoding, SiLU activation, RMSNorm
- Vocab: 64,000 (expanded from Llama-2's 32K for Arabic)
- Context: 4,096 tokens

#### Loading (FP16 on A100 — no 4-bit needed)
```python
MODEL_NAME = "ALLaM-AI/ALLaM-7B-Instruct-preview"
MODEL_REVISION = "v2"  # Pin preview model revision

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, revision=MODEL_REVISION)
tokenizer.pad_token = tokenizer.eos_token  # MUST set — not set by default
tokenizer.padding_side = 'left'

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    revision=MODEL_REVISION,
    torch_dtype=torch.float16,
    device_map="auto"
)
```

#### Special Considerations
- **PREVIEW model** — alpha status, pin to `revision="v2"` for reproducibility
- **NOT gated** — no HuggingFace login required
- **MUST use `return_token_type_ids=False`** when tokenizing (same as Jais-2)
- **MUST set pad_token** — `tokenizer.pad_token = tokenizer.eos_token`
- **Chat template:** Llama-2 [INST] style, `apply_chat_template()` works
- **Recommended temp:** 0.6 (from model card), also test 0.7 for cross-model comparison
- **VRAM (FP16):** ~16-17 GB total — fits A100 (40 GB) comfortably
- **VRAM (4-bit):** ~6-7 GB total — fits T4 (15 GB) if needed
- **Batch size:** Start with 8 on A100
- **No pre-quantized versions** (GGUF/GPTQ/AWQ) — use bitsandbytes for 4-bit fallback
- **No `trust_remote_code` needed** — standard LlamaForCausalLM

#### Resources
- Model card: https://huggingface.co/ALLaM-AI/ALLaM-7B-Instruct-preview
- Paper: https://arxiv.org/abs/2407.15390 (ICLR 2025)
- OpenReview: https://openreview.net/forum?id=MscdsFVZrN
- Research doc: `research_decisions/allam_7b_research.md`
- Notebook: `experiments/Query_generator_allam_7b.ipynb`

---

### M4: Qwen3-4B (Mohammed)

**HuggingFace ID:** `Qwen/Qwen3-4B`
**License:** Apache 2.0
**Why test:** Newer generation than Qwen 2.5, matches 7B quality, 119 languages
**Status:** COMPLETE — 2nd best model. Dense NDCG@10=0.5691 (+14.0%). BM25 NDCG@10=0.4145 (-10.3%).
**Research doc:** `research_decisions/qwen3_4b_research.md`
**Notebook:** `experiments/Query_generator_qwen3_4b.ipynb`
**Experiment doc:** `docs/experiments/exp_007_qwen3_4b_dense.md`

#### Architecture (Researched)
- **Standard dense Transformer** — GQA (32Q/8KV heads), 36 layers, hidden=2560
- **NOT hybrid** — no Mamba/SSM. Batching works normally.
- **4.02B params** (3.6B non-embedding), ~8 GB in FP16
- **151,936 vocab** (same as Qwen 2.5), `tie_word_embeddings=true`
- **Trained on ~36T tokens** (2x Qwen 2.5's 18T), 119 languages (8 Arabic dialects)

#### Loading
```python
# FP16 on T4 — no quantization needed
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-4B",
    torch_dtype=torch.float16,
    device_map="auto"
)
```

#### Special Considerations
- **CRITICAL: Disable thinking mode** — Qwen3 produces `<think>...</think>` traces by default:
  ```python
  # Disable via apply_chat_template (RECOMMENDED):
  chat_text = tokenizer.apply_chat_template(
      messages,
      tokenize=False,
      add_generation_prompt=True,
      enable_thinking=False  # <-- This is the key parameter
  )
  ```
- **Alternative:** Append `/no_think` to user message for per-turn control
- **Safety fallback:** Strip leaked traces: `re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)`
- **NEVER use greedy decoding** — causes infinite repetitions (model card warning)
- **Non-thinking sampling:** temp=0.7, top_p=0.8, top_k=20 (model card recommendation)
- **Requires transformers >= 4.51.0** (earlier versions: `KeyError: 'qwen3'`)
- **No `token_type_ids` issue** (unlike Jais-2)
- **VRAM:** ~8-10 GB in FP16. Fits T4 easily.
- **Batch size:** 32 on A100 (33.9 GB free), 8 on T4

#### Actual Results (exp_007)
| Metric | Dense | BM25 |
|--------|-------|------|
| NDCG@10 | 0.5691 (+14.0%) | 0.4145 (-10.3%) |
| Recall@10 | 0.6824 (+10.9%) | 0.5403 (-9.4%) |
| Recall@100 | 0.8726 (+3.8%) | 0.8152 (-5.0%) |
| MRR | 0.6015 (+12.9%) | 0.4415 (-8.7%) |
| Runtime | 12.4 min | — |
| Speed | 232.6 q/min | — |
| Batch size | 32 | — |
| GPU | A100 (8.5 GB used) | — |
| Errors | 0 | — |

#### Key Benchmarks (vs Qwen 2.5-3B)
| Benchmark | Qwen3-4B | Qwen 2.5-3B | Delta |
|-----------|----------|-------------|-------|
| MMLU | 72.99 | 65.62 | +7.37 |
| BBH | 72.59 | 56.30 | +16.29 |
| MMMLU (multilingual) | 71.42 | 65.55 | +5.87 |

#### Resources
- Model card: https://huggingface.co/Qwen/Qwen3-4B
- Blog: https://qwenlm.github.io/blog/qwen3/
- Paper: arXiv:2505.09388

---

### M5: GPT-OSS 20B (Mohammed)

**HuggingFace ID:** `openai/gpt-oss-20b`
**License:** Apache 2.0
**Why test:** Only MoE model + only non-Arabic-specialized model in comparison. OpenAI's first open-source LLM.
**Status:** Research complete (March 2026). Implementation pending.

#### Research Complete (March 2026)
See `research_decisions/gpt_oss_20b_research.md` for full technical findings.

#### Architecture: MoE Transformer (GptOssForCausalLM)
- **NOT hybrid** — standard Transformer with MoE routing, batching should work
- 24 layers, 2880 hidden, 64 attention heads, 8 KV heads (GQA), head_dim=64
- **32 experts, top-4 routed per token** → 3.61B active params (of 20.91B total)
- Alternating sliding window (128 tokens) + full attention layers
- RoPE with YaRN scaling, SwiGLU activation, RMSNorm
- Vocab: 201,088 (o200k_harmony BPE via tiktoken, same base as GPT-4o)
- Context: 131,072 tokens (128K)
- Native MXFP4 quantization on MoE weights (trained at this precision)
- Developers: OpenAI
- Paper: arXiv:2508.10925

#### Loading (Unsloth BNB 4-bit — RECOMMENDED)
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/gpt-oss-20b",
    dtype=None,
    max_seq_length=1024,
    load_in_4bit=True,
    full_finetuning=False,
)
FastLanguageModel.for_inference(model)  # 2x speedup

# Generation with harmony format:
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": query}
]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
    reasoning_effort="low"  # Minimize CoT overhead
).to("cuda")

outputs = model.generate(**inputs, max_new_tokens=128, temperature=0.7, top_p=0.9, do_sample=True)
```

#### Special Considerations
- **CRITICAL: Harmony chat format is MANDATORY** — model "will not work correctly otherwise." `apply_chat_template()` handles this automatically.
- **Set `reasoning_effort="low"`** — minimizes chain-of-thought tokens for query expansion
- **Output parsing:** May need to extract `final` channel content and strip `analysis` reasoning tokens
- **Bleeding-edge dependencies:** Requires `torch>=2.8.0`, `triton>=3.4.0`, `transformers==4.56.2`, specific Unsloth commits
- **Arabic is a HIGH RISK:** English-dominant training, model card warns about non-English degradation. ILMAAM Arabic ~58%. Sanity-check first 5 queries carefully.
- **MoE batching:** Standard Transformer routing, should work — but MoE overhead may limit batch sizes. Start with 4, reduce if OOM.
- **NOT gated** — no HuggingFace login required
- **VRAM (Unsloth BNB 4-bit):** ~14 GB on T4. Use A100 for comfortable headroom.
- **Batch size:** Start with 4 on A100, 1-2 on T4
- **Model default temp:** 1.0 — test both 1.0 and 0.7 for comparison
- **Priority:** LOW — do this last, only if time permits
- **Thesis value:** ANY result is a finding — either MoE works for Arabic QE or Arabic-specialized training is essential

#### Resources
- Model card: https://huggingface.co/openai/gpt-oss-20b
- Paper: https://arxiv.org/abs/2508.10925
- Announcement: https://openai.com/index/introducing-gpt-oss/
- Unsloth model: https://huggingface.co/unsloth/gpt-oss-20b
- Unsloth docs: https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune
- Research doc: `research_decisions/gpt_oss_20b_research.md`

---

### O1: SILMA Kashif-2B (Osman)

**HuggingFace ID:** `silma-ai/SILMA-Kashif-2B-Instruct-v1.0`
**License:** Open weights
**Why test:** Purpose-built for Arabic RAG. Very small (2B), very fast.

#### Loading
```python
enhancer = Query2DocEnhancer(
    model_name="silma-ai/SILMA-Kashif-2B-Instruct-v1.0",
    max_new_tokens=128,
    temperature=0.7,
    batch_size=16  # Small model, can use larger batches
)
```

#### Special Considerations
- **Built on Gemma architecture** — uses Gemma chat template
- **RAG-optimized but extractive-focused:** May give short, factual answers instead of rich pseudo-documents. This could actually be fine for query expansion (concise = relevant terms)
- **Chat template:** May use Gemma-style. If `apply_chat_template` fails:
  ```python
  prompt = f"<start_of_turn>user\n{system_prompt}\n{query}<end_of_turn>\n<start_of_turn>model\n"
  ```
- **Context length:** Only 12K tokens (plenty for our use case)
- **VRAM:** ~4-5 GB in FP16. Fits easily. Can use batch_size=16
- **Speed:** Fastest model. Expect ~15-20 min for 2,896 queries
- **Key question:** Can a 2B extractive model generate useful expansions, or is it too small?

#### Resources
- Model card: https://huggingface.co/silma-ai/SILMA-Kashif-2B-Instruct-v1.0
- RAGQA Benchmark: https://huggingface.co/blog/karimouda/silma-ragqa-benchmark-v10

---

### O2: Qwen 2.5-7B-Instruct, 4-bit (Osman)

**HuggingFace ID:** `Qwen/Qwen2.5-7B-Instruct` (or pre-quantized: `unsloth/Qwen2.5-7B-Instruct-bnb-4bit`)
**License:** Apache 2.0
**Why test:** Stronger version of the already-working Qwen 2.5 3B. Direct size comparison.

#### Loading (use pre-quantized for easiest setup)
```python
# Option A: Pre-quantized from Unsloth (easiest)
enhancer = Query2DocEnhancer(
    model_name="unsloth/Qwen2.5-7B-Instruct-bnb-4bit",
    max_new_tokens=128,
    temperature=0.7,
    batch_size=4
)
# Note: Query2DocEnhancer loads FP16 by default. For pre-quantized models,
# you need to modify loading or load manually:

from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "unsloth/Qwen2.5-7B-Instruct-bnb-4bit",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("unsloth/Qwen2.5-7B-Instruct-bnb-4bit")

# Option B: Quantize yourself with bitsandbytes
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct",
    quantization_config=bnb_config,
    device_map="auto"
)
```

#### Special Considerations
- **Same chat template as Qwen 2.5 3B** — `apply_chat_template` works identically
- **Osman already knows this codebase** — should be fastest to implement
- **VRAM (4-bit):** ~4 GB weights + overhead ≈ 6-8 GB total
- **Batch size:** Start with 4, try 8 if VRAM allows
- **Key comparison:** Direct 3B vs 7B for Qwen 2.5. Quantifies the size-quality tradeoff.
- **Expected:** Better quality than 3B but slower. ~60-80 min for 2,896 queries.

#### Resources
- Pre-quantized: https://huggingface.co/unsloth/Qwen2.5-7B-Instruct-bnb-4bit
- GPTQ variant: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4

---

### O3: Qwen3-8B (Osman)

**HuggingFace ID:** `Qwen/Qwen3-8B`
**License:** Apache 2.0
**Why test:** Newest generation Qwen, 119 languages, significant quality jump

#### Loading (4-bit quantization required)
```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-8B",
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B")
```

#### Special Considerations
- **Same thinking mode issue as Qwen3-4B** — see M4 above. Disable it:
  ```python
  # Strip thinking traces from output
  import re
  pseudo_doc = re.sub(r'<think>.*?</think>', '', pseudo_doc, flags=re.DOTALL).strip()
  ```
- **Key comparison:** Qwen3-8B vs Qwen 2.5-7B. Measures generation improvement between model families.
- **VRAM (4-bit):** ~4.5 GB weights + overhead ≈ 7-9 GB total
- **Batch size:** Start with 4
- **Expected:** Best Qwen quality in our comparison

#### Resources
- Model card: https://huggingface.co/Qwen/Qwen3-8B
- Blog: https://qwenlm.github.io/blog/qwen3/

---

### O4: Gemma 3 4B-IT (Osman)

**HuggingFace ID:** `google/gemma-3-4b-it`
**License:** Gemma Terms of Use (requires acceptance on HuggingFace)
**Why test:** Google's multilingual model, 140+ languages, baseline comparison

#### Loading
```python
# IMPORTANT: Accept license on HuggingFace first, then login
# huggingface-cli login

enhancer = Query2DocEnhancer(
    model_name="google/gemma-3-4b-it",
    max_new_tokens=128,
    temperature=0.7,
    batch_size=8
)
```

#### Special Considerations
- **Gated model** — must accept license at https://huggingface.co/google/gemma-3-4b-it and login in Colab:
  ```python
  from huggingface_hub import login
  login(token="YOUR_HF_TOKEN")
  ```
- **Gemma chat template:** Uses `<start_of_turn>` format. `apply_chat_template` should work.
- **Weakest Arabic** among our candidates (OALL ~10pts below Falcon-3B). Good as a lower-bound comparison.
- **VRAM:** ~8-10 GB in FP16. Fits T4.
- **Batch size:** Start with 8

#### Resources
- Model card: https://huggingface.co/google/gemma-3-4b-it
- Docs: https://ai.google.dev/gemma

---

### O5: Aya Expanse 8B (Osman)

**HuggingFace ID:** `CohereLabs/aya-expanse-8b`
**License:** CC-BY-NC-4.0 (non-commercial — fine for thesis)
**Why test:** Purpose-built multilingual (101 langs), 83.9% win rate vs Llama 3.1 8B

#### Loading (4-bit quantization required)
```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "CohereLabs/aya-expanse-8b",
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("CohereLabs/aya-expanse-8b")
```

#### Special Considerations
- **Command-R architecture** (Cohere) — check chat template format. May use:
  ```python
  # If apply_chat_template fails, try Cohere format:
  prompt = f"<|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|>{system_prompt}<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|USER_TOKEN|>{query}<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>"
  ```
- **101 languages** — explicitly trained for Arabic among many others
- **Non-commercial license** — fine for thesis, note in paper
- **VRAM (4-bit):** ~4.5 GB weights + overhead ≈ 7-9 GB total
- **Batch size:** Start with 4

#### Resources
- Model card: https://huggingface.co/CohereLabs/aya-expanse-8b

---

## How to Modify Query2DocEnhancer for Each Model

The current `Query2DocEnhancer` class loads models in FP16. For 4-bit models, you have two options:

### Option A: Modify the class (recommended)

Create a modified version of `query2doc.py` that accepts a `quantization_config`:

```python
# In your notebook, before creating the enhancer:
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from src.enhancers.query2doc import Query2DocEnhancer

# For FP16 models (3B, 4B) — use as-is:
enhancer = Query2DocEnhancer(model_name="tiiuae/Falcon-H1-3B-Instruct")

# For 4-bit models (7B, 8B) — load model separately, then inject:
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Create enhancer with a small model first (to initialize the class)
enhancer = Query2DocEnhancer.__new__(Query2DocEnhancer)
enhancer.model_name = "inceptionai/Jais-2-8B-Chat"
enhancer.max_new_tokens = 128
enhancer.temperature = 0.7
enhancer.top_p = 0.9
enhancer.batch_size = 4

# Load model with quantization
enhancer.tokenizer = AutoTokenizer.from_pretrained("inceptionai/Jais-2-8B-Chat")
if enhancer.tokenizer.pad_token is None:
    enhancer.tokenizer.pad_token = enhancer.tokenizer.eos_token
enhancer.tokenizer.padding_side = 'left'

enhancer.model = AutoModelForCausalLM.from_pretrained(
    "inceptionai/Jais-2-8B-Chat",
    quantization_config=bnb_config,
    device_map="auto"
)
enhancer.model.eval()

enhancer.system_prompt = (
    "You are asked to write a passage that answers the given query. "
    "Do not ask the user for further clarification. "
    "Respond in Arabic only."
)
```

### Option B: Direct notebook implementation

If the class injection is too hacky, just implement the generation loop directly in the notebook. Copy the key functions from `query2doc.py` and modify as needed.

---

## Results Tracking

### Naming Convention

```
Experiment IDs:
  exp_003  = Qwen 2.5 3B + Dense (DONE - reference)
  exp_004  = [Model] + Dense
  exp_005  = [Model] + BM25S
  exp_006  = [Model] + Hybrid

File naming:
  results/[model_short_name]_dense/exp_NNN_metrics.json
  results/[model_short_name]_bm25/exp_NNN_metrics.json
```

### Results Table (fill as you go)

Copy this table and fill in results:

```
| Model | Type | Params | Quant | Recall@10 | Recall@100 | NDCG@10 | MRR | Runtime | Notes |
|-------|------|--------|-------|-----------|------------|---------|-----|---------|-------|
| Qwen 2.5 3B (ref) | Multi | 3B | FP16 | 0.6608 | 0.8594 | 0.5435 | 0.5742 | 40m | DONE |
| Falcon-H1-Arabic-3B | Arabic | 3B | BF16 | 0.6484 | 0.8531 | 0.5359 | 0.5681 | ~60-90m | batch=1 (Mamba bug). BM25: 0.4038. |
| **Jais-2-8B-Chat** | **Arabic** | **8B** | **BF16** | **0.7161** | **0.8981** | **0.6018** | **0.6356** | **12m** | **BEST MODEL. +20.5% NDCG. BM25: 0.5122 (+10.8%). BF16 required.** |
| **ALLaM-7B (preview)** | **Arabic** | **7B** | **FP16** | **0.3335** | **0.5465** | **0.2550** | **0.2708** | **16m** | **WORST MODEL. -48.9% NDCG vs baseline. Tokenizer bug (sentencepiece leak) + hallucinations. DROP.** |
| **Qwen3-4B (exp_007)** | **Multi** | **4B** | **FP16** | **0.6824** | **0.8726** | **0.5691** | **0.6015** | **12m** | **2nd BEST. +14.0% NDCG. BM25: 0.4145 (-10.3%). Easiest model — no quirks. batch=32.** |
| ~~GPT-OSS 20B~~ | ~~MoE~~ | ~~20.9B (3.6B active)~~ | ~~BNB 4-bit~~ | ~~—~~ | ~~—~~ | ~~—~~ | ~~—~~ | ~~~14h est.~~ | **DROPPED: 70x slower than Jais-2 (71.4s/batch vs 12m total). Severe hallucinations (3/5 queries factually wrong). English-dominant training. Forced-final-channel fix achieved 100% Arabic but facts unreliable.** |
| SILMA Kashif-2B | Arabic | 2B | FP16 | | | | | | |
| Qwen 2.5-7B | Multi | 7B | 4-bit | | | | | | |
| Qwen3-8B | Multi | 8B | 4-bit | | | | | | |
| Gemma 3 4B-IT | Multi | 4B | FP16 | | | | | | |
| Aya Expanse 8B | Multi | 8B | 4-bit | | | | | | |
```

---

## Priority Order

Given 3 days, you probably cannot test all 10 × 3 retrievers = 30 experiments. Here's the priority:

### Day 1 (12 Feb): Dense retrieval, easiest models first
- **Mohammed:** Falcon-H1-Arabic-3B (FP16, easy), Qwen3-4B (FP16, easy)
- **Osman:** SILMA Kashif-2B (FP16, tiny), Qwen 2.5-7B (familiar, pre-quantized)

### Day 2 (13 Feb): Dense retrieval, quantized models
- **Mohammed:** Jais-2-8B (4-bit), ALLaM-7B (4-bit)
- **Osman:** Qwen3-8B (4-bit), Gemma 3 4B-IT (FP16), Aya Expanse 8B (4-bit)

### Day 3 (14 Feb): Best models on BM25S + Hybrid + thesis writing
- Pick top 2-3 models from Dense results
- Run those on BM25S and Hybrid
- Start documenting results for thesis

### GPT-OSS 20B: Only if everything else is done and time permits

---

## Troubleshooting

### Common Issues

**OOM (Out of Memory):**
1. Reduce `batch_size` (try 2, then 1)
2. Reduce `max_new_tokens` (try 64)
3. Clear VRAM: `torch.cuda.empty_cache()`
4. Restart Colab runtime

**Model won't load:**
1. Check if gated → accept license on HuggingFace → `huggingface-cli login`
2. Check if needs specific library → read model card "Usage" section
3. Try `trust_remote_code=True` in `from_pretrained()`

**Chat template fails:**
1. Check model card for exact prompt format
2. Try `tokenizer.chat_template` to see if it's defined
3. Fall back to manual prompt formatting (see per-model guides above)

**Output is gibberish or in wrong language:**
1. The model likely doesn't support Arabic well → mark as failed, move on
2. Try adding "باللغة العربية" (in Arabic) to the prompt
3. Check a few outputs manually before running full experiment

**Output contains thinking traces (Qwen3):**
```python
import re
pseudo_doc = re.sub(r'<think>.*?</think>', '', pseudo_doc, flags=re.DOTALL).strip()
```

**4-bit model produces worse results than FP16:**
This is expected — quantization loses some quality. Document the gap.

---

## What to Document for Each Model

After testing, write a brief note (can be in the results JSON or a comment) covering:

1. **Did it load?** VRAM used, any install issues
2. **Does it follow the Arabic prompt?** Check first 5 outputs
3. **Output quality (subjective):** Are expansions relevant? Hallucinations?
4. **Metrics:** All 4 metrics
5. **Runtime:** Total time for 2,896 queries
6. **Recommendation:** Keep / Drop / Promising (needs tuning)
