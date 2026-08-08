# How we got to CSQE — the chain of thought

**Purpose:** one place that explains *why* the thesis landed on CSQE, in the order it actually
happened. Written for the defence narrative, so it also flags the places where the honest version
differs from the tidy version.

**Scope:** this is the decision trail only. For the delivery script see
[`F1_narrative_outline.md`](F1_narrative_outline.md); for the worked query see
[`F1_csqe_example.md`](F1_csqe_example.md).

---

## The chain in one line

An expert doesn't answer from memory, he opens the book → so the system should consult the corpus
before it expands → but every method that teaches a system the corpus *structure* needs the corpus
rebuilt → CSQE gets the "opens the book" half at zero indexing cost → and the real win turned out
to be **where** we put it, not the method alone.

---

## Step 1 — The seed: Rashad's consultation

**When:** before 2 Jan 2026 (exact date not recorded)
**File:** [`meetings/Consultation with Mohammed Rashad.md`](../../meetings/Consultation%20with%20Mohammed%20Rashad.md)

Rashad's argument, compressed:

- A RAG system should behave like a **subject-matter expert**, not a generic search engine.
- **The Mufti analogy.** A scholar does not memorise every ruling. He knows the *structure* — a
  question about ablution lives in the Chapter of Purity — and he knows which book to pull off the
  shelf. *"A standard LLM is like a layperson — it tries to answer generatively."*
- **"Map and Retrieve."** Cluster the data, summarise each cluster, let the LLM read the map first
  and decide where to look, then retrieve inside that region.
- **He was explicitly skeptical of RAPTOR** and hierarchical trees — "over-engineered," and likely
  no better than a simpler map for this scope.
- **Prove the delta, not the perfect system.** Baseline vs. enhanced. You don't need to beat Google.

Two things came out of this that survived all the way into the thesis: *the expansion should be
grounded in the corpus*, and *measure the improvement, not the absolute*.

---

## Step 2 — The team argued about it

**Files:** [`meetings/2.1.2026.md`](../../meetings/2.1.2026.md) (raw, lines 85–113) ·
[`meetings/2.1.2026_meeting_outcomes.md`](../../meetings/2.1.2026_meeting_outcomes.md) (cleaned)

The raw transcript is the two of you going back and forth on hierarchical chunking — RAPTOR,
Dense X, propositions, tree structures. The open question was whether to take RAPTOR wholesale and
improve it, or graft query enhancement onto its chunking.

The cleaned outcomes doc settled it for the moment:

> Hierarchical approaches (RAPTOR, etc.) deemed overly complex for our scope.

and recorded Rashad's idea as **"Technique 5: Context Injection — provide the LLM with knowledge
base structure/tree."** That is the first written form of what later became CSQE. It was parked,
not resolved.

**Also fixed here:** MIRACL Arabic as the dataset, hybrid BM25 + dense retrieval, retrieval metrics
only, generation deferred.

---

## Step 3 — It became a formal open question

**File:** [`research_decisions/open_questions.md`](../open_questions.md) §4 · meeting
[`6.1.2026.md`](../../meetings/6.1.2026.md) lines 984–1022

Logged as **"Hierarchical Structures — ⏳ Interesting but Needs Feasibility Study"**, with the
question stated as: *can we implement Rashad's context injection?*

In the 6 Jan meeting Osman put the requirement plainly: *can we inject into the context how the
knowledge base is structured, and then search accordingly?* — and asked for a feasibility study
before anyone wrote code. That study is Step 4.

This is the point worth making in the defence: **the idea was not accepted on authority.** It was
turned into a question and tested.

---

## Step 4 — Breadth-first: map everything

**When:** 28 Mar 2026
**File:** [`research_decisions/phase4_literature_review.md`](../phase4_literature_review.md)

Eight directions, ~25 papers, everything that could plausibly serve the mufti idea:

| | Direction | Representative papers |
|---|---|---|
| A | Corpus-steered query expansion | CSQE, KAR |
| B | Contextual retrieval (document-side) | Anthropic Contextual Retrieval, Late Chunking, CDE |
| C | Structure-aware document retrieval | DAPR, SEAL, MultiDocFusion, heading-aware chunking |
| D | Hierarchical retrieval | **RAPTOR**, LevelRAG |
| E | Knowledge graph + retrieval | KG2RAG, HippoRAG, GraphRAG |
| F | Proposition-level retrieval | Dense X |
| G | Metadata-aware retrieval | Multi-Meta-RAG, BMQExpander |
| H | Query2Doc extensions | RFG, ExpandR, AQE |

