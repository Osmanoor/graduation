# Thesis Writing Context

## CRITICAL: Read Before Writing Any Thesis Content
**Always read `research_decisions/thesis_writing_guide.md` first** — it contains ALL of Dr. Tahani's supervisory guidelines from the 17 March 2026 meeting, including chapter structure, formatting rules, examiner perspective, and a submission checklist.

## Template Location
`University_of_Khartoum__EEE_bachelor_s_thesis_template/`

## Current Chapter Status
- **Chapter 1 (Introduction):** Template only — write AFTER Ch 2, 3, 4
- **Chapter 2 (Literature Review):** Initial draft exists (`chapter2_generated.tex`), needs major update with model descriptions and expanded theoretical background
- **Chapter 3 (Methodology):** Template only — needs full write-up
- **Chapter 4 (Results & Discussion):** Template only — needs full write-up
- **Chapter 5 (Conclusion):** Template only — write AFTER Ch 2, 3, 4

## Writing Order (from Dr. Tahani)
1. Chapter 2 → 2. Chapter 3 (zigzag with 4) → 3. Chapter 4 (zigzag with 3) → 4. Chapter 1 → 5. Chapter 5 → 6. Abstract

## Key Rules When Writing

### Source Your Claims
- **Methodology claims:** Reference `research_decisions/technical_specifications.md`
- **Decision rationale:** Reference meeting outcomes in `meetings/`
- **Experiment results:** Reference specific files in `docs/experiments/`
- **Literature:** Reference papers in `papers/`
- **Model research:** Reference files in `research_decisions/` (e.g., `jais_2_research.md`, `falcon_h1_research.md`)

### Do NOT
- Invent experiment results not in `docs/experiments/` folder
- Claim decisions that aren't in the meeting outcomes
- Add citations without corresponding paper summary in `papers/`
- Put code in the thesis body (code goes in Appendix only)
- Re-explain models/concepts in Chapter 3 that are defined in Chapter 2

### Chapter 2 Content Required
- Theoretical background: LLMs, RAG, Query Enhancement, BM25, Dense Retrieval
- Mathematical models: BM25 formula, cosine similarity, NDCG, MRR, Recall
- ALL 10+ models described: Falcon-H1, Jais-2, Qwen 2.5 3B, Qwen3-4B, ALLaM, Aya, Gemma, SILMA, Qwen 2.5 7B, Qwen3 8B, GPT-OSS
- Related Work: 20+ papers reviewed
- Initial draft: `meetings/chapter2_initial_draft.md`
- Generated version: `Chapters/chapter2_generated.tex`

### Chapter 3 — Methodology (Use Flowcharts, Not Code)
- Base on `research_decisions/technical_specifications.md`
- Only describe what was actually implemented
- Include ALL work, even negative results (ALLaM failure, GPT-OSS drop)
- Setup/configuration details go here
- Zigzag structure: each section maps to a corresponding Chapter 4 section

### Chapter 4 — Results (Zigzag with Chapter 3)
- Only include results from documented experiments in `docs/experiments/`
- Include exact metric values from experiment docs
- Engineering analysis and discussion for each result
- Do NOT extrapolate or predict results

### Formatting
- 12pt Times New Roman, 1.5 line spacing, Justified
- References: IEEE format, numbered by order of appearance [1], [2]
- Figures: numbered by chapter (Figure 2.1), caption BELOW, capital F in text
- Tables: numbered by chapter (Table 4.1), caption ABOVE
- Abbreviations: full name (ABBR) on first use, then just ABBR
- Passive voice throughout

## Experiment Results Reference (for Chapter 4)

### Baselines
| Experiment | Retriever | NDCG@10 | Recall@10 | Recall@100 | MRR |
|-----------|-----------|---------|-----------|------------|-----|
| exp_001 | mDPR (Dense) | 0.4993 | 0.6156 | 0.8407 | 0.5328 |
| exp_002 | BM25S (Sparse) | 0.4621 | 0.5964 | 0.8577 | 0.4836 |

### Query2Doc + Dense (Model Comparison)
| Experiment | Model | NDCG@10 | Recall@10 | MRR | Status |
|-----------|-------|---------|-----------|-----|--------|
| exp_003 | Qwen 2.5 3B | 0.5435 | 0.6608 | 0.5742 | Baseline QE |
| exp_005 | Falcon-H1-3B | 0.5359 | 0.6484 | 0.5681 | OK |
| exp_006 | Jais-2-8B | 0.6018 | 0.7161 | 0.6356 | **BEST** |
| exp_007 | Qwen3-4B | 0.5691 | 0.6824 | 0.6015 | 2nd best |
| exp_008 | ALLaM-7B | 0.2550 | 0.3335 | 0.2708 | DROPPED |
| exp_009 | GPT-OSS-20B | — | — | — | DROPPED |

### Query2Doc + BM25
| Experiment | Model | NDCG@10 | vs Baseline |
|-----------|-------|---------|-------------|
| exp_004 | Qwen 2.5 3B | 0.4090 | -11.5% |
| exp_005 | Falcon-H1-3B | 0.4038 | -12.6% |
| exp_006 | Jais-2-8B | 0.5122 | +10.8% |
| exp_007 | Qwen3-4B | 0.4145 | -10.3% |

*Osman's models (SILMA, Qwen 2.5-7B, Qwen3-8B, Gemma 3 4B, Aya 8B): results available in his experiment docs*

## Writing Style
- Academic but clear
- Passive voice ("The experiment was conducted..." not "We conducted...")
- Cite sources properly (BibTeX / IEEE)
- Acknowledge limitations honestly
- No code in thesis body — use flowcharts and diagrams instead
