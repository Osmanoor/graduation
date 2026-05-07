# pt2 Analysis Notes — 23.1.2026 Part 2

**Source:** `meetings/23.1_2026.pt2.md` (107 lines)
**Speakers:** Mohammed (sharing screen, driving), Osman
**Coverage:** Continuation of **2.7**, then **2.8 → 2.15** (rest of Chapter 2), and **3.1 → 3.3** (start of Chapter 3)
**Duration / scope:** Mid-evening session ending with both tired ("نتم بكرة" — continue tomorrow Friday).

---

## Per-Item Discussion & Decisions

### Item 2.7 (continued from pt1) — Research gap / problem statement framing

**Discussion:**
- They formalised the choice into **two explicit options for the problem statement**:
  - **Option A (general):** "How can query enhancement improve Arabic RAG systems?" — broad, mirrors the original proposal, naturally covers all their experiments (small models, corpus-steered, hybrid, etc.).
  - **Option B (specific):** State the problem as multiple sub-questions tied to each experiment ("how can small models be used for QE in Arabic RAG", "how can corpus-steered approaches be used", etc.).
- Mohammed strongly prefers Option A. Reasoning: the problem statement should fully cover their objectives, not single out one angle. Small models is "part of the implementation, not the main motivation."
- Osman agreed: small models is something extra; the *direction* is QE for Arabic RAG.

**Decision:** **DEFER TO SUPERVISOR** — explicitly take this question to Dr. Tahani: should the problem statement be general (covering all approaches) or specific (singling out small models as the gap)? Their working preference is general.

---

### Item 2.8 — HyDE, Query2Doc, GRF described as the three main LLM-based QE techniques

**Discussion:**
- They feel the QE literature is much broader than just these three. The AI did include other papers across the Foundations / Modern / Arabic subsections, so it's not catastrophically wrong — but the QE *technique families* are not properly enumerated.
- Osman recalled: QE actually has multiple families — query expansion, query rewriting, query decomposition, query abstraction (proposition-based). They had read papers on each during the lit review.
- They located page 28–29 in the draft and confirmed only **query expansion + query rewriting** are mentioned; **decomposition and abstraction are missing** despite having papers for them.

**Decision:** **REVISE** — expand the QE techniques discussion to properly cover all four families they researched (expansion, rewriting, decomposition, abstraction), with the papers they actually read for each. Currently item 2.8 underrepresents the breadth of their lit review.

---

### Item 2.9 — Rewrite-Retrieve-Read positioned as a separate query rewriting category

**Discussion:**
- Brief. They confirmed the AI placed it on page 29. The categorization is fine but is part of the broader gap identified in 2.8 — query rewriting is mentioned but not in the same depth as expansion.

**Decision:** **APPROVE the categorization itself** but treat it as one of the items folded into the 2.8 expansion (rewriting needs to be properly developed alongside expansion, decomposition, abstraction).

---

### Item 2.10 — Arabic challenges section (morphology, diglossia, orthography, diacritics)

**Discussion:**
- The AI assumed Ch.1 framing implicitly — they never actually told it what the framing should be, and it built later chapters on top of that assumption.
- **Format observation (Osman):** the four challenges are written as paragraphs. Could be elevated to subsections (e.g., 2.1.5.1, 2.1.5.2 …). Single-paragraph subsections look thin, so they leaned toward keeping the paragraph form, but they remain undecided.
- **Substantive observation (Osman):** they noted that they researched these Arabic challenges but **don't really thread them through the implementation** — they're informational background, not load-bearing for the methodology. Mohammed's worry: if Dr. Fath (or another examiner) asks them to defend why these challenges are in the thesis or how they affected design, they don't have a strong answer.
- LaTeX side-rant from Mohammed: rendering Arabic in LaTeX caused many errors (hamza issues, parentheses), needed multiple package switches. Logistical, not thesis-content.

