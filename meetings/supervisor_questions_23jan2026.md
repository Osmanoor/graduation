# Supervisor Questions — Collected from Meeting 23 Jan 2026
**Meeting:** Mohammed Elhaj & Osman Bashir — AI Thesis Draft Review (Parts 1–6)
**Date collected:** 2026-04-25
**Target:** Dr. Tahani (next supervision meeting)
**Source doc reviewed:** `research_decisions/THESIS_DRAFT_AI_DECISIONS_REVIEW.md`

---

## 1. Problem Statement & Research Framing

### Q1. What scope should the problem statement have?
**Background:** The current draft frames the problem around small LLMs (<7B parameters) for Arabic query enhancement. But our actual work covers broader ground: general query expansion, corpus-steered QE, hybrid fusion, and model comparison across many models.

**The two options we identified:**
- **General:** "How can query enhancement improve Arabic RAG retrieval quality?" (covers all our experiments)
- **Specific:** "Can small open-source LLMs (<7B) perform effective zero-shot query expansion for Arabic?" (highlights the model-size angle as the central contribution)

**Our concern:** A specific statement around small models may not fully cover our corpus-steered and hybrid experiments. A general statement may be too broad.

**Question for Dr. Tahani:** Which scope is more appropriate for a thesis at this stage? Is the small-model angle strong enough as a central research question, or should we frame it as a broader investigation of query enhancement for Arabic?

---

### Q2. Research gap validity — small models claim
**Background:** The AI draft states: *"None of these studies tested models smaller than 7 billion parameters for zero-shot query expansion on Arabic text"* as the central research gap.

**Our concern (raised explicitly in the meeting):** This may not hold anymore — new papers may have been published since our literature survey. Osman noted that even if it holds, the claim may be too strong (implying we are the first ever, which requires a very thorough literature check).

**Question for Dr. Tahani:** Is this gap claim scientifically defensible for a bachelor's thesis? Do we need to do a fresh literature search before the final submission to validate this claim? And if a paper has been published covering this gap, how do we adjust the framing?

---

### Q3. Technology-driven vs. problem-driven narrative for Chapter 1
**Background:** In a previous meeting (17 March), Dr. Tahani said: *"You are engineers"* when discussing our approach. Our actual research process was technology-driven — we explored query enhancement techniques to see what works for Arabic, rather than starting from a specific problem statement.

**Our concern:** Chapter 1's introduction currently frames the work as problem-driven (Arabic IR challenges → query enhancement as a solution). But the real narrative was: we explored query enhancement techniques and validated them on Arabic.

**Question for Dr. Tahani:** Should Chapter 1 present a technology-driven narrative (exploring what works) or a problem-driven narrative (solving Arabic IR challenges)? Which framing is more appropriate for this thesis, and is our technology-driven approach acceptable in academic writing?

---

## 2. Chapter Structure Questions

### Q4. Should chapter summaries be included?
**Background:** The AI included a summary section (Section 2.5) with bullet points at the end of Chapter 2. Dr. Tahani did not specifically mention chapter summaries in any meeting.

**Question for Dr. Tahani:** Should each chapter end with a bullet-point summary, or should chapter summaries be omitted entirely? What is the department's expectation?

---

### Q5. Chapter 2 — should a dedicated dataset analysis section be added?
**Background:** Osman raised that Chapter 2 does not include the dataset comparison work we did (we compared ~8 datasets and selected MIRACL). This research happened as Task 1.x and was well-documented, but the AI skipped it.

**Question for Dr. Tahani:** Should Chapter 2 include a section on dataset selection methodology (comparing candidate datasets and justifying the choice of MIRACL Arabic)? Or is a brief mention in Chapter 3 sufficient?

---

### Q6. Should the query enhancement techniques section be expanded?
**Background:** Section 2.8 currently covers only HyDE, Query2Doc, and GRF as the main LLM-based QE techniques. The meeting identified that query rewriting (Rewrite-Retrieve-Read), query decomposition, and query abstraction techniques are missing — we have papers on these.

**Question for Dr. Tahani:** Should the literature review cover a broader taxonomy of query enhancement (expansion, rewriting, decomposition, abstraction), or is focusing on the three expansion-focused techniques sufficient for the scope of this thesis?

---

## 3. Abstract Questions

### Q7. Abstract length — how long is acceptable?
**Background:** The current draft abstract is 334 words, which falls within the typical 250–350 word range for master's theses. Dr. Tahani said to keep it "short and to the point."

**Question for Dr. Tahani:** Is 334 words acceptable for a bachelor's thesis abstract? Should we target under 300 words? Is one page the maximum, and should it be closer to half a page?

---

### Q8. Abstract final claim — "practical" vs "promising"
**Background:** The abstract concludes with: *"...establishing LLM-based query enhancement as a practical strategy for Arabic RAG systems."* The AI itself noted this may be overconfident since our experiments are benchmark-level, not production deployments.

