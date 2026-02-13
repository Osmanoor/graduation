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
**License:** Open source
**Why test:** Best 8B Arabic model, custom Arabic vocabulary

#### Loading (4-bit quantization required)
```python
# Install: pip install bitsandbytes accelerate
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "inceptionai/Jais-2-8B-Chat",
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("inceptionai/Jais-2-8B-Chat")
```

#### Special Considerations
- **Custom chat format:** Jais uses its own prompt format. Check model card for exact template.
  May need custom prompt formatting instead of `apply_chat_template`:
  ```python
  # Jais-specific format (check model card):
  prompt = f"### Instruction:\n{system_prompt}\n\n### Input:\n{query}\n\n### Response:\n"
  ```
- **Tokenizer:** Has custom Arabic-centric vocabulary (different from Qwen/Llama)
- **VRAM (4-bit):** ~5-6 GB weights + overhead ≈ 8-10 GB total
- **Batch size:** Start with 4 (larger model), increase if VRAM allows
- **Speed:** Will be slower than 3B models. Expect ~60-90 min for 2,896 queries

#### Resources
- Model card: https://huggingface.co/inceptionai/Jais-2-8B-Chat
- Blog: https://www.cerebras.ai/blog/jais2

---

### M3: ALLaM-7B-Instruct (Mohammed)

**HuggingFace ID:** `ALLaM-AI/ALLaM-7B-Instruct-preview`
**License:** TBD (check model card)
**Why test:** Saudi Arabic LLM, trained on 5.2T tokens (Arabic + English)

#### Loading (4-bit quantization required)
```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "ALLaM-AI/ALLaM-7B-Instruct-preview",
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("ALLaM-AI/ALLaM-7B-Instruct-preview")
```

#### Special Considerations
- **Preview model** — may have quirks or missing features
- **Access:** May require HuggingFace access request (gated model). Check model card. If gated, run `huggingface-cli login` in Colab first
- **Chat template:** Check if it uses Llama-style or custom format
- **VRAM (4-bit):** ~4 GB weights + overhead ≈ 6-8 GB total
- **Batch size:** Start with 4, increase if VRAM allows
- **Risk:** Limited community testing — may have unexpected behavior

#### Resources
- Model card: https://huggingface.co/ALLaM-AI/ALLaM-7B-Instruct-preview
- May need to check SDAIA documentation for proper usage

---

### M4: Qwen3-4B (Mohammed)

**HuggingFace ID:** `Qwen/Qwen3-4B`
**License:** Apache 2.0
**Why test:** Newer generation than Qwen 2.5, matches 7B quality, 119 languages

#### Loading
```python
enhancer = Query2DocEnhancer(
    model_name="Qwen/Qwen3-4B",
    max_new_tokens=128,
    temperature=0.7,
    batch_size=8
)
```

#### Special Considerations
- **Qwen3 has "thinking mode"** — by default it may produce `<think>...</think>` reasoning traces before answering. To disable:
  ```python
  # Add to generation config to skip thinking:
  generated_ids = model.generate(
      **inputs,
      max_new_tokens=128,
      temperature=0.7,
      top_p=0.9,
      do_sample=True,
      # Force no-thinking mode:
      chat_template_kwargs={"enable_thinking": False}
  )
  ```
  Or use the `/no_think` tag in the prompt. Check model card for details.
- **If thinking mode leaks into output:** Strip `<think>` tags from generated text:
  ```python
  import re
  pseudo_doc = re.sub(r'<think>.*?</think>', '', pseudo_doc, flags=re.DOTALL).strip()
  ```
- **Chat template:** Uses Qwen chat format (same family as Qwen 2.5, `apply_chat_template` should work)
- **VRAM:** ~8-10 GB in FP16. Fits T4.
- **Batch size:** Start with 8

#### Resources
- Model card: https://huggingface.co/Qwen/Qwen3-4B
- Blog: https://qwenlm.github.io/blog/qwen3/

---

### M5: GPT-OSS 20B (Mohammed)

**HuggingFace ID:** Needs identification — see notes below
**License:** TBD
**Why test:** Largest model in our comparison, tests quality vs size tradeoff

#### Identifying the Model
This model was discussed in the 23/1/2026 meeting as "GPT-OSS 20B via Unsloth." You need to identify the exact model. Candidates:
- **Mistral-Small-24B** → `mistralai/Mistral-Small-24B-Instruct-2501` (actually 24B)
- **Gemma 2 27B** → `google/gemma-2-27b-it` (actually 27B)
- **Command-R 35B** → too large
- **Check Unsloth hub for 20B models:** https://huggingface.co/unsloth

If you can't identify the exact "GPT-OSS 20B", pick the best available ~20B model that Unsloth supports on T4.

#### Loading (4-bit quantization REQUIRED, use Unsloth for efficiency)
```python
# Option A: Unsloth (faster, recommended)
# pip install unsloth
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/MODEL-NAME-bnb-4bit",  # Find on Unsloth hub
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True
)

# Option B: bitsandbytes (fallback)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "MODEL-ID",
    quantization_config=bnb_config,
    device_map="auto"
)
```

#### Special Considerations
- **VRAM (4-bit):** ~10 GB weights + overhead ≈ 12-14 GB. VERY tight on T4 (15 GB)
- **Batch size:** Must use 1 or 2 — cannot fit larger batches
- **Speed:** Will be very slow. Expect 2-4 hours for 2,896 queries
- **Risk:** May OOM during generation. If so, reduce `max_new_tokens` to 64
- **Priority:** LOW — do this last, only if time permits
- **Why still test:** If it fits and produces better expansions, the quality-size tradeoff is valuable for the thesis

#### Resources
- Unsloth models: https://huggingface.co/unsloth
- Unsloth GitHub: https://github.com/unslothai/unsloth

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
| Falcon-H1-Arabic-3B | Arabic | 3B | FP16 | | | | | | |
| Jais-2-8B-Chat | Arabic | 8B | 4-bit | | | | | | |
| ALLaM-7B | Arabic | 7B | 4-bit | | | | | | |
| Qwen3-4B | Multi | 4B | FP16 | | | | | | |
| GPT-OSS 20B | TBD | 20B | 4-bit | | | | | | |
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