**Decision:** **APPROVE the content** of Arabic challenges. **DEFER on format** (paragraphs vs subsections) — minor. **NOTE TO SELVES:** be ready in defense to explain *why* these challenges are in the thesis if they're not directly load-bearing. Possibly tighten the connection later.

---

### Item 2.11 — "Morphological gap" terminology + irrelevant citation

**Discussion (two parts):**

**Part A — the term itself:**
- The AI was upfront that this is its own coinage. Mohammed appreciated the honesty.
- Osman defended the term: it's intuitive, captures the concept well — "بديهي والله" (truly intuitive). He has no problem keeping it.

**Decision (term):** **APPROVE** — keep "morphological gap."

**Part B — the irrelevant inserted citation:**
- They noticed the AI inserted a citation (paper 12) right next to the morphological-gap discussion, claiming "paper 12 has demonstrated that these linguistic properties significantly affect RAG pipeline component selection, with sentence-aware chunking and multilingual embedding models outperforming simple alternatives for Arabic text."
- Mohammed: "this has nothing to do with our work" — the citation is about chunking and embedding-model selection, not about query enhancement or the morphological gap.
- They concluded the AI grabbed an Arabic-NLP paper's result and pasted it in to look supportive, but it doesn't actually support the surrounding text.

**Decision (citation):** **REVISE** — remove the paper-12 sentence (or replace it with a citation that genuinely supports the morphological-gap claim). This is a flag that the AI is inserting decorative citations — they should sweep for similar misuses elsewhere.

---

### Item 2.12 — BM25S parameter inconsistency (k1=1.5, b=0.75 in Ch.2 vs k1=0.9, b=0.4 in Ch.3)

**Discussion:**
- They opened Section 2.3.2 and confirmed the inconsistency exists.
- Hypothesis from Osman: the Ch.2 values are what the BM25S library/reference cites as defaults, while Ch.3 values are what they actually configured. So they may both be "correct" but the Ch.2 phrasing is misleading because it sounds like *their* setup.

**Decision:** **VERIFY then REVISE** — confirm which parameters were actually used in the experiments, then make Ch.2 either (a) say "BM25S default values are k1=1.5, b=0.75 but we used k1=0.9, b=0.4" or (b) just match Ch.3. Don't leave the inconsistency.

---

### Item 2.13 — 15+ papers in Related Work

**Discussion:** Not explicitly discussed; implicitly accepted.

**Decision:** **APPROVE (implicit)** — flag for re-check during the citation audit (item 2.15).

---

### Item 2.14 — Song & Zheng 2024 cited as the QE taxonomy reference

**Discussion (concerning):**
- Mohammed initially suspected the AI hallucinated this paper. They found it exists (arxiv) but: it's a 107-page survey, last revised 2026 (March 3, 2026 version), and **neither of them is confident they actually read it.** Mohammed has a vague visual memory of a figure from it; Osman doesn't recognise it.
- They acknowledge it does cover the right topic (QE survey/taxonomy), so the citation is *plausibly* defensible — but citing a 107-page paper they didn't actually read is academically risky.

**Decision:** **INVESTIGATE then DECIDE** — either: (a) actually read enough of Song & Zheng 2024 to defensibly cite it; or (b) remove the citation and replace with a paper they did read for the taxonomy framing. Flag as homework.

---

### Item 2.15 — BibTeX citation keys may not match References.bib

**Discussion:**
- They both agreed: every citation in the thesis needs to be checked against the actual `References.bib`. URLs need to work. Keys need to exist.
- Mohammed explicitly addressed the AI: "task ليك يا AI" — when you read this transcript, the task is to audit every citation in the thesis, verify the BibTeX keys exist, verify the URLs resolve, and verify the cited paper actually says what the thesis claims it says.

**Decision:** **REVISE — explicit AI task:** full citation audit (existence in `References.bib`, URL validity, key matching, content matching).

---

### Item 3.1 — Ch.3 organized as Dataset/Setup → Baseline → Error Analysis → Query2Doc → Model Comparison

