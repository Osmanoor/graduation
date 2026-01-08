# Swan and ArabicMTEB: Arabic-Centric Embedding Models
**arXiv:** 2411.01192  
**Date:** November 2024  
**Authors:** Bhatia et al. (UBC-NLP)

---

## Summary

Introduces Swan, a family of Arabic-centric embedding models, and ArabicMTEB, a comprehensive benchmark for Arabic text embeddings.

## Key Contributions

1. **Swan Models:**
   - Swan-Small (164M params, based on ARBERTv2)
   - Swan-Large (7.2B params, based on ArMistral)
   
2. **ArabicMTEB Benchmark:**
   - 94 datasets across 8 tasks
   - Covers MSA + dialects
   - Domain-specific and cultural evaluation

## Results Relevant to Our Project

### Overall Performance (Table 5)
| Model | Retrieval | STS | Avg |
|-------|-----------|-----|-----|
| Swan-Large | 65.63 | 59.10 | 62.45 |
| Me5-large | 64.01 | 59.45 | 61.65 |
| Swan-Small | 58.42 | 59.34 | 57.33 |

### Domain-Specific (Table 7)
Swan-Large achieves 82.49 avg vs OpenAI's 82.20 at 13x lower cost.

### Dialectal (Table 6)
Swan-Large: 70.45 avg (SOTA for dialectal Arabic)

## Training Data

- MIRACL (our primary dataset!)
- mMARCO Arabic
- ORCA datasets
- Synthetic MSA and dialectal data

## Relevance to Our Project

1. **Swan trained on MIRACL** - directly applicable
2. **Dialectally aware** - future-proofing
3. **Open source** - reproducible research
4. **Cost-effective** - fits our budget constraints

## Links

- GitHub: https://github.com/UBC-NLP/swan
- Paper: https://arxiv.org/abs/2411.01192

---

**Added to literature:** January 8, 2026
