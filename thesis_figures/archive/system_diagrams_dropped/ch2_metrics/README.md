# Dropped — Fig 2.6, the three retrieval metrics on one worked example

**Dropped 2026-08-09, same day it was built, on Elhaj's review:**
> "figure 2.6: it is not intuitive at all and i didn't understand them, ignore this fig, delete it."

The figure showed one ranked list of ten results with three relevant hits at ranks 2, 5 and 9,
the `1/log2(i+1)` discount under each rank, the DCG/IDCG arithmetic, and the three resulting
metric values (Recall@10 = 0.75, MRR = 0.50, NDCG@10 = 0.5148).

**Why it failed.** It tried to teach three metrics at once by making the reader follow the
arithmetic. Too much simultaneous detail — the discount row, the two sums and the three verdict
boxes competed instead of building on each other. §2.2.4's equations now stand alone, as they
did before.

**If this is ever revisited,** do one metric per figure, or show only the rank-discount curve
without the arithmetic. Do not reinstate this version as it is.

The generator (`gen_fig_2_6_metrics.py`) computes every printed value with assertions, so the
numbers were correct — the problem was the design, not the data.
