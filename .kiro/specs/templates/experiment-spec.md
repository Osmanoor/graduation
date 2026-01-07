# Spec: Experiment - [Experiment Name]

## Project Context
#[[file:research_decisions/technical_specifications.md]]
#[[file:research_decisions/open_questions.md]]

## Requirements

### Goal
[One sentence describing what this experiment will test]

### Hypothesis
[What do we expect to happen and why?]

### Alignment Check
- [ ] This experiment addresses a confirmed decision or open question from our docs
- [ ] Results will be comparable to our baseline metrics
- [ ] Can be completed within our resource constraints (Colab, ~6 week timeline)

### Success Criteria
| Metric | Baseline | Target |
|--------|----------|--------|
| Recall@10 | [from baseline] | [improvement or measure] |
| NDCG@10 | [from baseline] | [improvement or measure] |
| MRR | [from baseline] | [improvement or measure] |

## Design

### System Configuration
- **Dataset:** MIRACL Arabic [full / subset - specify size]
- **Retriever:** [Dense / BM25] - remember we test separately!
- **Embedding Model:** [Model name] - note if this is still under investigation
- **Query Enhancement:** [None for baseline / Technique name]

### Variables
- **Independent:** [What we're changing]
- **Dependent:** Recall@10, NDCG@10, MRR
- **Controlled:** [What stays constant]

## Tasks

### Setup
- [ ] Verify dataset is loaded correctly
- [ ] Confirm evaluation pipeline matches our standards
- [ ] Document exact configuration

### Execution
- [ ] Run on dev set first
- [ ] Log all metrics
- [ ] Save intermediate results

### Documentation
- [ ] Create `experiments/exp_XXX_[name].md` following our template
- [ ] Update `RESEARCH_CONTEXT_KERNEL.md.md` if significant finding
- [ ] Update `open_questions.md` if this resolves a question
