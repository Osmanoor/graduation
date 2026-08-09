"""Generate fig_2_6_metrics.tex — the three retrieval metrics on one worked example.

Task K6, spec: research_decisions/CH2_FIGURES_SPEC.md (Fig 2.6).

Every number printed in the figure is computed here, never typed by hand. The
figure explains Equations 2.5-2.9 of chapter2.tex (Recall@k, DCG, NDCG, MRR), so
the arithmetic must match those equations exactly:

    DCG@k   = sum_i (2^rel_i - 1) / log2(i + 1)      chapter2.tex:221
    NDCG@k  = DCG@k / IDCG@k                          chapter2.tex:228
    Recall@k= |relevant ∩ top-k| / |relevant|         chapter2.tex:207
    MRR     = mean over queries of 1 / rank_first     chapter2.tex:240

MIRACL uses binary relevance (qrels.tsv carries grades 0 and 1), so 2^rel - 1
collapses to rel and the gain at a relevant rank is just the discount.

Run:  python gen_fig_2_6_metrics.py
Then: cd system_diagrams && xelatex fig_2_6_metrics.tex
"""

from math import log2
from pathlib import Path

# ─── The worked example ────────────────────────────────────────────────────
# One query. Four relevant passages exist in the corpus; the retriever returns
# ten, with relevant ones landing at ranks 2, 5 and 9. Chosen so that the three
# metrics disagree (which is the pedagogical point) and so NDCG@10 lands inside
# the range the thesis actually reports (0.4621 -> 0.7137).
K = 10
RELEVANT_RANKS = [2, 5, 9]
TOTAL_RELEVANT = 4

rel = [1 if r in RELEVANT_RANKS else 0 for r in range(1, K + 1)]
disc = [1.0 / log2(i + 1) for i in range(1, K + 1)]
gain = [(2 ** r - 1) * d for r, d in zip(rel, disc)]

dcg = sum(gain)
idcg = sum(disc[:TOTAL_RELEVANT])          # ideal: all relevant docs at the top
ndcg = dcg / idcg
recall = len(RELEVANT_RANKS) / TOTAL_RELEVANT
mrr = 1.0 / min(RELEVANT_RANKS)
ratio = disc[0] / disc[K - 1]              # rank-1 vs rank-10 worth

assert abs(dcg - 1.3188) < 1e-3, dcg
assert abs(idcg - 2.5616) < 1e-3, idcg
assert abs(ndcg - 0.5148) < 1e-3, ndcg

# ─── Emit TikZ ─────────────────────────────────────────────────────────────
cells, marks, discs = [], [], []
for i in range(K):
    r = i + 1
    hit = rel[i] == 1
    cells.append(
        f"\\node[slot{',hit' if hit else ''}] (s{r}) at ({(r-1)*13}mm, 0) {{{r}}};")
    marks.append(
        f"\\node[relmark] at ({(r-1)*13}mm, -7mm) "
        f"{{{'$\\bullet$' if hit else '$\\cdot$'}}};")
    discs.append(
        f"\\node[discval] at ({(r-1)*13}mm, -13mm) {{{disc[i]:.3f}}};")

