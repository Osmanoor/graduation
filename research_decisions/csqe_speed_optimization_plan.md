# CSQE Speed Optimization Plan: Cross-Query Batching + BF16

**Date:** 2026-04-10  
**Status:** Plan ready — awaiting Mohammed's approval  
**Applies to:** `experiments/exp_013_csqe_aya_8b.ipynb`  
**Target GPU:** A100 80GB (Colab A100 High)

---

## Problem

| Metric | Current | Target |
|--------|---------|--------|
| Time per query | ~27s | ~2-3s |
| Total (2896 queries) | ~22h | ~1.5-2.5h |
| VRAM used | ~15/40 GB | ~40-50/80 GB |
| Generate calls | 2 per query = 5,792 total | 2 per batch of 16 = ~362 total |

**Root cause:** Each query makes 2 separate `model.generate()` calls sequentially. The GPU is idle between calls (CPU overhead for tokenization, decoding, dict assembly). With only 15GB used, 65GB of A100 80GB is wasted.

---

## Optimization Strategy (2 changes)

### Change 1: BF16 instead of 4-bit quantization

**Why:** 4-bit NF4 saves VRAM but adds dequantization overhead per forward pass. On A100 80GB we have plenty of room for BF16.

| Loading | Model VRAM | Remaining for KV cache + batching |
|---------|-----------|-----------------------------------|
| 4-bit NF4 (current) | ~5-6 GB | ~34 GB (on 40GB GPU) |
| BF16 (proposed) | ~16 GB | ~64 GB (on 80GB GPU) |

**Evidence:** Jais-2 8B runs in BF16 on A100 in our `Query_generator_jais_2_8b.ipynb` with batch_size=16. Aya Expanse 8B is the same size class.

**Code change (Cell 11):**
```python
# REMOVE: BitsAndBytesConfig entirely
# REPLACE with:
model = AutoModelForCausalLM.from_pretrained(
    CONFIG['model_name'],
    torch_dtype=torch.bfloat16,
    device_map='auto',
    trust_remote_code=True
)
```

No `max_memory` cap needed — BF16 8B model fits comfortably in 80GB.

### Change 2: Cross-query batching

**Why:** Instead of processing queries one-by-one, we group N queries and run a single `model.generate()` for all their corpus prompts, then another for all their blind prompts.

**Proven pattern (from our Aya Query2Doc notebook, batch_size=32):**
```python
# 1. apply_chat_template per query (loop — not batchable)
texts = [tokenizer.apply_chat_template(msgs, tokenize=False, ...) for msgs in all_messages]
# 2. Tokenize all at once with left-padding
inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=...).to(device)
# 3. Single generate call
outputs = model.generate(**inputs, ...)
# 4. Batch decode
input_length = inputs.input_ids.shape[1]
results = tokenizer.batch_decode(outputs[:, input_length:], skip_special_tokens=True)
```

This is identical to what we already use in `Query_generator_aya_8b.ipynb` (batch_size=32) and `Query_generator_jais_2_8b.ipynb` (batch_size=16).

---

## Detailed Design

### Two prompt types have different batch sizes

| Prompt type | Approx. input tokens | Recommended batch_size | Why |
|-------------|---------------------|----------------------|-----|
| Corpus (CSQE) | ~800-1000 tokens (5 docs × 128 tok + template + one-shot) | **8** | Long prompts = large KV cache per sequence |
| Blind (KEQE) | ~60-80 tokens (query + template) | **32** | Short prompts, minimal padding waste |

### num_return_sequences decision: **DROP IT for batching**

Currently we use `num_return_sequences=2` to get 2 samples per prompt in one call. With cross-query batching, combining `num_return_sequences=2` with `batch_size=B` means `B*2` active sequences — the output indexing becomes fragile and doubles memory.

**Better approach:** Run 2 separate batched passes for corpus (sample 1, sample 2) and 2 for blind. Total = 4 generate calls per batch instead of 2, but each call processes B queries → still a massive win over 2*2896 sequential calls.

**Math:**
- 4 calls × ceil(2896/B) batches
- Corpus (B=8): 4 × 362 = 1,448 calls... no wait:
  - Corpus pass 1: ceil(2896/8) = 362 calls
  - Corpus pass 2: 362 calls  
  - Blind pass 1: ceil(2896/32) = 91 calls
  - Blind pass 2: 91 calls
  - Total: 906 generate calls (vs. 5,792 current) = **6.4x fewer calls**

**Alternative (keep num_return_sequences=2):**
- Corpus: ceil(2896/8) = 362 calls, each producing 2 samples  
- Blind: ceil(2896/32) = 91 calls, each producing 2 samples
- Total: 453 calls = **12.8x fewer calls**
- Risk: output tensor shape = [B*2, seq_len], need reshape to [B, 2, seq_len]
- This works in HuggingFace: output order is [input0_seq0, input0_seq1, input1_seq0, input1_seq1, ...]

