# LLM Model Research for Query Expansion
**Created:** 24/1/2026
**Owner:** Mohammed
**Status:** 🔄 In Progress (Research complete, decision pending Osman's results)
**Related Task:** Task 4.0
**Last Updated:** 11/2/2026

---

## Research Goal

Identify a multilingual LLM for Arabic query expansion in our MIRACL retrieval pipeline.

**Preference:** Open-source / local models (avoid API dependency where possible)

---

## Requirements (from 23/1/2026 meeting)

### Must-Have
1. **Size:** Must run on T4 GPU (15GB VRAM) — ideally 2-4B params, up to 8B with quantization
2. **Language:** Multilingual with good Arabic (MSA) support
3. **Capability:** Can follow prompts for query expansion/rewriting
4. **Truthfulness:** Generates accurate expansions (not hallucinations)

### Nice-to-Have
- Open-source (preferred over API)
- Quantization support (4-bit, 8-bit) for larger models
- Proven performance on Arabic benchmarks (OALL, AMMLU)
- Active community support

### VRAM Reference
- **FP16:** ~2 GB per 1B parameters
- **4-bit quantized:** ~0.5 GB per 1B parameters (weights only)
- **Overhead (KV cache, activations):** +2-4 GB
- T4 budget: 15GB total

| Model Size | FP16 | 4-bit | Fits T4? |
|-----------|------|-------|----------|
| 2-3B | ~6 GB + overhead | N/A (not needed) | Yes (FP16) |
| 4B | ~8 GB + overhead | N/A (not needed) | Yes (FP16) |
| 7B | ~14 GB (tight) | ~3.5 GB + overhead = ~6-8 GB | Yes (4-bit) |
| 8B | ~16 GB (no) | ~4 GB + overhead = ~6-8 GB | Yes (4-bit) |
| 9B | ~18 GB (no) | ~4.5 GB + overhead = ~7-9 GB | Yes (4-bit) |

---

## Research Approach

### Phase 1: Literature Review ✅ COMPLETE (11/2/2026)
- [x] Review HyDE paper - InstructGPT 175B, no smaller model testing
- [x] Review Query2Doc paper - text-davinci-003 175B, tested 1.3B/6.7B (failed)
- [x] Review GRF papers - GPT-3 text-davinci-002 175B, no smaller model testing
- [x] Review GaQR paper - Distilled from GPT-3.5 to Llama2-7B (works!)
- [x] Review RQ-RAG paper - Fine-tuned Llama2-7B achieves SOTA
- [x] Review Query Aug. thesis - Distilled from GPT-3.5 to Flan-T5-base (~250M)
- [x] Review Arabic RAG paper (2025) - Aya-8B > StableLM-1.6B for Arabic
- [x] Check recent Arabic NLP papers for model recommendations

### Phase 2: Model Discovery ✅ COMPLETE (11/2/2026)
- [x] Search for latest multilingual models 2024-2026
- [x] Filter by size constraints (2-8B parameters)
- [x] Check model cards for Arabic performance benchmarks (OALL)
- [x] Identify quantization options for larger models
- [x] ChatGPT Deep Research: find papers testing small models for QE
- [x] Claude Code research: comprehensive model landscape survey

### Phase 3: Testing 🔄 IN PROGRESS
- [x] **Osman: Preliminary test of Qwen 2.5 3B** — showed improvements over baseline!
- [ ] Full evaluation of top candidates in Colab
- [ ] Measure RAM usage and inference speed
- [ ] Test prompt-following capability with sample queries
- [ ] Evaluate Arabic query expansion quality

---

## Phase 1: Literature Review Findings

### Foundational Papers (2022-2023)

| Paper | Year | LLM Used | Size | Smaller Tested? | Result |
|-------|------|----------|------|----------------|--------|
| HyDE (Gao et al.) | 2022 | InstructGPT | 175B | No | Baseline method |
| Query2Doc (Wang et al.) | 2023 | text-davinci-003 | 175B | Yes (OPT-1.3B, OPT-6.7B) | **Small models failed** (noise, factual errors) |
| GRF (Mackie et al.) | 2023 | text-davinci-002 | 175B | No | — |
| GRF Dense (Mackie et al.) | 2023 | GPT-3 | 175B | No | — |

### 2024 Papers (Fine-tuning Era)

| Paper | Year | LLM Used | Size | Key Finding |
|-------|------|----------|------|-------------|
| GaQR (2024) | 2024 | GPT-3.5 → Llama2-7B | 7B (student) | Distilled 7B model works, 4-9x faster than CoT |
| RQ-RAG (2024) | 2024 | Llama2-7B (fine-tuned) | 7B | Fine-tuned 7B achieves SOTA for its size |
| Query Aug. thesis (2024) | 2024 | GPT-3.5 → Flan-T5-base | ~250M | Even ~250M works with knowledge distillation |
| Arabic RAG (2025) | 2025 | Aya-8B, StableLM-1.6B | 1.6B-8B | Aya-8B preferred for Arabic generation |

### 2024-2025 Papers from Deep Research (Query Expansion Landscape)

| Paper | Year | LLM Used | Size | Tested Non-English? | Key Result |
|-------|------|----------|------|---------------------|------------|
| CSQE (Lei et al.) | 2024 | Llama2-7B/13B/70B, GPT-3.5 | 7-70B | No | **7B gave +30% mAP** (39.1 vs 30.1 BM25 baseline). Larger better but 7B significant |
| MUGI (Zhang et al.) | 2024 | Qwen2-7B, GPT-3.5/4 | 7B+ | No | Even 23M bi-encoder works with good expansions. +18% nDCG with GPT-4 |
| PBR (Zhang et al.) | 2025 | GPT-4o-mini (~8B) | ~8B | No | +10.5% Recall@5 for personalized QE |
| Yoon et al. | 2025 | Llama3.1-8B, Mistral-7B, GPT-4o-mini, Claude-3 | 7-8B+ | No | **All LLMs improved retrieval.** 8B models close to GPT-4. Knowledge leakage insight |
| KAR (Xia et al.) | 2025 | Llama-3.1-8B, GPT-4o | 8B+ | No | 8B sufficient with structured knowledge. +36 MRR points vs HyDE |
| AQE (Yang et al.) | 2025 | Mistral-7B, Llama-3 | 7B | No | +17.8% accuracy with alignment fine-tuning |
| ThinkQE (Lei et al.) | 2025 | Qwen-14B (R1-distill) | 14B | No | Chain-of-thought QE beat GPT-4 methods |

### Key Insights from Literature

1. **All foundational QE papers used 175B models** (GPT-3 family)
2. **Query2Doc (2023) found small models insufficient** — but tested OPT-1.3B/6.7B, which are far weaker than modern models
3. **2024-2025 papers prove 7-8B models work for QE** — CSQE showed even 7B gives +30% mAP over BM25
4. **Fine-tuning/distillation enables even smaller models** (~250M with distillation)
5. **No paper tested modern 2-4B models for zero-shot Arabic QE** — this is our research gap
6. **Preliminary evidence: Qwen 2.5 3B shows improvements** on our baseline (Osman's test) — potentially filling this gap

---

## Phase 2: Open-Source Model Candidates

### Tier 1: Arabic-Specialized Models (Highest Priority)

#### 1. Falcon-H1-Arabic-3B-Instruct
**Status:** Researched — Top candidate for Arabic
| Attribute | Details |
|-----------|---------|
| **Provider** | TII (Technology Innovation Institute, UAE) |
| **Parameters** | 3B |
| **Release** | January 2026 |
| **Architecture** | Hybrid Mamba-Transformer (linear-time scalability) |
| **Context Length** | 128K tokens |
| **Arabic Focus** | Purpose-built for Arabic (MSA + dialects) |
| **OALL v2 Score** | ~62% average — **10 points ahead of all 4B competitors** |
| **Arabic STEM** | ~82% native, ~73% synthetic |
| **ArabCulture** | ~62% |
| **AraDice (Dialects)** | ~50% |
| **Fits T4?** | **Yes — FP16 (~8 GB total)** |
| **Quantization needed?** | No |
| **HuggingFace** | `tiiuae/Falcon-H1-3B-Instruct` |
| **License** | Apache 2.0 |

**Strengths:** Best Arabic scores at 3B size. Purpose-built. Fits T4 easily.
**Risks:** Very new (Jan 2026). Hybrid architecture may need specific library support.

---

#### 2. Jais-2-8B-Chat
**Status:** Researched — Best 8B Arabic model
| Attribute | Details |
|-----------|---------|
| **Provider** | MBZUAI / Inception / Cerebras |
| **Parameters** | 8B |
| **Release** | December 2025 |
| **Arabic Training** | Trained from scratch with custom Arabic-centric vocabulary |
| **Instruction Data** | ~4M Arabic + ~10M English prompt-response pairs |
| **Arabic Benchmark** | "Outperforms all other Arabic-centric models of comparable size" (Cerebras) |
| **Fits T4?** | **Yes with 4-bit quantization (~5-6 GB weights)** |
| **HuggingFace** | `inceptionai/Jais-2-8B-Chat` |
| **License** | Full open-source |

**Strengths:** Custom Arabic vocabulary. Trained from scratch on Arabic data. Best 8B Arabic model.
**Risks:** Needs 4-bit quantization for T4.

---

#### 3. SILMA Kashif-2B-Instruct
**Status:** Researched — Arabic RAG specialist
| Attribute | Details |
|-----------|---------|
| **Provider** | SILMA AI (Arabic AI startup) |
| **Parameters** | 2B |
| **Arabic Focus** | Purpose-built for Arabic RAG tasks |
| **RAGQA Score** | 0.3575 (top-performing in 3-9B range) |
| **Context Length** | 12K tokens |
| **Fits T4?** | **Yes — FP16 easily** |
| **HuggingFace** | `silma-ai/SILMA-Kashif-2B-Instruct-v1.0` |
| **License** | Open weights |

**Strengths:** Specifically designed for Arabic RAG. Very small and fast.
**Risks:** Optimized for extractive QA, may not do well at generative query expansion. Limited to 12K context.

---

### Tier 2: Strong Multilingual Models

#### 4. Qwen 2.5-3B-Instruct ⭐ PRELIMINARY TEST SHOWS IMPROVEMENTS
**Status:** **Tested by Osman — shows improvements over baseline!**
| Attribute | Details |
|-----------|---------|
| **Provider** | Alibaba (Qwen Team) |
| **Parameters** | 3B |
| **Release** | September 2024 |
| **Languages** | 29+ officially supported (Arabic included) |
| **Fits T4?** | **Yes — FP16 easily** |
| **HuggingFace** | `Qwen/Qwen2.5-3B-Instruct` |
| **License** | Apache 2.0 |

**Strengths:** Already tested on our pipeline with positive results. Well-documented. Apache 2.0.
**Key fact:** Osman's preliminary test shows improvements over our mDPR baseline — details pending.

---

#### 5. Qwen 2.5-7B-Instruct (4-bit quantized)
**Status:** Researched — strongest general multilingual at 7B
| Attribute | Details |
|-----------|---------|
| **Provider** | Alibaba (Qwen Team) |
| **Parameters** | 7B |
| **Release** | September 2024 |
| **Languages** | 29+ (Arabic included) |
| **MMLU** | 74.2 |
| **Fits T4?** | **Yes with 4-bit (~6-8 GB total)** |
| **Pre-quantized** | `Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4` and `unsloth/Qwen2.5-7B-Instruct-bnb-4bit` |
| **Colab Tested?** | Yes — Unsloth provides free Colab T4 notebooks |
| **HuggingFace** | `Qwen/Qwen2.5-7B-Instruct` |
| **License** | Apache 2.0 |

**Strengths:** Strong Arabic baseline on OALL. Pre-quantized versions readily available. Well-tested on Colab T4.
**Risks:** Needs quantization. May be slower than 3B for 2,896 queries.

---

#### 6. Qwen3-4B
**Status:** Researched — newer generation
| Attribute | Details |
|-----------|---------|
| **Provider** | Alibaba (Qwen Team) |
| **Parameters** | 4B (3.6B non-embedding) |
| **Release** | May 2025 |
| **Languages** | 119 languages (3x coverage of Qwen 2.5) |
| **Performance** | Matches Qwen 2.5-7B in many benchmarks |
| **MMLU-Redux** | 83.7 |
| **Fits T4?** | **Yes — FP16** |
| **HuggingFace** | `Qwen/Qwen3-4B` |
| **License** | Apache 2.0 |

**Strengths:** Newer generation. 119 language support. Matches 7B quality.
**Risks:** Arabic-specific AMMLU scores not yet published.

---

#### 7. Gemma 3 4B-IT
**Status:** Researched
| Attribute | Details |
|-----------|---------|
| **Provider** | Google DeepMind |
| **Parameters** | 4B |
| **Release** | March 2025 |
| **Languages** | 140+ languages (Arabic included) |
| **Context Length** | 128K tokens |
| **Fits T4?** | **Yes — FP16** |
| **HuggingFace** | `google/gemma-3-4b-it` |
| **License** | Gemma Terms of Use |

**Strengths:** 140+ languages. 128K context. Multimodal.
**Weaknesses:** Weakest Arabic performance among candidates. OALL ~10 points below Falcon-H1-Arabic-3B.

---

#### 8. Phi-4 Mini
**Status:** Researched
| Attribute | Details |
|-----------|---------|
| **Provider** | Microsoft |
| **Parameters** | 3.8B |
| **Release** | February 2025 |
| **Languages** | 23 languages (Arabic included) |
| **Context Length** | 128K tokens |
| **Fits T4?** | **Yes — FP16** |
| **HuggingFace** | `microsoft/Phi-4-mini-instruct` |
| **License** | MIT |

**Strengths:** MIT license. 128K context. Good general performance.
**Weaknesses:** Primarily English-trained. OALL ~10 points below Falcon-H1-Arabic-3B.

---

### Tier 3: Larger Models (Require Quantization)

#### 9. Aya Expanse 8B
| Attribute | Details |
|-----------|---------|
| **Provider** | Cohere Labs |
| **Parameters** | 8B |
| **Languages** | 23 (Arabic explicitly optimized) |
| **Performance** | 83.9% win rate vs Llama-3.1-8B |
| **Fits T4?** | Yes with 4-bit quantization |
| **HuggingFace** | `CohereLabs/aya-expanse-8b` |
| **License** | CC-BY-NC-4.0 (non-commercial) |

**Note:** Non-commercial license may be restrictive.

#### 10. ALLaM-7B
| Attribute | Details |
|-----------|---------|
| **Provider** | SDAIA (Saudi Arabia) |
| **Parameters** | 7B |
| **Training** | 5.2 trillion tokens (Arabic + English) |
| **Fits T4?** | Yes with 4-bit quantization |
| **HuggingFace** | `ALLaM-AI/ALLaM-7B-Instruct-preview` |
| **License** | TBD |

**Note:** Preview status. Limited community testing.

### Not Recommended

| Model | Reason |
|-------|--------|
| **Llama 3.2 1B/3B** | Arabic NOT officially supported. Research shows it "lags behind" for Arabic |
| **AceGPT v1.5 13B** | Based on old LLaMA 2. 13B too heavy. Superseded by newer models |
| **SmolLM3 3B** | Arabic only secondary in training data |
| **Gemma Translator 270M** | Too specialized for translation. Too small for generative expansion |
| **GPT-OSS 20B** | Too large even with quantization. Unknown Arabic support |

---

## Phase 2: API Options (Backup / Comparison)

For processing ~2,896 queries (~580K total tokens):

### Free Tier APIs

| Provider | Model | Arabic Quality | Cost | Rate Limits | Feasibility |
|----------|-------|---------------|------|-------------|-------------|
| **Google Gemini** | 2.0 Flash / 1.5 Flash | Excellent | **$0** | Free tier generous | Easily handles 2,896 queries |
| **Groq** | Qwen3-32B, Llama4-17B | Very Good (via Qwen) | **$0** | ~300K tok/min, 1000 RPM | Done in minutes |
| **OpenRouter** | Llama-3.3-70B, various | Moderate | **$0** | Community-hosted | Many free models available |

### Very Cheap APIs (<$5 total)

| Provider | Model | Arabic Quality | Cost (580K tokens) | Notes |
|----------|-------|---------------|-------------------|-------|
| **Cohere** | Aya-23-8B / Aya-32B | Excellent (101 langs) | **~$1-2** | Purpose-built multilingual |
| **Together AI** | Various (Llama, Qwen, Gemma) | Varies | **~$0.50** | Flexible model selection |
| **DeepSeek** | V3.2 | Weak Arabic | **~$0.30** | Primarily Chinese/English — not recommended for Arabic |
| **Qwen/DashScope** | Qwen3, Qwen-2.5 | Very Good | **~$0.03-0.04/1K** | Free daily quota may exist |

### API Assessment

**Best free:** Google Gemini 2.0 Flash — free, excellent Arabic, no GPU needed
**Best cheap:** Cohere Aya — $1-2 total, purpose-built multilingual, 101 languages
**Best for speed:** Groq — free, Qwen3-32B, processes in minutes
**Not recommended:** DeepSeek (weak Arabic), HuggingFace Inference (low free limits)

---

## Comparative Summary

### Arabic-Focused Models (Open Source, Fits T4)

| Model | Params | Arabic Score (OALL) | Fits T4 (FP16)? | Fits T4 (4-bit)? | License | Best For |
|-------|--------|-------------------|-----------------|-------------------|---------|----------|
| **Falcon-H1-Arabic-3B** | 3B | ~62% (best at ≤4B) | Yes | N/A | Apache 2.0 | Best Arabic at 3B |
| **Jais-2-8B-Chat** | 8B | Best 8B Arabic | No | Yes (~5-6 GB) | Open source | Best Arabic at 8B |
| **SILMA Kashif-2B** | 2B | Good (RAG-optimized) | Yes | N/A | Open | Arabic RAG extraction |
| **Qwen2.5-3B** ⭐ | 3B | Good (29+ langs) | Yes | N/A | Apache 2.0 | **Already tested, shows improvement** |
| **Qwen2.5-7B** | 7B | Mid-high 50s | No | Yes (~6-8 GB) | Apache 2.0 | Strong multilingual |
| **Qwen3-4B** | 4B | Good (119 langs) | Yes | N/A | Apache 2.0 | Latest generation |
| **Gemma 3 4B** | 4B | Low 50s (weakest) | Yes | N/A | Gemma TOU | General multilingual |
| **Phi-4 Mini** | 3.8B | ~52% | Yes | N/A | MIT | General purpose |

### Ranking by Arabic Quality (from benchmarks + research)

1. **Jais-2-8B** — Best overall Arabic model at 8B (needs 4-bit)
2. **Falcon-H1-Arabic-3B** — Best at ≤4B size, purpose-built Arabic
3. **Qwen2.5-7B** — Strong multilingual (needs 4-bit)
4. **Qwen2.5-3B** — Good multilingual, already tested on our pipeline ⭐
5. **Qwen3-4B** — Newer generation, broad language support
6. **SILMA Kashif-2B** — RAG-optimized but may be too extractive-focused
7. **Phi-4 Mini** — Decent but Arabic is secondary
8. **Gemma 3 4B** — Weakest for Arabic among candidates

---

## Testing Protocol

### Test 1: Memory Fit
- [ ] Load model in Colab T4 GPU
- [ ] Measure RAM usage
- [ ] Verify model loads successfully

### Test 2: Inference Speed
- [ ] Generate expansions for 10 sample queries
- [ ] Measure time per query
- [ ] Calculate throughput (queries/minute)

### Test 3: Prompt Following
- [ ] Test with simple expansion prompt
- [ ] Test with complex expansion prompt
- [ ] Evaluate if model follows instructions

### Test 4: Arabic Quality
- [ ] Test with Arabic queries (short and long)
- [ ] Evaluate expansion quality (relevance, accuracy)
- [ ] Check for hallucinations

### Test 5: Integration
- [ ] Test integration with Dense baseline
- [ ] Run on sample queries
- [ ] Verify end-to-end pipeline works

---

## Sample Queries for Testing

### Short Queries (Information Poverty — our main target)
1. "الذكاء الاصطناعي" (Artificial Intelligence)
2. "القاهرة" (Cairo)
3. "كرة القدم" (Football)

### Medium Queries
1. "ما هي عاصمة مصر؟" (What is the capital of Egypt?)
2. "كيف يعمل الذكاء الاصطناعي؟" (How does AI work?)

### Long Queries
1. "أريد معلومات عن تاريخ الحضارة المصرية القديمة وأهم الإنجازات" (I want information about ancient Egyptian civilization history and major achievements)

---

## Decision Criteria

### Primary Criteria (Must Pass)
1. Fits on T4 GPU (15GB VRAM)
2. Inference speed < 5 seconds per query
3. Follows expansion prompts correctly
4. Good Arabic support (coherent output, not gibberish)

### Secondary Criteria (Nice to Have)
1. Open-source with permissive license
2. Expansion quality (relevance, accuracy)
3. No hallucinations
4. Good documentation and community

---

## Fine-tuning Consideration

**Status:** Deferred ("to be determined later")

**Potential Approach:**
1. Use AI Studio to generate correct query expansion examples
2. Create training dataset (original query → expanded query)
3. Fine-tune small model on this dataset
4. Evaluate improvement

**When to Consider:**
- If zero-shot prompting quality is insufficient
- If we have time after initial experiments
- Literature shows fine-tuned 7B matches GPT-3.5 (GaQR, RQ-RAG)

---

## Research Log

### 24/1/2026 - Research Started
- Created research document
- Defined requirements and candidate models
- Set up testing protocol

### 11/2/2026 - Literature Review Complete
- Reviewed all 8 relevant papers in our collection
- Key finding: ALL foundational QE papers used 175B models (GPT-3 family)
- Query2Doc is the ONLY paper that tested smaller models (1.3B, 6.7B) — both failed
- BUT: 2024 papers show fine-tuned 7B models work (GaQR, RQ-RAG)
- AND: Knowledge distillation can shrink to ~250M (Flan-T5-base)
- Critical gap: No paper tests modern 2-4B models for zero-shot Arabic QE

### 11/2/2026 - Model Discovery Complete (Claude Code + ChatGPT Deep Research)
- Claude Code: Comprehensive survey of 2024-2026 model landscape
- ChatGPT Deep Research: Found 7 new QE papers (CSQE, MUGI, PBR, Yoon, KAR, AQE, ThinkQE)
- All 7 papers confirm: modern 7-8B models give significant QE gains
- CSQE specifically: Llama2-7B gave +30% mAP over BM25 baseline
- Identified top open-source candidates: Falcon-H1-Arabic-3B, Jais-2-8B, Qwen 2.5 series
- Mapped all API options with pricing
- Deep Research findings fully aligned with Claude Code research

### 11/2/2026 - Preliminary Test Results (Osman)
- Osman tested Qwen 2.5 3B on our pipeline
- **Result: Shows improvements over baseline!**
- Details pending — need to fetch Osman's work for full analysis
- This is significant: answers our open question about whether modern 3B models can do zero-shot Arabic QE

---

## References

### Papers Reviewed (Foundational)
| Paper | Citation | URL |
|-------|----------|-----|
| HyDE | Gao et al., 2022 | "Precise Zero-Shot Dense Retrieval without Relevance Labels" |
| Query2Doc | Wang et al., 2023 | "Query Expansion with Large Language Models" |
| GRF | Mackie et al., 2023 | "Generative Relevance Feedback with Large Language Models" |
| GaQR | 2024 | Distillation from GPT-3.5 to Llama2-7B |
| RQ-RAG | 2024 | Fine-tuned Llama2-7B query refinement |

### Papers from Deep Research (2024-2025 QE Landscape)
| Paper | Citation | URL |
|-------|----------|-----|
| CSQE | Lei et al., 2024 | Corpus-Steered Query Expansion |
| PBR | Zhang et al., 2025 | [arxiv.org/html/2510.08935v1](https://arxiv.org/html/2510.08935v1) |
| Yoon et al. | 2025 | [arxiv.org/html/2504.14175v1](https://arxiv.org/html/2504.14175v1) |
| MUGI | Zhang et al., 2024 | [aclanthology.org/2024.findings-emnlp.103](https://aclanthology.org/2024.findings-emnlp.103.pdf) |
| KAR | Xia et al., 2025 | [aclanthology.org/2025.naacl-long.216](https://aclanthology.org/2025.naacl-long.216.pdf) |
| AQE | Yang et al., 2025 | [ar5iv.labs.arxiv.org/html/2507.11042](https://ar5iv.labs.arxiv.org/html/2507.11042) |
| ThinkQE | Lei et al., 2025 | [aclanthology.org/2025.findings-emnlp.965](https://aclanthology.org/2025.findings-emnlp.965.pdf) |

### Model Resources
| Resource | URL |
|----------|-----|
| Falcon-H1-Arabic Blog | [huggingface.co/blog/tiiuae/falcon-h1-arabic](https://huggingface.co/blog/tiiuae/falcon-h1-arabic) |
| Open Arabic LLM Leaderboard | [huggingface.co/spaces/OALL/Open-Arabic-LLM-Leaderboard](https://huggingface.co/spaces/OALL/Open-Arabic-LLM-Leaderboard) |
| Jais-2 Blog | [cerebras.ai/blog/jais2](https://www.cerebras.ai/blog/jais2) |
| SILMA Kashif | [silma.ai](https://silma.ai/) |
| SILMA RAGQA Benchmark | [huggingface.co/blog/karimouda/silma-ragqa-benchmark-v10](https://huggingface.co/blog/karimouda/silma-ragqa-benchmark-v10) |
| Gemini API Pricing | [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| Groq Models | [console.groq.com/docs/models](https://console.groq.com/docs/models) |
| Cohere Pricing | [cohere.com/pricing](https://cohere.com/pricing) |
| OpenRouter Free Models | [openrouter.ai/collections/free-models](https://openrouter.ai/collections/free-models) |

---

## Next Steps

1. **Fetch Osman's Qwen 2.5 3B results** — understand what he tested, metrics achieved, prompt used
2. **Decide model strategy** — based on Osman's results + this research
3. **Scale testing** — test top 2-3 candidates side by side
4. **Finalize decision** — update this doc, TASKS.md, RESEARCH_CONTEXT_KERNEL.md.md

---

## Final Decision

**Selected Model:** Pending — awaiting Osman's Qwen 2.5 3B results

**Top Candidates (Open Source):**
1. Qwen 2.5 3B ⭐ (already showing improvements)
2. Falcon-H1-Arabic-3B (best Arabic benchmarks)
3. Jais-2-8B-Chat (best 8B Arabic, needs 4-bit)

**Backup (API):**
1. Google Gemini 2.0 Flash (free tier)
2. Groq Qwen3-32B (free tier)
3. Cohere Aya (~$1-2)

**Next Task:** Fetch Osman's work → Finalize decision → Task 4.1 Implementation
