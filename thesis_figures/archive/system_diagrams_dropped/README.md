# Archived System Diagrams

**Date:** 2026-06-01
**Reason:** Osman's review feedback — "the diagrams are actually a lot and clear concepts should not have diagrams."

These five figures were dropped from the thesis on the principle that the underlying concepts are widely known to IR examiners and can be communicated in prose with no loss. Sources and PDFs are preserved here in case we want to re-introduce any of them.

## What was dropped (4 figures)

| Figure | Title | Why archived |
|--------|-------|--------------|
| Fig 2.2 | Query Enhancement taxonomy | Coverage overlaps with Table 2.1 (Reviewed QE papers) and the §2.4 prose. The text already positions Query2Doc + CSQE in the literature. |
| Fig 2.3 | Dense vs Sparse retrieval | Standard IR primer — readers of this thesis know both families. The complementary-strengths point is two sentences. |
| Fig 3.2 | MIRACL dataset structure | Two paragraphs of §3.2 prose convey the same: 2,061,414 passages, 2,896 dev queries, 29,197 qrels, TREC run format. No need to draw cylinders. |
| Fig 3.6 | BM25 query repetition mechanism | The mechanism is a one-line equation (q^n ⊕ pdoc); Fig 4.7 already shows the empirical sweep across all 9 models. The diagram is redundant. |

**Note:** Fig 2.1 (RAG architecture) was *initially* archived in this batch but was **restored** after Osman's FIGURE_NOTES (file: `FIGURE_NOTES_MOHAMMED.md`, despite the filename it's Osman's review) §1 was read — Osman wants Fig 2.1 kept *and* a companion figure added showing where the QE layer sits in the RAG pipeline.

## Surviving system diagrams (7)

The diagrams that remain in `../../system_diagrams/` are all methodology- or contribution-specific, with parameters that would be awkward to convey in prose:

- **Fig 3.1** — End-to-end pipeline (the thesis map)
- **Fig 3.3** — BM25S indexing flow (specific k₁=0.9, b=0.4 + Arabic tokenizer detail)
- **Fig 3.4** — mDPR encoding flow (specific encoder name, batch params, FAISS detail)
- **Fig 3.5** — Query2Doc generation (prompt template inline)
- **Fig 3.7** — Hybrid fusion CC + RRF (two equations side-by-side)
- **Fig 3.8** — CSQE pipeline (the main methodology contribution)
- **Fig 3.9** — Best system architecture (pairs with Fig 4.11)

## How to restore one if needed

```bash
# Move the .tex back
mv archive/system_diagrams_dropped/fig_X_Y_*.tex system_diagrams/

# Recompile + place in output/
cd system_diagrams/
xelatex fig_X_Y_*.tex
cp fig_X_Y_*.pdf ../output/pdf/
pdftoppm -png -r 200 fig_X_Y_*.pdf ../output/png/fig_X_Y_*
cd ../output/png && for f in fig_X_Y_*-1.png; do mv "$f" "${f%-1.png}.png"; done
```

Then update the master `../../README.md` registry to remove the ARCHIVED tag for that figure.