**Recommendation:** Start with the simpler 4-pass approach (no num_return_sequences). If it works and we want more speed, switch to 2-pass with num_return_sequences=2.

### max_length for tokenizer truncation

**Critical:** Current Aya notebook uses `max_length=512`. But CSQE corpus prompts are ~800-1000 tokens. We MUST set `max_length=2048` for corpus prompts. Blind prompts can keep 512.

---

## Cell-by-Cell Changes

### Cell 5 — CONFIG (minor update)
```python
# ADD these keys:
"corpus_batch_size": 8,    # batch size for corpus (long) prompts
"blind_batch_size": 32,    # batch size for blind (short) prompts
"max_prompt_length": 2048, # max tokenizer length for corpus prompts
```

### Cell 11 — Model Loading (simplify)
```python
# REMOVE: BitsAndBytesConfig, max_memory, low_cpu_mem_usage
# NEW:
model = AutoModelForCausalLM.from_pretrained(
    CONFIG['model_name'],
    torch_dtype=torch.bfloat16,
    device_map='auto',
    trust_remote_code=True
)
model.eval()
```

### Cell 12 — CSQEEnhancer (add batch methods)

Keep the existing `generate_samples()` and `enhance()` for sanity checks. Add new methods:

```python
def batch_generate(self, system_prompt, user_prompts, batch_size, temperature=None, max_length=2048):
    """
    Generate 1 sample per prompt, for a batch of prompts.
    Returns list of decoded strings, one per prompt.
    """
    if temperature is None:
        temperature = self.config['temperature']

    # Step 1: build chat texts
    texts = []
    for user_prompt in user_prompts:
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user',   'content': user_prompt},
        ]
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
        )
        texts.append(text)

    # Step 2: process in mini-batches
    all_outputs = []
    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start:start + batch_size]

        inputs = self.tokenizer(
            batch_texts,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to(self.model.device)

        input_length = inputs.input_ids.shape[1]

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.config['max_new_tokens'],
                temperature=temperature,
                top_p=self.config['top_p'],
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        decoded = self.tokenizer.batch_decode(
            outputs[:, input_length:],
            skip_special_tokens=True
        )
        all_outputs.extend([d.strip() for d in decoded])

    return all_outputs


def batch_enhance(self, qids, queries):
    """
    Full CSQE pipeline for a batch of queries.
    4 generate passes: corpus_sample1, corpus_sample2, blind_sample1, blind_sample2.
    Returns list of result dicts.
    """
    n = len(qids)
    corpus_bs = self.config['corpus_batch_size']
    blind_bs = self.config['blind_batch_size']

    # ── Step 1: Build all prompts ──
    corpus_prompts = []
    all_retrieved = []
    for qid, query in zip(qids, queries):
        docs = self.get_retrieved_docs(qid)
        all_retrieved.append(docs)
        doc_texts = [d['text'] for d in docs if d['text']]
        corpus_prompts.append(build_csqe_prompt(query, doc_texts))

    blind_prompts = [build_blind_prompt(q) for q in queries]

    # ── Step 2: Corpus expansions (2 passes) ──
    corpus_samples_1 = self.batch_generate(
        CSQE_SYSTEM, corpus_prompts, corpus_bs,
        temperature=1.0, max_length=2048
    )
    corpus_samples_2 = self.batch_generate(
        CSQE_SYSTEM, corpus_prompts, corpus_bs,
        temperature=1.0, max_length=2048
    )

    # ── Step 3: Blind expansions (2 passes) ──
    blind_samples_1 = self.batch_generate(
        BLIND_SYSTEM, blind_prompts, blind_bs,
        temperature=1.0, max_length=512
    )
    blind_samples_2 = self.batch_generate(
        BLIND_SYSTEM, blind_prompts, blind_bs,
        temperature=1.0, max_length=512
    )

    # ── Step 4: Assemble results ──
    alpha = self.config['query_repetition']
    results = []
    for i in range(n):
        corpus_exps = [corpus_samples_1[i], corpus_samples_2[i]]
        blind_exps = [blind_samples_1[i], blind_samples_2[i]]
        all_exps = corpus_exps + blind_exps
        final = (queries[i] + ' ') * alpha + ' '.join(all_exps)

        results.append({
            'qid': qids[i],
            'original': queries[i],
            'retrieved_docids': [d['docid'] for d in all_retrieved[i]],
            'retrieved_doc_texts': [d['text'] for d in all_retrieved[i]],
            'corpus_expansions': corpus_exps,
            'blind_expansions': blind_exps,
            'enhanced': final,
        })

    return results
```

### Cell 13 — Sanity Check (unchanged)

Keep using the sequential `enhance()` for the 5-query sanity check. This validates correctness before the batched run.

