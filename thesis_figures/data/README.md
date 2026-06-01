# Data folder

## raw/
Inputs as pulled — never modified by hand. Re-generate with `notebooks/00_pull_drive_data.ipynb`.

Provenance for each file is in `../data_manifest.yaml`.

## computed/
Derivatives produced by `notebooks/01_compute_per_query.ipynb`:

| File | Produced from | Schema |
|------|---------------|--------|
| `per_query_baseline_dense.csv` | `raw/baseline_dense_run.txt` + `raw/miracl_qrels_dev.json` | qid, ndcg10, recall10, mrr |
| `per_query_baseline_bm25.csv` | `raw/baseline_bm25_run.txt` + qrels | qid, ndcg10, recall10, mrr |
| `per_query_csqe_bm25.csv` | `raw/bm25_csqe_run.txt` + qrels | qid, ndcg10, recall10, mrr |
| `per_query_csqe_hybrid_rrf.csv` | `raw/hybrid_csqe_rrf_k20.txt` + qrels | qid, ndcg10, recall10, mrr |
| `query_lengths.csv` | `raw/miracl_topics_dev.json` | qid, query, word_count, length_bin |
| `csqe_vs_blind_delta.csv` | per-query CSQE - per-query Aya-blind | qid, csqe_ndcg, blind_ndcg, delta, query_length, length_bin |

All CSVs use UTF-8, comma-separated, header row, no index column.
