"""Generate the BM25 twin of Figure 4.3 (fig_4_5_models_bar_v1) for the defence deck.

Run:  python thesis_figures/gen_fig_bm25_bar.py

Why this script exists (defence prep, 2026-08-15):

Chapter 4 has a dense model-comparison figure (Figure 4.3, fig_4_5_models_bar_v1)
but reports the BM25 sweep as a table only (Table 4.6, sec:res_mc_bm25). The
defence needs the two side by side on one slide: every model clears the dashed
baseline on dense, and most fall below it on BM25. That contrast is the whole
Query2Doc finding and it does not survive being read off a table.

Design is copied from regen_fig_4_3_dense_bar.py deliberately -- same figsize,
same per-model colours, same dashed baseline rule -- so the two charts read as
one pair. Only the data column and the baseline value differ.

Column: n1_ndcg10, i.e. Query2Doc with NO query repetition. That is the correct
column for this slide: the repetition fix is the *next* slide's story, and using
best_ndcg10 here would erase the degradation the slide exists to show.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "notebooks"))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from _helpers import DATA_RAW, color_for_model, save_fig  # noqa: E402

BASELINE_ROW = "BM25 baseline (no QE)"


def main() -> None:
    bm25 = pd.read_csv(DATA_RAW / "model_comparison_bm25.csv")
    baseline = float(bm25.loc[bm25.model == BASELINE_ROW, "n1_ndcg10"].iloc[0])

    active = bm25[bm25.model != BASELINE_ROW].copy()
    active = active.sort_values("n1_ndcg10", ascending=False).reset_index(drop=True)

    assert len(active) == 9, f"expected 9 Query2Doc models, got {len(active)}"

    n_above = int((active.n1_ndcg10 > baseline).sum())
    n_below = len(active) - n_above
    assert n_below == 6, f"expected 6 models below baseline, got {n_below}"

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(active.model, active.n1_ndcg10,
           color=[color_for_model(m) for m in active.model], edgecolor="black")
    ax.axhline(baseline, color="#1f6f8a", linestyle="--", linewidth=1,
               label=f"BM25 baseline ({baseline:.3f})")
    ax.set_ylabel("NDCG@10")
    ax.set_ylim(0, max(active.n1_ndcg10) * 1.1)
    ax.legend(loc="upper right")
    plt.xticks(rotation=30, ha="right")

    save_fig(fig, "fig_4_5b_models_bar_bm25_v1")
    print(f"  above baseline: {n_above}   below baseline: {n_below}")
    print("  bars:", ", ".join(active.model))


if __name__ == "__main__":
    main()
