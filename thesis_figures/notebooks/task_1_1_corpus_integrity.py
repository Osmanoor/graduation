#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 1.1 (Workstream 1) — Verify dataset integrity for the 258 CSQE failures.

Claim under test (from exp_error_analysis_csqe.md / §4.10):
    "257/258 failures are universally irretrievable — the relevant qrel
     document is not present in the indexed Wikipedia corpus dump."

This script tests that claim directly, with NO GPU / index / Colab needed.
For each failure query (Config A RRF nDCG@10 < 0.1) it checks whether the
query's relevant qrel docid(s) actually exist in the indexed corpus.

Inputs (all under thesis_figures/data/raw/):
    corpus_ids.pkl          list[str] of every docid in the BM25S/FAISS index
                            (Drive id 1X-anlUuyDarN9wnnTCTQ7Gk-KuNkpqD0, ~24 MB)
    hybrid_csqe_rrf_k20.txt Config A RRF TREC run = "scores_csqe"
                            (Drive id 1y1ceNTgvdespuduqwomLigHwsTe-ZI3d, ~12 MB)
    miracl_qrels_dev.json   MIRACL Arabic dev qrels {qid: {docid: rel}}  (local)

Cross-check (no extra download — already in the repo):
    ../../arabic-rag-query-enhancement/results/baseline_bm25/exp_002_baseline_bm25.txt
                            BM25 baseline run, used to confirm "BM25 also scores 0"

Outputs:
    data/computed/task_1_1_failure_corpus_check.csv   per-failure verdict table
    console summary + routing verdict (see STREAM_1_KICKOFF.md "Outcome branches")
