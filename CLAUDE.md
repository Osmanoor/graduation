# Arabic RAG Query Enhancement - Research Assistant

## Source of Truth
**Always read these files before responding to project questions:**
- `RESEARCH_CONTEXT_KERNEL.md.md` - Core project context
- `TASKS.md` - Task tracking and status
- `research_decisions/open_questions.md` - Open questions
- `research_decisions/technical_specifications.md` - Architecture decisions

## Critical Rules
1. **Never invent decisions** - If not in the referenced files, say "This hasn't been decided yet"
2. **Never assume task status** - Check `TASKS.md` for actual status
3. **Distinguish clearly:**
   - CONFIRMED = explicitly decided in meetings
   - UNDER INVESTIGATION = not yet decided
   - AI SUGGESTION = my recommendation (mark clearly)
4. **When uncertain, ask** - Don't guess about project state

## Project Quick Facts (Verified)
- **Deadline:** February 15, 2026
- **Dataset:** MIRACL Arabic (MSA only)
- **Baseline:** Dense and BM25 tested SEPARATELY
- **Metrics:** Recall@10, NDCG@10, MRR
- **Resources:** Google Colab, limited API budget

## Settled (was "not decided" — all resolved by experiment)
- Retrievers: mDPR (dense) + BM25S (sparse)
- Technique: Query2Doc first, then CSQE (2 corpus + 2 blind, α=4)
- Generator: Aya Expanse 8B (CC-BY-NC — see Ch.5 licence caveat + Challenges item 8)

## Still open
- Nothing experimental. Remaining work is thesis editing (see `research_decisions/THESIS_FINAL_SUBMISSION_TASKS.md`).

## Response Format
1. State what the docs say (with file reference)
2. If docs don't cover it, say so explicitly
3. If suggesting something new, prefix with "**AI Suggestion:**"

---

## Context Loading Rules

When the user's task matches a specific domain, read the corresponding context file from `.claude/contexts/` BEFORE responding:

| User is working with... | Load this context file |
|-------------------------|----------------------|
| Files in `papers/` or analyzing papers | `.claude/contexts/paper-analysis.md` |
| Files in `experiments/` or documenting experiments | `.claude/contexts/experiment-documentation.md` |
| Python code, `src/`, baseline implementation | `.claude/contexts/baseline-implementation.md` |
| `.tex` files, thesis chapters, `University_of_Khartoum*` | `.claude/contexts/thesis-writing.md` |
| Searching for papers, literature review | `.claude/contexts/literature-search.md` |

---

## Workflow Triggers

When the user says any of these phrases, read `.claude/contexts/workflows.md` and follow the matching workflow:

| User says... | Workflow to follow |
|-------------|-------------------|
| "daily standup" or "plan my day" | Daily Research Standup |
| "complete task" or "mark task done" | Complete Task |
| "log experiment" or "document experiment" | Update Experiment Log |
| "summarize paper" or "add paper" | Summarize Paper |
| "sync decisions" or "after meeting" | Sync Decisions |
| "prepare meeting" or "supervisor meeting" | Prepare Supervisor Meeting |

---

## Model Experiment Workflow (Task 4.0b)

When Mohammed asks to work on a new model for the model comparison experiments, follow this workflow **in order**:

### Phase 1: Research (BEFORE writing any code)
1. **Read context files first:**
   - `research_decisions/model_comparison_guide.md` — per-model instructions
   - `research_decisions/llm_model_research.md` — benchmarks and rankings
   - `research_decisions/falcon_h1_research.md` — lessons learned from first model
   - `research_decisions/jais_2_research.md` — lessons learned from second model
2. **Research the model** (use Agent tool for web research):
   - Architecture: Is it a standard Transformer? (critical for batching)
   - VRAM: FP16 size, 4-bit size, overhead (SSM buffers? KV cache?)
   - Arabic benchmarks: OALL, AraGen, AMMLU scores
   - Known issues: chat template, token_type_ids, padding, gated access
   - Citations: paper/blog, developers, training details
3. **Create research doc:** `research_decisions/{model_name}_research.md` with all findings + citations

### Phase 2: Implementation
4. **GPU strategy:**
   - A100 (40GB): Try FP16 first, 4-bit fallback
   - T4 (15GB): 4-bit required for 7B+, FP16 for ≤4B
5. **Create/update notebook** in `experiments/Query_generator_{model}.ipynb`:
   - Apply batching (if standard Transformer) or single-query (if hybrid architecture)
   - Include OOM fallback handler
   - Include VRAM reporting and batch-size suggestion
   - Remove `token_type_ids` if model requires it
6. **Sanity check:** Always test first 5 queries before full run

