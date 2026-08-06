"""Regenerate Figure 4.9 (fig_4_8_gains_v1) — Dense vs BM25 Query2Doc gain per model.

Run:  python thesis_figures/regen_fig_4_9_gains.py

Why this script exists (task E2, decisions from the E1 review meeting):

1. ENCODING FIX. The committed render of this figure had mojibake axis labels:
   the Greek delta rendered as `Î"` because the plotting run read the U+0394
   source as latin-1. The notebook source was already correct, so the fix is
   simply to re-render from a UTF-8-clean process. This file is written and read
   as UTF-8 and asserts the label is intact before saving.

2. SILMA WAS SILENTLY MISSING. Notebook 03 joined the dense and BM25 tables on a
   slug built by stripping non-alphanumerics. The dense CSV calls the model
   "SILMA Kashif-2B" (slug `silmakashif2b`) and the BM25 CSV calls it
   "SILMA 2B" (slug `silma2b`), so the inner join dropped it and the figure
   showed 8 of 9 models while the caption implied all of them. An explicit
   name map replaces the fuzzy slug join.

3. VISUAL REDESIGN. The previous layout put every point in one colour with
   uniform label offsets, so Falcon-H1-3B and Qwen 2.5 3B overlapped and the
   headline message (only two models improve BOTH retrievers) was not visible.
   Now: the both-positive quadrant is shaded and annotated, points use the
   thesis-stable per-model colours shared with Figures 4.5 and 4.8, and label
   offsets are set per model to remove collisions.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "notebooks"))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from _helpers import DATA_RAW, color_for_model, save_fig  # noqa: E402

DENSE_BASELINE = 0.4993
BM25_BASELINE = 0.4621

# Explicit dense-CSV name -> BM25-CSV name. Replaces the slug join that lost SILMA.
NAME_MAP = {
    "SILMA Kashif-2B": "SILMA 2B",
    "Qwen 2.5 3B": "Qwen 2.5-3B",
    "Falcon-H1-3B": "Falcon-H1-3B",
    "Qwen3-4B": "Qwen3-4B",
    "Gemma 3 4B": "Gemma 3 4B",
    "Qwen 2.5-7B": "Qwen 2.5-7B",
    "Jais-2-8B": "Jais-2-8B",
    "Qwen3-8B": "Qwen3-8B",
    "Aya Expanse 8B": "Aya Expanse 8B",
}

# Per-model label placement: (dx_pt, dy_pt, horizontal_alignment).
# Tuned against the plotted coordinates so no two labels collide.
LABEL_OFFSETS = {
    "SILMA Kashif-2B": (7, -3, "left"),
    "Gemma 3 4B": (8, -2, "left"),
    "Falcon-H1-3B": (-9, -11, "right"),
    "Qwen 2.5 3B": (8, 3, "left"),
    "Qwen3-4B": (8, -3, "left"),
    "Qwen3-8B": (8, -4, "left"),
    "Qwen 2.5-7B": (-9, 6, "right"),
    "Aya Expanse 8B": (-9, -4, "right"),
    "Jais-2-8B": (-9, 6, "right"),
}


def main() -> None:
    dense = pd.read_csv(DATA_RAW / "model_comparison_dense.csv")
    bm25 = pd.read_csv(DATA_RAW / "model_comparison_bm25.csv")

    bm25_by_name = dict(zip(bm25["model"], bm25["n1_ndcg10"]))

    rows = []
    for dense_name, bm25_name in NAME_MAP.items():
        hit = dense.loc[dense["model"] == dense_name, "ndcg_10"]
        if hit.empty:
            raise SystemExit(f"dense CSV missing model: {dense_name}")
        if bm25_name not in bm25_by_name:
            raise SystemExit(f"BM25 CSV missing model: {bm25_name}")
        rows.append({
            "model": dense_name,
            "dense_delta": float(hit.iloc[0]) - DENSE_BASELINE,
            "bm25_delta": float(bm25_by_name[bm25_name]) - BM25_BASELINE,
        })
    df = pd.DataFrame(rows)
    assert len(df) == 9, f"expected 9 models, joined {len(df)}"

    fig, ax = plt.subplots(figsize=(6.2, 4.3))

    xlo, xhi = -0.004, 0.150
    ylo, yhi = -0.132, 0.072

    # Shade the both-positive quadrant: the figure's headline message.
    # Anchored at the origin so the tint never extends into negative Dense gain.
    ax.add_patch(plt.Rectangle((0, 0), xhi, yhi, facecolor="#1f6f8a",
                               alpha=0.10, edgecolor="none", zorder=0))
    ax.annotate("Both retrievers improve",
                xy=(xhi - 0.004, yhi - 0.004), ha="right", va="top",
                fontsize=8.5, style="italic", color="#1f6f8a", zorder=2)
    ax.annotate("BM25 degrades at $n{=}1$",
                xy=(xhi - 0.004, ylo + 0.004), ha="right", va="bottom",
                fontsize=8.5, style="italic", color="#8c8c8c", zorder=2)

    ax.axhline(0, color="#4d4d4d", linewidth=0.9, zorder=1)
    ax.axvline(0, color="#4d4d4d", linewidth=0.9, zorder=1)

    for _, r in df.iterrows():
        both_positive = r.bm25_delta > 0
        ax.scatter(r.dense_delta, r.bm25_delta,
                   s=95 if both_positive else 70,
                   color=color_for_model(r.model),
                   edgecolor="black" if both_positive else "none",
                   linewidth=0.7, zorder=4)
        dx, dy, ha = LABEL_OFFSETS[r.model]
        ax.annotate(r.model, (r.dense_delta, r.bm25_delta),
                    xytext=(dx, dy), textcoords="offset points",
                    fontsize=8.5, ha=ha, va="center",
                    fontweight="bold" if both_positive else "normal",
                    zorder=5)

    xlabel = "Δ NDCG@10 on Dense (Query2Doc vs. mDPR baseline)"
    ylabel = "Δ NDCG@10 on BM25 (Query2Doc $n{=}1$ vs. BM25 baseline)"
    assert "Δ" in xlabel and "Δ" in ylabel, "delta glyph lost"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)

    fig.tight_layout()
    save_fig(fig, "fig_4_8_gains_v1")


if __name__ == "__main__":
    main()