tex = f"""% Fig 2.6 — The three retrieval metrics on one worked example.
%
% GENERATED FILE — do not edit by hand.
% Source: thesis_figures/gen_fig_2_6_metrics.py   (regenerate, do not patch)
%
% Why this figure exists: NDCG@10 is the headline number of the whole thesis, and
% §2.2.4 defines it with two equations and no intuition. One example covers all
% three metrics and shows WHY they disagree, which a definition list cannot do.
\\documentclass[border=4pt]{{standalone}}
\\usepackage{{tikz}}
\\usepackage{{amsmath}}
\\input{{_style.tex}}

\\begin{{document}}
\\begin{{tikzpicture}}[
    slot/.style={{rectangle, draw=thDataS, fill=white, rounded corners=1.5pt,
                 minimum width=10mm, minimum height=7mm, font=\\footnotesize}},
    hit/.style={{draw=thRetS, fill=thRetF, line width=0.9pt}},
    relmark/.style={{font=\\small, color=thRetS}},
    discval/.style={{font=\\scriptsize, color=thMuted}},
    rowlab/.style={{font=\\footnotesize\\bfseries, color=thMuted, anchor=east}},
    calc/.style={{rectangle, draw=thFusionS, fill=thFusionF, rounded corners=2pt,
                 align=left, inner sep=6pt, font=\\footnotesize, line width=0.7pt}},
    verdict/.style={{thBase, draw=thHiS, fill=thHiF, line width=1pt,
                    align=center, font=\\footnotesize, minimum height=8mm}}
]

  % ─── The ranked list ────────────────────────────────────────────────────
  {chr(10).join('  ' + c for c in cells)}
  {chr(10).join('  ' + m for m in marks)}
  {chr(10).join('  ' + d for d in discs)}

  \\node[rowlab] at (-9mm, 0)     {{rank}};
  \\node[rowlab] at (-9mm, -7mm)  {{relevant}};
  \\node[rowlab] at (-9mm, -13mm) {{$1/\\log_2(i{{+}}1)$}};

  \\node[thLabel, anchor=west] at (-9mm, 8mm)
    {{one query · {TOTAL_RELEVANT} relevant passages exist in the corpus · top-{K} returned}};

  % ─── The arithmetic ─────────────────────────────────────────────────────
  \\node[calc, anchor=north west] at (-9mm, -22mm) (calcbox) {{%
    $\\text{{DCG@}}{K} \\;=\\; {gain[1]:.3f} + {gain[4]:.3f} + {gain[8]:.3f}
       \\;=\\; \\mathbf{{{dcg:.4f}}}$\\\\[3pt]
    $\\text{{IDCG@}}{K} \\;=\\; {disc[0]:.3f} + {disc[1]:.3f} + {disc[2]:.3f} + {disc[3]:.3f}
       \\;=\\; \\mathbf{{{idcg:.4f}}}$
       \\quad{{\\scriptsize(all {TOTAL_RELEVANT} relevant at the top)}}}};

  % ─── The three verdicts ─────────────────────────────────────────────────
  \\node[verdict, minimum width=38mm, anchor=north west] at (-9mm, -44mm) (v1)
    {{\\textbf{{Recall@{K} = {recall:.2f}}}\\\\{{\\scriptsize did we find them?}}\\\\
      {{\\scriptsize {len(RELEVANT_RANKS)} of {TOTAL_RELEVANT} found}}}};
  \\node[verdict, minimum width=38mm, right=6mm of v1] (v2)
    {{\\textbf{{MRR = {mrr:.2f}}}\\\\{{\\scriptsize how soon was the first?}}\\\\
      {{\\scriptsize first hit at rank {min(RELEVANT_RANKS)}}}}};
  \\node[verdict, minimum width=38mm, right=6mm of v2] (v3)
    {{\\textbf{{NDCG@{K} = {ndcg:.4f}}}\\\\{{\\scriptsize are they near the top?}}\\\\
      {{\\scriptsize every hit discounted by rank}}}};

  \\node[thLabel, anchor=north west, text width=125mm] at (-9mm, -58mm)
    {{the same ranking scores {recall:.2f}, {mrr:.2f} and {ndcg:.3f} --- a document at rank~1
     is worth {ratio:.2f} times one at rank~{K}, which is why only NDCG penalises
     burying a relevant passage}};

\\end{{tikzpicture}}
\\end{{document}}
"""

out = Path(__file__).parent / "system_diagrams" / "fig_2_6_metrics.tex"
out.write_text(tex, encoding="utf-8")

print(f"DCG@{K}   = {dcg:.4f}")
print(f"IDCG@{K}  = {idcg:.4f}")
print(f"NDCG@{K}  = {ndcg:.4f}")
print(f"Recall@{K}= {recall:.2f}")
print(f"MRR      = {mrr:.2f}")
print(f"rank-1 worth {ratio:.2f}x rank-{K}")
print(f"\nwrote {out}")
