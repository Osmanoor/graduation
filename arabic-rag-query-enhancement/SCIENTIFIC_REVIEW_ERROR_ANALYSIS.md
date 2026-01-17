Scientific Review: Arabic RAG Error Analysis
Date: January 17, 2026 Reviewer: Antigravity (Agentic AI) Subject: Error Analysis Methodology & Results for Experiment 001 Status: ✅ APPROVED (Based on Quantitative Evidence Only)

Executive Summary
The error analysis for Experiment 001 has been reviewed. To ensure scientific rigor, we strictly distinguish between Statistically Validated Findings (derived from the full $N=2896$ dataset) and Qualitative Hypotheses (derived from small samples).

Critical Decision: The choice of Query Expansion is authorized based solely on the quantitative evidence (Item 2.1 below). The qualitative counts are treated as non-binding observations.

1. Statistically Validated Findings ($N=2896$)
The following facts are derived from the entire validation distribution and form the only scientific basis for our architectural decisions:

High Failure Rate: 39% of all queries ($1,130/2,896$) failed to achieve effective ranking (NDCG@10 < 0.3). This confirms the need for intervention.
Short Query Performance Gap: Short queries (1-3 tokens) consistently underperform, achieving only ~59% of the ranking quality of long queries (9+ tokens).
Significance: This is a dataset-wide trend. It scientifically proves that lack of information/context is a primary driver of failure.
Retrieval-Ranking Gap: High Recall@100 (~84%) vs. Low NDCG@10 (~50%) indicates the Retriever finds documents but ranks them poorly, often due to term mismatch or lack of semantic signal in the query.
2. Qualitative Observations ($N=20$) - Hypothesis Only
Disclaimer: These observations are derived from a sample of 20 queries (~0.7% of failures). They are statistically insignificant and are NOT used to quantify error distribution.

Observation: We observed instances of spelling errors (e.g., Hamza variations) and Named Entity mismatches in the sample.
Scientific Status: These are Hypotheses, not facts. We hypothesize that fixing spelling may help, but we do not base our ROI calculation on the "40%" figure observed in the sample.
3. Justification for Query Expansion
We approve Query Expansion based on the Quantitative Evidence (1.2):

Problem: The data proves that shortness correlates with failure. Short queries lack the semantic signal to match relevant documents in the dense space.
Solution: Query Expansion (specifically Query2doc style) systematically addresses this by injecting additional terms and context, directly countering the "information poverty" of short queries.
Role of Normalization: Included as a low-cost "hygiene" step to address the hypothesized spelling issues, without banking on specific failure rates.
4. Recommendations for Future Validation
To scientifically validate the failure distribution (i.e., "How many queries actually fail due to spelling?"), we recommend the following Future Work (not blocking current implementation):

LLM-as-a-Judge: Use an LLM to categorize a statistically significant sample ($N \ge 385$ for 95% CI with 5% margin) of failed queries.
Automated Taxonomy: Systematically tag all 1,130 failed queries for "Shortness" (deterministic) vs "Spelling" (requires LLM judge).
Conclusion
Proceed with Query Expansion because the Quantitative Data proves that short/low-context queries are the primary bottleneck. Do not rely on the "40% spelling" metric for your thesis claims; rely on the "Short vs Long" performance gap.