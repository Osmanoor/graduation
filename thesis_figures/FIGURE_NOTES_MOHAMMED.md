# Figure Review Notes — Mohammed → Elhaj

These are my notes from going through `thesis_figures/REVIEW.html`. Grouped by the
type of change so we can quickly decide per item: **edit**, **drop**, **add**, or
**discuss**. Nothing here is final — flag anything you disagree with.

---

## 1. New figures / additions to consider

- **Fig 2.1 (RAG architecture) — add a companion diagram.**
  We should have a figure in the same style as Fig 2.1 that shows **where the QE
  layer fits** inside the RAG pipeline. Right now 2.1 shows the generic
  query → retriever → LLM → answer flow; we need one that marks the QE layer's
  position explicitly.

- **Fig 3.1 (End-to-end pipeline) — just rename, no new figure needed.**
  We already have the full CSQE pipeline as **Fig 3.8**, so there's no need to
  create a second end-to-end diagram. Instead, **rename Fig 3.1** to frame it as
  the *first / baseline* thesis pipeline, and treat **Fig 3.8 (CSQE) as the
  *final* end-to-end pipeline** — the one that gives our best result. So this is a
  labeling/framing change only.

---

## 2. Edits to existing figures

- **Fig 2.2 (QE taxonomy) — move the in-image label to the caption.**
  Delete the **"built on in this thesis"** text that sits *inside* the image
  (the dashed-box annotation) and put that note in the **caption** instead.

- **Fig 3.8 (CSQE pipeline, three-stage) — redesign, it's messy.**
  The current version is cluttered and the three stages aren't clear. This is an
  important figure (it's our main method) so it needs a cleaner, more readable
  layout.

- **All diagram figures — general styling pass.**
  Every system/diagram figure should be tidied up and made **more visually
  organized, and probably more colorful**. Consistent style across all of them.

---

## 3. Figures to discuss — "do we actually need this?"

Open the question for each; arguing to cut:

- **Fig 2.2** — Query Enhancement taxonomy. (See also the caption edit above — but
  do we keep the figure at all?)
- **Fig 3.2** — MIRACL dataset structure.
- **Fig 3.3** — BM25S indexing flow.
- **Fig 3.4** — mDPR encoding flow.
- **Fig 3.6** — BM25 query repetition mechanism. (Leaning toward dropping this one.)
- **Fig 3.7** — Hybrid fusion: CC and RRF.

- **Fig 4.2 (Failure cliff, 34%) vs Fig 4.1.**
  Isn't Fig 4.2 basically showing the **same thing as Fig 4.1**? They feel
  redundant (especially against the 4.1 CDF variant). Decide whether we need both.

---

## 4. Variation preferences (overriding / confirming the ★★★ picks)

- **Fig 4.3 (NDCG by query length).**
  I think **v2 is nicer** (review recommends v1).

- **Fig 4.5 (Sorted NDCG across 10 LLMs).**
  We can **include both v1 and v3** rather than picking one.

- **Fig 4.9 (Hybrid CC α sweep, no QE).**
  **v2 is better — more informative** (review recommends v1).

---

## 5. Data / source check-ins

- **Fig 4.4 (Recall@k curve, k=1…100).**
  Do we actually **have the data to plot this**? Need to confirm before finalizing.

- **Chapter 4.3 / Table 4.2 / Fig 4.5 (Model comparison, Dense).**
  For the full Osman model results, check
  `arabic-rag-query-enhancement/docs/OSMAN_MODEL_COMPARISON_RESULTS.md`.
  This should let us fill in the missing R@10 / R@100 / MRR for Osman's 5 models
  (currently blocking Fig 4.5 v3 and parts of Table 4.2).

---

## 6. Questions to prepare for (the doctor may ask)

- **Fig 4.10 (CSQE α repetition sweep).**
  If α = 1 through 4 give essentially the **same result**, why did we choose
  **α = 4 instead of α = 1**? We need a clear justification ready — the examiner
  will likely ask this.