**Discussion:**
- Initially confused: Mohammed asked "where's corpus-steered?" — then realised this item was written before the Phase 4 expansion, so the order describes the original draft only.
- They walked the actual table of contents and confirmed the *current* full order: dataset setup → baseline → error analysis → Query2Doc → model comparisons → parameter tuning → query repetition → hybrid → corpus-steered → per-query analysis.
- Osman noted there's also dataset *information* vs dataset *setup* — these need to be split cleanly. Currently the literature review only really covers MIRACL; the other ~7 datasets they evaluated will go in the Ch.2 dataset analysis section (linked back to item 2.1).

**Decision:** **APPROVE** the structure as it now stands (post-Phase 4). Action: when adding the dataset analysis section to Ch.2, the *other datasets* go there in summary form, *MIRACL* goes there in detail, and Ch.3 dataset section is just the experimental setup.

---

### Item 3.2 — Each methodology section maps 1:1 to a Ch.4 results section

**Discussion:** Brief. Confirmed and approved — every methodology has a corresponding result.

**Decision:** **APPROVE.**

---

### Item 3.3 — mDPR "intentionally selected as a weaker baseline" to maximize headroom

**Discussion (important honesty moment):**
- The AI's framing is that mDPR was a *deliberate* choice for headroom. **Both Mohammed and Osman admitted this is post-hoc.**
- The actual reasons mDPR was chosen, in order:
  1. **Practical:** they needed an existing pre-built MIRACL-compatible index to move fast.
  2. **Concern:** they had genuine worries during selection that it might be too weak — this was a concern, not a deliberate design feature.
- Osman: "the real reason was [practical convenience]; we had concerns it might actually be weak. It wasn't a deliberate choice [for headroom]; it was a worry."
- Mohammed: prefers to either remove the rationale entirely or honestly acknowledge it. "Maybe better not to mention" the headroom framing.

**Decision:** **REVISE** — remove or soften the "intentionally weak baseline" framing. Either:
- (a) Just describe what was used (mDPR pre-trained on MS MARCO, available index) without inventing a strategic rationale; or
- (b) Honestly note: "mDPR was used because a MIRACL-compatible pre-built index was available; we acknowledge the baseline is on the weaker end relative to fine-tuned models."

This decision affects item **5.5** as well (Ch.5 challenges section, where the same framing reappears as "this was intentional"). Apply consistently.

---

## Cross-Cutting Insights & Action Items Raised in pt2

- **Citation-discipline action item:** Full audit of every citation in the thesis (key matching, URL validity, content match). Mohammed explicitly tagged this as an AI task.
- **Decorative-citation pattern detected:** The AI inserted a paper-12 citation that doesn't actually support the surrounding text (item 2.11). This pattern likely exists elsewhere — sweep for similar.
- **Cited-but-unread paper detected:** Song & Zheng 2024 (107 pages) cited but possibly not actually read (item 2.14). This pattern may also exist elsewhere — anything cited as "taxonomy" or "survey" should be sanity-checked.
- **Honesty-over-narrative principle:** Where the AI invented strategic rationales after the fact (mDPR weak baseline = item 3.3, also affects 5.5), the team prefers to soften or remove rather than defend a post-hoc story under examination. Same standard should apply when they encounter similar items later (e.g., framing experimental choices as deliberate when they were actually constraints).
- **Defense readiness gap:** The Arabic challenges section (item 2.10) doesn't connect strongly to their methodology — risk in defense if examiners ask "how did this challenge inform your work?" Note for later.
- **LaTeX/Arabic rendering:** Logistical pain point Mohammed mentioned, not a thesis-content issue. Skipping per the side-topic rule.

---

## Items Touched But Deferred

- **Item 5.5** (Ch.5 challenges, weak baseline framing) — same decision as 3.3 must be applied. Will revisit when Ch.5 is reached.

---

## Items Not Yet Discussed

Continues from item 3.4 onward in pt3.
