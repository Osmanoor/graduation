"""Task H1 - re-run SILMA's 8 BM25 repetition configs from the temperature-0.1 expansions.

Mirrors `experiments/phase4_quick_wins (1).ipynb` cells 7, 8 and 15 exactly:
  fixed    : enhanced = (query + ' ') * n + pseudo_doc,  n in {1,3,5,7,10}
  adaptive : n = max(1, int(len(pdoc.split()) / (len(query.split()) * beta))),  beta in {2,4,6}

Gate order:
  1. baseline raw queries  -> must reproduce 0.4621 (proves index + tokenisation match)
  2. SILMA temp-0.1 n=1    -> must reproduce 0.4277 (the handoff's sanity check)
  3. remaining 7 configs   -> only if both gates pass

Each config is checkpointed to disk as it completes, so a crash or interruption
does not cost the retrievals already paid for. Re-running resumes.

Usage:  python h1_silma_rerun.py
"""
import json
import os
import pickle
import sys
import time

import bm25s
import Stemmer
import nltk
import pytrec_eval

BASE = r"f:\Desktop\graduation\arabic-rag-query-enhancement"
DATA = os.path.join(BASE, "data", "miracl_ar")
PKL_DIR = os.path.join(BASE, "results", "enhanced_queries")
OUT_DIR = os.path.join(BASE, "results", "exp_11b_silma_temp01")
CKPT = os.path.join(OUT_DIR, "_checkpoints")

FIXED_NS = [1, 3, 5, 7, 10]
BETAS = [2, 4, 6]
METRIC_NAMES = ["ndcg_cut_10", "recall_10", "recall_100", "recip_rank"]

EXPECT_BASELINE = 0.4621          # results/baseline_bm25/exp_002_metrics.json
EXPECT_SILMA_N1 = 0.4277          # chapter4.tex:292, Table 4.7 SILMA row (temp 0.1)
TOL = 5e-5


# ---------------------------------------------------------------- data
def load_topics_qrels():
    topics = {}
    with open(os.path.join(DATA, "topics.tsv"), encoding="utf-8") as f:
        for line in f:
            qid, q = line.rstrip("\n").split("\t")
            topics[qid] = q
    qrels = {}
    with open(os.path.join(DATA, "qrels.tsv"), encoding="utf-8") as f:
        for line in f:
            qid, _, docid, rel = line.rstrip("\n").split("\t")
            qrels.setdefault(qid, {})[docid] = int(rel)
    return topics, qrels


def extract(pkl_name):
    d = pickle.load(open(os.path.join(PKL_DIR, pkl_name), "rb"))
    qids = [str(q) for q in d["query_ids"]]
    originals = d["original_queries"]
    pseudo_docs = [e[len(o):].strip() for o, e in zip(originals, d["enhanced_queries"])]
    return qids, originals, pseudo_docs


def build_fixed(originals, pseudo_docs, n):
    return [(o + " ") * n + p for o, p in zip(originals, pseudo_docs)]


def build_adaptive(originals, pseudo_docs, beta):
    out, ns = [], []
    for o, p in zip(originals, pseudo_docs):
        o_len = max(len(o.split()), 1)
        n = max(1, int(len(p.split()) / (o_len * beta)))
        out.append((o + " ") * n + p)
        ns.append(n)
    return out, ns


# ------------------------------------------------------------ retrieval
class Runner:
    def __init__(self, qrels):
        nltk.download("stopwords", quiet=True)
        from nltk.corpus import stopwords

        self.stopwords = stopwords.words("arabic")
        self.stemmer = Stemmer.Stemmer("arabic")
        self.qrels = qrels
        print(f"Arabic stopwords: {len(self.stopwords)}", flush=True)

        print("Loading BM25S index ...", flush=True)
        t0 = time.time()
        self.retriever = bm25s.BM25.load(
            os.path.join(DATA, "bm25s_index"), load_corpus=False, mmap=True
        )
        with open(os.path.join(DATA, "corpus_ids.pkl"), "rb") as f:
            self.corpus_ids = pickle.load(f)
        print(f"  {len(self.corpus_ids):,} documents in {time.time() - t0:.0f}s", flush=True)

    def run(self, queries, qids, k=100):
        tokens = bm25s.tokenize(
            queries, stopwords=self.stopwords, stemmer=self.stemmer, show_progress=False
        )
        idx, scores = self.retriever.retrieve(tokens, k=k, show_progress=False)
        run = {}
        for i, qid in enumerate(qids):
            run[qid] = {self.corpus_ids[d]: float(s) for d, s in zip(idx[i], scores[i])}

        # Fresh evaluator per call; pytrec_eval omits a measure for a query whose
        # run is degenerate, so aggregate defensively and surface any such query
        # instead of dying on a KeyError.
        evaluator = pytrec_eval.RelevanceEvaluator(self.qrels, set(METRIC_NAMES))
        per_query = evaluator.evaluate(run)

        agg, incomplete = {}, {}
        for m in METRIC_NAMES:
            vals = [v[m] for v in per_query.values() if m in v]
            missing = len(per_query) - len(vals)
            if missing:
                incomplete[m] = missing
            # Queries pytrec_eval could not score contribute 0, matching the
            # notebook's denominator of len(eval_results).
            agg[m] = sum(vals) / len(per_query)
        agg["num_queries"] = len(per_query)
        if incomplete:
            print(f"    WARNING: metrics missing for some queries: {incomplete}", flush=True)
        return agg, run


