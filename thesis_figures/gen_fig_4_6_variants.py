"""Figure 4.6 (compiled PDF) redesigns — dense multi-metric per model, WITH baseline.

Replaces `fig_4_5_models_grouped_v3.pdf`, which showed no baseline, included an
`Aya 8B CSQE` bar that does not belong in a Query2Doc chart (E1 report defect 5.3),
and used a 0-anchored y-axis on which all ten models look identical.

Variants produced:
  v4_panels   small multiples, one panel per metric, stems drawn from the baseline
  v5_baseline original grouped bars + an explicit baseline group and reference lines
  v6_delta    grouped bars of the gain over baseline (zero line = no-QE baseline)

Run:  python thesis_figures/gen_fig_4_6_variants.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "notebooks"))
from _helpers import *  # noqa: F401,F403  (style, paths, save_fig, color_for_model)

METRICS = [("NDCG@10", "ndcg_10"), ("Recall@10", "recall_10"), ("MRR", "mrr")]
BASELINE_ROW = "mDPR (no QE)"
GREY = "#8c8c8c"
DARK_GREY = "#5c5c5c"

dense = pd.read_csv(DATA_RAW / "model_comparison_dense.csv")
base = dense.loc[dense.model == BASELINE_ROW].iloc[0]
BASE = {col: float(base[col]) for _, col in METRICS}

# Query2Doc models only: drop the baseline row, the dropped ALLaM run, and the
# CSQE variant (a different technique, reported in Section 4.9).
q2d = dense[~dense.model.isin([BASELINE_ROW, "ALLaM-7B", "Aya 8B CSQE"])].copy()
q2d = q2d.sort_values("ndcg_10", ascending=False).reset_index(drop=True)
print(f"{len(q2d)} models, baseline = {BASE}")


# ---------------------------------------------------------------- v4: panels
# Model rows are shared across the three panels, so the ranking reads like a
# table. Each stem starts at that metric's baseline, which lets the axis zoom
# without the misleading truncated-bar effect.
fig, axes = plt.subplots(1, 3, figsize=(7.2, 4.0), sharey=True)
order = q2d.iloc[::-1].reset_index(drop=True)  # best at top
y = np.arange(len(order))

for ax, (label, col) in zip(axes, METRICS):
    b = BASE[col]
    ax.axvline(b, color=DARK_GREY, linestyle="--", linewidth=1, zorder=1)
    for i, r in order.iterrows():
        c = color_for_model(r.model)
        ax.plot([b, r[col]], [i, i], color=c, linewidth=1.6, zorder=2)
        ax.plot([r[col]], [i], "o", color=c, markersize=5.5, zorder=3)
        ax.annotate(f"{r[col]:.3f}", (r[col], i), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=7.5,
                    color="#333333")
    lo = b - (order[col].max() - b) * 0.10
    hi = order[col].max() + (order[col].max() - b) * 0.55
    ax.set_xlim(lo, hi)
    ax.set_title(label, fontsize=10, pad=6)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="x", labelsize=8)
    # Baseline value sits under the last row, clear of the title and the stems.
    ax.annotate(f"no-QE baseline {b:.3f}", (b, -0.55), xytext=(3, 0),
                textcoords="offset points", ha="left", va="center",
                fontsize=7.5, color=DARK_GREY)

axes[0].set_yticks(y)
axes[0].set_yticklabels(order.model)
axes[0].set_ylim(-0.7, len(order) - 0.2)
fig.tight_layout(w_pad=1.4)
save_fig(fig, "fig_4_5_models_grouped_v4_panels")


# ------------------------------------------------- v5: grouped + baseline group
# Conservative fix to the existing chart: same grouped-bar idiom, but the
# baseline is drawn as its own leading group and carried across as dashed lines.
fig, ax = plt.subplots(figsize=(7.6, 4.2))
labels = [BASELINE_ROW] + q2d.model.tolist()
x = np.arange(len(labels))
w = 0.27
metric_greys = ["#1f6f8a", "#7a7a7a", "#b3b3b3"]

for i, (label, col) in enumerate(METRICS):
    vals = [BASE[col]] + q2d[col].tolist()
    colors = ["#d9d9d9"] + [metric_greys[i]] * len(q2d)
    ax.bar(x + (i - 1) * w, vals, w, color=colors, edgecolor="black",
           hatch=["////"] + [""] * len(q2d))
    ax.axhline(BASE[col], color=metric_greys[i], linestyle="--", linewidth=0.9,
               zorder=0)

# Proxy handles, otherwise the legend inherits the hatch from the baseline bar.
from matplotlib.patches import Patch
handles = [Patch(facecolor=metric_greys[i], edgecolor="black", label=lab)
           for i, (lab, _) in enumerate(METRICS)]

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=30, ha="right")
ax.get_xticklabels()[0].set_style("italic")
ax.set_ylabel("Score")
ax.set_ylim(0, 0.83)
ax.legend(handles=handles, loc="upper right", ncol=3)
ax.annotate("hatched group and dashed lines = mDPR baseline (no QE)",
            (0.01, 0.965), xycoords="axes fraction", fontsize=8, color=DARK_GREY)
fig.tight_layout()
save_fig(fig, "fig_4_5_models_grouped_v5_baseline")


# ------------------------------------------------------------- v6: delta bars
# Everything is expressed as a gain over the no-QE baseline, so the zero line
# *is* the baseline and the between-model spread uses the full axis height.
fig, ax = plt.subplots(figsize=(7.6, 4.2))
x = np.arange(len(q2d))
for i, (label, col) in enumerate(METRICS):
    ax.bar(x + (i - 1) * w, q2d[col] - BASE[col], w, label=label,
           color=metric_greys[i], edgecolor="black")

ax.axhline(0, color="black", linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(q2d.model, rotation=30, ha="right")
ax.set_ylabel("Gain over mDPR baseline")
ax.legend(loc="upper right", ncol=3)
note = "  |  ".join(f"{lab} baseline = {BASE[col]:.4f}" for lab, col in METRICS)
ax.annotate(note, (0.0, -0.34), xycoords="axes fraction", fontsize=8,
            color=DARK_GREY)
fig.tight_layout()
save_fig(fig, "fig_4_5_models_grouped_v6_delta")

print("done")
