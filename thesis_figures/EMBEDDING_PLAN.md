# Figure & Table Embedding Plan

For Mohammed (or anyone embedding figures into chapter `.tex` files). For each figure or table:

- **Where** — the target chapter + section
- **Snippet** — exact LaTeX block to paste, ready to use
- **Cross-reference suggestion** — one example sentence that cites the figure in body text

## Prerequisites

- `1-main.tex` already includes `\graphicspath{{Figures/}{../thesis_figures/output/pdf/}{../thesis_figures/system_diagrams/}}` so figure filenames resolve without a path prefix.
- Tables are LaTeX `tabular` snippets in `output/pdf/table_X_Y.tex` — `\input{}` them inside a `\begin{table}...\end{table}` wrapper.
- Compile a visual preview anytime with `xelatex thesis_figures/preview_all_figures.tex` — it shows every figure/table at thesis width with the caption + label + xref the embedding produces.

## Conventions (Dr. Tahani's writing guide)
- **Figures:** caption BELOW; "As shown in Figure~\ref{fig:foo}…" (capital F)
- **Tables:** caption ABOVE; same `\ref` style with capital T
- Width: `0.85\textwidth` for most data figures; `0.95\textwidth` for wide grouped/multi-line; `0.6\textwidth` for donut/single-panel
- All blocks wrapped in `[H]` (use `\usepackage{float}` — already loaded)

---

# Chapter 2

## Figure 2.1 — RAG system architecture · §2.1
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_2_1_rag_arch.pdf}
  \caption{High-level architecture of a Retrieval-Augmented Generation (RAG)
  system. A user query is sent to a retriever that consults the corpus and
  returns the top-$k$ passages, which are passed alongside the query to an LLM
  to produce a context-augmented answer.}
  \label{fig:rag_arch}
\end{figure}
```
*xref:* "The Retrieval-Augmented Generation framework (Figure~\ref{fig:rag_arch}) couples a retriever with a generator; the query enhancement layer studied in this thesis sits between the user query and the retriever."

## Table 2.1 — Reviewed QE papers · §2.4
```latex
\begin{table}[H]
  \centering
  \caption{Query-enhancement papers reviewed for this thesis.}
  \label{tab:reviewed_qe}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_2_1.tex}
\end{table}
```
*xref:* "Table~\ref{tab:reviewed_qe} summarises the query-enhancement literature, grouped by whether the technique is lexical or LLM-based generative."

## Table 2.2 — LLM models used · §2.5
```latex
\begin{table}[H]
  \centering
  \caption{Open-source LLMs evaluated for Arabic query enhancement, ordered by parameter count.}
  \label{tab:models_used}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_2_2.tex}
\end{table}
```
*xref:* "The eleven models in Table~\ref{tab:models_used} span 2--20 B parameters, with multilingual generalists (Qwen, Gemma, Aya) alongside Arabic-specialised models (SILMA, Falcon-H1, Jais-2, ALLaM)."

---

# Chapter 3

## Figure 3.1 — End-to-end pipeline · §3.1
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_3_1_pipeline.pdf}
  \caption{The thesis evaluation pipeline. A user query passes through the
  query-enhancement layer; BM25S and mDPR retrieve independently; their ranked
  lists are fused (CC or RRF) and the top-$k$ passages are scored against the
  MIRACL Arabic dev qrels.}
  \label{fig:pipeline}
\end{figure}
```
*xref:* "Figure~\ref{fig:pipeline} shows the overall evaluation pipeline used throughout this thesis."

## Figure 3.3 — BM25S indexing · §3.4
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.65\textwidth]{fig_3_3_bm25s.pdf}
  \caption{BM25S indexing pipeline applied to the MIRACL Arabic corpus.
  Passages are tokenised with PyStemmer, stopword-removed using 245 Arabic
  stopwords, then indexed under BM25S with $k_1{=}0.9$ and $b{=}0.4$.}
  \label{fig:bm25s_indexing}
