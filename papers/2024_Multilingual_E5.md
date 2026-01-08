# Multilingual E5 Text Embeddings: A Technical Report
**Year:** 2024
**Authors:** Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, Furu Wei
**Venue:** Technical Report (Microsoft)
**arXiv:** 2402.05672

## Short Description
Open-source multilingual text embedding models (small/base/large) extending English E5 to 100+ languages. Trained with contrastive pre-training on 1B multilingual pairs, followed by fine-tuning on labeled datasets including MIRACL. Instruction-tuned variant achieves SOTA on MTEB.

## Research Question
How to extend English E5 embeddings to support 100+ languages while maintaining competitive performance on both English and multilingual tasks?

## Main Methodology

### Model Variants
| Model | Parameters | Dimension | Base Model |
|-------|------------|-----------|------------|
| mE5-small | 118M | 384 | Multilingual MiniLM |
| mE5-base | 278M | 768 | XLM-RoBERTa-base |
| mE5-large | 560M | 1024 | XLM-RoBERTa-large |
| mE5-large-instruct | 560M | 1024 | XLM-RoBERTa-large + GPT-4 data |

### Two-Stage Training
1. **Weakly-supervised Contrastive Pre-training:**
   - ~1B multilingual text pairs
   - Batch size 32k, 30k steps
   - Sources: Wikipedia, mC4, CC-News, NLLB, Reddit, S2ORC, xP3

2. **Supervised Fine-tuning:**
   - ~1.6M labeled samples
   - Hard negatives + knowledge distillation from cross-encoder
   - Includes MIRACL (40k) and Mr.TyDi (50k)

### Instruction-Tuned Variant
- Additional 500k synthetic data from GPT-3.5/4
- 150k unique instructions, 93 languages
- Task-specific instruction templates

## Dataset & Benchmark

### Pre-training Data (~1B pairs)
- Wikipedia: 150M
- mC4: 160M
- Multilingual CC News: 160M
- NLLB (translation): 160M
- Reddit: 160M
- S2ORC: 50M
- Stackexchange: 50M
- xP3: 80M

### Fine-tuning Data (~1.6M samples)
- MS-MARCO Passage: 500k
- NQ, TriviaQA, SQuAD: 220k
- NLI: 275k
- **MIRACL: 40k** ✅
- **Mr.TyDi: 50k** ✅
- DuReader: 86k

## Key Results

### MIRACL Arabic (Table 6 in paper)
| Model | nDCG@10 | Recall@100 |
|-------|---------|------------|
| BM25 | 39.3 | 78.7 |
| mDPR | 41.5 | 78.8 |
| mE5-small | 71.4 | 96.2 |
| mE5-base | 71.6 | 95.9 |
| **mE5-large** | **76.0** | **97.3** |
| mE5-large-instruct | 76.8 | 97.5 |

### MTEB English Benchmark
| Model | Average |
|-------|---------|
| LaBSE | 45.2 |
| Cohere-multilingual-v3 | 64.0 |
| BGE-large-en-v1.5 | 64.2 |
| mE5-small | 57.9 |
| mE5-base | 59.5 |
| mE5-large | 61.5 |
| **mE5-large-instruct** | **64.4** |

### MIRACL All Languages Average
| Model | nDCG@10 | Recall@100 |
|-------|---------|------------|
| BM25 | 39.3 | 78.7 |
| mDPR | 41.5 | 78.8 |
| mE5-small | 60.8 | 92.4 |
| mE5-base | 62.3 | 93.1 |
| mE5-large | 66.5 | 94.3 |
| mE5-large-instruct | 65.7 | 94.6 |

## Relevance to Our Project

- **Applicable to Arabic?** ✅ Yes - Explicitly trained on MIRACL Arabic (40k samples) and evaluated
- **Uses MIRACL?** ✅ Yes - Both in fine-tuning (40k) and evaluation
- **Retrieval metrics reported?** nDCG@10, Recall@100 (matches our metrics exactly)
- **Feasible for us?** ✅ Yes
  - mE5-small (118M): ~3-4 hours on Colab, fits easily
  - mE5-base (278M): ~6-8 hours on Colab, fits well
  - mE5-large (560M): ~12-15 hours on Colab, tight but doable

### Specific Benefits for Our Project
1. **Trained on MIRACL Arabic** - Direct applicability, no domain shift
2. **Multiple sizes** - Can use small for prototyping, large for final
3. **Microsoft-backed** - Well-documented, reliable, reproducible
4. **No special prefix needed** - Simpler implementation than instruction-based models

### Potential Concerns
1. mE5-large embedding time (~12-15 hours) requires overnight Colab session
2. Slightly lower than BGE-M3 on Arabic (76.0 vs 78.4 nDCG@10)

## Notes

### HuggingFace Models
- `intfloat/multilingual-e5-small`
- `intfloat/multilingual-e5-base`
- `intfloat/multilingual-e5-large`
- `intfloat/multilingual-e5-large-instruct`

### Usage (no prefix needed for mE5)
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('intfloat/multilingual-e5-large')
embeddings = model.encode(texts)
```

### GitHub
https://github.com/microsoft/unilm/tree/master/e5