**Question for Dr. Tahani:** Is the word "practical" appropriate given we only evaluated on a benchmark (MIRACL), not a deployed system? Should we soften this to "promising strategy" or "viable approach"?

---

## 4. Methodology & Claims Questions

### Q9. BM25 parameter inconsistency — which values were used?
**Background:** Section 2.3.2 states BM25S default parameters k1=1.5, b=0.75. Chapter 3 states our configured values k1=0.9, b=0.4. These are inconsistent.

**Internal resolution:** Chapter 3 values (k1=0.9, b=0.4) are the actual values used in experiments. The Ch.2 values describe the library defaults, not our configuration.

**Question for Dr. Tahani:** Is it acceptable to describe library defaults in Chapter 2 and configured values in Chapter 3, as long as this is clearly stated? Or should we only mention the values we actually used throughout?

---

### Q10. Hypothesis framing concern in Chapter 3
**Background:** Chapter 3 (Methodology) states upfront the hypothesis: *"BM25 benefits from vocabulary breadth in expanded queries, while the dense encoder degrades on long input queries."* But this was a post-hoc interpretation after seeing the results — we did not pre-register this hypothesis before running the experiments.

**Our concern (raised in the meeting):** An examiner could ask: *"How did you know dense retrieval would degrade before you ran the experiment?"*

**Question for Dr. Tahani:** Should we remove the hypothesis framing from Chapter 3 methodology and instead present it as a finding in Chapter 4 results? Or is it acceptable to state hypotheses in methodology even if they were derived post-hoc, as long as the language is softened (e.g., "we investigated whether...")?

---

## 5. Results & Novelty Claims

### Q11. Second-order research gap — asymmetric QE on hybrid retrieval
**Background:** Chapter 4 claims a new research gap: *"The combination of corpus-steered query expansion with asymmetric hybrid fusion (applying QE only to BM25, not dense) has not been studied."* The AI flagged this as requiring verification — it may not be true for the general case (non-Arabic), only for Arabic.

**Question for Dr. Tahani:** Is it scientifically acceptable to claim this as a novel contribution for Arabic, even if similar work exists in English? Do we need to perform a literature search specifically for this combination before making this claim in the thesis?

---

### Q12. Dropped models — include or exclude from thesis?
**Background:** GPT-OSS-20B was attempted but dropped before completing (resource limitations and hallucination issues). ALLaM-7B was run but gave severely degraded results (-48.9% NDCG). Both are currently mentioned in the thesis draft.

**Question for Dr. Tahani:** Should dropped/failed models be discussed in the thesis, and if so, how? Is it scientifically valid to report that GPT-OSS was "dropped due to resource constraints" without reporting results, or does this create a selection bias concern?

---

## 6. Citation & Reference Questions

### Q13. Song & Zheng (2024) taxonomy paper — is it peer-reviewed?
**Background:** The AI cited "Song & Zheng (2024)" as the taxonomy reference for query enhancement categories. During the meeting we noticed this paper is on arXiv (submitted March 2024) and we are not certain if it is peer-reviewed.

**Question for Dr. Tahani:** Is it acceptable to cite an arXiv preprint as the main taxonomy framework, or should we find a peer-reviewed equivalent?

---

### Q14. All citation keys must be verified
**Internal task flagged in meeting:** All BibTeX citation keys in the thesis must be cross-checked against the actual `References.bib` file to ensure they exist and match. This is a technical task we will resolve internally.

*(No supervisor input needed — listed here for completeness as a tracked action item.)*

---

## Summary Table

| # | Question | Priority | Chapter Affected |
|---|----------|----------|-----------------|
| Q1 | Problem statement scope (general vs. small models specific) | **High** | Ch.1, Ch.2 abstract, Ch.5 |
| Q2 | Research gap claim validity (small models, need literature check?) | **High** | Ch.2, Ch.1 |
| Q3 | Technology-driven vs. problem-driven narrative | **High** | Ch.1 |
| Q4 | Should chapter summaries be included? | Medium | All chapters |
| Q5 | Add dataset selection section to Ch.2? | Medium | Ch.2 |
| Q6 | Expand QE techniques coverage (rewriting, decomposition)? | Medium | Ch.2 |
| Q7 | Abstract length limit (334 words ok?) | Medium | Abstract |
| Q8 | "Practical" vs "promising" in abstract conclusion | Low | Abstract |
| Q9 | BM25 parameter inconsistency (Ch.2 defaults vs Ch.3 configured) | Low | Ch.2, Ch.3 |
| Q10 | Hypothesis framing — move from Ch.3 to Ch.4? | **High** | Ch.3, Ch.4 |
| Q11 | Second-order gap claim — asymmetric QE on hybrid (needs lit search?) | **High** | Ch.4 |
| Q12 | Dropped models — include or exclude? | Medium | Ch.3, Ch.4 |
| Q13 | Song & Zheng (2024) — peer-reviewed or preprint? | Low | Ch.2 |
| Q14 | Verify all citation keys (internal task) | Low | All |