\end{figure}
```
*xref:* "The sparse retrieval pipeline (Figure~\ref{fig:bm25s_indexing}) uses BM25S with Arabic-aware tokenisation."

## Figure 3.4 — mDPR encoding · §3.5
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.7\textwidth]{fig_3_4_mdpr.pdf}
  \caption{Dense retrieval pipeline using multilingual DPR. Queries are
  encoded in batches on a single A100 GPU under FP16; the resulting
  768-dimensional vectors are searched against a pre-built FAISS index.}
  \label{fig:mdpr_encoding}
\end{figure}
```
*xref:* "Dense retrieval (Figure~\ref{fig:mdpr_encoding}) is implemented via the multilingual DPR encoder applied to the pre-built MIRACL FAISS index."

## Figure 3.5 — Query2Doc generation · §3.6
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_3_5_query2doc.pdf}
  \caption{Query2Doc generation: the original query is wrapped in a fixed
  prompt template; an open-source LLM generates a short pseudo-document;
  the pseudo-document is concatenated with the query before retrieval.}
  \label{fig:query2doc}
\end{figure}
```
*xref:* "The Query2Doc pipeline (Figure~\ref{fig:query2doc}) follows the original Wang et al.\ (2023) formulation, with the LLM and generation parameters varied per experiment."

## Figure 3.7 — Hybrid fusion: CC and RRF · §3.7
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_3_7_hybrid.pdf}
  \caption{Two retriever-fusion methods evaluated in this thesis. Convex
  Combination (left) computes a weighted sum of normalised retrieval scores;
  Reciprocal Rank Fusion (right) sums the reciprocal of each retriever's rank.}
  \label{fig:hybrid_fusion}
\end{figure}
```
*xref:* "Two complementary fusion strategies (Figure~\ref{fig:hybrid_fusion}) are evaluated: CC requires score normalisation, while RRF is parameter-light and operates on ranks alone."

## Figure 3.8 — CSQE pipeline · §3.8
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_3_8_csqe.pdf}
  \caption{Corpus-Steered Query Expansion (CSQE) pipeline. Stage 1: BM25
  retrieves a first-pass top-$k_1$ context. Stage 2: corpus context plus the
  original query are fed to the Aya LLM, which generates a corpus-grounded
  pseudo-document. Stage 3: the query (repeated $\alpha$ times) is concatenated
  with the pseudo-document and fed to a BM25 second pass.}
  \label{fig:csqe_pipeline}
\end{figure}
```
*xref:* "The corpus-steered variant (Figure~\ref{fig:csqe_pipeline}) replaces the blind LLM expansion of Figure~\ref{fig:query2doc} with one grounded in the corpus, mitigating the entity-hallucination failures observed in the blind setting."

## Figure 3.9 — Best system architecture · §3.8.3 / §4.7
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_3_9_best_system.pdf}
  \caption{Architecture of the thesis's best-performing system. CSQE-expanded
  queries are fed to BM25 while the original short queries are fed to mDPR;
  the two ranked lists are fused with Reciprocal Rank Fusion ($k=20$), yielding
  the headline nDCG@10 of 0.714.}
  \label{fig:best_system}
\end{figure}
```
*xref:* "The best-performing configuration (Figure~\ref{fig:best_system}) applies expansion asymmetrically: only the sparse retriever receives the CSQE-grounded query."

## Table 3.1 — Per-model hardware config · §3.6
```latex
\begin{table}[H]
  \centering
  \caption{Hardware and precision configuration used for each LLM evaluated.}
  \label{tab:hardware_config}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_3_1.tex}
\end{table}
```
*xref:* "All experiments ran on a single A100 40\,GB GPU under the configurations listed in Table~\ref{tab:hardware_config}."

## Table 3.2 — Per-model generation hyperparams · §3.6
```latex
\begin{table}[H]
  \centering
  \caption{Pseudo-document generation hyperparameters per model.}
  \label{tab:gen_hyperparams}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_3_2.tex}
\end{table}
```
*xref:* "Generation hyperparameters per model are summarised in Table~\ref{tab:gen_hyperparams}."

---

# Chapter 4