### Cell 14 — Generation Loop (batched)

```python
# Process in macro-batches (e.g., 200 queries at a time)
MACRO_BATCH = 200  # process 200 queries, then checkpoint

start_idx = 0
results = []

# Resume from checkpoint if exists
if os.path.exists(CONFIG['checkpoint_path']):
    with open(CONFIG['checkpoint_path'], 'rb') as f:
        checkpoint = pickle.load(f)
    results = checkpoint['results']
    start_idx = len(results)
    print(f'Resuming from query {start_idx}')

remaining_qids = query_ids[start_idx:]
remaining_texts = query_texts[start_idx:]

start_time = time.time()

for batch_start in tqdm(range(0, len(remaining_qids), MACRO_BATCH), desc='CSQE batches'):
    batch_end = min(batch_start + MACRO_BATCH, len(remaining_qids))
    batch_qids = remaining_qids[batch_start:batch_end]
    batch_texts_chunk = remaining_texts[batch_start:batch_end]

    try:
        batch_results = enhancer.batch_enhance(batch_qids, batch_texts_chunk)
        results.extend(batch_results)
    except Exception as e:
        print(f'Batch error at {batch_start}: {e}')
        # Fallback: process this batch sequentially
        for qid, query in zip(batch_qids, batch_texts_chunk):
            try:
                result = enhancer.enhance(qid, query)
                result['qid'] = qid
                results.append(result)
            except Exception as e2:
                results.append({...fallback dict...})

    # Checkpoint after each macro-batch
    with open(CONFIG['checkpoint_path'], 'wb') as f:
        pickle.dump({'results': results, 'config': CONFIG}, f)

    elapsed = time.time() - start_time
    done = len(results) - start_idx
    rate = done / (elapsed / 60)
    remaining_q = len(query_ids) - len(results)
    print(f'  {len(results)}/{len(query_ids)} | {rate:.0f} q/min | ~{remaining_q/rate:.0f}min left')
```

---

## Speed Estimate

### Per-batch timing breakdown

| Step | Items | Time estimate | Notes |
|------|-------|---------------|-------|
| Build corpus prompts | 200 queries | ~0.5s | CPU only (truncation, template) |
| Corpus generate pass 1 | 200/8=25 mini-batches | ~50s | ~2s per mini-batch (800-tok input, 128-tok output) |
| Corpus generate pass 2 | 25 mini-batches | ~50s | Same |
| Blind generate pass 1 | 200/32=7 mini-batches | ~7s | ~1s per mini-batch (short input) |
| Blind generate pass 2 | 7 mini-batches | ~7s | Same |
| Assemble + checkpoint | 200 results | ~0.5s | CPU only |
| **Total per macro-batch** | | **~115s** | |

**Total: ceil(2896/200) = 15 macro-batches × 115s = ~29 min**

Conservative estimate with overhead: **45-90 minutes** (vs. current ~22 hours).

### Why BF16 is faster than 4-bit for batched generation

4-bit NF4 dequantizes weights on every forward pass. With batching, the same weights are dequantized for B sequences simultaneously. BF16 skips this entirely — the weights are already in compute-ready format. Typical speedup: 1.3-1.8x on A100 (which has native BF16 tensor cores).

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| BF16 model doesn't fit in 80GB | Very low (16GB model, 80GB GPU) | Fall back to 4-bit with batching |
| Padding waste for corpus prompts | Medium (variable doc lengths) | Use batch_size=8 to limit worst-case padding |
| Batched generation produces different quality | Low (same model, same params) | Sanity check still runs sequentially first |
| OOM during corpus batch generate | Low-Medium | Start with batch_size=4, increase if VRAM permits |
| Left-padding misalignment issues | Very low (proven in our other notebooks) | tokenizer.padding_side='left' already set |

---

## Fallback Plan

If cross-query batching causes issues:

**Fallback A: BF16 + sequential (no batching)**
- Just switch to BF16, keep per-query generation
- Expected speedup: 1.3-1.8x from BF16 alone → ~12-17h
- Minimal code change, very safe

**Fallback B: 4-bit + batching (no BF16)**  
- Keep 4-bit quantization, add cross-query batching
- Expected speedup: ~6x from batching → ~3.5h
- Useful if BF16 causes issues (unlikely on A100)

---

## Implementation Order

1. **First:** Change Cell 11 to BF16 loading (2 min change)
2. **Second:** Run sanity check with existing sequential code — verify BF16 produces same quality
3. **Third:** Add `batch_generate()` and `batch_enhance()` to Cell 12
4. **Fourth:** Run sanity check comparing sequential vs batched output (same 5 queries)
5. **Fifth:** Update Cell 14 with batched loop
6. **Sixth:** Run full 2896 queries

Each step is independently testable. If any step fails, we can stop and debug without losing prior progress.
