"""Shared helpers for thesis figure notebooks.

All notebooks `from _helpers import *` to inherit:
- thesis matplotlib style
- consistent paths to data/ and output/
- savefig that writes both PDF (vector for LaTeX) and PNG (review)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# -- paths ----------------------------------------------------------------
NOTEBOOK_DIR = Path(__file__).resolve().parent
THESIS_FIGURES = NOTEBOOK_DIR.parent
DATA_RAW = THESIS_FIGURES / "data" / "raw"
DATA_COMPUTED = THESIS_FIGURES / "data" / "computed"
OUTPUT_PDF = THESIS_FIGURES / "output" / "pdf"
OUTPUT_PNG = THESIS_FIGURES / "output" / "png"

# -- style ---------------------------------------------------------------
plt.style.use(str(THESIS_FIGURES / "styles" / "thesis_style.mplstyle"))


def save_fig(fig, slug: str, *, also_pdf: bool = True, also_png: bool = True) -> None:
    """Save figure to output/pdf/<slug>.pdf and output/png/<slug>.png.

    `slug` is the file stem, e.g., 'fig_4_11_progression_v1'. The figure is closed afterward.
    """
    if also_pdf:
        fig.savefig(OUTPUT_PDF / f"{slug}.pdf", format="pdf")
    if also_png:
        fig.savefig(OUTPUT_PNG / f"{slug}.png", format="png", dpi=300)
    plt.close(fig)
    print(f"  saved: {slug}")


def load_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_csv(path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


def load_trec_run(path) -> pd.DataFrame:
    """Parse a TREC run file. Format: qid Q0 docid rank score tag."""
    cols = ["qid", "Q0", "docid", "rank", "score", "tag"]
    df = pd.read_csv(path, sep=r"\s+", names=cols, dtype={"qid": str, "docid": str})
    return df


def compute_per_query_metrics(run_df: pd.DataFrame, qrels: dict, k_ndcg: int = 10, k_recall=(10, 100)):
    """Compute per-query nDCG@k, Recall@k, MRR using pytrec_eval.

    `qrels` is a dict {qid: {docid: relevance}} as produced by MIRACL.
    Returns a DataFrame with columns: qid, ndcg10, recall10, recall100, mrr, num_relevant.
    """
    try:
        import pytrec_eval
    except ImportError as e:
        raise ImportError("pip install pytrec_eval") from e

    # Build run in pytrec_eval format: {qid: {docid: score}}
    run = {}
    for qid, group in run_df.groupby("qid"):
        run[str(qid)] = {str(d): float(s) for d, s in zip(group["docid"], group["score"])}

    measures = {f"ndcg_cut.{k_ndcg}", f"recip_rank"} | {f"recall.{k}" for k in k_recall}
    qrels_str = {str(q): {str(d): int(r) for d, r in v.items()} for q, v in qrels.items()}
    evaluator = pytrec_eval.RelevanceEvaluator(qrels_str, measures)
    results = evaluator.evaluate(run)

    rows = []
    for qid, m in results.items():
        rows.append({
            "qid": qid,
            f"ndcg{k_ndcg}": m.get(f"ndcg_cut_{k_ndcg}", 0.0),
            "recall10": m.get("recall_10", 0.0),
            "recall100": m.get("recall_100", 0.0),
            "mrr": m.get("recip_rank", 0.0),
            "num_relevant": sum(1 for v in qrels_str.get(qid, {}).values() if v > 0),
        })
    return pd.DataFrame(rows)


def length_bin(n_words: int) -> str:
    """Categorical bin used in error analysis.

    Scheme A (Decision 2026-05-31): 1-3 / 4-8 / 9+ words, unifies §4.2 and §4.10.
    Preserves the founding short-query motivation (§4.2 ratio 0.345 vs 0.476).
    """
    if n_words <= 3:
        return "Short (1-3)"
    if n_words <= 8:
        return "Medium (4-8)"
    return "Long (9+)"


LENGTH_BIN_ORDER = ["Short (1-3)", "Medium (4-8)", "Long (9+)"]


# Stable model → color mapping used across model-comparison figures
# (e.g., Fig 4.5 bar chart and Fig 4.7 repetition lines).
# Best-performing model (Aya 8B) gets the thesis primary teal accent.
# Other colors are muted hues chosen for grayscale-safe printing while
# remaining mutually distinguishable in colour.
MODEL_COLORS = {
    "Aya Expanse 8B": "#1f6f8a",   # primary teal (best, headline)
    "Jais-2-8B":      "#6d4a8f",   # purple
    "Qwen3-8B":       "#3d7a4f",   # green
    "Qwen 2.5-7B":    "#a05a30",   # rust / brown-orange
    "ALLaM-7B":       "#8c4040",   # muted red (dropped)
    "Qwen3-4B":       "#4a6fa5",   # slate blue
    "Gemma 3 4B":     "#c8983a",   # gold
    "Qwen 2.5-3B":    "#5c7a8a",   # blue-grey
    "Falcon-H1-3B":   "#7a5a8a",   # lavender
    "SILMA 2B":       "#8a7a5a",   # taupe
}


def _slug(s: str) -> str:
    """Loose normalisation for matching model names across CSVs."""
    import re
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


# Pre-compute slug → color so Fig 4.5 / Fig 4.7 can look up by either form.
_SLUG_COLORS = {_slug(k): v for k, v in MODEL_COLORS.items()}
# Common alternates: "SILMA Kashif-2B" / "Qwen 2.5 3B" (space variant)
_SLUG_COLORS[_slug("SILMA Kashif-2B")] = MODEL_COLORS["SILMA 2B"]
_SLUG_COLORS[_slug("Qwen 2.5 3B")]      = MODEL_COLORS["Qwen 2.5-3B"]


def color_for_model(name: str, fallback: str = "#6a6a6a") -> str:
    """Return the thesis-stable color for a model name. Falls back to muted grey."""
    return _SLUG_COLORS.get(_slug(name), fallback)


def annotate_bars(ax, fmt: str = "{:.3f}", offset: float = 0.005) -> None:
    """Add value labels above each bar in a bar plot."""
    for p in ax.patches:
        h = p.get_height()
        ax.annotate(fmt.format(h),
                    xy=(p.get_x() + p.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8)


print(f"helpers loaded. DATA_RAW={DATA_RAW.name}/  OUTPUT_PDF={OUTPUT_PDF.name}/")