## Table 4.1 — Baselines · §4.1
```latex
\begin{table}[H]
  \centering
  \caption{Baseline retrieval performance on the MIRACL Arabic dev set (2,896 queries).}
  \label{tab:baselines}
  \input{../thesis_figures/output/pdf/table_4_1.tex}
\end{table}
```
*xref:* "As Table~\ref{tab:baselines} shows, mDPR and BM25 are complementary."

## Figure 4.1 — Per-query nDCG@10 distribution · §4.1
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_1_ndcg_hist_v1.pdf}
  \caption{Per-query nDCG@10 distribution for the two baseline retrievers on
  the MIRACL Arabic dev set. Both exhibit a bimodal distribution: a large
  mass near zero and another near one, with relatively few in the middle.}
  \label{fig:per_query_dist}
\end{figure}
```
*xref:* "Both baselines exhibit a sharply bimodal per-query distribution (Figure~\ref{fig:per_query_dist})."

## Figure 4.2 — Failure cliff · §4.2.1
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_2_failure_cliff_v1.pdf}
  \caption{Cumulative distribution of per-query nDCG@10 on the mDPR baseline.
  The marked threshold at 0.3 separates 33.9\% of queries on which the
  baseline performs poorly from the remainder.}
  \label{fig:failure_cliff}
\end{figure}
```
*xref:* "Figure~\ref{fig:failure_cliff} reveals that 33.9\% of queries fall below an nDCG@10 of 0.3 — the failure cliff that motivates query enhancement."

## Figure 4.3 — nDCG@10 by query length · §4.2.2  (Osman: prefer v2)
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_3_length_violin_v2.pdf}
  \caption{Distribution of mDPR nDCG@10 within each query-length bucket
  (1--3 / 4--8 / 9+ words). Short queries achieve the lowest mean nDCG@10
  (0.345) while medium queries achieve the highest (0.511); the relationship
  is non-monotonic.}
  \label{fig:length_dist}
\end{figure}
```
*xref:* "The per-bucket distribution (Figure~\ref{fig:length_dist}) shows that short queries are clearly the weakest bucket, but the relationship is non-monotonic."

## Figure 4.4 — Recall@k curve · §4.2.3
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_4_recall_curve.pdf}
  \caption{Mean Recall@$k$ for mDPR and BM25 on the MIRACL Arabic dev set,
  $k$ on a log axis. Approximately 10\% of relevant passages remain
  unrecovered even at depth 100, indicating a recall ceiling for the
  baselines.}
  \label{fig:recall_curve}
\end{figure}
```
*xref:* "The recall ceiling visible in Figure~\ref{fig:recall_curve} — roughly 10\% of relevant passages unrecovered even at depth 100 — motivates hybrid retrieval and corpus-steered expansion."

## Table 4.2 — Dense models · §4.3
```latex
\begin{table}[H]
  \centering
  \caption{Query2Doc dense-retrieval results across ten LLMs, ordered by nDCG@10.}
  \label{tab:dense_models}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_4_2.tex}
\end{table}
```

## Figure 4.5 — Dense bar across models · §4.3  (Osman: include both v1 + v3)
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_4_5_models_bar_v1.pdf}
  \caption{nDCG@10 of each evaluated LLM on the Query2Doc dense pipeline,
  sorted descending. The dashed reference line marks the mDPR baseline
  (0.499); each model uses its consistent thesis colour, identical to
  Figure~\ref{fig:repetition_sweep}.}
  \label{fig:models_bar}
\end{figure}

\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_4_5_models_grouped_v3.pdf}
  \caption{Grouped per-model bars for nDCG@10, Recall@10 and MRR on the
  Query2Doc dense pipeline.}
  \label{fig:models_grouped}
\end{figure}
```
*xref:* "Figure~\ref{fig:models_bar} ranks the ten models by nDCG@10 on the Query2Doc dense pipeline; the grouped variant (Figure~\ref{fig:models_grouped}) shows the same ranking holds for Recall@10 and MRR."

## Figure 4.6 — Model size vs gain · §4.3
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_6_size_v2_labelled.pdf}
  \caption{Relationship between model parameter count (billions) and gain over
  the mDPR baseline. A weak positive trend is visible across the full set, and
  the Qwen-family subset corroborates the size-quality correlation within a
  single architecture.}
  \label{fig:size_vs_gain}
\end{figure}
```
*xref:* "Figure~\ref{fig:size_vs_gain} shows a positive but weak association between model parameter count and Query2Doc gain over the baseline."

