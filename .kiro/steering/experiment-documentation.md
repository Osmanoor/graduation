---
inclusion: fileMatch
fileMatchPattern: "**/exp_*.md,**/experiment*.md,experiments/**/*.md"
---

# Experiment Documentation Standards

## Required Structure

Every experiment doc MUST have:

```markdown
# Experiment [NUMBER]: [Title]
**Date:** [YYYY-MM-DD]
**Status:** [Planning | Running | Complete | Failed]
**Owner:** [Mohammed | Osman | Both]

## What We Tested
[One paragraph: what system configuration, what we measured]

## Setup
- **Dataset:** MIRACL Arabic - [full | subset of X passages]
- **Retriever:** [Dense | BM25] (we test separately!)
- **Embedding Model:** [Name] (if Dense)
- **Hardware:** Google Colab [Free | Pro]

## Results

| Metric | Value |
|--------|-------|
| Recall@10 | X.XXX |
| NDCG@10 | X.XXX |
| MRR | X.XXX |

## What We Learned
[Key observations, what worked, what didn't]

## Next Steps
[What to try next based on these results]

## Code/Notebook
[Link to Colab notebook or code file]
```

## Rules

1. **Never fabricate metrics** - Only record actual measured values
2. **Always note subset size** - If not full dataset, document exactly how many passages/queries
3. **Document failures** - Failed experiments are valuable data
4. **Link to code** - Every experiment needs reproducible code reference