### Phase 3: Documentation
7. **After experiment runs:** Fill in "Lessons Learned" section in notebook
8. **Create experiment doc:** `docs/experiments/exp_NNN_{model}_dense.md`
9. **Update comparison table** in `research_decisions/model_comparison_guide.md`

### Key Lessons from Previous Models
- **Falcon-H1 (exp_005):** Hybrid Mamba architecture has batching bugs — forced batch_size=1. Always check architecture type first.
- **Jais-2 (exp_006):** Standard Transformer, batching works. Must remove token_type_ids. BF16 required (Squared-ReLU overflows FP16).
- **ALLaM-7B (exp_008):** Preview/alpha model DESTROYED retrieval (-48.9%). Sentencepiece tokenizer bug leaked `▁` into output. Verify decoded output for special chars before full runs.
- **Qwen3-4B (exp_007):** Easiest model. Must disable thinking mode (`enable_thinking=False`). Never use greedy decoding. FP16 on T4/A100, batch_size=32 on A100.
- **GPT-OSS-20B (exp_009):** DROPPED. MoE architecture (32 experts) is 70x slower than dense models via BNB 4-bit. Harmony chat format requires forced-final-channel prefix to skip English reasoning. 3/5 sanity queries had severe factual hallucinations despite 100% Arabic output. English-dominant training = unreliable for Arabic QE.
- **General:** Model-specific temperature settings matter. Don't assume temp=0.7 works for all models.

### Reference Baselines — Dense Retrieval (mDPR + Query2Doc)
| Model | NDCG@10 | Recall@10 | Recall@100 | MRR |
|-------|---------|-----------|------------|-----|
| mDPR (no QE) | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| Qwen 2.5 3B (exp_003) | 0.5435 | 0.6608 | 0.8594 | 0.5742 |
| Falcon-H1-3B (exp_005) | 0.5359 | 0.6484 | 0.8531 | 0.5681 |
| **Qwen3-4B (exp_007)** | **0.5691** | **0.6824** | **0.8726** | **0.6015** |
| **Jais-2-8B (exp_006)** | **0.6018** | **0.7161** | **0.8981** | **0.6356** |
| **Aya Expanse 8B blind QE (Osman)** | **0.6164** | **0.7256** | **0.9001** | **0.6493** |
| **Aya 8B CSQE (exp_013)** | **0.5915** | **0.7073** | **0.8816** | **0.6225** |
| ~~ALLaM-7B (exp_008)~~ | ~~0.2550~~ | ~~0.3335~~ | ~~0.5465~~ | ~~0.2708~~ |
| ~~GPT-OSS-20B (exp_009)~~ | ~~DROPPED~~ | ~~DROPPED~~ | ~~DROPPED~~ | ~~DROPPED~~ |

### Reference Baselines — BM25 with Query Repetition (Exp 1.1, 2026-04-04)
| Model | n=1 (current) | Best Config | Best nDCG@10 | Δ vs n=1 |
|-------|--------------|-------------|-------------|----------|
| BM25 baseline (no QE) | 0.4621 | — | 0.4621 | — |
| **Aya Expanse 8B** | 0.5046 | **β=2** | **0.5855** | +0.0808 |
| Jais-2-8B | 0.5122 | β=2 | 0.5731 | +0.0610 |
| Qwen 2.5-7B | 0.4682 | n=5 | 0.5358 | +0.0675 |
| Qwen3-8B | 0.4459 | n=7 | 0.5328 | +0.0868 |
| Gemma 3 4B | 0.3447 | n=7 | 0.5277 | +0.1831 |
| Qwen3-4B | 0.4145 | n=7 | 0.5244 | +0.1098 |
| Qwen 2.5-3B | 0.4090 | n=5 | 0.5185 | +0.1095 |
| Falcon-H1-3B | 0.4038 | n=10 | 0.5113 | +0.1074 |
| SILMA 2B | 0.4194 | n=5 | 0.4832 | +0.0639 |

### Reference Baselines — Hybrid Fusion (Exp 1.2, 2026-04-04)
| Method | NDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25 alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| mDPR alone | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| **Hybrid CC (α=0.5)** | **0.6266** | 0.7478 | 0.9458 | **0.6577** |
| **Hybrid RRF (k=20)** | **0.6267** | **0.7597** | **0.9466** | 0.6517 |

**Strongest non-QE baseline: 0.6267 nDCG@10 (Hybrid RRF).** All QE experiments must beat this.

### Reference Baselines — CSQE (Exp 013, 2026-04-10)
| Method | NDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|---------|-----------|------------|-----|
| BM25 alone | 0.4621 | 0.5964 | 0.8577 | 0.4836 |
| Aya 8B blind QE, BM25, β=2 (exp_011) | 0.5855 | — | — | — |
| **Aya 8B CSQE, BM25 (exp_013)** | **0.6157** | **0.7447** | **0.9422** | **0.6380** |
| **Aya 8B CSQE, Dense (exp_013)** | **0.5915** | **0.7073** | **0.8816** | **0.6225** |
| Hybrid RRF k=20 (exp_012) | 0.6267 | 0.7597 | 0.9466 | 0.6517 |