## Table 4.3 — BM25 best configs · §4.4 / §4.6
```latex
\begin{table}[H]
  \centering
  \caption{Best BM25 query-repetition configuration per model.}
  \label{tab:bm25_best}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_4_3.tex}
\end{table}
```

## Figure 4.7 — BM25 repetition sweep · §4.6
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_4_7_repetition_v1.pdf}
  \caption{nDCG@10 on the BM25 retriever as a function of query-repetition
  count $n$ for each LLM-generated pseudo-document. Six of nine models start
  below the BM25 baseline at $n{=}1$; all nine recover or exceed it at their
  optimum $n$. Colours match Figure~\ref{fig:models_bar}.}
  \label{fig:repetition_sweep}
\end{figure}
```
*xref:* "The repetition sweep (Figure~\ref{fig:repetition_sweep}) shows that six of nine models initially degrade BM25 at $n{=}1$, but all nine recover at an appropriate repetition count."

## Figure 4.8 — Dense vs BM25 gains · §4.4 / §4.6
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_8_gains_v1.pdf}
  \caption{Per-model Query2Doc gain on the Dense retriever versus the BM25
  retriever. Only Aya Expanse 8B and Jais-2 8B sit in the both-positive
  quadrant; most other models help Dense but degrade BM25 at $n{=}1$.}
  \label{fig:dense_vs_bm25_gains}
\end{figure}
```
*xref:* "Figure~\ref{fig:dense_vs_bm25_gains} reveals an asymmetry: only the two strongest models help both retrievers at $n{=}1$."

## Table 4.4 — Hybrid baselines · §4.7
```latex
\begin{table}[H]
  \centering
  \caption{Hybrid retrieval baselines without query enhancement.}
  \label{tab:hybrid_baselines}
  \input{../thesis_figures/output/pdf/table_4_4.tex}
\end{table}
```

## Figure 4.9 — Hybrid CC α sweep · §4.7  (Osman: prefer v2)
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_4_9_alpha_sweep_v2_all.pdf}
  \caption{Convex-combination $\alpha$ sweep for the no-QE hybrid baseline,
  showing nDCG@10, Recall@\{10,100\} and MRR. nDCG@10 peaks near $\alpha = 0.5$.}
  \label{fig:hybrid_alpha}
\end{figure}
```
*xref:* "Sweeping the CC weight (Figure~\ref{fig:hybrid_alpha}) reveals the no-QE optimum at $\alpha = 0.5$."

## Table 4.5 — CSQE ablation · §4.8
```latex
\begin{table}[H]
  \centering
  \caption{Ablation of the CSQE pseudo-document.}
  \label{tab:csqe_ablation}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_4_5.tex}
\end{table}
```

## Table 4.6 — CSQE vs blind QE · §4.8
```latex
\begin{table}[H]
  \centering
  \caption{Comparison of CSQE against blind Query2Doc using Aya Expanse 8B as the generator.}
  \label{tab:csqe_vs_blind}
  \input{../thesis_figures/output/pdf/table_4_6.tex}
\end{table}
```

## Table 4.7 — Configurations A/B/C · §4.9
```latex
\begin{table}[H]
  \centering
  \caption{Performance of the three retriever-assignment configurations across CC and RRF fusion.}
  \label{tab:configs_abc}
  \scriptsize
  \input{../thesis_figures/output/pdf/table_4_7.tex}
\end{table}
```

## Figure 4.11 — System progression · §4.9 (HEADLINE)
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.95\textwidth]{fig_4_11_progression_v2_annot.pdf}
  \caption{Progression of nDCG@10 from the BM25 baseline (0.462) through
  intermediate query-enhancement steps to the best system,
  BM25-only-expanded with RRF fusion, at 0.714. Annotations on each bar
  report the gain over the best previous configuration.}
  \label{fig:progression}
\end{figure}
```
*xref:* "Figure~\ref{fig:progression} traces the cumulative gain from the BM25 baseline to the best system, showing a +0.087 nDCG@10 lift over the strongest no-QE hybrid."

