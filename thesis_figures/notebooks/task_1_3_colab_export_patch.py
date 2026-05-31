# =====================================================================
# Task 1.3 export patch — per-query metrics, Config A RRF vs Aya-blind
# =====================================================================
# WHERE: paste as a NEW CELL in
#   docs/experiments/phase4_quick_wins_Ablation_erroranalysis.ipynb
#   right AFTER the cell that defines scores_csqe / scores_blind /
#   bm25_scores / shared_qids / deltas  (~line 11732).
#
# WHY Colab: scores_blind comes from aya_blind_bm25_run, which is built by
#   live BM25S retrieval (retrieve_bm25_from_dict) — that needs the index,
#   so this one CSV must be generated in the notebook. Everything downstream
#   (§4.10 re-derivation) is then done locally from the exported CSV.
#
# COLUMNS (per Mohammed's choice): nDCG@10 + Recall@10 + MRR for all three
#   runs, plus the headline nDCG@10 delta (CSQE − blind).
# =====================================================================
import os, shutil
import pandas as pd
import pytrec_eval


def per_query_metrics(run, metrics=('ndcg_cut_10', 'recall_10', 'recip_rank')):
    """{qid: {metric: value}} via pytrec_eval, using the notebook's `qrels`."""
    qrel_dict = {str(qid): {str(d): int(r) for d, r in docs.items()}
                 for qid, docs in qrels.items()}
    ev = pytrec_eval.RelevanceEvaluator(qrel_dict, set(metrics))
    return ev.evaluate(run)


m_csqe  = per_query_metrics(config_a_run)        # Config A RRF (BM25-only-expanded hybrid)
m_blind = per_query_metrics(aya_blind_bm25_run)  # Aya blind BM25 n=1
m_bm25  = per_query_metrics(bm25_run)            # BM25 baseline (no QE)


def g(d, q, k):
    return d.get(q, {}).get(k, 0.0)


rows = []
for q in shared_qids:
    rows.append({
        "qid": q,
        # Config A RRF (BM25-only-expanded hybrid)
        "ndcg10_csqe_hybrid":   g(m_csqe, q, 'ndcg_cut_10'),
        "recall10_csqe_hybrid": g(m_csqe, q, 'recall_10'),
        "mrr_csqe_hybrid":      g(m_csqe, q, 'recip_rank'),
        # Aya blind BM25 n=1 baseline
        "ndcg10_aya_blind_bm25":   g(m_blind, q, 'ndcg_cut_10'),
        "recall10_aya_blind_bm25": g(m_blind, q, 'recall_10'),
        "mrr_aya_blind_bm25":      g(m_blind, q, 'recip_rank'),
        # BM25 baseline (no QE)
        "ndcg10_bm25_baseline":   g(m_bm25, q, 'ndcg_cut_10'),
        "recall10_bm25_baseline": g(m_bm25, q, 'recall_10'),
        "mrr_bm25_baseline":      g(m_bm25, q, 'recip_rank'),
        # headline delta (nDCG@10)
        "delta_ndcg10_csqe_vs_blind":
            g(m_csqe, q, 'ndcg_cut_10') - g(m_blind, q, 'ndcg_cut_10'),
    })

out = pd.DataFrame(rows)
os.makedirs("results", exist_ok=True)
out.to_csv("results/csqe_vs_blind_per_query.csv", index=False)

# persist to Drive so it survives the runtime
dst = ("/content/drive/MyDrive/graduation project/colab_data/"
       "results_phase4/csqe_vs_blind_per_query.csv")
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copy("results/csqe_vs_blind_per_query.csv", dst)

# ---- sanity checks (must match exp_error_analysis_csqe.md) ----
d = out["delta_ndcg10_csqe_vs_blind"]
print("rows:           ", len(out),          "(expect 2896)")
print("mean delta nDCG:", round(d.mean(), 4), "(expect ~+0.1890)")
print("frac delta > 0: ", round((d > 0).mean(), 3),  "(expect ~0.568)")
print("frac delta == 0:", round((d == 0).mean(), 3), "(expect ~0.266)")
print("frac delta < 0: ", round((d < 0).mean(), 3),  "(expect ~0.166)")
print("Config A mean nDCG@10:", round(out['ndcg10_csqe_hybrid'].mean(), 4))
print("Saved -> results/csqe_vs_blind_per_query.csv  and  Drive copy")

try:
    from google.colab import files
    files.download("results/csqe_vs_blind_per_query.csv")
except Exception:
    pass
