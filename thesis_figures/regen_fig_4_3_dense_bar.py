"""Regenerate Figure 4.3 (fig_4_5_models_bar_v1) — dense NDCG@10 across models.

Run:  python thesis_figures/regen_fig_4_3_dense_bar.py

Why this script exists (task E1b, decision of the 2026-08-06 review meeting):

The chart carried a tenth bar, "Aya 8B CSQE" (0.5915), which does not belong in
it. The figure is captioned as the Query2Doc pipeline and accompanies Table 4.8,
the Query2Doc dense leaderboard; the CSQE result is a different technique,
reported separately in Section 4.8, and it appears nowhere in that table. A
reader comparing figure against table found ten bars and nine rows.

Root cause: in `notebooks/03_model_comparison.ipynb` cell 6 the exclusion list
was `['mDPR (no QE)', 'ALLaM-7B']`, while cells 8 and 14 — which build the other
model-comparison figures — correctly exclude `'Aya 8B CSQE'` as well. The
notebook cell has been corrected to match; this script is the authoritative
regenerator and asserts the bar count so the row cannot creep back in.

ALLaM-7B remains excluded, as it always was: it is the dropped model, listed in
Table 4.8 under a separate "Dropped model" rule, and its -48.9% result would
compress the scale of every other bar.

Design is unchanged from the committed figure (7x4, per-model thesis colours,
dashed baseline rule) so only the spurious bar disappears.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "notebooks"))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from _helpers import DATA_RAW, color_for_model, save_fig  # noqa: E402

# Rows that are not Query2Doc model results and must never be plotted here.
EXCLUDE = ["mDPR (no QE)", "ALLaM-7B", "Aya 8B CSQE"]


def main() -> None:
    dense = pd.read_csv(DATA_RAW / "model_comparison_dense.csv")
    baseline = float(dense.loc[dense.model == "mDPR (no QE)", "ndcg_10"].iloc[0])

    active = dense[~dense.model.isin(EXCLUDE)].copy()
    active = active.sort_values("ndcg_10", ascending=False).reset_index(drop=True)

    assert len(active) == 9, f"expected 9 Query2Doc models, got {len(active)}"
    assert "Aya 8B CSQE" not in set(active.model), "CSQE row leaked back in"

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(active.model, active.ndcg_10,
           color=[color_for_model(m) for m in active.model], edgecolor="black")
    ax.axhline(baseline, color="#1f6f8a", linestyle="--", linewidth=1,
               label=f"mDPR baseline ({baseline:.3f})")
    ax.set_ylabel("NDCG@10")
    ax.set_ylim(0, max(active.ndcg_10) * 1.1)
    ax.legend(loc="upper right")
    plt.xticks(rotation=30, ha="right")

    save_fig(fig, "fig_4_5_models_bar_v1")
    print("  bars:", ", ".join(active.model))


if __name__ == "__main__":
    main()