## Figure 4.12 — Per-query Δ histogram · §4.10
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_12_delta_hist_v1.pdf}
  \caption{Distribution of the per-query difference between the CSQE+Hybrid
  system and the Aya-blind BM25 baseline. Shaded bands mark the Big Win
  region ($\Delta > 0.3$) and the Regression region ($\Delta < -0.1$);
  56.8\% of queries improve, 16.6\% regress.}
  \label{fig:delta_dist}
\end{figure}
```
*xref:* "The per-query difference distribution (Figure~\ref{fig:delta_dist}) shows that 56.8\% of queries improve under CSQE+Hybrid versus Aya-blind, with a mean improvement of +0.189 nDCG@10."

## Figure 4.13 — NDCG by first-pass relevance · §4.10  (Osman: prefer v2)
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_13_firstpass_v2_annot.pdf}
  \caption{CSQE+Hybrid versus Aya-blind baseline conditioned on whether the
  BM25 first-pass top-1 document is relevant (qrel $\ge$ 1). When the
  first-pass document is relevant ($n = 1{,}061$) CSQE+Hybrid reaches 0.888;
  when it is not ($n = 1{,}835$) it reaches 0.581.}
  \label{fig:first_pass}
\end{figure}
```
*xref:* "Figure~\ref{fig:first_pass} reveals that first-pass quality is the largest behavioural modulator of CSQE: when BM25's top-1 is already relevant, CSQE+Hybrid reaches 0.888 nDCG@10 versus 0.581 otherwise."

## Figure 4.14 — Δ by query length, grouped · §4.10
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{fig_4_14_lengthgain_v2_grouped.pdf}
  \caption{Per-bucket comparison of Aya-blind BM25 and CSQE+Hybrid using the
  1--3 / 4--8 / 9+ word buckets. CSQE+Hybrid improves every bucket; short
  queries gain the most proportionally (+43.6\%) and medium queries the most
  absolutely (+0.197).}
  \label{fig:length_gain}
\end{figure}
```
*xref:* "Figure~\ref{fig:length_gain} confirms that CSQE+Hybrid lifts every length bucket, with the largest proportional gain on short queries (+43.6\%)."

## Figure 4.15 — Regression types · §4.10
```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.6\textwidth]{fig_4_15_regtype_v2_donut.pdf}
  \caption{Type breakdown of the 367 queries that regress under CSQE+Hybrid
  ($\Delta < -0.1$). Type A (strong-BM25-hurt-by-expansion) accounts for
  52\%, Type B (poisoned first-pass) for 36\%, and Type C (other) for 12\%.}
  \label{fig:regression_types}
\end{figure}
```
*xref:* "Of the 367 regressing queries (Figure~\ref{fig:regression_types}), Type A — strong BM25 results diluted by the expansion — accounts for the majority."

---

# Not embedded (per registry decisions)
- **Fig 4.10** (CSQE α sweep) — cut from thesis per recommendation; replace with one sentence in §4.8: *"Varying $\alpha$ from 1 to 4 changed nDCG@10 by less than 0.002; $\alpha = 4$ was used throughout."*
- **Fig 2.2 / 2.3 / 3.2 / 3.6** — archived per Osman's review; sources in `archive/system_diagrams_dropped/`.

# Pending
- **Fig 2.1 companion** (per Osman §1) — new figure needed showing where the QE layer sits inside the RAG pipeline. Same visual style as Fig 2.1. Plan: design in TikZ once §2.1 prose is settled, so the figure follows the claim.
- **Fig 3.3 / 3.4 / 3.7 joint decision** — Osman flagged these for discussion (keep vs cut). Currently embedded; ready to remove if you decide to cut.
- **WS6.4 BibTeX fixes** — 10 entries need to be corrected before any `\cite{}` to those keys is trusted. See `research_decisions/WS6_RESEARCH_REPORT.md` appendix.