CSQE config: k=5 first-pass, 2 corpus + 2 blind samples, α=4 query repetition, temp=1.0, 128 tokens/doc.

### Reference Baselines — CSQE Ablation (Exp 013c/013d, 2026-04-11)
| Method | BM25 nDCG@10 | BM25 R@10 | BM25 R@100 | BM25 MRR | Config A RRF nDCG@10 |
|--------|-------------|-----------|------------|---------|---------------------|
| 013c: Corpus-only (4c+0b, α=4) | 0.5381 | 0.6457 | 0.8790 | 0.5651 | 0.6616 |
| 013d: Blind-only (0c+4b, α=4) | 0.5752 | 0.7089 | 0.9201 | 0.6032 | 0.7082 |
| 013: CSQE 2+2 (α=4) | 0.6157 | 0.7447 | 0.9422 | 0.6380 | 0.7137 |

Alpha sweep (Config A RRF): α=1→0.7123, α=2→0.7121, α=3→0.7130, α=4→0.7137 (nearly flat).

### Error Analysis Key Numbers (2026-04-11)
- CSQE improves 56.8% of queries, regresses 16.6%, ties 26.6%; mean delta +0.1890 nDCG@10
- ⚠️ Per-query MEAN of the best system is 0.6936, NOT 0.7137. The 0.7137 headline is the corpus-level pooled evaluation. Never mix the two (ch4 Table 4.17 caption).
- Baseline for all per-query deltas = Aya blind BM25 n=1 = 0.5046 (not the hybrid, not 0.5855)
- 1st-pass IS relevant (1,061 queries, 36.6%): CSQE+Hybrid = **0.8877** nDCG@10
- 1st-pass NOT relevant (1,835 queries): CSQE+Hybrid = 0.5814 nDCG@10
- Query-length buckets — CANON is 1-3 / 4-8 / 9+ words (ch4 Tables 4.4 and 4.19). Do NOT use "<5 / >=10 words".
- Baseline (mDPR, no QE) by bucket: 1-3 words 0.345 (n=147) | 4-8 words 0.511 (n=2,495) | 9+ words 0.476 (n=254)
- CSQE+Hybrid gain by bucket: 1-3 words +0.161 (+43.6%) | 4-8 words +0.197 (+38.8%) | 9+ words +0.132 (+23.3%)
- Regressions (367): Type A 191 (52%, strong BM25 hurt by expansion), Type B 131 (36%, poisoned first-pass), Type C 45 (12%)
- ⚠️ SILMA 2B BM25 n=1: canon is **0.4277** (temp 0.1, ch4 Table 4.7). The 0.4194 in the repetition sweep is a temp-0.7 artefact — see task H1 in THESIS_FINAL_SUBMISSION_TASKS.md.

### Reference Baselines — CSQE + Hybrid Fusion (Exp 2.1, 2026-04-10)
| Method | Fusion | nDCG@10 | Recall@10 | Recall@100 | MRR |
|--------|--------|---------|-----------|------------|-----|
| Hybrid RRF k=20 (no QE) | RRF | 0.6267 | 0.7597 | 0.9466 | 0.6517 |
| B: Dense-expanded (BM25 raw + Dense+CSQE) | RRF | 0.6474 | 0.7928 | 0.9571 | 0.6578 |
| B: Dense-expanded (BM25 raw + Dense+CSQE) | CC α=0.4 | 0.6588 | 0.7851 | 0.9569 | 0.6777 |
| C: Both-expanded (BM25+CSQE + Dense+CSQE) | RRF | 0.6936 | 0.8290 | 0.9660 | 0.7037 |
| C: Both-expanded (BM25+CSQE + Dense+CSQE) | CC α=0.5 | 0.6959 | 0.8249 | 0.9647 | 0.7079 |
| A: BM25-expanded (BM25+CSQE + Dense raw) | CC α=0.6 | 0.7088 | 0.8302 | 0.9717 | 0.7268 |
| **A: BM25-expanded (BM25+CSQE + Dense raw)** | **RRF k=20** | **0.7137** | **0.8363** | **0.9734** | **0.7362** |

**Like-for-like RRF comparison (use THIS for the placement claim): 0.7137 (sparse-only) > 0.6936 (both) > 0.6474 (dense-only).**

**Best system: 0.7137 nDCG@10** (+0.0870 over hybrid, +54.5% over BM25 alone).
**Key insight:** Apply CSQE only to BM25 — Dense encoder degrades on long expanded queries.
