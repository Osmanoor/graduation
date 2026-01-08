# Jina-embeddings-v3: Multilingual Embeddings With Task LoRA
**Year:** 2024
**Authors:** Saba Sturua, Isabelle Mohr, Mohammad Kalim Akram, Michael Günther, Bo Wang, et al.
**Venue:** arXiv preprint
**arXiv:** 2409.10173

## Short Description
570M parameter multilingual embedding model with task-specific LoRA adapters for query/passage encoding, classification, clustering, and text matching. Supports 8192 tokens and Matryoshka representation learning for flexible embedding dimensions.

## Research Question
How to create task-optimized embeddings without complex instruction prompts, while maintaining efficiency compared to LLM-based embeddings?

## Main Methodology

### Architecture
| Spec | Value |
|------|-------|
| Base Model | Modified XLM-RoBERTa |
| Parameters | 559M base + 13M adapters = 572M total |
| Max Tokens | 8192 |
| Output Dimension | 1024 (reducible to 32 via MRL) |
| Positional Encoding | RoPE (Rotary Position Embeddings) |
| Attention | FlashAttention 2 |
| Pooling | Mean pooling |

### Task-Specific LoRA Adapters (Key Innovation)
Instead of instruction prompts, uses 5 lightweight LoRA adapters (<3% of params):

| Adapter | Use Case |
|---------|----------|
| `retrieval.query` | Encoding queries in asymmetric retrieval |
| `retrieval.passage` | Encoding documents in asymmetric retrieval |
| `text-matching` | STS, symmetric retrieval, deduplication |
| `classification` | Text classification tasks |
| `separation` | Clustering, reranking |

### Three-Stage Training
1. **Pre-Training:** MLM on CulturaX corpus (89 languages), 100k steps at 512 tokens + 60k steps at 8192 tokens
2. **Embedding Fine-Tuning:** Bi-directional InfoNCE loss on 1B+ text pairs
3. **Adapter Training:** Task-specific training with dedicated loss functions

### Failure Analysis Training
Identified and fixed 4 common retrieval failures:
- F1: Misleading syntactic similarities
- F2: Named entity misinterpretation
- F3: Polar question misunderstanding
- F4: Low-quality document preference

## Dataset & Benchmark

### Training Data
- **Pre-training:** CulturaX corpus (89 languages, ~20% English)
- **Fine-tuning:** 1B+ text pairs from 300+ sub-datasets
- **Adapter training:** MS-MARCO, NQ, STS datasets, synthetic data

### Evaluation
- MTEB benchmark (English)
- Multilingual benchmarks
- Long-context retrieval (NarrativeQA)

## Key Results

### MTEB English Benchmark
| Task | Jina-v3 | mE5-large-instruct |
|------|---------|-------------------|
| Retrieval | 53.87 | 52.47 |
| Classification | **82.58** | 77.56 |
| STS | **85.80** | 84.78 |
| Clustering | 47.35 | 47.49 |
| Reranking | 58.45 | 58.58 |
| **Average** | **65.52** | 64.41 |

### Comparison with LLM-based Embeddings
| Model | Params | Dim | MTEB Avg |
|-------|--------|-----|----------|
| Jina-v3 | 570M | 1024 | 65.52 |
| e5-mistral-7b | 7.1B | 4096 | 66.63 |

Jina-v3 is 12x smaller with only 1% lower performance.

### Matryoshka Representation Learning
| Dimension | MTEB Avg | Retrieval |
|-----------|----------|-----------|
| 1024 | 65.52 | 53.87 |
| 512 | 64.80 | 52.58 |
| 256 | 63.76 | 50.81 |
| 128 | 62.17 | 48.54 |
| 64 | 59.78 | 44.93 |
| 32 | 55.89 | 39.62 |

## Relevance to Our Project

- **Applicable to Arabic?** ⚠️ Maybe - Supports Arabic (89 languages) but not specifically evaluated on MIRACL
- **Uses MIRACL?** ❌ No - Not mentioned in training or evaluation
- **Retrieval metrics reported?** MTEB retrieval metrics (not MIRACL-specific)
- **Feasible for us?** ✅ Yes - API available with 10M free tokens

### Specific Benefits for Our Project
1. **Free API tier:** 10M tokens free per account
2. **Task-specific adapters:** Separate query vs passage encoding
3. **Flexible dimensions:** Can reduce to 256 or 128 for faster search
4. **No GPU needed:** API-based prototyping

### Potential Concerns
1. **Not trained/evaluated on MIRACL** - Unknown Arabic retrieval performance
2. **API dependency** - Need to re-embed with open-source for final experiments
3. **Token costs for full corpus:** 2.1M passages × ~100 tokens = 210M tokens (exceeds free tier)

### Token Usage Calculation for MIRACL
- Corpus embedding (one-time): ~210M tokens (need paid tier or multiple accounts)
- Query embedding per iteration: ~3000 queries × 20 tokens = 60K tokens (negligible)

## Notes

### API Usage
```python
from jina import Client

client = Client(token='YOUR_TOKEN')
embeddings = client.encode(
    texts=['query text'],
    task='retrieval.query'  # or 'retrieval.passage'
)
```

### Open-Source Model
- HuggingFace: `jinaai/jina-embeddings-v3`
- Can run locally on GPU (570M params, ~2-3GB VRAM)

### Key Insight
Jina-v3 is best for:
- Fast prototyping with API
- Classification and STS tasks
- When you need task-specific encoding

Less suitable for:
- MIRACL Arabic (not evaluated)
- Full corpus embedding on free tier