Its verdict: *"the mufti analogy finds strong support in the literature"* — and it splits the field
into **query-side** (change the query) vs **document-side** (change the index). Query-side wins on
feasibility because it builds on the Query2Doc pipeline that already existed.

---

## Step 5 — Depth-first: three families, one survivor

**When:** 4 Apr 2026
**File:** [`research_decisions/mufti_approach_deep_research.md`](../mufti_approach_deep_research.md)
← **the decision document**

Three parallel investigations, one per family:

| | Family | Verdict | Killed by |
|---|---|---|---|
| 1 | Query-side ([detail](../family1_corpus_aware_query_expansion_analysis.md)) | ✅ **chosen** | — |
| 2 | Index-side ([detail](../family2_index_metadata_enrichment_analysis.md)) | ❌ rejected | cost of re-indexing 2.1M passages |
| 3 | Retrieval-time ([detail](../family3_structure_guided_miracl_investigation.md)) | ⚠️ possible, weak | small gains for the effort |

**Family 2 is the important one for the defence.** It is where Rashad's "know the structure" half
died, and it died on numbers, not on taste:

| Method | One-time cost | Re-index? | Est. gain |
|---|---|---|---|
| Contextual Retrieval (Anthropic) | $3,000–$20,000 | yes | +3–8% |
| RAPTOR | $216 | yes | +1–4% |
| DAPR title prepending | $23 | yes | +2–5% (−11.6% on one dataset) |
| Late Chunking | $0–$21 | yes | incompatible with mDPR |

And the finding that makes it final:

> All Family 2 approaches are **fundamentally index-time methods**. There is no query-side
> adaptation and no incremental path. You cannot get the benefit without rebuilding the corpus.

RAPTOR at $216 was technically affordable. It was rejected because MIRACL queries are mostly
factoid, and RAPTOR's gains are on multi-hop — i.e. Rashad's own instinct about over-engineering,
now with a number attached.

**Family 3** (Multi-Meta-RAG style filtering) was feasible at $0 but capped at +2–5%, and MIRACL
carries no section headings or categories — only `docid`, `title`, `text`. Not enough structure to
build a map from.

**Family 1 → CSQE** (Lei et al., EACL 2024, arXiv:2402.18031) won on: zero indexing cost, 2–3 days
of work, no external ontology or KG needed (none exist at scale for Arabic), and — the reason it
fits Arabic specifically — CSQE's published advantage is **largest exactly when the LLM lacks
knowledge of the domain** (NovelEval, +21%). Arabic is low-resource for these models. That is the
same situation.

**Checked, not assumed:** [`validation_report_critical_claims.md`](../validation_report_critical_claims.md)
fact-checked seven claims from this research. Four confirmed, two partially, two unverifiable
(WikiExtractor behaviour, HippoRAG/GraphRAG infeasibility). Worth knowing which parts of the
argument rest on softer ground.

---

## Step 6 — Build it, then find the real result

**Files:** [`csqe_implementation_plan.md`](../csqe_implementation_plan.md) ·
[`csqe_parameter_verification.md`](../csqe_parameter_verification.md) ·
[`exp_error_analysis_csqe.md`](../../arabic-rag-query-enhancement/docs/experiments/exp_error_analysis_csqe.md)

Final config: Aya Expanse 8B, k=5 first pass, **2 corpus + 2 blind** samples, α=4 repetition,
temp 1.0, 128 tokens per doc.

Results, against the canonical baselines:

| System | nDCG@10 |
|---|---|
| BM25 alone | 0.4621 |
| Aya blind QE on BM25 (β=2) | 0.5855 |
| **CSQE on BM25** (exp_013) | **0.6157** |
| Hybrid RRF, no QE at all | 0.6267 |
| **CSQE on BM25 only + raw dense, RRF** (exp 2.1) | **0.7137** |

**The ablation matters** — CSQE is not purely corpus-grounded, and the mix beats either half:
corpus-only 0.5381, blind-only 0.5752, **2+2 mix 0.6157**.

**And the actual contribution was placement.** Applying the expansion to *both* retrievers made
things worse. Same fusion (RRF), only the placement changes:

| Expansion applied to | nDCG@10 |
|---|---|
| **Word-matcher (BM25) only** | **0.7137** |
| Both | 0.6936 |
| Meaning-matcher (dense) only | 0.6474 |

---

## Say it this way (the 90-second version)

