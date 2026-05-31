# System Diagrams — all TikZ

**Updated 2026-05-31:** all 12 system diagrams (Figs 2.1, 2.2, 2.3, 3.1–3.9) are now written in TikZ with `\documentclass{standalone}`. Excalidraw sources removed — TikZ produces submission-ready vector PDFs without manual polish.

## File list

| Source | Output |
|--------|--------|
| `fig_2_1_rag_arch.tex` | `../output/pdf/fig_2_1_rag_arch.pdf` |
| `fig_2_2_qe_taxonomy.tex` | `../output/pdf/fig_2_2_qe_taxonomy.pdf` |
| `fig_2_3_dense_vs_sparse.tex` | `../output/pdf/fig_2_3_dense_vs_sparse.pdf` |
| `fig_3_1_pipeline.tex` | `../output/pdf/fig_3_1_pipeline.pdf` |
| `fig_3_2_miracl.tex` | `../output/pdf/fig_3_2_miracl.pdf` |
| `fig_3_3_bm25s.tex` | `../output/pdf/fig_3_3_bm25s.pdf` |
| `fig_3_4_mdpr.tex` | `../output/pdf/fig_3_4_mdpr.pdf` |
| `fig_3_5_query2doc.tex` | `../output/pdf/fig_3_5_query2doc.pdf` |
| `fig_3_6_repetition.tex` | `../output/pdf/fig_3_6_repetition.pdf` |
| `fig_3_7_hybrid.tex` | `../output/pdf/fig_3_7_hybrid.pdf` |
| `fig_3_8_csqe.tex` | `../output/pdf/fig_3_8_csqe.pdf` |
| `fig_3_9_best_system.tex` | `../output/pdf/fig_3_9_best_system.pdf` |

## How to rebuild

```bash
cd system_diagrams/
for f in fig_*.tex; do xelatex -interaction=nonstopmode "$f"; done
cp *.pdf ../output/pdf/
rm -f *.aux *.log *.out
```

Or compile a single file: `xelatex fig_3_1_pipeline.tex`.

## Toolchain

- `xelatex` from MiKTeX or TeX Live (verified MiKTeX works on Windows).
- TikZ libraries used across files: `positioning`, `arrows.meta`, `calc`, `shapes.geometric`, `fit`, `backgrounds`.
- `amsmath` loaded in `fig_3_7_hybrid.tex` for `\text` in the fusion equations.

## Embedding in the thesis

Two equivalent options per figure:

1. **`\includegraphics`** (recommended): the simplest path. Drop a `\includegraphics{output/pdf/fig_X_Y_*.pdf}` inside a `\begin{figure}` block in the chapter `.tex`.
2. **Inline TikZ**: copy just the `\begin{tikzpicture}...\end{tikzpicture}` block (without `\documentclass`) into the chapter, paste alongside the figure's `\caption`. Requires the chapter's preamble to load the same TikZ libraries.

Option 1 is safer because the standalone PDFs are deterministic — no risk of library conflicts inside the thesis preamble.

## Style notes

- Black-and-white safe (grayscale fills via `fill=black!N`).
- All boxes use 2pt rounded corners for visual consistency with the data figures rendered by matplotlib.
- Arrow style is `Stealth[length=2.5mm]` throughout.
- Font defaults to LaTeX serif; the standalone class crops to the diagram bounding box, so when embedded in the thesis the font picks up the document body font automatically.