"""

import os, sys, json, pickle
from pathlib import Path

import pytrec_eval

# Windows consoles default to cp1252 and choke on Arabic; force UTF-8 output.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---------------------------------------------------------------- paths
HERE = Path(__file__).resolve().parent           # thesis_figures/notebooks
RAW  = HERE.parent / "data" / "raw"
OUT  = HERE.parent / "data" / "computed"
OUT.mkdir(parents=True, exist_ok=True)
REPO = HERE.parents[1]                            # graduation/

CORPUS_IDS_PKL = RAW / "corpus_ids.pkl"
CONFIG_A_RUN   = RAW / "hybrid_csqe_rrf_k20.txt"
QRELS_JSON     = RAW / "miracl_qrels_dev.json"
BM25_BASE_RUN  = (REPO / "arabic-rag-query-enhancement" / "results"
                  / "baseline_bm25" / "exp_002_baseline_bm25.txt")

FAILURE_THRESHOLD = 0.1   # Config A nDCG@10 < 0.1  (matches the error-analysis doc)

# ---------------------------------------------------------------- helpers
def load_trec_run(path):
    """Parse a 6-column TREC run file -> {qid: {docid: score}} (str keys)."""
    run = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 6:
                continue
            qid, _, docid, _, score, _ = parts[:6]
            run.setdefault(str(qid), {})[docid] = float(score)
    return run


def per_query_ndcg10(run, qrels):
    """{qid: ndcg@10} via pytrec_eval, same recipe as the notebook."""
    qrel_dict = {str(qid): {str(d): int(r) for d, r in docs.items()}
                 for qid, docs in qrels.items()}
    ev = pytrec_eval.RelevanceEvaluator(qrel_dict, {"ndcg_cut_10"})
    res = ev.evaluate(run)
    return {qid: v.get("ndcg_cut_10", 0.0) for qid, v in res.items()}


def main():
    # ---- guard: required downloads present?
    missing = [p for p in (CORPUS_IDS_PKL, CONFIG_A_RUN) if not p.exists()]
    if missing:
        print("MISSING required input(s):")
        for p in missing:
            print(f"  - {p}")
        print("\nDownload from Drive into thesis_figures/data/raw/ :")
        print("  corpus_ids.pkl          -> https://drive.google.com/file/d/1X-anlUuyDarN9wnnTCTQ7Gk-KuNkpqD0/view")
        print("  hybrid_csqe_rrf_k20.txt -> https://drive.google.com/file/d/1y1ceNTgvdespuduqwomLigHwsTe-ZI3d/view")
        sys.exit(1)

    # ---- load corpus docid set
    print(f"Loading corpus IDs from {CORPUS_IDS_PKL.name} ...")
    with open(CORPUS_IDS_PKL, "rb") as f:
        corpus_ids = pickle.load(f)
    corpus_set = set(map(str, corpus_ids))
    print(f"  corpus documents indexed: {len(corpus_set):,}")
    # sanity: docid format should be 'articleid#passageid'
    sample = next(iter(corpus_set))
    print(f"  sample corpus docid: {sample!r}  ('#' present: {'#' in sample})")

    # ---- load qrels
    qrels = json.load(open(QRELS_JSON, encoding="utf-8"))
    print(f"  qrels queries: {len(qrels):,}")

    # ---- Config A RRF run -> per-query nDCG@10 -> failure set
    print(f"\nComputing Config A RRF per-query nDCG@10 from {CONFIG_A_RUN.name} ...")
    config_a_run = load_trec_run(CONFIG_A_RUN)
    scores_csqe  = per_query_ndcg10(config_a_run, qrels)
    failure_qids = sorted([q for q, s in scores_csqe.items() if s < FAILURE_THRESHOLD],
                          key=lambda q: scores_csqe[q])
    print(f"  Config A run queries: {len(config_a_run):,}")
    print(f"  failures (nDCG@10 < {FAILURE_THRESHOLD}): {len(failure_qids)}")

    # ---- BM25 baseline cross-check (local, no download)
    bm25_scores = {}
    if BM25_BASE_RUN.exists():
        bm25_run = load_trec_run(BM25_BASE_RUN)
        bm25_scores = per_query_ndcg10(bm25_run, qrels)
    else:
        print(f"  (BM25 baseline run not found at {BM25_BASE_RUN}; skipping cross-check)")

    # ---- per-failure verdict
    rows = []
    n_irretrievable = n_genuine = 0
    for qid in failure_qids:
        rels = [str(d) for d, r in qrels.get(qid, {}).items() if int(r) > 0]
        present = [d for d in rels if d in corpus_set]
        verdict = "irretrievable" if len(present) == 0 else "genuine_failure"
        if verdict == "irretrievable":
            n_irretrievable += 1
        else:
            n_genuine += 1
        rows.append({
            "qid": qid,
            "ndcg10_config_a": round(scores_csqe.get(qid, 0.0), 4),
            "ndcg10_bm25_baseline": round(bm25_scores.get(qid, 0.0), 4) if bm25_scores else "",
            "n_relevant": len(rels),
            "n_present_in_corpus": len(present),
            "verdict": verdict,
            "missing_docids": ";".join([d for d in rels if d not in corpus_set][:5]),
        })

    # ---- write CSV
    import csv
    out_csv = OUT / "task_1_1_failure_corpus_check.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- summary + routing
    n = len(failure_qids)
    print("\n" + "=" * 60)
    print("TASK 1.1 RESULT — dataset integrity of the failure set")
    print("=" * 60)
    print(f"  failure queries (Config A nDCG@10 < {FAILURE_THRESHOLD}): {n}")
    print(f"  irretrievable  (no relevant docid in corpus): {n_irretrievable}  ({n_irretrievable/n:.1%})")
    print(f"  genuine_failure(relevant docid IS in corpus):  {n_genuine}  ({n_genuine/n:.1%})")
    if bm25_scores:
        both_zero = sum(1 for q in failure_qids
                        if scores_csqe.get(q, 0) == 0 and bm25_scores.get(q, 0) == 0)
        print(f"  cross-check: Config A == 0 AND BM25 baseline == 0: {both_zero}/{n}")
    print(f"\n  wrote: {out_csv}")

    print("\nROUTING (per STREAM_1_KICKOFF.md):")
    if abs(n_irretrievable - 257) <= 5:
        print("  ~257 irretrievable -> CLAIM HOLDS. Update §4.10 with the verified")
        print("  number; proceed to Tasks 1.2 / 1.3.")
    elif n_irretrievable < n * 0.5:
        print("  irretrievable << claimed -> CLAIM IS WRONG. Failures are genuine")
        print("  retrieval failures; §4.10 narrative needs rewrite. Still proceed to")
        print("  1.2/1.3 but with corrected baseline counts.")
    else:
        print(f"  n_irretrievable={n_irretrievable} is between the two branches.")
        print("  Inspect the CSV (genuine_failure rows) before deciding §4.10 wording.")
    print("=" * 60)


if __name__ == "__main__":
    main()