> Our supervisor's consultant gave us an analogy: a scholar doesn't answer from memory, he opens
> the book. We tried to build that. We surveyed eight directions and about twenty-five papers, and
> we found the analogy has two halves. The first half — *teach the system the structure of the
> library* — every method that does it requires rebuilding the index over two million passages,
> from twenty-three dollars to twenty thousand, with no incremental path and no validation in
> Arabic. We ruled that out on cost and risk, and we documented the cost. The second half —
> *consult the corpus before you answer* — costs one extra retrieval pass and nothing else. That
> is CSQE, and that is what we built. Then we found something the literature hadn't reported: it
> matters enormously *which* retriever you give the expansion to. Word-matching only: 0.7137.
> Both: 0.6936. That asymmetry is our contribution.

---

## Honesty guards

These are the places where the tidy story and the true story differ. Volunteer them; don't get
caught on them.

**1. We took half the analogy.** Rashad's Mufti knows *which chapter to open*. Ours only *opens the
book instead of guessing*. The structure-awareness half was never implemented. If Rashad or anyone
from that meeting is in the room, say "we took one half of your analogy, and here is the cost table
that killed the other half" — that's a stronger answer than hoping nobody notices.
*(Same as trap #5 in the narrative outline.)*

**2. The research doc over-predicted.** `mufti_approach_deep_research.md` estimated CSQE would reach
**0.74–0.80** and set minimum success at *"beat the hybrid baseline, 0.6267."* CSQE on BM25 came in
at **0.6157** — narrowly *below* that bar. The method alone did not clear its own success criterion.
The 0.7137 came from CSQE **plus** the placement finding. Do not let a slide imply CSQE alone got
there.

**3. The novelty claim has been narrowed since.** The April research said "first LLM-based
corpus-aware QE for Arabic." [`WS6_RESEARCH_REPORT.md`](../WS6_RESEARCH_REPORT.md) later found
**Exp4Fuse** (Liu et al., ACL 2025 Findings), which applies QE to a single sparse retriever and
fuses — the closest prior art, and it must be cited. Also **Macmillan-Scott et al. (2025)**, doing
Arabic QE with a <7B model, though cross-lingual rather than monolingual MIRACL. The claim survives
only when narrowed to *monolingual MSA Arabic, dense–sparse hybrid*. Say the narrow version.

**4. RAPTOR was rejected on scope, not on quality.** It's a good method. It costs $216 and helps
multi-hop questions; MIRACL is mostly factoid. If asked "why not RAPTOR," that is the answer — not
"it's too complex."

---

## File index

**Origin**
- [`meetings/Consultation with Mohammed Rashad.md`](../../meetings/Consultation%20with%20Mohammed%20Rashad.md) — the Mufti analogy, Map-and-Retrieve, RAPTOR skepticism
- [`meetings/2.1.2026.md`](../../meetings/2.1.2026.md) — raw hierarchical-chunking debate (lines 85–113)
- [`meetings/2.1.2026_meeting_outcomes.md`](../../meetings/2.1.2026_meeting_outcomes.md) — "Technique 5: Context Injection"; §8 Rashad insights
- [`meetings/6.1.2026.md`](../../meetings/6.1.2026.md) — feasibility study requested (lines 984–1022)
- [`research_decisions/open_questions.md`](../open_questions.md) §4 — logged as an open question

**Research**
- [`phase4_literature_review.md`](../phase4_literature_review.md) — 8 directions, ~25 papers
- [`mufti_approach_deep_research.md`](../mufti_approach_deep_research.md) — **the decision doc**
- [`family1_corpus_aware_query_expansion_analysis.md`](../family1_corpus_aware_query_expansion_analysis.md) — CSQE, KAR, BMQExpander
- [`family2_index_metadata_enrichment_analysis.md`](../family2_index_metadata_enrichment_analysis.md) — **the cost table that killed structure-awareness**
- [`family3_structure_guided_miracl_investigation.md`](../family3_structure_guided_miracl_investigation.md) — MIRACL metadata audit
- [`validation_report_critical_claims.md`](../validation_report_critical_claims.md) — fact-check of the above
- [`WS6_RESEARCH_REPORT.md`](../WS6_RESEARCH_REPORT.md) — later narrowing of the novelty claim

**Build and results**
- [`csqe_implementation_plan.md`](../csqe_implementation_plan.md) · [`csqe_parameter_verification.md`](../csqe_parameter_verification.md)
- [`exp_error_analysis_csqe.md`](../../arabic-rag-query-enhancement/docs/experiments/exp_error_analysis_csqe.md)

**Defence**
- [`F1_narrative_outline.md`](F1_narrative_outline.md) — Act 8 is this story, scripted
- [`F1_csqe_example.md`](F1_csqe_example.md) — the الأسماء الخمسة worked example
