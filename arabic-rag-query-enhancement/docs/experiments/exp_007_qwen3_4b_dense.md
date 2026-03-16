# Experiment 007: Qwen3-4B + Query2Doc

**Date:** March 16, 2026
**Status:** Complete
**Researcher:** Mohammed Elhaj
**Baseline:** Experiment 001 (Dense) / Experiment 002 (BM25)
**Reference:** Experiment 003 (Query2Doc + Qwen 2.5 3B, Dense)

---

## Objective

Test Qwen3-4B as the LLM for Query2Doc query expansion, comparing it against:
1. **Qwen 2.5-3B (exp_003):** Same family, older generation — does Qwen3's generational improvement (2x training data, 119 languages, wider architecture) translate to better Arabic QE?
2. **All other tested models:** Where does Qwen3-4B rank in the model comparison (Task 4.0b)?

**Research Questions:**
1. Does the Qwen3 generational improvement translate to better Arabic query expansion?
2. How does 4B (Qwen3) compare to 3B (Qwen 2.5) — does +33% params + 2x data help?
3. Does Qwen3's thinking mode need to be disabled? Does `enable_thinking=False` work reliably?
4. How does Qwen3-4B compare to Jais-2-8B (best model so far)?

---

## Model: Qwen3-4B

| Property | Value |
|----------|-------|
| **HuggingFace ID** | `Qwen/Qwen3-4B` |
| **Developer** | Alibaba Cloud (Qwen Team) |
| **Parameters** | 4.02B (3.6B non-embedding) |
| **Architecture** | Standard dense Transformer (`Qwen3ForCausalLM`) |
| **Attention** | GQA: 32 Q heads, 8 KV heads, head_dim=128 |
| **Layers / Hidden** | 36 layers, 2560 hidden |
| **Training Data** | ~36 trillion tokens (2x Qwen 2.5) |
| **Languages** | 119 (including 8 Arabic dialects: MSA, Najdi, Levantine, Egyptian, Moroccan, Mesopotamian, Ta'izzi-Adeni, Tunisian) |
| **Vocab** | 151,936 tokens (same as Qwen 2.5) |
| **Context** | 32,768 native; 131,072 with YaRN |
| **License** | Apache 2.0 |
| **Paper** | arXiv:2505.09388 |

### Why Qwen3-4B Was Selected

- **Direct generational comparison:** Same Qwen family as baseline (exp_003), allowing isolated measurement of Qwen3's improvements
- **Matches Qwen2.5-7B quality at 4B params:** Demonstrated across MMLU, BBH, MMMLU benchmarks
- **No quantization needed:** 8 GB in FP16, fits T4 and A100 easily
- **Standard Transformer:** No batching bugs (unlike Falcon-H1), no dtype issues (unlike Jais-2)
- **119 languages with explicit Arabic dialect coverage**

---

## Methodology

### Query Enhancement: Query2Doc

Same technique as exp_003. Only the model was swapped.

**System Prompt (same as all experiments):**
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
| `model_name` | `Qwen/Qwen3-4B` | — |
| `max_new_tokens` | 128 | Same as all experiments |
| `temperature` | 0.7 | Qwen3 non-thinking recommendation |
| `top_p` | 0.8 | Qwen3 non-thinking recommendation (vs 0.9 in exp_003) |
| `top_k` | 20 | Qwen3 non-thinking recommendation (new param) |
| `do_sample` | True | MUST sample — greedy causes infinite repetitions |
| `batch_size` | 32 | A100 optimal (33.9 GB free after 8.5 GB model load) |
| `dtype` | `float16` | Standard FP16, no quantization |
| `enable_thinking` | False | CRITICAL: disables `<think>` tag generation |

### Qwen3-Specific: Thinking Mode

Qwen3 models produce internal reasoning in `<think>...</think>` tags by default. This was disabled via:
```python
chat_text = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True,
    enable_thinking=False  # Disables <think> tags
)
```

A regex fallback (`re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)`) was included but never triggered — `enable_thinking=False` worked perfectly across all 2,896 queries.

---

## Experimental Setup

### Dataset
- **Corpus:** MIRACL Arabic (2,061,414 passages)
- **Queries:** 2,896 (dev set)
- **Language:** Modern Standard Arabic (MSA)

### Hardware
- **GPU:** NVIDIA A100-SXM4-40GB (Colab Pro+)
- **VRAM used:** 8.5 GB (model) / 42.4 GB total
- **Free VRAM:** 33.9 GB

### Retrieval Configuration
- **Dense:** mDPR (`castorini/mdpr-tied-pft-msmarco`) + FAISS prebuilt index
- **BM25:** BM25S (pure Python) with pre-built index
- **k:** 100 documents per query

### Evaluation Metrics
- Recall@10, Recall@100, NDCG@10, MRR

### Bug Fix During Experiment
- **VRAM calculation bug:** `torch.cuda.get_device_properties(0).total_mem` raised `AttributeError`. Fixed to correct attribute name `total_memory`.

---

## Results

### Dense Retrieval

| Metric | Baseline (exp_001) | Qwen3-4B (exp_007) | vs Baseline | vs Qwen 2.5 3B (exp_003) |
|--------|--------------------|--------------------|-------------|--------------------------|
| **NDCG@10** | 0.4993 | **0.5691** | **+14.0%** | +4.7% (0.5435) |
| **Recall@10** | 0.6156 | **0.6824** | **+10.9%** | +3.3% (0.6608) |
| **Recall@100** | 0.8407 | **0.8726** | **+3.8%** | +1.5% (0.8594) |
| **MRR** | 0.5328 | **0.6015** | **+12.9%** | +4.8% (0.5742) |

### BM25 Retrieval

| Metric | Baseline (exp_002) | Qwen3-4B (exp_007) | vs Baseline | vs Jais-2-8B (exp_006) |
|--------|--------------------|--------------------|-------------|------------------------|
| **NDCG@10** | 0.4621 | 0.4145 | -10.3% | 0.5122 (+10.8%) |
| **Recall@10** | 0.5964 | 0.5403 | -9.4% | 0.6448 (+8.1%) |
| **Recall@100** | 0.8577 | 0.8152 | -5.0% | 0.8834 (+3.0%) |
| **MRR** | 0.4836 | 0.4415 | -8.7% | 0.5397 (+11.6%) |

### Full Model Comparison (Dense)

| Model | Params | Quant | NDCG@10 | Recall@10 | Recall@100 | MRR | vs Baseline |
|-------|--------|-------|---------|-----------|------------|-----|-------------|
| mDPR baseline | — | — | 0.4993 | 0.6156 | 0.8407 | 0.5328 | — |
| ALLaM-7B (exp_008) | 7B | FP16 | 0.2550 | 0.3335 | 0.5465 | 0.2708 | -48.9% |
| Falcon-H1-3B (exp_005) | 3B | BF16 | 0.5359 | 0.6484 | 0.8531 | 0.5681 | +7.3% |
| Qwen 2.5 3B (exp_003) | 3B | FP16 | 0.5435 | 0.6608 | 0.8594 | 0.5742 | +8.9% |
| **Qwen3-4B (exp_007)** | **4B** | **FP16** | **0.5691** | **0.6824** | **0.8726** | **0.6015** | **+14.0%** |
| **Jais-2-8B (exp_006)** | **8B** | **BF16** | **0.6018** | **0.7161** | **0.8981** | **0.6356** | **+20.5%** |

**Ranking:** Jais-2-8B > **Qwen3-4B** > Qwen 2.5-3B > Falcon-H1-3B > ALLaM-7B

---

## Analysis

### 1. Generational Improvement Confirmed

Qwen3-4B beats Qwen 2.5-3B on every metric (+4.7% NDCG@10, +3.3% Recall@10, +4.8% MRR). The Qwen3 improvements translate directly to better query expansion:

| Factor | Qwen 2.5-3B | Qwen3-4B | Impact |
|--------|-------------|----------|--------|
| Training data | ~18T tokens | ~36T tokens | 2x more diverse knowledge |
| Languages | 29 | 119 (8 Arabic dialects) | Better Arabic coverage |
| Architecture | 16Q/2KV GQA | 32Q/8KV GQA | Richer attention patterns |
| Parameters | 3.09B | 4.02B | +30% capacity |

This is a key thesis finding: **within the same model family, newer generations produce meaningfully better query expansions**, and the improvement compounds across multiple architectural and data advances.

### 2. Best Sub-8B Model

Qwen3-4B at +14.0% NDCG@10 is nearly double the improvement of Qwen 2.5-3B (+8.9%) and Falcon-H1 (+7.3%). For resource-constrained deployments (T4 with 15 GB, no quantization), Qwen3-4B is the clear winner — 8.5 GB VRAM vs Jais-2's 16.6 GB.

### 3. Training Data Volume > Arabic Specialization

Qwen3-4B (multilingual, 36T tokens) outperforms Falcon-H1-3B (Arabic-specialized, OALL ~62%) despite Falcon's higher Arabic benchmark scores. This suggests that:
- **Volume and diversity of training data** matters more than Arabic-specific optimization for query expansion
- **Arabic NLP benchmarks (OALL, AraGen)** don't directly predict query expansion quality
- The relationship between benchmark scores and downstream task performance is not straightforward

### 4. BM25 Term Dilution Pattern Continues

Qwen3-4B follows the same BM25 degradation pattern as Qwen 2.5-3B and Falcon-H1 (-10.3% NDCG@10). Only Jais-2 improves BM25, likely due to its concise, lexically-precise Arabic expansions from the Arabic-centric 150K vocabulary. This is a technique limitation (simple concatenation dilutes original query terms) rather than a model limitation.

### 5. Easiest Engineering Experience

| | Qwen 2.5 3B | Falcon-H1-3B | Jais-2-8B | **Qwen3-4B** |
|--|-------------|-------------|-----------|-------------|
| GPU required | T4 (free) | A100 ($10/mo) | A100 ($10/mo) | T4 or A100 |
| VRAM | ~6 GB | ~10-11 GB | ~16.6 GB | **~8.5 GB** |
| Batch size | 8 | 1 (bug) | 16 | **32** |
| Runtime | ~40 min | ~60-90 min | ~12 min | **~12 min** |
| Special handling | None | Mamba bugs, BF16 | BF16, token_type_ids | **enable_thinking=False only** |
| Errors | 0 | 0 | 0 | **0** |

---

## Runtime Performance

| Phase | Time | Notes |
|-------|------|-------|
| Model download | ~20 sec | ~8 GB (first run only) |
| Query generation | 12.4 min | 91 batches of 32, 232.6 q/min |
| Dense retrieval | ~5 min | FAISS prebuilt index |
| BM25 retrieval | ~5 min | Pre-built BM25S index |
| Evaluation | <1 min | — |

**Speed comparison:**
| Model | Speed (q/min) | Batch Size |
|-------|--------------|------------|
| Falcon-H1-3B | ~32-48 | 1 |
| Qwen 2.5 3B | ~72 | 8 |
| **Qwen3-4B** | **232.6** | **32** |
| Jais-2-8B | 241.5 | 16 |

---

## Files Generated

```
enhanced_queries_qwen3_4b.pkl   # Enhanced queries, saved to Google Drive
```

Pickle file structure:
```python
{
    'query_ids': [...],       # 2,896 query IDs
    'original': [...],        # Original query texts
    'enhanced': [...],        # Enhanced query texts (original + pseudo-doc)
    'metadata': {
        'model': 'Qwen/Qwen3-4B',
        'architecture': 'Standard Transformer (RoPE, SiLU, RMSNorm, GQA 32Q/8KV)',
        'quantization': 'None (FP16)',
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 20,
        'thinking_mode': 'disabled (enable_thinking=False)',
        'batch_size': 32,
        'gpu': 'NVIDIA A100-SXM4-40GB',
        'runtime_minutes': 12.4,
        'queries_per_minute': 232.6,
        'errors': 0
    }
}
```

---

## Lessons Learned

### Technical
1. **FP16 fits easily on both T4 and A100** — lightest model tested (8.5 GB). No quantization needed anywhere.
2. **Batch size 32 optimal on A100** — 33.9 GB free after model load gives massive headroom.
3. **Thinking mode disabled correctly** — `enable_thinking=False` worked perfectly, zero leaks across 2,896 queries.
4. **Easiest model in the comparison** — no batching bugs, no dtype issues, no token_type_ids removal. Just load and run.
5. **VRAM bug fix:** `total_mem` -> `total_memory` in `torch.cuda.get_device_properties(0)`.

### Research
1. **Qwen3 generational improvement translates to better Arabic QE** — +4.7% NDCG@10 over Qwen 2.5-3B.
2. **2nd best model overall** — behind Jais-2-8B but ahead of all 3B models.
3. **Training data volume > Arabic specialization** for query expansion.
4. **BM25 term dilution is technique-level**, not model-level — confirmed by 4th model showing same pattern.

---

## References

1. Wang, L., Yang, N., & Wei, F. (2023). Query2doc: Query Expansion with Large Language Models. arXiv:2303.07678.
2. Qwen Team (2025). Qwen3 Technical Report. arXiv:2505.09388.
3. Yang, A., et al. (2024). Qwen2.5 Technical Report. arXiv:2412.15115.
4. Zhang, X., et al. (2023). MIRACL: A Multilingual Retrieval Dataset. TACL.
5. Model card: https://huggingface.co/Qwen/Qwen3-4B
6. Research notes: `research_decisions/qwen3_4b_research.md`

---

**Experiment conducted by:** Mohammed Elhaj
**Institution:** University of Khartoum
**Date:** March 16, 2026