def show(label, agg, expected=None):
    line = (
        f"{label:<30} nDCG@10={agg['ndcg_cut_10']:.4f}  R@10={agg['recall_10']:.4f}  "
        f"R@100={agg['recall_100']:.4f}  MRR={agg['recip_rank']:.4f}"
    )
    if expected is not None:
        delta = agg["ndcg_cut_10"] - expected
        line += f"   [expected {expected:.4f}, delta {delta:+.5f}] {'PASS' if abs(delta) < TOL else 'FAIL'}"
    print(line, flush=True)


def cached(name, fn):
    """Run fn() once; reuse the checkpoint on later invocations."""
    path = os.path.join(CKPT, f"{name}.json")
    if os.path.exists(path):
        agg = json.load(open(path))
        print(f"  (resumed {name} from checkpoint)", flush=True)
        return agg
    t0 = time.time()
    agg = fn()
    agg["_seconds"] = round(time.time() - t0, 1)
    json.dump(agg, open(path, "w"), indent=2)
    return agg


# ----------------------------------------------------------------- main
def main():
    os.makedirs(CKPT, exist_ok=True)
    topics, qrels = load_topics_qrels()
    runner = Runner(qrels)

    qids, originals, pseudo_docs = extract("silma_2b_temp01.pkl")
    assert all(topics[q] == o for q, o in zip(qids, originals)), "query text mismatch"

    print("\n=== Gate 1: BM25 baseline, raw queries ===", flush=True)
    raw = [topics[q] for q in qids]
    baseline = cached("baseline_raw", lambda: runner.run(raw, qids)[0])
    show("BM25 baseline (no QE)", baseline, EXPECT_BASELINE)
    if abs(baseline["ndcg_cut_10"] - EXPECT_BASELINE) >= TOL:
        print("\nGate 1 FAILED - index or tokenisation does not match. STOPPING.", flush=True)
        sys.exit(2)

    print("\n=== Gate 2: SILMA temp-0.1, n=1 (handoff sanity check) ===", flush=True)
    results = {}
    results["n=1"] = cached("n1", lambda: runner.run(build_fixed(originals, pseudo_docs, 1), qids)[0])
    show("SILMA 2B (temp 0.1) n=1", results["n=1"], EXPECT_SILMA_N1)
    if abs(results["n=1"]["ndcg_cut_10"] - EXPECT_SILMA_N1) >= TOL:
        print("\nGate 2 FAILED - n=1 is not 0.4277. Per the handoff: STOP and report.", flush=True)
        sys.exit(3)

    print("\n=== Full sweep: SILMA 2B, temperature 0.1 ===", flush=True)
    avg_ns = {}
    for n in FIXED_NS[1:]:
        results[f"n={n}"] = cached(
            f"n{n}", lambda n=n: runner.run(build_fixed(originals, pseudo_docs, n), qids)[0]
        )
        show(f"n={n}", results[f"n={n}"])
    for beta in BETAS:
        queries, ns = build_adaptive(originals, pseudo_docs, beta)
        avg_ns[f"beta={beta}"] = sum(ns) / len(ns)
        results[f"beta={beta}"] = cached(
            f"beta{beta}", lambda queries=queries: runner.run(queries, qids)[0]
        )
        show(f"beta={beta} (avg n={avg_ns[f'beta={beta}']:.1f})", results[f"beta={beta}"])

    best_cfg = max(results, key=lambda c: results[c]["ndcg_cut_10"])
    best = results[best_cfg]
    delta = best["ndcg_cut_10"] - results["n=1"]["ndcg_cut_10"]

    print("\n=== Result ===", flush=True)
    print(f"best config : {best_cfg}")
    print(f"nDCG@10     : {best['ndcg_cut_10']:.4f}")
    print(f"Recall@10   : {best['recall_10']:.4f}")
    print(f"Recall@100  : {best['recall_100']:.4f}")
    print(f"MRR         : {best['recip_rank']:.4f}")
    print(f"delta vs n=1: {delta:+.4f}")
    print(f"beats BM25 baseline 0.4621: {best['ndcg_cut_10'] > EXPECT_BASELINE}")
    print(f"beats Falcon-H1 best 0.5113 (row order): {best['ndcg_cut_10'] > 0.5113}")

    payload = {
        "model": "SILMA 2B",
        "pkl": "silma_2b_temp01.pkl",
        "temperature": 0.1,
        "num_queries": results["n=1"]["num_queries"],
        "bm25s_version": bm25s.__version__,
        "arabic_stopwords": len(runner.stopwords),
        "baseline_no_qe": baseline,
        "configs": results,
        "adaptive_avg_n": avg_ns,
        "best_config": best_cfg,
        "delta_vs_n1": delta,
    }
    out = os.path.join(OUT_DIR, "silma_temp01_metrics.json")
    json.dump(payload, open(out, "w"), indent=2)
    print(f"\nsaved -> {out}")

    order = ["n=1", "n=3", "n=5", "n=7", "n=10", "beta=2", "beta=4", "beta=6"]
    cells = []
    for c in order:
        v = f"{results[c]['ndcg_cut_10']:.4f}"
        cells.append(f"\\textbf{{{v}}}" if c == best_cfg else v)
    print("\nAppendix B (tab:bm25_repetition) row:")
    print("        SILMA 2B & " + " & ".join(cells) + r" \\")
    tex_cfg = best_cfg.replace("beta=", r"\beta=")
    print("\nTable 4.12 (tab:bm25_best_config) row:")
    print(
        f"        SILMA 2B & ${tex_cfg}$ & {best['ndcg_cut_10']:.4f} & "
        f"{best['recall_10']:.4f} & {best['recall_100']:.4f} & "
        f"{best['recip_rank']:.4f} & {delta:+.4f} \\\\"
    )


if __name__ == "__main__":
    main()
