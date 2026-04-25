# Supervisor Questions — Collected from Meeting 23 Jan 2026
**Meeting:** Mohammed Elhaj & Osman Bashir — AI Thesis Draft Review (Parts 1–6)
**Date collected:** 2026-04-25
**Target:** Dr. Tahani (next supervision meeting)
**Source doc reviewed:** `research_decisions/THESIS_DRAFT_AI_DECISIONS_REVIEW.md`

> **Scope note:** This file contains only the questions you and Osman *explicitly* flagged for Dr. Tahani during the recorded review (the literal "نسألها / flag for Tahani" moments). Items you discussed and resolved yourselves are tracked elsewhere as internal tasks, not here.

---

## Q1. Problem statement scope — general or specific?
**Where flagged:** Pt1 — *"الحاجة دي من الملخص دا، نطلع بيها طوالي لتهاني"*

The current draft frames the problem around small LLMs (<7B) for Arabic query enhancement, but our experiments cover broader ground (corpus-steered QE, hybrid fusion, model comparison).

The two options we considered:
- **General:** "How can query enhancement improve Arabic RAG retrieval quality?" — covers all our experiments
- **Specific:** "Can small open-source LLMs (<7B) perform effective zero-shot query expansion for Arabic?" — highlights the model-size angle

**Question:** Should the problem statement be general (covering the full direction) or specific to small models? A specific statement may not cover our corpus-steered/hybrid work; a general statement may dilute the contribution.

---

## Q2. Should chapter summaries be included?
**Where flagged:** Pt1 — *"ممكن الحاجة دي نعمل ليها flag إنه هل الـ chapter summary ممكن نخده ولا لأ"*

The AI added a Chapter Summary section (e.g. Section 2.5) with bullet points at the end of each chapter. You did not specifically mention chapter summaries in any prior meeting.

**Question:** Should each chapter end with a bullet-point summary, or is this filler that should be removed?

---

## Q3. Cross-referencing labels — what does the AI's note mean?
**Where flagged:** Pt2 / Pt5 — *"we should flag this clearly for Dr. Tahani"*

The AI's review note says: *"33 cross-references in Chapter 2, 26 in Chapter 3, 29 in Chapter 4 for internal linking."* We could not figure out what this is meant to convey or whether it represents a problem.

**Question:** Is heavy cross-referencing between chapters expected/desired in a thesis? Are unused LaTeX labels acceptable, or should we clean them up?

---

## Q4. Thesis layout — is the chapter-description phrasing acceptable?
**Where flagged:** Pt4 — *"ممكن بس نراجعها مع تهاني، هل الصيغة دي سليمة ولا ما سليمة"*

The thesis layout section currently reads as four paragraphs with no sub-headings: *"Chapter 2 establishes…, Chapter 3 presents…, Chapter 4 reports…, Chapter 5 presents an overall conclusion."*

**Question:** Is this the standard form for the thesis-layout section, or should it be restructured (e.g. with sub-headings, or in a different style)?

---

## Q5. Abstract length — one page or two?
**Where flagged:** Pt5 — *"محتاجين إلا نتأكد من دكتورة تهاني ذاتها.. هل صفحة، ولا صفحتين ولا قدر شنو"*

The current draft abstract is 334 words (within the typical 250–350 range for a master's thesis). You said in an earlier meeting to keep it "short and to the point."

**Question:** What is the maximum acceptable abstract length for this thesis? Half a page, one page, or two pages? And is the dual Arabic + English abstract definitely required by the department?

---

## Q6. Technology-driven vs. problem-driven narrative for Chapter 1
**Where flagged:** Pt4 — *"ممكن تسألها، وممكن يعني نخليها تهبب لينا في الموضوع ده"*

In a previous meeting you said *"you are engineers"* when discussing our approach. Our actual research process was technology-driven — we explored query enhancement techniques to see what works for Arabic, rather than starting from a specific Arabic IR problem.

But Chapter 1 currently presents a problem-driven narrative (Arabic IR challenges → query enhancement as a solution).

**Question:** Should Chapter 1 reflect what we actually did (technology-driven exploration) or be reframed as problem-driven? Is a technology-driven framing academically acceptable for an engineering bachelor's thesis?
