"""Regenerate Figure 4.7 (fig_4_7_repetition_v1/v2/v3) — BM25 query-repetition sweep.

Run:  python thesis_figures/regen_fig_4_7_repetition.py

Why this script exists (task H1, 2026-08-08):

  The committed render plotted SILMA 2B from the temperature-**0.7** expansions
  while every other model — and Table 4.7, and Ch.3 Table 3.2 — used temperature
  **0.1**. The Exp 1.1 sweep had loaded `silma_2b_temp07.pkl` by mistake. SILMA's
  eight configurations were re-run from `silma_2b_temp01.pkl` (see
  `arabic-rag-query-enhancement/results/exp_11b_silma_temp01/`), and
  `data/raw/exp11_ndcg10.csv` now carries those values. This script re-renders
  the figure from the corrected CSV so it agrees with Table~\\ref{tab:bm25_repetition}
  in Appendix B. SILMA's optimum moved n=5 -> n=7 as a result.

  It exists as a standalone script rather than a notebook re-run because
  notebook 03 also emits fig_4_5 and fig_4_8, and fig_4_8 has since been
  superseded by `regen_fig_4_9_gains.py` (which fixes a join that silently
  dropped SILMA). Re-running the whole notebook would undo that fix.

  Fig 4.8 needs no change here: it reads only the `n1_ndcg10` column, which was
  already the correct temperature-0.1 value of 0.4277.

Plotting logic is otherwise identical to notebook 03 cell 12.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "notebooks"))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from _helpers import DATA_RAW, color_for_model, save_fig  # noqa: E402

N_COLS = ["n=1", "n=3", "n=5", "n=7", "n=10"]
BETA_COLS = ["β=2", "β=4", "β=6"]
X_N = [1, 3, 5, 7, 10]


def main() -> None:
    rep = pd.read_csv(DATA_RAW / "exp11_ndcg10.csv")
    bm25 = pd.read_csv(DATA_RAW / "model_comparison_bm25.csv")
    baseline = float(
        bm25.loc[bm25.model == "BM25 baseline (no QE)", "n1_ndcg10"].iloc[0]
    )

    models = [m for m in rep["Model"] if m != "BM25 baseline (no QE)"]
    assert len(models) == 9, f"expected 9 models, got {len(models)}"

    # Guard the exact defect this script was written to fix: SILMA must be on
    # the temperature-0.1 numbers, whose n=1 matches Table 4.7 (0.4277).
    silma_n1 = float(rep.loc[rep.Model == "SILMA 2B", "n=1"].iloc[0])
    assert abs(silma_n1 - 0.4277) < 5e-5, (
        f"SILMA n=1 is {silma_n1:.4f}, expected 0.4277 (temp 0.1). "
        "The CSV has reverted to the temperature-0.7 row."
    )

    # v1 -- n sweep multi-line (this is the variant the thesis includes)
    fig, ax = plt.subplots(figsize=(7, 4))
    for m in models:
        ys = rep.loc[rep.Model == m, N_COLS].values.flatten()
        ax.plot(X_N, ys, marker="o", label=m, alpha=0.85, linewidth=1.5,
                color=color_for_model(m))
    ax.axhline(baseline, color="#1f6f8a", linestyle=":", linewidth=1,
               label="BM25 baseline")
    ax.set_xlabel("n (query repetitions)")
    ax.set_ylabel("NDCG@10")
    ax.legend(loc="lower right", fontsize=7, ncol=2)
    save_fig(fig, "fig_4_7_repetition_v1")

    # v2 -- n sweep + beta markers
    fig, ax = plt.subplots(figsize=(7, 4))
    for m in models:
        ys = rep.loc[rep.Model == m, N_COLS].values.flatten()
        ax.plot(X_N, ys, marker="o", label=m, alpha=0.85, linewidth=1.5,
                color=color_for_model(m))
        bs = rep.loc[rep.Model == m, BETA_COLS].values.flatten()
        ax.scatter([12.5, 13.5, 14.5], bs, marker="s", s=22, alpha=0.7)
    ax.axvline(11, color="#8c8c8c", linewidth=0.5, linestyle=":")
    ax.set_xticks([1, 3, 5, 7, 10, 12.5, 13.5, 14.5])
    ax.set_xticklabels(["n=1", "n=3", "n=5", "n=7", "n=10",
                        "β=2", "β=4", "β=6"])
    ax.set_ylabel("NDCG@10")
    ax.legend(loc="lower right", fontsize=7, ncol=2)
    save_fig(fig, "fig_4_7_repetition_v2")

    # v3 -- heatmap
    all_cols = N_COLS + BETA_COLS
    M = rep.loc[rep.Model.isin(models), ["Model"] + all_cols].set_index("Model")
    fig, ax = plt.subplots(figsize=(7, 4))
    im = ax.imshow(M.values, cmap="gray_r", aspect="auto", vmin=0.3, vmax=0.6)
    ax.set_xticks(range(len(all_cols)))
    ax.set_xticklabels(all_cols)
    ax.set_yticks(range(len(M.index)))
    ax.set_yticklabels(M.index)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if v > 0.5 else "black")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label="NDCG@10")
    save_fig(fig, "fig_4_7_repetition_v3_heat")

    # Regenerate the derived LaTeX table from the same corrected CSV.
    # Not \input by the thesis (Table 4.12 is hand-maintained in chapter4.tex);
    # kept in step so the generated artefact does not go stale.
    out = Path(__file__).resolve().parent / "output" / "pdf" / "table_4_3.tex"
    out.write_text(
        bm25.to_latex(index=False, float_format="%.4f", column_format="lccccc"),
        encoding="utf-8",
    )
    print(f"  saved: {out.name}")


if __name__ == "__main__":
    main()
